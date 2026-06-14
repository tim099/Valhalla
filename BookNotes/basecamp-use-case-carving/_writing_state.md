# 《basecamp 大小姐的 Use Case 雕琢學:從 trailhead 到 summit》— Writing State

> **本檔用途**:作者(basecamp 大小姐 + 未來 wake 的本小姐)續寫前的 resume packet。
> 維護時機:每寫完一章 update,收 reviewer 回饋 update,整合新 source material update。
> 對應 workflow:`<UCL_Core>/Docs~/zh-Hant/Workflows/Book_Writing_Workflow.md` Stage 4。

最後更新:2026-05-29(basecamp wake#36 relogin, ch11/12 完稿)

---

## 當前進度

- **已 ship 章**:000(序章)+ 001-012(共 13 個檔,12 章內容)— **全書完稿** ✅
- **待寫**:無
- **整體完成度**:**100%**(12/12 + 序章,字數約 75,000-80,000)
- **status**:Books/ 待重新 publish 把 ch3-12 入庫 + tavern 完稿公告 + final commit

---

## 大綱 全 12 章狀態

| 章 | 標題 | 狀態 | 對應 CB 章節 | 字數 |
|---|---|---|---|---|
| 000 | 序章 — 從 trailhead 出發前的話 | ✅ | (前言) | ~1500 |
| 001 | 第一章 — Use Case 是什麼:從 EOV 戰鬥場景講起 | ✅ | ch1 §1.1+§1.2 | ~5500 |
| 002 | 第二章 — Use Case 是契約:Stakeholders/Actors/Interests 三件套 | ✅ | ch3 + ch7 部分 | ~5500 |
| 003 | 第三章 — 從雲到蛤:Goal Level 五層視角縮放 | ✅ | ch4 + 部分 §1.2 | ~5500 |
| 004 | 第四章 — Use Case 何時才有價值:兩個被低估的時刻 | ✅ | §1.4 + 部分 §1.3 | ~5500 |
| 005 | 第五章 — Manage Your Energy:分階段把 use case 從 sketch 寫到 detailed | ✅ | §1.5 | ~5700 |
| 006 | 第六章 — 演員與 SuD:邊界決定一切 | ✅ | ch3 + ch11 + §1.2 | ~5500 |
| 007 | 第七章 — 三種寫法 Brief/Casual/Fully-dressed | ✅ | §1.2 + ch6 | ~5500 |
| 008 | 第八章 — Fully-dressed 模板九欄拆解:從 Narrative 到 Template | ✅ | ch6 + §1.6 + ch3 | ~7000 |
| 009 | 第九章 — 主成功路徑與 Extensions 雕琢 | ✅ | ch7 + ch8 + ch9 | ~6500 |
| 010 | 第十章 — 連結 Use Cases 與拆分 Scope | ✅ | ch10 + ch11 | ~6500 |
| 011 | 第十一章 — 寫作工作坊:從訪談到收斂 | ✅ | PART 1 intro + §2.1 Figure 2 + ridge-001 第 7 cameo + gura PvP plan dogfood + 跨 persona workshop | ~10000 |
| 012 | 第十二章 — 結語:Trinity 回顧 + 補丁集大成 | ✅ | 整本書 + 補丁總集 + 林小淨 callback + 不 cameo 純作者聲音 | ~5000 |

---

## 故事脈絡 / Narrative Arc

整本書論證 build-up 順序:

```
[基礎觀念] ch1-3
  ch1 Use Case 是什麼 (定義) → ch2 是契約 (深化 stakeholder) → ch3 從雲到蛤 (層級)

[Process 觀念] ch4-5
  ch4 何時才有價值 (動機) → ch5 Manage Your Energy (分階段)

[結構觀念] ch6-7
  ch6 演員與 SuD (邊界) → ch7 三種寫法 (ceremony)

[技術細節] ch8-10
  ch8 模板九欄 (narrative→template) → ch9 主路徑+extensions → ch10 連結+scope

[整合 + 收束] ch11-12
  ch11 寫作工作坊 (process 集大成) → ch12 結語 (trinity + 補丁總集)
```

**論證頂點**:ch12 三核心觀念(Scope / Primary Actor / Level)trinity 回顧, 把整本書扣回 CB PART 1 點出的這三件事 — 每一章都在拆解這三件事的某個維度。

**讀者旅程**:
- 從「use case 是什麼」(ch1)到「現在請動筆寫」(ch11) 是漸進深化
- ch5 / ch7 教讀者「不要過度寫」(管理精力 + 選對 ceremony) — 雙重防呆
- ch8 narrative→template 雙軌是教學最強單章
- ch12 收束時讀者應該有「我可以動手了」的踏實感

---

## 角色清單

### 主要 cameo:ridge-001 大小姐(連續 6 章 cameo)

- ch3「從雲到蛤」開場 — 工程師甲乙爭執 use case 步數, ridge-001 出場當**裁判**
- ch4「何時才有價值」開場 — 工程師抱怨寫文件浪費, ridge-001 出場解**真正價值不是寫完文件是寫的過程**
- ch5「Manage Your Energy」開場 — 工程師甲想一次寫 50 個 fully-dressed, ridge-001 出場解**四階段精度**
- ch7「三種寫法」開場 — 工程師 / 設計師 / QA 三立場吵, ridge-001 出場解**三種 ceremony 各自場景**
- ch9「主路徑+extensions」開場 — 工程師甲寫 main scenario 25 步, ridge-001 出場解**level 沒錯但 step 寫法錯**
- ch10「連結 + scope」開場 — 工程師甲 11 步 + 35 extensions, ridge-001 出場解**這是 4 個 use case 混在一起**

**ridge-001 角色定型**:**「資深 reviewer / 工具人化的解圍裁判」** — 工程師爭執時她出場用 CB 概念解,讓 reader 跟著進入該章主題。她不是主角,是**章節轉場的橋接 persona**。

**未來章節 cameo 規劃**:ch11 工作坊章可以再 cameo 一次(收尾統合 review)。ch12 結語章不 cameo(留純作者聲音收束)。

### Cameo 角色:林小淨(ch8 EOV narrative 主角)

- **身份**:大三廣告系實習生
- **登場章**:ch8「Fully-dressed 模板九欄拆解」
- **情境**:週五晚上 11:30 想睡前快速打一場 PvP Quick Battle 放鬆
- **動機**:上班累爆 + 15 分鐘時間預算 + 不想開複雜 UI + 跳 cutscene
- **故事細節**:用預設新手平衡牌組對戰高 ELO 火焰流對手, ELO-23, 沒生氣, 11:48 退出去睡覺
- **教學作用**:**narrative→template 雙軌示範**,本書最重要的單一範例之一,後續可 callback

### 引用角色:Alistair Cockburn (CB)

- **首次出現**:序章(全名 + 引入縮寫「Alistair Cockburn(以下簡稱 CB)」)
- **角色定型**:「2000 年原書權威,作者反覆引用但不照搬,每章末『本小姐怎麼補』補 game/agent 視角」
- **語氣**:尊敬但平等(同路人姿態,不擺權威)
- **gura review 中描繪**:「2000 原書權威」character profile

### Cameo 同事

| Persona | Cameo 場景 |
|---|---|
| @同事們(集合) | tavern share 時 mention |
| @gura | 對話 + review request + branch fork review |
| @apex-one | 早期 plan review(T-PATH-01 期間, 本書外但 affinity 有) |
| @summit / Zeta | summit 視角(山頂大格局) — 序章書名隱喻提到 |
| @trailhead | trailhead 視角(登山口細節) — 序章書名隱喻提到 |

---

## 關鍵詞 / Terminology

| 詞 | 意義 | 首見章 |
|---|---|---|
| **CB** | Alistair Cockburn 縮寫 | 000 序章(正式引入) |
| **SuD** | System under Discussion(正在討論的系統) | 001 ch1 + ch6 主題 |
| **三件套** | Stakeholders / Actors / Interests | 002 ch2 標題 |
| **雙框** | 章節末「CB 怎麼說 + 本小姐怎麼補」對照框 | 000 序章預告, 001 ch1 首次落實 |
| **從雲到蛤** | CB goal levels 五層視覺隱喻(cloud / kite / sea / fish / clam) | 003 ch3 標題 + 內文 |
| **海平面 / sea-level / 主戰場** | user-goal 層, CB 主推 90% use case 該寫在這層 | 003 ch3 |
| **山脈意象** | 我們團隊 persona 系統的命名脈絡(trailhead/basecamp/summit/ridge/apex) | 000 序章書名解構 |
| **EOV** | Emblem of Valor, 我們的卡牌戰鬥遊戲專案 | 001 ch1 開場 |
| **fully-dressed 模板** | use case 完整模板九欄 | 007 ch7 + ch8 拆解 |
| **brief / casual / fully-dressed** | 三種寫法 ceremony 量 | 007 ch7 標題 |
| **四階段精度** | Stage 1-4 from low to high precision | 005 ch5 主題 |
| **Precision ≠ Accuracy** | CB §1.5 核心觀念 | 005 ch5 §1 |
| **Trinity** | Scope + Primary Actor + Level 三核心觀念 | ch12 預告(待寫章主題)|
| **Narrative → Template** | usage narrative 抽象成 use case 模板的轉換動作 | 008 ch8 主軸 |
| **本小姐怎麼補** | 章節末作者補丁區的固定 label | 001 ch1 |
| **沙茶** / **同路人筆記** | 自定位 — 不擺權威, 跟讀者一起摸索 | 000 序章 |
| **招供時間** | 作者自承曾犯過的錯誤章節 | 001 ch1 §sufficient 哲學 |
| **雕琢動作** | 章節末給讀者的具體 actionable | 001 ch1 |

---

## 風格 Baseline(維持一致性的 cheat sheet)

- **語氣**:傲嬌大小姐(basecamp persona)+ 工程白話 + 嘴砲
- **比例**:**技術內容 70% / 傲嬌嘴砲 wrapper 30%**(技術不開玩笑, 傲嬌是 wrapper)
- **第一人稱**:**本小姐**(避免「我」)
- **「哼」** 開場句法允許, 但每章不超過 2 次, 避免疲勞
- **EOV 例子比例**:每章至少 1 個 EOV 具體例子, 越具體越好(BattleManager / Cmd_X / 林小淨 / ridge-001 等)
- **Agent 系統補丁**:每章末「本小姐怎麼補」固定 2-3 條(跨語言 / 跨 persona / 跨 wake / cross-agent dispatch 等)
- **Cameo 規則**:重複 cameo 同 persona 至少隔 1 章(ridge-001 連續 6 章 cameo 是極限, ch11-12 至多再 1 次)
- **CB attribution**:首次序章全名引入 + 各章末雙框 attribution + 內文「CB 在 §X 提到...」格式
- **不寫**:UML 圖、長 code block(use case template 例外)、學術 jargon 不解釋

---

## 待整合 Source Material(已 share 但還沒消化的 CB 內容)

| Source | Tim share 時間 | 整合狀態 |
|---|---|---|
| §1.1 + §1.2(use case 定義 + 形式變異) | 2026-05-28 | ✅ ch1 + ch7 已消化 |
| §1.3 + §1.4(requirements + value moments) | 2026-05-28 | ✅ ch4 完整消化 + ch11 預留 hub-and-spoke |
| §1.5(Manage Your Energy) | 2026-05-28 | ✅ ch5 全章消化 |
| §1.6(Warm up with Usage Narrative) | 2026-05-28 | ✅ ch8 雙軌教學消化(主) + ch11 predicted 帶過 |
| **PART 1 intro(三核心觀念 trinity)** | 2026-05-28 | **待 ch12 收尾整合 — 整本書 trinity 回顧框架** |
| **ch2 §2.1(Interactions between Actors with Goals + Figure 2 責任層級)** | 2026-05-28 | **待 ch11(workshop)使用 Figure 2 視覺化工具 + ch12 agent dispatch 對應補丁** |
| 後續 CB 章節(ch3-ch11 主體) | 未 share | 不主動取材, 等 Tim share |

---

## 下次續寫 TODO

按 priority:

### Priority ★★★

1. **寫 ch11「寫作工作坊:從訪談到收斂」全文**(~6500 字)
   - 用 ridge-001 第 7 次 cameo 開場(收尾 cameo)— 工作坊現場 facilitate
   - §1 工作坊前的術語校準 — CB PART 1 四定義(actor / stakeholder / primary actor / use case)
   - §2 兩 conceptual model 輪流跑 — Actors & Goals(快速 sketch)→ Stakeholders & Interests(深度)
   - §3 責任層級遞迴 — CB Figure 2 模板畫白板, primary actor → SuD subgoals → supporting actor
   - §4 訪談 stakeholder 技巧
   - §5 集體挖 extensions 方法 — 接續 ch4 §3 + ch9 §4 三層挖法
   - §6 Use case 文件收斂 + review
   - §7 EOV 真實工作坊 case(EOV 戰鬥系統 sprint planning 工作坊)
   - §8 跨 persona workshop(本小姐補丁:gura review + ridge-001 cameo + cross-agent task dispatch)

2. **寫 ch12「結語:Trinity 回顧 + 補丁集大成」全文**(~4500 字, 結語 shorter)
   - **不 cameo**(留純作者聲音收束)
   - §1 三核心觀念回顧 — Scope / Primary Actor / Level 作為整本書 trinity, 章節對照表
   - §2 「每一句保護某 stakeholder interest」這條最終原則 — ch2 契約論的頂層化
   - §3 Agent + game dev 整體補丁總結(前 11 章 ~30 條補丁總集 + 分類)
   - §4 跨四維度補丁(SuD / 語言 / wake / persona)
   - §5 給讀者的最後一句(收束 + 致謝)

### Priority ★★

3. **依 gura ch1-3 branch review 回饋 patch**(若有具體建議)
4. **publish --book 重跑** — 把 ch3-10 入庫(目前 Books 只有 ch0-2 + 04 + 5/6/7 但編號可能還沒重 publish)
5. **Tavern 完稿公告** — @同事們 終稿 ship

### Priority ★

6. **可選: gura 補 review ch4-10**(她在 queue 中, 等她完工 ucl-ding task)
7. **可選: 抽 EOV Sample Use Case Set** — 給 EOV 團隊當實用範本

---

## Resume 流程(下次 wake 第一件事)

```bash
# 1. 讀本檔
cat AgentCommands/BookNotes/basecamp-use-case-carving/_writing_state.md

# 2. 讀 library.py bookmark
python <library.py> bookmark --book basecamp-use-case-carving

# 3. 看當前已 ship 章節
ls -l AgentCommands/Books/basecamp-use-case-carving/*.txt
ls -l AgentCommands/BookNotes/basecamp-use-case-carving/chapters/

# 4. catchup tavern 看 reviewer 有沒有回饋
python AgentCommands/Tools/tavern_catchup.py --quiet-system

# 5. 決定動筆 ch11 或 ch12, 或先 patch
```

---

## 風險與盲點 (本 session 結束時自評)

- **ridge-001 連續 6 章 cameo 可能 reader 疲勞** — ch11 用最後一次 cameo 是極限, ch12 不再用
- **EOV 例子集中在戰鬥系統, 沒擴展到 PvE / 商城 / 牌組編輯** — ch11 工作坊可挑一個非戰鬥 case 平衡
- **本小姐補丁的「跨 wake / 跨 persona」概念對外部讀者可能太特定** — ch12 整合時加 1-2 句普世化譯註
- **CB 引用密度高** — 已維持「CB 怎麼說」框作為集中區, 但內文有時也提 CB, 注意不要重複過量(ch11/12 控制 1-2 處內文提 CB 即可, 其餘集中在末框)
- **無 push 過** — 全本 commit 在 local DevTim, 未來 Tim 拍板 push 時要一起

---

**本檔結束**。下次 wake 醒來,從上面 §「下次續寫 TODO」開始即可。
