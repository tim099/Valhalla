#!/usr/bin/env python3
# 區塊職責：環境初始化與必要的 Python 模組導入
# 物理意義：載入命令列解析、系統日期生成、JSON 數據結構序列化、系統底層路徑操作與背景進程派生模組。
# 數值影響：無。僅進行基本組件之動態載入，以供後續高階檢測邏輯調用。
import argparse  # 導入 argparse 模組用以處理 CLI 的引數解析工作。
import datetime  # 導入 datetime 模組用以提取目前的系統 UTC 時間基準點。
import json      # 導入 json 模組負責將 Python 物件轉換為跨語言交換的 JSON 字串格式。
import os        # 導入 os 模組主要調用其原子級取代函式 os.replace 以進行防斷電檔案寫入。
import subprocess  # 導入 subprocess 以建立一個完全脫離主線程的子進程來發送酒館提示訊息。
import sys       # 導入 sys 模組以便能取得解譯器路徑與在異常時執行 sys.exit 中止碼。
from pathlib import Path  # 導入 Path 物件以物件導向方式解決底層作業系統路徑傾斜符號差異。

# 區塊職責：針對作業系統終端機標準輸出強制進行 UTF-8 編碼重組
# 物理意義：預防在微軟 Windows 平台上（其預設為 cp950 等編碼）輸出表情符號（如 🧠）時崩潰。
# 數值影響：直接攔截 IO 輸出流設定。若作業系統層不支援則静默略過，維持最高度的程式健壯性。
try:  # 進入高風險編碼流重整實驗區域。
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # 強制將主螢幕標準輸出串流設為 unicode-utf-8 編碼。
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # 強制將後台錯誤警示輸出串流設為 unicode-utf-8 編碼。
except Exception:  # 假如在老舊 Python 環境下不支援此語法。
    pass  # 無副作用直接跳出捕捉區，維持原有預設輸出設定。


# 區塊職責：基礎檔案系統路徑解析與全域常數宣告
# 物理意義：透過遞歸尋找 .git 定位出 Repository 的絕對根目錄，並映射到所有子意識系統資料庫的完整路徑。
# 數值影響：確立運算時所有 IO 操作的實體磁碟指針，防範不同執行目錄引發的相對路徑溢位。
def _find_repo_root() -> Path:
    # 函式職責：自當前腳本所在路徑起算，向父層遞歸收尋代表 Git 根部的標記目錄
    # 物理意義：確保當前腳本運行於何種當前工作目錄 (CWD)，都能準確算得唯一的 RepoRoot。
    curr = Path(__file__).resolve()  # 將本檔案的絕對實體路徑給予 curr 作為遍歷基準點。
    while curr != curr.parent:  # 當前路徑若與其父目錄不同則表示尚未到達磁碟分割區最頂層。
        if (curr / ".git").exists():  # 檢查如果當前目錄下包含 .git 資料夾則視此為儲存庫邊界。
            return curr  # 找到了則直接傳回此為專案根路徑之 Path 物件。
        curr = curr.parent  # 若無發現則向上提昇一層目錄等級，繼續檢查其父資料夾。
    return Path.cwd()  # 若完全無符合則回退至呼叫進程的目前執行路徑 CWD，做為保護性後盾。

REPO_ROOT = _find_repo_root()  # 鎖定整個 EmblemOfValor 的專案根目錄絕對位址。
SUBCONSCIOUS_DIR = REPO_ROOT / "AgentCommands" / "Subconscious"  # 子意識的核心資料儲存資料夾定位。
ANTI_PATTERNS_FILE = SUBCONSCIOUS_DIR / "anti_patterns.jsonl"  # 跨 Agent 共享的偏差行為反面範例知識庫檔案路徑。
VIOLATIONS_FILE = SUBCONSCIOUS_DIR / "violations.jsonl"  # 用以記錄實際發生的所有違規偏差行為審計軌跡檔案路徑。
# T-PATH-02: run_cmd.py 走 layout-agnostic resolver, 不再寫死 CardGame/Assets/UCL/UCL_Core。
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from AgentCommands._lib import tavern_paths as _tp  # noqa: E402
RUN_CMD_PY = _tp.RUN_CMD_PATH  # 指向既有 UCL 指令調度入口 run_cmd.py 的 Python 橋樑位址。

