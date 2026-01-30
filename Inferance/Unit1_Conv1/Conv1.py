import sys
import os

# 1. 取得目前 Conv1.py 的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 往上跳兩層，到達 PL_Sim_Core 資料夾
# 第一層是 Unit1_Conv1，第二層是 Inferance
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

# 3. 組合出目標資料夾 Calculations\Conv1_Sim 的路徑
target_dir = os.path.join(root_dir, "Calculations", "Conv1_Sim")

# 4. 加入搜尋路徑
if target_dir not in sys.path:
    sys.path.append(target_dir)

# 5. 現在可以匯入 Conv1_Sim.py 了
import Conv1_Sim as conv1

