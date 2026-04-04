#!/usr/bin/env python3
"""
Extract individual sentences from all content_text files.
"""

import os
import re
from pathlib import Path

def extract_sentences(text):
    """Extract sentences from text, handling Dutch punctuation."""
    # Remove line numbers (e.g., "1→", "35→")
    text = re.sub(r'^\s*\d+→', '', text, flags=re.MULTILINE)

    # Split on sentence endings: . ! ?
    # But preserve decimal numbers and common abbreviations
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)

    cleaned_sentences = []
    for sent in sentences:
        sent = sent.strip()
        # Skip empty, very short (< 5 chars), or header-like lines
        if len(sent) > 5 and not sent.isupper():
            # Remove extra whitespace
            sent = ' '.join(sent.split())
            # Only keep if it has actual content (not just punctuation/numbers)
            if re.search(r'[a-zA-Z]', sent):
                cleaned_sentences.append(sent)

    return cleaned_sentences

def main():
    content_dir = Path('/Users/athatipamula/personal/dutch/finalprep/content_text')
    all_sentences = []

    # Get all .txt files sorted
    txt_files = sorted(content_dir.glob('*.txt'))

    print(f"Found {len(txt_files)} text files")

    for txt_file in txt_files:
        print(f"Processing {txt_file.name}...")
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()

            sentences = extract_sentences(text)

            # Add source file info to each sentence
            for sent in sentences:
                all_sentences.append({
                    'text': sent,
                    'source': txt_file.name
                })

            print(f"  Extracted {len(sentences)} sentences")

        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTotal sentences extracted: {len(all_sentences)}")

    # Generate HTML
    html = """<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Sentences - Dutch A2</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .stats {
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sentence {
            background: white;
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 6px;
            border-left: 4px solid #3498db;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s;
        }
        .sentence:hover {
            box-shadow: 0 3px 8px rgba(0,0,0,0.15);
            transform: translateX(2px);
        }
        .sentence-text {
            font-size: 16px;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .source {
            font-size: 12px;
            color: #7f8c8d;
            font-style: italic;
        }
        .sentence-num {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 8px;
        }
        .filter-info {
            background: #e8f4f8;
            padding: 10px;
            border-radius: 5px;
            margin: 15px 0;
            font-size: 14px;
            color: #34495e;
        }
    </style>
</head>
<body>
    <h1>📝 Extracted Sentences - Dutch A2 Course Materials</h1>

    <div class="stats">
        <strong>Total Sentences:</strong> {total_sentences}<br>
        <strong>Source Files:</strong> {total_files}<br>
        <strong>Extraction Date:</strong> {date}
    </div>

    <div class="filter-info">
        ℹ️ <strong>Quality Check:</strong> Review sentences for accuracy. Check if:
        <ul style="margin: 5px 0;">
            <li>Sentences are complete (not cut off)</li>
            <li>No merged sentences</li>
            <li>OCR errors are minimal</li>
            <li>Dialogue lines are properly separated</li>
        </ul>
    </div>
"""

    # Add sentences
    for idx, sent_data in enumerate(all_sentences, 1):
        html += f"""
    <div class="sentence">
        <div class="sentence-text">
            <span class="sentence-num">{idx}</span>
            {sent_data['text']}
        </div>
    </div>
"""

    html += """
</body>
</html>
"""

    # Save HTML
    from datetime import datetime
    html = html.replace('{total_sentences}', str(len(all_sentences)))
    html = html.replace('{total_files}', str(len(txt_files)))
    html = html.replace('{date}', datetime.now().strftime('%Y-%m-%d %H:%M'))

    output_file = Path('/Users/athatipamula/personal/dutch/finalprep/extracted_sentences_review.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ HTML generated: {output_file}")
    print(f"   Open in browser to review {len(all_sentences)} sentences")

if __name__ == '__main__':
    main()
