from pathlib import Path


# ========== 小工具 ==========
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
#transpose_txt('tile_buffer3.txt', 'tile_buffer3.txt')

# 轉置工具 -- 但是不讀檔案
def transpose_list(input_matrix, show_detail = False):
    """
    將輸入的二維 list 進行轉置 (行列互換)。
    
    Args:
        input_matrix (list): 原始的二維列表 (e.g., [[1, 2], [3, 4]])
        show_detail (bool): 是否顯示除錯/系統訊息
        
    Returns:
        list: 轉置後的二維列表，若出錯或為空則回傳空 list
    """
    try:
        # 1. 檢查資料有效性
        if not input_matrix:
            if show_detail:
                print("輸入的 List 是空的。")
            return []
            
        # 額外檢查：確保輸入確實是 list 類型
        if not isinstance(input_matrix, list):
            if show_detail: 
                print("錯誤：輸入資料必須是 List。")
            return []

        # 2. 轉置資料
        # zip(*matrix) 會將原本的 Row 拆開並重新組合成 Column (Tuple 形式)
        # 這裡使用 list() 將其轉回列表形式，保持結構一致為 list of lists
        transposed_matrix = [list(row) for row in zip(*input_matrix)]

        # 3. 輸出訊息
        if show_detail:
            # 取得原始維度與新維度供參考
            rows = len(input_matrix)
            cols = len(input_matrix[0]) if rows > 0 else 0
            new_rows = len(transposed_matrix)
            new_cols = len(transposed_matrix[0]) if new_rows > 0 else 0
            
            print(f"[系統]: 資料轉置完成！")
            print(f"       原始維度: {rows}x{cols} -> 新維度: {new_rows}x{new_cols}")

        return transposed_matrix

    except TypeError as e:
        print(f"類型錯誤 (可能是輸入了非矩陣格式的 List)：{e}")
        return []
    except Exception as e:
        print(f"發生錯誤：{e}")
        return []
    
# 把檔案讀取成二維陣列，方便轉換
def file_to_list(file_path, show_detail=False):
    """
    讀取文字檔並轉換為二維列表 (List of Lists)。
    以換行區分 Row，以空白區分 Column。

    Args:
        file_path (str): 檔案路徑
        show_detail (bool): 是否顯示讀取資訊

    Returns:
        list: 讀取後的二維列表，若檔案不存在或出錯回傳空 list
    """
    matrix = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 1. strip() 會移除字串頭尾的空白與換行符號 (\n)
                # 2. 如果 strip() 後是空字串 (例如文件尾端的空行)，則跳過不處理
                if line.strip():
                    # 預設 split() 會以任何空白字元 (空格、Tab) 切割
                    matrix.append(line.strip().split())

        if show_detail:
            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0
            print(f"[系統]: 檔案讀取成功！路徑: {file_path}")
            print(f"       讀入維度: {rows} 列 x  {cols} 行")

        return matrix

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {file_path}")
        return []
    except Exception as e:
        print(f"讀取檔案發生錯誤：{e}")
        return []
    
'''
tile_buffer0 = file_to_list("./data/tile_buffer1.txt", True)
print("tets matrix:\n", tile_buffer0)
tile_buffer0 = transpose_list(tile_buffer0, True)
print("\n")
print("tets matrix:\n", tile_buffer0)
'''

