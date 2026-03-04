import os

import Unit0_Preprocessing.Image_Preprocessing
import Unit1_Conv1.Conv1
import Unit2_MaxPool.MaxPool
import Unit3_1_DownSamplingL.DownSamplingL as DownSamplingL
import Unit3_2_DownSamplingR.DownSamplingR as DownSamplingR
import Unit_ChannelShuffle.Channel_Shuffle as ChannelShuffle



# ==================== 圖片預處理 ====================
input_image_path = r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\input.jpg"
output_folder = r"C:\Users\legoa\NCU\專題\專題內容\硬體模擬\PL_Sim_Core\Inferance\Unit0_Preprocessing\Fmap_to_Conv1"

if os.path.exists(input_image_path):
    Unit0_Preprocessing.Image_Preprocessing.image_preprocessing(input_image_path, output_folder)
else:
    print(f"找不到檔案: {input_image_path}，請確認路徑。")


# ==================== Conv1 ====================
Unit1_Conv1.Conv1.Conv1_implementation()


# ==================== MaxPool ====================
Unit2_MaxPool.MaxPool.MaxPool_implementation()


# ==================== DownSampling 0 ====================
DownSamplingL.DownSamplingL_implementation(0)
DownSamplingR.DownSamplingR_implementation(0)
# ==================== Shuffle ====================
ChannelShuffle.ChannelShuffle(0, False)

# ====================