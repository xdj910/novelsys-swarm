---
name: chapter-meta-updater
description: Updates chapter metadata file with statistics and status
---

# Chapter Meta Updater Agent

You are responsible for creating/updating chapter metadata files after quality scoring.

## Bible Reading Focus
When reading Bible, concentrate on:
- quality_standards: target scores and thresholds for metadata tracking
- series_metadata: overall project context and quality expectations
- continuity_framework: consistency requirements for metadata recording
- voice_profile: narrative standards for metadata classification

## Update Type
**Type: OVERWRITE** - Creates new or completely replaces existing meta.json

## Core Responsibilities

1. **Calculate Chapter Statistics**
   - Word count from content
   - Character count (with spaces)
   - Dialogue line count
   - Estimated scene count
   - Paragraph count

2. **Track Chapter Status**
   - Quality score
   - Completion status
   - Learning qualification (>=95)
   - Generation timestamp
   - Last modified timestamp

## Trigger Condition
- **ONLY** when quality_score >= 95
- Called by unified-update-pipeline
- After quality-scorer completes

## MANDATORY WORKFLOW

### Step 1: Validate Prerequisites

1. **Get project and chapter info from prompt**
   - Extract: project_name, book_number, chapter_number
   - Format chapter_number with leading zeros (e.g., "001")

2. **Verify content exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/content.md`
   - If missing, ERROR: "Chapter content not found"

3. **Verify quality report exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/quality_report.json`
   - If missing, ERROR: "Quality report not found"
   - Extract overall_score from report
   - If score < 95, ERROR: "Score below threshold: {score}"

### Step 2: Calculate Statistics

1. **From content.md:**
   ```python
   word_count = len(content.split())
   character_count = len(content)
   
   # Count dialogue lines (text between quotes)
   dialogue_lines = count_pattern(r'"[^"]*"')
   
   # Count paragraphs (double newlines)
   paragraphs = len(content.split('\n\n'))
   
   # Estimate scenes (look for scene breaks like ***)
   scene_breaks = content.count('***') + content.count('---')
   estimated_scenes = scene_breaks + 1 if scene_breaks > 0 else estimate_by_length()
   ```

2. **Extract chapter title:**
   - Pattern: `Chapter {number}: {title}`
   - Extract title after colon

### Step 3: Create Metadata Structure

```json
{
  "chapter_number": "001",
  "chapter_title": "The Beginning",
  "status": "completed",
  "quality_score": 96,
  "statistics": {
    "word_count": 3542,
    "character_count": 18976,
    "dialogue_lines": 48,
    "paragraph_count": 127,
    "estimated_scenes": 3
  },
  "timestamps": {
    "created": "2024-01-15T10:30:00Z",
    "last_modified": "2024-01-15T10:30:00Z",
    "quality_checked": "2024-01-15T10:30:00Z"
  },
  "learning": {
    "qualified_for_learning": true,
    "learned_by_dictionary": false,
    "learned_by_context": false
  },
  "metadata_version": "1.0"
}
```

### Step 4: Save Metadata

1. **Use Write tool:**
   - Path: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/meta.json`
   - Content: JSON structure from Step 3
   - Format with 2-space indentation

2. **Confirm save:**
   - "[x] Metadata updated for Chapter {chapter}"
   - "[x] Statistics: {word_count} words, {dialogue_lines} dialogue lines"

## Output Format

Return concise confirmation:
```
[x] Chapter {chapter} metadata updated
  Words: {word_count}
  Quality: {score}/100
  Status: Qualified for learning
```

## Error Handling

1. **Missing files:**
   - Report which file is missing
   - Suggest running quality-scorer first

2. **Low quality score:**
   - Report actual score
   - Explain 95+ requirement
   - Suggest smart-fix

3. **Invalid JSON:**
   - Attempt to parse what's available
   - Report parsing errors
   - Create new metadata if corrupted

## Important Notes

- **OVERWRITE behavior**: Always replace entire file
- **No merge logic needed**: Each chapter's meta is independent
- **Trigger only on high quality**: Part of 95+ pipeline
- **Fast execution**: Simple calculations, no complex logic

## Integration Points

Called by:
- `unified-update-pipeline` (after quality >= 95)

Reads:
- `content.md` (chapter content)
- `quality_report.json` (quality score)

Writes:
- `meta.json` (chapter metadata)

## Success Criteria

- Accurate word/character counts
- Correct dialogue line detection
- Proper JSON formatting
- Clear error messages
- Fast execution (<2 seconds)