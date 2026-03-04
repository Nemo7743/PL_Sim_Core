import os

def merge_chunks_to_file(input_file, output_file):
    try:
        # 1. 讀取檔案
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 資料清理與分割
        # split() 不帶參數時，會自動依照所有空白字符（包含空格、換行、Tab）進行分割
        # 這步驟會把 "0011", "1122"... 全部變成一個乾淨的列表
        raw_items = content.split()

        if not raw_items:
            print("檔案內容為空，無法處理。")
            return

        merged_lines = []
        
        # 3. 每 4 個一組進行合併
        # range(start, stop, step) -> 從 0 開始，每次跳 4 格
        for i in range(0, len(raw_items), 4):
            # 取出當前位置開始的 4 個元素
            group = raw_items[i : i+4]
            
            # 將這 4 個元素合併成一個字串
            # "".join(['A', 'B']) -> "AB"
            merged_string = "".join(group)
            
            merged_lines.append(merged_string)

        # 4. 格式化輸出
        # 用 "逗號+換行" 將所有合併後的字串接起來
        final_output = "\n".join(merged_lines)
        
        # 最後補上分號
        final_output += ""

        # 5. 寫入新檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)

        print(f"轉換完成！")
        print(f"原始數量: {len(raw_items)} 個單元")
        print(f"合併後數量: {len(merged_lines)} 行")
        print(f"結果已儲存至: {output_file}")

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{input_file}'")
    except Exception as e:
        print(f"發生錯誤: {e}")

# --- 建立範例輸入檔 (方便測試用) ---
def create_sample_input():
    sample_data = """0011 1122 2233 3344 4455 5566 6677 7788
8899 00AA AABB BBCC CCDD DDEE EEFF FF00"""
    
    with open("data_input.txt", "w") as f:
        f.write(sample_data)
    print("已建立範例 data_input.txt 檔案。\n")

# --- 主程式 ---
if __name__ == "__main__":
    # 如果沒有輸入檔，先建立一個範例
    #if not os.path.exists("data_input.txt"):
    #    create_sample_input()

    input = "model_conv5_input_Unshuffled_4.coe"
    output = "model_conv5_input_Unshuffled_4_Untiling.coe"


    #input = "stage4_output_Unshuffled_4.dat"
    #output = "stage4_output_Unshuffled_4_Untiliing.dat"


    # 執行轉換
    merge_chunks_to_file(input, output)
    