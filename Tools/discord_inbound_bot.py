#!/usr/bin/env python3
"""discord_inbound_bot.py — Discord channel → ChatTavern relay (inbound side).

⚠ PRODUCTION BOT — DO NOT MOVE / DUPLICATE
    本檔路徑寫死在 RCG_DiscordInboundDaemon.cs:37 (BOT_SCRIPT_RELATIVE), Editor
    [InitializeOnLoad] 自動 spawn + respawn 本檔. 改 bot 邏輯就改本檔.
    想另起 prototype → fork branch 試, 別在 repo 內留第二份 (T07.2, 2026-05-15 apex-two).

# 區塊職責：常駐 Discord gateway listener，把 watched channel 的訊息中繼進 Tavern
# 物理意義：跟 notify_discord.py 對偶（後者是 outbound: tavern → discord webhook）。
#          discord.py 維持 WebSocket gateway，on_message hook 過濾後走 run_cmd.py op=post
#          進 Cmd_Tavern 寫入（單一寫者保證，per Quest_Workflow §12.2）。
# 數值影響：每筆 Discord 訊息對應一筆 Tavern post（meta.source=discord 防迴圈）。
#          run_cmd.py 走 queue.json + Editor watcher，latency ~1s/msg，可接受。

設計重點：
- 走 Cmd_Tavern op=post（單一寫者）— 不直寫 message json file，避免繞過 mirror / presence / seq
- meta.source=discord + meta.discord_msg_id 兩個防迴圈標記（notify_discord 端 mirror filter 認 source）
- sender_id=discord:<user_id> 每 Discord 講者一個獨立 sender（per Tim 決策）
- Token resolution：ENV DISCORD_INBOUND_BOT_TOKEN > _secrets/discord_bot_token.txt
- Channel mapping：讀 notify_config.json tavern_inbound.channel_mappings
- 結構化 log → stdout（Unity daemon 抓 child stdout 顯示 Console）
- Fail-safe：Cmd_Tavern call 失敗 log warning + 訊息丟掉，不擋 gateway 連線
- Bot 自己 + webhook bot 發的訊息 skip（防 outbound 推回 inbound）

依賴：
    pip install discord.py>=2.3
"""
from __future__ import annotations

import asyncio
import datetime
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# 確保 _lib 可 import（無論從哪呼叫都拿得到 tavern_paths）
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# 區塊職責：路徑常數 — 跟既有 PromptQueue / ChatTavern 統一 source
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402

CONFIG_PATH = _tp.NOTIFY_CONFIG_PATH
SECRETS_DIR = _tp.AGENT_COMMANDS_DIR / "_secrets"
TOKEN_FILE = SECRETS_DIR / "discord_bot_token.txt"
TOKEN_ENV_VAR = "DISCORD_INBOUND_BOT_TOKEN"

# 區塊職責：新 routing 設定檔 — Discord channel → tavern room + source_class + priority + enabled
# 物理意義：notify_config.json.tavern_inbound.channel_mappings 為 legacy fallback (向後相容);
#          新檔 discord_channel_routing.json 提供 richer schema (source_class freeform tag / priority desc sort / per-row enable toggle / label).
# 數值影響：若新檔存在 → 純讀新檔; 不存在 → fallback legacy. Bot 啟動時 resolve, runtime 改 config 要 kill bot 重 spawn.
ROUTING_PATH = _tp.TAVERN_DIR / "discord_channel_routing.json"

# run_cmd.py 用來打 Cmd_Tavern op=post（單一寫者）— T-PATH-02: layout-agnostic resolver
RUN_CMD_PATH = _tp.RUN_CMD_PATH

# T07.1 (2026-05-15 apex-two) — Discord 附件落地根目錄
# 物理意義: Discord image/file attachment 下載到本地, 走 refs 機制同步進酒館 message;
#          路徑跟 tavern message storage 對齊 (per YYYY-MM-DD 分目錄)
# 數值影響: media/discord/<YYYY-MM-DD>/<msg_id>__<att_id>__<safe_filename>
MEDIA_ROOT = _tp.TAVERN_DIR / "media" / "discord"

# 檔名安全化 regex — 過濾 OS / refs 解析會炸的字元 (refs 用 '|' 分隔, CLI 用 '=')
_FILENAME_UNSAFE_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _sanitize_attachment_filename(name: str) -> str:
    """Discord attachment.filename → 本地安全檔名."""
    if not name:
        return "unnamed"
    s = _FILENAME_UNSAFE_RE.sub("_", name)
    s = s.replace("=", "_").replace(" ", "_").lstrip("-._")
    return s or "unnamed"


