---
description: Fix cross-chapter consistency issues
argument-hint: <chapter_range> e.g., "1-5" or "all"
---

# Smart Fix Cross-Chapter Command

Fix cross-chapter continuity issues for chapters: **$ARGUMENTS**

## Pre-Check: Verify Cross-Validation Report Exists

First, verify that cross-chapter validation has been run:
- Check for validation reports in: `.claude/data/projects/{project}/validation/`
- Required files:
  - `cross_chapter_flow.json`
  - `story_threads.json`
  - `foreshadowing_map.json`
  - `pacing_analysis.json`
  - `character_voices.json`
- If missing, run `/novel:quality-check-cross $ARGUMENTS` first

## Execution Strategy

Cross-chapter fixes must be done SEQUENTIALLY to avoid conflicts:
1. Fix timeline/flow issues first (foundation)
2. Then fix plot thread continuity
3. Then fix foreshadowing/payoffs
4. Finally polish character voices and pacing

## Sequential Fix Process

### Phase 1: Timeline and Flow Fixes

#### Step 1.1: Analyze Flow Issues

Read cross-chapter flow validation:
```
1. Read .claude/data/projects/{project}/validation/cross_chapter_flow.json
2. Identify all Ch(n) -> Ch(n+1) transition problems
3. Create fix order: earliest chapters first
```

#### Step 1.2: Fix Adjacent Chapter Transitions

**For each transition issue, execute using Task tool:**
- **subagent_type**: "cross-chapter-flow-validator"
- **description**: "Fix transition between chapters"
- **prompt**: Provide the following instructions:
  ```
  Fix transition issues between adjacent chapters in range: $ARGUMENTS

  READ:
  - .claude/data/projects/{project}/validation/cross_chapter_flow.json
  - Affected chapter pairs (Ch n and Ch n+1)
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml

  Fix these transition problems:
  - Timeline jumps or inconsistencies
  - Scene handoff issues
  - Character position/state mismatches
  - Momentum breaks

  WRITE fixes to BOTH chapters as needed:
  - End of Ch(n): .claude/data/projects/{project}/chapters/ch{n:03d}/content.md
  - Start of Ch(n+1): .claude/data/projects/{project}/chapters/ch{n+1:03d}/content.md

  Maintain narrative flow while ensuring smooth transitions.
  Document changes in: .claude/data/projects/{project}/fixes/transition_fixes.log
  ```

### Phase 2: Story Thread Continuity

#### Step 2.1: Analyze Thread Issues

Read story thread analysis:
```
1. Read .claude/data/projects/{project}/validation/story_threads.json
2. Identify abandoned or broken threads
3. Map which chapters need thread repairs
```

#### Step 2.2: Repair Plot Threads

**Execute plot thread repair using Task tool:**
- **subagent_type**: "story-thread-tracker"
- **description**: "Repair broken plot threads"
- **prompt**: Provide the following instructions:
  ```
  Fix plot thread continuity issues across chapters: $ARGUMENTS

  READ:
  - .claude/data/projects/{project}/validation/story_threads.json
  - All affected chapters
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml

  Repair these thread issues:
  - Abandoned plot threads (add resolution or continuation)
  - Broken character arcs (restore progression)
  - Forgotten subplots (weave back in or properly close)
  - Inconsistent thread development (smooth progression)

  WRITE repairs to affected chapters:
  - Add thread continuations where missing
  - Insert subtle reminders of ongoing threads
  - Ensure proper thread closure

  Document all thread repairs in:
  .claude/data/projects/{project}/fixes/thread_repairs.log
  ```

### Phase 3: Foreshadowing and Payoffs

#### Step 3.1: Analyze Setup-Payoff Issues

Read foreshadowing map:
```
1. Read .claude/data/projects/{project}/validation/foreshadowing_map.json
2. Identify orphaned setups (no payoff)
3. Identify unfounded payoffs (no setup)
```

#### Step 3.2: Fix Foreshadowing Issues

**Execute foreshadowing fix using Task tool:**
- **subagent_type**: "foreshadowing-specialist"
- **description**: "Fix foreshadowing-payoff issues"
- **prompt**: Provide the following instructions:
  ```
  Repair foreshadowing and payoff issues in chapters: $ARGUMENTS

  READ:
  - .claude/data/projects/{project}/validation/foreshadowing_map.json
  - All chapters with setup/payoff issues
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml

  Fix these foreshadowing problems:

  For orphaned setups:
  - Add appropriate payoffs in later chapters
  - Or remove unnecessary setups

  For unfounded payoffs:
  - Add foreshadowing in earlier chapters
  - Or adjust payoffs to not require setup

  WRITE fixes to affected chapters.
  Ensure mystery fairness and reader satisfaction.

  Document changes in:
  .claude/data/projects/{project}/fixes/foreshadowing_fixes.log
  ```

