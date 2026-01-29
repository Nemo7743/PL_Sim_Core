import statistics
# ======== 小工具 ========
# 轉置txt
def transpose_txt(input_file, output_file):
    try:
        # 1. 讀取檔案
        with open(input_file, 'r', encoding='utf-8') as f:
            # 讀取每一行，去除前後空白，並依據空格切割成 list
            # 使用 if line.strip() 是為了避免讀取到空行
            matrix = [line.strip().split() for line in f if line.strip()]

        # 檢查是否有資料
        if not matrix:
            print("檔案是空的。")
            return

        # 2. 轉置資料
        # zip(*matrix) 會將原本的 Row 拆開並重新組合成 Column
        transposed_matrix = list(zip(*matrix))

        # 3. 寫入新檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            for row in transposed_matrix:
                # 將 tuple 轉回字串，並用空格連接
                f.write(" ".join(row) + "\n")
        
        print(f"[系統]: {input_file} 轉置完成！已儲存至 {output_file}")

    except FileNotFoundError:
        print(f"找不到檔案：{input_file}")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 執行轉置
#transpose_txt('tile_buffer1.txt', 'tile_buffer1.txt')

''''''
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
''''''

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



# ======== 讀取檔案 -- 確認通道數用 ========
def channel_check():

    with open("tile_buffer1_Tr.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile0_amount = content.count('\n')
        else:
            channel_tile0_amount = content.count('\n') + 1

    with open("tile_buffer2_Tr.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile1_amount = content.count('\n')
        else:
            channel_tile1_amount = content.count('\n') + 1

    with open("tile_buffer3_Tr.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile2_amount = content.count('\n')
        else:
            channel_tile2_amount = content.count('\n') + 1
    
    with open("tile_buffer4_Tr.txt", "r", encoding = "utf-8") as f:
        content = f.read()
        if content.endswith('\n'):
            channel_tile3_amount = content.count('\n')
        else:
            channel_tile3_amount = content.count('\n') + 1


    if(channel_tile0_amount != channel_tile1_amount or channel_tile1_amount != channel_tile2_amount or channel_tile2_amount != channel_tile0_amount or channel_tile3_amount != channel_tile0_amount or channel_tile3_amount != channel_tile1_amount or channel_tile3_amount != channel_tile2_amount):
        print("[錯誤]: 四個輸入文本的通道數量不相同，到底為什麼可以犯這種錯 =.=")
    else:
        channel_amount = channel_tile0_amount
        tile_w = len(content.split())//channel_amount
        if(tile_w%2 == 0):# W 為偶數，沒問題
            print("[通過]: 通道檢查通過，無錯誤，夯")
            return channel_amount, tile_w
        else:
            print("[錯誤]: W 不應該為奇數，你個SB")
            return channel_amount, tile_w

'''
channel_amount = 0
tile_w = 0
print("[系統]: 執行輸入文本檢查")
channel_amount, tile_w = channel_check()
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

'''
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
'''

# ==== weight ====
# 不需要

# ==== bias ====
# 不需要


# ======== 進行 GlbAvgPool 計算 ========
def Calculation(stride = 1, show_detail = True, tile0 = [], tile1 = [], tile2 = [], tile3 = [], tile_w = 0):
    conv_PW = 0
    output = []
    if(stride != -1):
        print("[錯誤]: Stride 在 GlbAvgPool 不存在")
        output.append("Poop")
        return output

    for i in range(1024):
        output_inn = []
        avg_calc = []
        for j in range(0, 4, 1):
            avg_calc.append(tile0[i][j])
        for j in range(0, 4, 1):
            avg_calc.append(tile1[i][j])
        for j in range(0, 4, 1):
            avg_calc.append(tile2[i][j])
        for j in range(0, 4, 1):
            avg_calc.append(tile3[i][j])
        output_inn.append(statistics.mean(avg_calc))
        output.append(output_inn)
        if(show_detail):
            print("mean num:", statistics.mean(avg_calc), "   in:", avg_calc)

    return output


def GlbAvgPool(stride, show_detail):
    # ======== 轉置輸入 FMap 檔案 ========
    print("====================")
    print("[系統]: 轉置輸入 FMap 檔案")
    transpose_txt("tile_buffer1.txt", "tile_buffer1_Tr.txt")
    transpose_txt("tile_buffer2.txt", "tile_buffer2_Tr.txt")
    transpose_txt("tile_buffer3.txt", "tile_buffer3_Tr.txt")
    transpose_txt("tile_buffer4.txt", "tile_buffer4_Tr.txt")

    # ======== 讀取檔案 -- 確認通道數用 ========
    channel_amount = 0
    tile_w = 0
    print("\n\n====================")
    print("[系統]: 執行通道數檢查")
    channel_amount, tile_w = channel_check()

    # ======== 讀取檔案 -- 運算用 ========
    # ==== tile ====
    tile0 = []
    tile1 = []
    tile2 = []
    tile3 = []
    print("\n\n====================")
    print("[系統]: 讀取tile_buffer1_Tr.txt")
    read_tile("tile_buffer1_Tr.txt", tile0, channel_amount, tile_w)
    read_tile("tile_buffer1_Tr.txt", tile1, channel_amount, tile_w)
    read_tile("tile_buffer1_Tr.txt", tile2, channel_amount, tile_w)
    read_tile("tile_buffer1_Tr.txt", tile3, channel_amount, tile_w)

    if(show_detail):
        print("[系統]: 以下為各 tile_buffer，供檢查")
        # 印出 tile0 確認
        print("\ntile_buffer1:")
        for i in range(0, channel_amount, 1):
            print("W =", len(tile0[i]), f"tile1_{i}: ", end="")
            for j in range(0, len(tile0[i]), 1):
                print(f"{tile0[i][j]:<5}", end="")
            print("\n", end="")
        # 印出 tile1 確認
        print("\ntile_buffer2:")
        for i in range(0, channel_amount, 1):
            print("W =", len(tile1[i]), f"tile2_{i}: ", end="")
            for j in range(0, len(tile1[i]), 1):
                print(f"{tile1[i][j]:<5}", end="")
            print("\n", end="")
        # 印出 tile2 確認
        print("\ntile_buffer3:")
        for i in range(0, channel_amount, 1):
            print("W =", len(tile2[i]), f"tile3_{i}: ", end="")
            for j in range(0, len(tile2[i]), 1):
                print(f"{tile2[i][j]:<5}", end="")
            print("\n", end="")
        # 印出 tile3 確認
        print("\ntile_buffer4:")
        for i in range(0, channel_amount, 1):
            print("W =", len(tile3[i]), f"tile4_{i}: ", end="")
            for j in range(0, len(tile3[i]), 1):
                print(f"{tile3[i][j]:<5}", end="")
            print("\n", end="")
    
    # ==== weight ====
    # 不需要

    # ==== bias ====
    # 不需要

    # ======== 進行 GlbAvgPool 計算 ========
    print("\n\n====================")
    output = Calculation(stride, show_detail, tile0, tile1, tile2, tile3, tile_w)

    if(show_detail):
        print("[系統]: 以下為最終計算結果")

    # 進位轉換
    hex_output = []
    for i in range(0, len(output), 1):
        hex_output.append(DecToHex(output[i]))

    if(show_detail):
        print("output(Float10) =", output)
        print("output( Q8.8  ) =", hex_output)
        print("\n")
    
    # ======== 儲存運算結果 ========
    print("[系統]: 正在儲存計算結果至 output_need_transpose.txt")
    with open('output_need_transpose.txt', 'w', encoding='utf-8') as f:
        for i in range(len(hex_output)):
            for j in range(len(hex_output[i])):
                if(j == len(hex_output[i]) - 1):
                    f.write(str(hex_output[i][j]) + "\n")
                else:
                    f.write(str(hex_output[i][j]) + " ")
    
    transpose_txt("output_need_transpose.txt", "output.txt")

    print("\n[完成]: GlbAvgPool 運算完成")

if __name__ == "__main__":
    GlbAvgPool(stride = -1, show_detail = True)
