---
name: parallel-quality-check
description: Run parallel quality validation for multiple chapters
tools:
  - Task
  - Read
  - TodoWrite
  - Glob
  - Bash
---

# Parallel Quality Check Command

WARNING:️  **DEPRECATED**: This command has been superseded by the new two-phase approach:
- `/novel:quality-check-individual` - Phase 1: Individual chapter validation
- `/novel:quality-check-cross` - Phase 2: Cross-chapter analysis

**Why the change?**
- Better quality gates: Fix individual issues before cross-chapter analysis
- More efficient: No wasted cross-chapter validation on broken chapters
- User control: Choose when to run each phase
- Clearer results: Separate reporting for different validation types

**Migration Guide:**
```bash
# Old way (deprecated):
/novel:parallel-quality-check all

# New way (recommended):
/novel:quality-check-individual all    # First: fix individual chapters
/novel:quality-check-cross all         # Then: validate cross-chapter flow
```

---

## Legacy Implementation (Still Functional)

Run parallel quality validation for chapters: **$ARGUMENTS**

## Validation

First, check if `$ARGUMENTS` exists:

```bash
# If empty, stop and show usage
if [ -z "$ARGUMENTS" ]; then
    echo "[ ] No chapters specified."
    echo ""
    echo "Usage: /novel:parallel-quality-check [all|1-5|1,3,5|odd|even]"
    echo ""
    echo "Examples:"
    echo "  /novel:parallel-quality-check all      # Check all chapters"
    echo "  /novel:parallel-quality-check 1-11     # Check chapters 1 to 11"
    echo "  /novel:parallel-quality-check 1,3,5,7  # Check specific chapters"
    echo "  /novel:parallel-quality-check odd      # Check odd chapters"
    exit 1
fi
```

If validation fails, STOP execution and display the error message above.

## Processing Arguments

Once `$ARGUMENTS` is confirmed to exist, parse it:

- **"all"**  ->  Find all chapters in `data/projects/*/chapters/ch*/content.md`
- **"X-Y"**  ->  Parse range (e.g., "1-11" means chapters 1 through 11)
- **"X,Y,Z"**  ->  Parse list (e.g., "1,3,5,7" means those specific chapters)
- **"odd"/"even"**  ->  Filter chapters by pattern
- **Single number**  ->  Check that one chapter only

## Phase 1: Individual Chapter Validation

**TRUE PARALLEL EXECUTION**: Launch ALL agents simultaneously (no dependencies!)
**CRITICAL**: You MUST launch EXACTLY 4 agents per chapter IN PARALLEL

```python
print(f"Phase 1: Launching {4 * len(chapters_to_check)} agents in PARALLEL...")

# Launch ALL agents simultaneously - no waiting between calls!
for chapter_num in chapters_to_check:
    # These 4 agents have NO dependencies - launch them ALL at once
    Task("continuity-guard-specialist", 
         f"Check chapter {chapter_num} consistency. Read: data/projects/*/chapters/ch{chapter_num:03d}/content.md")
    
    Task("plot-hole-detector", 
         f"Find issues in chapter {chapter_num}. Read: data/projects/*/chapters/ch{chapter_num:03d}/content.md")
    
    Task("bible-compliance-validator", 
         f"Validate Bible compliance for chapter {chapter_num}. "
         f"Read BOTH: chapters/ch{chapter_num:03d}/content.md AND bible.yaml")
    
    Task("quality-scorer", 
         f"Score chapter {chapter_num}. Read: data/projects/*/chapters/ch{chapter_num:03d}/content.md")

print(f"[x] Phase 1: Launched {4 * len(chapters_to_check)} parallel agents")
print("All agents running simultaneously - no waiting!")

# WAIT FOR PHASE 1 COMPLETION
print("Waiting for all Phase 1 agents to complete...")
# All Task agents should complete before proceeding
print("[x] Phase 1 agents completed")
```