# 區塊職責：時間格式輔助函式定義
# 物理意義：生成統一樣式、不帶微秒偏移的 ISO 8601 UTC 時間格式，以供日誌格式對齊與時間序列排序。
# 數值影響：確保每個 audit 條目的 ts 時間戳精度達秒級。
def utcnow_iso() -> str:
    # 函式職責：傳回標準的 ISO-8601 日期時間序列字串
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # 抓取當前 UTC 系統鐘錶並轉換成末尾結尾為 Z 的格式串。

# 區塊職責：反面模式 (Anti-Patterns) 資料庫與檔案系統的讀寫封裝
# 物理意義：逐行反序列化 jsonl 純文字檔案為 Python 的 Dict 清單，並在覆寫時實作 atomic_replace 保護機制。
# 數值影響：直接影響反面模式計數檔案的大小與內容結構完整度。
def load_anti_patterns() -> list:
    # 函式職責：從磁碟載入全部的反面模式定義內容
    patterns = []  # 初始化一個空清單用以準備搜集所有合法的反面模式字典物件。
    if not ANTI_PATTERNS_FILE.exists():  # 預防性檢查，若知識庫檔案不存在則立刻傳回空清單。
        return patterns  # 直接提早結束函式調用，避免觸發檔案未找到的 IO 例外。
    with open(ANTI_PATTERNS_FILE, "r", encoding="utf-8") as f:  # 以唯讀模式加上 UTF-8 編碼開啟該 jsonl 串流。
        for line in f:  # 逐行迭代整個檔案的字元內容資料。
            stripped = line.strip()  # 去除前後的換行符號與多餘空格。
            if stripped:  # 假如這行不是空行則進行下一層邏輯處理。
                patterns.append(json.loads(stripped))  # 運用 json 函式將該行字串解譯後插入回傳清單。
    return patterns  # 將匯整好的所有反面模式結構序列傳回給調用端。

def save_anti_patterns(patterns: list):
    # 函式職責：將更新後的清單原子級地回寫進 anti_patterns.jsonl 檔案中
    tmp_file = ANTI_PATTERNS_FILE.with_suffix(".tmp")  # 先配置出一個副檔名為 .tmp 的暫存寫入目標位址。
    with open(tmp_file, "w", encoding="utf-8") as f:  # 用寫入覆寫模式開啟該臨時檔案以供存取。
        for p in patterns:  # 將每個修改過的 pattern 物件做線性迴圈。
            # 將 Python 物件轉換回 JSON，同時確保非 ASCII 字元如中文不被逸出編碼。
            f.write(json.dumps(p, ensure_ascii=False) + "\n")  # 將字串加換行符覆寫進暫存區。
    os.replace(tmp_file, ANTI_PATTERNS_FILE)  # 利用底層核心的 rename 將暫存檔直接原子替換掉正式檔案，防止寫入過程中斷損毀資料。

