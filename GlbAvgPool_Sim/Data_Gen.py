def generate_hex_text(rows, cols):
    """
    rows: 基數的數量 (例如 0, 1000, 2000...)
    cols: 每行遞增到的十進位數值 (1024)
    """
    output = []
    
    for r in range(rows):
        base = r * 0x1000  # 每一行的開頭是 0000, 1000, 2000, 3000...
        line_elements = []
        
        for i in range(cols):
            # 計算當前數值並格式化為 4 位 16 進位，不足補 0
            hex_val = f"{base + i:04x}"
            line_elements.append(hex_val)
        
        # 將該行元素用空格連結
        output.append(" ".join(line_elements))
    
    return "\n".join(output)

# 設定生成 4 行（如同你的範例），每行延伸到十進位 1024
result = generate_hex_text(rows=4, cols=1024)

# 將結果存入檔案，方便你查看或匯入硬體模擬工具
with open("tile_buffer4.txt", "w") as f:
    f.write(result)

print("文本已生成並儲存至 hex_output.txt")