---
description: Fix chapter issues to reach quality threshold
argument-hint: <chapter_number>
---

# Smart Fix Command

Intelligently fix chapter **$ARGUMENTS** to achieve 95+ quality score.

## Pre-Check: Verify Quality Report Exists

First, verify that quality check has been run:
- Check for: `.claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/quality_check.json`
- If missing, run `/novel:quality-check-individual $ARGUMENTS` first

## Execution Strategy

### Step 1: Analyze Quality Report

Read the quality check results:
```
1. Read .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/quality_check.json
2. Read .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/plot_holes.json (if exists)
3. Read .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/consistency_check.json (if exists)
4. Read .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/bible_compliance.json (if exists)
```

Identify issues by priority:
- **Critical (must fix)**: Score < 80 in any dimension
- **High (should fix)**: Score 80-85 in any dimension
- **Medium (nice to fix)**: Score 85-90 in any dimension
- **Low (polish)**: Score 90-94 in any dimension

### Step 2: Fix Critical Issues First

#### 2.1 Bible Compliance Issues (if compliance < 90)

**Execute Bible compliance fix using Task tool:**
- **subagent_type**: "bible-compliance-validator"
- **description**: "Fix Bible violations in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Fix Bible compliance issues in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml
  - .claude/data/projects/{project}/entity_dictionary.yaml
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/bible_compliance.json

  Fix these violations:
  - Character personality deviations
  - World-building inconsistencies
  - Magic/technology rule violations
  - Entity naming inconsistencies

  WRITE fixed content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Maintain narrative flow while fixing violations.
  ```

#### 2.2 Plot Holes (if plot coherence < 85)

**Execute plot hole fix using Task tool:**
- **subagent_type**: "plot-hole-detector"
- **description**: "Fix plot holes in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Fix plot holes identified in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/plot_holes.json
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml

  Fix these issues:
  - Logic flaws and unreasonable developments
  - Causal chain breaks
  - Information gaps
  - Convenience problems

  WRITE fixed content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Ensure all plot threads are logical and well-motivated.
  ```

#### 2.3 Consistency Issues (if consistency < 90)

**Execute consistency fix using Task tool:**
- **subagent_type**: "continuity-guard-specialist"
- **description**: "Fix consistency issues in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Fix consistency issues in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/consistency_check.json
  - Previous chapter if exists: ch[**$ARGUMENTS**-1]/content.md

  Fix these consistency problems:
  - Timeline continuity breaks
  - Character position/state errors
  - Setting detail conflicts
  - Internal logic issues

  WRITE fixed content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Maintain smooth narrative while fixing inconsistencies.
  ```

### Step 3: Enhance Quality Dimensions

#### 3.1 Character Depth (if score < 90)

**Execute character enhancement using Task tool:**
- **subagent_type**: "character-psychology-specialist"
- **description**: "Enhance character depth in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Enhance character psychological depth in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/quality_check.json

  Enhance:
  - Internal monologues and motivations
  - Character reactions and emotions
  - Psychological consistency
  - Character growth moments

  WRITE enhanced content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Add depth without changing plot events.
  ```

#### 3.2 Dialogue Quality (if dialogue score < 90)

**Execute dialogue polish using Task tool:**
- **subagent_type**: "dialogue-master-specialist"
- **description**: "Polish dialogue in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Polish and enhance dialogue in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml
  - Character voice profiles

  Improve:
  - Character voice distinctiveness
  - Natural conversation flow
  - Subtext and tension
  - Cultural authenticity

  WRITE polished content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Maintain character personalities while improving dialogue.
  ```

#### 3.3 Emotional Impact (if emotional score < 85)

**Execute emotional enhancement using Task tool:**
- **subagent_type**: "emotion-weaver-specialist"
- **description**: "Enhance emotional impact in ch$ARGUMENTS"
- **prompt**: Provide the following instructions:
  ```
  Enhance emotional resonance in chapter $ARGUMENTS.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml
  - Emotional arc planning

  Enhance:
  - Emotional peaks and valleys
  - Reader empathy points
  - Atmospheric mood
  - Sensory details

  WRITE enhanced content to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md

  Deepen emotional experience without changing events.
  ```

### Step 4: Re-validate After Fixes

**Execute quality re-scoring using Task tool:**
- **subagent_type**: "quality-scorer"
- **description**: "Re-score ch$ARGUMENTS after fixes"
- **prompt**: Provide the following instructions:
  ```
  Re-evaluate chapter $ARGUMENTS quality after fixes.

  READ:
  - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md (newly fixed)
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml

  Score all dimensions and compare with previous scores.

  WRITE new quality assessment to:
  .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/quality_check_after_fix.json

  Include:
  - New overall_score
  - Dimension improvements
  - Remaining issues (if any)
  ```

## Fix Priority Matrix

| Score Range | Priority | Action Required | Target Score |
|------------|----------|----------------|--------------|
| < 80 | CRITICAL | Must fix immediately | 85+ |
| 80-84 | HIGH | Fix before publication | 90+ |
| 85-89 | MEDIUM | Fix if time permits | 92+ |
| 90-94 | LOW | Polish touches | 95+ |
| 95+ | NONE | Already excellent | Maintain |

## Iterative Improvement Loop

If after first fix attempt, score is still < 95:
1. Analyze what dimensions are still low
2. Apply targeted fixes for those specific areas
3. Re-validate
4. Repeat up to 3 times maximum


## Success Criteria

- Original issues identified correctly
- Appropriate fixes applied based on severity
- New quality score >= 95 (or maximum achievable)
- No new issues introduced
- Chapter remains coherent and engaging
- All hooks executed successfully

## Failure Handling

If unable to achieve 95+ after 3 iterations:
1. Document remaining issues in `.claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/fix_limitations.md`
2. Suggest manual intervention for complex issues
3. Consider if Bible needs adjustment
4. Log fix attempts for learning system

---
**Execute fixes systematically by priority to ensure comprehensive chapter improvement.**