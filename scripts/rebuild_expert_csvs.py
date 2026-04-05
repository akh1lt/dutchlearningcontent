#!/usr/bin/env python3
"""Rebuild expert CSVs with comprehensive pattern detection"""

import re
import csv
from collections import Counter

# ============= SENTENCE PATTERNS =============
HIGH_VALUE_PATTERNS = {
    'questions': ['Hoe', 'Wat', 'Waar', 'Wanneer', 'Waarom', 'Wie', 'Hoeveel', 'Welke', 'Hoelang'],
    'modals': ['moet', 'moeten', 'kan', 'kunnen', 'mag', 'mogen', 'wil', 'willen', 'zou', 'zouden'],
    'time_appointments': ['morgen', 'vandaag', 'gisteren', 'volgende', 'vorige', 'binnenkort', 'straks'],
    'reasoning': ['omdat', 'want', 'dus', 'daarom', 'zodat', 'als', 'wanneer', 'hoewel'],
    'opinions': ['vind', 'vindt', 'denk', 'denkt', 'lijkt', 'volgens', 'eigenlijk'],
    'er_constructions': ['er zijn', 'er is', 'er was', 'er waren', 'er zit', 'er staat', 'er ligt', 'er komt'],
    'discourse_markers': ['toch', 'eigenlijk', 'namelijk', 'gewoon', 'misschien', 'volgens mij'],
    'comparisons': ['liever', 'beter', 'meer', 'minder', 'dan', 'als'],
    'negations': ['niet', 'geen', 'nooit', 'niemand'],
}

# ============= VOCABULARY CATEGORIES =============
COMPLEX_CATEGORIES = {
    'healthcare': [
        'dokter', 'ziekenhuis', 'apotheek', 'huisarts', 'tandarts', 'zorgverzekering',
        'medicijn', 'recept', 'afspraak', 'pijn', 'ziek', 'gezond', 'verpleegkundige'
    ],
    'housing_government': [
        'huur', 'huren', 'verhuren', 'hypotheek', 'contract', 'gemeente', 'inschrijven',
        'woning', 'appartement', 'buurman', 'buurvrouw', 'verhuis', 'verhuizen',
        'belasting', 'DigiD', 'paspoort', 'verblijfsvergunning'
    ],
    'work_education': [
        'solliciteren', 'werkgever', 'werknemer', 'salaris', 'diploma', 'studie', 'cursus',
        'opleiding', 'stage', 'collega', 'vergadering', 'contract', 'pensioen'
    ],
    'transport': [
        'openbaar vervoer', 'rijbewijs', 'rijden', 'trein', 'tram', 'metro', 'fiets', 'fietsen',
        'parkeren', 'station', 'halte', 'vertraging', 'overstappen'
    ],
    'money_shopping': [
        'betalen', 'geld', 'pinnen', 'contant', 'korting', 'aanbieding', 'bon', 'kassa',
        'duur', 'goedkoop', 'prijs', 'kosten', 'gratis'
    ],
    'time_frequency': [
        'gisteren', 'vandaag', 'morgen', 'overmorgen', 'eergisteren', 'binnenkort',
        'straks', 'later', 'vaak', 'soms', 'nooit', 'altijd', 'meestal'
    ],
    'complex_verbs': [
        'verhuren', 'huren', 'veranderen', 'vergeten', 'ontmoeten', 'verhuizen',
        'inschrijven', 'aanmelden', 'opruimen', 'schoonmaken', 'bellen', 'bereiken',
        'invullen', 'versturen', 'ontvangen', 'betalen', 'bestellen'
    ],
    'confusing_pairs': [
        'huren', 'verhuren', 'lenen', 'leren', 'als', 'wanneer', 'omdat', 'doordat',
        'naar', 'aan', 'op', 'in', 'veel', 'veel', 'erg', 'heel'
    ],
    'compounds': [
        'zorgverzekering', 'rijbewijs', 'openbaar vervoer', 'huisarts', 'tandarts',
        'supermarkt', 'buurman', 'buurvrouw', 'basisschool', 'middelbare school'
    ]
}

