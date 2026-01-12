#!/usr/bin/env python3
"""
Script to fix data fields in publication files to use correct date from Chemical formula URL.
"""

import os
import re
import glob

def main():
    # Get all publication index.md files
    pub_files = glob.glob('content/publications/**/index.md', recursive=True)
    
    print(f"Found {len(pub_files)} publication files to process.")
    
    # Regular expressions
    chemical_formula_pattern = re.compile(r'!\[Chemical formula\]\((https?://[^)]+)\)', re.MULTILINE)
    data_pattern = re.compile(r'^\s*data:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)
    publication_pattern = re.compile(r'^\s*publication:', re.MULTILINE)
    
    processed_count = 0
    
    for file_path in pub_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Chemical formula URL
        formula_match = chemical_formula_pattern.search(content)
        if not formula_match:
            continue
        
        formula_url = formula_match.group(1)
        
        # Extract substring between content/ and next /
        content_idx = formula_url.find('content/')
        if content_idx == -1:
            continue
        
        start_idx = content_idx + len('content/')
        end_idx = formula_url.find('/', start_idx)
        if end_idx == -1:
            continue
        
        extracted_str = formula_url[start_idx:end_idx]
        
        # Format the correct data value
        correct_data_value = f'data: "{extracted_str}-01"'
        
        # Check if data field exists and needs updating
        data_match = data_pattern.search(content)
        if data_match:
            current_data = data_match.group(1)
            expected_data = f"{extracted_str}-01"
            
            if current_data != expected_data:
                # Update existing data field
                new_content = data_pattern.sub(correct_data_value, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                processed_count += 1
                print(f"Fixed: {file_path} - Updated data from {current_data} to {expected_data}")
        else:
            # Data field doesn't exist, add it below publication line
            lines = content.split('\n')
            new_lines = []
            publication_found = False
            
            for line in lines:
                new_lines.append(line)
                
                if publication_pattern.match(line.strip()):
                    new_lines.append(f'\n{correct_data_value}')
                    publication_found = True
            
            if publication_found:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                processed_count += 1
                print(f"Added: {file_path} - Added data {expected_data}")
    
    print(f"\nDone!")
    print(f"Processed files: {processed_count}")

if __name__ == "__main__":
    main()
