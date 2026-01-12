import os
import re
import glob

def fix_yaml_syntax(file_path):
    """Fix YAML syntax errors in publication files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix abstract field
    abstract_pattern = r'abstract:\s*(.*?)\n\n\n# Summary'
    match = re.search(abstract_pattern, content, re.DOTALL)
    if match:
        abstract_content = match.group(1).strip()
        # If abstract doesn't start with quotes, add them
        if not (abstract_content.startswith('"') or abstract_content.startswith("'")):
            new_abstract = f'abstract: "{abstract_content}"'
            content = content.replace(f'abstract: {abstract_content}', new_abstract)
    
    # Fix summary field
    summary_pattern = r'summary:\s*(.*?)\n\n# tags'
    match = re.search(summary_pattern, content, re.DOTALL)
    if match:
        summary_content = match.group(1).strip()
        # If summary doesn't start with quotes, add them
        if not (summary_content.startswith('"') or summary_content.startswith("'")):
            new_summary = f'summary: "{summary_content}"'
            content = content.replace(f'summary: {summary_content}', new_summary)
    
    # Fix date field if it has wrong year
    content = re.sub(r'date: \'2013-07-01T00:00:00\'\'', "date: '2015-01-01T00:00:00+00:00'", content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed YAML syntax in: {file_path}")

# Get all generated publication files
base_dir = 'f:/work/prime-quartz_unzipped/prime-quartz-main/content/publications'
publication_files = glob.glob(os.path.join(base_dir, '**', 'index.md'), recursive=True)

# Filter out the original conference-paper and preprint files
to_fix_files = [f for f in publication_files if 'conference-paper' not in f and 'preprint' not in f]

# Fix each file
for file_path in to_fix_files:
    fix_yaml_syntax(file_path)

print(f"Fixed YAML syntax in {len(to_fix_files)} files.")