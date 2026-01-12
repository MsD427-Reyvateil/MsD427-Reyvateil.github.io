import os
import re
import requests
import shutil

# 配置路径
markdown_dir = 'f:\work\prime-quartz_unzipped\资源\publications_markdown'
images_dir = 'f:\work\prime-quartz_unzipped\prime-quartz-main\content\publications\images'

# 确保图片目录存在
os.makedirs(images_dir, exist_ok=True)

# 提取所有图片URL
image_urls = []

# 遍历所有Markdown文件
for filename in os.listdir(markdown_dir):
    if filename.endswith('.md'):
        markdown_path = os.path.join(markdown_dir, filename)
        
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取封面图片URL
        cover_match = re.search(r'- 封面:(https?://[^\s]+)', content)
        if cover_match:
            image_urls.append(cover_match.group(1))
        
        # 提取研究成果图片URL
        research_match = re.search(r'- 研究成果:(https?://[^\s]+)', content)
        if research_match:
            image_urls.append(research_match.group(1))

# 去重
image_urls = list(set(image_urls))
print(f"共提取到 {len(image_urls)} 个图片URL")

# 下载图片
for i, url in enumerate(image_urls):
    try:
        print(f"正在下载: {url}")
        # 发送请求下载图片
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        # 从URL中提取文件名
        filename = url.split('/')[-1]
        # 生成本地文件路径
        local_path = os.path.join(images_dir, filename)
        
        # 保存图片
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"成功下载: {filename}")
    except Exception as e:
        print(f"下载失败: {url} - {e}")

print("所有图片下载完成！")

# 生成图片URL映射
print("\n图片URL映射:")
for filename in os.listdir(images_dir):
    local_path = os.path.join(images_dir, filename)
    # GitHub仓库中的URL格式
    github_url = f"https://raw.githubusercontent.com/lllolllolll/prime-quartz/main/content/publications/images/{filename}"
    print(f"{filename}: {github_url}")
