import os

# 设定你的图片路径
img_dir = "assets/images/2025/film"
# 你的GitHub Pages URL前缀 (根据之前的配置)
base_url = "/assets/images/2025/film/"

# 获取所有 jpg/jpeg 文件并排序
files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg'))])

print("gallery_film:")
for f in files:
    print(f"  - url: {base_url}{f}")
    print(f"    image_path: {base_url}{f}")
    print(f"    alt: \"{f}\"")
