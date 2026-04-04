# Prompt for External LLM Tagging

## Task
Tag Dutch A1-A2 sentences with linguistic features for pattern clustering. Focus on CORE STRUCTURAL features only.

## Taxonomy (Use ONLY these tags)

### 1. Sentence Type (pick ONE)
- `Declarative` - Statement
- `Question-YN` - Yes/no question
- `Question-Wh` - Wh-question (wie, wat, waar, wanneer, hoe, waarom)
- `Imperative` - Command
- `Exclamative` - Exclamation/fragment

### 2. Verb Pattern (pick ONE primary, can add secondary)
- `Simple-Present` - Ik werk, Hij woont
- `Simple-Past` - Ik werkte, Hij was
- `Perfect` - Ik heb gewerkt, Hij is gegaan
- `Modal+Inf` - Ik kan zwemmen, Je moet werken (kunnen, mogen, moeten, willen, zullen)
- `Gaan+Inf` - Ik ga werken (near future)
- `Te-Inf` - Om te werken, Het is moeilijk te doen
- `Aan-het+Inf` - Ik ben aan het werken (progressive)

### 3. Word Order (pick ONE)
- `V2` - Verb in second position (standard main clause)
- `V1` - Verb first (questions, imperatives)
- `V-final` - Verb at end (subordinate clauses)

### 4. Key Features (pick ALL that apply)
- `Negation-niet` - Sentence has "niet"
- `Negation-geen` - Sentence has "geen"
- `Negation-never` - nooit, niemand, niets
- `Separable-Verb` - Has separable verb (opbellen, meegaan, etc.)
- `Subordinate` - Has subordinate clause (omdat, als, dat, etc.)
- `ER-construction` - Has "er" (er is, er zijn, ik ga ernaar, etc.)
- `Modal-Particle` - Has maar, toch, wel, even, hoor, eigenlijk
- `Reflexive` - Has reflexive pronoun (zich, me, je)
- `Passive` - Passive construction (worden + participle)
- `Relative-Clause` - Has relative clause (die, dat, waar)

## Output Format

Comma-separated tags, no spaces after commas. Order: Type, Verb Pattern, Word Order, Features

Example:
```
Declarative,Simple-Present,V2,Negation-geen
Question-YN,Modal+Inf,V1
Declarative,Perfect,V2,Subordinate,V-final
```

## Examples

**Sentence:** Ik heb geen tv
**Tags:** `Declarative,Simple-Present,V2,Negation-geen`

**Sentence:** Kun je mij helpen?
**Tags:** `Question-YN,Modal+Inf,V1`

**Sentence:** Ik weet dat hij morgen komt
**Tags:** `Declarative,Simple-Present,V2,Subordinate,V-final`

**Sentence:** Ze is aan het werken
**Tags:** `Declarative,Aan-het+Inf,V2`

**Sentence:** Ik bel je straks op
**Tags:** `Declarative,Simple-Present,V2,Separable-Verb`

**Sentence:** Er zijn veel mensen hier
**Tags:** `Declarative,Simple-Present,V2,ER-construction`

**Sentence:** Kom maar binnen
**Tags:** `Imperative,Simple-Present,V1,Modal-Particle`

**Sentence:** Ik heb het niet gezien
**Tags:** `Declarative,Perfect,V2,Negation-niet`

## Instructions

1. Tag each sentence with 3-7 tags total
2. Always include: Sentence Type + Verb Pattern + Word Order
3. Add Key Features only if present
4. If multiple verb patterns (e.g., modal + perfect), list both: `Modal+Inf,Perfect`
5. Don't overthink - focus on obvious structural features
6. Output ONLY the tags, comma-separated, no explanations

## CSV Format

Your CSV should have columns: `id,sentence,tags`

Fill the `tags` column with the comma-separated tags for each sentence.
