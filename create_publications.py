import json
import os
import re

# 从web_reference中提取的文献数据
literature_data = [
    {
        "title": "Catalytic (4+2) Annulation via Regio- and Enantioselective Interception of in-situ Generated Alkylgold Intermediate",
        "authors": "Ming Bao+, Yi Zhou+, Haoxuan Yuan+, Guizhi Dong, Chao Li, Xiongda Xie, Kewei Chen, Kemiao Hong, Zhi-Xiang Yu*, and Xinfang Xu*",
        "journal": "Angew. Chem. Int. Ed.",
        "year": "2024",
        "volume": "63",
        "page": "e202401557"
    },
    {
        "title": "Direct insertion into the C–C bond of unactivated ketones with NaH-mediated aryne chemistry",
        "authors": "Fan Luo#, Chen-Long Li#, Peng Ji, Yuxin Zhou, Jingjing Gui, Lingyun Chen, Yuejia Yin, Xinyu Zhang, Yanwei Hu, Xiaobei Chen, Xuejun Liu, Xiaodong Chen, Zhi-Xiang Yu*, Wei Wang*, Shi-Lei Zhang*",
        "journal": "Chem",
        "year": "2023",
        "volume": "9",
        "page": "2620-2636"
    },
    {
        "title": "Catalytic Enantioselective Construction of 6-4 Ring-Junction All-Carbon Stereocenters and Mechanistic Insights",
        "authors": "Jia-Yin Wang, Chen-Long Li, Ting Xu, Meng-Fan Li, Wen-Juan Hao, Shu-Jiang Tu, Jianyi Wang*, Guigen Li, Zhi-Xiang Yu*, and Bo Jiang*",
        "journal": "Chin. J. Chem.",
        "year": "2022",
        "volume": "40",
        "page": "1767-1776"
    },
    {
        "title": "Synthesis of Quaternary Carbon-Centered Benzoindolizidinones via Novel Photoredox-Catalyzed Alkene Aminoarylation: Facile Access to Tylophorine and Analogues",
        "authors": "Chao Zhang, Yi Wang, Yugang Song, Hongying Gao, Yonghui Sun, Xiuyun Sun, Yiqing Yang, Ming He, Zimo Yang, Lingpeng Zhan, Zhi-Xiang Yu*, and Yu Rao*",
        "journal": "CCS Chem.",
        "year": "2019",
        "volume": "1",
        "page": "352−364"
    },
    {
        "title": "Conformational Bias by a Removable Silyl Group: Construction of Bicyclo[n.3.1]alkenes by Ring Closing Metathesis",
        "authors": "Minggui Lin, Pei-Jun Cai, Zhixiong Zeng, Na Lin, Yang Shen, Bin Tang, Fan Li, Chen Chen, Zhi-Xiang Yu*, Yandong Zhang*",
        "journal": "Chem. Eur. J.",
        "year": "2018",
        "volume": "24",
        "page": "2334-2338"
    },
    {
        "title": "Cycloaddition Reaction of Vinylphenylfurans and Dimethyl Acetylenedicarboxylate to [8+2] Isomers via Tandem [4+2]/Diradical Alkene-Alkene Coupling/[1,3]-H Shift Reactions: Experimental Exploration and DFT Understanding of Reaction Mechanism",
        "authors": "Kai Chen, Feng Wu, Lijuan Ye, Ziyou Tian, Zhi-Xiang Yu*, Shifa Zhu*",
        "journal": "J. Org. Chem.",
        "year": "2016",
        "volume": "81",
        "page": "8155-8168"
    },
    {
        "title": "Organocatalytic Asymmetric Tandem Nazarov Cyclization/Semipinacol Rearrangement: Rapid Construction of Chiral Spiro[4.4]nonane-1,6-diones",
        "authors": "Bin-Miao Yang, Pei-Jun Cai, Yong-Qiang Tu* Zhi-Xiang Yu, Zhi-Min Chen, Shuang-Hu Wang, Shao-Hua Wang, and Fu-Min Zhang",
        "journal": "J. Am. Chem. Soc.",
        "year": "2015",
        "volume": "137",
        "page": "8344-8347"
    },
    {
        "title": "On‐Demand Selection of the Reaction Path from Imino Diels–Alder to Ene‐Type Cyclization: Synthesis of Epiminopyrimido[4,5‐b]azepines",
        "authors": "Yuewei Zhang, Yue Zhu, Lianyou Zheng, Lian-Gang Zhuo, Fengzhi Yang, Qun"
    }
]

