import cv2
import numpy as np
import matplotlib.pyplot as plt

# 讀取圖片 (請將 'your_image.jpg' 替換成你的圖片路徑)
img_path = 'resized_opencv_128x128.png'
img = cv2.imread(img_path)

if img is None:
    print("無法讀取圖片，請檢查路徑是否正確。")
else:
    # 確保原始圖片大小為 384x384 (如果不是，先強制 resize 方便測試)
    if img.shape[:2] != (384, 384):
        print(f"原圖大小為 {img.shape[:2]}，強制轉換為 384x384")
        img = cv2.resize(img, (384, 384))

    # -------------------------------------------------------------
    # 方法一：使用 OpenCV 內建的 resize (預設為雙線性插值 INTER_LINEAR)
    # -------------------------------------------------------------
    resized_cv2 = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)

    # -------------------------------------------------------------
    # 方法二：暴力九宮格取值 (直接捨棄 8 個像素，每 3 個取 1 個)
    # -------------------------------------------------------------
    # 使用 Numpy 切片 [start:stop:step]，步長(step)設為 3
    # img[高度切片, 寬度切片, 通道] -> img[::3, ::3]
    resized_brute = img[0::3, 0::3]

    # --- 以下為將結果視覺化呈現的程式碼 ---
    
    # OpenCV 讀取圖片預設是 BGR 格式，轉換成 RGB 格式供 matplotlib 顯示
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_cv2_rgb = cv2.cvtColor(resized_cv2, cv2.COLOR_BGR2RGB)
    resized_brute_rgb = cv2.cvtColor(resized_brute, cv2.COLOR_BGR2RGB)

    # 使用 matplotlib 繪製對比圖
    plt.figure(figsize=(15, 6))

    plt.subplot(1, 3, 1)
    plt.title('Original (384x384)')
    plt.imshow(img_rgb)
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('OpenCV Bilinear (128x128)')
    plt.imshow(resized_cv2_rgb)
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Brute-force Subsample (128x128)')
    plt.imshow(resized_brute_rgb)
    plt.axis('off')

    plt.tight_layout()
    plt.show()


    # 如果你想把結果存成實體圖片檔，可以取消下方的註解：
    cv2.imwrite('result_cv2_bilinear.png', resized_cv2)
    cv2.imwrite('result_brute_force_LU.png', resized_brute)