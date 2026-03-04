import numpy as np
import cv2

def convert_txt_uyvy_fixed_endian_to_png(txt_path, output_png_path, width=640, height=384):
    print(f"開始處理檔案: {txt_path} ...")
    
    # 1. 讀取純文字檔案，並過濾掉換行符號與空白
    with open(txt_path, 'r') as f:
        hex_string = f.read().replace('\n', '').replace('\r', '').replace(' ', '')
    
    # 2. 將 16 進位字串轉換為真實的位元組 (bytes)
    try:
        byte_data = bytes.fromhex(hex_string)
    except ValueError as e:
        print(f"解析 Hex 字串失敗: {e}")
        return

    # --- 關鍵修正：處理 64-bit Little-Endian 位元組順序反轉 ---
    # 將資料轉為 Numpy 陣列，並切分為多個長度為 8 (64-bit) 的區塊
    arr_64b = np.frombuffer(byte_data, dtype=np.uint8).reshape(-1, 8)
    
    # 將每個區塊內的位元組順序左右反轉 [:, ::-1]，然後轉回 bytes
    fixed_byte_data = arr_64b[:, ::-1].tobytes()
    # -----------------------------------------------------------

    expected_bytes = width * height * 2
    
    # 防呆機制：檢查修正後的資料長度
    if len(fixed_byte_data) != expected_bytes:
        print(f"⚠️ 警告: 資料長度 ({len(fixed_byte_data)} bytes) 與預期的 ({expected_bytes} bytes) 不符！")
        if len(fixed_byte_data) < expected_bytes:
            print("❌ 錯誤: 資料量不足，程式提前結束。")
            return
        else:
            print("ℹ️ 提示: 資料過長，將自動截斷。")
            fixed_byte_data = fixed_byte_data[:expected_bytes]

    # 3. 轉換為 UYVY 矩陣 (將 fixed_byte_data 轉為 numpy array)
    uyvy_array = np.frombuffer(fixed_byte_data, dtype=np.uint8).reshape((height, width, 2))

    # 4. 使用 OpenCV 將 UYVY 轉換為 BGR 格式 (恢復使用 UYVY)
    bgr_image = cv2.cvtColor(uyvy_array, cv2.COLOR_YUV2BGR_UYVY)

    # 5. 儲存成 PNG 檔案
    cv2.imwrite(output_png_path, bgr_image)
    print(f"✅ 轉換成功！圖片已儲存至: {output_png_path}")

# ==========================================
# 執行範例
# ==========================================
if __name__ == "__main__":
    input_file = "new_image_hex_64b.txt"  
    output_file = "output_fixed.png"
    
    convert_txt_uyvy_fixed_endian_to_png(input_file, output_file)