## Phase 2: Cross-Chapter Validation

**TIMING**: Phase 2 starts ONLY AFTER all Phase 1 agents have completed.
**CRITICAL**: After Phase 1 completes, you MUST launch ALL 5 cross-chapter agents.
**DO NOT SKIP - THESE ARE REQUIRED FOR COMPLETE VALIDATION**

```python
print("Starting Phase 2: Cross-Chapter Validation...")

# Step 1: Define the 5 REQUIRED cross-chapter agents
CROSS_CHAPTER_AGENTS = [
    "cross-chapter-flow-validator",
    "story-thread-tracker",
    "foreshadowing-payoff-mapper",
    "book-pacing-analyzer",
    "character-voice-cross-validator"
]

# Launch ALL 5 agents simultaneously - they have no dependencies!
print("Phase 2: Launching 5 cross-chapter agents in PARALLEL...")

Task("cross-chapter-flow-validator",
     "Validate all adjacent chapter transitions. "
     "Read all chapters and check Ch(n) -> Ch(n+1) flow, "
     "time continuity, and narrative momentum.")

Task("story-thread-tracker",
     "Track all plot threads and character arcs across chapters. "
     "Identify abandoned threads, validate arc progression, "
     "and ensure all storylines are properly developed.")

Task("foreshadowing-payoff-mapper",
     "Map all foreshadowing setups to payoffs. "
     "Identify orphaned setups, unfounded reveals, "
     "and validate Chekhov's gun principle.")

Task("book-pacing-analyzer",
     "Analyze overall book pacing arc across all chapters. "
     "Detect sagging middle, rushed endings, and ensure "
     "proper story rhythm from beginning to end.")

Task("character-voice-cross-validator",
     "Validate character voice consistency across all chapters. "
     "Detect voice drift, ensure distinctiveness, "
     "and prevent author voice intrusion.")

print("[x] Phase 2: Launched 5 parallel cross-chapter agents")
print("All cross-chapter agents running simultaneously!")
```

### Cross-Chapter Validation Coverage:
- **Adjacent transitions**: cross-chapter-flow-validator
- **Plot threads & Character arcs**: story-thread-tracker  
- **Foreshadowing lifecycle**: foreshadowing-payoff-mapper
- **Overall pacing arc**: book-pacing-analyzer
- **Voice consistency**: character-voice-cross-validator

## Output Format

### Summary Report
```
PARALLEL QUALITY CHECK RESULTS
==============================
Chapters Checked: [list]
Average Score: X/100
Pass Threshold: 95/100

PASSED: [chapters with 95+]
FAILED: [chapters below 95]

Key Issues:
1. [Most common problem]
2. [Second most common]
3. [Third most common]
```

### Context Firewall

All agent outputs use Context Firewall:
- Main thread receives 50-char summaries
- Full reports saved to `.claude/context/details/`
- Token savings: ~70%

## Execution Checklist

**MANDATORY EXECUTION VERIFICATION**:
- [ ] Phase 1: Launched 4 agents x N chapters = 4N total agents
- [ ] Phase 2: Launched exactly 5 cross-chapter agents
- [ ] Total agents launched: 4N + 5

**Example for 11 chapters**:
- Phase 1: 4 x 11 = 44 agent tasks
- Phase 2: 5 cross-chapter agents
- Total: 49 agent tasks

**IF YOU DID NOT LAUNCH ALL AGENTS, THE COMMAND HAS FAILED!**

## Error Handling

If no chapters found:
```
[ ] No chapters found in current project.
First create chapters with: /novel:chapter-start 1
```

If project not initialized:
```
[ ] No active project.
Initialize with: /novel:init [project-name]
```

If agents not launched:
```
[ ] Failed to launch all required agents.
Phase 1 requires: 4 agents per chapter
Phase 2 requires: 5 cross-chapter agents
Please re-run the command and ensure all agents are launched.
```