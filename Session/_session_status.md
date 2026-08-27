# （已退場）SessionStatus 回傳檔不再寫在這裡

> 這裡曾是**全域單槽**，兩個人同時查 session 狀態會互相覆蓋（TASK-0059，與 TASK-0026 ① 同族）。

回傳檔現在落在 **`letters/<persona>/cmd/sessionstatus_<scope>.md`** ——
`run_cmd.py` 會直接印出「📄 回傳檔：<路徑>」，照那一行讀，不要背路徑。
