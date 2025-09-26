---
description: Generate new chapter with quality validation
argument-hint: <chapter_number>
---

# Chapter Start Command (v5.0 - Command Driven)

Generate chapter **$ARGUMENTS** using validated sequential pipeline.

**Deep Planning Protocol**: Think a lot about the narrative requirements for chapter $ARGUMENTS:
- Character development needs and emotional arcs at this story point
- Plot progression balance and pacing requirements  
- Continuity integration with all previous chapters
- Foreshadowing setup and payoff preparation across the broader narrative

Keep thinking about the chapter's role in the overall story architecture before beginning generation.

## AUTOMATED EXECUTION SEQUENCE

When this command is executed, Claude MUST perform these steps in order:

### Step 1: Setup and Validation
```
1. Read current project from .claude/data/context/current_project.json
2. Use Bash tool: mkdir -p .claude/data/projects/{project}/book_{current_book}/chapters/ch**$ARGUMENTS**/
3. Use Bash tool: mkdir -p .claude/data/projects/{project}/shared
4. Verify Bible exists: .claude/data/projects/{project}/book_{current_book}/bible.yaml
5. If Bible missing, STOP with error: "[ ] Error: Bible not found"
6. Auto-create entity dictionary if missing using entity-dictionary-creator
```

### Step 2: Generate Outline (MUST COMPLETE)

**Execute outline generation using Task tool:**
- **subagent_type**: "outline-generator"
- **description**: "Generate outline for chapter $ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  You need to generate an outline for chapter $ARGUMENTS.
  
  REQUIRED SAVE PATH: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/outline.json
  
  Follow your built-in workflow:
  1. Read the Bible, previous chapter, and entity dictionary
  2. Generate a detailed outline
  3. SAVE IT to the path above using Write tool
  
  Your success depends on:
  - Reading at least 2 files (verified by Read tool usage)
  - Saving the outline (verified by Write tool usage)
  - File existing after you complete
  ```

**VALIDATION**: After Task completes, verify outline.json exists. If not, STOP.

### Step 3: Pre-Generation Entity Validation

**Execute entity validation using Task tool:**
- **subagent_type**: "entity-validator"
- **description**: "Validate entity consistency"
- **prompt**: Provide the following instructions:
  ```
  Pre-validate entity naming for chapter $ARGUMENTS:
  1. Load entity dictionary from .claude/data/projects/{project}/shared/entity_dictionary.yaml
  2. Load chapter outline from .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/outline.json
  3. Check all entity references in outline against dictionary
  4. Flag any inconsistencies or new entities
  5. Block generation if critical violations found
  6. Report validation status and recommendations
  ```

### Step 4: Generate Initial Draft (MUST COMPLETE)

**Execute draft generation using Task tool and WAIT for completion:**
- **subagent_type**: "scene-generator"
- **description**: "Write chapter $ARGUMENTS draft"
- **prompt**: Provide the following mandatory instructions:
  ```
  MANDATORY ACTIONS IN ORDER:
  
  1. USE Read TOOL to read: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/outline.json
     - If missing, STOP with error: "[ ] Error: Required file not found"
     - Confirm: "Outline loaded"
  
  2. USE Read TOOL to read: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: characters (personalities), voice_profile (speech patterns), universe (settings)
     - Skip other sections to save processing
     - Confirm: "Bible loaded (characters & world)"
  
  3. USE Read TOOL to read: .claude/data/projects/{project}/shared/entity_dictionary.yaml
     - Confirm: "Entity Dictionary loaded"
  
  4. Write 3000-5000 words following the outline
     - Start with: "Chapter $ARGUMENTS: [Title from outline]"
     - This is creative fiction, not summary
     - STRICTLY follow entity dictionary naming rules
  
  5. USE Write TOOL to save to: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v1.md
     - Confirm: "Draft saved"
  ```

**VALIDATION**: After Task completes, verify draft_v1.md exists. If not, STOP.

### Step 5: Enhance Characters (MUST COMPLETE)

**Execute character enhancement using Task tool and WAIT:**
- **subagent_type**: "character-psychology-specialist"
- **description**: "Enhance character depth"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v1.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: characters section (backgrounds, motivations, relationships)
     - Skip other sections to save processing
  3. Enhance with internal thoughts, emotions, mannerisms
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v2.md
  ```

**VALIDATION**: Verify draft_v2.md exists.

### Step 6: Polish Dialogue (MUST COMPLETE)

**Execute dialogue polishing using Task tool and WAIT:**
- **subagent_type**: "dialogue-master-specialist"
- **description**: "Polish dialogue"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v2.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: voice_profile section (speech patterns, vocabulary, dialects)
     - Skip other sections to save processing
  3. Make each character's voice distinct
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v3.md
  ```

**VALIDATION**: Verify draft_v3.md exists.

### Step 7: Enrich World (MUST COMPLETE)

**Execute world enrichment using Task tool and WAIT:**
- **subagent_type**: "world-building-specialist"
- **description**: "Add world details"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v3.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: universe section (locations, culture, environment)
     - Skip other sections to save processing
  3. Add sensory details, atmosphere, setting
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v4.md
  ```

