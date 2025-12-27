import os
import shutil

# ================= 配置区域 =================
# Markdown 文件路径
md_file_path = "_pages/photo-2025.md"

# 图片根目录
base_dir = "assets/images/2025/film"
# 缩略图目录
thumbs_dir = os.path.join(base_dir, "thumbs")

# URL 前缀
url_prefix_film = "/assets/images/2025/film/"
url_prefix_thumb = "/assets/images/2025/film/thumbs/"
# ===========================================

def normalize_files():
    print(f"🔄 正在标准化文件名 (统一为 .jpg)...")
    
    # 获取所有文件
    if not os.path.exists(base_dir):
        print(f"❌ 错误：找不到文件夹 {base_dir}")
        return []

    files = os.listdir(base_dir)
    renamed_count = 0
    
    for filename in files:
        file_path = os.path.join(base_dir, filename)
        
        # 跳过文件夹
        if os.path.isdir(file_path):
            continue
            
        # 分离文件名和后缀
        name, ext = os.path.splitext(filename)
        
        # 如果不是图片，跳过
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.bmp']:
            continue
            
        # 目标新文件名：后缀统一改为 .jpg (小写)
        new_filename = f"{name}.jpg"
        new_file_path = os.path.join(base_dir, new_filename)
        
        # 如果当前文件名不是 .jpg 结尾 (比如是 .jpeg 或 .JPG)，则重命名
        if filename != new_filename:
            # 1. 重命名原图
            os.rename(file_path, new_file_path)
            print(f"   [原图] {filename} -> {new_filename}")
            
            # 2. 检查并重命名对应的缩略图 (如果存在)
            thumb_old_path = os.path.join(thumbs_dir, filename)
            thumb_new_path = os.path.join(thumbs_dir, new_filename)
            
            if os.path.exists(thumb_old_path):
                os.rename(thumb_old_path, thumb_new_path)
                print(f"   [缩略] {filename} -> {new_filename}")
            
            renamed_count += 1

    print(f"✅ 标准化完成：重命名了 {renamed_count} 个文件。\n")

def generate_md():
    print(f"📝 正在生成 {md_file_path} ...")
    
    # 获取整理后的文件列表
    final_files = sorted([
        f for f in os.listdir(base_dir) 
        if os.path.isfile(os.path.join(base_dir, f)) 
        and f.lower().endswith('.jpg')
    ])
    
    content = []
    
    # --- 写入头部 YAML ---
    content.append("---")
    content.append('title: "2025 Portfolio"')
    content.append("permalink: /photography/2025/")
    content.append("layout: splash")
    content.append("author_profile: true")
    content.append("header:")
    content.append('  overlay_color: "#333"')
    
    # 数码部分 (空)
    content.append("gallery_digital: []")
    
    # 胶片部分
    content.append("gallery_film:")
    
    for f in final_files:
        thumb_path_local = os.path.join(thumbs_dir, f)
        has_thumb = os.path.exists(thumb_path_local)
        
        # 写入 YAML
        content.append(f"  - url: {url_prefix_film}{f}")
        
        if has_thumb:
            content.append(f"    image_path: {url_prefix_thumb}{f}")
        else:
            content.append(f"    image_path: {url_prefix_film}{f}")
            
        alt_text = os.path.splitext(f)[0]
        content.append(f'    alt: "{alt_text}"')

    content.append("---")
    
    # --- 写入正文 ---
    content.append("")
    content.append("## 📷 Digital")
    content.append("(Coming Soon)")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## 🎞️ Film")
    content.append('{% include gallery id="gallery_film" caption="Shot on Film" %}')
    
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
        
    print(f"✅ MD 文件写入完成! 包含 {len(final_files)} 张图片。")

if __name__ == "__main__":
    normalize_files() # 先改名
    generate_md()     # 后写文件