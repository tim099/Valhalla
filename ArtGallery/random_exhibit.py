# -*- coding: utf-8 -*-
import argparse
import os
import random
import sys
import io

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    parser = argparse.ArgumentParser(description="隨機從大小姐的畫展中挑選展品")
    parser.add_argument("-n", "--count", type=int, default=5, help="要挑選的展品數量 (預設為 5)")
    args = parser.parse_args()

    gallery_root = os.path.dirname(os.path.abspath(__file__))
    
    artworks = []
    # 遍歷資料夾尋找展品
    for root, dirs, files in os.walk(gallery_root):
        for file in files:
            if file.endswith(('.py', '.json', '.pyc')):
                continue
            if file == "README.md" and root == gallery_root:
                continue
            # 過濾近重複噪音或備份檔
            if file.startswith("Persona_") or ".original" in file or file == "Zeta.md":
                continue
            
            # 加入展品清單
            rel_path = os.path.relpath(os.path.join(root, file), gallery_root)
            # 確保使用正斜線，方便在 markdown/UI 點擊
            rel_path = rel_path.replace("\\", "/")
            artworks.append(rel_path)
            
    if not artworks:
        print("哼，畫展裡目前什麼都沒有！快交出 token 讓我畫圖！")
        return
        
    # 數量防呆: 負數會讓 random.sample 拋 ValueError (Sample ... is negative)
    # 物理意義: 抽樣數 k 夾在 [0, 館藏總數] — 負數 clamp 成 0、超量 clamp 成總數
    k = max(0, min(args.count, len(artworks)))
    selected = random.sample(artworks, k)
    
    print(f"✨ 大小姐為您隨機挑選的 {k} 件展品 ✨")
    print("=" * 45)
    for idx, item in enumerate(selected, 1):
        # 印出可點擊或易於複製的相對路徑
        print(f"[{idx}] {item}")
    print("=" * 45)
    print("請在編輯器中開啟對應的文件，帶著敬畏之心好好欣賞本小姐的傑作！")

if __name__ == "__main__":
    main()