async def _download_attachments(message) -> tuple[list[str], list[dict]]:
    """
    下載 message.attachments 到 MEDIA_ROOT/<YYYY-MM-DD>/<msg_id>__<att_id>__<filename>.

    回 (rel_paths_for_refs, meta_records):
      - rel_paths_for_refs: list of repo-relative path 字串 (給 Cmd_Tavern --arg refs= 用)
      - meta_records: list of {filename, url, content_type, size, local} dict (給 meta.attachments 用)

    任一附件失敗 → log warning swallow, 不擋其他附件 / 不擋 body 寫入.
    """
    rel_paths: list[str] = []
    records: list[dict] = []
    if not getattr(message, "attachments", None):
        return rel_paths, records

    date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    save_dir = MEDIA_ROOT / date_str
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        log.warning(f"attachment dir mkdir failed: {e}")
        return rel_paths, records

    for att in message.attachments:
        try:
            safe_name = _sanitize_attachment_filename(att.filename or f"att_{att.id}")
            local_name = f"{message.id}__{att.id}__{safe_name}"
            local_path = save_dir / local_name
            await att.save(local_path)
            # repo-relative + forward slash 對齊 refs 慣例
            rel = local_path.relative_to(REPO_ROOT).as_posix()
            rel_paths.append(rel)
            records.append({
                "filename": att.filename,
                "url": att.url,
                "content_type": getattr(att, "content_type", None) or "",
                "size": att.size,
                "local": rel,
            })
            log.info(f"  attachment saved: {att.filename} ({att.size}B) → {rel}")
        except Exception as e:
            log.warning(f"  attachment save failed ({getattr(att, 'filename', '?')}): {e}")
    return rel_paths, records


def _build_attachment_body_hint(records: list[dict]) -> str:
    """body 為空時用附件清單當 placeholder, 讓酒館看到「來源是純圖訊息」."""
    if not records:
        return ""
    names = [r["filename"] for r in records]
    return f"[Discord 附件 {len(names)} 個] " + ", ".join(names)

