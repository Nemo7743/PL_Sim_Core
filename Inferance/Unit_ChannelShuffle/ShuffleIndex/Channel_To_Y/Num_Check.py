def is_number(s):
    """檢查字串是否可以轉換為數字（支援整數、負數與小數）"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def count_comma_separated_numbers(file_path):
    """計算文字檔中，以逗號隔開的數字數量"""
    try:
        # 開啟並讀取檔案 (使用 utf-8 編碼以防有中文或其他字元)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 根據逗號分割文字內容
        items = content.split(',')
        
        number_count = 0
        
        for item in items:
            # strip() 會自動移除字串前後的空白與換行符號 (\n, \t, 空格等)
            cleaned_item = item.strip()
            
            # 如果清理過後的字串是數字，則計數加 1
            if is_number(cleaned_item):
                number_count += 1
                
        return number_count
        
    except FileNotFoundError:
        return "錯誤：找不到指定的檔案，請檢查路徑是否正確。"
    except Exception as e:
        return f"發生未知的錯誤：{e}"

# ========== 測試區塊 ==========
if __name__ == "__main__":
    # 假設你的檔案名稱叫做 data.txt
    file_path = 'Channel_To_Y_All.txt'
    
    # 你可以先在程式碼同目錄下建立一個 data.txt 來測試
    # 例如裡面寫入: 123, 45.6, text, -78, 
    # , 99,   100  
    
    result = count_comma_separated_numbers(file_path)
    print(f"檔案中以逗號隔開的數字總共有：{result} 個")