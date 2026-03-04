import os

def process_unshuffle(input_filename, output_filename, times):
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤: 找不到檔案 '{input_filename}'")
        return

    with open(input_filename, 'r', encoding='utf-8') as f_in:
        # 讀取所有行，並去除首尾空白
        lines = [line.strip() for line in f_in.readlines()]

    groups = []
    current_group = []

    # 步驟 1: 解析檔案，根據空白行分組
    for line in lines:
        if line:  # 如果這一行有內容
            current_group.append(line)
        else:
            # 如果遇到空白行，且當前群組有資料，則儲存並重置
            if current_group:
                groups.append(current_group)
                current_group = []
    
    # 處理最後一組（防止檔案最後沒有空白行而漏掉）
    if current_group:
        groups.append(current_group)

    # 步驟 2: 進行反 Shuffle 處理並寫入
    with open(output_filename, 'w', encoding='utf-8') as f_out:
        for index, group in enumerate(groups):
            
            # 將當前群組的資料暫存到 working_data
            working_data = group

            # --- 核心修改：根據設定次數進行迴圈 ---
            for i in range(times):
                # even_part: 取出索引為 0, 2, 4... 的元素
                even_part = working_data[::2]
                # odd_part: 取出索引為 1, 3, 5... 的元素
                odd_part = working_data[1::2]
                
                # 合併：偶數在前，奇數在後，更新 working_data 以便進行下一輪（如果有的話）
                working_data = even_part + odd_part
            # ------------------------------------

            # 寫入檔案
            for item in working_data:
                f_out.write(f"{item}\n")
            
            # 如果不是最後一組數據，加上空白行分隔
            if index < len(groups) - 1:
                f_out.write("\n")

    print(f"處理完成！(共執行 {times} 次 Unshuffle)")
    print(f"結果已儲存至 '{output_filename}'")

# --- 主程式執行區 ---
if __name__ == "__main__":
    
    #input_file = "model_conv5_input.coe"
    #output_file = "model_conv5_input_Unshuffled_4.coe"

    #input_file = "stage4_output.dat"
    #output_file = "stage4_output_Unshuffled_4.dat"

    input_file = "input.txt"
    output_file = "output.txt"
    UNSHUFFLE_TIMES = 4
    
    # 這裡將設定變數 UNSHUFFLE_TIMES 傳入函式
    process_unshuffle(input_file, output_file, UNSHUFFLE_TIMES)
