import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image

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

    # OpenCV 讀取圖片預設是 BGR 格式，我們先在此統一轉換成 RGB 格式
    # 這樣後續給 Matplotlib 和 torchvision 使用時顏色才會正確
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # -------------------------------------------------------------
    # 方法一：使用 OpenCV 內建的 resize (預設為雙線性插值 INTER_LINEAR)
    # -------------------------------------------------------------
    resized_cv2 = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)
    resized_cv2_rgb = cv2.cvtColor(resized_cv2, cv2.COLOR_BGR2RGB)

    # -------------------------------------------------------------
    # 方法二：九宮格取樣左上角 (直接捨棄 8 個像素，每 3 個取 1 個)
    # -------------------------------------------------------------
    # 從 0 開始切片，明確表示取左上角
    resized_brute = img[1::3, 1::3]
    resized_brute_rgb = cv2.cvtColor(resized_brute, cv2.COLOR_BGR2RGB)

    # -------------------------------------------------------------
    # 方法三：使用 torchvision 的 Resize
    # -------------------------------------------------------------
    # 1. 將 NumPy Array (RGB) 轉換為 PIL Image
    pil_img = Image.fromarray(img_rgb)
    
    # 2. 定義 torchvision 的轉換 (預設也是雙線性插值 Bilinear)
    # 也可以透過 interpolation=transforms.InterpolationMode.NEAREST 等更改插值法
    # tv_resize_transform = transforms.Resize((128, 128))
    tv_resize_transform = transforms.Resize(
    (128, 128), 
    interpolation=transforms.InterpolationMode.BILINEAR, 
    antialias=False  # 關鍵：關閉抗鋸齒以貼近 OpenCV 行為
    )
    
    # 3. 執行轉換
    resized_tv_pil = tv_resize_transform(pil_img)
    
    # 4. 將結果轉回 NumPy Array 供 Matplotlib 繪圖
    resized_tv_rgb = np.array(resized_tv_pil)

    # --- 以下為將結果視覺化呈現的程式碼 ---
    
    # 使用 matplotlib 繪製對比圖 (調整為 1x4 的排列)
    plt.figure(figsize=(20, 5))

    plt.subplot(1, 4, 1)
    plt.title('Original (384x384)')
    plt.imshow(img_rgb)
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.title('OpenCV Bilinear (128x128)')
    plt.imshow(resized_cv2_rgb)
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.title('Subsample Top-Left (128x128)')
    plt.imshow(resized_brute_rgb)
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.title('Torchvision Resize (128x128)')
    plt.imshow(resized_tv_rgb)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # 如果你想把結果存成實體圖片檔，可以取消下方的註解：
    cv2.imwrite('result_cv2_bilinear.png', resized_cv2)
    cv2.imwrite('result_brute_force.png', resized_brute)
    
    # 注意：若要用 cv2.imwrite 存 torchvision 的結果，要先從 RGB 轉回 BGR
    resized_tv_bgr = cv2.cvtColor(resized_tv_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite('result_torchvision.png', resized_tv_bgr)