def ChannelShuffle_Index_Calculate(idx_lst = None, features = -1, show_detail = False):
    '''
    Docstring for ChannelShuffle
    
    :param idx_lst: 想要被 shuffle 的 index list
    :param features: 表示這層 ChannelShuffle 是在 Shuffle 哪一個 FeatureMap
    :param show_detail: 是否顯示細節
    '''
    if(show_detail): print("Feature map now =", features)

    # ========== 參數檢查並設定常數( "總" tile ( 就是這裡的 "fmap" ) 數量 ) ==========
    if(features == -1):
        print("[錯誤]: features 參數不能是 -1 或留白，只能是: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]")
    elif(features not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]):
        print("[錯誤]: features 只能是: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]，目前的 features =", features)
    elif(features in [0, 1, 2, 3]):
        fmap_num = 16
        channel_num = 48
    elif(features in [4, 5, 6, 7, 8, 9, 10, 11]):
        fmap_num = 8
        channel_num = 96
    elif(features in [12, 13, 14, 15]):
        fmap_num = 4
        channel_num = 192

    # ========== 狀態分類 ========== 降採樣 / 普通計算
    if(features in [0, 4, 12]):
        is_down_sampling = True
    else:
        is_down_sampling = False

    
    # ========== 輸出 Shuffle 前的 index ==========
    if(show_detail):
        print("Before shuffle")
        print("Left : ", idx_lst[0:channel_num//2])
        print("Right: ", idx_lst[channel_num//2:])

    # ========== 執行 Channel Shuffle ==========
    shuffled_idx_lst = []

    for j in range(channel_num//2):
        shuffled_idx_lst.append(idx_lst[j])
        shuffled_idx_lst.append(idx_lst[channel_num//2 + j])

    # ========== 輸出 Shuffle 後的 index ==========
    if(show_detail):
        print("After shuffle")
        print("Left : ", shuffled_idx_lst[0:channel_num//2])
        print("Right: ", shuffled_idx_lst[channel_num//2:])
        print("\n\n")

    return shuffled_idx_lst
    


if __name__ == "__main__":
    
    for i in range(15):
        # ========== 參數設定 ==========
        # 表示現在要算哪一個 fmap
        features = i

        # ========== 狀態分類 ========== 降採樣 / 普通計算
        if(features in [0, 4, 12]):
            is_down_sampling = True
        else:
            is_down_sampling = False
        
        if(features in [0, 1, 2, 3]):
            fmap_num = 16
            channel_num = 48
        elif(features in [4, 5, 6, 7, 8, 9, 10, 11]):
            fmap_num = 8
            channel_num = 96
        elif(features in [12, 13, 14, 15]):
            fmap_num = 4
            channel_num = 192

        # ========== 建立 index list ==========
        if(is_down_sampling):
            idx_lst = []
            for i in range(channel_num):
                idx_lst.append(i)

        # ========== 進行計算 ==========
        idx_lst = ChannelShuffle_Index_Calculate(idx_lst, features, True)