import os
from PIL import Image

# =================CONFIG=================
# 1. 图片所在的源文件夹路径 (请根据实际情况修改!)
source_dir = "assets/images/2025/film"

# 2. 缩略图存放的文件夹名称 (必须在源文件夹内)
thumb_dir_name = "thumbs"

# 3. 网站上的基础 URL 前缀
base_url_prefix = "/assets/images/2025/film/"

# 4. 缩略图的最大边长 (像素)
# 600px 对于网页画廊来说是一个很好的平衡点，既清晰又不会太大
MAX_DIMENSION = 1500
# ========================================

thumbs_output_dir = os.path.join(source_dir, thumb_dir_name)

# 确保缩略图文件夹存在
if not os.path.exists(thumbs_output_dir):
    os.makedirs(thumbs_output_dir)
    print(f"Created thumbnail directory: {thumbs_output_dir}")

# 获取所有 JPG 文件
files = sorted([f for f in os.listdir(source_dir) 
                if f.lower().endswith(('.jpg', '.jpeg')) 
                and os.path.isfile(os.path.join(source_dir, f))])

yaml_output = []

print(f"Processing {len(files)} images...")

for f in files:
    original_path = os.path.join(source_dir, f)
    thumb_path = os.path.join(thumbs_output_dir, f)
    
    # --- 1. 生成缩略图 ---
    with Image.open(original_path) as img:
        # 计算新尺寸，保持比例，最长边不超过 MAX_DIMENSION
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
        # 保存缩略图，质量设为 85% 足够网页使用
        img.save(thumb_path, "JPEG", quality=85)
        print(f"Generated thumbnail for: {f}")

    # --- 2. 生成 YAML 代码格式 ---
    # url 指向原始大图
    full_img_url = f"{base_url_prefix}{f}"
    # image_path 指向刚才生成的缩略图
    thumb_img_url = f"{base_url_prefix}{thumb_dir_name}/{f}"
    
    yaml_block = f"""  - url: {full_img_url}
    image_path: {thumb_img_url}
    alt: "{f.split('.')[0]}" """ # 使用文件名作为简单的描述
    yaml_output.append(yaml_block)

print("\n" + "="*20 + " YAML OUTPUT " + "="*20)
print("复制下面的代码到你的 .md 文件中的 gallery_film: 下方\n")
print("gallery_film:")
print("\n".join(yaml_output))
print("\n" + "="*40)