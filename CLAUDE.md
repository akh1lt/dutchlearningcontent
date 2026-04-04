# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Dutch A2 exam preparation repository for inburgering (civic integration). The project consolidates study materials from a Link+ Dutch language course into high-ROI study notes for maximum learning efficiency.

**Project Goal**: Create condensed, bilingual (Dutch-English) study materials that extract the most frequently used vocabulary and sentence patterns (80/20 principle) for daily Dutch communication and A2 exam success.

## Repository Structure

### Core Study Materials
- `MUST_DO_HIGH_ROI_NOTES_FINAL.md` - Primary condensed study guide (~280 essential words, high-frequency patterns)
- `COMPREHENSIVE_REFERENCE_FINAL.md` - Complete reference with all ~700 vocabulary words, 30 dialogues, full grammar
- `exam.md` - Exam structure and requirements (4 tests: vocabulary, listening, reading, writing)
- `additionalvocab.md` - High-priority vocabulary list from the course (vocab_level_1)
- `grammer.md` - Grammar scope for the course

### Source Materials
- `content/` - Original study materials as PNG images (image_01.png through image_15.png)
- `content_text/` - Extracted text from content images (image_01.txt through image_15.txt)
- `extracted_texts.md` - Consolidated extracted text from all images

### Analysis & Working Files
- `plan.md` - Original project plan and objectives
- `ANALYSIS_BATCH_01.md` - Vocabulary and pattern frequency analysis
- `DATA_ANALYSIS_BATCH_01.md` - Statistical analysis of extracted content
- `INSTRUCTOR_ANALYSIS_BATCH_01.md` - Instructor-focused analysis
- `INSTRUCTOR_INTERPRETATION_BATCH_01.md` - Additional interpretation notes
- `COMPLETE_DATA_ANALYSIS.md` - Comprehensive data analysis results
- `analysis.json` - Structured analysis data

### Generated HTML Files
- `high_roi_notes.html` - HTML version of condensed study guide
- `comprehensive_reference.html` - HTML version of complete reference
- `high_roi_cheatsheet.html` - Quick reference cheatsheet
- `data_analysis.html` - Analysis visualization

## Key Principles

### Content Philosophy
1. **80/20 Optimization**: Focus on high-frequency vocabulary and patterns that unlock the most communication capability
2. **Bilingual Format**: All content should be Dutch with English explanations/translations
3. **Exam-Oriented**: Prioritize content that appears in A2 exam contexts (especially writing test which has strictest grammar requirements)
4. **Grammar Balance**: Grammar should be ~25-30% of focus, not the center - practical usage patterns matter more
5. **Real-World Application**: Target daily life proficiency and inburgering exam success, not just course completion

### Content Hierarchy
1. **Tier 1 Priority**: Repeating sentence patterns and top-frequency vocabulary across multiple texts
2. **Tier 2 Priority**: Common conversational chunks and question forms
3. **Tier 3 Priority**: Grammar rules (learned through patterns, not memorization)
4. **Lower Priority**: Rare vocabulary or complex grammar structures

## Exam Context

**Four Tests** (from exam.md):
1. Vocabulary: 20 questions, 15 min, pass = 12/20
2. Listening: 20 questions, 20 min, pass = 14/20
3. Reading: 20 questions, 45 min, pass = 14/20
4. Writing: 5 sentences + short text, 30 min, pass = 15/22
   - Grammar mistakes cost 1 point per sentence in the 5-sentence section
   - Content (1pt) + Grammar (1pt) per sentence
   - de/het articles don't count as errors

**Critical**: Writing test has the highest failure rate due to grammar penalties. Study materials must emphasize correct sentence structures.

## Working with This Repository

### When Adding/Updating Vocabulary
- Always include Dutch-English bilingual format
- Mark frequency/priority (Tier 1/2/3 or vocab_level_1/2)
- Add example sentences in context
- Group by theme/topic when possible

### When Analyzing Text Content
- Look for repeating patterns across multiple source texts
- Rank by frequency of appearance
- Extract complete sentence patterns, not just isolated words
- Note which themes appear most often (indicates exam relevance)

### When Creating Study Materials
- Generate both condensed (high-ROI) and comprehensive versions
- HTML exports should be clean, printable, and mobile-friendly
- Cross-reference between must-do notes and comprehensive reference
- Include "Why this matters" context for learners

### Python Usage
Python scripts are permitted (configured in .claude/settings.local.json) for:
- Text extraction from images
- Statistical analysis of vocabulary frequency
- Pattern detection across multiple texts
- JSON data manipulation for analysis.json

## Custom Agent

The repository includes `dutch-a2-learning-specialist` agent for:
- Dutch language learning at A2 level
- Inburgering exam preparation advice
- Practical vocabulary for daily life in the Netherlands
- Pattern-based grammar understanding (not rule memorization)
- High-impact vs low-value vocabulary guidance

Invoke when working on Dutch language content, exam preparation strategies, or vocabulary prioritization decisions.