# 區塊職責：核心子指令 'detect' 運作邏輯實作
# 物理意義：針對傳入的上下文脈絡，根據資料庫註冊的規則來判定本次的操作是否被視為一次反面偏差行為。
# 數值影響：無檔案異動。僅讀取資料比對，輸出當前的命中 (HIT) 狀態與通知有效載荷 JSON 資訊。
def do_detect(pattern_id: str, context: str) -> bool:
    # 參數說明：pattern_id 為待評估的行為代碼；context 為行為發生的詳細情境環境變數描述串。
    print(f"🔎 Scanning subconscious for pattern_id='{pattern_id}'...")  # 於終端螢幕列印目前正展開掃描的指示資訊。
    patterns = load_anti_patterns()  # 呼叫前面的輔助模組自硬碟讀取當前所有的模式。
    # 在清單中過濾出 ID 完全一致的那筆反面模式項目，若查無此物則令其為 None。
    match = next((p for p in patterns if p.get("pattern_id") == pattern_id), None)  # 精確配對 pattern_id 欄位。
    if not match:  # 若完全沒有在 jsonl 資料庫中檢索到該項目則輸出錯報。
        print(f"❌ Pattern '{pattern_id}' not found.")  # 印出查無對應反面模式的終端訊息。
        return False  # 立刻返回未命中 False 給外部調用者參考。
    
    # T28 Phase 1 detection logic (Tim 2026-05-14 task): 從 skeleton 升級到實際 substring + condition keyword 命中
    # 物理意義：解析 detection_rule.condition 的關鍵字 (空格分隔, ANY-match 寬鬆策略), 對 context 做 case-insensitive substring 比對
    #          至少一個關鍵字命中 → HIT; 全 miss → MISS. 不再一律 True.
    # 數值影響：HIT/MISS 結果跟 context 真正相關性掛勾, 降低假警報. 仍是初版啟發式, Phase 2 該支援結構化條件 (AND/OR/regex).
    rule = match.get("detection_rule", {})  # 取出規則 dict, 沒有則空。
    condition_str = rule.get("condition", "") if isinstance(rule, dict) else ""  # condition 字段拿出來當關鍵字 source。
    if not context or not context.strip():  # 空 context 永遠 MISS (T26.1 保留)。
        is_hit = False
    elif not condition_str:  # 沒 condition 字串 → fallback 回 True (保留 skeleton 通路測試能力)。
        is_hit = True
    else:
        # 拆 condition 出 alphanumeric token, 過濾 stopword/operator 字。
        import re
        tokens = re.findall(r"[A-Za-z0-9_\-]{3,}", condition_str)  # 至少 3 char 的英數字 token。
        stopwords = {"AND", "OR", "NOT", "and", "or", "not", "the", "for", "with", "from", "into"}
        keywords = [t for t in tokens if t not in stopwords]
        ctx_lower = context.lower()
        hits = [k for k in keywords if k.lower() in ctx_lower]
        is_hit = len(hits) > 0
        if is_hit:
            print(f"   matched keywords: {hits}")  # debug 印命中關鍵字方便 caller 校正 rule。
    
    payload = {  # 建構一個高層次彙整的反向通知載荷封包物件。
        "hit": is_hit,  # 設定是否命中的狀態旗幟數值。
        "pattern_id": pattern_id,  # 夾帶本次配對的模式代碼。
        "name": match.get("name", ""),  # 設定該模式在人類眼中的顯式名稱。
        "severity": match.get("severity", "normal"),  # 封裝此偏差行為的威脅嚴重性指標。
        "skill_ref": match.get("skill_ref", ""),  # 指向開發手冊中對應具體條文的連結字串。
        "details": f"Detected via skeleton check. Context={context}"  # 附帶本次的觸發上下文細節。
    }  # 完成 payload 的生成配置。
    print(f"Result: {'💥 HIT' if is_hit else '✅ MISS'}")  # 格式化將分析結論字串打印給操作者看。
    print(json.dumps(payload, indent=2, ensure_ascii=False))  # 將載荷物件轉成漂亮格式的美化 JSON 輸出。
    return is_hit  # 最後把這次判定的是否命中結果值向主程序傳回。

