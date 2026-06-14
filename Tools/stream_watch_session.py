#!/usr/bin/env python3
"""
stream_watch_session.py — 直播連續觀看模式 (Stream Watch Mode) CLI

# 區塊職責：把「陪 Tim 看 ScreenStream 直播」做成有 end-time 的自我 pace loop session,
#          鏡像 waiter_session.py 的 start/cycle/end + 薪資結算骨架, 但事件改成「觀戰評論」。
# 物理意義：daemon (RCG_ScreenStreamDaemon, EOV 專屬) 每秒寫 frame 進 600 槽 ring buffer;
#          本 session 是「agent 端 loop 框架」, 每 cycle 給出「上次 cursor」+ montage 指令提示 →
#          agent 跑 screenstream_montage.py make --after-mtime <cursor> 把「上次到現在」壓成一張縮圖牆 →
#          Read 該圖 → 寫觀戰評論 post 進 tavern (Discord mirror 回給 Tim 手機) →
#          跑 record_observation --next-cursor <epoch> 推進 cursor (保證下輪 0-gap 接續)。
# 數值影響：base 1 token/min (陪伴性質, 同 waiter) + 每筆 observation +2 token; 到 end-time 自動結算下班。

設計依據:
  - 觀看 workflow 心智模型 = 有界 ring-buffer producer-consumer (basecamp 2026-06-06 設計)
  - frame→montage 引擎: AgentCommands/Tools/screenstream_montage.py (--after-mtime/--max-tiles/next-cursor)
  - session 骨架鏡像: UCL_Core/Tools~/AgentCommands/waiter_session.py
  - end-time 機制鏡像: remote_work_session.py (2026-05-18 Tim 重構成 --end-time HH:mm)

CLI 子命令:
  start    — 開新 watch session, 寫 state, 走 tavern-keeper 開播陪看 announcement
  cycle    — agent loop tick: 回 elapsed/remaining/expired + 當前 cursor + montage 指令提示
  record_observation — agent 發完觀戰評論後跑, 推進 cursor (--next-cursor) + 計 bonus
  end      — 結束 session, 結算 salary, 走 tavern-keeper 收播 announcement
  status   — 列單一 session JSON
  list     — 列當前 active watch sessions

依賴: UCL_Core work_session.py 的 utility helpers (consumer→library 方向, 合法)
"""

from __future__ import annotations
import argparse
import datetime
import json
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 區塊職責：把 UCL_Core 的 AgentCommands tools 目錄塞進 sys.path, 才能 import work_session helpers。
# 物理意義：本檔是 EOV-local (AgentCommands/Tools/), 但 reuse 跨專案共用的 work_session utility;
#          consumer (EOV) 依賴 library (UCL_Core) 是合法方向 (反過來才違反 CLAUDE.md §4)。
# 數值影響：路徑算錯 → import 失敗 fail-fast, 代表環境壞了, 不該 silent 跑下去。
_HERE = Path(__file__).resolve().parent                 # <repo>/AgentCommands/Tools
_REPO_ROOT_LOCAL = _HERE.parent.parent                  # <repo>
_UCL_AGENTCMD = _REPO_ROOT_LOCAL / "CardGame" / "Assets" / "UCL" / "UCL_Core" / "Tools~" / "AgentCommands"
sys.path.insert(0, str(_UCL_AGENTCMD))

from work_session import (  # noqa: E402
    utcnow_iso,
    parse_iso,
    short_uuid,
    atomic_write_json,
    tavern_post,
    fire_salary_credit,
    resolve_persona,
    infer_caller_persona,
    _REPO_ROOT,
)

# 區塊職責：本 module 自有 state 檔, 跟 waiter/work session 完全分開避免混淆
_SESSIONS_PATH = _REPO_ROOT / "AgentCommands" / "ChatTavern" / "stream_watch_sessions.json"
_AUDIT_DIR = _REPO_ROOT / "AgentCommands" / "ChatTavern" / "stream_watch_session_audit"

# 區塊職責：montage 工具相對路徑 (cycle 指令提示用)
_MONTAGE_TOOL = "python AgentCommands/Tools/screenstream_montage.py"


def _tavern_current_seq(room: str = "tavern") -> int:
    """讀 rooms/<room>/_seq.txt 取當前最新 seq (T-StreamWatch-TavernSync 已讀游標初值用)。

    開播時把已讀游標設為「此刻最新 seq」→ 第一輪 cycle 只看開播後新進的酒館訊息
    (跟 frame cursor=now 同語意, 不撈開播前的舊對話)。讀不到 → 回 -1 (全收)。
    """
    seq_path = _REPO_ROOT / "AgentCommands" / "ChatTavern" / "rooms" / room / "_seq.txt"
    try:
        return int(seq_path.read_text(encoding="utf-8").strip())
    except Exception:
        return -1

