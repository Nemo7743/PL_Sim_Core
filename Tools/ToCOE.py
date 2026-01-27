import os

def clean_txt_to_coe(input_filename):
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    # 產生輸出的 .coe 檔名 (保持原本的主檔名)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.coe"

    try:
        # 讀取原始 txt 檔案
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 刪除空格和換行符號
        # replace 順序：先刪除空格，再刪除換行(\n)，最後刪除回車(\r)以防 Windows 格式殘留
        cleaned_content = content.replace(" ", "").replace("\n", "").replace("\r", "")

        # 寫入至 .coe 檔案
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"轉換成功！已輸出檔案：{output_filename}")
        print(f"原始長度：{len(content)} -> 處理後長度：{len(cleaned_content)}")

    except Exception as e:
        print(f"發生錯誤：{e}")


if __name__ == "__main__":
    # ==========================================
    # 請在這裡輸入你的 txt 檔名
    # ==========================================
    target_file = 'tile_buffer1.txt' 

    clean_txt_to_coe(target_file)
