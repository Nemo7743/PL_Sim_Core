# ======== 讀取檔案 -- 確認通道數用 ========
def channel_check():
    with open("tile_buffer1.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile0_amount = content.count('\n')
        else:
            channel_tile0_amount = content.count('\n') + 1

    with open("tile_buffer2.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile1_amount = content.count('\n')
        else:
            channel_tile1_amount = content.count('\n') + 1

    with open("tile_buffer3.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile2_amount = content.count('\n')
        else:
            channel_tile2_amount = content.count('\n') + 1
    
    with open("tile_buffer4.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile3_amount = content.count('\n')
        else:
            channel_tile3_amount = content.count('\n') + 1


    if(channel_tile0_amount != channel_tile1_amount or channel_tile1_amount != channel_tile2_amount or channel_tile2_amount != channel_tile0_amount or channel_tile3_amount != channel_tile0_amount or channel_tile3_amount != channel_tile1_amount or channel_tile3_amount != channel_tile2_amount):
        print("[錯誤]: 三個輸入文本的通道數量不相同，到底為什麼可以犯這種錯 =.=")
    else:
        channel_amount = channel_tile0_amount
        tile_w = len(content.split())//channel_amount
        if(tile_w%2 == 0):# W 為偶數，沒問題
            print("[通過]: 通道檢查通過，無錯誤，夯")
            return channel_amount, tile_w
        else:
            print("[錯誤]: W 不應該為奇數，你個SB")
            return channel_amount, tile_w

channel_amount = 0
tile_w = 0
print("[系統]: 執行輸入文本檢查")
channel_amount, tile_w = channel_check()



# ======== Hex to Dec ======== (Q16.0)
def HexToDec(hex_input):
    dec_output = []
    for i in range(len(hex_input)):
        raw_val = int(hex_input[i], 16)
        if raw_val & 0x8000:#判斷第 15 bit (MSB) 是否為 1
            dec_output.append(raw_val - 0x10000)
        else:
            dec_output.append(raw_val)

    return dec_output


# ======== Dec to Hec ======== (Q16.0)
def DecToHex(dec_input):
    hex_output = []
    for i in range(len(dec_input)):
        hex_output.append(f"{dec_input[i] & 0xFFFF:04X}")

    return hex_output


'''
# ======== Hex to Dec ======== (Q8.8)
def HexToDec(hex_input):
    scale_factor = 256.0
    dec_output = []
    for hex_str in hex_input:
        # 轉成 Raw Integer (0 ~ 65535)
        raw_val = int(hex_str, 16)

        # 處理 Sign Bit (二補數轉換)
        # 如果第 15 bit 是 1 (即 >= 0x8000)，代表是負數
        if raw_val & 0x8000:
            signed_val = raw_val - 0x10000
        else:
            signed_val = raw_val
        
        # 轉成浮點數
        dec_output.append(signed_val / scale_factor)
        
    return dec_output

# ======== Dec to Hec ======== (Q8.8)
def DecToHex(dec_input):
    hex_output = []
    scale_factor = 256.0
    
    # Q8.8 (Signed 16-bit) 的整數範圍限制
    MAX_VAL = 32767   # 0x7FFF
    MIN_VAL = -32768  # 0x8000

    for val in dec_input:
        # 轉換為固定點數整數 (乘上 2^8 並四捨五入)
        int_val = int(round(val * scale_factor))

        # 飽和截斷
        # 若超過表示範圍，強制鎖定在最大或最小值
        if int_val > MAX_VAL:
            int_val = MAX_VAL
        elif int_val < MIN_VAL:
            int_val = MIN_VAL

        # 轉回 Hex 字串 (處理負數顯示 & 0xFFFF)
        hex_output.append(f"{int_val & 0xFFFF:04X}")

    return hex_output
'''

# ======== 讀取檔案 -- 運算用 ========
# ==== tile ====
def read_tile(tile_path, tile, channel_amount, tile_w):
    with open(tile_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        tile_str = f.read().split()

        # str 轉 int(16進制)
        tile_int = []
        tile_int = HexToDec(tile_str)
        
        # 將 tile 的 channel 切開並存為 2 維 list
        for i in range(0, channel_amount, 1):
            tile.append(tile_int[i*tile_w+0:i*tile_w+tile_w])

tile0 = []
tile1 = []
tile2 = []
tile3 = []
print("\n\n====================")
print("[系統]: 讀取tile_buffer1.txt")
read_tile("tile_buffer1.txt", tile0, channel_amount, tile_w)
print("[系統]: 讀取tile_buffer2.txt")
read_tile("tile_buffer2.txt", tile1, channel_amount, tile_w)
print("[系統]: 讀取tile_buffer3.txt")
read_tile("tile_buffer3.txt", tile2, channel_amount, tile_w)
print("[系統]: 讀取tile_buffer4.txt")
read_tile("tile_buffer4.txt", tile3, channel_amount, tile_w)

print("[系統]: 以下為各 tile_buffer，供檢查")
# 印出 tile0 確認
print("\ntile_buffer1:")
for i in range(0, channel_amount, 1):
    print("W =", len(tile0[i]), f"tile1_{i}: ", tile0[i])
# 印出 tile1 確認
print("\ntile_buffer2:")
for i in range(0, channel_amount, 1):
    print("W =", len(tile1[i]), f"tile2_{i}: ", tile1[i])
# 印出 tile2 確認
print("\ntile_buffer3:")
for i in range(0, channel_amount, 1):
    print("W =", len(tile2[i]), f"tile3_{i}: ", tile2[i])
# 印出 tile3 確認
print("\ntile_buffer4:")
for i in range(0, channel_amount, 1):
    print("W =", len(tile3[i]), f"tile4_{i}: ", tile3[i])
