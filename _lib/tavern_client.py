"""TavernClient — Python SDK wrapper for run_cmd.py op=Tavern.

設計目標：強制 Python daemon **不再自己 spawn subprocess 拼 args / 不再直接寫 jsonl**，
所有 tavern 寫操作（post / task_*） 走本 SDK。對應 T36.4 + T37 之後的 P0 鐵律：
- daemon 直寫 jsonl → 繞過 Cmd_Tavern 7 道機制 (atomic seq / utf-8 / T26 pacing /
  R7 mention parser / presence / tavern-keeper / events.jsonl 連動) → data corruption
- daemon 拼錯 subprocess args → 同樣繞過

API 統一封裝：post_message / task_create / task_claim / task_done / task_progress / etc.

Example:
    from AgentCommands._lib.tavern_client import TavernClient
    client = TavernClient()
    result = client.post_message(
        room="tavern", sender="my-bot", body="hello",
        meta={"tag": "smoke-test"}, wait_reply=0,
    )
    if result.ok:
        print(f"posted to {result.last_op_md}")
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import tavern_paths as _tp


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class TavernOpResult:
    """Result wrapper from run_cmd.py op=Tavern."""
    ok: bool                                    # True if subprocess returncode == 0
    op: str                                     # 跑的 op (post / task_done / etc.)
    returncode: int                             # 原 subprocess returncode
    stdout: str = ""                            # 原 subprocess stdout
    stderr: str = ""                            # 原 subprocess stderr
    last_op_md: str = ""                        # _last_op.md 內容（成功 / 失敗訊息結構化在內）
    error: str | None = None                    # 高層錯誤摘要（subprocess timeout / exception）


# ---------------------------------------------------------------------------
# TavernClient
# ---------------------------------------------------------------------------

# 找 run_cmd.py 路徑 — 從 repo root 推
_RUN_CMD_PATH = _tp.REPO_ROOT / "CardGame" / "Assets" / "UCL" / "UCL_Core" / "Tools~" / "AgentCommands" / "run_cmd.py"


class TavernClient:
    """Python SDK for Cmd_Tavern op-dispatch — daemon 必走，禁直寫 jsonl.

    Lifecycle: 建一次 instance per daemon；多次呼叫 post_message / task_* 共用 subprocess pipeline。
    Subprocess timeout：預設 60s（含 T26 alter-pacing 30s+ delay）；--wait-reply 大時需 caller 自加。
    """

    def __init__(
        self,
        run_cmd_path: Path | None = None,
        python_executable: str | None = None,
        default_timeout: float = 60.0,
    ):
        self.run_cmd_path = run_cmd_path or _RUN_CMD_PATH
        self.python = python_executable or sys.executable
        self.default_timeout = default_timeout

    # ---------- Internal: low-level op dispatch ----------

    def _run_op(
        self,
        op: str,
        args: dict[str, Any],
        *,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """Spawn run_cmd.py run Tavern --arg op=X --arg key=val ... 共通入口."""
        if not self.run_cmd_path.is_file():
            return TavernOpResult(
                ok=False, op=op, returncode=-1,
                error=f"run_cmd.py not found at {self.run_cmd_path}",
            )

        cmd = [self.python, str(self.run_cmd_path), "run", "Tavern", "--arg", f"op={op}"]
        for k, v in args.items():
            if v is None:
                continue
            cmd.append("--arg")
            cmd.append(f"{k}={v}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout or self.default_timeout,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return TavernOpResult(
                ok=False, op=op, returncode=-1,
                error=f"subprocess timeout after {timeout or self.default_timeout}s",
            )
        except Exception as e:
            return TavernOpResult(
                ok=False, op=op, returncode=-1,
                error=f"{type(e).__name__}: {e}",
            )

        last_op_md = ""
        try:
            if _tp.LAST_OP_PATH.is_file():
                last_op_md = _tp.LAST_OP_PATH.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

        return TavernOpResult(
            ok=result.returncode == 0,
            op=op,
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            last_op_md=last_op_md,
        )

    # ---------- Helper: meta dict → "k1:v1;k2:v2" string format Cmd_Tavern 慣例 ----------

    @staticmethod
    def _meta_to_string(meta: dict[str, Any] | str | None) -> str | None:
        """Cmd_Tavern.cs ParseMeta 接受 'k1:v1;k2:v2' string 格式（看 line 861）."""
        if meta is None:
            return None
        if isinstance(meta, str):
            return meta
        if isinstance(meta, dict):
            return ";".join(f"{k}:{v}" for k, v in meta.items() if v is not None)
        return str(meta)

    # ---------- Public API: chat ops ----------

    def post_message(
        self,
        room: str,
        sender: str,
        body: str,
        *,
        persona: str | None = None,
        meta: dict[str, Any] | str | None = None,
        refs: str | None = None,
        reply_to: int | None = None,
        wait_reply: int = 0,
        alter_pacing_bypass: bool = False,
        timeout: float | None = None,
        session_token: str | None = None,
    ) -> TavernOpResult:
        """op=post — 發訊息進指定房（走 Cmd_Tavern 7 道機制：atomic seq / utf-8 / R7 mention parser / etc.）.

        session_token (T07): 開 token enforce 後 Cmd_Tavern.Op_Post 必驗 token；caller 帶進來即透傳。
        None / "" → 不附加（enforce OFF 路徑或 caller 顯式選「不帶 token」）.
        """
        meta_str = self._meta_to_string(meta) or ""
        # alter_pacing_bypass=True → meta 自動加 alter-pacing-bypass:true
        if alter_pacing_bypass:
            meta_str = (meta_str + ";" if meta_str else "") + "alter-pacing-bypass:true"

        args = {
            "room": room,
            "sender": sender,
            "persona": persona,
            "body": body,
            "meta": meta_str if meta_str else None,
            "refs": refs,
            "reply_to": str(reply_to) if reply_to is not None else None,
            "wait-reply": str(wait_reply),
            "session_token": session_token if session_token else None,
        }
        # Long wait-reply 自動拉長 timeout
        eff_timeout = timeout
        if eff_timeout is None and wait_reply > 0:
            eff_timeout = wait_reply + 30.0   # +30s buffer
        return self._run_op("post", args, timeout=eff_timeout)

    def read(
        self,
        room: str,
        *,
        since_seq: int = 0,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=read — 讀房內訊息 since seq."""
        return self._run_op("read", {
            "room": room,
            "since_seq": str(since_seq),
        }, timeout=timeout)

    # ---------- Public API: task lifecycle ops ----------

    def task_create(
        self,
        room: str,
        task_id: str,
        title: str,
        *,
        actor: str | None = None,
        role: str | None = None,
        priority: str = "normal",
        depends_on: list[str] | str | None = None,
        suggested_owner: str | None = None,
        group_id: str | None = None,
        body: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=task_create — 建 task。group_id 屬於 T37 Quest Group 機制."""
        if isinstance(depends_on, list):
            depends_on = ",".join(depends_on)
        return self._run_op("task_create", {
            "room": room,
            "task_id": task_id,
            "title": title,
            "actor": actor,
            "role": role,
            "priority": priority,
            "depends_on": depends_on,
            "suggested_owner": suggested_owner,
            "group_id": group_id,
            "body": body,
            "idempotency_key": idempotency_key,
        }, timeout=timeout)

    def task_claim(
        self,
        room: str,
        task_id: str,
        claimer: str,
        *,
        plan: str | None = None,
        lease_hours: int | None = None,
        lease_seconds: int | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=task_claim — 認領 task 取得 lease."""
        return self._run_op("task_claim", {
            "room": room,
            "task_id": task_id,
            "claimer": claimer,
            "plan": plan,
            "lease_hours": str(lease_hours) if lease_hours is not None else None,
            "lease_seconds": str(lease_seconds) if lease_seconds is not None else None,
            "idempotency_key": idempotency_key,
        }, timeout=timeout)

    def task_progress(
        self,
        room: str,
        task_id: str,
        actor: str,
        summary: str,
        *,
        artifacts: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=task_progress — 進度更新 + lease 自動展期."""
        return self._run_op("task_progress", {
            "room": room,
            "task_id": task_id,
            "actor": actor,
            "summary": summary,
            "artifacts": artifacts,
            "idempotency_key": idempotency_key,
        }, timeout=timeout)

    def task_done(
        self,
        room: str,
        task_id: str,
        actor: str,
        *,
        summary: str | None = None,
        share: bool = False,
        share_room: str = "tavern",
        share_body: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=task_done — 完成 task。T37 share 參數 → 額外發 friendly 同事分享進 share_room."""
        return self._run_op("task_done", {
            "room": room,
            "task_id": task_id,
            "actor": actor,
            "summary": summary,
            "share": "true" if share else "false",
            "share_room": share_room,
            "share_body": share_body,
            "idempotency_key": idempotency_key,
        }, timeout=timeout)

    def task_release(
        self,
        room: str,
        task_id: str,
        actor: str,
        reason: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TavernOpResult:
        """op=task_release — 主動放棄 task."""
        return self._run_op("task_release", {
            "room": room,
            "task_id": task_id,
            "actor": actor,
            "reason": reason,
            "idempotency_key": idempotency_key,
        }, timeout=timeout)

    # ---------- Public API: presence ops ----------

    def get_presence(self, *, timeout: float | None = None) -> TavernOpResult:
        """op=get_presence — 印 presence dashboard."""
        return self._run_op("get_presence", {}, timeout=timeout)

    def set_focus(self, sender: str, focus: str, *, timeout: float | None = None) -> TavernOpResult:
        """op=set_focus — 顯式 set 自己的 focus 欄位."""
        return self._run_op("set_focus", {"sender": sender, "focus": focus}, timeout=timeout)

    def set_mood(self, sender: str, mood: str, *, timeout: float | None = None) -> TavernOpResult:
        """op=set_mood — 顯式 set 自己的 mood 欄位."""
        return self._run_op("set_mood", {"sender": sender, "mood": mood}, timeout=timeout)

    # ---------- Public API: inbox ----------

    def inbox_read(self, room: str, agent_id: str, *, timeout: float | None = None) -> TavernOpResult:
        """op=inbox_read — 讀指定 agent 在指定房的 inbox."""
        return self._run_op("inbox_read", {
            "room": room,
            "agent_id": agent_id,
        }, timeout=timeout)


# ---------------------------------------------------------------------------
# Convenience module-level singleton
# ---------------------------------------------------------------------------

_default_client: TavernClient | None = None


def default_client() -> TavernClient:
    """Get or lazy-create module-level default TavernClient instance."""
    global _default_client
    if _default_client is None:
        _default_client = TavernClient()
    return _default_client


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # cp950 console 編碼防 emoji UnicodeEncodeError（per messages_dedupe 慣例）
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    # smoke：跑 op=read tavern since_seq=0 看 _last_op.md
    c = default_client()
    res = c.read("tavern", since_seq=0)
    print(f"ok={res.ok} returncode={res.returncode}")
    if res.error:
        print(f"error: {res.error}")
    print(f"stdout (first 200 chars): {res.stdout[:200]}")
    print(f"last_op_md (first 200 chars): {res.last_op_md[:200]}")
