import requests
from bs4 import BeautifulSoup
import os
import re

# 网站URL
base_url = 'https://www.chem.pku.edu.cn/zxyu/publications/index.htm'

# 保存元素块的目录
blocks_dir = 'f:/work/prime-quartz_unzipped/资源/publications_blocks'

# 确保目录存在
os.makedirs(blocks_dir, exist_ok=True)

# 发送请求获取网页内容
try:
    response = requests.get(base_url, timeout=10, verify=False)  # 跳过SSL证书验证
    response.raise_for_status()  # 检查请求是否成功
    html_content = response.text
except requests.RequestException as e:
    print(f"获取网页失败: {e}")
    exit(1)

# 忽略SSL警告
requests.packages.urllib3.disable_warnings()  # 禁用SSL警告

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有符合条件的元素块
# 根据示例，我们需要查找包含论文信息的表格
# 分析示例HTML，论文元素块具有以下特征：
# 1. 包含论文标题链接
# 2. 包含作者和期刊信息
# 3. 结构与示例相似
paper_blocks = soup.find_all('table')

# 过滤掉可能不是论文块的表格
filtered_blocks = []
for block in paper_blocks:
    # 获取所有链接
    links = block.find_all('a', href=True)
    # 获取所有字体标签，通常包含论文信息
    font_tags = block.find_all('font')
    
    # 检查是否符合论文块特征：
    # 1. 包含链接
    # 2. 包含字体标签（通常包含论文信息）
    # 3. 链接包含pdf或doi等论文相关链接
    # 4. 排除导航栏等非论文块
    is_paper_block = False
    for link in links:
        href = link.get('href', '')
        # 论文链接通常包含.pdf或doi等关键词
        if '.pdf' in href.lower() or 'doi' in href.lower() or '/docs/' in href:
            is_paper_block = True
            break
    
    # 另外检查是否包含作者和期刊信息
    if not is_paper_block and font_tags:
        # 检查字体标签中是否包含作者和期刊信息
        text = block.get_text(separator=' ', strip=True)
        if 'and' in text and ('J. ' in text or 'Angew. ' in text or 'Org. ' in text or 'Chem. ' in text):
            is_paper_block = True
    
    # 排除导航栏等非论文块
    if is_paper_block:
        # 检查是否包含导航链接，排除导航栏
        nav_keywords = ['Home', 'Group', 'Research', 'Publications', 'News']
        nav_found = any(keyword in block.get_text() for keyword in nav_keywords)
        if not nav_found:
            filtered_blocks.append(block)

# 保存每个元素块为HTML文件
print(f"共找到 {len(filtered_blocks)} 个论文元素块")

for i, block in enumerate(filtered_blocks):
    # 生成唯一文件名
    file_name = f"paper_block_{i+1}.html"
    file_path = os.path.join(blocks_dir, file_name)
    
    # 保存元素块的HTML内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(block))
    
    print(f"已保存: {file_path}")

print("所有元素块已保存完成！")