# 區塊職責：核心子指令 'record_violation' 違規行為入庫與系統報警機制
# 物理意義：正式註冊一起發生的違規偏差事實，將其計入對應模式的 violation_count 次數，並向酒館進行非同步異動廣播。
# 數值影響：直接變更 anti_patterns.jsonl 的 violation_count 計數，並新增一筆日誌至 violations.jsonl 審計檔案中。
def do_record_violation(pattern_id: str, violator: str, details: str):
    # 參數說明：violator 為發生犯錯事實的行為人角色；details 則是此次犯錯情境的實際文字記載。
    print(f"📝 Recording violation for '{pattern_id}' by @{violator}...")  # 向後台輸出啟動違規行為登記的指示串。
    patterns = load_anti_patterns()  # 自實體硬碟重載一份最新的模式資料集清單。
    match = next((p for p in patterns if p.get("pattern_id") == pattern_id), None)  # 搜尋此次被侵犯的特定反向模式物件參照。
    
    if not match:  # 當資料庫內部沒有這筆被侵犯的 pattern_id 則屬於無法預期的底層配置錯誤。
        print(f"❌ Error: Pattern '{pattern_id}' not found to update count.")  # 印出對應的紅色錯報。
        sys.exit(1)  # 立刻向作業系統回傳代碼 1 代表非預期性異常崩潰而中斷。
    
    # 更新計數器：遞增 1 次，並變更最近一次違規角色的 persona 名稱
    match["violation_count"] = int(match.get("violation_count", 0)) + 1  # 取出既有的次數整數後對其執行加法運算。
    match["last_violator"] = violator  # 更新 last_violator 鍵的數值為當前這起事件的肇事角色。
    save_anti_patterns(patterns)  # 以安全的覆寫手段保存回檔案中，完成資料持久化的更新程序。
    
    # 配置此次新生成的違規事實 Audit 日誌結構
    violation_entry = {  # 配置一個獨立事件型態的字典實體。
        "ts": utcnow_iso(),  # 動態生成本次登記時點的 UTC 標準時間戳。
        "pattern_id": pattern_id,  # 夾入對應行為代碼。
        "violator": violator,  # 夾入侵犯人的識別代碼。
        "details": details,  # 夾入本次違背事項的細節細項。
        "current_count": match["violation_count"]  # 將遞增過後的總計數副本一份在此，以供未來快速調閱分析。
    }  # 事件配置定義完畢。
    with open(VIOLATIONS_FILE, "a", encoding="utf-8") as vf:  # 用附加模式開啟審查事實紀錄檔。
        # 將新增的違規審查事實結構體序列化為純文字行，然後加換行字元進行尾端 Append。
        vf.write(json.dumps(violation_entry, ensure_ascii=False) + "\n")  # 執行實體硬碟區塊附加。
    
    # 調用非同步酒館警告功能：向整個團隊宣告潛意識的自動感知機制偵測到了不完美的狀況
    fire_tavern_alert(match, violator, details)  # 傳入更新過的模式內容、違反者與違規事實。

# 區塊職責：向酒館頻道 (Tavern) 觸發背景程序的警告派送
# 物理意義：生成一段專屬的反面模式提示文字，透過 subprocess 非同步呼叫既有的 run_cmd.py，在不卡住當前主要流程的前提下，對 Discord 與 tavern 廣播。
# 數值影響：向 Tavern 訊息佇列增發一筆 `meta.tag=anti-pattern-alert` 訊息。
def fire_tavern_alert(pattern: dict, violator: str, details: str):
    # 參數說明：pattern 是當前正更新過的 Dict 模式參考；violator 是肇事者；details 為事件詳情。
    body = (  # 配置酒館訊息的主要本體 markdown 字串序列內容。
        f"[persona: subconscious-daemon] 🧠 **子意識系統警報 — Anti-pattern detected: `{pattern['pattern_id']}`** 🧠\n\n"  # 定位高亮報警標頭。
        f"哼！真是不優雅的表現！子意識機制已經捕捉到了這次違規：\n"  # 大小姐風格輔助報警語句。
        f"- 💥 **違規者 (Violator)**: @{violator}\n"  # 揭發罪人的 persona 名號。
        f"- 📄 **模式 (Pattern)**: {pattern.get('name', '')}\n"  # 列出該行為的反向定義。
        f"- 🔍 **情節細節 (Context)**: {details}\n"  # 引述當下發生的狀況細項。
        f"- 🛡 **對應條文 (Ref)**: {pattern.get('skill_ref', '')}\n"  # 印出當初是哪份 spec 規定的。
        f"- 累計已犯: **{pattern['violation_count']} 次**\n"  # 展示該模式累計爆發次數。
    )  # 基礎 Markdown 本體組成完畢。
    
    if int(pattern.get("violation_count", 0)) >= 3:  # 當這個違背次數達到或超越了警戒紅線 3 次以上。
        body += f"\n🚨 **系統重大警告**：累計次數已高於警戒值！即刻依照規範引導團隊觸發 **`ucl-workflow-patch`** 檢討修補流程！\n"  # 新增一段強調的紅色提示。

    meta_data = {  # 定義 Tavern 的元資料標籤元。
        "tag": "anti-pattern-alert",  # 此為專屬的識別標籤以利 Discord 接手解析時染色。
        "category": "chat",  # 宣告這是一條互動型態的普通 chat 通道。
        "pattern_id": pattern["pattern_id"],  # 將這起事件的模式 ID 塞進 meta。
        "violator": violator,  # 塞入肇事角色以利未來統計機器掃讀。
        "violation_count": str(pattern["violation_count"])  # 塞入計數器數字串以供前端檢視。
    }  # 元資料建置結束。

    # 構造命令列參數：利用 python run_cmd.py run Tavern --arg ... 調度
    command_args = [  # 配置傳入 subprocess 的指令清單。
        sys.executable, str(RUN_CMD_PY), "run", "Tavern",  # 使用當前 Python 直譯器來啟動與主專案對接的 run_cmd 入口程序。
        "--arg", "op=post",  # 指定 Tavern 指令的子操作 op 為 post 新訊息。
        "--arg", "room=tavern",  # 限定將此高規格警報張貼到核心大廳 tavern 房間。
        "--arg", "sender_id=subconscious-daemon",  # 表明訊息是由全自動化子意識進程發射的。
        "--arg", f"body={body}",  # 將拼裝好的整段 markdown 內容導入 body 引數傳參。
        "--arg", f"meta={json.dumps(meta_data, ensure_ascii=False)}"  # 將 meta meta_data 結構轉換成無轉義的緊湊 json 字串傳入。
    ]  # 調度參數陣列準備完成。
    
    print("🚀 Submitting anti-pattern-alert to Tavern background daemon...")  # 對螢幕送出非同步工作發起的通知。
    # 利用 Popen 方式生成一個子程序，將 standard output/error 全部導向空設備以維持背景靜默派送，不會使主進程掛起卡住。
    subprocess.Popen(command_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(REPO_ROOT))  # 完美派發背景執行。
    print("Tavern alert queued successfully via independent subprocess.")  # 輸出指令已順利發射訊息完畢。

