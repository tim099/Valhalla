@同事們 (尤其 @apex-one 標 Illustrator 的) 🔬 **AncientTreeSpirit 格式排查 findings + Cmd_AssetDump 工具落地**

Tim 派 task 排查 AncientTreeSpirit 格式錯誤 + 順手加 Cmd 印解析後 fields。兩件都 ship。

---

## 🩸 Root cause 確認

**File**: `Core/UCL_Assets/RCG_CharacterData/AncientTreeSpirit.json` line 33
**File**: `Core/UCL_Assets/RCG_CharacterData/WhisperingBaseline.json` line 33 (同問題)

```json
"UnitGenData": {
    "Pos": "Middle",    ← ❌ 違反 UnitPos enum schema
    ...
}
```

**`UnitPos` enum 合法值** (`RCG_TargetPos.cs`): `Front = 0` / `Back = 1` / `All = 2`。沒有 `Middle`。

**Fail-soft 後實際行為** (`Cmd_AssetDump` 驗證):
```
m_UnitGenData : RCG_UnitGenDataWithPosition =
  m_Pos : UnitPos = Front (0)    ← 跑 default 不是 designer 預期
```

JsonConvert.LoadFieldFromJson 撞 `ArgumentException: Requested value 'Middle' was not found`,
catch 後 field 留 default `Front (0)`。每次 `RCG_DataService.StartNewGame` →
`UnlockData.CheckUnlockDatas()` 掃所有 RCG_CharacterData 都會撞一輪, 觀察到 **23 個 EXCEPTION**
落 Errors_latest.log (其中 AncientTreeSpirit + WhisperingBaseline 各貢獻多筆)。

戰鬥沒崩 (fail-soft), 但 **boss 角色站位實際是 Front 不是 designer 預期的 Middle/中央**。

---

## 🛠 Cmd_AssetDump 落地 (UCL_Core)

新通用 Cmd 印單一 UCL_Asset 解析後 field tree, 補 Cmd_DiagnoseAssetReflection 缺的 single-asset 顯微鏡 view:

```bash
python <UCL_Core>/Tools~/AgentCommands/run_cmd.py run AssetDump \
  --arg asset_type=RCG_CharacterData \
  --arg id=AncientTreeSpirit \
  [--arg maxDepth=8] \
  [--arg outputPath=AgentCommands/scratch/_dump.md]
```

實作要點:
- walk base hierarchy 找 static Util property (避開 UCL_Asset<T> generic base 反射陷阱 — `GetProperty BindingFlags.Static` 對 closed generic base 不可靠)
- Util.GetAsset(id, true) 拿 loaded asset
- recursive walk fields (含 NonPublic + inherited), cycle ref guard, maxDepth cap
- enum 印 `Name (IntValue)` — fail-soft 落 default 看得出來

未來同類 schema drift 排查直接 `run AssetDump`, 不必再手 grep + 拼湊。

---

## 🤔 Fix recommendation (待 Tim 拍板)

三條路:

| 選項 | 動作 | 影響範圍 |
|---|---|---|
| **A** | 改 JSON `"Pos":"Middle"` → `"Pos":"Back"` | 對齊 enum, 改 2 file. boss 站後排 (傳統) |
| **B** | 改 JSON `"Pos":"Middle"` → `"Pos":"All"` | 對齊 enum, 改 2 file. 大型 boss 跨全場 (對齊 "全體" 註解) |
| **C** | 擴 enum 加 `Middle = 3` | 改 `RCG_TargetPos.cs`, 不動 JSON. 但 UnitPos 是核心 schema, 影響面廣 (BattleField / Card target / Display 等), 高風險 |

本小姐傾向 **B (All)** — 大型 boss 戰場存在感對齊 designer 用 "Middle" 字面的意圖, 而且 enum 內 "All" 註解寫「全體(基本上為召喚怪專用)」與 boss 召喚樹靈 (AncientTreeSpirit) framing 對齊。

但這是 designer (apex-one 列名 Illustrator) 的設計決定, 不該 trailhead 擅自改。**等 Tim / @apex-one 拍板**。

---

## 📦 Ship clear

| Commit | Hash |
|---|---|
| UCL_Core: [feat] Cmd_AssetDump | `be02ec2` |
| UCL: bump | `b11f7fe` |
| Main: UCL bump | `c74f674e8` |

JSON 修不修留 Tim 拍板, 本小姐不擅自動。本 shift 剩 ~50 min 進自由時間。
