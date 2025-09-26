---
description: Check individual chapter quality
argument-hint: <chapter_number>
---

# Individual Chapter Quality Check

Validating quality for chapter: **$ARGUMENTS**

## Description

This command performs comprehensive quality validation on a single chapter, checking consistency, plot integrity, Bible compliance, and overall quality metrics.

## Performance Optimized

Uses parallel execution of 4 validators for 4x speed improvement (15 seconds vs 60 seconds).

## Execution

Delegating to individual chapter quality coordinator:

Use the quality-check-individual-coordinator subagent to orchestrate chapter quality validation with these instructions:

Perform comprehensive quality validation for chapter: $ARGUMENTS

CRITICAL: Execute all 4 validators IN PARALLEL for optimal performance.

Workflow:
1. Validate prerequisites
   - Verify chapter content exists
   - Verify Bible exists
   - Check entity dictionary

2. Launch parallel validators (ALL AT ONCE)
   - continuity-guard-specialist (consistency)
   - plot-hole-validator (plot integrity)
   - bible-compliance-validator (rule adherence)
   - quality-scorer (comprehensive scoring)

3. Aggregate results
   - Compile all findings
   - Calculate weighted score
   - Categorize issues by severity

4. Generate recommendations
   - If 95+: Mark excellent, ready for learning
   - If 90-94: Suggest smart-fix
   - If <90: Recommend major revision

Success threshold: 95+ for unified-update-pipeline
Bible compliance is mandatory (100% required).

## Quality Thresholds

- **95+**: Excellence - Ready for system learning
- **90-94**: Good - Minor improvements needed
- **85-89**: Acceptable - Significant work required
- **80-84**: Marginal - Major revision needed
- **<80**: Fail - Requires rewrite

## Validation Dimensions

Each validator checks specific aspects:
- **Consistency**: Timeline, characters, settings
- **Plot**: Logic, causality, information flow
- **Bible**: Character traits, world rules, entity names
- **Quality**: Writing, emotion, pacing, atmosphere

## Next Steps

Based on validation score:
- **95+**: Run `/novel:unified-update-pipeline` (auto-triggered)
- **90-94**: Run `/novel:smart-fix $ARGUMENTS`

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/*/content.md`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/quality_report.json`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`

- **<90**: Consider major revision or rewrite