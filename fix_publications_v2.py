import os
import re
import glob

def fix_publication_file(file_path):
    """Fix a single publication file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from the file
    title_pattern = r'title:\s*[\'"](.*?)[\'"]'
    title_match = re.search(title_pattern, content)
    if not title_match:
        return
    
    title = title_match.group(1)
    
    # Fix abstract field - replace with title
    new_abstract = f'abstract: "{title}"'
    content = re.sub(r'abstract:\s*.*?(?=\n\n\n# Summary)', new_abstract, content, flags=re.DOTALL)
    
    # Fix summary field - replace with title and add quotes if missing
    new_summary = f'summary: "{title}"'
    content = re.sub(r'summary:\s*.*?(?=\n\n# tags)', new_summary, content, flags=re.DOTALL)
    
    # Fix date field - extract year from filename if possible
    folder_name = os.path.basename(os.path.dirname(file_path))
    year_pattern = r'(20\d{2})'
    year_match = re.search(year_pattern, content)
    if year_match:
        year = year_match.group(0)
        content = re.sub(r'date:\s*\'.*?\'', f'date: \'{year}-01-01T00:00:00+00:00\'', content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {os.path.basename(file_path)}")

# Get all generated publication files
base_dir = 'f:/work/prime-quartz_unzipped/prime-quartz-main/content/publications'
publication_files = glob.glob(os.path.join(base_dir, '**', 'index.md'), recursive=True)

# Filter out the original conference-paper and preprint files
to_fix_files = [f for f in publication_files if 'conference-paper' not in f and 'preprint' not in f]

# Fix each file
for file_path in to_fix_files:
    fix_publication_file(file_path)

print(f"Fixed {len(to_fix_files)} files.")