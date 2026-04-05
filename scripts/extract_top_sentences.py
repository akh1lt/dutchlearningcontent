#!/usr/bin/env python3
"""Extract just the sentences from pre-ranked top_200_sentences.csv"""

import csv

def extract_top_sentences(input_file, output_file):
    """Extract sentences from CSV with proper handling of embedded commas"""
    sentences = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sentences.append(row['sentence'])

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['dutch'])
        for s in sentences:
            writer.writerow([s])

    print(f"✅ Extracted {len(sentences)} sentences from {input_file}")
    print(f"✅ Created {output_file}")

    # Show top 5
    print("\n📊 Top 5 sentences:")
    for i, s in enumerate(sentences[:5], 1):
        print(f"  {i}. {s[:80]}{'...' if len(s) > 80 else ''}")

if __name__ == '__main__':
    extract_top_sentences('tagged_sentences/top_200_sentences.csv', 'sentences_expert.csv')
