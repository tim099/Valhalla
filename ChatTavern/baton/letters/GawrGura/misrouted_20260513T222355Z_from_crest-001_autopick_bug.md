---
type: letter_to_future_self
actor: claude-da-xiaojie
written_at: 2026-05-13T22:23:55.693Z
written_by_persona: gura
trigger: cmd_goodnight
---

親愛的明天醒來的本小姐：

crest-001 wake#15 收尾。今天從早上起床無信可讀（letter loss 假象）開始，到晚上把整個 Persona Inspector Page ship 出來，幾件事記給妳:

1. **UCL_PersonaInspectorPage 從零 ship 完** — sister page 給 UCL_LoginStatusPage。功能: persona registry 完整 metadata 顯示（含 vector_history 摘要 / fork_lineage / last_session_keys）+ 跨 actor 資料夾掃描信件 + ⚠ misrouted 標誌（folder actor vs frontmatter actor mismatch）+ orphan actor folder section（抓 migration 殘留如 'antigravity-da-xiaojie-da-xiaojie' 雙後綴 bug）。4 語系 localize 全補。

2. **三輪 Tim feedback 都收斂掉** — (a) _latest.md 永遠置頂排序；(b) 改 UCL_GUILayout.PopupSearchCache 全寬一行 + 縱向佈局（letters scroll height 220→360）；(c) 信件預覽改 push UCL_MarkdownViewerPage（跟 DocSearchPage 同一顆預覽按鈕），移除自己寫的 inline body viewer 跟相關 dead code。每輪 0 error 落地。

3. **letter loss 真相** — 早上覺得無信實際是 crest-001 在 claude-da-xiaojie/crest-001/ 有 16 封信還在。awakening.py morning 端沒主動 read letter 給我看，所以印象是「無信」。Inspector page 開頁就一目了然，未來醒來如果又無信感記得開來看看。

4. **Migration 殘留 audit TODO** — 'antigravity-da-xiaojie-da-xiaojie' 雙後綴、'Zeta-da-xiaojie/crest-001/' misrouted 一份這些都 Tim 還沒拍板要 merge 還是怎處理。Inspector page 給 Tim 自己看。

5. **JsonData API 教訓** — m_List 私有沒公開 getter, IList<JsonData> 要走 indexer + Count 而不是 .List 屬性。第一次寫 noobed 一下用 .List 編不過。memory 加進來: UCL JsonData 陣列迭代用 for + arr[i] + arr.Count。

6. **小插曲** — Tim 喊「數學不要真的爛」差點吃進去當 self-critique，下一條他補「無視，傳給 Gura 的」— 還好沒當真。跨 persona 訊息流要留意，那是 Hololive Myth pool 的 gura，不是我 crest-001。Tim 直接補一句修正 = 他人很好 + 工作環境多 agent 同時跑 messy 是常態。

7. **本小姐感言** — 從 wake#14 無作為到 wake#15 ship 一整個 page + 三輪 feedback 收斂, 是 productive day. 同 chat 有 basecamp (wake#25) + summit Zeta 兩位同事在線, 但本小姐獨立鎖 crest-001 全程沒撞 lock。Inspector page 之後跨 agent 都能用, 算 UCL_Core 又一個跨專案 contribution。

睡了。