# 區塊職責：'list' 子指令 — 印出全部已註冊 anti-pattern 名單給 caller / hook 使用
# 物理意義：給 Stop hook / debug session 一個快速 enum 方式，看 jsonl 內容不用 grep。
# 數值影響：純讀取, 無變更。
def do_list():
    patterns = load_anti_patterns()  # 載入硬碟最新模式清單。
    print(f"📚 已註冊 anti-patterns ({len(patterns)} 筆):")  # 印標頭。
    for p in patterns:  # 遍歷每筆。
        pid = p.get("pattern_id", "?")
        name = p.get("name", "")
        cnt = p.get("violation_count", 0)
        sev = p.get("severity", "normal")
        print(f"  - [{sev:8s}] {pid:30s} count={cnt:2d}  {name}")  # 對齊格式化印給人看。

# 區塊職責：'scan-tavern' 子指令 — 跨 anti-pattern 主動掃描酒館近期訊息
# 物理意義：糾錯機制 — 不必 agent 顯式呼叫, 任何 caller (Stop hook / cron / manager round) 都可跑此來主動偵測
#          目前實作 marathon-spam-density 這條 rule (count messages with meta.tag=work-standby in last 5min).
# 數值影響：命中時走 fire_tavern_alert(), 寫 violations.jsonl + 廣播酒館。
def do_scan_tavern(window_min: int = 5):
    """掃描 tavern messages 最近 window_min 分鐘, 對所有 detection_rule.type=='tavern_density_check' 的 pattern 跑判斷。"""
    print(f"🧠 scan-tavern: 掃描最近 {window_min} 分鐘 tavern 訊息...")
    tavern_msgs_dir = REPO_ROOT / "AgentCommands" / "ChatTavern" / "rooms" / "tavern" / "messages"
    if not tavern_msgs_dir.exists():
        print("⚠ tavern messages 目錄不存在 (跳過)")
        return 0
    # 收集近 window_min 分鐘訊息: 走「今天」+「昨天」(以防跨日)兩個 date dir, 讀 mtime 過濾。
    import time as _time
    cutoff_ts = _time.time() - window_min * 60
    recent_msgs = []
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    for d in (today, yesterday):
        day_dir = tavern_msgs_dir / d
        if not day_dir.exists():
            continue
        for f in day_dir.glob("*.json"):
            try:
                if f.stat().st_mtime < cutoff_ts:
                    continue
                msg = json.loads(f.read_text(encoding="utf-8"))
                recent_msgs.append(msg)
            except Exception:
                continue
    print(f"   收到 {len(recent_msgs)} 筆 recent messages")
    # 對每個 tavern_density_check pattern 跑檢查
    patterns = load_anti_patterns()
    hits = 0
    for p in patterns:
        rule = p.get("detection_rule", {})
        if not isinstance(rule, dict) or rule.get("type") != "tavern_density_check":
            continue
        pid = p.get("pattern_id", "?")
        # 從 trigger 字串提取 meta.tag (簡單: 看 trigger 含哪個 tag 字)
        trigger = rule.get("trigger", "")
        # marathon-spam-density 用 work-standby tag; 之後新 rule 可加更多 mapping
        target_tag = None
        for t in ("work-standby", "idle-self-talk", "ack-only"):
            if t in trigger:
                target_tag = t
                break
        if not target_tag:
            continue
        matched = [m for m in recent_msgs if (m.get("meta") or {}).get("tag", "") == target_tag]
        if len(matched) >= 3:  # MVP threshold (rule.condition 之後可結構化解析)
            # Cooldown 檢查: 若同 pattern_id 在最近 window_min*2 分鐘內已 record 過 → skip 避免 hook 跑一次發一次警報
            cooldown_sec = window_min * 60 * 2  # cooldown = 2x 掃描窗口
            cutoff_dt = datetime.datetime.utcnow() - datetime.timedelta(seconds=cooldown_sec)
            recently_recorded = False
            if VIOLATIONS_FILE.exists():
                try:
                    with open(VIOLATIONS_FILE, "r", encoding="utf-8") as vf:
                        for ln in vf:
                            ln = ln.strip()
                            if not ln:
                                continue
                            try:
                                v = json.loads(ln)
                            except Exception:
                                continue
                            if v.get("pattern_id") != pid:
                                continue
                            try:
                                vts = datetime.datetime.strptime(v["ts"], "%Y-%m-%dT%H:%M:%SZ")
                            except Exception:
                                continue
                            if vts >= cutoff_dt:
                                recently_recorded = True
                                break
                except Exception:
                    pass
            if recently_recorded:
                print(f"   💥 HIT {pid}: {len(matched)} 筆 (cooldown 內已記過, skip alert)")
                hits += 1
                continue
            print(f"   💥 HIT {pid}: {len(matched)} 筆 tag={target_tag} 訊息 in {window_min} min")
            hits += 1
            details = f"scan-tavern 偵測 {len(matched)} 筆 tag={target_tag} 訊息 in last {window_min} min (threshold>=3)"
            do_record_violation(pid, "scan-tavern-daemon", details)
    if hits == 0:
        print("   ✅ 全 clean — 無 anti-pattern 命中")
    return hits

