#!/usr/bin/env python3
"""
Generate CSV of all extracted sentences for external tagging.
"""

import re
import csv
from pathlib import Path

def extract_sentences(text):
    """Extract sentences from text."""
    # Remove line numbers
    text = re.sub(r'^\s*\d+→', '', text, flags=re.MULTILINE)

    # Split on sentence endings
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)

    cleaned_sentences = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 5 and not sent.isupper():
            sent = ' '.join(sent.split())
            if re.search(r'[a-zA-Z]', sent):
                cleaned_sentences.append(sent)

    return cleaned_sentences

def main():
    content_dir = Path('/Users/athatipamula/personal/dutch/finalprep/content_text')
    all_sentences = []

    # Get all .txt files sorted
    txt_files = sorted(content_dir.glob('*.txt'))

    print(f"Processing {len(txt_files)} text files...")

    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()

            sentences = extract_sentences(text)

            for sent in sentences:
                all_sentences.append({
                    'id': len(all_sentences) + 1,
                    'sentence': sent,
                    'source_file': txt_file.name,
                    'tags': ''
                })

        except Exception as e:
            print(f"Error processing {txt_file.name}: {e}")

    print(f"Total sentences: {len(all_sentences)}")

    # Write to CSV
    output_file = Path('/Users/athatipamula/personal/dutch/finalprep/sentences_for_tagging.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'sentence', 'tags'])
        writer.writeheader()
        for row in all_sentences:
            writer.writerow({
                'id': row['id'],
                'sentence': row['sentence'],
                'tags': row['tags']
            })

    print(f"\n✅ CSV generated: {output_file}")
    print(f"   Columns: id, sentence, tags")
    print(f"   Ready for external tagging")

if __name__ == '__main__':
    main()
