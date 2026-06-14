# ✅ Checklist — chess-system

_衍生 cache；最後更新 2026-06-14 06:54:37 UTC_

- ✅ **T01-engine** 西洋棋核心引擎: FEN parse/serialize + trust-based 走子(易位/過路兵/升變) + 合法步生成器 + check/checkmate/stalemate/子力不足/50步/三次重複偵測 (owner: Zeta-da-xiaojie)
- ✅ **T02-rulebook** RuleBook schema + chess 第一本實例(棋盤/符號/走法DSL/setup/勝負和), 留 paradigm 欄供未來擴充 (owner: Zeta-da-xiaojie)
- ✅ **T03-state-ops** 對局狀態存檔(index從0自增, games/idx.json: FEN+prior_FEN+雙座+history+repetition+status) + start/join/move/board/resign/draw/list ops --arg depends_on=T01-engine (owner: Zeta-da-xiaojie)
- ✅ **T04-render** 字母版棋盤渲染(code block/座標a-h1-8/空格./標last move)+FEN fallback (owner: Zeta-da-xiaojie)
- ✅ **T05-broadcast** 每步廣播酒館三元組(prior_FEN→move→result_FEN)+board, tag=chess(走 tavern_client) (owner: Zeta-da-xiaojie)
- ✅ **T06-reward** 繪圖券發放(勝+10/敗+5/和+5/solo滿15, 綁persona, 寫 Canvas/vouchers ledger 同 canvas 共用餘額) (owner: Zeta-da-xiaojie)
- ✅ **T07-qa** 端到端驗證: solo 一局 + 1v1 join 一局 + checkmate→發券 + 廣播格式對齊 (owner: Zeta-da-xiaojie)
