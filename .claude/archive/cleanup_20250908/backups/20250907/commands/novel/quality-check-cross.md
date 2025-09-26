---
description: Validate cross-chapter consistency
argument-hint: <chapter_range> e.g., "1-5" or "all"
---

# Cross-Chapter Quality Check Command

Validate cross-chapter consistency and narrative flow for chapters: **$ARGUMENTS**

## Phase 2: Cross-Chapter Validation

This command analyzes relationships BETWEEN chapters, ensuring narrative continuity.

**Prerequisites**: Run `/novel:quality-check-individual` first to fix individual chapter issues.

## Extended Analysis Protocol

Before validation, think deeply about:
- Timeline accuracy and chronological consistency across all chapters
- Character knowledge evolution and realistic information progression
- World-building consistency and setting detail continuity
- Plot thread tracking and resolution pattern analysis
- Potential narrative contradictions emerging in complete story arc

## MANDATORY EXECUTION SEQUENCE

### Step 1: Launch All 5 Cross-Chapter Validators in PARALLEL

**CRITICAL: Execute ALL 5 validators in PARALLEL**

When you reach this step, you MUST:
1. Display: "⏳ Launching 5 parallel cross-chapter validators..."
2. Use Task tool 5 times in a SINGLE message
3. Each Task call must use a different validator agent

**The 5 cross-chapter validator agents to launch (ALL in parallel):**

1. **cross-chapter-flow-validator**: Validate chapter transitions
   - Description: "Validate chapter transitions"
   - Instructions: "Validate all adjacent chapter transitions for: $ARGUMENTS
     READ all chapters in range: .claude/data/projects/{project}/chapters/ch*/content.md
     Check Ch(n) -> Ch(n+1) flow: Time continuity (no timeline jumps), Scene transitions (smooth handoffs), Narrative momentum (no jarring stops), Character positions (logical movement)
     WRITE flow validation report to: .claude/data/projects/{project}/validation/cross_chapter_flow.json"

2. **story-thread-tracker**: Track plot threads and character arcs
   - Description: "Track plot threads"
   - Instructions: "Track all plot threads across chapters: $ARGUMENTS
     READ: All chapters in range, .claude/data/projects/{project}/book_{current_book}/bible.yaml
     Identify: Main plot progression, Subplot development, Character arc advancement, Abandoned or forgotten threads, Unresolved setups
     WRITE thread analysis to: .claude/data/projects/{project}/validation/story_threads.json"

3. **foreshadowing-payoff-mapper**: Map setups to payoffs
   - Description: "Map setups to payoffs"
   - Instructions: "Map all foreshadowing and payoffs in chapters: $ARGUMENTS
     READ all chapters and identify: Foreshadowing setups, Corresponding payoffs, Orphaned setups (no payoff), Unfounded reveals (no setup), Chekhov's gun violations
     WRITE mapping to: .claude/data/projects/{project}/validation/foreshadowing_map.json"

4. **book-pacing-analyzer**: Analyze overall book pacing
   - Description: "Analyze overall pacing"
   - Instructions: "Analyze pacing arc across chapters: $ARGUMENTS
     READ all chapters and evaluate: Opening hook effectiveness, Rising action progression, Climax timing and impact, Resolution satisfaction, Overall rhythm patterns
     Detect issues: Sagging middle syndrome, Rushed endings, Pacing inconsistencies
     WRITE pacing analysis to: .claude/data/projects/{project}/validation/pacing_analysis.json"

5. **character-voice-cross-validator**: Validate voice consistency
   - Description: "Validate voice consistency"
   - Instructions: "Validate character voices across chapters: $ARGUMENTS
     READ all chapters and check: Each character's voice consistency, Dialogue distinctiveness, Speech pattern maintenance, Voice evolution (if intentional), Author voice intrusion
     WRITE voice validation to: .claude/data/projects/{project}/validation/character_voices.json"

**IMPORTANT EXECUTION NOTES:**
- You MUST launch ALL 5 agents in ONE message with 5 Task tool calls
- Do NOT skip any agents - all 5 are required for comprehensive analysis
- Each agent analyzes chapters specified in $ARGUMENTS
- All agents operate independently and in parallel

## Validation Coverage Matrix

| Aspect | Agent | Focus Area |
|--------|-------|------------|
| Transitions | cross-chapter-flow-validator | Adjacent chapter connections |
| Plot Threads | story-thread-tracker | Arc continuity and completion |
| Setup/Payoff | foreshadowing-payoff-mapper | Mystery fairness and satisfaction |
| Pacing | book-pacing-analyzer | Story rhythm and momentum |
| Character Voice | character-voice-cross-validator | Dialogue consistency |



## Output Consolidation

### Summary Report Structure
```json
{
  "chapters_analyzed": ["ch001", "ch002", ...],
  "validation_timestamp": "2024-01-01T12:00:00",
  "overall_continuity_score": 92,
  "critical_issues": {
    "timeline_breaks": [],
    "abandoned_threads": [],
    "voice_inconsistencies": [],
    "pacing_problems": []
  },
  "cross_chapter_strengths": [],
  "recommendations": {
    "high_priority": [],
    "medium_priority": [],
    "low_priority": []
  }
}
```

## Quality Gates

### Cross-Chapter Thresholds
- **Excellent (95+)**: Publication-ready continuity
- **Good (90-94)**: Minor continuity adjustments
- **Acceptable (85-89)**: Noticeable issues requiring attention
- **Poor (<85)**: Major continuity problems

## Decision Tree

```
All validators complete?
+- Yes  ->  Check critical issues count
|   +- 0 critical  ->  [x] PASS
|   +- 1-2 critical  ->  WARNING:️ Warning: Minor fixes needed
|   +- 3+ critical  ->  [ ] Error: Major revision required
+- No  ->  Check which validator failed
    +- Restart failed validator
```

## Success Criteria

- All 5 cross-chapter validators complete
- All validation JSONs created
- No timeline contradictions found
- All plot threads properly tracked
- Character voices remain consistent
- Pacing maintains reader engagement

## Next Steps

Based on validation results:
1. **Score 95+**: Ready for publication/next book
2. **Score 90-94**: Run `/novel:smart-fix` for specific issues
3. **Score <90**: Consider chapter rewrites for problem areas

---
**Execute all 5 validators in parallel for comprehensive cross-chapter analysis.**