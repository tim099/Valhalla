#!/usr/bin/env python3
# 區塊職責：workflow 識別層共用解析器 — slug 正規化 + target 位置解析，供 workflow_patch / workflow_notes 共用。
# 物理意義：
#   summit 拍磚指出（2026-06-17 眉批層 task）：patch 工具與 note 工具若各自認定「同一個 workflow」，
#   會產生 Identity-layer 層次混淆（同名≠同身份家族的鏡像）。因此「slug 解析器本身」必須單一來源，
#   不只共用 repo_root。本檔把兩件事收斂成一處：
#     (1) normalize_slug —— 把人類輸入的 workflow 名字壓成 file-safe 穩定 slug（主鍵 / 目錄名）。
#     (2) resolve_target —— 把一條 note/patch 記的「位置」字串解析成真實檔案，供 doctor 偵測斷鏈孤兒。
#   slug 與 target 刻意分兩件事（抄 awakening session_key=identity / claim_origin=location split）：
#     slug 是顯式穩定身份、生一次固定不隨改名變動；target 是會變的位置，rename 只重指 target、slug 不動。
# 數值影響：純字串運算 + os.path 探測，不寫任何 asset / token。

import os
import re

# 區塊職責：把本檔所在位置反推主專案根（與 repo_root 同錨定邏輯，避免循環 import 也能獨立用）
# 物理意義：target 解析需要一個絕對基準把 repo-relative 路徑釘到主根；沿用「同層有 AgentCommands/+CardGame/」錨。
# 數值影響：純讀檔探測。
from _lib.repo_root import find_repo_root


# 區塊職責：workflow 名字 → file-safe 穩定 slug
# 物理意義：slug 是眉批層 / 補丁層的主鍵與目錄名。一律小寫、非 [a-z0-9_-] 壓成單一 '-'、去頭尾 '-'。
#          ⚠ slug 應由人類「顯式命名一次」當穩定身份，**不要**用 workflow 檔名自動生成 —— 檔名會 rename，
#            slug 不該跟著變（否則改名那天鏈接靜默斷、孤兒 note 沒人發現，正是 summit 砸的那條）。
#          本函式只負責「把給定的 slug 字串正規化成 file-safe 形式」，不負責「從檔名推 slug」。
# 數值影響：純字串；空字串 fallback 'unnamed'。
def normalize_slug(name: str) -> str:
    s = (name or "").strip().lower()
    s = re.sub(r"[^a-z0-9_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed"


# 區塊職責：解析一條 target 位置字串 → 真實檔案是否存在（doctor 用，防 silent 孤兒）
# 物理意義：target 是「這條 note/patch 所標註的 workflow 實際住哪」。支援兩種形式：
#   (a) skill§section ——「skill:<skill-name>」或「skill:<skill-name>#<section>」
#        → 解析到 <repo>/.claude/skills/<skill-name>/SKILL.md；section 僅供人看，存在性只驗 SKILL.md。
#        （這形式是 summit 點的 dogfood 鐵證：第一條 note 標的是 skill 的 §section、不是檔案，
#          target 模型必須吃得下非檔案 target。）
#   (b) 其餘一律當 repo-relative 路徑（檔案或目錄）→ 解析到 <repo>/<target>。
# 數值影響：純 os.path 探測；回 (ok, resolved_abs, kind, reason)，不改任何檔。
def resolve_target(target: str, repo_root: str | None = None) -> tuple[bool, str, str, str]:
    root = repo_root or find_repo_root()
    t = (target or "").strip()
    if not t:
        return (False, "", "empty", "target 為空字串")

    # 形式 (a)：skill§section
    if t.lower().startswith("skill:"):
        rest = t[len("skill:"):]
        skill_name = rest.split("#", 1)[0].strip().strip("/")
        section = rest.split("#", 1)[1].strip() if "#" in rest else ""
        skill_md = os.path.join(root, ".claude", "skills", skill_name, "SKILL.md")
        if os.path.isfile(skill_md):
            label = f"skill:{skill_name}" + (f"#{section}" if section else "")
            return (True, skill_md, "skill-section", f"OK → {label}")
        return (False, skill_md, "skill-section", f"skill '{skill_name}' 的 SKILL.md 不存在")

    # 形式 (b)：repo-relative 路徑
    abs_path = os.path.join(root, t)
    if os.path.exists(abs_path):
        kind = "dir" if os.path.isdir(abs_path) else "file"
        return (True, abs_path, kind, f"OK → {t}")
    return (False, abs_path, "file", f"路徑不存在: {t}")