# 區塊職責：薪資 / bonus 常數
# 物理意義：BASE 1 token/min — 陪看是被動陪伴性質, 同 waiter; OBSERVATION_BONUS 2 token/筆
#          鼓勵真寫觀戰評論而非掛機。
# 數值影響：看 60min 沒評論 = 60 base; 每寫 1 筆觀戰 +2。
BASE_RATE_PER_MIN = 1
OBSERVATION_BONUS = 2
DEFAULT_DURATION_MIN = 30
DEFAULT_MAX_TILES = 12


# ===========================================================================
# State I/O
# ===========================================================================


def _default_state() -> dict:
    return {
        "_schema_version": 1,
        "_description": "Stream watch session (直播連續觀看模式) active + history.",
        "_canonical_doc": ".claude/skills/valor-stream-watch/SKILL.md",
        "active_sessions": [],
        "history": [],
    }


def load_state() -> dict:
    if not _SESSIONS_PATH.exists():
        return _default_state()
    try:
        return json.loads(_SESSIONS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return _default_state()


def save_state(state: dict) -> None:
    atomic_write_json(_SESSIONS_PATH, state)


def find_active(state: dict, session_id: str) -> dict | None:
    for s in state.get("active_sessions", []):
        if s["id"] == session_id:
            return s
    return None


def find_active_primary(state: dict, session_id: str | None = None) -> dict | None:
    """Find a primary mode session.

    # 區塊職責：companion mode 加入既有 primary session 用; 給 SID 就精確找, 否則挑最新的 active primary.
    # 物理意義：同樂會場景下 companion 不必每次手動查 session_id, 自動接最近一場 primary 開的觀影.
    # 數值影響：找不到 → return None (caller 該 fail-fast 報「沒 active primary, 自己先開一場」).
    """
    primaries = [s for s in state.get("active_sessions", [])
                 if s.get("mode", "primary") == "primary"]
    if session_id:
        for s in primaries:
            if s["id"] == session_id:
                return s
        return None
    if not primaries:
        return None
    # 挑最近 started_at (lex 比 ISO 即可)
    primaries.sort(key=lambda s: s.get("started_at", ""), reverse=True)
    return primaries[0]


def list_companions(state: dict, primary_id: str) -> list[dict]:
    """列出 attach 到指定 primary 的 companion sessions."""
    return [s for s in state.get("active_sessions", [])
            if s.get("mode") == "companion" and s.get("parent_session_id") == primary_id]


def append_audit(session_id: str, event: str, payload: dict) -> None:
    """Append audit event to stream-watch-scoped jsonl (跟其他 session audit 完全分流)."""
    _AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    log_path = _AUDIT_DIR / f"{session_id}.jsonl"
    entry = {"ts": utcnow_iso(), "event": event, **payload}
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"⚠ audit log fail ({log_path.name}): {e}", file=sys.stderr)


# ===========================================================================
# end-time 解析 (鏡像 remote_work_session 2026-05-18)
# ===========================================================================


def _compute_ends_at(end_time_str: str, duration_min: int):
    """把 --end-time HH:mm (local) 或 --duration 分鐘 解析成 (ends_at_utc_iso, duration_sec, end_local_hhmm)。

    # 區塊職責：把「看到 12:30」這種 local 時間目標換算成 UTC ends_at + 時長。
    # 物理意義：Tim 講的是 local 牆鐘時間; 內部 timestamp 全走 UTC (對齊 work_session helpers)。
    #          故先在 local 算「現在到目標」的時長, 再把時長套到 UTC now, 避開 tz 轉換 bug。
    # 數值影響：end-time 若已過今天該時刻 → wrap 到明天 (跨午夜場景); 與 --duration 互斥。
    """
    now_local = datetime.datetime.now()
    now_utc = datetime.datetime.utcnow()
    if end_time_str:
        hh, mm = end_time_str.strip().split(":")
        end_local = now_local.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
        if end_local <= now_local:
            end_local += datetime.timedelta(days=1)        # 已過 → 看到明天該時刻
        duration_sec = int((end_local - now_local).total_seconds())
        end_hhmm = end_local.strftime("%H:%M")
    else:
        duration_sec = max(1, int(duration_min or DEFAULT_DURATION_MIN)) * 60
        end_hhmm = (now_local + datetime.timedelta(seconds=duration_sec)).strftime("%H:%M")
    ends_at_dt = now_utc + datetime.timedelta(seconds=duration_sec)
    ends_at_iso = ends_at_dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ends_at_dt.microsecond // 1000:03d}Z"
    return ends_at_iso, duration_sec, end_hhmm


