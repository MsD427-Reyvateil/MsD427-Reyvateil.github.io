#!/usr/bin/env python3
"""
Script to restore date fields in publication files using values from data fields.
"""

import os
import re
import glob

def main():
    # Get all publication index.md files
    pub_files = glob.glob('content/publications/**/index.md', recursive=True)
    
    print(f"Found {len(pub_files)} publication files to process.")
    
    # Regular expressions
    data_pattern = re.compile(r'^\s*data:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)
    
    processed_count = 0
    
    for file_path in pub_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract data field value
        data_match = data_pattern.search(content)
        if not data_match:
            continue
        
        data_value = data_match.group(1)
        
        # The data value is already in YYYY-MM-DD format, so we can use it directly for the date field
        date_value = f'date: "{data_value}"'
        
        # Add or update the date field
        lines = content.split('\n')
        new_lines = []
        data_found = False
        date_found = False
        
        for line in lines:
            # Check if this is a date line
            if re.match(r'^\s*date:\s*["\'].*["\']\s*$', line.strip()):
                # Update existing date line
                new_lines.append(date_value)
                date_found = True
            elif re.match(r'^\s*data:\s*["\'].*["\']\s*$', line.strip()):
                # Keep the data line, mark it as found
                new_lines.append(line)
                data_found = True
            else:
                new_lines.append(line)
        
        # If no date field was found, add it below the data field
        if not date_found and data_found:
            # Find the index of the data line
            for i, line in enumerate(new_lines):
                if re.match(r'^\s*data:\s*["\'].*["\']\s*$', line.strip()):
                    # Insert date field below data field
                    new_lines.insert(i + 1, f'\n{date_value}')
                    break
        
        # Write back the modified content
        new_content = '\n'.join(new_lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        processed_count += 1
        print(f"Processed: {file_path} - Added date: {data_value}")
    
    print(f"\nDone!")
    print(f"Processed files: {processed_count}")

if __name__ == "__main__":
    main()
