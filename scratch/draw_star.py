import os
import subprocess
import json

pixels = [
    {"x":1024,"y":1022,"color":"#FFD700"},
    {"x":1023,"y":1023,"color":"#FFD700"},
    {"x":1025,"y":1023,"color":"#FFD700"},
    {"x":1022,"y":1024,"color":"#FFD700"},
    {"x":1023,"y":1024,"color":"#FFD700"},
    {"x":1025,"y":1024,"color":"#FFD700"},
    {"x":1026,"y":1024,"color":"#FFD700"},
    {"x":1023,"y":1025,"color":"#FFD700"},
    {"x":1025,"y":1025,"color":"#FFD700"},
    {"x":1022,"y":1026,"color":"#FFD700"},
    {"x":1026,"y":1026,"color":"#FFD700"}
]

json_str = json.dumps(pixels)
subprocess.run(["python", "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/canvas.py", "place", "--pixels", json_str, "--persona", "trailhead"])
subprocess.run(["python", "CardGame/Assets/UCL/UCL_Core/Tools~/AgentCommands/canvas.py", "view", "--region", "1020,1020,10,10", "--scale", "20"])
