import os

def convert_txt_to_coe(input_file, output_file):
    try:
        # 1. 讀取 TXT 檔案
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 資料清理與分割
        # 移除換行符號，去除前後空白
        content = content.replace('\n', '').strip()
        
        # 如果原始資料最後有分號，先移除以免轉換錯誤
        if content.endswith(';'):
            content = content[:-1]

        # 依照逗號分割成列表
        str_numbers = content.split(',')

        binary_list = []
        
        # 3. 轉換邏輯
        for s in str_numbers:
            s = s.strip() # 去除數字前後的空白
            if s: # 確保不是空字串
                try:
                    num = int(s)
                    # 格式化為 14-bit 二進位，不足補 0
                    # 0: 補零, 14: 長度14, b: 二進位
                    bin_str = f"{num:014b}"
                    binary_list.append(bin_str)
                except ValueError:
                    print(f"警告：無法轉換 '{s}'，已跳過。")

        # 4. 組合輸出內容
        # 檔頭
        header = "memory_initialization_radix=2;\nmemory_initialization_vector=\n"
        
        # 組合數據：用 "逗號+換行" 連接
        # COE 檔規範：最後一筆資料後面通常接分號，其餘接逗號
        data_block = ",\n".join(binary_list) + ";"

        final_content = header + data_block

        # 5. 寫入 COE 檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"轉換成功！")
        print(f"來源檔案: {input_file}")
        print(f"輸出檔案: {output_file}")
        print(f"總共轉換了 {len(binary_list)} 筆資料。")

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{input_file}'，請確認檔案是否在同一目錄下。")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")

# --- 建立範例輸入檔 (為了方便您測試，這段會自動建立 input.txt) ---
def create_sample_input():
    sample_data = "0, 96, 2, 98, 4, 100, 6, 102, 8, 104, 10, 106, 12, 108, 14, 110, 16, 112, 18, 114, 20, 116, 22, 118, 24, 120, 26, 122, 28, 124, 30, 126, 32, 128, 34, 130, 36, 132, 38, 134, 40, 136, 42, 138, 44, 140, 46, 142, 48, 144, 50, 146, 52, 148, 54, 150, 56, 152, 58, 154, 60, 156, 62, 158, 64, 160, 66, 162, 68, 164, 70, 166, 72, 168, 74, 170, 76, 172, 78, 174, 80, 176, 82, 178, 84, 180, 86, 182, 88, 184, 90, 186, 92, 188, 94, 190;"
    with open("input.txt", "w") as f:
        f.write(sample_data)
    print("已建立範例 input.txt 檔案。\n")

# --- 主程式執行區 ---
if __name__ == "__main__":
    # 如果 input.txt 不存在，先建立一個範例 (您可以註解掉這行)
    #if not os.path.exists("input.txt"):
    #    create_sample_input()
        
    # 執行轉換
    input_file = "Channel_To_Y_All_V2.txt"
    output_file = "Channel_To_Y.coe"

    #input_file = "stage0.txt"
    #output_file = "Channel_To_Y.coe"


    convert_txt_to_coe(input_file, output_file)