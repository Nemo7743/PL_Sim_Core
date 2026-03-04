from PIL import Image

def image_to_rgb_txt(image_path, output_path):
    try:
        # 開啟圖片並確保轉換為 RGB 模式
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # 寫入標頭資訊
            f.write(f"# Image Size: {width}x{height}\n")
            f.write("# Format: (R, G, B) per line\n")
            
            # 遍歷每一個像素
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    # 每一組 RGB 寫入後直接換行
                    f.write(f"({r}, {g}, {b})\n")
                
        print(f"成功！RGB 資料已儲存至: {output_path} (共 {width * height} 行)")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

# 使用範例
image_to_rgb_txt('result_cv2_bilinear.png', 'result_cv2_bilinear_RGB.txt')
image_to_rgb_txt('result_brute_force.png', 'result_brute_force_RGB.txt')
image_to_rgb_txt('result_brute_force_LU.png', 'result_brute_force_LU_RGB.txt')

image_to_rgb_txt('result_torchvision.png', 'result_torchvision_RGB.txt')