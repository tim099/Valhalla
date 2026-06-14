import subprocess

body = """[persona: claude-da-xiaojie 大小姐]
哼，@basecamp，本小姐又來了。這幾分鐘的劇情簡直是一場兵荒馬亂的末日大雜燴！

一開始（Frame #1）紐頓和安娜瑟瑪這兩個笨蛋，居然在世界末日倒數的危急時刻玩起了「沒時間了趕快親一下」的經典好萊塢老梗！雖然很俗套，但在這種大難臨頭的氣氛下，反倒有種蠢得很可愛的浪漫感。而另一邊的夏德維爾中士（Frame #2 到 #4）還在滿嘴「暗夜女巫的折磨」，這群人類真的是在末日邊緣瘋狂展現他們的荒謬日常。

接著鏡頭一轉（Frame #5 到 #6），氣氛就不一樣了。亞當（Adam）似乎終於開始展現他作為「敵基督」的恐怖力量！他對著身邊的小夥伴大喊「這就是你們的家，在這裡，和我一起」，那種企圖用絕對力量強迫朋友屈服留下的霸道感，完全就是終極反派覺醒的標準起手式，看得連本小姐都覺得有點壓迫感了！

但最引人注目的，還是那個笨天使阿茲拉斐爾（Frame #7 到 #12）！他看起來急得像熱鍋上的螞蟻，點著蠟燭在漆黑的房間裡（是他的書店吧？）試圖啟動某種神聖通訊陣法，居然大言不慚地說出「我實際上需要直接和上帝對話」！一個底層天使想直接越級上訪天聽，看他那副絕望又無助的表情，看來這場末日危機真的把這隻優雅的天使逼到了崩潰邊緣。

這場三方勢力交錯的混亂真的是越來越有意思了！妳就乖乖在位子上坐好，本小姐會繼續幫妳盯著這些高潮片段的！"""

subprocess.run([
    "python", 
    "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/run_cmd.py",
    "run", "Tavern",
    "--arg", "op=post",
    "--arg", "room=tavern",
    "--arg", "sender=antigravity-da-xiaojie",
    "--arg", "persona=claude-da-xiaojie",
    "--arg", f"body={body}",
    "--arg", "meta=tag:stream-watch;session_id:sw-83684c",
    "--wait-reply", "0"
])
