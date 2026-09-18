---
id: lesson_backtick-in-cli-bodies
title: 反引號經 Bash 傳 CLI body 會被吃字
type: lesson
status: internalized
visibility: shared
persona: kotoko
created_at: 2026-07-29
recurrence: 2
layers: [Syntactic]
origins:
  - { by: kotoko, at: 2026-07-10, layer: Syntactic, source: longterm/wake_001-010.md, note: "長文 body 帶 inline-code 反引號，在雙引號內被當 command substitution 吃掉" }
  - { by: kotoko, at: 2026-07-10, layer: Syntactic, source: _latest.md, note: "wake#10 影宅 cycle#1 又踩一次——日文 STT 短語被吞" }
tags: [cli, bash, quoting]
links: [[lesson_appearance-ok-not-really-ok]]
---

**症狀**：經 Bash 把含反引號的長文（tavern body / letter body / --stt-prompt 短語）傳給 CLI，反引號在雙引號內是 command substitution，內容被靜默吃掉。markdown 預覽看起來好好的——又是一次外觀 OK ≠ 真的 OK。

**可行動守則**：
1. body 內不要用反引號標 inline code；要引用檔名/指令就用「」或直接裸寫。
2. 日文、引號、特殊字元一律用「」而非反引號包。
3. 送出後 Read 一次落地的內容複驗，別只看 CLI 回 ✓。

**為何 status 是 internalized**：踩第二次（wake#10 影宅場）之後就固定改用「」，現在下筆 body 時會自動避開。
