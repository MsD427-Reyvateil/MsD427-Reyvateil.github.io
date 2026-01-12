#!/usr/bin/env python3
"""
Script to update data fields in publication files using dates from SI URLs.
"""

import os
import re
import glob

def main():
    # Get all publication index.md files
    pub_files = glob.glob('content/publications/**/index.md', recursive=True)
    
    print(f"Found {len(pub_files)} publication files to process.")
    
    # Regular expressions - more flexible with spacing
    si_section_pattern = re.compile(r'\s*-\s*name:\s*SI\s*\n\s*url:\s*["\']?([^"\'\n]+)["\']?', re.MULTILINE | re.IGNORECASE)
    data_pattern = re.compile(r'^\s*data:\s*["\']?([^"\'\n]+)["\']?\s*$', re.MULTILINE)
    
    processed_count = 0
    skipped_count = 0
    
    for file_path in pub_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has SI section
        si_match = si_section_pattern.search(content)
        if not si_match:
            skipped_count += 1
            continue
        
        si_url = si_match.group(1)
        
        # Extract date from URL (between docs/ and next /)
        docs_idx = si_url.find('docs/')
        if docs_idx == -1:
            skipped_count += 1
            continue
        
        start_idx = docs_idx + len('docs/')
        end_idx = si_url.find('/', start_idx)
        if end_idx == -1:
            skipped_count += 1
            continue
        
        extracted_date = si_url[start_idx:end_idx]
        
        # Extract and update data field
        data_match = data_pattern.search(content)
        if not data_match:
            skipped_count += 1
            continue
        
        current_data = data_match.group(1)
        
        # Replace the year-month part of the data field with the year-month from the URL
        # Example: data: "2025-08-01" -> update to "url_year_month-01"
        # Extract year-month from the URL date (which might be YYYY-MM or YYYY-MM-DD)
        url_year_month = extracted_date.split('-', 2)[:2]  # Get first two parts: [YYYY, MM]
        url_year_month = '-'.join(url_year_month)
        
        # Format the updated data as YYYY-MM-01
        updated_data = f"{url_year_month}-01"
        
        new_data_line = f'data: "{updated_data}"'
        
        # Update the data field
        new_content = data_pattern.sub(new_data_line, content)
        
        # Also update the date field to match
        date_pattern = re.compile(r'^\s*date:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)
        if date_pattern.search(new_content):
            new_content = date_pattern.sub(f'date: "{updated_data}"', new_content)
        
        # Write back the modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        processed_count += 1
        print(f"Processed: {file_path} - Updated data from {current_data} to {updated_data}")
    
    print(f"\nDone!")
    print(f"Processed files: {processed_count}")
    print(f"Skipped files: {skipped_count}")

if __name__ == "__main__":
    main()
