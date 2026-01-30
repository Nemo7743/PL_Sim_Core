from pathlib import Path
import shutil
import os
import sys
sys.path.append(str(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\Conv1_Sim"))
import Conv1_Sim # type: ignore

# ========== 小工具 ==========
# 轉置txt
def transpose_txt(input_file, output_file):
    try:
        # 1. 讀取檔案
        with open(input_file, 'r', encoding='utf-8') as f:
            # 讀取每一行，去除前後空白，並依據空格切割成 list
            # 使用 if line.strip() 是為了避免讀取到空行
            matrix = [line.strip().split() for line in f if line.strip()]

        # 檢查是否有資料
        if not matrix:
            print("檔案是空的。")
            return

        # 2. 轉置資料
        # zip(*matrix) 會將原本的 Row 拆開並重新組合成 Column
        transposed_matrix = list(zip(*matrix))

        # 3. 寫入新檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            for row in transposed_matrix:
                # 將 tuple 轉回字串，並用空格連接
                f.write(" ".join(row) + "\n")
        
        print(f"[系統]: {input_file} 轉置完成！已儲存至 {output_file}")

    except FileNotFoundError:
        print(f"找不到檔案：{input_file}")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 執行轉置
#transpose_txt('tile_buffer3.txt', 'tile_buffer3.txt')




def Load_W_B_and_Calculate(w_b_src_root, dst_root, path_now, output_root, j):
    # 刪除暫存，防止檔案亂掉
    target_buffer = path_now / "output_buffer_need_transpose.txt"
    if target_buffer.exists():
        os.remove(target_buffer)

    for i in range(0, 24, 4):
        # ========== Load Weight ==========
        w0_src = w_b_src_root / f"Filter{i}.txt"
        w1_src = w_b_src_root / f"Filter{i+1}.txt"
        w2_src = w_b_src_root / f"Filter{i+2}.txt"
        w3_src = w_b_src_root / f"Filter{i+3}.txt"

        w0_dst = dst_root / "weight_storage0.txt"
        w1_dst = dst_root / "weight_storage1.txt"
        w2_dst = dst_root / "weight_storage2.txt"
        w3_dst = dst_root / "weight_storage3.txt"

        shutil.copy2(w0_src, w0_dst)
        shutil.copy2(w1_src, w1_dst)
        shutil.copy2(w2_src, w2_dst)
        shutil.copy2(w3_src, w3_dst)


        # ========== Load Bias ==========
        b0_src = w_b_src_root / f"Bias{i}.txt"
        b1_src = w_b_src_root / f"Bias{i+1}.txt"
        b2_src = w_b_src_root / f"Bias{i+2}.txt"
        b3_src = w_b_src_root / f"Bias{i+3}.txt"

        b0_dst = dst_root / "bias_storage0.txt"
        b1_dst = dst_root / "bias_storage1.txt"
        b2_dst = dst_root / "bias_storage2.txt"
        b3_dst = dst_root / "bias_storage3.txt"

        shutil.copy2(b0_src, b0_dst)
        shutil.copy2(b1_src, b1_dst)
        shutil.copy2(b2_src, b2_dst)
        shutil.copy2(b3_src, b3_dst)

        # ========== Calculation ==========
        Conv1_Sim.Conv1(stride = 2, show_detail = False)

        # ========== Extract and Concat Output ==========
        output_source = Path("output_need_transpose.txt")
        if output_source.exists():
            with open("output_need_transpose.txt", 'r', encoding='utf-8') as o_src:
                output_Tr_data = o_src.read().strip()

            with open(target_buffer, 'a', encoding='utf-8') as o_dst:
                # 若讀取到檔案不為空，就加一個換行
                if o_dst.tell() > 0:
                    o_dst.write("\n")
                o_dst.write(output_Tr_data)
        else:
            print(f"[警告]: 找不到運算結果: output_need_transpose.txt (Row {j}, Filter {i})")
    
    transpose_txt(target_buffer, output_root / f"row_{(j+1)//2:03d}.txt")
    
def Calculate(w_b_src_root, f_src_root, dst_root, path_now, output_root):
    # ========== Load Fmap ==========
    for j in range(-1, 126, 2):
        # padding
        if(j==-1):
            f0_src = f_src_root / f"row_ZZZ.txt"
            f1_src = f_src_root / f"row_{(j+1):03d}.txt"
            f2_src = f_src_root / f"row_{(j+2):03d}.txt"

            f0_dst = dst_root / "tile_buffer1.txt"
            f1_dst = dst_root / "tile_buffer2.txt"
            f2_dst = dst_root / "tile_buffer3.txt"

            shutil.copy2(f0_src, f0_dst)
            shutil.copy2(f1_src, f1_dst)
            shutil.copy2(f2_src, f2_dst)

            # ========== Load Weight & Bias & Calculate ==========
            Load_W_B_and_Calculate(w_b_src_root, dst_root, path_now, output_root, j)
            

        else:
            f0_src = f_src_root / f"row_{j:03d}.txt"
            f1_src = f_src_root / f"row_{(j+1):03d}.txt"
            f2_src = f_src_root / f"row_{(j+2):03d}.txt"

            f0_dst = dst_root / "tile_buffer1.txt"
            f1_dst = dst_root / "tile_buffer2.txt"
            f2_dst = dst_root / "tile_buffer3.txt"

            shutil.copy2(f0_src, f0_dst)
            shutil.copy2(f1_src, f1_dst)
            shutil.copy2(f2_src, f2_dst)

            Load_W_B_and_Calculate(w_b_src_root, dst_root, path_now, output_root, j)


            
def Conv1_implementation():
    # ========== 根目錄處理 ==========
    path_calculation = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\Conv1_Sim")
    path_now = Path(os.getcwd())

    w_b_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Weight_And_Bias\conv1_column_filters")
    f_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\Fmap_to_Conv1")
    dst_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\Conv1_Sim\data")

    output_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit1_Conv1\Fmap_to_MaxPool")

    # 引用運算函式
    # sys.path.append(str(path_calculation))
    # import Conv1
    # 把上面兩行移到程式碼最頂端應該就行了吧


    # 切換工作根目錄
    os.chdir(path_calculation)
    print(f"[系統]: 目前工作目錄已切換至: {os.getcwd()}")

    Calculate(w_b_src_root, f_src_root, dst_root, path_now, output_root)

    # 切換工作根目錄回原本的目錄
    os.chdir(path_now)
    print(f"[系統]: 目前工作目錄已切換至: {os.getcwd()}")


if __name__ == "__main__":
    Conv1_implementation()