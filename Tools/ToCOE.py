import os

def clean_txt_to_coe_W(input_filename, output_filename=None):
    """
    讀取 txt，去除空白換行，並轉為 Vivado BRAM Initialization COE 格式。
    格式: Hex (Radix 16), 64-bit (16 hex chars) per line.
    """
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    if output_filename is None:
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.coe"

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = content.replace(" ", "").replace("\n", "").replace("\r", "").upper()

        if len(cleaned_content) % 16 != 0:
            print(f"[警告] {os.path.basename(input_filename)} 的資料長度不是 16 的倍數，最後一筆資料可能會被補零或截斷。")

        chunk_size = 16 
        co_data_lines = []
        
        for i in range(0, len(cleaned_content), chunk_size):
            chunk = cleaned_content[i : i + chunk_size]
            co_data_lines.append(chunk)

        if not co_data_lines:
            print(f"[警告] 檔案 {input_filename} 內容為空。")
            return

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("memory_initialization_radix=16;\n")
            f.write("memory_initialization_vector=\n")
            
            for line in co_data_lines[:-1]:
                f.write(line + ",\n")
            
            f.write(co_data_lines[-1] + ";")

    except Exception as e:
        print(f"處理 {input_filename} 時發生錯誤：{e}")

def clean_txt_to_coe_B(input_filename, output_filename=None):
    """
    讀取 txt，去除空白換行，並轉為 Vivado BRAM Initialization COE 格式。
    格式: Hex (Radix 16), 32-bit (8 hex chars) per line.
    """
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    if output_filename is None:
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.coe"

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = content.replace(" ", "").replace("\n", "").replace("\r", "").upper()

        if len(cleaned_content) % 8 != 0:
            print(f"[警告] {os.path.basename(input_filename)} 的資料長度不是 8 的倍數，最後一筆資料可能會被截斷。")

        chunk_size = 8 
        co_data_lines = []
        
        for i in range(0, len(cleaned_content), chunk_size):
            chunk = cleaned_content[i : i + chunk_size]
            co_data_lines.append(chunk)

        if not co_data_lines:
            print(f"[警告] 檔案 {input_filename} 內容為空。")
            return

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("memory_initialization_radix=16;\n")
            f.write("memory_initialization_vector=\n")
            
            for line in co_data_lines[:-1]:
                f.write(line + ",\n")
            
            f.write(co_data_lines[-1] + ";")

    except Exception as e:
        print(f"處理 {input_filename} 時發生錯誤：{e}")
        

def clean_txt_to_dat(input_filename, output_filename=None):
    """
    讀取 txt，去除空白換行，並將內容每 4 個數字 (16 chars) 換一行輸出為 .dat 檔。
    """
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    if output_filename is None:
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.dat"

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 先把所有不必要的符號 (空白、換行) 全部清乾淨，變成一長串連續字串
        #    例如: "19801981198219831984..."
        cleaned_content = content.replace(" ", "").replace("\n", "").replace("\r", "").upper()

        # 2. 設定切割長度
        #    假設原本文字是 "1980" (4個字)，你要每 4 個數字換一行
        #    所以每行長度 = 4 (字元) * 4 (個數字) = 16 字元
        chars_per_line = 4 * 4  # = 16

        dat_lines = []
        
        # 3. 使用迴圈每 16 個字元切一段
        for i in range(0, len(cleaned_content), chars_per_line):
            chunk = cleaned_content[i : i + chars_per_line]
            dat_lines.append(chunk)

        if not dat_lines:
            print(f"[警告] 檔案 {input_filename} 內容為空。")
            return

        # 4. 寫入檔案，用 join 加上換行符號
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(dat_lines))

        # print(f"[OK] 已輸出：{output_filename}")

    except Exception as e:
        print(f"處理 {input_filename} 時發生錯誤：{e}")

def process_folder_structure(source_root, target_root, BorWorO):
    """
    歷遍 source_root 資料夾，將所有 txt 檔轉換並輸出至 target_root，
    同時保持原有的資料夾結構。
    """
    print(f"開始處理資料夾：{source_root}")
    print(f"輸出目標資料夾：{target_root}")
    print("-" * 30)

    count = 0
    
    # os.walk 會遞迴歷遍所有子目錄
    for dirpath, dirnames, filenames in os.walk(source_root):
        # 1. 計算相對路徑 (例如: subfolder/data)
        rel_path = os.path.relpath(dirpath, source_root)
        
        # 2. 建立對應的目標資料夾路徑
        current_target_dir = os.path.join(target_root, rel_path)
        
        # 如果目標資料夾不存在，則建立它
        if not os.path.exists(current_target_dir):
            os.makedirs(current_target_dir)

        # 3. 處理該層級下的所有檔案
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                # 組合完整的來源檔案路徑
                src_file = os.path.join(dirpath, filename)
                
                # 【修正重點】根據處理類型決定副檔名 (.coe 或 .dat)
                if BorWorO == 'O':
                    dst_extension = ".dat"
                else:
                    dst_extension = ".coe"
                
                dst_filename = os.path.splitext(filename)[0] + dst_extension
                dst_file = os.path.join(current_target_dir, dst_filename)
                
                # 呼叫轉換函式
                if(BorWorO == 'W'):
                    clean_txt_to_coe_W(src_file, dst_file)
                elif(BorWorO == 'B'):
                    clean_txt_to_coe_B(src_file, dst_file)
                elif(BorWorO == 'O'):
                    clean_txt_to_dat(src_file, dst_file)
                else:
                    print("模式錯誤：請輸入 W, B 或 O")
                    continue
                
                count += 1
                print(f"[OK] {rel_path}/{filename} -> {rel_path}/{dst_filename}")

    print("-" * 30)
    print(f"處理完成！共轉換了 {count} 個檔案。")

# ==========================================
# 設定區
# ==========================================
if __name__ == "__main__":
    # ==================== 權重 (Weights) ======================
    input_folder = 'Raw_W' 
    output_folder = 'COE_W'

    if os.path.exists(input_folder):
        process_folder_structure(input_folder, output_folder, 'W')
    else:
        print(f"錯誤：找不到輸入資料夾 '{input_folder}'")


    # ==================== 偏差 (Bias) ======================
    input_folder = 'Raw_B'
    output_folder = 'COE_B'

    if os.path.exists(input_folder):
        process_folder_structure(input_folder, output_folder, 'B')
    else:
        print(f"錯誤：找不到輸入資料夾 '{input_folder}'")

    
    # ==================== 轉換 Output (Dat) ======================
    input_folder = 'Raw_O'
    output_folder = 'DAT_O'

    if os.path.exists(input_folder):
        process_folder_structure(input_folder, output_folder, 'O')
    else:
        print(f"錯誤：找不到輸入資料夾 '{input_folder}'")