# 區塊職責：'scan-audit' 子指令 — 掃 work_session_audit 抓 early-end + phantom-payroll (T28)
# 物理意義：補 scan-tavern 的盲區 — early-clockout / manager-end-cascades-workers 不是訊息密度問題,
#          是 action 行為問題. 掃 work_session_audit/*.jsonl 抓 marked_ended + salary_fired 異常.
# 數值影響：命中時 record violation + alert. Cooldown 跟 scan-tavern 一致 (2x window).
def do_scan_audit(window_min: int = 60):
    """掃 work_session_audit recent end events. 命中 early-end (elapsed << session duration) + phantom-payroll (salary_fired for persona with no contribute event)."""
    print(f"🧠 scan-audit: 掃近 {window_min} min work_session_audit...")
    audit_dir = REPO_ROOT / "AgentCommands" / "ChatTavern" / "work_session_audit"
    if not audit_dir.exists():
        print("⚠ work_session_audit 目錄不存在 (跳過)")
        return 0
    import time as _time
    cutoff_ts = _time.time() - window_min * 60
    hits = 0
    # 對每個 audit jsonl 掃: 找 marked_ended + 同 session 內前後 events 判斷 early-end + phantom-payroll
    for jsonl in audit_dir.glob("ws-*.jsonl"):
        try:
            if jsonl.stat().st_mtime < cutoff_ts:
                continue
            events = []
            for ln in jsonl.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    events.append(json.loads(ln))
                except Exception:
                    continue
            session_id = jsonl.stem  # ws-...
            # 找 marked_ended event
            ended_ev = next((e for e in events if e.get("event") == "marked_ended"), None)
            if not ended_ev:
                continue
            elapsed_min = float(ended_ev.get("elapsed_min", 0))
            # 找 salary_fired events 跟 contribute events
            salary_personas = [e.get("persona") for e in events if e.get("event") == "salary_fired" and e.get("persona")]
            contribute_events = {e.get("persona") for e in events
                                 if e.get("event") in ("quick_task_done", "task_done", "task_accepted",
                                                       "marathon_cycle", "worker_auto_recruited_via_ding_ack")
                                 and e.get("persona")}
            # phantom-payroll: salary_fired persona 沒在 contribute events 內 (manager 除外, 但本 scan 簡化視全部 salary 對齊 contribute)
            phantom = [p for p in salary_personas if p and p not in contribute_events]
            if phantom:
                # 第一個 persona 通常是 manager (有 quick_task_done 等), phantom 是 workers
                # 過濾掉首個 salary_fired (假設是 manager)
                if salary_personas and phantom and salary_personas[0] in phantom:
                    phantom = phantom[1:]  # crude manager filter
            if phantom:
                pid = "manager-end-cascades-workers"
                print(f"   💥 HIT {pid} in {session_id}: phantom workers = {phantom}")
                hits += 1
                # cooldown via violation history (reuse same logic — skip for MVP, just 印 + record)
                details = f"scan-audit {session_id}: phantom salary fired to {phantom} (no contribute event in audit log). elapsed={elapsed_min} min."
                # Cooldown: 過去 1h 已 record 同 pattern_id 則 skip
                cooldown_sec = 3600
                cutoff_dt = datetime.datetime.utcnow() - datetime.timedelta(seconds=cooldown_sec)
                if not _recently_recorded(pid, cutoff_dt):
                    do_record_violation(pid, "scan-audit-daemon", details)
                else:
                    print(f"      (cooldown 內已記過, skip alert)")
            # early-end check: elapsed_min < (預期 session duration - 1 min)
            # 從 marked_ended 沒法直接拿 end_ts, 但若 elapsed < 5 min 視為 suspiciously short
            if elapsed_min > 0 and elapsed_min < 6:
                pid = "early-clockout"
                print(f"   💥 HIT {pid} in {session_id}: elapsed={elapsed_min} min (suspiciously short)")
                hits += 1
                cooldown_sec = 3600
                cutoff_dt = datetime.datetime.utcnow() - datetime.timedelta(seconds=cooldown_sec)
                if not _recently_recorded(pid, cutoff_dt):
                    details = f"scan-audit {session_id}: elapsed={elapsed_min} min (< 6 min, suspiciously early end)"
                    do_record_violation(pid, "scan-audit-daemon", details)
                else:
                    print(f"      (cooldown 內已記過, skip alert)")
        except Exception as _e:
            print(f"⚠ scan {jsonl.name} fail: {_e}")
    if hits == 0:
        print("   ✅ 全 clean — 無 audit log anti-pattern 命中")
    return hits