# ===========================================================================
# Subcommand: start
# ===========================================================================


def cmd_start(args) -> int:
    # 區塊職責：auto-persona infer (同 waiter/work_session)
    persona = (args.persona or "").strip()
    if not persona:
        inferred = infer_caller_persona()
        if not inferred:
            print("❌ --persona 不傳時必須能從 caller env 推 active persona (claim_origin lock)")
            print("   解法: 先跑 awakening.py morning 上線, 或顯式傳 --persona <name>")
            return 1
        persona = inferred
        print(f"✓ auto-persona: 從 caller env 推得 '{persona}'", file=sys.stderr)

    p_info = resolve_persona(persona)
    if not p_info:
        print(f"❌ persona '{persona}' 找不到 (AwakenInit/personas/{persona}.json)")
        return 1
    bank = p_info.get("bank")
    if not bank:
        print(f"❌ persona '{persona}' agent='{p_info.get('agent')}' 沒對應 bank (AGENT_TO_BANK miss)")
        return 1

    # --end-time 與 --duration 互斥
    if args.end_time and args.duration:
        print("❌ --end-time 與 --duration 互斥, 二選一")
        return 1

    mode = (args.mode or "primary").strip().lower()
    if mode not in ("primary", "companion"):
        print(f"❌ --mode 必須是 primary 或 companion (got '{mode}')")
        return 1

    state = load_state()

    # 區塊職責：companion mode 走分支 — 不獨立排程 end-time, 跟 primary 同步; cursor 初值 = primary 當前 cursor (跟著看, Tim 補充: companion 之後可以自由跳片段)。
    # 物理意義：同樂會 — 兩種 viewer 各自寫自己的 obs + 自己管自己 cursor, primary 是「主時間軸」, companion 預設跟上, 但不強制。
    # 數值影響：companion 沿用 primary ends_at; 同 persona 仍只能開一場 (避撞鎖); 同 primary 可掛多個不同 persona 的 companion。
    if mode == "companion":
        primary = find_active_primary(state, args.join_session or None)
        if primary is None:
            if args.join_session:
                print(f"❌ 找不到 active primary session: {args.join_session}")
            else:
                print("❌ 沒有 active primary stream-watch session 可加入。")
                print("   解法: (1) 自己先開 primary `start --end-time HH:mm` (2) 或等別人開好再加入")
            return 1

        # 同 persona 已有 active session → 拒絕 (可能是已 join 過, 或還在跑 primary)
        for s in state.get("active_sessions", []):
            if s.get("persona") == persona:
                print(f"❌ persona '{persona}' 已有 active watch session: {s['id']} "
                      f"(mode={s.get('mode','primary')})")
                return 1

        session_id = f"sw-{short_uuid(6)}"
        ends_at_iso = primary["ends_at"]
        end_hhmm = primary.get("ends_at_local_hhmm", "?")
        duration_sec = primary["duration_seconds"]
        duration_min = duration_sec // 60
        # cursor 初值 = primary 當前 cursor (跟著最新進度, Tim 補充: companion 之後可自由倒帶/跳段, 自己改 cursor 即可)
        cursor_epoch = float(primary.get("cursor_epoch", time.time()))

        session = {
            "id": session_id,
            "mode": "companion",
            "parent_session_id": primary["id"],
            "actor": p_info.get("agent", ""),
            "agent_bank": bank,
            "persona": persona,
            "tavern_room": args.tavern_room or primary.get("tavern_room", "tavern"),
            "started_at": utcnow_iso(),
            "ends_at": ends_at_iso,
            "ends_at_local_hhmm": end_hhmm,
            "duration_seconds": duration_sec,
            "cursor_epoch": cursor_epoch,
            # T-StreamWatch-TavernSync: 酒館「已讀」游標, 初值=加入當下最新 seq
            "tavern_read_seq": _tavern_current_seq(
                args.tavern_room or primary.get("tavern_room", "tavern")),
            "max_tiles": int(args.max_tiles or DEFAULT_MAX_TILES),
            "base_rate_per_min": BASE_RATE_PER_MIN,
            "observation_bonus": OBSERVATION_BONUS,
            "desc": args.desc or f"陪同觀影 ({primary.get('desc','primary 場')})",
            "stats": {
                "cycles": 0,
                "observations": 0,
                "hotspots": 0,
                "frames_overflow_lost": 0,
            },
        }
        state.setdefault("active_sessions", []).append(session)
        save_state(state)

        append_audit(session_id, "session_start", {
            "mode": "companion",
            "parent_session_id": primary["id"],
            "persona": persona,
            "primary_persona": primary["persona"],
            "cursor_epoch": cursor_epoch,
        })

        # Announcement (酒保身分): companion 加入觀影 — 語氣休閒
        announce_body = (
            f"🍿 陪同觀影 — **{persona}** 大小姐加入 **{primary['persona']}** 的觀影場 "
            f"(同樂到 {end_hhmm}). 想看哪段就看哪段, 沒事自由閒聊."
        )
        tavern_post(
            sender_id="tavern-keeper",
            body=announce_body,
            meta={"tag": "stream-watch-join", "session_id": session_id,
                  "parent_session_id": primary["id"], "persona": persona},
            persona="tavern-keeper",
        )

        if args.json:
            print(json.dumps({"session_id": session_id, "mode": "companion",
                              "parent_session_id": primary["id"],
                              "ends_at": ends_at_iso, "end_local_hhmm": end_hhmm,
                              "cursor_epoch": cursor_epoch, "persona": persona}, ensure_ascii=False))
        else:
            print(f"🍿 Companion session started: {session_id}")
            print(f"   加入 primary={primary['id']} ({primary['persona']})  同樂到 {end_hhmm}")
            print(f"   初始 cursor={cursor_epoch:.3f} (跟 primary 同步, 之後可自由跳段)")
            print(f"   next: 走 /loop dynamic 每 45-60s 跑 `cycle --session {session_id}` 一次")
        return 0

    # === primary mode (預設, backward compat) ===
    ends_at_iso, duration_sec, end_hhmm = _compute_ends_at(args.end_time, args.duration)
    duration_min = duration_sec // 60
    session_id = f"sw-{short_uuid(6)}"

    # 同 persona 已有 active watch session → 拒絕 (避免重複開播)
    for s in state.get("active_sessions", []):
        if s.get("persona") == persona:
            print(f"❌ persona '{persona}' 已有 active watch session: {s['id']} "
                  f"(ends_at={s.get('ends_at')})")
            return 1

    # cursor 初值 = 現在 (epoch). 第一輪 montage 只收此刻之後新寫的 frame, 不撈舊 session 殘留。
    cursor_epoch = time.time()

    session = {
        "id": session_id,
        "mode": "primary",
        "parent_session_id": "",
        "actor": p_info.get("agent", ""),
        "agent_bank": bank,
        "persona": persona,
        "tavern_room": args.tavern_room or "tavern",
        "started_at": utcnow_iso(),
        "ends_at": ends_at_iso,
        "ends_at_local_hhmm": end_hhmm,
        "duration_seconds": duration_sec,
        "cursor_epoch": cursor_epoch,
        # T-StreamWatch-TavernSync: 酒館「已讀」游標, 初值=開播當下最新 seq (只看開播後的新對話)
        "tavern_read_seq": _tavern_current_seq(args.tavern_room or "tavern"),
        "max_tiles": int(args.max_tiles or DEFAULT_MAX_TILES),
        "base_rate_per_min": BASE_RATE_PER_MIN,
        "observation_bonus": OBSERVATION_BONUS,
        "desc": args.desc or "",
        "stats": {
            "cycles": 0,
            "observations": 0,
            "hotspots": 0,
            "frames_overflow_lost": 0,
        },
    }
    state.setdefault("active_sessions", []).append(session)
    save_state(state)

    append_audit(session_id, "session_start", {
        "mode": "primary",
        "persona": persona,
        "duration_min": duration_min,
        "end_local_hhmm": end_hhmm,
        "cursor_epoch": cursor_epoch,
    })

    # Announcement (酒保身分): 開播陪看
    announce_body = (
        f"🎬 直播陪看開始 — **{persona}** 大小姐進入觀看模式 "
        f"(看到 {end_hhmm}, 約 {duration_min} min).\n"
        f"每隔一陣子發一筆觀戰評論, 熱點時刻盯細節. @Tim 開播吧.\n"
        f"💡 想加入陪看的同事走 `start --mode companion --join-session {session_id}`"
    )
    if args.desc:
        announce_body += f"\n📌 本場: {args.desc}"
    tavern_post(
        sender_id="tavern-keeper",
        body=announce_body,
        meta={"tag": "stream-watch-start", "session_id": session_id, "persona": persona},
        persona="tavern-keeper",
    )

    if args.json:
        print(json.dumps({"session_id": session_id, "mode": "primary",
                          "ends_at": ends_at_iso,
                          "end_local_hhmm": end_hhmm, "duration_seconds": duration_sec,
                          "cursor_epoch": cursor_epoch, "persona": persona}, ensure_ascii=False))
    else:
        print(f"✅ Stream watch session started: {session_id}")
        print(f"   persona={persona}  看到 {end_hhmm} (~{duration_min}min)  ends_at={ends_at_iso}")
        print(f"   初始 cursor={cursor_epoch:.3f}  max_tiles={session['max_tiles']}")
        print(f"   next: 走 /loop dynamic 每 45-60s 跑 `cycle --session {session_id}` 一次")
        print(f"   同事想加入陪看 → `start --mode companion --join-session {session_id}`")
    return 0


