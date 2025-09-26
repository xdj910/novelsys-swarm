---
description: Write the next chapter in sequence
---

# Next Chapter Command

Automatically write the next chapter in your current project.

## Purpose

Simple command to continue writing without remembering chapter numbers.
Finds the last completed chapter and writes the next one.

## EXECUTION FLOW

### Step 1: Identify Current Progress

1. **Get current project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - Extract project_name
   - If missing, Display: "[ ] Error: No active project. Use /novel:project-switch first"

2. **Find last completed chapter:**
   - Use Glob tool: `.claude/data/projects/{project}/book_{current_book}/chapters/ch*/meta.json`
   - Find highest numbered chapter with quality_score >= 95
   - If no chapters exist, next_chapter = 1
   - Otherwise, next_chapter = last_completed + 1

3. **Verify Bible exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
   - If missing, Display: "[ ] Error: Bible not found. Run /novel:bible-create first"

### Step 2: Display Status

Show user what will happen:

```
📖 Project: {project_name}
📊 Progress: {completed_chapters} chapters completed
✍️ Starting: Chapter {next_chapter}

Initiating chapter generation...
```

### Step 3: Generate Next Chapter

Simply invoke chapter-start with the calculated number:

```bash
/novel:chapter-start {next_chapter}
```

This will:
- Generate complete chapter through all enhancement steps
- Score quality
- If >=95, trigger unified-update-pipeline
- Update all 6 core files automatically

### Step 4: Post-Generation Summary

After chapter-start completes, display:

```
[x] Chapter {next_chapter} Complete!
📊 Quality Score: {score}/100
📝 Word Count: {words}

{if score >= 95}
✨ High quality achieved! All systems updated:
- Entity dictionary learned new variations
- Project statistics updated
- Character/plot/world context enriched

Next: /novel:next-chapter to continue writing
{else}
WARNING:️ Warning: Quality below threshold ({score}/100)
Suggestion: /novel:smart-fix {next_chapter}
{endif}
```

## ERROR HANDLING

### No Chapters Yet
```
Starting your first chapter!
 ->  /novel:chapter-start 1
```

### Bible Missing
```
[ ] Error: Cannot write chapters without Bible
Please run: /novel:bible-create
```

### Project Not Set
```
[ ] Error: No active project
Please run: /novel:project-switch <project_name>
Or create new: /novel:project-new <project_name>
```

## SUCCESS CRITERIA

- Correctly identifies next chapter number
- Invokes chapter-start with right number
- Clear feedback to user
- Handles edge cases gracefully

## Usage Examples

```bash
# First time
/novel:next-chapter
> Starting: Chapter 1

# After writing 5 chapters
/novel:next-chapter  
> Progress: 5 chapters completed
> Starting: Chapter 6

# Keep writing
/novel:next-chapter
/novel:next-chapter
/novel:next-chapter
# Writes chapters 7, 8, 9...
```

## Integration Notes

- This is a **wrapper** around chapter-start
- All quality checks and updates handled by chapter-start
- No complex resume logic needed
- Simple, predictable behavior

---
**Simple command for continuous novel writing.**