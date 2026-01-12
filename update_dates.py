import os
import re
from datetime import datetime, timedelta

# 定义目标目录
target_dir = r"F:\work\prime-quartz_unzipped\prime-quartz-main\content\publications"

# 初始化前一个日期变量
previous_date = None

# 从177到1遍历文件夹
for i in range(177, 0, -1):
    # 构建文件夹路径
    folder_name = f"paper_block_{i}"
    folder_path = os.path.join(target_dir, folder_name)
    file_path = os.path.join(folder_path, "index.md")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取date字段值
        date_match = re.search(r'date:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"', content)
        if date_match:
            current_date_str = date_match.group(1)
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
            
            # 如果不是第一个文件，检查是否需要修改日期
            if i != 177:
                if current_date == previous_date:
                    # 日期相同，日数+1
                    new_date = current_date + timedelta(days=1)
                    new_date_str = new_date.strftime("%Y-%m-%d")
                    
                    # 更新文件内容
                    new_content = re.sub(r'date:\s*"[0-9]{4}-[0-9]{2}-[0-9]{2}"', f'date: "{new_date_str}"', content)
                    
                    # 写入更新后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"Updated {folder_name}: {current_date_str} -> {new_date_str}")
                    
                    # 更新previous_date为新日期
                    previous_date = new_date
                else:
                    # 日期不同，直接更新previous_date
                    previous_date = current_date
                    print(f"Kept {folder_name}: {current_date_str}")
            else:
                # 第一个文件，初始化previous_date
                previous_date = current_date
                print(f"Initial {folder_name}: {current_date_str}")
        else:
            print(f"No date found in {folder_name}")
    else:
        print(f"File not found: {file_path}")
