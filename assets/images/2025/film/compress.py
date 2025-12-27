import os
from PIL import Image

# =================CONFIG=================
# 目标文件夹
source_dir = "assets/images/2025/film"
# 排除的文件夹 (缩略图文件夹)
exclude_dir = "thumbs"

# 【关键修改】压缩参数
# 1. 压缩质量设为 70 (即保留 70% 的质量)
JPEG_QUALITY = 70 

# 2. 长边最大像素限制 (建议保留此设置，防止几千万像素的原图撑爆)
# 如果你想完全保留原分辨率，把这个数字改得巨大，比如 10000
MAX_LONG_SIDE = 2500 
# ========================================

def compress_image(file_path):
    try:
        with Image.open(file_path) as img:
            # 强制转换为 RGB (防止 PNG/RGBA 报错)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            width, height = img.size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

            # 如果图片已经很小(小于1MB)且尺寸不大，就不折腾了，避免重复压缩变糊
            if max(width, height) <= MAX_LONG_SIDE and file_size_mb < 1.0:
                print(f"[Skipping] {os.path.basename(file_path)} (Small enough)")
                return

            # 计算新的尺寸
            new_width, new_height = width, height
            if max(width, height) > MAX_LONG_SIDE:
                ratio = MAX_LONG_SIDE / max(width, height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"[Resizing] {os.path.basename(file_path)}: {width}x{height} -> {new_width}x{new_height}")
            
            print(f"[Compressing] {os.path.basename(file_path)} to Quality {JPEG_QUALITY}...")

            # 核心：save 时指定 quality=70
            img.save(file_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# 主程序
print(f"Start optimizing images to Quality {JPEG_QUALITY}...")
total_saved = 0

for root, dirs, files in os.walk(source_dir):
    if exclude_dir in dirs:
        dirs.remove(exclude_dir)
        
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            full_path = os.path.join(root, file)
            old_size = os.path.getsize(full_path)
            
            compress_image(full_path)
            
            new_size = os.path.getsize(full_path)
            total_saved += (old_size - new_size)

print(f"\nDone! Total space saved: {total_saved / (1024*1024):.2f} MB")