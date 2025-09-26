# Agent I/O Specifications - Research System

## Universal I/O Pattern for All Research Agents

### Input from Main Claude
```yaml
Standard Prompt Format:
  "Research {domain} and save findings to knowledge base.
   Context: {relevant_conversation_context}
   Search scope: {specific_parameters}
   Output directory: knowledge_base/{domain}/"

Example:
  "Research market trends and save findings to knowledge base.
   Context: User interested in writing mystery novel
   Search scope: mystery genre trends 2024-2025
   Output directory: knowledge_base/trends/"
```

### Output to Knowledge Base
```yaml
File Structure:
  Raw Data: knowledge_base/{domain}/raw_data_{timestamp}.json
  Summary: knowledge_base/{domain}/summary_{timestamp}.json

Timestamp Format: YYYYMMDDHHmmss (e.g., 20250115143022)
```

### Return to Main Claude
```yaml
Success Response:
  status: "success"
  summary: "Brief 2-3 sentence natural language summary"
  files_created: ["path/to/summary.json", "path/to/raw_data.json"]
  confidence: 0.85

Error Response:
  status: "failed" or "partial"
  error: "Description of issue"
  fallback: "Suggested alternative approach"
```

## Agent-Specific I/O Specifications

### 1. trend-analyzer

**Input Prompt Examples:**
```
"Research fiction market trends and save to knowledge base.
 Context: User exploring what to write
 Search scope: general fiction trends 2024-2025
 Output directory: knowledge_base/trends/"
```

**Output Files:**
```json
// summary_20250115143022.json
{
  "timestamp": "2025-01-15T14:30:22Z",
  "domain": "fiction_market",
  "key_trends": [
    {"genre": "Mystery", "growth": "+45%", "confidence": 0.9},
    {"genre": "Romance", "growth": "+23%", "confidence": 0.85}
  ],
  "emerging": ["Climate Fiction", "Cozy Fantasy"],
  "declining": ["Hard SciFi", "Western"],
  "sources": 8,
  "quality_score": 0.88
}
```

### 2. competitor-scanner

**Input Prompt Examples:**
```
"Research competition in tropical mystery niche and save to knowledge base.
 Context: User planning tropical cozy mystery
 Search scope: tropical/island mystery novels 2023-2025
 Output directory: knowledge_base/competitors/"
```

**Output Files:**
```json
// analysis_20250115143055.json
{
  "timestamp": "2025-01-15T14:30:55Z",
  "niche": "tropical_mystery",
  "top_competitors": [
    {
      "title": "Death in Paradise",
      "author": "Robert Thorogood",
      "sales_rank": 1250,
      "reviews": 4500,
      "strengths": ["Setting", "Humor"],
      "weaknesses": ["Pacing"]
    }
  ],
  "market_gaps": [
    "No cooking-themed tropical mysteries",
    "Underserved: Caribbean islands beyond Jamaica"
  ],
  "saturation_level": "moderate",
  "opportunity_score": 0.75
}
```

### 3. audience-profiler

**Input Prompt Examples:**
```
"Research reader demographics for cozy mysteries and save to knowledge base.
 Context: User writing cozy mystery in tropical setting
 Search scope: cozy mystery reader preferences and demographics
 Output directory: knowledge_base/audience/"
```

**Output Files:**
```json
// demographics_20250115143088.json
{
  "timestamp": "2025-01-15T14:30:88Z",
  "genre": "cozy_mystery",
  "primary_audience": {
    "age_range": "25-45",
    "gender_split": "70% female, 30% male",
    "location": "US suburban/rural",
    "education": "College+",
    "income": "$40k-80k"
  },
  "reading_preferences": {
    "chapter_length": "2000-3000 words",
    "book_length": "60000-80000 words",
    "series_preference": "85% prefer series",
    "violence_tolerance": "minimal",
    "romance_subplot": "desired but not required"
  },
  "discovery_channels": [
    "Kindle Unlimited (45%)",
    "BookBub (30%)",
    "Goodreads (15%)"
  ]
}
```

### 4. voice-analyzer

**Input Prompt Examples:**
```
"Analyze successful writing voices in cozy mystery genre and save to knowledge base.
 Context: User needs to select author voice for tropical cozy mystery
 Search scope: bestselling cozy mystery author styles
 Output directory: knowledge_base/voice/"
```

