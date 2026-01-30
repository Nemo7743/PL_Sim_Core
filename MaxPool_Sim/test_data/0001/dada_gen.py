def generate_maxpool_data():
    rows = 64
    cols = 4
    
    # 1. 生成 Input Tile Buffers
    # 模式：Row i -> [i, 0x1000+i, 0x2000+i, 0x3000+i]
    buffer_data = []
    for r in range(rows):
        row_vals = []
        for c in range(cols):
            base = c * 0x1000
            val = base + r
            row_vals.append(f"{val:04X}")
        buffer_data.append(row_vals)
    
    # 寫入檔案 (三個檔案內容相同)
    for i in range(1, 4):
        with open(f"tile_buffer{i}.txt", "w") as f:
            for row in buffer_data:
                f.write(" ".join(row) + "\n")
        print(f"[生成] tile_buffer{i}.txt 完成")

    # 2. 生成預期輸出 output.txt
    # 根據單調遞增特性，Max Pooling 結果就是 Window 的最右側值 (index j+1)
    output_rows = []
    for j in range(0, rows, 2): # j = 0, 2, ..., 62
        row_out = []
        # Max index is j+1 for all cases (including j=0 where window is [Pad, 0, 1])
        max_idx = j + 1
        
        for c in range(cols):
            base = c * 0x1000
            val = base + max_idx
            row_out.append(f"{val:04X}")
        output_rows.append(row_out)

    # 寫入 Output
    with open("output.txt", "w") as f:
        for row in output_rows:
            f.write(" ".join(row) + "\n")
    print("[生成] output.txt (預期結果) 完成")

if __name__ == "__main__":
    generate_maxpool_data()