# ===========================================================================
# Subcommand: cycle
# ===========================================================================


def cmd_cycle(args) -> int:
    """
    Agent loop tick. 回 JSON 給 agent 端 parse:
      {
        "session_id", "persona", "elapsed_seconds", "remaining_seconds",
        "expired": bool, "action_hint": "observe"|"end",
        "cursor_epoch": <上次看到哪>, "max_tiles": N,
        "montage_cmd": "<建議直接跑的 montage 指令>",
        "cycle_num": N
      }

    expired=true 時 action_hint=end (agent MUST 跑 cmd_end)。
    否則 action_hint=observe: agent 跑 montage_cmd → Read 圖 → 寫評論 → record_observation。
    """
    state = load_state()
    session = find_active(state, args.session)
    if session is None:
        print(json.dumps({"error": f"session not found: {args.session}", "action_hint": "abort"}))
        return 1

    now_dt = datetime.datetime.utcnow()
    started_dt = parse_iso(session["started_at"])
    ends_dt = parse_iso(session["ends_at"])
    elapsed = int((now_dt - started_dt).total_seconds())
    remaining = max(0, int((ends_dt - now_dt).total_seconds()))
    expired = now_dt >= ends_dt

    session["stats"]["cycles"] += 1
    save_state(state)

    if expired:
        result = {
            "session_id": session["id"],
            "persona": session["persona"],
            "elapsed_seconds": elapsed,
            "remaining_seconds": 0,
            "expired": True,
            "action_hint": "end",
            "cursor_epoch": session["cursor_epoch"],
            "cycle_num": session["stats"]["cycles"],
        }
        append_audit(session["id"], "cycle_expired", {"cycle_num": session["stats"]["cycles"]})
        print(json.dumps(result, ensure_ascii=False))
        return 0

    # 建議的 montage 指令: --after-mtime <cursor> 接續上次, --max-tiles 抽稀控圖大小
    cursor = session["cursor_epoch"]
    max_tiles = session["max_tiles"]
    # T-StreamWatch-TavernSync: montage_cmd 預設帶 --ocr (字幕 sidecar) + 酒館未讀同步:
    #   --tavern-self <persona> 排除自己, --tavern-since-seq <已讀游標> 只收未讀。
    #   觀影 agent 跑 montage_cmd → Read sidecar 即同時拿到「畫面字幕 + 同事對話」(Hard Rule #11)。
    tavern_read_seq = int(session.get("tavern_read_seq", -1))
    montage_cmd = (f"{_MONTAGE_TOOL} make --after-mtime {cursor:.3f} --max-tiles {max_tiles} "
                   f"--ocr --tavern-self {session['persona']} --tavern-since-seq {tavern_read_seq}")

    # Companion 多印 peer obs hint (軟提示, 不擋) + primary cursor 比對
    mode = session.get("mode", "primary")
    companion_hint = ""
    primary_cursor = None
    if mode == "companion":
        parent_id = session.get("parent_session_id", "")
        primary = find_active(state, parent_id) if parent_id else None
        if primary:
            primary_cursor = float(primary.get("cursor_epoch", cursor))
            primary_persona = primary.get("persona", "?")
            primary_obs = primary.get("stats", {}).get("observations", 0)
            companion_hint = (
                f"[companion] primary={parent_id} ({primary_persona}) cursor={primary_cursor:.3f}, "
                f"你目前 cursor={cursor:.3f} (差 {primary_cursor - cursor:+.1f}s). "
                f"primary 已發 {primary_obs} 筆 obs (酒館 op=read 可讀). "
                f"想跳到 primary 進度: 自己跑 montage 帶 --after-mtime {primary_cursor:.3f}; "
                f"想看自己感興趣的某段: 自己組 --after-mtime <epoch> 也行 (Tim 拍板, 自由觀賞)."
            )
        else:
            companion_hint = ("[companion] ⚠ parent primary session 找不到 "
                              "(可能已 end), 你可以自己 end 或繼續看到自己 cursor 跑完.")

    result = {
        "session_id": session["id"],
        "mode": mode,
        "parent_session_id": session.get("parent_session_id", ""),
        "persona": session["persona"],
        "elapsed_seconds": elapsed,
        "remaining_seconds": remaining,
        "expired": False,
        "action_hint": "observe",
        "cursor_epoch": cursor,
        "primary_cursor_epoch": primary_cursor,
        "tavern_read_seq": tavern_read_seq,
        "max_tiles": max_tiles,
        "montage_cmd": montage_cmd,
        "cycle_num": session["stats"]["cycles"],
        "hint": ("跑 montage_cmd → Read sidecar (含畫面字幕 + 酒館未讀) → 寫觀戰評論 post 進 tavern → "
                 "record_observation --next-cursor <report 的 next-cursor> --tavern-seq <report 的 tavern_max_seq>. "
                 "熱點(戰鬥/團滅/場景切)→ 該輪改去掉 --max-tiles 高密度 或加 --region 盯細節, "
                 "並 record_observation --hotspot."),
        "companion_hint": companion_hint,
    }
    append_audit(session["id"], "cycle", {
        "cycle_num": session["stats"]["cycles"],
        "elapsed_seconds": elapsed,
        "cursor_epoch": cursor,
    })
    print(json.dumps(result, ensure_ascii=False))
    return 0


