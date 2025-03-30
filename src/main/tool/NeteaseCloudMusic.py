import os
import subprocess
from ncmdump import dump
from pydub import AudioSegment

# 源目录和目标目录
source_dir = "D:\CloudMusic\VipSongsDownload"  # 放置 .ncm 文件的目录
decoded_dir = "E:\Decoded_Files"  # 存放解密后的文件
mp3_dir = "E:\VipSongsDownload"  # 最终 MP3 存放目录

# 确保目标目录存在
os.makedirs(decoded_dir, exist_ok=True)
os.makedirs(mp3_dir, exist_ok=True)

# 遍历目录下所有 NCM 文件
for filename in os.listdir(source_dir):
    if filename.endswith(".ncm"):
        ncm_path = os.path.join(source_dir, filename)
        decoded_path = os.path.join(decoded_dir, filename.replace(".ncm", ".flac"))  # 解密后默认是 FLAC 或 MP3
        mp3_path = os.path.join(mp3_dir, filename.replace(".ncm", ".mp3"))

        try:
            # 解密 NCM 文件
            dump(ncm_path, decoded_path)
            print(f"解密成功: {ncm_path} -> {decoded_path}")

            # 转换为 MP3
            audio = AudioSegment.from_file(decoded_path, format="flac")  # 如果是 MP3，可改为 format="mp3"
            audio.export(mp3_path, format="mp3", bitrate="192k")
            print(f"转换成功: {decoded_path} -> {mp3_path}")

            # 可选：删除解密后的文件
            os.remove(decoded_path)

        except Exception as e:
            print(f"处理失败: {ncm_path}, 错误: {e}")

print("所有文件已解密并转换为 MP3！")
