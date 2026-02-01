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

'''
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

# ======== Hex to Dec ======== (Q16.16)
def HexToDec_Q16_16(hex_input):
    # Q16.16 表示有 16 個小數位
    # Scale Factor = 2^16 = 65536.0
    scale_factor = 65536.0
    
    dec_output = []
    for hex_str in hex_input:
        # 轉成 Raw Integer (32-bit 範圍: 0 ~ 4294967295)
        raw_val = int(hex_str, 16)

        # 處理 Sign Bit (32-bit 二補數轉換)
        # Q16.16 是 32-bit 格式，MSB 是第 31 bit (即 >= 0x80000000)
        if raw_val & 0x80000000:
            # 若為負數，減去 2^32 (0x100000000)
            signed_val = raw_val - 0x100000000
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




# ======== 讀取檔案 -- 確認通道數用 ========
def channel_check(tile0, weight):
    if(len(weight) != 4):
        print(f"[錯誤]: Bias 數量應該要是 4，但偵測到 {len(weight)} 個 bias")
        return "FUC it's wrong"

    weight0_len = len(weight[0])-1
    weight1_len = len(weight[1])-1
    weight2_len = len(weight[2])-1
    weight3_len = len(weight[3])-1

    channel_tile0_amount = len(tile0)

    if(channel_tile0_amount != weight0_len or channel_tile0_amount != weight1_len or channel_tile0_amount != weight2_len or channel_tile0_amount != weight3_len):
        print("[錯誤]: 權重和 FMap 的通道數量不匹配，到底為什麼可以犯這種錯 =.=")
    else:
        channel_amount = channel_tile0_amount
        tile_w = len(tile0[0])
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

def assem_bias(bias_path):
    bias_str = []

    with open("data/bias_storage0.txt", "r", encoding = "utf-8") as f:
        bias_str.append(f.read())
    with open("data/bias_storage1.txt", "r", encoding = "utf-8") as f:
        bias_str.append(f.read())
    with open("data/bias_storage2.txt", "r", encoding = "utf-8") as f:
        bias_str.append(f.read())
    with open("data/bias_storage3.txt", "r", encoding = "utf-8") as f:
        bias_str.append(f.read())

    with open(bias_path, "w", encoding = "utf-8") as f:
        for i in range(0, len(bias_str), 1):
            f.write(bias_str[i])
            f.write("\n")

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
def read_weight(weight_path, weight):
    with open(weight_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        weight_str_a = f.read().split()

    # 將讀取到的權重做成一個 list
    weight_str_b = []
    for i in range(0, len(weight_str_a)+1, 1):
        if(i == 0):
            weight_str_b.append('0')
        else:
            weight_str_b.append(weight_str_a[i-1])

    # str 轉 int(16進制)
    weight_int = []
    weight_int = HexToDec(weight_str_b)
    
    # 將本次權重插入 list 形成二維陣列
    weight.append(weight_int)
'''
weight = []
print("\n\n====================")
print("[系統]: 讀取weight_storage0.txt")
read_weight("weight_storage0.txt", weight)
print("[系統]: 讀取weight_storage1.txt")
read_weight("weight_storage1.txt", weight)
print("[系統]: 讀取weight_storage2.txt")
read_weight("weight_storage2.txt", weight)
print("[系統]: 讀取weight_storage3.txt")
read_weight("weight_storage3.txt", weight)

