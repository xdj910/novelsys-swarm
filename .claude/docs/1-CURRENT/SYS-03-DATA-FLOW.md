# SYS-03-DATA-FLOW - Data Transformation Pipeline
*How 5 JSON Research Files Become 7 Production Documents*

## Data Flow Overview

```
Natural Language Conversation
         ↓
    Trigger Detection
         ↓
    Research Phase (5 JSON files)
         ↓
    Synthesis Phase
         ↓
    7 Production Documents
```

## Stage 1: Natural Language Input

### Input Types
```yaml
Exploratory:
  "I'm thinking about writing a mystery novel"
  "想写个推理小说"

Specific:
  "What's popular in cozy mysteries?"
  "Caribbean setting with environmental themes"

Progressive:
  "Tell me more about the target audience"
  "Let's explore voice options"
```

### Trigger Detection (Main Claude)
```python
# Main Claude processes conversation
detected_triggers = [
    "writing project" -> research-coordinator
    "what's popular" -> trend-analyzer
    "target readers" -> audience-profiler
]
```

## Stage 2: Research Data Collection

### 5 Research JSON Files

#### 1. trend_analysis_[timestamp].json (5-10KB)
```json
{
  "metadata": {
    "timestamp": "20250115_143022",
    "confidence": 0.85,
    "sources": 12
  },
  "market_trends": {
    "growing_genres": ["cozy mystery +45%", "climate fiction +156%"],
    "declining_genres": ["hard sci-fi -12%"],
    "seasonal_patterns": {...}
  },
  "recommendations": [...]
}
```

#### 2. competitor_analysis_[niche]_[timestamp].json (8-15KB)
```json
{
  "market_analysis": {
    "top_competitors": [...],
    "market_gaps": ["no cooking cozy in tropical setting"],
    "success_patterns": [...]
  },
  "differentiation_opportunities": [...]
}
```

#### 3. audience_profile_[timestamp].json (6-12KB)
```json
{
  "demographics": {
    "primary_age": "45-65",
    "gender_distribution": "75% female",
    "education": "70% college+"
  },
  "behaviors": {
    "books_per_year": 14,
    "preferred_length": "60-80k words"
  }
}
```

#### 4. comprehensive_voice_analysis_[timestamp].json (15-25KB)
```json
{
  "voice_profiles": [
    {
      "name": "Island Community Storyteller",
      "samples": [15 examples],
      "patterns": [12 sentence patterns],
      "vocabulary_tiers": {
        "basic": "70%",
        "elevated": "25%",
        "specialized": "5%"
      }
    }
  ]
}
```

#### 5. topic_analysis_[timestamp].json (8-12KB)
```json
{
  "theme_opportunities": [
    {
      "theme": "marine conservation",
      "market_fit": 0.89,
      "complexity": "accessible"
    }
  ],
  "setting_options": [...],
  "plot_structures": [...]
}
```

## Stage 3: Intelligent Synthesis

### Transformation Logic

```python
# bible-generator performs these operations:

def synthesize_research(all_json_data):
    # 1. COMBINATION - Merge related data
    character_framework = merge(
        audience['preferences'] +
        competitor['successful_characters'] +
        voice['personality_traits']
    )

    # 2. DERIVATION - Infer new insights
    series_plan = derive_from(
        trends['series_popularity'] +
        topics['10_theme_opportunities']
    ) -> "10-book series structure"

    # 3. EXPANSION - Elaborate details
    voice_guide = expand(
        voice['15_samples']
        -> detailed_implementation_guide
        -> practice_exercises
        -> troubleshooting_tips
    )

    # 4. SPECIALIZATION - Split by use case
    voice_implementation = split(
        voice_data ->
        [style_guide, consistency_checklist]
    )

    # 5. INFERENCE - Create missing elements
    cultural_guide = infer_from(
        topics['caribbean_setting'] +
        audience['cultural_sensitivity_expectations']
    ) -> comprehensive_cultural_guide
```

## Stage 4: Document Generation

### Output Document Matrix

| Source JSON | → Transformation → | Output Documents |
|------------|-------------------|------------------|
| All 5 JSONs | Comprehensive synthesis | series_bible.yaml |
| voice_analysis | Expansion + Examples | VOICE_STYLE_GUIDE.md |
| voice_analysis | Checklist extraction | VOICE_CONSISTENCY_CHECKLIST.md |
| topics + audience | Cultural inference | CULTURAL_AUTHENTICITY_GUIDE.md |
| topics + settings | Accuracy requirements | ENVIRONMENTAL_ACCURACY_STANDARDS.md |
| trends + topics | Series projection | SERIES_PLAN_10_BOOKS.md |
| audience + competitor | Character design | CHARACTER_DEVELOPMENT_FRAMEWORK.md |

### Document Relationships

```
series_bible.yaml (Master Document)
    ├── References all other documents
    ├── Synthesis confidence scores
    └── Cross-validation points

VOICE_STYLE_GUIDE.md ←→ VOICE_CONSISTENCY_CHECKLIST.md
    (Implementation)         (Validation)

CULTURAL_AUTHENTICITY_GUIDE.md ←→ ENVIRONMENTAL_ACCURACY_STANDARDS.md
    (Cultural context)              (Physical setting)

SERIES_PLAN_10_BOOKS.md ←→ CHARACTER_DEVELOPMENT_FRAMEWORK.md
    (Plot progression)         (Character arcs)
```

## Data Integrity Measures

### Atomic Operations
```python
# Safe write pattern (no corruption)
write_to_temp('.tmp')
atomic_rename('.tmp', 'final.json')
```

### Version Control
```yaml
Files maintain version history:
  - topic_analysis_20250115_143022.json
  - topic_analysis_20250115_161545.json
  - topic_analysis_20250115_182103.json
```

### Validation Checks
```python
# Each stage validates previous
if not valid_json(research_file):
    return error_state

if not complete_coverage(all_research):
    suggest_additional_research()

if not quality_threshold(synthesis):
    request_human_review()
```

## Progressive Enhancement

### Incremental Building
```yaml
Cycle 1:
  trend-analyzer -> initial market understanding

Cycle 2:
  audience-profiler -> refined target

Cycle 3:
  voice-analyzer -> style development

Each cycle builds on previous knowledge
```

### Feedback Integration
```yaml
User: "Voice too formal"
System: Regenerate voice-related documents only
        Preserve other research
```

## File Size Management

### Typical Sizes
```yaml
Research JSONs: 5-25KB each
Output Documents: 8-20KB each
Total Bible Suite: ~100KB

# Well within Claude's context window
# No summarization needed
```

### Chunked Reading (If Needed)
```python
# For large files
chunk_size = 2000  # lines
offset = 0
while offset < total_lines:
    chunk = Read(file, offset, chunk_size)
    process(chunk)
    offset += chunk_size
```

## Quality Metrics

### Coverage Assessment
```yaml
Required Coverage:
  - Market analysis: ✓
  - Audience definition: ✓
  - Voice documentation: ✓
  - Theme research: ✓
  - Competition analysis: ✓

Production Readiness: 86%
```

### Confidence Scoring
```yaml
Each document includes:
  confidence: 0.0-1.0
  source_count: number of research inputs
  gaps_identified: areas needing more research
```

## References
- IMP-01-RESEARCH-SYSTEM.md for complete system
- SYS-02-COMPONENTS.md for agent details
- CLAUDE.md for architecture compliance