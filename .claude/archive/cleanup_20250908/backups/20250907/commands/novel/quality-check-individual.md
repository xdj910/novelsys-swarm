---
description: Check individual chapter quality
argument-hint: <chapter_number>
---

# Individual Chapter Quality Check Command

Check quality for individual chapter: **$ARGUMENTS**

## Phase 1: Individual Chapter Validation

This command focuses on single-chapter quality, preparing it for cross-chapter validation.

## Quality Validation Steps

### Step 1: Prerequisites Validation

**CRITICAL**: Before proceeding, verify all required files exist:

1. **Read current project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - Extract project name

2. **Verify chapter content exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{current_book}/chapters/ch**$ARGUMENTS**/content.md`
   - If content.md missing, STOP with error: "Cannot check quality - Chapter **$ARGUMENTS** content not found"

3. **Verify Bible exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
   - If bible.yaml missing, STOP with error: "Cannot check quality - Bible not found for validation"

### Step 2: Chapter Consistency Check

Execute Task:
```
Task(
    subagent_type="continuity-guard-specialist",
    description="Check ch$ARGUMENTS consistency",
    prompt="""
    Validate chapter $ARGUMENTS internal consistency.

    READ:
    - .claude/data/projects/{project}/book_{current_book}/chapters/ch**$ARGUMENTS**/content.md
    - .claude/data/projects/{project}/book_{current_book}/bible.yaml

    Check for:
    - Timeline consistency within chapter
    - Character behavior consistency
    - Setting detail coherence
    - Internal logic integrity

    WRITE validation report to:
    .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/consistency_check.json
    """
)
```

### Step 2: Plot Hole Detection

Execute Task:
```
Task(
    subagent_type="plot-hole-detector",
    description="Detect ch$ARGUMENTS plot issues",
    prompt="""
    Identify plot holes in chapter $ARGUMENTS.

    READ:
    - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
    - .claude/data/projects/{project}/book_{current_book}/bible.yaml

    Detect:
    - Logic flaws
    - Causal chain breaks
    - Information gaps
    - Convenience problems

    WRITE findings to:
    .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/plot_holes.json
    """
)
```

### Step 3: Bible Compliance Verification

Execute Task:
```
Task(
    subagent_type="bible-compliance-validator",
    description="Verify ch$ARGUMENTS Bible compliance",
    prompt="""
    Validate chapter $ARGUMENTS against Bible rules.

    READ:
    - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
    - .claude/data/projects/{project}/book_{current_book}/bible.yaml
    - .claude/data/projects/{project}/entity_dictionary.yaml

    Verify:
    - Character personality alignment
    - World-building consistency
    - Magic/technology rules
    - Timeline accuracy
    - Entity name consistency

    WRITE compliance report to:
    .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/bible_compliance.json
    """
)
```

### Step 4: Quality Scoring

Execute Task:
```
Task(
    subagent_type="quality-scorer",
    description="Score ch$ARGUMENTS quality",
    prompt="""
    Generate comprehensive quality score for chapter $ARGUMENTS.

    READ:
    - .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/content.md
    - .claude/data/projects/{project}/book_{current_book}/bible.yaml
    - Previous validation reports if they exist

    Score dimensions (0-100):
    - Character depth
    - Plot coherence
    - Writing quality
    - Emotional impact
    - Consistency
    - Bible compliance
    - Cultural authenticity
    - Mystery fairness
    - Atmosphere
    - Pacing

    WRITE comprehensive score to:
    .claude/data/projects/{project}/chapters/ch**$ARGUMENTS**/quality_check.json

    Include:
    - overall_score
    - detailed_scores
    - strengths
    - improvements_needed
    """
)
```

## Quality Gates

### Stage Requirements
- **Foundation (80%)**: Basic structure and consistency
- **Content (85%)**: Writing quality and engagement
- **Integration (90%)**: Ready for cross-chapter checks
- **Excellence (95%)**: Publication-ready quality

### Decision Tree
```
Score >= 95: [x] EXCELLENT - Ready for cross-chapter validation
Score 90-94: WARNING:️ Warning: GOOD - Minor improvements recommended
Score 85-89: WARNING:️ Warning: ACCEPTABLE - Significant improvements needed
Score 80-84: WARNING:️ Warning: MARGINAL - Major revision required
Score < 80:  [ ] Error: FAIL - Requires rewrite or smart-fix
```


## Output Structure

All validation reports should follow this structure:
```json
{
  "chapter": "ch001",
  "timestamp": "2024-01-01T12:00:00",
  "validator": "agent-name",
  "overall_score": 92,
  "issues_found": [],
  "recommendations": [],
  "strengths": []
}
```

## Success Criteria

- All 4 validation tasks complete
- All JSON files created and valid
- Overall quality score calculated
- Clear recommendations provided

## Next Steps

After individual chapter validation:
1. If score < 90: Run `/novel:smart-fix $ARGUMENTS`
2. If score >= 90: Run `/novel:quality-check-cross` for multi-chapter validation

---
**Execute systematically to ensure comprehensive chapter quality validation.**