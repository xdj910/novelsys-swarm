# SYS-02-COMPONENTS - Research System Components
*7 Components: 1 Coordinator + 6 Agents*

## Component Overview

```
research-coordinator (Planning Layer)
    |
    ├── trend-analyzer
    ├── competitor-scanner
    ├── audience-profiler
    ├── voice-analyzer
    ├── topic-explorer
    └── bible-generator (Synthesis)
```

## 1. research-coordinator

### Purpose
Orchestrates progressive research workflow by analyzing context and suggesting next steps

### Key Features
- **PROACTIVE**: Triggers on "writing project", "story ideas", "book planning"
- **Progressive**: Suggests 1-2 next steps, not all at once
- **No Task Tool**: Returns JSON plans only (prevents recursion)

### Output Format
```json
{
  "exploration_state": {
    "current_position": "initial_interest",
    "completed_steps": [],
    "user_signals": {}
  },
  "next_step_suggestions": [
    {
      "agent": "trend-analyzer",
      "rationale": "Understanding market trends helps validate your interest",
      "effort_level": "15-20 minutes"
    }
  ]
}
```

## 2. trend-analyzer

### Purpose
Research market trends and genre patterns

### Triggers
- "market trends", "what's popular", "business opportunities"

### Output
`knowledge_base/trends/trend_analysis_[timestamp].json`

### Key Data
- Market size and growth
- Genre trends
- Seasonal patterns
- Platform preferences

## 3. competitor-scanner

### Purpose
Analyze competition and identify market gaps

### Triggers
- "competitors", "competition", "market saturation"

### Output
`knowledge_base/competitors/[niche]_[timestamp].json`

### Key Data
- Top competitors analysis
- Market gaps
- Differentiation opportunities
- Success patterns

## 4. audience-profiler

### Purpose
Research target reader demographics and preferences

### Triggers
- "readers", "audience", "target market", "who will read"

### Output
`knowledge_base/audience/audience_profile_[timestamp].json`

### Key Data
- Demographics (age, gender, education)
- Reading behaviors
- Content preferences
- Discovery channels
- Purchase patterns

## 5. voice-analyzer

### Purpose
Comprehensive writing style analysis and documentation

### Triggers
- Writing style discussions, voice exploration

### Output
`knowledge_base/voice/comprehensive_voice_analysis_[timestamp].json`

### Key Features
- **15 samples per voice**
- **12 sentence patterns**
- **3-tier vocabulary system**
- Complete implementation guide

### Voice Framework (3-3-3+1)
```yaml
Core Elements:
  - Perspective (1st, 3rd limited, 3rd omniscient)
  - Tone (cool, warm, hot)
  - Pacing (slow, medium, fast)

Style Markers:
  - Sentence rhythm
  - Vocabulary choices
  - Descriptive density

Genre Adaptations:
  - Mystery conventions
  - Romance expectations
  - Thriller requirements

+1 Cultural Layer:
  - Regional authenticity
  - Code-switching patterns
  - Cultural sensitivity
```

## 6. topic-explorer

### Purpose
Research themes, settings, and story opportunities

### Triggers
- "story ideas", "themes", "what to write about", "plot concepts"

### Output
`knowledge_base/topics/topic_analysis_[timestamp].json`

### Key Data
- High-opportunity themes
- Setting possibilities
- Plot structures
- Conflict types
- Environmental elements

## 7. bible-generator

### Purpose
Synthesize all research into comprehensive production documents

### Input
All 5 research JSON files

### Output (7 Documents)

#### 1. series_bible.yaml (15-20KB)
- Comprehensive project bible
- All synthesized decisions
- Confidence scores
- Cross-references

#### 2. VOICE_STYLE_GUIDE.md (12-15KB)
- Core voice identity
- Sentence patterns with examples
- Vocabulary management system
- Dialogue guidelines

#### 3. VOICE_CONSISTENCY_CHECKLIST.md (8-10KB)
- Pre-writing preparation
- During writing checks
- Chapter completion review
- Series consistency tracking

#### 4. CULTURAL_AUTHENTICITY_GUIDE.md (12-15KB)
- Cultural elements and sensitivity
- Code-switching patterns
- Community dynamics
- Authenticity standards

#### 5. ENVIRONMENTAL_ACCURACY_STANDARDS.md (15-18KB)
- Setting accuracy requirements
- Scientific/technical details
- Geographic specifics
- Climate and weather patterns

#### 6. SERIES_PLAN_10_BOOKS.md (15-18KB)
- Individual book concepts
- Series arc development
- Character progression
- Theme evolution

#### 7. CHARACTER_DEVELOPMENT_FRAMEWORK.md (16-20KB)
- Character arc templates
- Voice differentiation
- Relationship mapping
- Growth milestones

## Intelligence in Synthesis

### Not Simple Merging
The bible-generator performs intelligent operations:

```python
# Example transformations
def generate_documents(research_data):
    # Combination: merge related data
    character_framework = combine(
        audience_data['preferences'],
        competitor_data['successful_characters']
    )

    # Derivation: infer from patterns
    series_plan = derive(
        trend_data['series_popularity'],
        topic_data['theme_opportunities']
    )

    # Expansion: elaborate on summaries
    voice_guide = expand(
        voice_data['samples'],
        into=['implementation', 'examples', 'exercises']
    )

    # Specialization: split for different uses
    voice_docs = split(
        voice_data,
        into=['style_guide', 'consistency_checklist']
    )
```

## Component Communication

### File-Based (No Direct Calls)
```yaml
Agent A writes: knowledge_base/type_a/data.json
Agent B reads: knowledge_base/type_a/data.json
Agent B writes: knowledge_base/type_b/data.json

# No recursion possible!
```

### Atomic Operations
```python
# Safe write pattern
write_to_temp_file(data)
atomic_rename(temp_file, final_file)
```

## Quality Metrics

### Research Coverage
- Confidence scores (0.0-1.0)
- Source diversity tracking
- Gap identification
- Completeness assessment

### Output Quality
- Document completeness checks
- Cross-reference validation
- Consistency verification
- Production readiness assessment

## References
- Agent files in `.claude/agents/`
- CLAUDE.md for architecture rules
- Template system for agent patterns