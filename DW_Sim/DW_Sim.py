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


channel_amount = 0
tile_w = 0
print("[系統]: 執行輸入文本檢查")
channel_amount, tile_w = channel_check()


# ======== 讀取檔案 -- 運算用 ========
# ==== tile ====
def read_tile(tile_path, tile):
    with open(tile_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        tile_str = f.read().split()

        # str 轉 int(16進制)
        tile_int = []
        for i in tile_str:
            tile_int.append(int(i, 16))
        
        # 將 tile 的 channel 切開並存為 2 維 list
        for i in range(0, channel_amount, 1):
            tile.append(tile_int[i*tile_w+0:i*tile_w+tile_w])
        
tile0 = []
tile1 = []
tile2 = []
print("\n[系統]: 讀取tile_buffer1.txt")
read_tile("tile_buffer1.txt", tile0)
print("[系統]: 讀取tile_buffer2.txt")
read_tile("tile_buffer2.txt", tile1)
print("[系統]: 讀取tile_buffer3.txt")
read_tile("tile_buffer3.txt", tile2)

print("[系統]: 以下為各 tile_buffer 輸出，供檢查")
# 印出 tile0 確認
print("\ntile_buffer1:")
for i in range(0, channel_amount, 1):
    print(len(tile0[i]), tile0[i])
# 印出 tile1 確認
print("\ntile_buffer2:")
for i in range(0, channel_amount, 1):
    print(len(tile0[i]), tile0[i])
# 印出 tile2 確認
print("\ntile_buffer3:")
for i in range(0, channel_amount, 1):
    print(len(tile0[i]), tile0[i])


# ==== weight ====
def read_weight(weight_path, weight):
    with open(weight_path, "r", encoding = "utf-8") as f:
        # 讀取 txt 成 list
        weight_str = f.read().split()

        # str 轉 int(16進制)
        weight_int = []

        for i in range(0, len(weight_str), 1):
            if(i == 1 or i == 2 or i == 3 or i == 7 or i == 11 or i== 15):
                continue
            elif(i == 0):
                weight_int.append(int(weight_str[0]+weight_str[1], 16))
            else:
                weight_int.append(int(weight_str[i], 16))
        
        weight.append(weight_int)

weight = []
print("\n[系統]: 讀取weight_storage0.txt")
read_weight("weight_storage0.txt", weight)
print("[系統]: 讀取weight_storage1.txt")
read_weight("weight_storage1.txt", weight)
print("[系統]: 讀取weight_storage2.txt")
read_weight("weight_storage2.txt", weight)
print("[系統]: 讀取weight_storage3.txt")
read_weight("weight_storage3.txt", weight)

print("[系統]: 以下為各 weight_storage 輸出，供檢查\n")
print(f"weight_storage0:\nbias: {weight[0][0]}, W0: {weight[0][1:]}")
print(f"weight_storage1:\nbias: {weight[1][0]}, W0: {weight[1][1:]}")
print(f"weight_storage2:\nbias: {weight[2][0]}, W0: {weight[2][1:]}")
print(f"weight_storage3:\nbias: {weight[3][0]}, W0: {weight[3][1:]}")


# ======== 進行 DW 計算 ========
'''
stride = 2 的padding 情況：

0 x x x x x x x x x x x x x x 0
0 x x x x x x x x x x x x x x 0
0 x x x x x x x x x x x x x x 0

'''
print("\n[系統]: 以下為計算細節輸出，供檢查運算過程")

stride = 2
conv331 = 0
output = []
for i in range(len(weight)):
    for j in range(0, tile_w-stride+2, stride):
        conv331 = weight[i][0]
        print("bias: ", conv331)

        # ======== padding左 ========
        if(j==0):#padding左
            conv331 = weight[i][1]*0 + weight[i][4]*0 + weight[i][7]*0 + conv331
            print(f"{conv331:>8} = {weight[i][1]:>5}(W{i}) * {0:>5}(padd)+  "
                f"{weight[i][4]:>5}(W{i}) * {0:>5}(padd)+  "
                f"{weight[i][7]:>5}(W{i}) * {0:>5}(padd)+  "
                f"{conv331}(bias)")
            
            for k in range(1, 3, 1):
                conv331 = weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1] + conv331
                print(f"{conv331:>8} = {weight[i][k+1]:>5}(W{i}) * {tile0[i][j+k-1]:>5}(T1)  +  "
                    f"{weight[i][k+3+1]:>5}(W{i}) * {tile1[i][j+k-1]:>5}(T2)  +  "
                    f"{weight[i][k+6+1]:>5}(W{i}) * {tile2[i][j+k-1]:>5}(T3)  +  "
                    f"{conv331 - weight[i][k+1]*tile0[i][j+k-1] + weight[i][k+3+1]*tile1[i][j+k-1] + weight[i][k+6+1]*tile2[i][j+k-1]}(prev)")

        # ======== 無padding ========        
        else:
            for k in range(1, 4, 1):
                conv331 = weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2] + conv331

                if(k == 1):
                    print(f"{conv331:>8} = {weight[i][k]:>5}(W{i}) * {tile0[i][j+k-2]:>5}(T1)  +  "
                        f"{weight[i][k+3]:>5}(W{i}) * {tile1[i][j+k-2]:>5}(T2)  +  "
                        f"{weight[i][k+6]:>5}(W{i}) * {tile2[i][j+k-2]:>5}(T3)  +  "
                        f"{conv331 - weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2]}(bias)")
                else:
                    print(f"{conv331:>8} = {weight[i][k]:>5}(W{i}) * {tile0[i][j+k-2]:>5}(T1)  +  "
                        f"{weight[i][k+3]:>5}(W{i}) * {tile1[i][j+k-2]:>5}(T2)  +  "
                        f"{weight[i][k+6]:>5}(W{i}) * {tile2[i][j+k-2]:>5}(T3)  +  "
                        f"{conv331 - weight[i][k]*tile0[i][j+k-2] + weight[i][k+3]*tile1[i][j+k-2] + weight[i][k+6]*tile2[i][j+k-2]}(prev)")
        output.append(conv331)
print("\n[系統]: 以下為最終計算結果")
print("output =", output)


print("\n[系統]: 正在儲存計算結果至 output.txt")
with open('output.txt', 'w', encoding='utf-8') as f:
    for i in range(len(output)):
        f.write(str(output[i]) + " ")