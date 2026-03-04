import os

# 目標資料夾路徑
target_dir = r'c:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\Fmap_to_Conv1'

# 準備替換的內容：128列的 "0100 0100 0100 0100"
line_content = "0100 0100 0100 0100"
content = (line_content + "\n") * 128

def replace_files_content():
    if not os.path.exists(target_dir):
        print(f"錯誤：找不到資料夾 {target_dir}")
        return

    files_processed = 0
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        
        # 只處理檔案，排除資料夾
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_processed += 1
                print(f"已更新: {filename}")
            except Exception as e:
                print(f"更新 {filename} 時發生錯誤: {e}")

    print(f"\n完成！共處理了 {files_processed} 個檔案。")

if __name__ == "__main__":
    replace_files_content()
