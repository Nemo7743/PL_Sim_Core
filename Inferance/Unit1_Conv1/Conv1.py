from pathlib import Path
import shutil

# 定義基礎路徑 (使用原始字串 r'' 避免轉義字元問題)
src_base = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\Fmap_to_Conv1")
dst_path = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit1_Conv1\data\tile_buffer1.txt")

# 確保目標資料夾存在
dst_path.parent.mkdir(parents=True, exist_ok=True)
filename = f"row_000.txt"
src_file = src_base / filename
shutil.copy2(src_file, dst_path)
'''
for i in range(128):
    # 使用 :03d 進行補零，產生 000, 001, 002...
    filename = f"row_{i:03d}.txt"
    src_file = src_base / filename
    
    # 檢查檔案是否存在再搬運
    if src_file.exists():
        # 注意：如果目標是同一個檔案，會不斷被覆蓋
        # 如果你想根據 i 命名目標檔案，建議 dst_path 也要動態生成
        shutil.copy2(src_file, dst_path)
        print(f"已複製: {filename}")
    else:
        print(f"找不到檔案: {src_file}")

'''


src_base = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\Fmap_to_Conv1")
# 確保目標資料夾存在
dst_path.parent.mkdir(parents=True, exist_ok=True)

# ========== Load Weight ==========
for i in range(0, 24, 4):
    print(i)
# ========== Load Bias ==========
for i in range(0, 24, 4):
    print(i)
# ========== Load Fmap ==========
for i in range(0, 128, 2):
    print(i-1)



w_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Weight_And_Bias\conv1_column_filters")
w_dst_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\Conv1_Sim\data")

for i in range(0, 24, 4):
    # ========== Load Weight ==========
    w0_name = f"Filter{i}"
    w1_name = f"Filter{i+1}"
    w2_name = f"Filter{i+2}"
    w3_name = f"Filter{i+3}"

    w0_src = w_src_root / w0_name
    w1_src = w_src_root / w1_name
    w2_src = w_src_root / w2_name
    w3_src = w_src_root / w3_name
        
    w0_dst = w_dst_root / ""
    w1_dst = ""
    w2_dst = ""
    w3_dst = ""




