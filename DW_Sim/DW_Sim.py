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


    if(channel_tile0_amount != channel_tile1_amount or channel_tile1_amount != channel_tile2_amount or channel_tile2_amount != channel_tile0_amount):
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


'''
channel_amount = 0
tile_w = 0
print("[系統]: 執行輸入文本檢查")
channel_amount, tile_w = channel_check()
'''


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
print("\n\n====================")
print("[系統]: 讀取tile_buffer1.txt")
read_tile("tile_buffer1.txt", tile0)
print("[系統]: 讀取tile_buffer2.txt")
read_tile("tile_buffer2.txt", tile1)
print("[系統]: 讀取tile_buffer3.txt")
read_tile("tile_buffer3.txt", tile2)

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
'''

# ==== weight ====
def read_weight(weight_path, weight):
    with open(weight_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        weight_str_a = f.read().split()

        #將bias的兩個字串合併以及跳過再存回
        weight_str_b = []
        for i in range(0, len(weight_str_a), 1):
            if(i == 1 or i == 2 or i == 3 or i == 7 or i == 11 or i== 15):
                continue
            elif(i == 0):
                weight_str_b.append(weight_str_a[0]+weight_str_a[1])
            else:
                weight_str_b.append(weight_str_a[i])

        # str 轉 int(16進制)
        weight_int = []
        weight_int = HexToDec(weight_str_b)
        
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

# ======== 進行 DW 計算 ========
def Calculation(stride = 2, show_detail = True, weight = [], tile0 = [], tile1 = [], tile2 = [], tile_w = 0):
    

    if(stride < 1 or stride > 2 or weight == [] or tile0 == [] or tile1 == [] or tile2 == [] or tile_w == 0):
        print("[錯誤]: 函式 DW_Calc 的參數輸入錯誤，這很有問題")
        return ["錯爛"]
    
    if(stride == 2):
        '''
        stride = 2 的padding 情況: 

        0 x x x x x x x x x x x x x x 0(沒算到)
        0 x x x x x x x x x x x x x x 0(沒算到)
        0 x x x x x x x x x x x x x x 0(沒算到)

        '''
        if(show_detail):
            print("[系統]: 以下為計算細節輸出，供檢查運算過程")
        conv331 = 0
        output = []
        for i in range(len(weight)):
            # 初始化暫存
            output_inn = []

            for j in range(0, tile_w-stride+2, stride):
                conv331 = weight[i][0]
                if(show_detail):
                    print("bias: ", conv331)
                # ======== padding左 ========
                if(j==0):#padding左
                    conv331 = weight[i][1]*0 + weight[i][4]*0 + weight[i][7]*0 + conv331
                    if(show_detail):
                        print(f"{conv331:>20} = {weight[i][1]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][4]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][7]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{conv331}(bias)")
                    
                    for k in range(1, 3, 1):
                        conv331 = weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1] + conv331
                        if(show_detail):
                            print(f"{conv331:>20} = {weight[i][k+1]:>15}(W{i}) * {tile0[i][j+k-1]:>15}(T1)  +  "
                                f"{weight[i][k+3+1]:>15}(W{i}) * {tile1[i][j+k-1]:>15}(T2)  +  "
                                f"{weight[i][k+6+1]:>15}(W{i}) * {tile2[i][j+k-1]:>15}(T3)  +  "
                                f"{conv331 - (weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1])}(prev)")

                # ======== 無padding ========        
                else:
                    for k in range(1, 4, 1):
                        conv331 = weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2] + conv331

                        if(show_detail):
                            if(k == 1):
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(bias)")
                            else:
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(prev)")
                output_inn.append(conv331)
            output.append(output_inn)

    
    elif(stride == 1):
        '''
        stride = 1 的padding 情況: 基本一樣

        0 x x x x x x x x x x x x x x 0
        0 x x x x x x x x x x x x x x 0
        0 x x x x x x x x x x x x x x 0

        '''
        if(show_detail):
            print("[系統]: 以下為計算細節輸出，供檢查運算過程")
        conv331 = 0
        output = []
        for i in range(len(weight)):
            # 初始化暫存
            output_inn = []

            for j in range(0, tile_w-stride+1, stride):
                conv331 = weight[i][0]
                if(show_detail):
                    print("bias: ", conv331)
                # ======== padding左 ========
                if(j==0):#padding左
                    conv331 = weight[i][1]*0 + weight[i][4]*0 + weight[i][7]*0 + conv331
                    if(show_detail):
                        print(f"{conv331:>20} = {weight[i][1]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][4]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][7]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{conv331}(bias)")
                    
                    for k in range(1, 3, 1):
                        conv331 = weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1] + conv331
                        if(show_detail):
                            print(f"{conv331:>20} = {weight[i][k+1]:>15}(W{i}) * {tile0[i][j+k-1]:>15}(T1)  +  "
                                f"{weight[i][k+3+1]:>15}(W{i}) * {tile1[i][j+k-1]:>15}(T2)  +  "
                                f"{weight[i][k+6+1]:>15}(W{i}) * {tile2[i][j+k-1]:>15}(T3)  +  "
                                f"{conv331 - (weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1])}(prev)")
                            

                # ======== padding右 ========
                elif(j == tile_w-stride):
                    for k in range(1, 3, 1):
                        conv331 = weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2] + conv331
                        if(show_detail):
                            if(k == 1):
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(bias)")
                            else:
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(prev)")
                    
                    conv331 = weight[i][3]*0 + weight[i][6]*0 + weight[i][9]*0 + conv331
                    if(show_detail):
                        print(f"{conv331:>20} = {weight[i][3]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][6]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{weight[i][9]:>15}(W{i}) * {0:>15}(padd)+  "
                            f"{conv331}(prev)")


                # ======== 無padding ========
                else:
                    for k in range(1, 4, 1):
                        conv331 = weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2] + conv331
                        if(show_detail):
                            if(k == 1):
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(bias)")
                            else:
                                print(f"{conv331:>20} = {weight[i][k]:>15}(W{i}) * {tile0[i][j+k-2]:>15}(T1)  +  "
                                    f"{weight[i][k+3]:>15}(W{i}) * {tile1[i][j+k-2]:>15}(T2)  +  "
                                    f"{weight[i][k+6]:>15}(W{i}) * {tile2[i][j+k-2]:>15}(T3)  +  "
                                    f"{conv331 - (weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2])}(prev)")
                output_inn.append(conv331)
            output.append(output_inn)


    else:
        print("[錯誤]: 防呆都有寫你還可以進到這裡來，你本人就是 Bug 吧......")
        return []

    return output


'''
output = DW_Calc(2, True)
print("\n[系統]: 以下為最終計算結果")
hex_output = DecToHeX(output)
print("output(int10) =", output)
print("output(int16) =", hex_output)


