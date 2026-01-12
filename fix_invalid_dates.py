#!/usr/bin/env python3
"""
Script to fix invalid date fields in publication files.
"""

import os
import re
import glob

def main():
    # Get all publication index.md files
    pub_files = glob.glob('content/publications/**/index.md', recursive=True)
    
    print(f"Found {len(pub_files)} publication files to process.")
    
    # Regular expressions
    date_pattern = re.compile(r'^\s*date:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)
    
    fixed_count = 0
    
    for file_path in pub_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract date field value
        date_match = date_pattern.search(content)
        if not date_match:
            continue
        
        date_value = date_match.group(1)
        
        # Check if date is valid YYYY-MM-DD format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_value):
            # Invalid date, fix it
            print(f"Fixing invalid date in {file_path}: {date_value}")
            
            # Replace with default date or extract year from publication info if possible
            # For simplicity, we'll use a safe default date
            fixed_date = '2000-01-01'
            
            # Update the date field
            fixed_date_line = f'date: "{fixed_date}"'
            new_content = date_pattern.sub(fixed_date_line, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            fixed_count += 1
    
    print(f"\nDone!")
    print(f"Fixed files: {fixed_count}")

if __name__ == "__main__":
    main()
