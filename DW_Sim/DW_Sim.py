

# ======== 讀取檔案 -- 確認通道數用 ========
with open("tile0.txt", "r", encoding = "utf-8") as f:
    content = f.read()
    if content.endswith('\n'):
        channel_tile0_amount = content.count('\n')
    else:
        channel_tile0_amount = content.count('\n') + 1

with open("tile1.txt", "r", encoding = "utf-8") as f:
    content = f.read()
    if content.endswith('\n'):
        channel_tile1_amount = content.count('\n')
    else:
        channel_tile1_amount = content.count('\n') + 1

with open("tile2.txt", "r", encoding = "utf-8") as f:
    content = f.read()
    if content.endswith('\n'):
        channel_tile2_amount = content.count('\n')
    else:
        channel_tile2_amount = content.count('\n') + 1


if(channel_tile0_amount != channel_tile1_amount or channel_tile1_amount != channel_tile2_amount or channel_tile2_amount != channel_tile0_amount):
    print("[警告]: 三個輸入文本的通道數量不相同")
else:
    channel_amount = channel_tile0_amount
    tile_w = len(content.split())//channel_amount
    print(len(content.split()))



with open("weight.txt", "r", encoding = "utf-8") as f:
    content = f.read()
    if content.endswith('\n'):
        weight_amount = content.count('\n')
    else:
        weight_amount = content.count('\n') + 1

if(weight_amount != channel_amount):
    print("[警告]: 輸入文本的通道數量和權重數量不匹配！", "輸入通道數量:", channel_amount, " 權重數量(組):", weight_amount)



# ======== 讀取檔案 -- 運算用 ========
# ==== tile0 ====
with open("tile0.txt", "r", encoding = "utf-8") as f:
    # 讀取 txt 成 list
    tile0_str = f.read().split()

    # str 轉 int(16進制)
    tile0_int = []
    for i in tile0_str:
        tile0_int.append(int(i, 16))
    
    # 將 tile 的 channel 切開並存為 2 維 list
    tile0 = []
    #num_weight = len(tile0_int)//9
    for i in range(0, channel_amount, 1):
        tile0.append(tile0_int[i*tile_w+0:i*tile_w+tile_w])
    
    # 印出 tile 確認
    for i in range(0, channel_amount, 1):
        print(len(tile0[i]), tile0[i])


# ==== tile1 ====
with open("tile1.txt", "r", encoding = "utf-8") as f:
    # 讀取 txt 成 list
    tile1_str = f.read().split()

    # str 轉 int(16進制)
    tile1_int = []
    for i in tile1_str:
        tile1_int.append(int(i, 16))
    
    # 將 tile 的 channel 切開並存為 2 維 list
    tile1 = []
    #num_weight = len(tile0_int)//9
    for i in range(0, channel_amount, 1):
        tile1.append(tile1_int[i*tile_w+0:i*tile_w+tile_w])
    
    # 印出 tile 確認
    for i in range(0, channel_amount, 1):
        print(len(tile1[i]), tile1[i])


# ==== tile2 ====
with open("tile1.txt", "r", encoding = "utf-8") as f:
    # 讀取 txt 成 list
    tile2_str = f.read().split()

    # str 轉 int(16進制)
    tile2_int = []
    for i in tile2_str:
        tile2_int.append(int(i, 16))
    
    # 將 tile 的 channel 切開並存為 2 維 list
    tile2 = []
    #num_weight = len(tile0_int)//9
    for i in range(0, channel_amount, 1):
        tile2.append(tile2_int[i*tile_w+0:i*tile_w+tile_w])
    
    # 印出 tile 確認
    for i in range(0, channel_amount, 1):
        print(len(tile2[i]), tile2[i])


# ==== weight ====
with open("weight.txt", "r", encoding = "utf-8") as f:
    # 讀取 txt 成 list
    weight_str = f.read().split()

    # str 轉 int(16進制)
    weight_int = []
    for i in weight_str:
        weight_int.append(int(i, 16))

    # 將 filter 切開存為 2 維 list
    weight = []
    num_weight = len(weight_int)//9
    for i in range(0, num_weight, 1):
        weight.append(weight_int[i*9+0:i*9+9])

    # 印出 weight 確認
    for i in range(0, num_weight, 1):
        print(weight[i][0:3], weight[i][3:6], weight[i][6:9], sep="\n")
        print("\n")
    


#======== 進行 DW 計算 ========
stride = 2

output = []
for i in range(len(weight)):
    conv331 = 0
    print(conv331)
    for j in range(0, tile_w-stride, stride):
        for k in range(0, 3, 1):
            conv331 = weight[i][k]*tile0[i][j+k] + weight[i][k+3]*tile1[i][j+k] + weight[i][k+6]*tile2[i][j+k] + conv331
            print(f"{conv331:<8} = {weight[i][k]:<5} * {tile0[i][j+k]:<5}  +  "
                f"{weight[i][k+3]:<5} * {tile1[i][j+k]:<5}  +  "
                f"{weight[i][k+6]:<5} * {tile2[i][j+k]:<5}  +  prev conv331")
    output.append(conv331)
print(output)