print("\n[系統]: 正在儲存計算結果至 output.txt")
with open('output.txt', 'w', encoding='utf-8') as f:
    for i in range(len(hex_output)):
        f.write(str(hex_output[i]) + " ")

print("\n[完成]: DW 運算完成")
'''

def DW(stride, show_detail):
    # ======== 讀取檔案 -- 確認通道數用 ========
    channel_amount = 0
    tile_w = 0
    print("====================")
    print("[系統]: 執行輸入文本檢查")
    channel_amount, tile_w = channel_check()

    # ======== 讀取檔案 -- 運算用 ========
    # ==== tile ====
    tile0 = []
    tile1 = []
    tile2 = []
    print("\n\n====================")
    print("[系統]: 讀取tile_buffer1.txt")
    read_tile("tile_buffer1.txt", tile0, channel_amount, tile_w)
    print("[系統]: 讀取tile_buffer2.txt")
    read_tile("tile_buffer2.txt", tile1, channel_amount, tile_w)
    print("[系統]: 讀取tile_buffer3.txt")
    read_tile("tile_buffer3.txt", tile2, channel_amount, tile_w)

    if(show_detail):
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
    
    # ==== weight ====
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

    if(show_detail):
        print("[系統]: 以下為各 weight_storage，供檢查\n")
        print(f"weight_storage0:\nbias: {weight[0][0]}, W0: {weight[0][1:]}\n")
        print(f"weight_storage1:\nbias: {weight[1][0]}, W0: {weight[1][1:]}\n")
        print(f"weight_storage2:\nbias: {weight[2][0]}, W0: {weight[2][1:]}\n")
        print(f"weight_storage3:\nbias: {weight[3][0]}, W0: {weight[3][1:]}")


    # ======== 進行 DW 計算 ========
    print("\n\n====================")
    output = Calculation(stride, show_detail, weight, tile0, tile1, tile2, tile_w)
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
    print("[系統]: 正在儲存計算結果至 output.txt")
    with open('output.txt', 'w', encoding='utf-8') as f:
        for i in range(len(hex_output)):
            for j in range(len(hex_output[i])):
                if(j == len(hex_output[i]) - 1):
                    f.write(str(hex_output[i][j]) + "\n")
                else:
                    f.write(str(hex_output[i][j]) + " ")

    print("\n[完成]: DW 運算完成")

if __name__ == "__main__":
    DW(stride = 1, show_detail = True)