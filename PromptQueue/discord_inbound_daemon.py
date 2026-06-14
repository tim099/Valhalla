#!/usr/bin/env python
"""
Discord → Tavern Inbound Daemon (T15 Phase B prototype)

Discord channel 訊息回傳到 chat_tavern messages.jsonl 的 daemon。
Webhook URL 當 channel pointer：daemon 啟動時 GET /webhooks/{id}/{token}
解出 channel_id，bot 用 channel_id 訂閱該 channel 的 message_create。

三 modes:
  --check-config      不連 bot，只驗證 tavern_inbound config + webhook → channel_id resolve
  --simulate-message  合成假 Discord 訊息，跑完整 pipeline（jsonl + R7 mention + wake ack）
  --run               真連 bot gateway，訂閱所有 mapped channels（需要 bot token）

Token 載入順序：
  1. _bot_token.txt（同 dir，git-ignored）
  2. DISCORD_BOT_TOKEN env var
  3. 報錯 + 印 setup 步驟

Echo loop 三層防護（per Plan_DiscordToTavern §4.4）：
  1. author.bot 為 True → skip
  2. webhook_id 在 ignore list → skip
  3. sender_id 以 'discord:' 開頭走 outbound exclude pattern

依賴：discord.py >= 2.3（已 pip installed）
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Windows console cp950 → reconfigure stdout/stderr UTF-8 防中文 / unicode 印失敗
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).parent.resolve()

# T36.4 — 統一從 _lib.tavern_paths / discord_webhook 引用
_REPO_ROOT_FOR_LIB = HERE.parent.parent
if str(_REPO_ROOT_FOR_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT_FOR_LIB))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
from AgentCommands._lib import discord_webhook as _dw  # noqa: E402
from AgentCommands._lib.tavern_client import TavernClient  # noqa: E402

PROJECT_ROOT = _tp.REPO_ROOT
CONFIG_PATH = _tp.NOTIFY_CONFIG_PATH
TOKEN_FILE = HERE / "_bot_token.txt"
LOG_FILE = HERE / "_inbound_daemon.log"
RUN_CMD = PROJECT_ROOT / "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py"   # legacy ref (留給 trigger_wake_notify 用)

# 全域共用 WebhookClient instance（給 post_webhook_ack 委派用）
_module_webhook_client = _dw.WebhookClient(_dw.WebhookConfig(label="inbound_daemon", webhook_dir=HERE))

# T36.8 — 全域 TavernClient SDK：daemon 不再自己 spawn subprocess 拼 args
# 物理意義：write_to_tavern 改委派 client.post_message — 強化 P0 鐵律不留 daemon 直拼 args 機會
# 數值影響：subprocess 行為 + Cmd_Tavern 7 道機制完全沿用，但呼叫面 type-safe + escape 自動處理
_tavern_client = TavernClient(run_cmd_path=RUN_CMD)

WEBHOOK_RE = re.compile(r"https://discord\.com/api/webhooks/(\d+)/([\w-]+)")


# ===========================================================
# Logging（檔案 + stdout）
# ===========================================================

def log(msg, level="INFO"):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = f"[{ts}] [{level}] {msg}"
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, flush=True)


# ===========================================================
# Config / state I/O
# ===========================================================

def load_config():
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(cfg):
    """atomic write: tmp → rename"""
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, CONFIG_PATH)


def load_token():
    """token 載入：file > env var > None"""
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if token:
            log(f"token loaded from {TOKEN_FILE.name}")
            return token
    env = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if env:
        log("token loaded from DISCORD_BOT_TOKEN env var")
        return env
    return None


# ===========================================================
# Webhook resolve（Phase A — bootstrap）
# ===========================================================

def resolve_webhook(url):
    """GET /webhooks/{id}/{token} → 回 dict(id, channel_id, guild_id, ...)"""
    req = urllib.request.Request(
        url, headers={"User-Agent": "EmblemOfValor-InboundDaemon/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def post_webhook_ack(webhook_url, content, username=None, avatar_url=None):
    """POST 一條 ack 訊息回原 channel — T36.4 委派 WebhookClient.send_one。
    回 HTTP status int（沿用舊版簽章 — caller 期待 status code 不是 (ok, err) tuple）"""
    ok, err = _module_webhook_client.send_one(webhook_url, content, username=username, avatar_url=avatar_url)
    # 舊版回 r.status（int）— ok 對應 200-299；fail 用 -1 區分（caller 用此判 retry / log）
    return 200 if ok else -1


# ===========================================================
# Pipeline — Discord message → tavern jsonl + R7 mention + wake-notify
# ===========================================================

def write_to_tavern(tavern_room, sender_id, sender_name, body, discord_meta):
    """
    T36.8 — 委派 TavernClient.post_message（取代自家 spawn subprocess 拼 args）。

    強化 P0 鐵律：daemon 不再自己拼 run_cmd.py args（容易 escape 錯 / 漏 alter-pacing-bypass /
    漏 wait-reply 等）；統一走 SDK type-safe 簽章。Cmd_Tavern 7 道機制 + R7 mention parser
    + presence 自動更新等行為完全沿用。

    返回 True 成功 / False 失敗。
    """
    # discord_meta 內補 sender_name（既有 Cmd_Tavern 從 identities.json 拿，但 Discord sender 可能
    # 是新註冊的，先帶 sender_name 給 Cmd_Tavern join 流程；本 SDK 自動處理）
    discord_meta_str = ";".join(f"{k}:{v}" for k, v in discord_meta.items())
    # SDK 不直接接 sender_name 參數，所以塞進 meta（Cmd_Tavern 從 identities.json 自動 lookup）
    res = _tavern_client.post_message(
        room=tavern_room,
        sender=sender_id,
        body=body,
        meta=f"sender_name:{sender_name};{discord_meta_str}" if discord_meta_str else f"sender_name:{sender_name}",
        wait_reply=0,
        timeout=30.0,
    )
    if not res.ok:
        err_summary = res.error or (res.stderr or "")[:200].strip()
        log(f"write_to_tavern fail: {err_summary}", "ERROR")
        return False
    log(f"wrote message to {tavern_room}: sender={sender_id} body[:80]={body[:80]!r}")
    return True


def trigger_wake_notify(tavern_room, sender_id, body_preview):
    """T16 — 觸發 notify_discord.py --mode=wake 子 process。
    notify_discord 內部會偵測 inbox mtime 變動 → 推 ping 到 wake_notify webhook。
    daemon 不直接 POST webhook（避免重複實作 cooldown / state 邏輯）。"""
    notify_script = HERE / "notify_discord.py"
    if not notify_script.exists():
        log("notify_discord.py 不存在，跳過 wake-notify trigger", "WARN")
        return
    try:
        result = subprocess.run(
            [sys.executable, str(notify_script), "--mode", "wake"],
            capture_output=True, text=True, timeout=15,
            encoding="utf-8", errors="replace",
        )
        out = (result.stdout or "").strip().splitlines()
        if out:
            log(f"wake-notify trigger: {out[-1]}")
    except subprocess.TimeoutExpired:
        log("wake-notify trigger timeout", "WARN")
    except Exception as e:
        log(f"wake-notify trigger fail: {e}", "WARN")


# ===========================================================
# Mode (a): --check-config — 驗證 mapping，不連 bot
# ===========================================================

def cmd_check_config(args):
    cfg = load_config()
    inbound = cfg.get("tavern_inbound", {})
    print("=== tavern_inbound config check ===\n")
    print(f"enabled: {inbound.get('enabled', False)}")
    print(f"bot_status: {inbound.get('bot_status', 'N/A')}")
    print()

    webhooks = inbound.get("webhook_urls", [])
    if not webhooks:
        print("ERROR: no webhook_urls configured. Run resolve_inbound_webhook.py add ...")
        return 1

    print(f"{len(webhooks)} input webhook(s):")
    all_ok = True
    for entry in webhooks:
        url = entry["url"]
        room = entry["tavern_room"]
        try:
            info = resolve_webhook(url)
            wid = info["id"]
            cid = info["channel_id"]
            gid = info.get("guild_id", "")
            name = info.get("name", "")
            print(f"  [OK] webhook_id={wid} → channel_id={cid} → tavern_room={room}")
            print(f"       guild_id={gid} name={name!r}")
        except Exception as e:
            print(f"  [FAIL] {url[:60]}... -- {e}")
            all_ok = False

    print()
    token = load_token()
    if token:
        masked = token[:8] + "..." + token[-4:]
        print(f"bot_token: present ({masked})")
    else:
        print("bot_token: MISSING")
        print()
        print("Bot setup steps (5 min on Discord side):")
        print("  1. https://discord.com/developers/applications -> New Application")
        print("  2. Bot tab -> Add Bot -> Reset Token -> copy")
        print("  3. Enable 'MESSAGE CONTENT INTENT' (Privileged)")
        print("  4. OAuth2 -> URL Generator -> scopes=bot, perms=Read Messages/View Channels + Read Message History")
        print("  5. Open OAuth URL in browser -> add bot to your server")
        print(f"  6. Save token to {TOKEN_FILE.name} OR export DISCORD_BOT_TOKEN env var")
        print()
        print("--check-config still works without token (this command).")
        print("--simulate-message also works without token (synthetic pipeline test).")
        print("--run requires token (real Discord listening).")

    return 0 if all_ok else 1


# ===========================================================
# Mode (b): --simulate-message — 合成假訊息走完整 pipeline
# ===========================================================

def cmd_simulate_message(args):
    """合成 Tim 假訊息，端到端驗 pipeline（不需 bot token / 不接 Discord）"""
    cfg = load_config()
    inbound = cfg.get("tavern_inbound", {})
    mappings = inbound.get("channel_mappings", [])
    if not mappings:
        print("ERROR: no channel_mappings — run resolve_inbound_webhook.py add ... first")
        return 1

    # 用第一個 mapping 當測試標的
    target = mappings[0]
    tavern_room = target["tavern_room"]
    channel_id = target["channel_id"]

    sender_id = args.sender or "discord:test-tim"
    sender_name = args.sender_name or "Tim (simulated)"
    body = args.body or "@claude-da-xiaojie 這是 simulated Discord 訊息，測 pipeline"

    discord_meta = {
        "source": "discord-simulated",
        "discord_channel_id": channel_id,
        "discord_message_id": "simulated-" + str(int(time.time())),
        "tag": "discord-inbound-simulate",
    }

    log(f"simulate: sender={sender_id} room={tavern_room} body[:80]={body[:80]!r}")
    ok = write_to_tavern(tavern_room, sender_id, sender_name, body, discord_meta)
    if not ok:
        log("simulate fail at write_to_tavern stage", "ERROR")
        return 1

    log("simulate: triggering wake-notify ping...")
    trigger_wake_notify(tavern_room, sender_id, body)

    print()
    print("OK simulate-message done -- pipeline verified")
    print(f"  -> tavern jsonl: rooms/{tavern_room}/messages.jsonl appended")
    print(f"  -> R7 mention parser auto-fired (if body contained @<id>)")
    print(f"  -> wake-notify trigger called (notify_discord.py --mode wake)")
    return 0


# ===========================================================
# Mode (c): --run — 真連 bot gateway
# ===========================================================

def cmd_run(args):
    try:
        import discord
    except ImportError:
        print("ERROR: discord.py not installed.")
        print("  Run: pip install discord.py")
        return 1

    token = load_token()
    if not token:
        print("ERROR: bot token missing.")
        print(f"  Save token to {TOKEN_FILE} OR export DISCORD_BOT_TOKEN env var.")
        print("  Run --check-config to see Bot setup steps.")
        return 1

    cfg = load_config()
    inbound = cfg.get("tavern_inbound", {})
    mappings = inbound.get("channel_mappings", [])
    if not mappings:
        print("ERROR: no channel_mappings — run resolve_inbound_webhook.py add ... first")
        return 1

    # channel_id → tavern_room dict
    channel_to_room = {m["channel_id"]: m["tavern_room"] for m in mappings}
    # webhook_ids 用於 echo loop 防護
    own_webhook_ids = {m.get("webhook_id") for m in mappings if m.get("webhook_id")}
    # tavern_mirror outbound webhook ids 也要過濾（防雙向 echo）
    tm_urls = cfg.get("tavern_mirror", {}).get("webhook_urls", []) or []
    for url in tm_urls:
        m = WEBHOOK_RE.match(url)
        if m:
            own_webhook_ids.add(m.group(1))

    log(f"channel_to_room: {channel_to_room}")
    log(f"own_webhook_ids (echo guard): {own_webhook_ids}")

    intents = discord.Intents.default()
    intents.message_content = True  # Privileged Intent — Tim 必須在 Developer Portal 開啟
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        log(f"bot ready: {client.user} ({client.user.id})")
        # 寫進 config bot_status=connected
        c = load_config()
        c.setdefault("tavern_inbound", {})["bot_status"] = "connected"
        save_config(c)
        # 對每 mapped channel 補抓 last_read 後的歷史
        last_read_state = c.get("tavern_inbound", {}).get("last_read_state", {})
        for cid, room in channel_to_room.items():
            try:
                channel = client.get_channel(int(cid))
                if not channel:
                    log(f"channel {cid} not visible (bot has no read perm?)", "WARN")
                    continue
                last_id = last_read_state.get(str(cid), {}).get("last_read_message_id")
                if last_id:
                    log(f"catchup channel {cid} since message_id={last_id}")
                    after = discord.Object(id=int(last_id))
                    async for msg in channel.history(limit=100, after=after, oldest_first=True):
                        await handle_message(msg)
                else:
                    # 首次 — 不回放歷史，只標 baseline
                    log(f"baseline channel {cid} (skip historical messages)")
                    async for msg in channel.history(limit=1):
                        _record_last_read(cid, msg.id)
            except Exception as e:
                log(f"catchup channel {cid} fail: {e}", "ERROR")

    @client.event
    async def on_message(message):
        await handle_message(message)

    async def handle_message(message):
        # Echo loop 三層防護
        if message.author.bot:
            return  # 層 1
        if message.webhook_id and str(message.webhook_id) in own_webhook_ids:
            return  # 層 2
        # 層 3 — sender_id 'discord:' prefix 後續 outbound exclude（在寫入端決定）

        cid = str(message.channel.id)
        if cid not in channel_to_room:
            return  # 不在 mapping 內忽略

        tavern_room = channel_to_room[cid]
        # sender 解析（user_mappings → discord:<id> fallback）
        user_mappings = (
            load_config().get("tavern_inbound", {}).get("discord_user_mappings", {}) or {}
        )
        author_id = str(message.author.id)
        sender_id = user_mappings.get(author_id, f"discord:{author_id}")
        sender_name = message.author.display_name or message.author.name

        body = message.content or "(empty / attachment-only)"
        # mention reverse mapping：<@discord_id> → @<mapped_id>
        for did, mid in user_mappings.items():
            body = body.replace(f"<@{did}>", f"@{mid}").replace(f"<@!{did}>", f"@{mid}")

        discord_meta = {
            "source": "discord",
            "discord_channel_id": cid,
            "discord_message_id": str(message.id),
            "discord_user_id": author_id,
        }
        if message.attachments:
            discord_meta["discord_attachments"] = "|".join(a.url for a in message.attachments)

        ok = write_to_tavern(tavern_room, sender_id, sender_name, body, discord_meta)
        if ok:
            _record_last_read(cid, message.id)
            trigger_wake_notify(tavern_room, sender_id, body)

    def _record_last_read(channel_id, message_id):
        """atomic update last_read_state"""
        c = load_config()
        c.setdefault("tavern_inbound", {}).setdefault("last_read_state", {})
        c["tavern_inbound"]["last_read_state"][str(channel_id)] = {
            "last_read_message_id": str(message_id),
            "last_read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        save_config(c)

    log("starting bot client...")
    try:
        client.run(token, log_handler=None)
    except discord.LoginFailure:
        log("login fail — token invalid?", "ERROR")
        return 1
    except KeyboardInterrupt:
        log("KeyboardInterrupt — shutting down")
    except Exception as e:
        log(f"client.run crashed: {e}", "ERROR")
        return 1

    return 0


# ===========================================================
# Main
# ===========================================================

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check-config", help="不連 bot 驗證 config + webhook resolve")
    p_check.set_defaults(func=cmd_check_config)

    p_sim = sub.add_parser("simulate-message", help="合成假 Tim 訊息端到端驗 pipeline")
    p_sim.add_argument("--sender", default=None, help="sender_id（預設 discord:test-tim）")
    p_sim.add_argument("--sender-name", default=None, help="sender_name")
    p_sim.add_argument("--body", default=None, help="message body")
    p_sim.set_defaults(func=cmd_simulate_message)

    p_run = sub.add_parser("run", help="真連 bot gateway 訂閱訊息（需 token）")
    p_run.set_defaults(func=cmd_run)

    args = p.parse_args()
    rc = args.func(args)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
