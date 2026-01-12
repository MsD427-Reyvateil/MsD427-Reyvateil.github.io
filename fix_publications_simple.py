import os
import glob

def fix_publication_file(file_path):
    """Fix YAML syntax errors in a single publication file"""
    print(f"Fixing: {file_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the lines that need fixing
    abstract_line = None
    summary_line = None
    title_line = None
    
    for i, line in enumerate(lines):
        if line.startswith('title:'):
            title_line = i
        elif line.startswith('abstract:'):
            abstract_line = i
        elif line.startswith('summary:'):
            summary_line = i
    
    # Extract title
    title = ''
    if title_line is not None:
        title = lines[title_line].split(':', 1)[1].strip().strip("'\"\n")
    
    # Fix abstract line
    if abstract_line is not None:
        lines[abstract_line] = f'abstract: "{title}"\n'
    
    # Fix summary line
    if summary_line is not None:
        lines[summary_line] = f'summary: "{title}"\n'
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# Get all generated publication files
base_dir = 'f:/work/prime-quartz_unzipped/prime-quartz-main/content/publications'
publication_files = glob.glob(os.path.join(base_dir, '**', 'index.md'), recursive=True)

# Filter out the original conference-paper and preprint files
to_fix_files = [f for f in publication_files if 'conference-paper' not in f and 'preprint' not in f]

# Fix each file
for file_path in to_fix_files:
    fix_publication_file(file_path)

print(f"Fixed {len(to_fix_files)} files.")