print("[系統]: 以下為各 weight_storage，供檢查\n")
print(f"weight_storage0:\nbias: {weight[0][0]}, W0: {weight[0][1:]}\n")
print(f"weight_storage1:\nbias: {weight[1][0]}, W0: {weight[1][1:]}\n")
print(f"weight_storage2:\nbias: {weight[2][0]}, W0: {weight[2][1:]}\n")
print(f"weight_storage3:\nbias: {weight[3][0]}, W0: {weight[3][1:]}")
'''

# ==== bias ====
def read_bias(bias_path, weight):
    with open(bias_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        bias_str_a = f.read().split()
    
    # str 轉 int(16進制)
    weight_int = []
    weight_int = HexToDec_Q16_16(bias_str_a)

    # 將 bias 存入陣列的 [0]
    for i in range(0, len(bias_str_a), 1):
        weight[i][0] = weight_int[i]


# ======== 進行 PW 計算 ========
def Calculation(stride = 1, show_detail = True, weight = [], tile0 = [], tile_w = 0):
    conv_PW = 0
    output = []
    if(stride != 1):
        print("[錯誤]: Stride 在 PW 只能是 1，天才")
        output.append("Poop")
        return output


    for i in range(0, len(weight), 1):
        output_inn = []
        for j in range(0, tile_w, 1):
            
            conv_PW = weight[i][0]
            for k in range(0, len(tile0), 1):
                conv_PW = weight[i][k+1] * tile0[k][j] + conv_PW
                if(show_detail):
                    if(k==0):
                        print(f"{conv_PW:>20} = {weight[i][k+1]:15}(W{i}) * {tile0[k][j]:>15}(T1_Out_Ch{i}) + {conv_PW - (weight[i][k+1] * tile0[k][j]):>15}(bias)")
                    else:
                        print(f"{conv_PW:>20} = {weight[i][k+1]:15}(W{i}) * {tile0[k][j]:>15}(T1_Out_Ch{i}) + {conv_PW - (weight[i][k+1] * tile0[k][j]):>15}(prev)")
            output_inn.append(conv_PW)
            if(show_detail):
                print(conv_PW)
        output.append(output_inn)

    return output


def PW(tile0, weight, stride, show_detail):
    '''
    Docstring for PW
    
    :param tile0: 二維陣列[ in_channel(0-不一定) ][ w(0-不一定) ]
    :param weight: 二維陣列[ out_channel(0-3) ][ b(0) + w(1-不一定) ]
    :param stride: 必須是 1
    :param show_detail: 要不要顯示運算過程
    '''

    '''
    # ======== 轉置輸入 FMap 檔案 ========(這個部分外部讀取檔案的程式碼已經先轉置過了，不用做)
    print("====================")
    print("[系統]: 轉置輸入 FMap 檔案")
    transpose_txt("data/tile_buffer1.txt", "tile_buffer1_Tr.txt")
    # 讀取 bias 0 - 3 組合成新檔案
    assem_bias("bias_storage.txt")
    '''
    # ======== 確認通道數 ========
    channel_amount = 0
    tile_w = 0
    if(show_detail):
        print("\n\n====================")
        print("[系統]: 執行通道數檢查")
    channel_amount, tile_w = channel_check(tile0, weight)

    # ======== 展示當前運算的 Fmap 和 Weight ========
    # ==== tile ====
    if(show_detail): print("\n\n====================")
    '''
    print("[系統]: 讀取tile_buffer1_Tr.txt")
    read_tile("tile_buffer1_Tr.txt", tile0, channel_amount, tile_w)
    '''
    if(show_detail):
        print("[系統]: 以下為各 tile_buffer，供檢查")
        # 印出 tile0 確認
        print("\ntile_buffer1:")
        for i in range(0, channel_amount, 1):
            print("W =", len(tile0[i]), f"tile1_{i}: ", end="")
            for j in range(0, len(tile0[i]), 1):
                print(f"{tile0[i][j]:<5}", end="")
            print("\n", end="")
    
    # ==== weight ====
    weight = []
    if(show_detail): print("\n\n====================")
    '''
    print("[系統]: 讀取weight_storage0.txt")
    read_weight("data/weight_storage0.txt", weight)
    print("[系統]: 讀取weight_storage1.txt")
    read_weight("data/weight_storage1.txt", weight)
    print("[系統]: 讀取weight_storage2.txt")
    read_weight("data/weight_storage2.txt", weight)
    print("[系統]: 讀取weight_storage3.txt")
    read_weight("data/weight_storage3.txt", weight)
    '''
    # ==== bias ====
    '''
    print("[系統]: 讀取bias_storage.txt")
    read_bias("bias_storage.txt", weight)
    '''
    if(show_detail):
        print("[系統]: 以下為各 weight_storage，供檢查\n")
        print(f"weight_storage0:\nbias: {weight[0][0]}, W0: {weight[0][1:]}\n")
        print(f"weight_storage1:\nbias: {weight[1][0]}, W1: {weight[1][1:]}\n")
        print(f"weight_storage2:\nbias: {weight[2][0]}, W2: {weight[2][1:]}\n")
        print(f"weight_storage3:\nbias: {weight[3][0]}, W3: {weight[3][1:]}")
    
    # ======== 進行 PW 計算 ========
    if(show_detail):  print("\n\n====================")
    output = Calculation(stride, show_detail, weight, tile0, tile_w)
    if(show_detail):
        print("[系統]: 以下為最終計算結果")

    if(show_detail): 
        # 進位轉換
        hex_output = []
        for i in range(0, len(output), 1):
            hex_output.append(DecToHex(output[i]))

    if(show_detail):
        print("output(Float10) =", output)
        print("output( Q8.8  ) =", hex_output)
        print("\n")

    print("\n[完成]: PW 運算完成")
    return output

if __name__ == "__main__":
    PW(stride = 1, show_detail = True)