# 將二維運算結果寫入檔案
def list_to_file(array_2d, filename, show_detail=False):
    """
    將二維陣列儲存為 txt 檔案。
    格式：元素間以空格隔開，列與列之間換行。
    
    參數:
    array_2d (list): 二維陣列 (List of Lists)
    filename (str): 檔案名稱 (包含路徑與副檔名，如 'output.txt')
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for row in array_2d:
                # 1. map(str, row): 將列中的每個元素 (如數字) 強制轉為字串
                # 2. ' '.join(...): 將這些字串用空格連接起來
                # 3. f.write(...\n): 寫入檔案並加上換行符號
                f.write(' '.join(map(str, row)) + '\n')
        if(show_detail):
            print(f"成功將二維陣列儲存至: {filename}")
    except IOError as e:
        print(f"檔案寫入錯誤: {e}")

# ======== Hex to Dec ======== (Q8.8) (2D list)
def HexToDec(hex_input):
    scale_factor = 256.0
    dec_output = []
    
    # [新增] 外層迴圈：遍歷每一列 (Row)
    for row in hex_input:
        current_row_dec = []  # 暫存當前這一列的結果

        # [原本的迴圈] 現在改為遍歷 row 中的每個 hex_str
        for hex_str in row:
            # 轉成 Raw Integer (0 ~ 65535)
            raw_val = int(hex_str, 16)

            # 處理 Sign Bit (二補數轉換)
            # 如果第 15 bit 是 1 (即 >= 0x8000)，代表是負數
            if raw_val & 0x8000:
                signed_val = raw_val - 0x10000
            else:
                signed_val = raw_val
            
            # 轉成浮點數
            # [修改] 將結果加入當前的列 list
            current_row_dec.append(signed_val / scale_factor)
        
        # [新增] 將處理完的一整列加入最終輸出
        dec_output.append(current_row_dec)
        
    return dec_output

# ======== Hex to Dec ======== (Q16.16) (1D list)
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

# ======== Dec to Hec ======== (Q8.8) (3D List)
def DecToHex_3D(dec_input_3d):
    hex_output_3d = []  # 最外層的 3D List
    scale_factor = 256.0
    
    # Q8.8 (Signed 16-bit) 的整數範圍限制
    MAX_VAL = 32767   # 0x7FFF
    MIN_VAL = -32768  # 0x8000

    # Layer 1: 遍歷每個 2D Matrix
    for matrix in dec_input_3d:
        matrix_output = []
        
        # Layer 2: 遍歷每一行 (Row)
        for row in matrix:
            row_output = []
            
            # Layer 3: 遍歷每個數值 (原本的邏輯)
            for val in row:
                # 轉換為固定點數整數 (乘上 2^8 並四捨五入)
                int_val = int(round(val * scale_factor))

                # 飽和截斷
                # 若超過表示範圍，強制鎖定在最大或最小值
                if int_val > MAX_VAL:
                    int_val = MAX_VAL
                elif int_val < MIN_VAL:
                    int_val = MIN_VAL

                # 轉回 Hex 字串 (處理負數顯示 & 0xFFFF)
                row_output.append(f"{int_val & 0xFFFF:04X}")
            
            # 將處理完的一行加入 Matrix
            matrix_output.append(row_output)
        
        # 將處理完的 Matrix 加入 3D List
        hex_output_3d.append(matrix_output)

    return hex_output_3d



# ========= 讀取Fmap ==========
def Load_All_Fmap(f_src_root, fmap_num):

    fmap = []
    '''
    fmap 資料結構 = 
    [
    [fmap zzz (二維)]
    [fmap 000 (二維)]
    [fmap 001 (二維)]
    ...
    [fmap 126 (二維)]
    [fmap 127 (二維)]
    ]
    '''

    buffer_2D_lst = []

    # ========== 讀取檔案並轉置 ==========
    # 雖然是可以用一行就解決掉，但我覺得這樣可讀性就差了點
    '''
    1. 讀取檔案成為二維陣列
    2. 將二維陣列轉置
    3. 將字串以 16 進位的 Q8.8 轉換為 10 進位數字
    4. 附加在 fmap 這個三維陣列上
    '''

    # padding
    buffer_2D_lst = file_to_list(f_src_root / "row_ZZZ.txt")
    buffer_2D_lst = transpose_list(buffer_2D_lst)
    buffer_2D_lst = HexToDec(buffer_2D_lst)
    fmap.append(buffer_2D_lst)


    # 讀取普通 Fmap
    for i in range(0, fmap_num, 1):
        buffer_2D_lst = file_to_list(f_src_root / f"row_{i:03d}.txt")
        buffer_2D_lst = transpose_list(buffer_2D_lst)
        buffer_2D_lst = HexToDec(buffer_2D_lst)
        fmap.append(buffer_2D_lst)
    return fmap


def ChannelShuffle(features = -1, show_detail = False):
    '''
    Docstring for ChannelShuffle
    
    :param features: 表示這層 ChannelShuffle 是在 Shuffle 哪一個 FeatureMap
    '''
    # ========== 參數檢查並設定常數( "總" Fmap 數量 ) ==========
    if(features == -1):
        print("[錯誤]: features 參數不能是 -1 或留白，只能是: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]")
    elif(features not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]):
        print("[錯誤]: features 只能是: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]，目前的 features =", features)
    elif(features in [0, 1, 2, 3]):
        fmap_num = 16
    elif(features in [4, 5, 6, 7, 8, 9, 10, 11]):
        fmap_num = 8
    elif(features in [12, 13, 14, 15]):
        fmap_num = 4

    # ========== 狀態分類 ========== 降採樣 / 普通計算
    if(features in [0, 4, 12]):
        is_down_sampling = True
    else:
        is_down_sampling = False


    # ========== 讀取 Fmap ( 左分支 ) ==========
    if(is_down_sampling):
        fmapL_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance") / f"Unit{features+3}_1_DownSamplingL" / Path(r"Fmap_to_ChannelShuffle")
    else:
        fmapL_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit_ChannelShuffle\Fmap_to_Next_CalculateL")

    fmapL = Load_All_Fmap(fmapL_src_root, fmap_num)
    if(show_detail): print("fmaps of fmapL ( including padding ) =", len(fmapL))

    

    # ========== 讀取 Fmap ( 右分支 ) ==========
    if(is_down_sampling):
        fmapR_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance") / f"Unit{features+3}_2_DownSamplingR" / Path(r"Fmap_to_ChannelShuffle")
    else:
        fmapR_src_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance") / f"Unit{features+3}_2_OG_Calculate" / Path(r"Fmap_to_ChannelShuffle")

    fmapR = Load_All_Fmap(fmapR_src_root, fmap_num)
    if(show_detail): print("fmaps of fmapR ( including padding ) =", len(fmapR))


    # ========== 執行 Channel Concat ==========
    concated_fmap = []
    '''
    concated_fmap 資料結構 = 
    [
    [fmap 000 (二維)]
    [fmap 001 (二維)]
    ...
    [fmap ???-1 (二維)]
    [fmap ??? (二維)]
    ]
    '''

    # 進行 Concat
    for i in range(0, fmap_num):
        buffer_2d_lst = []

        for j in range(len(fmapL[i+1])):
            buffer_2d_lst.append(fmapL[i+1][j])
        
        for j in range(len(fmapR[i+1])):
            buffer_2d_lst.append(fmapR[i+1][j])
        
        concated_fmap.append(buffer_2d_lst)

    if(show_detail): print("Total fmap num after concat =", len(concated_fmap))
    if(show_detail): print("Total channel num after concat =", len(concated_fmap[1]))



    # ========== 執行 Channel Shuffle ==========
    shuffled_fmap = []
    '''
    shuffled_fmap 資料結構 = 
    [
    [fmap zzz (二維)]
    [fmap 000 (二維)]
    [fmap 001 (二維)]
    ...
    [fmap ???-1 (二維)]
    [fmap ??? (二維)]
    ]
    '''

    for i in range(fmap_num):
        buffer_2d_lst = []

        if(show_detail): print(f"\nshuffling fmap num: {i}")
        for j in range(len(concated_fmap[i])//2):
            buffer_2d_lst.append(concated_fmap[i][j])
            buffer_2d_lst.append(concated_fmap[i][ len(concated_fmap[i])//2 + j ])

            if(show_detail): 
                print(f"channel index: {j}")
                print(f"channel index: {len(concated_fmap[i])//2 + j}")

        shuffled_fmap.append(buffer_2d_lst)
    
    if(show_detail): 
        print("Total fmap num after shuffle =", len(shuffled_fmap))
        print("Total channel num after shuffle =", len(shuffled_fmap[0]))


    # ========== 執行 Channel Split ==========
    # 偷算參數
    total_channels = len(shuffled_fmap[0])

    # 初始化
    fmapL = []
    fmapR = []

    # 進行 Channel Split
    for i in range(fmap_num):
        buffer_2d_lst_L = []
        buffer_2d_lst_R = []

        for j in range(total_channels//2):
            buffer_2d_lst_L.append(shuffled_fmap[i][j])
            buffer_2d_lst_R.append(shuffled_fmap[i][j + total_channels//2])
        
        fmapL.append(buffer_2d_lst_L)
        fmapR.append(buffer_2d_lst_R)

    # 進行轉置
    for i in range(len(fmapL)):
        fmapL[i] = transpose_list(fmapL[i], False)
        fmapR[i] = transpose_list(fmapR[i], False)
    
    # 傳換成字串( 表示16進制數字 ) 
    fmapL = DecToHex_3D(fmapL)
    fmapR = DecToHex_3D(fmapR)

    # 進行 Padding: 加入 Padding Tile
    p_tile = []
    for i in range(len(fmapL[0])):
        inn_p_tile = []
        for j in range(len(fmapL[0][i])):
            inn_p_tile.append("0000")
        p_tile.append(inn_p_tile)
    # 加入三維陣列
    fmapL.insert(0, p_tile)
    fmapR.insert(0, p_tile)

    # ========== 儲存左右分支 ==========
    L_dst_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit_ChannelShuffle\Fmap_to_Next_CalculateL")
    R_dst_root = Path(r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit_ChannelShuffle\Fmap_to_Next_CalculateR")

    if(show_detail):
        for i in range(len(fmapL)):
            if(i == 0):
                list_to_file(fmapL[i], L_dst_root / f"row_ZZZ.txt")
                list_to_file(fmapR[i], R_dst_root / f"row_ZZZ.txt")
            else:
                list_to_file(fmapL[i], L_dst_root / f"row_{((i-1)):03d}.txt")
                list_to_file(fmapR[i], R_dst_root / f"row_{((i-1)):03d}.txt")

    
    return fmapL, fmapR

if __name__ == "__main__":
    ChannelShuffle(0, False)