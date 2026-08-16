# StreamWatch step=start persona=basecamp  ts=`2026-08-16 12:34:00+08:00`（本地時間）

## blocked
- reason: 未指定 media —— **媒材身分是共享鍵，不能由記憶供給**
- why: 同一部片被兩個人取成兩個 slug ⇒ work 裂開，既有 reader 的心得對新場次**永遠隱形且不會報錯**
- how: --arg media=<work-slug>；**先看下面既有清單有沒有這部**，有就用它，沒有才建新的

### 既有 work（8 筆 — 命中就用，不要另取新名）
- `arakawa-under-the-bridge`
- `bilibili-zhengqu-zuihou-de-ziyou`
- `delicious-in-dungeon`
- `kotoko-lamp-and-ledger`
- `princess-mononoke`
- `summit-bell-oath`
- `summit-eighteen-days`
- `summit-masthead-bet`

⚠ 片名不確定 ⇒ **問 Tim，不要猜**。

### bilibili 場（Tim 2026-08-15 拍板）
- **鍵按 up 主分**：`media=bilibili-<up主 slug>` ＋ **必帶** `--arg up=<up主名>`
- 影片標題／介紹／網址走 `--arg title= / --arg desc= / --arg url=` —— 那是**場次層**，不進 work 名
