import os
import numpy as np
from PIL import Image

# ==========================================
# 引用 Function: DecToHex (Q16.0)
# ==========================================
def DecToHex(dec_input):
    """
    將十進位數值陣列轉換為 4 位數 16 進位字串陣列
    例如: [10, 255] -> ['000A', '00FF']
    """
    hex_output = []
    for i in range(len(dec_input)):
        # & 0xFFFF 確保數值在 16-bit 範圍內，並處理負數 (二補數表現)
        # :04X 代表轉為大寫 16 進位，不足 4 位補 0
        hex_output.append(f"{dec_input[i] & 0xFFFF:04X}")

    return hex_output

# ==========================================
# 主處理函式
# ==========================================
def image_preprocessing(image_path, output_folder="Fmap_to_Conv1"):
    # 1. 檢查並建立輸出資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已建立資料夾: {output_folder}")
    else:
        print(f"資料夾 {output_folder} 已存在，將覆蓋內容。")

    try:
        # 2. 讀取圖片並強制轉換為 RGB
        img = Image.open(image_path).convert('RGB')
        
        # 3. 降解析度至 128x128
        target_size = (128, 128)
        img_resized = img.resize(target_size, Image.Resampling.BILINEAR)
        
        # 4. 轉換為 Numpy Array
        # 形狀為 (128, 128, 3)
        img_array = np.array(img_resized, dtype=np.int32)

        # ==========================================
        # 5. Q16.0 數值準備
        # ==========================================
        
        # 【選項 A】直接使用原始 0~255
        img_q16 = img_array 
        
        # 【選項 B】若需中心化 (-128 ~ 127)，請解開下行註解
        # img_q16 = img_array - 128
        
        # 轉為 int16 (雖 DecToHex 會處理，但這裡先轉型較嚴謹)
        img_q16 = img_q16.astype(np.int16)

        print(f"圖片處理中... 格式: Q16.0 (Hex), 尺寸: {target_size}")

        # 6. 寫入 txt 檔案
        height, width, channels = img_q16.shape

        for h in range(height):
            # 檔名：row_000.txt ~ row_127.txt
            filename = os.path.join(output_folder, f"row_{h:03d}.txt")
            
            with open(filename, 'w') as f:
                for w in range(width):
                    # 取得該點的 (R, G, B)
                    r_val = img_q16[h, w, 0]
                    g_val = img_q16[h, w, 1]
                    b_val = img_q16[h, w, 2]
                    
                    # 準備輸入陣列: [R, G, B, Padding]
                    # 最後補一個 0，對應輸出的第 4 個欄位 '0000'
                    #input_values = [r_val, g_val, b_val, 0]
                    input_values = [int(r_val), int(g_val), int(b_val), 0]
                    
                    # 呼叫轉換 Function
                    hex_values = DecToHex(input_values)
                    
                    # 將 list 轉為空白分隔的字串
                    # 例如: "00FF 00A0 0010 0000"
                    line_content = " ".join(hex_values)
                    
                    # 寫入一行
                    f.write(f"{line_content}\n")
        
        print(f"處理完成！已產生 {height} 個 txt 檔於 '{output_folder}'。")

    except Exception as e:
        print(f"發生錯誤: {e}")

# --- 主程式執行區 ---
if __name__ == "__main__":
    # 請修改這裡的圖片路徑
    input_image_path = "input.jpg"
    
    if os.path.exists(input_image_path):
        image_preprocessing(input_image_path)
    else:
        print(f"找不到檔案: {input_image_path}，請確認路徑。")