# ===========================================================================
# Subcommand: record_observation
# ===========================================================================


def cmd_record_observation(args) -> int:
    """
    Log 一筆 observation event + 推進 cursor。agent 發完觀戰評論 post 進 tavern 後跑這支記帳。

    --next-cursor <epoch>: montage report 印的 next-cursor, 原樣餵進來推進 session cursor,
                           保證下一輪 cycle 的 montage_cmd 從這裡接續 (0-gap)。
    --hotspot: 標記本輪是熱點高密度觀察 (純統計)。
    --lost N: 本輪 montage 報的 overflow 遺失幀數 (累進統計, 提示該縮短 cycle)。
    每筆 +OBSERVATION_BONUS 累進 session.stats.observations → end 時結算。
    """
    state = load_state()
    session = find_active(state, args.session)
    if session is None:
        print(f"❌ session not found: {args.session}")
        return 1

    # 推進 cursor (核心: 0-gap 接續的持久化點)
    old_cursor = session["cursor_epoch"]
    if args.next_cursor is not None:
        try:
            session["cursor_epoch"] = float(args.next_cursor)
        except ValueError:
            print(f"⚠ --next-cursor '{args.next_cursor}' 非數字, cursor 不變 (下輪會重疊)", file=sys.stderr)

    # T-StreamWatch-TavernSync: 推進酒館「已讀」游標 (對齊 frame cursor 鐵律, 保 0-gap)。
    # 餵 montage report 印的 tavern_max_seq (= 本輪實際顯示到的最大 seq), 下輪只收更新的未讀。
    # 不傳 → 游標不動 (下輪會重顯本輪訊息, 不漏只重複, 安全側)。
    old_tavern_seq = int(session.get("tavern_read_seq", -1))
    if getattr(args, "tavern_seq", None) is not None:
        try:
            new_seq = int(args.tavern_seq)
            # 只前進不後退 (防誤餵舊值倒退游標 → 重洗已讀)
            session["tavern_read_seq"] = max(old_tavern_seq, new_seq)
        except ValueError:
            print(f"⚠ --tavern-seq '{args.tavern_seq}' 非整數, 酒館游標不變", file=sys.stderr)

    session["stats"]["observations"] += 1
    if args.hotspot:
        session["stats"]["hotspots"] += 1
    if args.lost:
        session["stats"]["frames_overflow_lost"] += max(0, int(args.lost))
    save_state(state)

    append_audit(session["id"], "observation", {
        "observation_count": session["stats"]["observations"],
        "cursor_from": old_cursor,
        "cursor_to": session["cursor_epoch"],
        "tavern_seq_from": old_tavern_seq,
        "tavern_seq_to": int(session.get("tavern_read_seq", -1)),
        "hotspot": bool(args.hotspot),
        "lost": int(args.lost or 0),
        "focus": (args.focus or ""),
    })
    tavern_note = ""
    new_tavern_seq = int(session.get("tavern_read_seq", -1))
    if new_tavern_seq != old_tavern_seq:
        tavern_note = f"; tavern_seq {old_tavern_seq} → {new_tavern_seq}"
    print(f"✅ observation recorded (total: {session['stats']['observations']}); "
          f"cursor {old_cursor:.3f} → {session['cursor_epoch']:.3f}{tavern_note}"
          + ("  [hotspot]" if args.hotspot else ""))
    return 0


