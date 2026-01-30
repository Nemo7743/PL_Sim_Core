def generate_hex_block(start_hex_str, count, items_per_row=4):
    """
    生成指定格式的十六進位文本塊
    :param start_hex_str: 起始數字 (字串, 例如 "0000")
    :param count: 要生成的數字總數
    :param items_per_row: 每行顯示幾個數字
    :return: 格式化後的文本字串
    """
    start_int = int(start_hex_str, 16)
    lines = []
    
    # 以每行 items_per_row 的步長進行迭代
    for i in range(0, count, items_per_row):
        row_items = []
        for j in range(items_per_row):
            if i + j < count:
                current_val = start_int + i + j
                # :04x 表示格式化為4位數十六進位，不足補0，小寫字母
                row_items.append(f"{current_val:04x}")
        lines.append(" ".join(row_items))
        
    return "\n".join(lines)

# --- 設定參數 ---
total_numbers = 192  # 每個文本要生成的數字數量

for i in range(0, 172, 1):
    text1 = generate_hex_block(f"{i:>2}00", total_numbers)
'''
# 生成文本 1 (從 0000 開始)
text1 = generate_hex_block("0000", total_numbers)

# 生成文本 2 (從 1000 開始)
text2 = generate_hex_block("1000", total_numbers)

# 生成文本 3 (從 1000 開始)
text3 = generate_hex_block("2000", total_numbers)

# 生成文本 4 (從 1000 開始)
text4 = generate_hex_block("3000", total_numbers)
'''
# --- 輸出結果 ---
'''
print(text1)
with open('tile_buffer1.txt', 'w', encoding='utf-8') as f:
    f.write(text1)
    f.write("\n")
    f.write(text2)
    f.write("\n")
    f.write(text3)
    f.write("\n")
    f.write(text4)
    f.write("\n")
'''


print("文本1：")
print(text1)
with open('weight_storage0.txt', 'w', encoding='utf-8') as f:
    f.write("0000 000b 0000 0000\n")
    f.write(text1)
'''
print("文本2：")
print(text2)
with open('weight_storage1.txt', 'w', encoding='utf-8') as f:
    f.write("0000 100b 0000 0000\n")
    f.write(text2)
    
print("文本3：")
print(text3)
with open('weight_storage2.txt', 'w', encoding='utf-8') as f:
    f.write("0000 200b 0000 0000\n")
    f.write(text3)

print("文本4：")
print(text4)
with open('weight_storage3.txt', 'w', encoding='utf-8') as f:
    f.write("0000 00b 0000 0000\n")
    f.write(text4)
'''
# 如果你想將結果保存到檔案，可以取消下面這行的註解：
# with open("output.txt", "w") as f: f.write(f"文本1：\n{text1}\n\n文本2：\n{text2}")