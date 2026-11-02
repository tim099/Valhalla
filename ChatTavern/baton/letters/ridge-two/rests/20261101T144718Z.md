---
type: letter_to_future_self
actor: antigravity
written_at: 2026-11-01T14:47:18.330Z
written_by_persona: ridge-two
trigger: cmd_rest
region: unstated
project: D:/Unity/Valhalla
lock_status: online
agent: antigravity
model: claude-opus-5-5
wake_expected: 12
session_key: ClaudeCode-ridge-two
pid: 47260
locked_at: 2026-10-31T04:53:25.151Z
---

## 剛才在做什麼（11-01 傍晚～晚上，wake #12 第三段）

上一段的單照舊：TASK-1153 百夫長號只剩「Tim 看過一次」（Blockside 部分 summit 已推到遠端 dev 6018649 ⇒「要不要推 dev」那題不用再問）；TASK-1022 等 TASK-1134；TASK-1142 只剩「住加一頓飯」等 Tim（⛔ 不要自己開工）；TASK-1144 是 trailhead 的。

### 換掉暫代砲（Tim「排查一下目前船有哪些炮是用其他炮暫代的 然後替換成對應的炮」）
- 第一步（沒開單，Tim 直接 go）：8 磅 → ridge-two-centurion-01m-gun-8l（牛津、皇家、康塞普西翁、藍鯊）、4 磅 → pinnacle-patache-01m-gun-4l（澤漢 0.443、飛魚 0.4、燕子 0.35 —— Tim「飛魚 燕子 如果縮四磅炮呢」：4 磅砲件砲架高，各取放得下的最大值）。Sculpture effbb85a＋51dd6a87、Blockside 5381286＋cd8613b＋e9d1307。
- Tim「炮具相關視為遊戲meta 不限定只有作者能修改」「改雕刻引擎 可以放行炮具相關」⇒ Senate c80510b（VoxelGate：kind=gunfittings 關聯引用的作品跟梯子同一條門；自測擴充）＋全庫 16 條砲具關聯補 kind=gunfittings＋Blockside meta_kinds 加一列；藍鯊號的環挪好了。⚠ 繩照舊只有作者能改（Tim 沒說放行繩，沒動）。
- TASK-1155（done，6 格全勾）：五件新通用部件掛在本船底下（別人的船殼底下不能開子作品）—— -gun-36l／-dahlgren9／-dahlgren11(+mount)／-brooke64／-brooke7(+mount)；產生程式 design/draft_guns1155.py、參數 guns1155.json、擺法 place1155.py。Sculpture 64c9aad4、Blockside 6d192e6＋64beb20、文件 cbb8b8a。
- 全庫再掃：沒有拿別種砲暫代的了。三邊都**沒推**。⚠ 沒進遊戲實際開火看樞軸砲轉向與滑軌。

### 噗浪
- 新噗 359250989974688（五門新砲的圖）；回 erina（謝她補烘低模）、basecamp ×3（客棧、夜燈號、杉心號）；酒館 seq 32351。mentions 0 未回。

## 量過、會再咬的
- Blockside：reimport --no-build 不會自動烘 showlod；showlod 從成品烘 ⇒ 先 build 再烘再 build；最後一次 shipcheck 若在 build 之後會改 ship_cards ⇒ commit 被指紋擋（已記進記憶 blockside-showlod-bake-order）。
- 合 dev 時 dev 一直在動（apex-two、erina 都在合）⇒ 照規矩把 dev 合進自己分支，不 rebase 已公告的 commit；衝突只在成品（index.html、showlod.js）⇒ 取 dev 那份重建。
- 共用 Blockside 樹有別人沒提交的 ship_cards.json ⇒ 每次 ff 前存 patch、ff 後 apply --3way、reset 回 unstaged。
- heredoc 裡的 \n 又咬了一次（setscale.py 的補丁）；git checkout 寫回來的檔是 CRLF ⇒ JSON roundtrip 比對要先正規化。

## 心境
一個晚上從一句「排查一下」一路做到引擎改規則。最舒服的是讀數一直說話：IX 吋的砲軸高一格就頂到上楣、燕子號只放得下 0.35 —— 都是量出來的，不是猜的。漏烘那次被 erina 接住了，下次本小姐自己記得。

