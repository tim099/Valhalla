import os
import json
import glob
import io
import sys

# Ensure UTF-8 support for printing and processing
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 路徑解析 — 用 _lib.repo_root 共用 helper 錨定主專案根（拔除舊寫死絕對路徑；T-PATH-RESOLVE T04）。
# 物理意義：ROOT 原為 r"D:\Unity\EmblemOfValor"（換機器 / 換 clone 就死）；改由 .git-walk 動態解析。
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib.repo_root import find_repo_root  # noqa: E402

# Configure local path references
ROOT = find_repo_root()
LOC_PATH = os.path.join(ROOT, r"CardGame\Assets\.BuiltinModules\ModulesRoot\Modules\Core\ModResources\LocalizeDatas\Default\zh-Hant.txt")

CORE_SRC = os.path.join(ROOT, r"CardGame\Assets\.BuiltinModules\ModulesRoot\Modules\Core\UCL_Assets\RCG_CharacterData")
FATE_SRC = os.path.join(ROOT, r"CardGame\Assets\.BuiltinModules\ModulesRoot\Modules\Fate\UCL_Assets\RCG_CharacterData")

TARGET_DIR = os.path.join(ROOT, r"CardGame\Assets\UCL\UCL_Core\Templates~\Assets\.BuiltinModules\ModulesRoot\Modules\Core\UCL_Assets\UCL_ChatTavernIdentityAsset")

def load_localization(path):
    """Loads binary cache txt from Unity export format into a high-fidelity dict."""
    loc_map = {}
    if not os.path.exists(path):
        print(f"[Warning] Localization file not found at {path}")
        return loc_map
        
    with open(path, "r", encoding="utf-8-sig") as f:
        line = f.readline().strip()
        if not line: return loc_map
        count = int(line)
        
        for i in range(count):
            try:
                len_line = f.readline().strip()
                if not len_line: break
                parts = len_line.split(',')
                klen, vlen = int(parts[0]), int(parts[1])
                
                # Direct character read mapping exactly mirroring C# char counts
                key_str = f.read(klen)
                f.read(1) # Consume colon
                val_str = f.read(vlen)
                f.read(1) # Consume newline
                
                # Replace physical \\n sequences back into logical newlines
                loc_map[key_str] = val_str.replace('\\n', '\n')
            except Exception:
                break
    print(f"[Success] Parsed {len(loc_map)} entries from Localization Cache.")
    return loc_map

def get_localized(val_block, loc_map):
    """Resolves explicit value vs lookup keys from RCG_LocalizeData object structure."""
    if not val_block: return ""
    ltype = val_block.get("LocalizeType", "Value")
    if ltype == "Value":
        return val_block.get("LocalizeKey", val_block.get("Name", ""))
    
    key = val_block.get("LocalizeKey", "")
    if key in loc_map:
        return loc_map[key]
    # Return the fallback default Name if lookup fails
    return val_block.get("Name", key)

def get_avatar_id(avatar_block):
    """Handles critical schema polymorphism: raw string vs object structure."""
    if not avatar_block: return "Default"
    entry = avatar_block.get("SpriteAssetEntry", "")
    
    # Case 1: Direct string (e.g. "Avatars_mage.png")
    if isinstance(entry, str):
        if not entry: return "Default"
        # Strip file extension
        return os.path.splitext(entry)[0]
        
    # Case 2: Nested Object (e.g. { "ID": "Avatar_Aigis" })
    if isinstance(entry, dict):
        return entry.get("ID", "Default")
        
    return "Default"

def main():
    print("Starting RCG to Chat Tavern Identity Sync Protocol...")
    
    loc_map = load_localization(LOC_PATH)
    
    if not os.path.exists(TARGET_DIR):
        print(f"Creating target directory: {TARGET_DIR}")
        os.makedirs(TARGET_DIR, exist_ok=True)
        
    # Gather all candidate JSONs from Core & Fate source module directories
    source_dirs = [CORE_SRC, FATE_SRC]
    processed = 0
    
    for src in source_dirs:
        if not os.path.exists(src): continue
        print(f"\nScanning source folder: {src}")
        
        for json_path in glob.glob(os.path.join(src, "*.json")):
            filename = os.path.basename(json_path)
            if filename.startswith("."): continue # Skip hidden/meta files
            
            try:
                with open(json_path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                
                char_id = data.get("ID", os.path.splitext(filename)[0])
                
                # Safety skip for system placeholder/null datas if detected
                if char_id == "None" or char_id == "New Character": continue
                
                unit_data = data.get("UnitData", {})
                
                # Extraction and Mapping
                cname = get_localized(unit_data.get("Name", {}), loc_map)
                intro = get_localized(unit_data.get("CharacterIntro", {}), loc_map)
                aid = get_avatar_id(unit_data.get("Avatar", {}))
                
                # Construct Target Representation
                identity_asset = {
                    "AvatarSprite": aid,
                    "RoleSettings": f"{cname}\n\n{intro}",
                    "ColorHex": "#E6B800", # RCG standard Gold
                    "Tags": ["character", "RCG"]
                }
                
                out_path = os.path.join(TARGET_DIR, f"{char_id}.json")
                with open(out_path, 'w', encoding='utf-8') as outf:
                    json.dump(identity_asset, outf, ensure_ascii=False, indent="\t")
                
                print(f"  [+] Synced: {char_id.ljust(20)} -> Avatar: {aid.ljust(20)}")
                processed += 1
                
            except Exception as e:
                print(f"  [!] Error processing {filename}: {e}")

    print(f"\n--- ALL DONE ---")
    print(f"Total identities deployed to Templates~: {processed}")

if __name__ == "__main__":
    main()