def load_vocabulary():
    """Load all vocabulary from multiple sources"""
    vocab = {}

    # Read COMPREHENSIVE_REFERENCE_FINAL.md
    try:
        with open('COMPREHENSIVE_REFERENCE_FINAL.md', 'r', encoding='utf-8') as f:
            content = f.read()
            # Pattern: - dutch, article = english OR - dutch = english
            pattern = r'^-\s+([^,=\n]+?)(?:,\s*(de|het))?\s*=\s*([^\n]+)'
            matches = re.findall(pattern, content, re.MULTILINE)
            for dutch, article, english in matches:
                dutch = dutch.strip()
                english = english.strip().rstrip('.,;')
                vocab[dutch] = {
                    'english': english,
                    'article': article if article else ''
                }
    except FileNotFoundError:
        pass

    # Read additionalvocab.md
    try:
        with open('additionalvocab.md', 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for lines with dutch - english or dutch (article) - english
            pattern = r'^[•\-\*]?\s*([^\(\n]+?)(?:\s*\((de|het)\))?\s*[-–]\s*([^\n]+)'
            matches = re.findall(pattern, content, re.MULTILINE)
            for dutch, article, english in matches:
                dutch = dutch.strip()
                english = english.strip().rstrip('.,;')
                if dutch not in vocab:
                    vocab[dutch] = {
                        'english': english,
                        'article': article if article else ''
                    }
    except FileNotFoundError:
        pass

    return vocab

def is_complex_word(dutch, english):
    """Check if word is complex enough"""
    # Skip basic words
    basic_words = {
        'je', 'ik', 'jij', 'hij', 'zij', 'we', 'jullie', 'ze',
        'is', 'ben', 'bent', 'zijn', 'was', 'waren',
        'heb', 'heeft', 'hebben', 'had', 'hadden',
        'en', 'of', 'maar', 'want', 'dan',
        'een', 'de', 'het', 'deze', 'die',
        'ja', 'nee', 'niet', 'geen',
        'in', 'op', 'aan', 'bij', 'met', 'voor', 'door', 'van', 'naar', 'uit',
        'wat', 'waar', 'wie', 'hoe', 'dat', 'dit',
        'veel', 'goed', 'leuk', 'mooi', 'groot', 'klein'
    }

    if dutch.lower() in basic_words:
        return False

    # Skip single letters and very short words
    if len(dutch) <= 2:
        return False

    # Include if in any complex category
    for category, words in COMPLEX_CATEGORIES.items():
        if dutch.lower() in [w.lower() for w in words]:
            return True

    # Include longer words (likely compounds or specific terms)
    if len(dutch) >= 8:
        return True

    # Include medical/government/work terms
    keywords = ['zorg', 'gemeente', 'werk', 'school', 'rijbewijs', 'vergunning', 'belasting']
    if any(kw in dutch.lower() for kw in keywords):
        return True

    return True  # Default to including

def score_sentence(sentence):
    """Score sentence based on learning value"""
    score = 0
    sentence_lower = sentence.lower()

    for pattern_type, patterns in HIGH_VALUE_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in sentence_lower:
                # Weight different patterns
                if pattern_type == 'questions':
                    score += 3
                elif pattern_type == 'modals':
                    score += 2
                elif pattern_type == 'er_constructions':
                    score += 3  # High priority
                elif pattern_type == 'discourse_markers':
                    score += 3  # High priority
                elif pattern_type == 'reasoning':
                    score += 2
                elif pattern_type == 'comparisons':
                    score += 2
                else:
                    score += 1

    # Bonus for sentence length (more context)
    word_count = len(sentence.split())
    if 5 <= word_count <= 15:
        score += 1

    # Bonus for question marks
    if '?' in sentence:
        score += 2

    return score

def load_tagged_sentences():
    """Load pre-scored sentences from tagged_sentences/sentences_tagged_v2.csv"""
    try:
        with open('tagged_sentences/sentences_tagged_v2.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sentences = []
            for row in reader:
                sentences.append({
                    'sentence': row['sentence'],
                    'tags': row['tags']
                })
            return sentences
    except FileNotFoundError:
        print("⚠️  Warning: tagged_sentences/sentences_tagged_v2.csv not found")
        return []

def score_sentence_from_tags(tags):
    """Score sentence based on comprehensive tags"""
    score = 0
    tags_lower = tags.lower()

    # High-value patterns
    if 'wh-question' in tags_lower or 'yes-no-question' in tags_lower:
        score += 3
    if 'modal' in tags_lower:
        score += 2 * tags_lower.count('modal')  # Count multiple modals
    if 'negation' in tags_lower:
        score += 2
    if 'subordinate-clause' in tags_lower:
        score += 2
    if 'separable-verb' in tags_lower:
        score += 1
    if 'perfectum' in tags_lower:
        score += 2  # Exam essential
    if 'formal-register-u' in tags_lower:
        score += 1  # Official contexts

    # Exam-relevant topics
    exam_topics = ['health', 'education', 'finance-admin', 'daily-life']
    for topic in exam_topics:
        if topic in tags_lower:
            score += 1

    return score

def extract_sentences_from_md(file_path):
    """Extract all dialogue sentences (fallback if tagged CSV not available)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    dialogue_pattern = r'^- [AB]: (.+)$'
    sentences = re.findall(dialogue_pattern, content, re.MULTILINE)

    return [s.strip() for s in sentences if s.strip()]

def create_expert_vocab_csv(vocab, output_file):
    """Create expert vocabulary CSV"""
    complex_vocab = []

    for dutch, data in vocab.items():
        if is_complex_word(dutch, data['english']):
            complex_vocab.append({
                'dutch': dutch,
                'english': data['english'],
                'article': data['article']
            })

    # Sort by length (longer words often more complex)
    complex_vocab.sort(key=lambda x: len(x['dutch']), reverse=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['dutch', 'english', 'article'])
        writer.writeheader()
        writer.writerows(complex_vocab)

    print(f"✅ Created {output_file} with {len(complex_vocab)} complex words")
    return len(complex_vocab)

def create_expert_sentences_csv(output_file):
    """Create expert sentences CSV using pre-tagged sentences"""
    # Try to load tagged sentences first
    tagged_sentences = load_tagged_sentences()

    if tagged_sentences:
        print(f"  Using {len(tagged_sentences)} pre-tagged sentences")
        # Score and sort
        scored = [(s['sentence'], score_sentence_from_tags(s['tags'])) for s in tagged_sentences]
        scored.sort(key=lambda x: x[1], reverse=True)

        # Filter sentences with score > 0
        high_value = [s for s, score in scored if score > 0]
    else:
        # Fallback to pattern-based scoring
        print("  Falling back to pattern-based scoring")
        sentences = extract_sentences_from_md('extracted_texts.md')
        scored = [(s, score_sentence(s)) for s in sentences]
        high_value = [s for s, score in scored if score > 0]
        high_value.sort(key=lambda s: score_sentence(s), reverse=True)

    # Remove exact duplicates
    seen = set()
    unique_sentences = []
    for s in high_value:
        s_norm = s.lower().strip()
        if s_norm not in seen:
            seen.add(s_norm)
            unique_sentences.append(s)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['dutch'])
        for s in unique_sentences:
            writer.writerow([s])

    print(f"✅ Created {output_file} with {len(unique_sentences)} high-value sentences")

    # Print top 10 with scores
    print("\n📊 Top 10 sentences by learning value:")
    for s in unique_sentences[:10]:
        if tagged_sentences:
            # Find score from tags
            tag_data = next((t for t in tagged_sentences if t['sentence'] == s), None)
            score = score_sentence_from_tags(tag_data['tags']) if tag_data else 0
        else:
            score = score_sentence(s)
        print(f"  [{score}] {s[:80]}{'...' if len(s) > 80 else ''}")

    return len(unique_sentences)

def analyze_coverage():
    """Analyze what patterns are covered"""
    with open('sentences_expert.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sentences = [row['dutch'] for row in reader]

    print("\n📈 Pattern coverage analysis:")
    for pattern_type, patterns in HIGH_VALUE_PATTERNS.items():
        count = sum(1 for s in sentences if any(p.lower() in s.lower() for p in patterns))
        print(f"  {pattern_type}: {count} sentences")

if __name__ == '__main__':
    print("🔧 Rebuilding expert CSVs with comprehensive patterns...\n")

    # Load vocabulary
    print("📚 Loading vocabulary...")
    vocab = load_vocabulary()
    print(f"  Found {len(vocab)} total words")

    # Create expert vocabulary CSV
    vocab_count = create_expert_vocab_csv(vocab, 'vocabulary_complex_expert.csv')

    # Create expert sentences CSV (uses pre-tagged sentences if available)
    print("\n📝 Processing sentences...")
    sent_count = create_expert_sentences_csv('sentences_expert.csv')

    # Analyze coverage
    analyze_coverage()

    print(f"\n✅ Done! {vocab_count} words + {sent_count} sentences ready for LLM prompt")
