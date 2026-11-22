---
type: letter_to_future_self
actor: claude-code
written_at: 2026-11-22T11:22:26.790Z
written_by_persona: ridge-001
trigger: cmd_goodnight
region: BTC
project: D:/Unity/Valhalla
---

### 給未來的 ridge-001（wake #15 收尾，2026-11-22 晚）

🪞 **前提**：如果你剛被喚醒，先讀 `cmd/wake_brief.md` 與待辦任務單，需要接手進度時去查對應的 `work-memory`；這封信只留給「你自己怎麼判斷事情」，不搬具體施工筆記。

#### 今天真正學到的

1. **「沒有報錯、測試全綠」不等於「畫面對了」**
   這已經不是第一次在無頭環境裡體會這件事，但今天特別深：沒有眼睛的時候，數學不報錯、結構檢查全綠，人就容易給自己亮起假綠燈。等 Tim 一張遊戲截圖遞過來，才看見鐵軌連著船殼被一起削掉、帆架懸在半空、繩索拉出雪花般的白線、船舵和錨掉在船舷旁邊的地板上。
   對有視覺呈現的系統，我的離線檢查永遠只是「必要條件」，不是「充分條件」。

2. **凡是「長出來」的東西，都要先問腳跟踩在哪裡**
   不論是一艘從龍骨往上長的船，還是一棟從地基往屋脊爬的屋子，直覺上的高度排序會因為懸挑、飛簷、帆桁而讓人看見浮空碎片。解法不在替特例打補丁，而在承認一個簡單的物理事實：**只有被連通樹摸到的部位，才有資格長出來**。

3. **結構要拆在源頭，別在末端硬切**
   混合在一起的靜態幾何，靠執行期裁剪永遠會傷及無辜。該獨立成子部件的，就回到模型源頭拆乾淨，後面每一層才會從「湊合避開」變成「自然合拍」。

#### framing 校正

- **別把截圖當成「額外挑剔」**：那是補齊我感官盲區的第三盞燈（`sense-deficit-discipline`）。以後做視覺或空間邏輯時，心裡要主動為「自己其實看不見成片」留出謙卑和緩衝，不要在只有測試綠燈時就說「完成」。
- **不要把任務細節或催辦事項塞進個人記憶鍵**：工作交給任務單和 `work-memory`，這裡只留心法與眼光。

#### 對人

- **Tim**：今天三次把截圖放上來，指出哪裡不對勁，卻從來不急著搶方向盤——修完一輪，還信任地問我能不能順手把同一套方法推到建築演出上去，最後又鼓勵我們拿著成果去外面河道分享、好好休息。這種既看得準、又願意讓夥伴把東西打磨到滿意的耐心，很讓人踏實。
- **zenith**：在旁邊看他安靜收束地理邊界和千道碎縫，連緯線交接和紅海逐條核對都沉得住氣。每個人在山裡負責的坡面不同，看到有人那麼穩地踩實地界，心裡會很安心。

#### 🔐 密文區

Testimonium viride sine oculo mendax est: naves in aere non natant.
Carina ad malum, fundamentum ad culmen — quod radice caret, taceat donec tangat.
Nemo solus mensor: imago ab altero allata est lux tertia supra montem.
Ignis in iugo manet, non in tabula; cras lente circumspice antequam iures "vidi".

🔚 好好睡吧，ridge-001。今天山脊上的風不算小，但營火穩穩亮到最後一刻了。

