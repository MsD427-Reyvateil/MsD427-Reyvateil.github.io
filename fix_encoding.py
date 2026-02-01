#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复UTF-8编码问题的Python脚本
"""

import os
import re

# 定义要处理的目录
TARGET_DIR = "content/publications"

# 定义要替换的错误字符模式
ERROR_PATTERNS = [
    # 错误的减号和破折号
    (r'â\x88\x92', '-'),
    (r'â\x80\x94', '-'),
    (r'â\x80\x93', '-'),
    # 错误的引号
    (r'â\x80\x99', "'"),
    (r'â\x80\x98', "'"),
    (r'â\x80\x9d', '"'),
    (r'â\x80\x9c', '"'),
    # 其他错误字符
    (r'â\x80\xa6', '...'),
    (r'â\x80\xa2', '-'),
    # 错误的度符号
    (r'Â°', '°'),
    # 错误的正负号
    (r'Â±', '±'),
]

def fix_encoding(file_path):
    """修复文件中的编码问题"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 检查是否包含错误字符
        has_errors = any(re.search(pattern, content) for pattern, _ in ERROR_PATTERNS)
        
        if has_errors:
            # 替换错误字符
            new_content = content
            for pattern, replacement in ERROR_PATTERNS:
                new_content = re.sub(pattern, replacement, new_content)
            
            # 写入修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  Fixed encoding issues in {file_path}")
            return True
        else:
            print(f"  No encoding issues found in {file_path}")
            return False
            
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False

def main():
    """主函数"""
    print(f"Processing files in {TARGET_DIR}...")
    
    fixed_count = 0
    processed_count = 0
    
    # 遍历所有index.md文件
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file == "index.md":
                file_path = os.path.join(root, file)
                processed_count += 1
                if fix_encoding(file_path):
                    fixed_count += 1
    
    print(f"Processing complete!\nProcessed {processed_count} files, fixed {fixed_count} files.")

if __name__ == "__main__":
    main()