# 保存图片的目录
image_dir = 'F:/work/prime-quartz_unzipped/prime-quartz-main/content/publications/picture'

# 确保图片目录存在
os.makedirs(image_dir, exist_ok=True)

# 创建出版物列表
publications = []

# 遍历文献数据，创建出版物条目
for i, data in enumerate(literature_data):
    # 提取文献信息
    title = data["title"]
    authors = data["authors"]
    year = data.get("year", "Unknown")
    
    # 生成文献封面图片路径（目前使用现有图片，后续可以添加真实图片）
    cover_img_path = f"/publications/picture/20240406011024544723.jpg"  # 使用现有图片
    formula_img_path = f"/publications/picture/20240406011115604810.png"  # 使用现有图片
    
    # 创建出版物字典
    publication = {
        "文献封面图片": cover_img_path,
        "文献名称": title,
        "作者名称": authors,
        "时间": year,
        "化学式图片": formula_img_path
    }
    
    publications.append(publication)

# 保存为JSON文件
with open('publications.json', 'w', encoding='utf-8') as f:
    json.dump(publications, f, ensure_ascii=False, indent=4)

print(f"Successfully created {len(publications)} publication entries.")
print(f"JSON file saved as publications.json")

# 现在创建出版物项目
# 读取模板文件
with open('f:/work/prime-quartz_unzipped/prime-quartz-main/content/publications/conference-paper/index.md', 'r', encoding='utf-8') as f:
    template = f.read()

# 为每个出版物创建一个文件夹和index.md文件
publications_dir = 'f:/work/prime-quartz_unzipped/prime-quartz-main/content/publications'

for i, publication in enumerate(publications):
    # 创建文件夹名称（使用标题的简化版本）
    folder_name = re.sub(r'[^a-zA-Z0-9]', '-', publication["文献名称"][:50]).lower()
    folder_path = os.path.join(publications_dir, folder_name)
    
    # 创建文件夹
    os.makedirs(folder_path, exist_ok=True)
    
    # 替换模板中的内容
    content = template.replace('An example conference paper', publication["文献名称"])
    
    # 替换作者
    authors_line = 'authors:'
    authors_content = '  - admin\n  - Robert Ford'
    # 简化处理，实际可能需要更复杂的解析
    new_authors_content = '  - admin'
    content = content.replace(f'{authors_line}\n{authors_content}', f'{authors_line}\n{new_authors_content}')
    
    # 替换日期
    content = content.replace('date: \'2013-07-01T00:00:00+00:00\'', f'date: \'{publication["时间"]}-01-01T00:00:00+00:00\'')
    
    # 替换摘要
    abstract = publication["文献名称"]
    content = content.replace('abstract: \t\tRhodium-Catalyzed [3 + 1 + 2] Cycloaddition of Type II Diene-Vinylcyclopropanes and Carbon Monoxide for the Synthesis of 5/6 Skeletons with Two Adjacent Bridgehead Quaternary Centers', f'abstract: {abstract}')
    content = content.replace('summary: Rhodium-Catalyzed [3 + 1 + 2] Cycloaddition of Type II Diene-Vinylcyclopropanes and Carbon Monoxide for the Synthesis of 5/6 Skeletons with Two Adjacent Bridgehead Quaternary Centers', f'summary: {abstract}')
    
    # 替换图片
    content = content.replace('image:\n  caption: \'Image credit: [**Unsplash**](https://unsplash.com/photos/pLCdAaMFLTE)\'\n  focal_point: \'\'\n  preview_only: false', f'image:\n  caption: \'{publication["文献名称"]}\'' )
    
    # 保存index.md文件
    index_path = os.path.join(folder_path, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created publication: {folder_name}")

print(f"Successfully created {len(publications)} publication projects.")