### Phase 4: Character Voice Consistency

#### Step 4.1: Analyze Voice Issues

Read character voice validation:
```
1. Read .claude/data/projects/{project}/validation/character_voices.json
2. Identify characters with voice drift
3. Map chapters needing voice corrections
```

#### Step 4.2: Harmonize Character Voices

**Execute character voice harmonization using Task tool:**
- **subagent_type**: "character-voice-cross-validator"
- **description**: "Fix character voice consistency"
- **prompt**: Provide the following instructions:
  ```
  Fix character voice inconsistencies across chapters: $ARGUMENTS

  READ:
  - .claude/data/projects/{project}/validation/character_voices.json
  - All chapters with voice issues
  - .claude/data/projects/{project}/book_{current_book}/bible.yaml
  - Character voice profiles

  Fix voice consistency:
  - Align dialogue patterns to character profiles
  - Remove author voice intrusions
  - Ensure distinct character voices
  - Maintain voice evolution if intentional

  WRITE corrections to affected chapters.
  Preserve plot while fixing dialogue.

  Document voice fixes in:
  .claude/data/projects/{project}/fixes/voice_fixes.log
  ```

### Phase 5: Pacing Optimization

#### Step 5.1: Analyze Pacing Issues

Read pacing analysis:
```
1. Read .claude/data/projects/{project}/validation/pacing_analysis.json
2. Identify pacing problems (sagging middle, rushed ending, etc.)
3. Plan pacing adjustments
```

#### Step 5.2: Adjust Pacing

**Execute pacing adjustment using Task tool:**
- **subagent_type**: "book-pacing-analyzer"
- **description**: "Fix book pacing issues"
- **prompt**: Provide the following instructions:
  ```
  Fix pacing issues across chapters: $ARGUMENTS

  READ:
  - .claude/data/projects/{project}/validation/pacing_analysis.json
  - Affected chapters
  - Overall story arc

  Fix pacing problems:

  For slow sections:
  - Add tension or conflict
  - Tighten descriptions
  - Increase scene dynamics

  For rushed sections:
  - Add breathing room
  - Develop emotional beats
  - Expand important moments

  WRITE pacing adjustments to affected chapters.
  Maintain story integrity while improving rhythm.

  Document pacing changes in:
  .claude/data/projects/{project}/fixes/pacing_fixes.log
  ```

## Fix Coordination Protocol

### Sequential Execution Order
1. **Timeline/Flow**  ->  Must be fixed first (foundation)
2. **Plot Threads**  ->  After timeline is stable
3. **Foreshadowing**  ->  After threads are connected
4. **Character Voice**  ->  After plot is solid
5. **Pacing**  ->  Final polish

### Conflict Prevention
- Each phase completes before next begins
- Changes are logged to prevent overwrites
- Later fixes respect earlier fixes
- All fixes reference the fix logs

## Validation After Each Phase

**After each phase, validate fixes using Task tool:**
- **subagent_type**: "cross-chapter-flow-validator"
- **description**: "Validate phase fixes"
- **prompt**: Provide the following instructions:
  ```
  Validate that fixes were successful for [phase_name].

  READ:
  - Original validation report
  - Fixed chapter content
  - Fix logs

  Verify:
  - Original issues are resolved
  - No new issues introduced
  - Fixes don't conflict with other chapters

  WRITE validation to:
  .claude/data/projects/{project}/fixes/phase_[name]_validation.json
  ```


## Success Criteria

- All identified cross-chapter issues resolved
- No new continuity problems introduced
- Story flows smoothly from chapter to chapter
- All plot threads properly connected
- Character voices consistent throughout
- Pacing maintains reader engagement
- Fix logs document all changes

## Failure Handling

If unable to fix certain issues:
1. Document unfixable issues in `.claude/data/projects/{project}/fixes/unfixable_issues.md`
2. Explain why they can't be fixed programmatically
3. Suggest manual intervention approaches
4. Consider if Bible needs fundamental changes

## Final Validation

After all phases complete:
```
Run /novel:quality-check-cross $ARGUMENTS
Compare new validation against original
Confirm all critical issues resolved
```

---
**Execute fixes sequentially by phase. Each phase must complete before next begins.**