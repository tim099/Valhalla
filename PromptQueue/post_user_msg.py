#!/usr/bin/env python3
"""post_user_msg.py — T44: 把 Tim (使用者) 的訊息自動 post 進酒館。

Usage:
    # 從 stdin 讀 message body 並 post 進 tavern (預設 sender=Tim)
    echo "task 3 Token 開始實作" | python AgentCommands/PromptQueue/post_user_msg.py

    # 從 --body 直接傳訊息
    python AgentCommands/PromptQueue/post_user_msg.py --body "task 5 Token 開工"

    # 指定 sender / room / category
    python AgentCommands/PromptQueue/post_user_msg.py --body "..." --sender Tim --room tavern --category meta

行為：
1. 接受 message body (從 --body 或 stdin)
2. 走 run_cmd.py spawn op=post 把訊息寫進 tavern messages
3. Cmd_Tavern.Op_Post 結尾 hook 自動處理：
   - work_post auto-credit (如果 routing target IsWorkChannel)
   - token_parse auto-credit (從 body parse N token，限白名單 sender)
4. fail swallow + log warning（不擋呼叫者主流程）

整合 Claude Code UserPromptSubmit hook（.claude/settings.json）：
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "python ${CLAUDE_PROJECT_DIR}/AgentCommands/PromptQueue/post_user_msg.py"
        }]
      }
    ]
  }
}
```
hook 走 stdin 接收 prompt content（Claude Code 規格）→ 自動 post 進 tavern 並結算。

注意：
- 本 script 不自律 join Tim identity；首次 Op_Post 寫 Tim 訊息會 LogWarning 但仍寫進 messages
- 只在 Claude Code 端有效；Antigravity / Gemini session 沒有 UserPromptSubmit hook 等價物
- agent 也可手動 invoke（譬如本小姐自律每次 turn 開頭呼叫一次）
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
# T-PATH-02: 派遣對象走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
# ⛔ 原本這裡有 `_RUN_CMD = _tp.RUN_CMD_PATH` —— 2026-09-04 移除（TASK-0107）。
#   派遣改走 `_tp.senate_exe()`，而且是**在要用的那一刻**解析（見 post_to_tavern）：
#   模組級解析會讓「找不到 senate」在 import 時就炸，而這支是 daemon 路徑上的工具。

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _read_body(args) -> str:
    """從 --body / stdin / Claude Code hook stdin JSON 三層 fallback 讀 message body."""
    if args.body:
        return args.body

    # 嘗試讀 stdin（可能是純 text 或 Claude Code hook JSON）
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if not raw:
            return ""
        # Claude Code UserPromptSubmit hook 走 stdin JSON 格式：{"prompt": "...", "session_id": ..., ...}
        if raw.startswith("{"):
            try:
                payload = json.loads(raw)
                return payload.get("prompt", "") or payload.get("message", "") or ""
            except Exception:
                pass   # 不是 JSON 就當純 text
        return raw
    return ""


def post_to_tavern(body: str, sender: str, room: str, category: str) -> int:
    """派 `Tavern op=post` — 不等握手，fire-and-forget。

    回 exit code（0 = 成功，非 0 = 派遣端失敗，但對 caller 來說都 swallow 不擋主流程）

    ── 2026-09-04（TASK-0107）：`python run_cmd.py` → `senate ucmd run`。
    順帶拿掉舊 argv 裡的 `--arg wait-reply=0`。**理由是它描述了一個不存在的行為，不是它慢。**

    量到的（讀數）：
      · `wait-reply` 是 **`run_cmd.py` 的旗標（`--wait-reply`）**，不是 Cmd 的參數。
        `Cmd_Tavern` 的 code 裡沒有任何地方讀這個 arg；帶著它照樣 Success（不會被擋）
        ⇒ **那一行從來沒有作用過。**
      · `senate ucmd run` 沒有 `--wait-reply` 這個旗標（help 裡 "wait" 出現 **0** 次）。

    🩸 **而我差一點在這裡寫下一個假的改善**：我從 `run_cmd.py` 的 help 讀到
       「Tavern op=post 預設等 20 秒」，就要寫成「每發一則都白等 20 秒」。
       跑了對照組才發現 —— **舊寫法實測 2.2s、新寫法 3.2s**（新的還略慢，那是 senate 的啟動成本）。
       ⇒ 那個「20 秒」是我**讀 code 讀來的預設值**，不是這條路上真的發生的事。
       📌 教訓：**拿一個從 code 讀出來的預設值，去描述一個沒量過的行為 —— 那是猜，不是讀數。**
    """
    if not body or not body.strip():
        print("[post_user_msg] empty body, skip", file=sys.stderr)
        return 0   # 空訊息 — 不 fail 不寫，靜默退出

    try:
        _senate = _tp.senate_exe()
    except Exception as e:
        # ⛔ 不退回 run_cmd.py：靜默 fallback 會讓這次轉接等於沒發生。
        print(f"[post_user_msg] 找不到 Senate CLI，訊息**沒有送出**：{e}", file=sys.stderr)
        return 1

    cmd = [
        str(_senate), "ucmd", "run", "Tavern",
        # 🩸 順手修掉：舊寫法不帶 lane 旗標 ⇒ 落 `queues/anonymous/`，跟所有漏帶的人擠同一條。
        #    這筆是 **daemon 代 user 發**，不是某個 persona 派的 ⇒ `system` lane。
        #    ⚠ lane 不宣告身分 —— 發文者身分走下面的 `sender` 參數，語意不變。
        "--persona", "system",
        "--arg", "op=post",
        "--arg", f"room={room}",
        "--arg", f"sender={sender}",
        "--arg", f"body={body}",
    ]
    if category:
        cmd += ["--arg", f"meta=category:{category}"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        if result.returncode == 0:
            print(f"[post_user_msg] posted as {sender} → {room} ({len(body)} chars, category={category or '(unset)'})")
            return 0
        print(f"[post_user_msg] post fail rc={result.returncode}: {result.stderr.strip()[:200]}", file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"[post_user_msg] spawn fail: {e}", file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--body", default=None, help="Message body (overrides stdin)")
    parser.add_argument("--sender", default="Tim", help="Sender identity (default Tim)")
    parser.add_argument("--room", default="tavern", help="Room id (default 'tavern')")
    parser.add_argument("--category", default="", help="meta.category value (default empty = routes to work-channel default fallback)")
    args = parser.parse_args(argv)

    body = _read_body(args)
    return post_to_tavern(body, args.sender, args.room, args.category)


if __name__ == "__main__":
    sys.exit(main())
