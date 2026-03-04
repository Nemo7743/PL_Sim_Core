from PIL import Image

# 1. 讀取圖片
input_path = "0001.png"
img = Image.open(input_path)

# 2. 將圖片 resize 成 128x128
# Image.Resampling.LANCZOS 提供較高品質的縮放效果
resized_img = img.resize((384, 384), Image.Resampling.LANCZOS)

# 3. 儲存圖片
resized_img.save("resized_128x128.png")

print("圖片縮放完成！")



import cv2

# 1. 讀取圖片
img = cv2.imread('0001.png', cv2.IMREAD_UNCHANGED) # IMREAD_UNCHANGED 可保留 PNG 的透明層

# 2. 將圖片 resize 成 128x128
# 注意：OpenCV 的參數順序是 (寬, 高)
resized_img = cv2.resize(img, (384, 384), interpolation=cv2.INTER_AREA)

# 3. 儲存圖片
cv2.imwrite('resized_opencv_128x128.png', resized_img)

print("OpenCV 縮放完成！")




