import os

def write_hex_file(filename, data_list, items_per_line=16, use_newline=True):
    """
    將整數列表轉換為 Hex 字串並寫入檔案
    use_newline: 是否在達到 items_per_line 時換行
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for i, val in enumerate(data_list):
            # 處理負數的 Hex 格式
            hex_val = f"{val & 0xFFFFFFFF:08x}" if filename.startswith("bias") else f"{val & 0xFFFF:04x}"
            
            f.write(hex_val)
            
            # 檢查是否為最後一個元素
            is_last = (i == len(data_list) - 1)
            
            if not is_last:
                # 換行與空格邏輯
                if use_newline and (i + 1) % items_per_line == 0:
                    f.write("\n")
                else:
                    f.write(" ")
                    
    print(f"[生成] {filename} 完成")

# ==========================================
# 1. 設定數值 (Q8.8) - 保持不變
# ==========================================
VAL_0_0 = 0      # 0x0000
VAL_0_5 = 128    # 0x0080
VAL_1_0 = 256    # 0x0100
VAL_2_0 = 512    # 0x0200
VAL_4_0 = 1024   # 0x0400
VAL_NEG_1 = -256 # 0xFF00

BIAS_0 = 0       # 0.0
BIAS_1 = 65536   # 1.0 (0x00010000)

# ==========================================
# 2. 準備資料陣列 - 保持不變
# ==========================================
tile_buffer = [VAL_0_0] * 1024
weight_0 = [VAL_0_0] * 1024
weight_1 = [VAL_0_0] * 1024

tile_buffer[0]    = VAL_1_0
tile_buffer[1]    = VAL_2_0
tile_buffer[2]    = VAL_NEG_1
tile_buffer[1023] = VAL_0_5

weight_0[0] = VAL_2_0
weight_0[1] = VAL_0_5

weight_1[2]    = VAL_1_0
weight_1[1023] = VAL_4_0

# ==========================================
# 3. 寫入檔案 (修改處)
# ==========================================
# Bias 保持原樣 (1個一行)
bias_data = [BIAS_0, BIAS_1, 0, 0]
write_hex_file("bias_storage0.txt", [bias_data[0]], items_per_line=1)
write_hex_file("bias_storage1.txt", [bias_data[1]], items_per_line=1)

# Weights: 每 4 個數字加一個換行
write_hex_file("weight_storage0.txt", weight_0, items_per_line=4, use_newline=True)
write_hex_file("weight_storage1.txt", weight_1, items_per_line=4, use_newline=True)

# Input Tile: 不加入任何換行 (全部連成一條線)
write_hex_file("tile_buffer1.txt", tile_buffer, use_newline=False)

print("\n[系統]: 所有測試資料生成完畢！")