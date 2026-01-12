import os
from bs4 import BeautifulSoup
import re

# 配置路径
html_dir = 'f:\work\prime-quartz_unzipped\资源\publications_blocks'
markdown_dir = 'f:\work\prime-quartz_unzipped\资源\publications_markdown'

# 确保输出目录存在
os.makedirs(markdown_dir, exist_ok=True)

# 基础URL，用于将相对路径转换为绝对路径
base_url = 'https://www.chem.pku.edu.cn/zxyu/'

# 遍历所有HTML文件
for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        html_path = os.path.join(html_dir, filename)
        markdown_filename = filename.replace('.html', '.md')
        markdown_path = os.path.join(markdown_dir, markdown_filename)
        
        print(f"正在转换: {filename} -> {markdown_filename}")
        
        try:
            # 读取HTML文件
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取封面图片URL（第一个图片）
            cover_img = soup.find('img')
            cover_url = ''
            if cover_img:
                cover_src = cover_img.get('src', '')
                if cover_src.startswith('../'):
                    # 将相对路径转换为绝对路径
                    cover_url = base_url + cover_src[3:]
                else:
                    cover_url = cover_src
            
            # 提取论文标题（链接文本）
            title_link = soup.find('a')
            title = ''
            if title_link:
                title = title_link.text.strip()
            
            # 提取作者和刊物信息
            author = ''
            journal_info = ''
            
            # 查找所有 <font size="2"> 标签
            font_tags = soup.find_all('font', size='2')
            
            for font_tag in font_tags:
                # 直接获取font标签内的完整HTML内容
                font_html = str(font_tag)
                
                # 检查是否包含作者和刊物信息的特征
                if ('and' in font_html or ',' in font_html) and ('J. ' in font_html or 'Angew. ' in font_html or 'Org. ' in font_html or 'Chem. ' in font_html):
                    # 创建一个新的BeautifulSoup对象
                    font_soup = BeautifulSoup(font_html, 'html.parser')
                    
                    # 移除所有注释
                    for comment in font_soup.find_all(text=lambda text: isinstance(text, str) and '<!--' in text):
                        comment.extract()
                    
                    # 获取所有文本内容
                    all_text = font_soup.get_text(separator=' ', strip=True)
                    
                    # 分离作者和刊物信息
                    # 查找第一个数字年份，通常是刊物信息的开始
                    year_match = re.search(r'\b\d{4}\b', all_text)
                    
                    if year_match:
                        # 作者信息在年份之前
                        author = all_text[:year_match.start()].strip()
                        # 刊物信息从年份开始
                        journal_part = all_text[year_match.start():].strip()
                        
                        # 提取完整的刊物信息，直到遇到下一个作者信息或结束
                        # 常见格式：Year, Volume, PageRange
                        # 使用正则表达式匹配完整的刊物信息
                        journal_regex = r'(\d{4})\s*[,\s]+(.*?)(?:\.|$)'  
                        journal_match = re.search(journal_regex, journal_part)
                        
                        if journal_match:
                            # 查找期刊名称
                            # 期刊名称通常在作者信息之后，年份之前
                            # 在原始font_html中查找期刊名称
                            journal_name_match = re.search(r'(Angew\. Chem\. Int\. Ed\.|J\. Org\. Chem\.|Chem\. Eur\. J\.|Org\. Lett\.|J\. Am\. Chem\. Soc\.|Chem\.)', font_html)
                            if journal_name_match:
                                journal_name = journal_name_match.group(1)
                                journal_info = f"{journal_name} {journal_match.group(0).strip()}"
                            else:
                                journal_info = journal_match.group(0).strip()
                        else:
                            journal_info = journal_part
                    else:
                        # 如果没有找到年份，尝试其他方法
                        # 查找期刊名称
                        journal_name_match = re.search(r'(Angew\. Chem\. Int\. Ed\.|J\. Org\. Chem\.|Chem\. Eur\. J\.|Org\. Lett\.|J\. Am\. Chem\. Soc\.|Chem\.)', font_html)
                        if journal_name_match:
                            journal_name = journal_name_match.group(1)
                            # 作者信息在期刊名称之前
                            author = all_text[:journal_name_match.start()].strip()
                            # 刊物信息从期刊名称开始
                            journal_info = all_text[journal_name_match.start():].strip()
                    
                    # 清理作者和刊物信息
                    author = re.sub(r'\s+', ' ', author).strip()
                    journal_info = re.sub(r'\s+', ' ', journal_info).strip()
                    
                    # 移除任何残留的HTML标签
                    journal_info = BeautifulSoup(journal_info, 'html.parser').get_text(strip=True)
                    
                    # 如果找到有效信息，跳出循环
                    if author and journal_info:
                        break
            
            # 进一步清理
            author = re.sub(r'\s+', ' ', author).strip()
            journal_info = re.sub(r'\s+', ' ', journal_info).strip()
            
            # 确保刊物信息格式正确
            if journal_info and not journal_info.endswith('.'):
                journal_info += '.'
            
            # 确保作者信息不包含期刊名称
            for journal_name in ['Angew. Chem. Int. Ed.', 'J. Org. Chem.', 'Chem. Eur. J.', 'Org. Lett.', 'J. Am. Chem. Soc.', 'Chem.']:
                if journal_name in author:
                    author = author.replace(journal_name, '').strip()
                    break
            
            # 提取研究成果图片URL（第二个图片）
            img_tags = soup.find_all('img')
            research_img_url = ''
            if len(img_tags) >= 2:
                research_img = img_tags[1]
                research_src = research_img.get('src', '')
                if research_src.startswith('../'):
                    # 将相对路径转换为绝对路径
                    research_img_url = base_url + research_src[3:]
                else:
                    research_img_url = research_src
            
            # 生成Markdown内容
            markdown_content = f"- 封面:{cover_url}\n"
            markdown_content += f"- 文字1：\"{title}\"\n"
            markdown_content += f"- 作者： \"{author}\"\n"
            markdown_content += f"- 刊物时间编号：{journal_info}\n"
            markdown_content += f"- 研究成果：{research_img_url}\n"
            
            # 保存Markdown文件
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                
        except Exception as e:
            print(f"转换失败: {filename} - {e}")
            continue

print("所有文件转换完成！")