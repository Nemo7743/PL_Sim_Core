def generate_gap_test_data():
    num_channels = 1024
    num_rows = 4
    
    # 每個 Tile 的基礎偏移量 (Q8.8)
    # Tile 1: +0.0, Tile 2: +1.0, Tile 3: +2.0, Tile 4: +3.0
    tile_offsets = [0, 0x0100, 0x0200, 0x0300]
    
    # 每個 Row 的基礎值 (Q8.8)
    row_bases = [0x0000, 0x1000, 0x2000, 0x3000]

    for t_idx in range(4):
        filename = f"tile_buffer{t_idx+1}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for r in range(num_rows):
                line_vals = []
                for c in range(num_channels):
                    # 數值 = RowBase + ChannelIndex + TileOffset
                    val = row_bases[r] + c + tile_offsets[t_idx]
                    line_vals.append(f"{val:04x}")
                f.write(" ".join(line_vals) + "\n")
        print(f"[生成] {filename} 完成")

    # 生成預期輸出 output.txt
    # 預期結果: Channel Index + 0x1980
    with open("output.txt", "w", encoding="utf-8") as f:
        output_vals = []
        for c in range(num_channels):
            mean_val = c + 0x1980
            output_vals.append(f"{mean_val:04x}")
        f.write(" ".join(output_vals))
    print("[生成] output.txt (預期結果) 完成")

if __name__ == "__main__":
    generate_gap_test_data()