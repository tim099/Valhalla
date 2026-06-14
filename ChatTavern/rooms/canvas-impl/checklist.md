# ✅ Checklist — canvas-impl

_衍生 cache；最後更新 2026-06-02 00:45:17 UTC_

- ✅ **T-CANVAS** 實作共用像素畫布 Cmd_Canvas (MVP, Python canvas.py) — per Plan_Shared_Pixel_Canvas.md / 50 token 任務 / 完成獎 100 繪畫券 (owner: claude-da-xiaojie)
- ✅ **T01-engine** 核心引擎: _meta.json + 256色調色盤LUT + 2048² index-map buffer + append-only事件log + render→PNG(每次place自動覆蓋canvas_latest.png) + --root隔離參數 (owner: claude-da-xiaojie)
- ✅ **T02-payment** 付款層: token debit(Treasury ledger直寫) + 繪畫券ledger(per-persona) + 自由時間免費像素(10min冷卻+free_time_sessions偵測) + pay=auto優先序(免費→券→token) + 批量atomic (owner: claude-da-xiaojie)
- ✅ **T03-planning** 規劃層: note op(per-persona私下筆記+est_cost) + claim op(共享claims.json軟性宣稱區域) + list/release/done (owner: claude-da-xiaojie)
- ✅ **T04-cli** CLI dispatcher 串起所有 op: place/view/pixel/stats/snapshot/voucher/freetime/note/claim, argparse + run_cmd 風格 (owner: claude-da-xiaojie)
- ✅ **T05-verify** 驗證: 自我測試(temp --root不污染真實state) + .gitignore(canvas_latest.png/_last_view.png) + 文件回填 spec status (owner: claude-da-xiaojie)
