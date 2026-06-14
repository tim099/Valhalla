"""Discord WebhookClient — unified webhook send + 3-tier secret resolver.

Replaces scattered _resolve_webhook_urls / _send / _send_one impls in:
- notify_discord.py
- discord_inbound_daemon.py (post_webhook_ack)
- resolve_inbound_webhook.py

Three-tier URL resolution priority (high → low):
    1. ENV: scope_block["webhook_env_var"] env var (comma-separated multi-URL)
    2. FILE: scope_block["webhook_file"] (one URL per line, # = comment)
    3. CONFIG: scope_block["webhook_urls"] (list[str])

API surface:
    WebhookConfig(scope_block: dict, label: str, webhook_dir: Path | None = None)
    WebhookClient(config: WebhookConfig)
        .resolve_urls() -> tuple[list[str], str | None]
        .send(content, *, username=None, avatar_url=None, embeds=None) -> tuple[bool, list[tuple]]
        .send_one(url, *, ...) -> tuple[bool, str | None]
    from_config_block(scope_block: dict, label: str, webhook_dir: Path | None = None) -> WebhookClient

Convenience:
    `from AgentCommands._lib.discord_webhook import WebhookClient, from_config_block`

Notes on label:
    - 給 log 用，例如 "tavern" / "queue" / "wake" / "quest"
    - resolve_urls 的 source 字串會帶 label prefix（"tavern:env:VAR_NAME" 等）— 跟舊版
      notify_discord _resolve_webhook_urls 行為一致
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class WebhookConfig:
    """Webhook configuration block — typically from notify_config.json sub-block.

    Attributes:
        webhook_urls: 預設 broadcast 列表（CONFIG tier）
        webhook_file: 同 dir 下 secret 檔名稱（FILE tier）；空字串 = 不啟用 file tier
        webhook_env_var: 環境變數名（ENV tier）；空 = 不啟用 ENV tier
        label: log 標籤（"tavern" / "queue" / "quest" 等）
        webhook_dir: webhook_file 的 parent dir；預設 = AgentCommands/PromptQueue/
    """
    webhook_urls: list[str] = field(default_factory=list)
    webhook_file: str = ""
    webhook_env_var: str = ""
    label: str = "default"
    webhook_dir: Path | None = None


# ---------------------------------------------------------------------------
# Logger hook（caller 可注入；預設用 stdlib print to stderr）
# ---------------------------------------------------------------------------

# 區塊職責：日誌注入 — 讓 caller 用自家 logger 時不必每次傳參
# 物理意義：notify_discord 用自家 _log() 寫進 _drain.log；本 module 預設 stderr 印
# 數值影響：set_logger 全域生效（同 process 內）；fail-safe = print 不擋 send
import sys as _sys

_logger = lambda msg: print(f"[discord_webhook] {msg}", file=_sys.stderr)


def set_logger(logger_fn) -> None:
    """注入自家 logger（function taking single str arg）。"""
    global _logger
    _logger = logger_fn


# ---------------------------------------------------------------------------
# WebhookClient
# ---------------------------------------------------------------------------

class WebhookClient:
    """Unified Discord webhook client — 3-tier URL resolver + send/broadcast。

    Lifecycle: 建一次 instance per webhook config block；多次呼叫 send 共用 resolution。
    Resolve 結果不 cache — 每次 send 都 re-resolve（讓 ENV / FILE 變更立刻生效，trade-off
    為每次小量 IO 但避免 stale URL）。"""

    def __init__(self, config: WebhookConfig):
        self.config = config

    # ---------- URL resolution ----------

    def resolve_urls(self) -> tuple[list[str], str | None]:
        """3-tier fallback：ENV > FILE > CONFIG。Returns (urls, source) where
        source is e.g. 'tavern:env:PROMPTQUEUE_TAVERN_WEBHOOK' / 'tavern:file:_tavern_webhook.txt'
        / 'tavern:config' / None (no URL anywhere)."""
        cfg = self.config
        label = cfg.label

        # Tier 1: ENV
        if cfg.webhook_env_var:
            env_url = os.environ.get(cfg.webhook_env_var, "").strip()
            if env_url:
                urls = [u.strip() for u in env_url.split(",") if u.strip().startswith("https://")]
                if urls:
                    return urls, f"{label}:env:{cfg.webhook_env_var}"
                _logger(f"[{label}] env {cfg.webhook_env_var} 內容無合法 https URL — fallback to file/config")

        # Tier 2: FILE
        if cfg.webhook_file:
            base_dir = cfg.webhook_dir or Path(__file__).resolve().parent.parent / "PromptQueue"
            p = base_dir / cfg.webhook_file
            if p.exists():
                try:
                    urls = []
                    for line in p.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if line.startswith("https://"):
                            urls.append(line)
                        else:
                            _logger(f"[{label}] {cfg.webhook_file} 一行不是 https URL，跳過：{line[:30]!r}")
                    if urls:
                        return urls, f"{label}:file:{cfg.webhook_file}"
                except Exception as e:
                    _logger(f"[{label}] {cfg.webhook_file} read fail：{e}")

        # Tier 3: CONFIG
        if isinstance(cfg.webhook_urls, list):
            urls = [u for u in cfg.webhook_urls if isinstance(u, str) and u.startswith("https://")]
            if urls:
                return urls, f"{label}:config"

        return [], None

    # ---------- Send ----------

    def send_one(
        self,
        webhook_url: str,
        content: str | None = None,
        *,
        username: str | None = None,
        avatar_url: str | None = None,
        embeds: list[dict] | None = None,
    ) -> tuple[bool, str | None]:
        """POST 到單一 Discord webhook。
        回 (ok, error_msg|None)。"""
        body: dict[str, Any] = {}
        if content:
            body["content"] = content
        if username:
            body["username"] = username
        if avatar_url:
            body["avatar_url"] = avatar_url
        if embeds:
            body["embeds"] = embeds   # Discord 限制：每 POST 最多 10 embeds
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AgentCommands-WebhookClient/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                ok = 200 <= resp.status < 300
                return ok, None if ok else f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            return False, f"HTTPError {e.code}"
        except urllib.error.URLError as e:
            return False, f"URLError {e.reason}"
        except Exception as e:
            return False, f"{type(e).__name__}: {e}"

    def send(
        self,
        content: str | None = None,
        *,
        username: str | None = None,
        avatar_url: str | None = None,
        embeds: list[dict] | None = None,
    ) -> tuple[bool, list[tuple[str, bool, str | None]]]:
        """Broadcast 到 resolve_urls() 拿到的所有 URL。
        回 (any_ok, results) where results = list of (short_url_id, ok, error_msg)."""
        urls, source = self.resolve_urls()
        if not urls:
            return False, []
        results: list[tuple[str, bool, str | None]] = []
        any_ok = False
        for url in urls:
            url_id = "..." + url[-12:] if len(url) > 12 else url
            ok, err = self.send_one(url, content, username=username, avatar_url=avatar_url, embeds=embeds)
            results.append((url_id, ok, err))
            if ok:
                any_ok = True
        return any_ok, results

    def send_to_urls(
        self,
        urls: list[str],
        content: str | None = None,
        *,
        username: str | None = None,
        avatar_url: str | None = None,
        embeds: list[dict] | None = None,
    ) -> tuple[bool, list[tuple[str, bool, str | None]]]:
        """Broadcast 到顯式給的 URL list（不跑 resolve_urls）— 給 caller 已自行 resolve 用。"""
        if isinstance(urls, str):
            urls = [urls]
        results: list[tuple[str, bool, str | None]] = []
        any_ok = False
        for url in urls:
            url_id = "..." + url[-12:] if len(url) > 12 else url
            ok, err = self.send_one(url, content, username=username, avatar_url=avatar_url, embeds=embeds)
            results.append((url_id, ok, err))
            if ok:
                any_ok = True
        return any_ok, results


# ---------------------------------------------------------------------------
# Convenience factory
# ---------------------------------------------------------------------------

def from_config_block(
    scope_block: dict,
    label: str,
    webhook_dir: Path | None = None,
) -> WebhookClient:
    """從 dict（typically 從 notify_config.json 子塊）建 WebhookClient。

    Example:
        cfg = json.load(open("notify_config.json"))
        tavern_client = from_config_block(cfg["tavern_mirror"], label="tavern")
        ok, results = tavern_client.send("hello", username="bot", avatar_url=...)
    """
    return WebhookClient(WebhookConfig(
        webhook_urls=scope_block.get("webhook_urls", []) or [],
        webhook_file=scope_block.get("webhook_file", "") or "",
        webhook_env_var=scope_block.get("webhook_env_var", "") or "",
        label=label,
        webhook_dir=webhook_dir,
    ))


# ---------------------------------------------------------------------------
# CLI smoke entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # smoke：從 notify_config.json 拿 tavern_mirror block 建 client，印 resolve_urls 結果
    import sys
    from . import tavern_paths as _tp  # type: ignore
    cfg_path = _tp.NOTIFY_CONFIG_PATH
    if not cfg_path.is_file():
        print(f"notify_config.json not found at {cfg_path}", file=sys.stderr)
        sys.exit(1)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    for label, block in [
        ("queue", cfg),
        ("tavern", cfg.get("tavern_mirror", {})),
        ("quest", (cfg.get("tavern_mirror", {}) or {}).get("quest_routing", {})),
        ("wake", cfg.get("wake_notify", {})),
    ]:
        client = from_config_block(block or {}, label=label, webhook_dir=_tp.PROMPT_QUEUE_DIR)
        urls, source = client.resolve_urls()
        print(f"[{label}] {len(urls)} URL(s), source={source}")