**VALIDATION**: Verify draft_v4.md exists.

### Step 8: Plant Clues (MUST COMPLETE)

**Execute clue planting using Task tool and WAIT:**
- **subagent_type**: "clue-planter"
- **description**: "Plant mystery clues"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v4.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: mystery_structure (clues to plant), foreshadowing (setups needed)
     - Skip other sections to save processing
  3. Plant clues naturally in descriptions, dialogue, and actions
  4. Ensure fair-play mystery rules (all clues available to reader)
  5. USE Edit TOOL to modify draft_v4.md with planted clues
  6. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v4_clues.md
  ```

**VALIDATION**: Verify draft_v4_clues.md exists.

### Step 9: Validate Continuity (MUST COMPLETE)

**Execute continuity validation using Task tool and WAIT:**
- **subagent_type**: "continuity-guard-specialist"
- **description**: "Check continuity"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v4_clues.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: series_metadata (timeline), universe (locations), characters (relationships)
     - Skip other sections to save processing
  3. USE Read TOOL: .claude/data/projects/{project}/shared/entity_dictionary.yaml
  4. Fix timeline, knowledge boundaries, consistency
  5. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v5.md
  ```

**VALIDATION**: Verify draft_v5.md exists.

### Step 10: Polish Prose (MUST COMPLETE)

**Execute prose polishing using Task tool and WAIT:**
- **subagent_type**: "prose-craft-specialist"
- **description**: "Polish prose"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v5.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: voice_profile (narrative style), themes (thematic expression)
     - Skip other sections to save processing
  3. Enhance sentence variety, imagery, flow
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v6.md
  ```

**VALIDATION**: Verify draft_v6.md exists.

### Step 11: Enhance Emotions (MUST COMPLETE)

**Execute emotion enhancement using Task tool and WAIT:**
- **subagent_type**: "emotion-weaver-specialist"
- **description**: "Enhance emotional depth"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v6.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: characters (emotional profiles), themes (emotional themes)
     - Skip other sections to save processing
  3. Enhance emotional curves, add sensory details for emotional resonance
  4. Deepen emotional layers without changing plot
  5. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v7.md
  ```

**VALIDATION**: Verify draft_v7.md exists.

### Step 12: Check Logic (MUST COMPLETE)

**Execute plot hole detection using Task tool and WAIT:**
- **subagent_type**: "plot-hole-detector"
- **description**: "Fix plot holes"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/draft_v7.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: mystery_structure (plot logic), characters (knowledge boundaries)
     - Skip other sections to save processing
  3. Fix any logic issues or plot holes
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/content.md
  ```

**VALIDATION**: Verify content.md exists.

### Step 13: Score Quality (MUST COMPLETE)

**Execute quality scoring using Task tool and WAIT:**
- **subagent_type**: "quality-scorer"
- **description**: "Score quality"
- **prompt**: Provide the following instructions:
  ```
  1. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/content.md
  2. USE Read TOOL: .claude/data/projects/{project}/book_{current_book}/bible.yaml
     - Focus ONLY on: series_metadata (genre standards), themes (thematic depth)
     - Skip other sections to save processing
  3. Score all dimensions (0-100)
  4. USE Write TOOL: .claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/quality_report.json
  
  Format: {"overall_score": N, "dimensions": {...}, "ready": true/false}
  ```

**VALIDATION**: Read quality_report.json and display score.

### Step 14: Unified Update Pipeline (CONDITIONAL)

**After quality scoring, check if score >= 95:**

1. **Read quality report:**
   - Use Read tool: `.claude/data/projects/{project}/book_{current_book}/chapters/ch$ARGUMENTS:03d/quality_report.json`
   - Extract overall_score

2. **If score >= 95:**
   - Display: "[x] Chapter qualifies for learning with score: {score}"
   - Execute unified-update-pipeline:
   ```bash
   /novel:unified-update-pipeline $ARGUMENTS
   ```
   - This will automatically update all 6 core files in parallel:
     * meta.json (chapter statistics)
     * entity_dictionary.yaml (learned variations)
     * project.json (aggregated stats)
     * characters.json (character development)
     * plot.json (plot progression)
     * world.json (world details)

3. **If score < 95:**
   - Display: "WARNING:️ Warning: Chapter score {score} below learning threshold (95)"
   - Display: "💡 Consider running /novel:smart-fix to improve quality"
   - No updates performed (preserving data quality)

## EXECUTION RULES

1. **MUST execute each Task sequentially** - wait for completion
2. **MUST validate file creation** after each step
3. **STOP if any validation fails** - report which step failed
4. **Agents MUST use Read and Write tools** - not just return content


## SUCCESS CRITERIA

- All 14 steps complete successfully
- All output files exist
- Quality score >= 95
- Context files updated with chapter content

## ERROR HANDLING

If any step fails:
1. Report which step failed
2. Show what file is missing
3. Suggest manual intervention or smart-fix command

---
**This is a COMMAND, not documentation. Execute these steps automatically.**