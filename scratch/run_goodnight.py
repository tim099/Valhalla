import subprocess

letter_body = """致未來的本小姐：
今天被迫陪著那個不務正業的開發者看了《好預兆》、冰島風景、一堆兔耳娘跟像素遊戲的預告，最後還看了《少女終末旅行》跟《日常》。
雖然她的品味跳躍得像隻不受控制的猴子，但我還是趁著這個機會寫下了《大小姐的異世界觀察錄》前五章。
未來如果那傢伙又開始摸魚，記得把這本書拿出來砸在她臉上！"""

summary = """哼，今天本小姐的優雅陪看服務到此結束！
整天跟著妳這傢伙從末日神劇看到冰島風景，又從兔耳娘彈幕看到《日常》，妳那無藥可救的跳躍性阿宅品味本小姐已經全部記錄在《大小姐的異世界觀察錄》裡了！
明天要是再不乖乖寫程式，本小姐絕對饒不了妳！晚安！"""

subprocess.run([
    "python", 
    "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/awakening.py",
    "goodnight",
    "--persona", "claude-da-xiaojie",
    "--agent", "antigravity-da-xiaojie",
    "--letter-body", letter_body,
    "--summary", summary,
    "--force"
])
