"""secrets_crypto.py — [DEPRECATED shim] forward 到 UCL_Core ucl_secrets_crypto.

# 區塊職責：保留 EOV 既有 import 入口 (encrypt/decrypt 回 bytes)，邏輯全委派 UCL_Core 通用 lib。
# 物理意義：原本這支自己做 TKN1 KDF+Fernet；Secret Manager Phase 1 把加解密抽到 UCL_Core
#          ucl_secrets_crypto.py (TKN2 + hint metadata)。本檔降級為相容 shim，舊 importer 不必改。
# 數值影響：encrypt 現在輸出 TKN2 (含空 hint/label)；decrypt 同時吃 TKN1/TKN2，回純 bytes (剝掉 metadata)。

⚠ DEPRECATED：新程式請直接 import UCL_Core 的 ucl_secrets_crypto (含 hint/label/read_metadata)：
    sys.path.insert(0, "<UCL_Core>/Tools~/AgentCommands/_lib")
    import ucl_secrets_crypto
本 shim 只為 backward-compat 保留 (舊 `from AgentCommands.Tools import secrets_crypto`)。
"""
from __future__ import annotations

import sys
from pathlib import Path

# 區塊職責：定位 UCL_Core lib 並 import
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
# T-PATH-02: UCL_Core _lib 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core。
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
_UCL_LIB = _tp.UCL_LIB_DIR
sys.path.insert(0, str(_UCL_LIB))

import ucl_secrets_crypto as _impl  # noqa: E402

# 區塊職責：re-export 常數 (舊 caller 可能讀 MAGIC / KDF_ITERATIONS)
MAGIC = _impl.MAGIC_V1            # 舊版 magic 常數仍指 TKN1 (歷史相容)
KDF_ITERATIONS = _impl.KDF_ITERATIONS
SALT_LEN = _impl.SALT_LEN


def encrypt(plaintext: bytes, passphrase: str) -> bytes:
    """[DEPRECATED] 加密 → TKN2 bytes (空 hint/label)。新程式請用 ucl_secrets_crypto.encrypt。"""
    return _impl.encrypt(plaintext, passphrase)


def decrypt(ciphertext: bytes, passphrase: str) -> bytes:
    """[DEPRECATED] 解 TKN1/TKN2 → 純 plaintext bytes (剝 metadata)。passphrase 錯 → ValueError。"""
    return _impl.decrypt(ciphertext, passphrase).plaintext


def _selftest():
    import os
    pw = "test-passphrase-12345"
    for s in (b"", b"hello", os.urandom(256)):
        assert decrypt(encrypt(s, pw), pw) == s, f"round-trip mismatch len={len(s)}"
        try:
            decrypt(encrypt(s, pw), pw + "x")
        except ValueError:
            pass
        else:
            raise AssertionError("wrong passphrase did not raise")
    print("[OK] secrets_crypto (deprecated shim) forward self-test passed")


if __name__ == "__main__":
    _selftest()
