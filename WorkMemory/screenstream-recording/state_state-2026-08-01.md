---
id: state_state-2026-08-01
topic: screenstream-recording
title: 錄播模式已上線可用（規格→實作→實錄→讀取全走完）
type: state
status: active
created_at: 2026-08-01
created_by: basecamp
links: []
related_docs: [ucl_core:Docs~/zh-Hant/Plan/Plan_ScreenStream_Recording_Mode.md]
---

已落地：daemon 雙寫不取 mod / 資料夾開錄即命名 / frame 6 位數嚴格不跳號 / manifest 狀態機含開機自癒 / OCR 分離到 <rec>/ocr / STT 停錄時複製 / actual_fps + frames.jsonl / 磁碟兜底。讀取端 montage 加 --frames-dir 與 --index-range。真環境實測 87 張跳號 0 處。commit 0557728 + 105159b (UCL_Core Dev)。

Pending: (1) STT 的 nsp/logp 沒進 chunk (2) VAD 切窗未做，固定 15s 會腰斬長句，需換 faster-whisper (3) build_stt_section 另一條渲染分支沒驗 (4) montage make --help 自己會炸 (5) --index-range 不含密度語意。

待 Tim 拍板：錄播期間 ring 要不要繼續滾（目前是雙寫，陪看不受影響）。

血證三則（都是我寫進 code 的錯）：OCR cache 共用目錄會互蓋／STT 檔名 epoch 是毫秒而我拿秒去比（沙箱 fixture 也是我用秒造的，測試驗證了假設而非真實格式）／後過濾寫成 OR 把真對白全砍（官方用 AND 是為了 BGM+人聲混音場景）。
