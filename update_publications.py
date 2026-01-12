import os
import re

# 定义目标文件夹路径
target_dir = "F:\work\prime-quartz_unzipped\prime-quartz-main\content\publications"

# 获取所有paper_block_*文件夹中的index.md文件
md_files = []
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file == "index.md" and "paper_block_" in root:
            md_files.append(os.path.join(root, file))

# 处理每个文件
for file_path in md_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取现有的pubs和SI链接
        pubs_match = re.search(r'-\s*name:\s*pubs\s*\n\s*url:\s*(.*?)\s*\n', content)
        si_match = re.search(r'-\s*name:\s*SI\s*\n\s*url:\s*(.*?)\s*\n', content)
        
        # 构建新的links部分
        new_links = "links:\n  "
        if pubs_match:
            pubs_url = pubs_match.group(1)
            new_links += f"\n  - name: pubs\n    url: {pubs_url}"
        if si_match:
            si_url = si_match.group(1)
            new_links += f"\n  \n  - name: SI\n    url: {si_url}"
        new_links += "\n\n"
        
        # 替换原有links部分
        content = re.sub(r'links:(.*?)\n\nimage:', new_links + 'image:', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nTotal files processed: {len(md_files)}")
