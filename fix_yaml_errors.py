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

# 修复每个文件
error_count = 0
fixed_count = 0

for file_path in md_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否存在错误
        if "url: image:" in content:
            error_count += 1
            
            # 提取paper_block编号
            block_num = re.search(r'paper_block_(\d+)', file_path).group(1)
            
            # 构建基本URL
            base_url = f"https://www.chem.pku.edu.cn/zxyu/docs/2018-10/20181010"
            
            # 替换错误内容
            new_content = re.sub(r'links:\s*\n(.*?)url:\s*image:\s*\n\nimage:', f'links:\n  \n  - name: pubs\n    url: https://pubs.acs.org/doi/10.1021/ja0698196\n  \n  - name: SI\n    url: {base_url}paper_block_{block_num}.pdf\n\nimage:', content, flags=re.DOTALL)
            
            # 写入修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            fixed_count += 1
            print(f"Fixed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nTotal files with errors: {error_count}")
print(f"Total files fixed: {fixed_count}")
