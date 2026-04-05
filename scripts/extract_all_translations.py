#!/usr/bin/env python3
"""
Extract all Dutch-English sentence pairs from gold-sentences.html
"""
import json
import re

# Read gold-sentences.html
with open('../gold-sentences.html', 'r', encoding='utf-8') as f:
    content = f.read()

translations = {}

# Extract ALL200 array
match = re.search(r'const ALL200=\[(.*?)\];', content, re.DOTALL)
if match:
    # Manual extraction since eval() is safer with controlled data
    all200_text = match.group(1)
    # Split by ]],[[
    items = all200_text.split(']],[')
    for item in items:
        item = item.strip('[]')
        parts = item.split('","')
        if len(parts) >= 2:
            dutch = parts[0].strip('"')
            english = parts[1].strip('"')
            translations[dutch] = english

print(f'Extracted {len(translations)} from ALL200')

# Extract SECTIONS array (contains P90 grammar pattern sentences)
# Format: {id:"...",title:"...",why:"...",rows:[["Dutch","English","note"],...]}
sections_matches = re.findall(r'rows:\[\[(.*?)\]\]', content, re.DOTALL)
for section_rows in sections_matches:
    # Split individual rows
    rows = section_rows.split('],[')
    for row in rows:
        parts = row.split('","')
        if len(parts) >= 2:
            dutch = parts[0].strip('"[')
            english = parts[1].strip('"')
            translations[dutch] = english

print(f'Total {len(translations)} sentence pairs after adding SECTIONS')

# Save to JSON
with open('../sentence_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print('✓ Saved to sentence_translations.json')

# Show sample
print('\nSample translations:')
for i, (dutch, english) in enumerate(list(translations.items())[:5]):
    print(f'{i+1}. {dutch}')
    print(f'   → {english}\n')
