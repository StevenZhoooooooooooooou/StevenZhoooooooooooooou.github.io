import os
from PIL import Image

# =================CONFIG=================
# 1. 图片所在的源文件夹路径
source_dir = "assets/images/2025/film"

# 2. 缩略图存放的文件夹名称
thumb_dir_name = "thumbs"

# 3. 网站上的基础 URL 前缀
base_url_prefix = "/assets/images/2025/film/"

# 4. 统一正方形边长 (像素)
# 所有缩略图都会变成 1500x1500 的正方形
SQUARE_SIZE = 1500
# ========================================

thumbs_output_dir = os.path.join(source_dir, thumb_dir_name)

# 确保缩略图文件夹存在
if not os.path.exists(thumbs_output_dir):
    os.makedirs(thumbs_output_dir)

# 获取所有 JPG 文件
files = sorted([f for f in os.listdir(source_dir) 
                if f.lower().endswith(('.jpg', '.jpeg')) 
                and os.path.isfile(os.path.join(source_dir, f))])

yaml_output = []

print(f"Processing {len(files)} images into Square Thumbnails...")

for f in files:
    original_path = os.path.join(source_dir, f)
    thumb_path = os.path.join(thumbs_output_dir, f)
    
    with Image.open(original_path) as img:
        # --- 核心逻辑开始 ---
        
        # 1. 创建一个纯白色的正方形画布 (RGB)
        # 如果你的网站背景不是纯白，可以修改 (255, 255, 255) 为对应的颜色
        square_bg = Image.new('RGB', (SQUARE_SIZE, SQUARE_SIZE), (255, 255, 255))
        
        # 2. 计算缩放比例，让图片能完整塞进正方形 (fit)
        img.thumbnail((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)
        
        # 3. 计算居中位置
        # (画布宽 - 图片宽) / 2
        offset_x = (SQUARE_SIZE - img.width) // 2
        offset_y = (SQUARE_SIZE - img.height) // 2
        
        # 4. 粘贴
        square_bg.paste(img, (offset_x, offset_y))
        
        # 5. 保存这个正方形缩略图
        square_bg.save(thumb_path, "JPEG", quality=90)
        print(f"Generated square thumbnail for: {f}")

    # --- 生成 YAML ---
    # url 指向原始大图 (点击后看原图，没有白边)
    full_img_url = f"{base_url_prefix}{f}"
    # image_path 指向带白边的正方形缩略图 (让排版整齐)
    thumb_img_url = f"{base_url_prefix}{thumb_dir_name}/{f}"
    
    # 提取文件名去掉后缀作为 alt
    alt_text = os.path.splitext(f)[0]
    
    yaml_block = f"""  - url: {full_img_url}
    image_path: {thumb_img_url}
    alt: "{alt_text}" """
    yaml_output.append(yaml_block)

print("\n" + "="*20 + " YAML OUTPUT " + "="*20)
print("请复制以下内容覆盖 gallery_film 部分：\n")
print("gallery_film:")
print("\n".join(yaml_output))
print("\n" + "="*40)