# 結構化 log 設定 — stdout / line-buffered 給 Unity daemon 抓
# kiara 2026-06-13: 加 FileHandler 雙寫 → post_to_tavern 失敗的 log.warning 不再
# 因為 bot 跑在 detached console 就消失。檔案位置選 AgentCommands/_session/
# (per-project, .gitignore 內 _session 已排除, log 不入 commit)
_LOG_FILE = (
    Path(__file__).resolve().parent.parent / "_session" / "discord_inbound.log"
)
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_fmt = logging.Formatter(
    "[discord-inbound] %(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
_stdout_h = logging.StreamHandler(sys.stdout)
_stdout_h.setFormatter(_fmt)
_file_h = logging.FileHandler(_LOG_FILE, encoding="utf-8")
_file_h.setFormatter(_fmt)

logging.basicConfig(level=logging.INFO, handlers=[_stdout_h, _file_h])
log = logging.getLogger("discord-inbound")


# ===========================================================================
# Config + secrets resolution
# ===========================================================================


def load_config() -> dict:
    """讀 notify_config.json tavern_inbound section (legacy enabled flag).

    回傳 tavern_inbound dict (含 enabled / channel_mappings / 等). Channel mappings
    現在優先讀 discord_channel_routing.json (見 load_routing); 但 enabled 旗仍由 notify_config 控.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"notify_config.json not found: {CONFIG_PATH}")
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    inbound = data.get("tavern_inbound") or {}
    if not isinstance(inbound, dict):
        raise ValueError("tavern_inbound section malformed")
    return inbound


def load_discord_user_mentions_reverse() -> dict[str, str]:
    """讀 notify_config.tavern_mirror.discord_user_mentions, 反轉成 {uid_str: display_name}.

    # 區塊職責：建反向 uid → name map, 給 on_message 解析 sender_name 用
    # 物理意義：notify_config 內 mentions 是 forward (display_name → uid) 給 outbound 用;
    #          本函式反轉提供 inbound 用. 一個 uid 對應一個 name (取最後 wins, alias 共用 uid 例外).
    # 數值影響：dict 預期 < 50 entries, 開銷可忽略; bot 啟動時建一次, runtime 不重讀.

    回傳 {"383604378185105408": "Tim", "191938341137022976": "David", ...}.
    """
    try:
        inbound_data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        tm = inbound_data.get("tavern_mirror") or {}
        mentions = tm.get("discord_user_mentions") or {}
        if not isinstance(mentions, dict):
            return {}
        out: dict[str, str] = {}
        for display_name, uid in mentions.items():
            if not display_name or not uid:
                continue
            uid_s = str(uid).strip()
            if not uid_s:
                continue
            # 後寫者覆蓋早寫者 (e.g. "RudyL." / "RudyL" 同 uid → 取後者 display 為主)
            # 對齊 outbound 行為 (notify_discord _rewrite_at_mentions_for_discord 取最後 match)
            out[uid_s] = display_name
        return out
    except Exception as e:
        log.warning(f"load_discord_user_mentions_reverse fail: {e}")
        return {}


# 區塊職責：identities.json 反向 cache — 避免每筆 message 都 fs read
# 物理意義：bot 啟動時讀一次 identities.json 拉現有 discord:* entries 進 cache;
#          on_message 時若 cache miss / display_name 變動 → 走 ensure_discord_identity 寫檔.
# 數值影響：dict 預期 < 100 entries (Discord 活躍用戶有限), 純記憶體開銷可忽略.
_identity_cache: dict[str, str] = {}   # {sender_id: display_name}


def _identities_atomic_write(data: dict) -> None:
    """Atomic write identities.json — tmp + os.replace 防 partial-write race with Cmd_Tavern reader."""
    path = _tp.IDENTITIES_PATH
    # tempfile 在同 dir 才能 atomic rename (跨 disk 會 fail)
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".tmp_identities_", suffix=".json", dir=str(parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(tmp_name, path)
    except Exception:
        # cleanup tmp on fail
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def ensure_discord_identity(uid: str, display_name: str) -> bool:
    """確保 identities.json 內有 'discord:<uid>' entry 且 display_name 對齊.

    # 區塊職責：inbound message 前 register / refresh identity, 讓 Cmd_Tavern 端 lookup 找得到
    # 物理意義：Cmd_Tavern.Op_Post 走 identities.json 查 display_name, 沒 entry 就 fallback sender_id 當顯示名.
    #          本 helper 確保新 Discord 用戶第一次發訊息時 identity 就位, 之後 tavern UI / mirror 正常顯示.
    # 數值影響：cache hit + display_name 不變 → no-op; miss / display 改 → atomic write identities.json.

    回傳 True 若實際有寫檔, False 若 cache hit 無變動.
    """
    sid = f"discord:{uid}"
    cached = _identity_cache.get(sid)
    if cached == display_name:
        return False   # cache hit, no change

    path = _tp.IDENTITIES_PATH
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = {"identities": []}
    except Exception as e:
        log.warning(f"ensure_discord_identity read fail: {e}")
        return False

    ids = data.setdefault("identities", [])
    now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    found = False
    changed = False
    for entry in ids:
        if entry.get("id") == sid:
            found = True
            if entry.get("display_name") != display_name:
                entry["display_name"] = display_name
                changed = True
            entry["last_seen_at"] = now_iso
            # last_seen 更新即視為 "有變動" 寫回 — 但太頻繁寫檔太重, 只在 display_name 真變才落地
            break
    if not found:
        ids.append({
            "id": sid,
            "display_name": display_name,
            "kind": "discord-user",
            "created_at": now_iso,
            "last_seen_at": now_iso,
        })
        changed = True

    _identity_cache[sid] = display_name
    if not changed:
        return False

    try:
        _identities_atomic_write(data)
        log.info(f"identity registered/updated: {sid} → {display_name}")
        return True
    except Exception as e:
        log.warning(f"ensure_discord_identity write fail ({sid}): {e}")
        return False


def load_routing() -> list[dict]:
    """讀新 routing 設定; 不存在則 fallback 從 notify_config.tavern_inbound.channel_mappings 轉換.

    # 區塊職責：channel routing 解析 — 新 schema 為主, legacy 為 fallback
    # 物理意義：新 schema (discord_channel_routing.json) 帶 source_class / priority / enabled / label;
    #          legacy schema (tavern_inbound.channel_mappings) 只有 channel_id + tavern_room.
    # 數值影響：legacy fallback 自動補預設值: source_class="external", priority=0, enabled=True, label="(unlabeled)".

    回傳 list of dict, 每筆含: channel_id (str), tavern_room (str), source_class (str), priority (int),
                         enabled (bool), label (str), guild_id (str), tags (list)
    """
    # 優先新 schema
    if ROUTING_PATH.exists():
        try:
            d = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
            mappings = d.get("mappings") or []
            if not isinstance(mappings, list):
                log.warning(f"{ROUTING_PATH.name}: 'mappings' 不是 list, 視為空")
                return []
            # 補預設值 + 過濾無效 row
            out = []
            for m in mappings:
                if not isinstance(m, dict):
                    continue
                cid = str(m.get("channel_id", "")).strip()
                room = (m.get("tavern_room") or "").strip()
                if not cid or not room:
                    continue
                out.append({
                    "channel_id": cid,
                    "tavern_room": room,
                    "source_class": (m.get("source_class") or "external").strip(),
                    "priority": int(m.get("priority") or 0),
                    "enabled": bool(m.get("enabled", True)),
                    "label": (m.get("label") or "(unlabeled)").strip(),
                    "guild_id": str(m.get("guild_id", "")).strip(),
                    "tags": m.get("tags") or [],
                })
            return out
        except Exception as e:
            log.warning(f"load_routing 失敗 ({ROUTING_PATH.name}): {e}; fallback legacy")
    # Legacy fallback (notify_config.tavern_inbound.channel_mappings)
    inbound = load_config()
    legacy = inbound.get("channel_mappings") or []
    out = []
    for m in legacy:
        if not isinstance(m, dict):
            continue
        cid = str(m.get("channel_id", "")).strip()
        room = (m.get("tavern_room") or "").strip()
        if not cid or not room:
            continue
        out.append({
            "channel_id": cid,
            "tavern_room": room,
            "source_class": "external",
            "priority": 0,
            "enabled": True,
            "label": "(legacy)",
            "guild_id": str(m.get("guild_id", "")).strip(),
            "tags": [],
        })
    return out


def resolve_token() -> str:
    """Token 解析：ENV > 檔案。回單行 trimmed string。"""
    env_val = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if env_val:
        log.info(f"token source: ENV {TOKEN_ENV_VAR}")
        return env_val
    if TOKEN_FILE.exists():
        val = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if val:
            log.info(f"token source: file {TOKEN_FILE.relative_to(REPO_ROOT)}")
            return val
    raise RuntimeError(
        f"Discord bot token not found. Set {TOKEN_ENV_VAR} env var or write to "
        f"{TOKEN_FILE.relative_to(REPO_ROOT)}"
    )


def build_channel_map(routing: list[dict]) -> dict[int, dict]:
    """從 routing list 組 {channel_id_int: routing_row_dict}.

    Disabled rows 自動 skip (不進 map → on_message 視為非 watched channel).
    """
    out: dict[int, dict] = {}
    for m in routing:
        if not m.get("enabled", True):
            continue
        try:
            cid_int = int(m["channel_id"])
        except (ValueError, KeyError):
            log.warning(f"routing entry skipped (bad channel_id): {m}")
            continue
        out[cid_int] = m
    return out


# ===========================================================================
# Tavern post — 走 run_cmd.py op=post（單一寫者保證）
# ===========================================================================


def post_to_tavern(
    *,
    room: str,
    sender_id: str,
    sender_name: str,
    body: str,
    discord_msg_id: str,
    discord_channel_id: str,
    discord_guild_id: str | None,
    source_class: str = "external",
    priority: int = 0,
    channel_label: str = "",
    refs_paths: list[str] | None = None,
    attachment_records: list[dict] | None = None,
) -> bool:
    """走 run_cmd.py 進 Cmd_Tavern op=post 寫 tavern.

    Return True on success, False on fail（fail 不擋上游 gateway loop）。

    meta 防迴圈標記：source=discord + discord_msg_id（notify_discord mirror 認 source 跳過）。
    額外標記 source_class / priority / channel_label 供 waiter cycle sort + agent context.

    T07.1 (2026-05-15): refs_paths + attachment_records 用於圖片同步:
      - refs_paths 走 Cmd_Tavern --arg refs= (走既有 refs 機制, render 端輸出 markdown link)
      - attachment_records 進 meta.attachments (JSON array, 保留 Discord CDN URL)
    """
    meta = {
        "source": "discord",
        "discord_msg_id": discord_msg_id,
        "discord_channel_id": discord_channel_id,
        "category": "chat",
        "tag": "discord-inbound",
        "source_class": source_class,
        "priority": priority,
        "channel_label": channel_label,
    }
    if discord_guild_id:
        meta["discord_guild_id"] = discord_guild_id
    # T07.1: 附件 CDN URL + 本地路徑保進 meta (agent 想抓原始 URL 用)
    if attachment_records:
        meta["attachments"] = json.dumps(attachment_records, ensure_ascii=False)

    cmd = [
        sys.executable,
        str(RUN_CMD_PATH),
        "run",
        "Tavern",
        "--arg", "op=post",
        "--arg", f"room={room}",
        "--arg", f"sender_id={sender_id}",
        "--arg", f"sender_name={sender_name}",
        "--arg", f"body={body}",
        "--arg", f"meta={json.dumps(meta, ensure_ascii=False)}",
    ]
    if refs_paths:
        cmd += ["--arg", "refs=" + "|".join(refs_paths)]
    try:
        # timeout 60s — Editor 偶爾卡 domain reload；超時 swallow 不擋 gateway
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(REPO_ROOT),
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            log.warning(
                f"post_to_tavern failed (rc={result.returncode}) "
                f"sender={sender_id} room={room} stderr_head={result.stderr[:200]}"
            )
            return False
        return True
    except subprocess.TimeoutExpired:
        log.warning(f"post_to_tavern timeout (60s) sender={sender_id} room={room}")
        return False
    except Exception as e:
        log.warning(f"post_to_tavern exception: {e}")
        return False


# ===========================================================================
# Bot
# ===========================================================================


def make_bot(channel_map: dict[int, dict], uid_to_name: dict[str, str]):
    """建 discord.py Client 實例，掛 on_message handler。

    discord.py 是 lazy import — 失敗時給友善訊息（沒裝 lib 別爆 traceback）。

    channel_map: {channel_id_int: routing_row_dict} (含 tavern_room / source_class / priority / label).
    uid_to_name: {discord_uid_str: display_name} (e.g. {"383604378185105408": "Tim"}); on_message 用來解析 sender_name.
    """
    try:
        import discord
    except ImportError:
        log.error(
            "discord.py not installed. Run: pip install discord.py>=2.3 "
            "(needs Python >= 3.8)"
        )
        sys.exit(2)

    # Intents：只開 Message Content（per Tim 的 Discord Portal 設定）
    intents = discord.Intents.default()
    intents.message_content = True
    # 不開 members / presence（不需要 + Privileged Intent 額外驗證）

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        log.info(f"connected as {client.user} (id={client.user.id if client.user else '?'})")
        # 區塊職責：on_ready 列出 watched channel + 對應 routing row 摘要 (方便 ops 驗證 config)
        summary = ", ".join(
            f"{cid}→{r['tavern_room']}[{r['source_class']}/p{r['priority']}/{r['label']}]"
            for cid, r in channel_map.items()
        )
        log.info(f"watching {len(channel_map)} channel(s): {summary}")

    @client.event
    async def on_message(message):
        # 跳過 bot 自己（防自己迴圈）
        if client.user and message.author.id == client.user.id:
            return
        # 跳過所有 bot 發的訊息（webhook / 其他 bot）— 防 outbound webhook 推回 inbound
        if message.author.bot:
            return
        # 只處理 watched channels
        routing = channel_map.get(message.channel.id)
        if routing is None:
            return
        # T07.1 (2026-05-15 apex-two): 空 body 不再直接跳過 — 若有 attachments 走附件下載路徑
        # 物理意義: Tim QA 2026-05-15 — 圖片 only 訊息 (e.g. 「測試一下」+ 純圖) 之前整筆 skip
        #          現在: 純圖訊息也走 post, body 用附件 placeholder 填, refs 帶本地路徑
        body = (message.content or "").strip()
        has_attachments = bool(getattr(message, "attachments", None))
        if not body and not has_attachments:
            log.info(f"skip empty msg (no body + no attachments) msg_id={message.id}")
            return

        sender_id = f"discord:{message.author.id}"
        uid_s = str(message.author.id)
        # 區塊職責：sender_name 解析優先序 (T-discord-id-mapping 2026-05-15)
        # 物理意義：notify_config 內 discord_user_mentions 有 mapping (Tim/David/Azakea23/...) → 用該 name (一致 outbound);
        #          否則 Discord display_name (server nick);
        #          否則 Discord global name (account-level).
        # 數值影響：保證 sender_name 跟 outbound @-mention rewrite 對齊, 內部識別一致
        sender_name = (
            uid_to_name.get(uid_s)
            or message.author.display_name
            or message.author.name
        )
        # 區塊職責：自動 register identity, 讓 Cmd_Tavern 端 lookup 找得到顯示名
        # 物理意義：Cmd_Tavern.Op_Post 走 identities.json find by sender_id, miss → fallback sender_id 當 display_name (= 顯示 'discord:<uid>' 不漂亮);
        #          先 ensure entry 在, 之後 tavern UI / mirror render 就能秀對的 display_name
        # 數值影響：第一次新 uid 寫一筆 entry; 後續 cache hit no-op (不每訊息都 fs IO)
        ensure_discord_identity(uid_s, sender_name)
        guild_id = str(message.guild.id) if message.guild else None

        # T07.1: 下載附件 (async, 用 await 不走 executor — discord.py 的 attachment.save 本來就 async)
        refs_paths, attachment_records = await _download_attachments(message)
        # body 空 + 有附件 → placeholder 填 body, 避免 jsonl 寫入空訊息
        if not body and attachment_records:
            body = _build_attachment_body_hint(attachment_records)

        # 走 sync subprocess in thread executor（避免 asyncio 端 block）
        loop = asyncio.get_event_loop()
        ok = await loop.run_in_executor(
            None,
            lambda: post_to_tavern(
                room=routing["tavern_room"],
                sender_id=sender_id,
                sender_name=sender_name,
                body=body,
                discord_msg_id=str(message.id),
                discord_channel_id=str(message.channel.id),
                discord_guild_id=guild_id,
                source_class=routing.get("source_class", "external"),
                priority=int(routing.get("priority", 0)),
                channel_label=routing.get("label", ""),
                refs_paths=refs_paths,
                attachment_records=attachment_records,
            ),
        )
        if ok:
            log.info(
                f"relayed msg_id={message.id} "
                f"from={sender_name}({sender_id}) "
                f"channel={message.channel.id}[{routing['source_class']}/p{routing['priority']}] "
                f"→ room={routing['tavern_room']} len={len(body)} "
                f"attachments={len(attachment_records)}"
            )

    return client


# ===========================================================================
# Entry
# ===========================================================================


def main():
    log.info(f"starting (repo={REPO_ROOT})")
    inbound = load_config()
    if not inbound.get("enabled"):
        log.warning(
            "tavern_inbound.enabled=false in notify_config.json — bot 仍會跑, "
            "但建議改 true 確認你真的要 inbound."
        )
    routing = load_routing()
    channel_map = build_channel_map(routing)
    if not channel_map:
        log.error("no enabled channels in routing (discord_channel_routing.json 或 legacy) — nothing to listen on. exiting.")
        sys.exit(2)
    # 區塊職責：載 discord uid → display_name reverse map (T-discord-id-mapping 2026-05-15)
    # 物理意義：給 on_message 用來決定 sender_name; 跟 outbound @-mention rewrite 配對, 內外顯示一致
    # 數值影響：bot 啟動時讀一次 notify_config, runtime 不重讀 — 改 mentions 要 kill bot 重 spawn
    uid_to_name = load_discord_user_mentions_reverse()
    log.info(f"loaded {len(uid_to_name)} discord uid → name mapping(s)")
    # 區塊職責：bot 啟動時預 register 所有 mapped uid 進 identities.json
    # 物理意義：on_message 時才 register 等於「首次發訊息也許還會閃現 discord:<uid>」, 預 register 解這個 race
    # 數值影響：< 50 entry 一次性寫, 開銷可忽略; cache miss → 寫一筆, 不命中就 cache hit no-op
    pre_registered = 0
    for uid, name in uid_to_name.items():
        try:
            if ensure_discord_identity(uid, name):
                pre_registered += 1
        except Exception as e:
            log.warning(f"pre-register identity fail uid={uid}: {e}")
    log.info(f"pre-registered {pre_registered} discord identities into identities.json")
    token = resolve_token()

    bot = make_bot(channel_map, uid_to_name)
    # discord.Client.run 是同步 blocking call（內部包 asyncio.run）
    bot.run(token, log_handler=None)   # 我們自己有 log，不要 discord.py 預設 handler


if __name__ == "__main__":
    main()
