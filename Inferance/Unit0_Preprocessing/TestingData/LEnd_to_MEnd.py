import os

def fix_endianness_in_txt(input_txt_path, output_txt_path):
    """
    讀取 64-bit Hex 字串，將小端序(Little-Endian)造成的位元組反轉恢復為正端序(Big-Endian)。
    """
    print(f"開始讀取並處理檔案: {input_txt_path} ...")
    
    # 1. 讀取原本的 txt 檔，並把所有換行符號與空白濾除，變成一串純 Hex 字串
    if not os.path.exists(input_txt_path):
        print(f"❌ 找不到檔案: {input_txt_path}")
        return

    with open(input_txt_path, 'r') as f:
        full_hex_string = f.read().replace('\n', '').replace('\r', '').replace(' ', '')
    
    print(f"檔案讀取完畢，總共包含 {len(full_hex_string)} 個 Hex 字元。")

    # 2. 開啟(或建立)新的 txt 檔準備寫入
    with open(output_txt_path, 'w') as f_out:
        # 每次抓取 16 個 Hex 字元 (代表 8 bytes = 64 bits)
        for i in range(0, len(full_hex_string), 16):
            chunk = full_hex_string[i:i+16]
            
            # 確保擷取到的是完整的 16 個字元 (8 bytes)
            if len(chunk) == 16:
                # 步驟拆解：
                # (1) bytes.fromhex(chunk) -> 將 16 個 Hex 字元轉成真正的 8 bytes
                # (2) [::-1] -> 將這 8 個 bytes 的順序完全左右顛倒 (修正 Little-Endian)
                # (3) .hex().upper() -> 把顛倒回來的 bytes 重新變回全大寫的 Hex 字串
                corrected_chunk = bytes.fromhex(chunk)[::-1].hex().upper()
                
                # 將修正好的字串寫入新檔案，並加上換行符號保持排版整齊
                f_out.write(corrected_chunk + '\n')
            else:
                # 如果檔案最後剩下的字元不足 16 個(異常狀況)，則直接寫入不作翻轉
                f_out.write(chunk + '\n')
                
    print(f"✅ 轉換成功！已將修正後的正確順序儲存至: {output_txt_path}")

# ==========================================
# 執行範例
# ==========================================
if __name__ == "__main__":
    # 輸入您的原始檔案 (帶有小端序錯位的資料)
    input_file = "new_image_hex_64b.txt"  
    
    # 輸出修正後的新檔案名稱
    output_file = "corrected_image_hex_64b.txt"
    
    fix_endianness_in_txt(input_file, output_file)