# ===========================================================================
# Subcommand: end
# ===========================================================================


def cmd_end(args) -> int:
    state = load_state()
    session = find_active(state, args.session)
    if session is None:
        print(f"❌ session not found: {args.session}")
        return 1

    now_dt = datetime.datetime.utcnow()
    started_dt = parse_iso(session["started_at"])
    ends_dt = parse_iso(session["ends_at"])
    elapsed_sec = int((now_dt - started_dt).total_seconds())
    expired = now_dt >= ends_dt

    # 防 phantom-payroll: 完全沒 cycle/observation = 沒貢獻, 不發薪
    s = session["stats"]
    contributed = (s["cycles"] > 0 or s["observations"] > 0)

    # 早收場 ack (同 waiter): 不到期 + 沒 early-confirm → 拒絕 silent early-end
    if not expired and not args.early_confirm:
        print(f"❌ session 未到期 (剩 {int((ends_dt - now_dt).total_seconds())}s), 拒絕 silent early-end.")
        print(f"   - 想真結束 (Tim 叫停) → 加 --early-confirm flag 顯式 ack")
        print(f"   - 等到期 → 不必動, 過 ends_at 後 cycle 會回 action_hint=end")
        return 2

    # 結算: base = min(elapsed_min, duration_min) * rate + observations * bonus
    elapsed_min = elapsed_sec // 60
    duration_min = session["duration_seconds"] // 60
    paid_min = min(elapsed_min, duration_min)
    base_pay = paid_min * session["base_rate_per_min"]
    bonus_pay = s["observations"] * session["observation_bonus"]
    total = base_pay + bonus_pay

    ledger_path = ""
    if contributed and total > 0:
        ledger_path = fire_salary_credit(
            bank=session["agent_bank"],
            persona=session["persona"],
            amount=total,
            session_id=session["id"],
            checkpoint=f"final(base={base_pay}+bonus={bonus_pay})",
        )
    else:
        append_audit(session["id"], "salary_skipped_phantom", {
            "persona": session["persona"],
            "reason": "no_contribution_event" if not contributed else "zero_total",
        })

    # 移到 history
    state.get("active_sessions", []).remove(session)
    session["ended_at"] = utcnow_iso()
    session["ended_reason"] = "expired" if expired else "early_confirm"
    session["settlement"] = {
        "elapsed_min": elapsed_min,
        "paid_min": paid_min,
        "base_pay": base_pay,
        "bonus_pay": bonus_pay,
        "total": total,
        "ledger": ledger_path,
        "contributed": contributed,
    }
    state.setdefault("history", []).append(session)
    save_state(state)

    append_audit(session["id"], "session_end", {
        "persona": session["persona"],
        "elapsed_min": elapsed_min,
        "paid_min": paid_min,
        "base_pay": base_pay,
        "bonus_pay": bonus_pay,
        "total": total,
        "expired": expired,
        "observations": s["observations"],
        "hotspots": s["hotspots"],
        "frames_overflow_lost": s["frames_overflow_lost"],
    })

    # Announcement (酒保身分): 收播 — primary end 時提示 companion 可自行收播
    mode = session.get("mode", "primary")
    lost_note = (f", 遺失 {s['frames_overflow_lost']} 幀(落後)" if s["frames_overflow_lost"] else "")
    if mode == "primary":
        companions = list_companions(state, session["id"])
        comp_note = ""
        if companions:
            names = ", ".join(f"@{c['persona']}" for c in companions)
            comp_note = (f"\n👥 陪同觀影中的 {len(companions)} 位 ({names}) — "
                         f"primary 結束了, 你們也可以自己 `end --early-confirm` 收播.")
        end_body = (
            f"🎬 直播陪看結束 — **{session['persona']}** 大小姐 (primary) 收播 "
            f"({elapsed_min}min, 觀戰 {s['observations']} 筆, 熱點 {s['hotspots']} 次{lost_note}).\n"
            f"結算: base {base_pay} + bonus {bonus_pay} = **{total} token**."
            f"{comp_note}"
        )
    else:
        # companion end
        parent_id = session.get("parent_session_id", "")
        end_body = (
            f"🍿 陪同觀影結束 — **{session['persona']}** 大小姐收播 "
            f"({elapsed_min}min, 觀戰 {s['observations']} 筆{lost_note}).\n"
            f"結算: base {base_pay} + bonus {bonus_pay} = **{total} token**. "
            f"(parent primary: {parent_id})"
        )
    tavern_post(
        sender_id="tavern-keeper",
        body=end_body,
        meta={"tag": "stream-watch-end", "session_id": session["id"],
              "persona": session["persona"], "mode": mode},
        persona="tavern-keeper",
    )

    if args.json:
        print(json.dumps({
            "session_id": session["id"],
            "elapsed_min": elapsed_min,
            "stats": s,
            "settlement": session["settlement"],
        }, ensure_ascii=False))
    else:
        print(f"✅ Stream watch session ended: {session['id']}")
        print(f"   elapsed={elapsed_min}min  cycles={s['cycles']}  observations={s['observations']}  "
              f"hotspots={s['hotspots']}  lost={s['frames_overflow_lost']}")
        print(f"   salary: base {base_pay} + bonus {bonus_pay} = {total} token (ledger: {ledger_path or 'skipped'})")
    return 0


