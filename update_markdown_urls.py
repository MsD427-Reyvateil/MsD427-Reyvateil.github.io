import os
import re

# 配置路径
input_dir = 'f:\work\prime-quartz_unzipped\资源\publications_markdown'
output_dir = 'f:\work\prime-quartz_unzipped\资源\publications_markdown_updated'
images_dir = 'f:\work\prime-quartz_unzipped\prime-quartz-main\content\publications\images'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 获取所有图片文件名，用于生成URL映射
image_files = os.listdir(images_dir)

# 遍历所有Markdown文件
for filename in os.listdir(input_dir):
    if filename.endswith('.md'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        print(f"正在处理: {filename}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换封面图片URL
        def replace_cover_url(match):
            original_url = match.group(1)
            # 从原始URL中提取文件名
            image_filename = original_url.split('/')[-1]
            # 直接生成GitHub URL，不检查文件是否存在
            github_url = f"https://raw.githubusercontent.com/lllolllolll/prime-quartz/main/content/publications/images/{image_filename}"
            return f"- 封面:{github_url}"
        
        content = re.sub(r'- 封面:(https?://[^\s]+)', replace_cover_url, content)
        
        # 替换研究成果图片URL
        def replace_research_url(match):
            original_url = match.group(1)
            # 从原始URL中提取文件名
            image_filename = original_url.split('/')[-1]
            # 直接生成GitHub URL，不检查文件是否存在
            github_url = f"https://raw.githubusercontent.com/lllolllolll/prime-quartz/main/content/publications/images/{image_filename}"
            return f"- 研究成果:{github_url}"
        
        content = re.sub(r'- 研究成果:(https?://[^\s]+)', replace_research_url, content)
        
        # 保存修改后的文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"成功保存: {filename}")

print("所有文件处理完成！")
print(f"修改后的Markdown文件已保存到: {output_dir}")
