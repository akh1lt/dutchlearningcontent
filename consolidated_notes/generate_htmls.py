#!/usr/bin/env python3
"""
Generate consolidated HTML study materials for Dutch A2 exam prep.
Enriches existing specialist notes with new sentence analysis data.
"""

import json
import markdown
from pathlib import Path

# Load data
with open('sentence_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('../MUST_DO_HIGH_ROI_NOTES_FINAL.md', 'r', encoding='utf-8') as f:
    high_roi_md = f.read()

with open('../COMPREHENSIVE_REFERENCE_FINAL.md', 'r', encoding='utf-8') as f:
    comprehensive_md = f.read()

# CSS for all pages
CSS = """
<style>
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
    background: #f9f9f9;
}
.container {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
h1 { color: #2c5282; border-bottom: 3px solid #4299e1; padding-bottom: 10px; }
h2 { color: #2d3748; margin-top: 30px; border-left: 4px solid #4299e1; padding-left: 12px; }
h3 { color: #4a5568; }
.nav {
    background: #2c5282;
    color: white;
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 25px;
}
.nav a {
    color: #90cdf4;
    text-decoration: none;
    margin-right: 15px;
    padding: 5px 10px;
    border-radius: 4px;
    transition: background 0.2s;
}
.nav a:hover { background: rgba(255,255,255,0.1); }
.sentence {
    background: #f7fafc;
    border-left: 4px solid #48bb78;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
}
.sentence .dutch { font-size: 1.2em; font-weight: 600; color: #2d3748; margin-bottom: 8px; }
.sentence .score { color: #e53e3e; font-weight: bold; font-size: 0.9em; }
.sentence .value { color: #38a169; font-size: 0.95em; margin: 8px 0; }
.sentence .value li { margin: 4px 0; }
.sentence .tags {
    font-size: 0.85em;
    color: #718096;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #e2e8f0;
}
.pattern-group {
    background: #edf2f7;
    padding: 20px;
    margin: 20px 0;
    border-radius: 6px;
}
.pattern-group h3 { color: #2c5282; margin-top: 0; }
.pattern-count {
    background: #4299e1;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.9em;
    margin-left: 10px;
}
.vocab-tier {
    background: #fff5f5;
    border-left: 4px solid #fc8181;
    padding: 15px;
    margin: 15px 0;
}
.study-tip {
    background: #fef5e7;
    border-left: 4px solid #f39c12;
    padding: 15px;
    margin: 20px 0;
    border-radius: 4px;
}
.study-tip strong { color: #d68910; }
code {
    background: #2d3748;
    color: #68d391;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
}
@media print {
    body { background: white; }
    .container { box-shadow: none; }
    .nav { display: none; }
}
@media (max-width: 600px) {
    body { padding: 10px; }
    .container { padding: 15px; }
    .sentence .dutch { font-size: 1.1em; }
}
</style>
"""

def generate_nav():
    return """
    <div class="nav">
        <strong>📚 Dutch A2 Study Materials</strong><br>
        <a href="index.html">🏠 Home</a>
        <a href="high_roi_notes_enriched.html">⚡ High ROI</a>
        <a href="mid_roi_notes.html">📈 Mid ROI</a>
        <a href="comprehensive_reference.html">📖 Comprehensive</a>
        <a href="sentence_practice_drills.html">💪 Drills</a>
    </div>
    """

def sentence_html(sent, show_translation=True, compact=False):
    """Generate HTML for a single sentence"""
    if compact:
        return f"""
        <div class="sentence">
            <div class="dutch">{sent['sentence']}</div>
            <div class="score">ROI Score: {sent['score']}</div>
        </div>
        """

    value_items = sent['learning_value'].split('; ')
    value_html = '<ul class="value">' + ''.join(f'<li>{item}</li>' for item in value_items[:5]) + '</ul>'

    return f"""
    <div class="sentence">
        <div class="dutch">{sent['sentence']}</div>
        <div class="score">ROI Score: {sent['score']} | ID: {sent['id']}</div>
        <strong>⭐ Learning Value:</strong>
        {value_html}
        <div class="tags">🏷️ {sent['tags'][:200]}{'...' if len(sent['tags']) > 200 else ''}</div>
    </div>
    """

# 1. INDEX.HTML - Navigation hub
print("Generating index.html...")
index_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dutch A2 Exam Preparation - Study Materials</title>
    {CSS}
</head>
<body>
<div class="container">
    <h1>🇳🇱 Dutch A2 Exam Preparation</h1>
    <p><strong>Complete study materials with AI-ranked sentences and expert-curated content</strong></p>

    <div class="study-tip">
        <strong>📋 Recommended Study Path:</strong><br>
        1. Start with <strong>High ROI Notes</strong> (2-3 weeks intensive)<br>
        2. Practice with <strong>Sentence Drills</strong> daily<br>
        3. Expand to <strong>Mid ROI Notes</strong> (4-6 weeks comprehensive)<br>
        4. Reference <strong>Comprehensive Guide</strong> as needed
    </div>

    <h2>Study Materials</h2>

    <div class="pattern-group">
        <h3>⚡ <a href="high_roi_notes_enriched.html">High ROI Notes (Enriched)</a></h3>
        <p><strong>Target:</strong> Pass exam with minimum time (2-3 weeks intensive prep)</p>
        <p><strong>Content:</strong></p>
        <ul>
            <li>280 essential vocabulary words (Tier 1 & 2)</li>
            <li>Core grammar (present, perfect, subordinate clauses)</li>
            <li><strong>NEW:</strong> Top 50 example sentences with learning value explanations</li>
            <li>10-day study plan</li>
        </ul>
    </div>

    <div class="pattern-group">
        <h3>📈 <a href="mid_roi_notes.html">Mid ROI Notes</a></h3>
        <p><strong>Target:</strong> Confident daily communication (4-6 weeks)</p>
        <p><strong>Content:</strong></p>
        <ul>
            <li>400-500 vocabulary words (expanded from top 100 sentences)</li>
            <li>Top 100 sentences organized by pattern</li>
            <li>Register distinction (formal U vs informal je)</li>
            <li>Pattern frequency data from course materials</li>
            <li>Extended grammar coverage</li>
        </ul>
    </div>

    <div class="pattern-group">
        <h3>📖 <a href="comprehensive_reference.html">Comprehensive Reference</a></h3>
        <p><strong>Target:</strong> Complete coverage for thorough mastery</p>
        <p><strong>Content:</strong></p>
        <ul>
            <li>700+ vocabulary words</li>
            <li>30 complete dialogues</li>
            <li>Full grammar reference</li>
            <li>All course materials consolidated</li>
        </ul>
    </div>

    <div class="pattern-group">
        <h3>💪 <a href="sentence_practice_drills.html">Sentence Practice Drills</a></h3>
        <p><strong>Target:</strong> Daily practice and memorization</p>
        <p><strong>Content:</strong></p>
        <ul>
            <li>Top 100 sentences ranked by learning ROI</li>
            <li>Organized by linguistic patterns</li>
            <li>Quick reference for daily drilling</li>
        </ul>
    </div>

    <h2>About This Material</h2>
    <p>These study materials combine:</p>
    <ul>
        <li><strong>Expert curation:</strong> Dutch A2 specialist-created vocabulary and grammar</li>
        <li><strong>AI analysis:</strong> 1,265 sentences analyzed and ranked by 15-factor ROI scoring</li>
        <li><strong>Pattern frequency:</strong> Based on actual Link+ course material usage</li>
        <li><strong>Exam focus:</strong> Optimized for inburgering A2 exam success</li>
    </ul>

    <div class="study-tip">
        <strong>💡 Study Tips:</strong><br>
        • Focus on HIGH ROI materials first (80/20 principle)<br>
        • Practice sentences daily - they demonstrate grammar in context<br>
        • Writing test has highest failure rate - master sentence structure<br>
        • Articles (de/het) don't count as errors in exam, but learn them anyway
    </div>
</div>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("✅ Generated index.html")

# 2. HIGH_ROI_NOTES_ENRICHED.HTML
print("Generating high_roi_notes_enriched.html...")

# Convert markdown to HTML
high_roi_html_content = markdown.markdown(high_roi_md, extensions=['extra', 'nl2br'])

# Add top 50 sentences section
top_50_section = """
<h2 id="top-50-practice">TOP 50 PRACTICE SENTENCES (NEW)</h2>

<div class="study-tip">
    <strong>🎯 How to Use These Sentences:</strong><br>
    These 50 sentences demonstrate the vocabulary and grammar patterns taught above.<br>
    • Each sentence shows which concepts it uses (look for the references)<br>
    • Average ROI score: 103.8 (highest learning value)<br>
    • 74% contain modal verbs, 46% show negation, 32% are questions<br>
    • Practice these daily to reinforce grammar patterns
</div>

"""

for i, sent in enumerate(data['top_50'], 1):
    top_50_section += f"<h3>#{i}</h3>\n" + sentence_html(sent) + "\n"

high_roi_enriched = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High ROI Notes (Enriched) - Dutch A2</title>
    {CSS}
</head>
<body>
<div class="container">
    {generate_nav()}
    {high_roi_html_content}
    <hr style="margin: 40px 0; border: 2px solid #4299e1;">
    {top_50_section}
</div>
</body>
</html>
"""

with open('high_roi_notes_enriched.html', 'w', encoding='utf-8') as f:
    f.write(high_roi_enriched)

print("✅ Generated high_roi_notes_enriched.html")

# 3. SENTENCE_PRACTICE_DRILLS.HTML
print("Generating sentence_practice_drills.html...")

drills_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentence Practice Drills - Dutch A2</title>
    {CSS}
</head>
<body>
<div class="container">
    {generate_nav()}
    <h1>💪 Sentence Practice Drills</h1>
    <p><strong>Top 100 sentences organized by linguistic patterns for daily practice</strong></p>

    <div class="study-tip">
        <strong>Practice Strategy:</strong><br>
        • Read each sentence out loud 5 times<br>
        • Identify the grammar pattern (modal, negation, question form)<br>
        • Try to create similar sentences using the same pattern<br>
        • Focus on one pattern group per day
    </div>
"""

# Organize by patterns
for pattern_name, sentences in sorted(data['patterns'].items(), key=lambda x: len(x[1]), reverse=True):
    drills_html += f"""
    <div class="pattern-group">
        <h2>{pattern_name} <span class="pattern-count">{len(sentences)} sentences</span></h2>
    """
    for sent in sentences[:20]:  # Limit to top 20 per pattern
        drills_html += sentence_html(sent, compact=False)
    drills_html += "</div>\n"

drills_html += """
</div>
</body>
</html>
"""

with open('sentence_practice_drills.html', 'w', encoding='utf-8') as f:
    f.write(drills_html)

print("✅ Generated sentence_practice_drills.html")

# 4. COMPREHENSIVE_REFERENCE.HTML
print("Generating comprehensive_reference.html...")

comprehensive_html_content = markdown.markdown(comprehensive_md, extensions=['extra', 'nl2br'])

comprehensive_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Reference - Dutch A2</title>
    {CSS}
</head>
<body>
<div class="container">
    {generate_nav()}
    {comprehensive_html_content}
</div>
</body>
</html>
"""

with open('comprehensive_reference.html', 'w', encoding='utf-8') as f:
    f.write(comprehensive_html)

print("✅ Generated comprehensive_reference.html")

print("\n✅ HTML generation complete!")
print("   Generated 4 files in consolidated_notes/")
print("   (mid_roi_notes.html will be generated separately due to size)")