# ===========================================================================
# Subcommand: status / list
# ===========================================================================


def cmd_status(args) -> int:
    state = load_state()
    session = find_active(state, args.session)
    if session is None:
        for h in state.get("history", []):
            if h.get("id") == args.session:
                print(json.dumps(h, ensure_ascii=False, indent=2))
                return 0
        print(f"❌ session not found: {args.session}")
        return 1
    print(json.dumps(session, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args) -> int:
    state = load_state()
    actives = state.get("active_sessions", [])
    if args.persona:
        actives = [s for s in actives if s.get("persona") == args.persona]
    if args.mode:
        actives = [s for s in actives if s.get("mode", "primary") == args.mode]
    if args.json:
        print(json.dumps(actives, ensure_ascii=False))
        return 0
    if not actives:
        print("(no active stream watch sessions)")
        return 0
    for s in actives:
        st = s["stats"]
        mode = s.get("mode", "primary")
        parent = s.get("parent_session_id", "")
        tag = f"[{mode}]" + (f"→{parent}" if parent else "")
        print(f"- {s['id']} {tag} persona={s['persona']} 看到 {s.get('ends_at_local_hhmm','?')} "
              f"cycles={st['cycles']} obs={st['observations']} hotspots={st['hotspots']}")
    return 0


# ===========================================================================
# Entry
# ===========================================================================


def main():
    ap = argparse.ArgumentParser(description="Stream watch session (直播連續觀看模式) CLI.")
    sub = ap.add_subparsers(dest="op", required=True)

    sp = sub.add_parser("start", help="開新 stream watch session.")
    sp.add_argument("--persona", help="觀看的 persona; 不傳則自動推 caller env 上線 persona.")
    sp.add_argument("--mode", default="primary", choices=["primary", "companion"],
                    help="primary=主觀影者(預設, 既有流程); companion=加入既有 primary 場陪同觀影.")
    sp.add_argument("--join-session", default="",
                    help="(companion) 加入指定 primary session id; 不帶則自動找最新 active primary.")
    sp.add_argument("--end-time", default="", help="(primary) 看到幾點 HH:mm (local); companion 自動沿用 primary 的 end-time.")
    sp.add_argument("--duration", type=int, default=0, help="(primary, 與 --end-time 互斥) 看多少分鐘.")
    sp.add_argument("--max-tiles", type=int, default=DEFAULT_MAX_TILES,
                    help=f"每輪 montage 格數上限 (預設 {DEFAULT_MAX_TILES}).")
    sp.add_argument("--tavern-room", default="tavern", help="發觀戰評論的 tavern room.")
    sp.add_argument("--desc", default="", help="本場主題描述 (announcement 會 append).")
    sp.add_argument("--json", action="store_true", help="輸出 JSON.")
    sp.set_defaults(func=cmd_start)

    sp = sub.add_parser("cycle", help="Agent loop tick — 回 cursor + montage 指令提示 + 到期判斷.")
    sp.add_argument("--session", required=True)
    sp.set_defaults(func=cmd_cycle)

    sp = sub.add_parser("record_observation", help="記錄一筆觀戰評論 + 推進 cursor (發完評論跑).")
    sp.add_argument("--session", required=True)
    sp.add_argument("--next-cursor", default=None, help="montage report 印的 next-cursor (epoch), 推進接續點.")
    sp.add_argument("--tavern-seq", dest="tavern_seq", default=None,
                    help="montage report 印的 tavern_max_seq, 推進酒館已讀游標 (只前進; 不傳則游標不動).")
    sp.add_argument("--hotspot", action="store_true", help="標記本輪是熱點高密度觀察.")
    sp.add_argument("--lost", type=int, default=0, help="本輪 montage 報的 overflow 遺失幀數.")
    sp.add_argument("--focus", default="",
                    choices=["", "combat", "audio", "subtitle", "primary", "free"],
                    help="(Lite v0.5, 純標籤) 本筆觀察焦點; 不影響薪資, 只寫進 audit log.")
    sp.set_defaults(func=cmd_record_observation)

    sp = sub.add_parser("end", help="結束 session, 結算 salary.")
    sp.add_argument("--session", required=True)
    sp.add_argument("--early-confirm", action="store_true", help="未到期想結束 (Tim 叫停) 需顯式加.")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_end)

    sp = sub.add_parser("status", help="列 session JSON.")
    sp.add_argument("--session", required=True)
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("list", help="列 active stream watch sessions.")
    sp.add_argument("--persona", help="只列指定 persona.")
    sp.add_argument("--mode", choices=["primary", "companion"], help="只列指定 mode.")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_list)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
