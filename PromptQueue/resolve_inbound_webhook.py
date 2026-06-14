#!/usr/bin/env python
"""
T14 — Webhook Pointer Resolver

把 input webhook URL → channel_id 解析後寫進 notify_config.json 的 tavern_inbound section。
驗證 T13 §1 設計（Webhook URL 當 channel pointer）。

用法：
    python resolve_inbound_webhook.py add <webhook_url> <tavern_room>
    python resolve_inbound_webhook.py list
    python resolve_inbound_webhook.py remove <webhook_id>

Discord API: GET /webhooks/{webhook_id}/{token} 回 webhook info（含 channel_id / guild_id）。
不需 Bot token；webhook token 即可。daemon bootstrap 跑一次拿 channel_id 寫進 cache，後續 bot 用 channel_id 訂閱。
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent.resolve()
CONFIG_PATH = HERE / "notify_config.json"
WEBHOOK_RE = re.compile(r"https://discord\.com/api/webhooks/(\d+)/([\w-]+)")


def parse_webhook(url):
    m = WEBHOOK_RE.match(url.strip())
    if not m:
        raise ValueError(f"invalid webhook URL: {url}")
    return m.group(1), m.group(2)


def fetch_webhook_info(url):
    req = urllib.request.Request(url, headers={"User-Agent": "EmblemOfValor-WebhookResolver/1.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def load_config():
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_add(args):
    wid, _ = parse_webhook(args.webhook_url)
    info = fetch_webhook_info(args.webhook_url)
    channel_id = info["channel_id"]
    guild_id = info.get("guild_id", "")

    cfg = load_config()
    inbound = cfg.setdefault("tavern_inbound", {
        "enabled": False,
        "bot_status": "pending-setup",
        "webhook_urls": [],
        "channel_mappings": [],
        "discord_user_mappings": {},
        "last_read_state": {},
    })

    # idempotent：同 webhook_id 已存在 → 更新 mapping
    inbound["webhook_urls"] = [
        e for e in inbound.get("webhook_urls", [])
        if parse_webhook(e["url"])[0] != wid
    ]
    inbound["webhook_urls"].append({
        "url": args.webhook_url,
        "tavern_room": args.tavern_room,
    })

    inbound["channel_mappings"] = [
        m for m in inbound.get("channel_mappings", [])
        if m.get("channel_id") != channel_id
    ]
    inbound["channel_mappings"].append({
        "channel_id": channel_id,
        "tavern_room": args.tavern_room,
        "webhook_id": wid,
        "guild_id": guild_id,
    })

    save_config(cfg)
    print(f"✓ resolved webhook {wid} → channel_id={channel_id}")
    print(f"  → tavern_room={args.tavern_room}")
    print(f"  guild_id={guild_id}")
    print(f"  config written: {CONFIG_PATH.relative_to(HERE.parent.parent)}")


def cmd_list(args):
    cfg = load_config()
    inbound = cfg.get("tavern_inbound", {})
    print(f"=== tavern_inbound ({CONFIG_PATH.name}) ===")
    print(f"enabled: {inbound.get('enabled', False)}")
    print(f"bot_status: {inbound.get('bot_status', 'N/A')}")
    mappings = inbound.get("channel_mappings", [])
    if not mappings:
        print("(no channel mappings)")
        return
    print(f"\n{len(mappings)} channel mapping(s):")
    for m in mappings:
        print(f"  channel_id={m['channel_id']} → tavern_room={m['tavern_room']} (webhook={m['webhook_id']})")


def cmd_remove(args):
    cfg = load_config()
    inbound = cfg.get("tavern_inbound", {})
    before = len(inbound.get("webhook_urls", []))
    inbound["webhook_urls"] = [
        e for e in inbound.get("webhook_urls", [])
        if parse_webhook(e["url"])[0] != args.webhook_id
    ]
    inbound["channel_mappings"] = [
        m for m in inbound.get("channel_mappings", [])
        if m.get("webhook_id") != args.webhook_id
    ]
    after = len(inbound["webhook_urls"])
    save_config(cfg)
    print(f"✓ removed webhook_id={args.webhook_id} ({before - after} entry/entries)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="resolve + register input webhook")
    p_add.add_argument("webhook_url")
    p_add.add_argument("tavern_room")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list current tavern_inbound mappings")
    p_list.set_defaults(func=cmd_list)

    p_remove = sub.add_parser("remove", help="remove webhook by id")
    p_remove.add_argument("webhook_id")
    p_remove.set_defaults(func=cmd_remove)

    args = p.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