**Output Files:**
```json
// style_analysis_20250115143122.json
{
  "timestamp": "2025-01-15T14:31:22Z",
  "genre": "cozy_mystery",
  "voice_options": [
    {
      "name": "Warm Conversational",
      "characteristics": {
        "sentence_length": "10-15 words average",
        "vocabulary": "Grade 7-9",
        "tone": "Friendly, approachable",
        "perspective": "First person"
      },
      "sample": "I never expected to find a body at the beach barbecue.",
      "market_fit": "65%",
      "similar_authors": ["Agatha Raisin series"]
    },
    {
      "name": "Witty Observer",
      "characteristics": {
        "sentence_length": "15-20 words average",
        "vocabulary": "Grade 8-10",
        "tone": "Dry humor, observational",
        "perspective": "Third person limited"
      },
      "sample": "The body at the barbecue was, everyone agreed, in rather poor taste.",
      "market_fit": "25%"
    }
  ]
}
```

### 5. topic-explorer

**Input Prompt Examples:**
```
"Research cozy mystery genre conventions and save to knowledge base.
 Context: User unfamiliar with cozy mystery requirements
 Search scope: cozy mystery definition, tropes, reader expectations
 Output directory: knowledge_base/topics/"
```

**Output Files:**
```markdown
// background_research_20250115143155.md

# Cozy Mystery Genre Research

## Definition
Cozy mysteries are a subgenre of crime fiction in which sex and violence occur off stage, the detective is an amateur sleuth, and the crime and detection take place in a small, socially intimate community.

## Essential Elements
1. **Amateur Sleuth**: Not police/FBI
2. **Small Community**: Everyone knows everyone
3. **Minimal Violence**: Deaths occur off-page
4. **No Graphic Content**: Family-friendly
5. **Puzzle Focus**: Logic over action

## Common Settings
- Small towns
- Bookshops
- Bakeries
- B&Bs
- Craft stores

## Reader Expectations
- Series with recurring characters
- Character development
- Community relationships
- Satisfying puzzle resolution
- Comfort reading experience
```

### 6. bible-generator (Special: No WebSearch)

**Input Prompt Examples:**
```
"Synthesize all research from knowledge base into project bible.
 Context: Research phase complete, ready to start writing
 Search scope: Read all files in knowledge_base subdirectories
 Output directory: knowledge_base/synthesis/"
```

**Output Files:**
```yaml
# research_bible_20250115143200.yaml

project_bible:
  # From trend analysis
  genre: "Cozy Mystery"
  market_opportunity: "High - 45% growth"

  # From competitor analysis
  unique_angle: "Cooking-themed tropical mystery"
  differentiation: "First in niche"

  # From audience profile
  target_readers:
    primary: "US women 25-45"
    secondary: "Cozy mystery series readers"

  # From voice analysis
  author_voice:
    style: "Warm Conversational"
    perspective: "First person"
    tone: "Light, humorous"

  # From topic research
  genre_requirements:
    - "Amateur sleuth protagonist"
    - "Small island community setting"
    - "Minimal violence"
    - "Series potential"

  # Synthesis
  elevator_pitch: "A chef-turned-amateur-detective solves mysteries
                   in a Caribbean resort while running a beachside
                   restaurant. Think 'Murder She Wrote' meets
                   'The Great British Bake Off' in paradise."

  research_confidence: 0.92
  ready_to_write: true
```

## Atomic File Operations Pattern

All agents MUST use atomic writes to prevent corruption:

```python
# CORRECT: Atomic write pattern
content = {"data": analyzed_results}
temp_file = f"{output_dir}/summary_{timestamp}.json.tmp"
final_file = f"{output_dir}/summary_{timestamp}.json"

# Write to temp file
Write(temp_file, json.dumps(content, indent=2))

# Atomic rename
Bash(f"mv '{temp_file}' '{final_file}'")

# WRONG: Direct write (can corrupt on interruption)
Write(final_file, content)  # Don't do this!
```

## Error Handling Standards

```python
try:
    # Research operations
    results = WebSearch(query)

    if not results:
        return {
            "status": "partial",
            "summary": "Limited results found",
            "fallback": "Consider broader search terms"
        }

except Exception as e:
    return {
        "status": "failed",
        "error": str(e),
        "fallback": "Try alternative research approach"
    }
```

## Testing Each Agent

### Individual Agent Test
```bash
# Create test prompt
echo "Research mystery market trends and save to knowledge base.
Context: Testing agent functionality
Search scope: mystery fiction 2024-2025
Output directory: knowledge_base/test/" > test_prompt.txt

# Run agent
claude code agent trend-analyzer < test_prompt.txt

# Verify outputs
ls -la knowledge_base/test/
cat knowledge_base/test/summary_*.json
```

### Integration Test Flow
```
1. Main Claude receives: "I want to write a mystery novel"
2. Triggers: trend-analyzer
3. Receives summary: "Mystery up 45%..."
4. User says: "What about tropical mysteries?"
5. Triggers: competitor-scanner + audience-profiler (parallel)
6. Receives both summaries
7. User says: "Let's do it"
8. Triggers: bible-generator
9. Receives complete bible
```

---

*Clean I/O = Clean Data = Clean Decisions*