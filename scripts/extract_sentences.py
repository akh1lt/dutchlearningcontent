#!/usr/bin/env python3
"""Extract top 200 sentences from 30 texts with frequency ranking"""

import re
from collections import Counter
import csv

def extract_sentences_from_md(file_path):
    """Extract all dialogue sentences from extracted_texts.md"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all dialogue lines (starting with - A: or - B:)
    dialogue_pattern = r'^- [AB]: (.+)$'
    sentences = re.findall(dialogue_pattern, content, re.MULTILINE)

    # Also extract text numbers for source tracking
    text_pattern = r'## Text (\d+):'
    texts = re.findall(text_pattern, content)

    # Match sentences to source texts (approximate)
    text_blocks = re.split(r'## Text \d+:', content)[1:]  # Skip header

    sentence_data = []
    for idx, block in enumerate(text_blocks):
        text_num = idx + 1
        block_sentences = re.findall(dialogue_pattern, block, re.MULTILINE)
        for sentence in block_sentences:
            sentence_data.append({
                'sentence': sentence.strip(),
                'source_text': f'Text {text_num}',
                'text_num': text_num
            })

    return sentence_data

def normalize_sentence(sentence):
    """Normalize for frequency counting (lowercase, remove punctuation)"""
    return re.sub(r'[^\w\s]', '', sentence.lower())

def rank_sentences_by_frequency(sentence_data):
    """Rank sentences by how similar they are (pattern frequency)"""
    # Count normalized sentences
    sentence_counter = Counter()
    sentence_map = {}  # normalized -> original

    for item in sentence_data:
        norm = normalize_sentence(item['sentence'])
        sentence_counter[norm] += 1
        if norm not in sentence_map:
            sentence_map[norm] = item

    # Rank by frequency
    ranked = []
    for norm_sent, count in sentence_counter.most_common(200):
        original_item = sentence_map[norm_sent]
        ranked.append({
            'dutch_sentence': original_item['sentence'],
            'source_text': original_item['source_text'],
            'frequency_rank': len(ranked) + 1,
            'occurrences': count
        })

    return ranked

def create_csv(sentences, output_file):
    """Create CSV with top 200 sentences"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'dutch_sentence', 'source_text', 'occurrences'])
        writer.writeheader()

        for item in sentences:
            writer.writerow({
                'rank': item['frequency_rank'],
                'dutch_sentence': item['dutch_sentence'],
                'source_text': item['source_text'],
                'occurrences': item['occurrences']
            })

    print(f"✅ Created {output_file} with {len(sentences)} sentences")

if __name__ == '__main__':
    # Extract sentences
    sentence_data = extract_sentences_from_md('extracted_texts.md')
    print(f"📊 Extracted {len(sentence_data)} total sentences from texts")

    # Rank by frequency
    top_sentences = rank_sentences_by_frequency(sentence_data)

    # Create CSV
    create_csv(top_sentences, 'sentences_top200.csv')

    # Show sample
    print("\n📝 Sample of top 10 sentences:")
    for item in top_sentences[:10]:
        print(f"  {item['frequency_rank']}. {item['dutch_sentence']} (occurs {item['occurrences']}x)")
