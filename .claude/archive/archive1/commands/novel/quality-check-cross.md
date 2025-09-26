---
description: Validate cross-chapter consistency
argument-hint: <chapter_range> e.g., "1-5" or "all"
---

# Cross-Chapter Quality Check

Validating cross-chapter consistency for: **$ARGUMENTS**

## Description

This command analyzes relationships BETWEEN chapters to ensure narrative continuity, plot consistency, and quality maintenance across your specified chapter range.

## Prerequisites

Individual chapters should score >=90 in quality-check-individual before running cross-chapter validation.

## Execution

Delegating to cross-chapter quality coordinator:

Use the quality-check-cross-coordinator subagent to orchestrate cross-chapter validation with these instructions:

Perform comprehensive cross-chapter quality validation for: $ARGUMENTS

Workflow:
1. Parse chapter range
   - Accept formats: '1-5', '3-8', or 'all'
   - Validate chapters exist
   - Check individual quality scores

2. Launch parallel validators
   - Execute 5 validators simultaneously
   - Each analyzes different continuity aspect
   - Collect all validation reports

3. Aggregate findings
   - Categorize issues by severity
   - Calculate weighted quality score
   - Identify patterns across chapters

4. Generate recommendations
   - Prioritize fixes by impact
   - Suggest specific improvements
   - Provide clear next steps

Validators to coordinate:
- cross-chapter-flow-validator (transitions)
- story-thread-tracker (plot threads)
- foreshadowing-payoff-mapper (setups/payoffs)
- character-voice-cross-validator (consistency)
- book-pacing-analyzer (momentum)

Success threshold: 95+ for publication readiness
Focus on reader experience and immersion.

## Quality Thresholds

- **95+**: Excellent continuity, publication-ready
- **90-94**: Good with minor adjustments needed
- **85-89**: Noticeable issues requiring attention
- **<85**: Major continuity problems to address

## Next Steps

Based on validation results:
- **Pass (95+)**: Continue with next chapters or publication
- **Minor Issues**: Run `/novel:smart-fix-cross` for targeted fixes

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/*/content.md`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/quality_report.json`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`

- **Major Issues**: Consider chapter revisions in problem areas