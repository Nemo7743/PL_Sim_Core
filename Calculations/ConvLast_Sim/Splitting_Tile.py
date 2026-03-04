def Splitting_Tile(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
            # 讀取每一行，去除前後空白，並依據空格切割成 list
            # 使用 if line.strip() 是為了避免讀取到空行
            matrix = [line.strip().split() for line in f if line.strip()]
    
    '''
    for i in range(len(matrix)):
          print(matrix[i])
    '''
    out_matrix = []

    for i in range(0, len(matrix[0]), 4):
        out_matrix.append(matrix[0][0+i : 4+i])
        out_matrix.append(matrix[1][0+i : 4+i])
        out_matrix.append(matrix[2][0+i : 4+i])
        out_matrix.append(matrix[3][0+i : 4+i])
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
            for row in out_matrix:
                f.write(" ".join(row) + "\n")


if __name__ == "__main__":
    input_file_path = r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\ConvLast_Sim\data\tile_buffer1.txt"
    output_file_path = r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Calculations\ConvLast_Sim\data\tile_buffer1_splitted.txt"

    Splitting_Tile(input_file_path, output_file_path)