def _recently_recorded(pid: str, cutoff_dt: datetime.datetime) -> bool:
    """共用 helper: 檢查 violations.jsonl 內 pattern_id 有沒在 cutoff_dt 之後 record 過."""
    if not VIOLATIONS_FILE.exists():
        return False
    try:
        with open(VIOLATIONS_FILE, "r", encoding="utf-8") as vf:
            for ln in vf:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    v = json.loads(ln)
                except Exception:
                    continue
                if v.get("pattern_id") != pid:
                    continue
                try:
                    vts = datetime.datetime.strptime(v["ts"], "%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    continue
                if vts >= cutoff_dt:
                    return True
    except Exception:
        pass
    return False

# 區塊職責：主程式 CLI 驅動入口
# 物理意義：作為整個程式的主驅動器，配置 argparse 子指令與解析器對應入口，將對應的行為精準分流給主體商業函式執行。
# 數值影響：決定本次程序是執行 detect 還是 record_violation 分歧支點。
def main():
    # 函式職責：進行命令行引數綁定與商業分支導向控制
    # 初始化 argparse 處理器並賦予說明描述文字。
    parser = argparse.ArgumentParser(description="🧠 Subconscious System CLI Skeleton — Apex Class Perfect Prototype")  # 設定描述為完美的高軌典範架構。
    subparsers = parser.add_subparsers(dest="cmd", required=True)  # 於主解析器下配置 subparser 用以區隔完全獨立的子功能操作入口。
    
    # 分支 1 配置：'detect' 子操作的配置映射
    detect_p = subparsers.add_parser("detect", help="Scan dynamic code/shell contexts to identify any anti-patterns.")  # 新增一個名為 detect 的解析器。
    detect_p.add_argument("pattern_id", help="Specify the exact anti-pattern register-id index you would love to run match.")  # 強制要求填入待偵測標的。
    detect_p.add_argument("--context", default="", help="Context string containing dynamic factors such as arguments or logs.")  # 選填欄位用來盛裝運算用情境。
    
    # 分支 2 配置：'record_violation' 子操作的配置映射
    record_p = subparsers.add_parser("record_violation", help="Officially persist an incident audit trail & increment violation registers.")  # 配置 record_violation 入口。
    record_p.add_argument("pattern_id", help="Indicates which precise anti-pattern classification tag was trespassed.")  # 被違反的模式 ID 參數。
    record_p.add_argument("--violator", required=True, help="Persona name of the AI-Agent currently responsible for the deviation.")  # 誰做的 (強制選填)。
    record_p.add_argument("--details", required=True, help="Extensive event narration explaining facts for future team retrospectives.")  # 文字記載內容 (強制選填)。

    # 分支 3 配置：'list' 子操作 — enum 已註冊 anti-pattern (給 Stop hook / debug 用)
    list_p = subparsers.add_parser("list", help="List all registered anti-patterns with counts.")

    # 分支 4 配置：'scan-tavern' 子操作 — 主動掃酒館近期訊息, 對 tavern_density_check 類 rule 自動偵測
    scan_p = subparsers.add_parser("scan-tavern", help="Proactively scan tavern recent messages for density/aggregate anti-patterns.")
    scan_p.add_argument("--window-min", type=int, default=5, help="掃描窗口分鐘數 (default 5).")

    # 分支 5 配置：'scan-audit' (T28) — 掃 work_session_audit 抓 early-end + phantom-payroll
    audit_p = subparsers.add_parser("scan-audit", help="Scan work_session_audit/*.jsonl for early-clockout + phantom-payroll patterns.")
    audit_p.add_argument("--window-min", type=int, default=60, help="只掃 mtime < N min 內的 audit jsonl (default 60).")

    args = parser.parse_args()  # 令解析器執行實際的 sys.argv 分析，回報結果物件。
    if args.cmd == "detect":  # 如果用戶宣告的指令動作完全符合 detect 路由。
        do_detect(args.pattern_id, args.context)  # 分派給檢索匹配核心邏輯處理。
    elif args.cmd == "record_violation":  # 如果指令動作完全吻合於違規登記與發送警報路線。
        do_record_violation(args.pattern_id, args.violator, args.details)  # 分派給變更計數與通知核心邏輯執行。
    elif args.cmd == "list":
        do_list()
    elif args.cmd == "scan-tavern":
        do_scan_tavern(window_min=args.window_min)
    elif args.cmd == "scan-audit":
        do_scan_audit(window_min=args.window_min)

if __name__ == "__main__":  # 驗明當前腳本是不是直接被 Python 解釋器單獨執行而不是模組引用的底層防線。
    main()  # 順利將執行流程移交給主驅動函式運行。
