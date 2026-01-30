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
        
        print(f"轉置完成！已儲存至 {output_file}")

    except FileNotFoundError:
        print(f"找不到檔案：{input_file}")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 執行轉置
transpose_txt('data_transposed.txt', 'data_transposed.txt')