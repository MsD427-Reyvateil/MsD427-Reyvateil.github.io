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
processed_count = 0

for file_path in md_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            # 注释掉abstract行
            if line.strip().startswith('abstract:') and not line.strip().startswith('#'):
                new_lines.append(f"# {line}")
                modified = True
            # 注释掉summary行
            elif line.strip().startswith('summary:') and not line.strip().startswith('#'):
                new_lines.append(f"# {line}")
                modified = True
            else:
                new_lines.append(line)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            processed_count += 1
            print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nTotal files processed: {processed_count}")
