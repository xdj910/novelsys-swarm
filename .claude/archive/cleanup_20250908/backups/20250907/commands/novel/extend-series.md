---
description: Extend series with additional books
argument-hint: <num_books> e.g., "3" to add 3 more books
---

# Series Extension Command

Extend an existing series beyond its original planned length in response to market success, reader demand, or creative vision expansion. Uses incremental approach to maintain series consistency.

## MANDATORY WORKFLOW

### Step 1: Validate Extension Prerequisites

1. **Check for active series project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - If no project: Display "[ ] Error: No active project. Use /novel:project-new to create a series first."
   - Extract project_name from current["project"]
   - Confirm: "[x] Active project identified: {project_name}"

2. **Validate project is a series:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Check if project.type == "series"
   - If not series: Display "[ ] Error: Project is not a series. Use /novel:next-book for standalone sequels or convert to series first."
   - Confirm: "[x] Series project validated"

3. **Check series bible exists:**
   - Use Read tool: `.claude/data/projects/{project_name}/series_bible.yaml`
   - If not found: Display "[ ] Error: Series Bible not found. Create series bible first."
   - Confirm: "[x] Series Bible located and accessible"

4. **Analyze current series status:**
   - Parse series_bible.yaml to identify existing phases
   - Count current books planned and phases completed
   - Identify extension readiness indicators
   - Confirm: "[x] Current series status analyzed"

### Step 2: Assess Extension Context

1. **Review existing series structure:**
   - Extract current books_planned from series bible
   - Identify which books are completed vs. planned
   - Analyze existing plot threads and their resolution status
   - Use Glob tool: `.claude/data/projects/{project_name}/book_*/bible.yaml` to count completed books
   - Confirm: "[x] Series structure assessed: {completed_books}/{planned_books} books"

2. **Check for previous extensions:**
   - Scan series bible for existing phase_N_extension sections
   - Count how many extensions have already been made
   - Identify current maximum planned book count
   - Confirm: "[x] Extension history analyzed"

3. **Validate extension readiness:**
   - Ensure at least original phase is substantially complete
   - Check for unresolved plot threads that could support extension
   - Verify no series-ending elements have been prematurely used
   - Confirm: "[x] Series ready for extension" or provide specific blockers

### Step 3: Gather Extension Requirements

Conduct focused planning session for series extension:

1. **Market Context Questions:**

   **"What's driving this series extension?"**
   - Reader demand and feedback
   - Sales performance exceeding expectations
   - Creative vision expansion
   - Market opportunity identification
   - Publisher/platform request

   **"How many additional books are you planning?"**
   - Conservative extension (2-3 books)
   - Moderate expansion (4-6 books)
   - Major extension (7+ books)
   - Open-ended based on success

2. **Creative Direction Questions:**

   **"What new story territory will the extension explore?"**
   - Deeper exploration of existing mysteries
   - New geographical or temporal settings
   - Introduction of new major characters
   - Escalation to larger stakes/scope
   - Exploration of character backstories

   **"How should the extension integrate with existing series?"**
   - Seamless continuation of existing arcs
   - New arc that references but stands apart
   - Prequel elements mixed with continuation
   - Multiple timeline or perspective approach

3. **Thread Management Questions:**

   **"Which current plot threads should the extension develop?"**
   - List unresolved elements from existing books
   - Identify seeds planted for future development
   - Determine which threads need extension vs. resolution

   **"What new mysteries or conflicts should be introduced?"**
   - New overarching mystery for extended series
   - Personal conflicts for character development
   - World-building expansion opportunities
   - Genre or tone evolution possibilities

### Step 4: Generate Extension Plan

1. **Create extension directory:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/extension_planning`
   - Confirm: "[x] Extension planning directory created"

2. **Design extension structure:**
   - Use Task tool with:
     * subagent_type: "series-bible-architect"
     * description: "Generate Series Extension Plan"
     * prompt: """
       Create series extension for project '{project_name}'

       EXTENSION_MODE: true

       Context to Read:
       - Existing Series Bible: .claude/data/projects/{project_name}/series_bible.yaml
       - Project Status: .claude/data/projects/{project_name}/project.json
       - All Book Bibles: Use Glob to read .claude/data/projects/{project_name}/book_*/bible.yaml

       Extension Requirements:
       - Additional books: {additional_books}
       - Extension driver: {market_context}
       - New story focus: {creative_direction}
       - Thread development: {thread_management}
       - Integration approach: {integration_style}

       Generate new phase_N_extension section for series bible.
       Maintain consistency with existing content.
       Create detailed planning for each additional book.
       Ensure smooth integration with completed books.

       Append extension to: .claude/data/projects/{project_name}/series_bible.yaml
       """
   - Confirm: "[x] Extension plan generation initiated"

### Step 5: Review Extension Quality

1. **Quality review extension:**
   - Use Task tool with:
     * subagent_type: "series-bible-reviewer"
     * description: "Review Series Extension Plan"
     * prompt: """
       Review series extension quality for project '{project_name}'

       EXTENSION_REVIEW: true

       Files to Review:
       - Extended Series Bible: .claude/data/projects/{project_name}/series_bible.yaml
       - Original Project Context: .claude/data/projects/{project_name}/project.json
       - Existing Book Bibles: Use Glob for .claude/data/projects/{project_name}/book_*/bible.yaml

       Review Focus:
       - Integration quality with existing series
       - Extension coherence and sustainability
       - Character arc continuation logic
       - Plot thread development appropriateness
       - Market viability of extended series

       Apply extension-specific scoring criteria.
       Focus on compatibility and enhancement rather than replacement.

       Save review to: .claude/data/projects/{project_name}/extension_planning/extension_review.json
       """
   - Confirm: "[x] Extension quality review initiated"

2. **Process review results:**
   - Use Read tool: `.claude/data/projects/{project_name}/extension_planning/extension_review.json`
   - Extract overall score and critical issues
   - If score < 95: Iterate extension planning
   - Display review summary to user
   - Confirm: "[x] Extension review processed"

### Step 6: Finalize Extension (if approved)

1. **Update project metadata:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Update books_planned to new total
   - Add extension history entry with date and reason
   - Update series_status to "extended"
   - Use Write tool: `.claude/data/projects/{project_name}/project.json`
   - Confirm: "[x] Project metadata updated with extension"

2. **Create extension documentation:**
   - Use Write tool: `.claude/data/projects/{project_name}/extension_planning/extension_summary.md`
   - Document extension rationale, new book summaries, and integration plan
   - Include timeline for writing extended books
   - Confirm: "[x] Extension documentation created"

3. **Prepare for next book generation:**
   - Identify which book should be written next
   - Verify readiness for /novel:next-book command
   - Display guidance for continuing with extended series
   - Confirm: "[x] Next steps prepared"

## Extension Quality Loop

If extension review score < 95, iterate:

### Quality Iteration Process

1. **Initialize Extension Version**
   - Set extension_version to 1
   - Set max_iterations to 3
   - Set quality_score to 0

2. **Iterative Review Loop**
   - WHILE quality_score < 95 AND extension_version <= max_iterations:
     - Review current extension using bible-reviewer agent
     - Get quality_score from review results
     - IF quality_score < 95:
       - Improve extension plan based on feedback
       - Increment extension_version
     - ELSE:
       - Break from loop

3. **Finalization Decision**
   - IF quality_score >= 95:
     - Finalize extension and update series bible
   - ELSE:
     - Request manual intervention for quality issues

## Error Handling

### Series Not Ready for Extension
```
"Series extension blocked. Issues found:
- Book {N} incomplete (only {completion}% done)
- Critical plot thread unresolved in current planning
- Extension would create continuity conflicts

Complete current phase before extending, or address these issues:
{specific_issues}

Use /novel:status to check current series state."
```

### Extension Conflicts
```
"Extension plan conflicts detected:
- Character arc already concluded in Book {N}
- Major mystery already fully revealed
- Series already has satisfying conclusion points

Suggested fixes:
1. Revise extension to introduce new mysteries
2. Create parallel storylines with existing characters
3. Consider spin-off series instead of extension

Revise extension plan? (y/n)"
```

### Over-Extension Warning
```
"Warning: Series would have {total_books} books after extension.
Market research suggests {genre} series over {threshold} books may face reader fatigue.

Considerations:
- Average successful {genre} series length: {average} books
- Reader retention typically drops after book {dropoff_point}

Proceed with extension anyway? (y/n)
Alternative: Consider breaking into multiple connected series."
```

## Success Output

```
[x] Series extended successfully!

📚 Series: {project_name}
📈 Extension: Phase {phase_number}
🎯 Books Added: {additional_books} (Total: {original_books} -> {new_total})

📋 Extension Summary:
   🎭 New Theme: {extension_theme}
   🧩 Integration: {integration_approach}
   📖 Books {range}: {book_titles}
   ⭐ Extension Score: {quality_score}/100

📊 Series Overview:
   Original Phase: Books 1-{original_count} [x]
   Extension Phase: Books {start}-{end} 📝 Ready to write

📁 Updated Structure:
.claude/data/projects/{project_name}/
├── series_bible.yaml           [x] Extended with Phase {N}
├── extension_planning/         📊 Extension documentation
│   ├── extension_review.json   [x] Quality review
│   └── extension_summary.md    [x] Extension overview
└── book_001/ -> book_{original} [x] Existing books preserved

🎬 Reader Experience:
   * Phase 1 Conclusion: {original_ending}
   * Phase {N} Opening: {extension_opening}
   * New Overarching Mystery: {new_mystery}
   * Extended Character Journeys: {character_growth}

💡 Next Steps:
   1. /novel:next-book - Create Book {next_book_number}
   2. /novel:status - View extended series progress
   3. Review Extension Plan: cat .claude/data/projects/{project_name}/extension_planning/extension_summary.md

🎯 Writing Schedule Recommendation:
   - Complete existing books before starting extension
   - Maintain reader engagement with consistent release schedule
   - Consider reader feedback between phases
```

## Market Intelligence Integration

### Success Metrics Tracking
- Monitor which elements drove extension decision
- Track reader feedback on series expansion
- Document market performance of extended series
- Create template for future extensions

### Extension Best Practices
- Maintain series voice and quality standards
- Provide satisfying conclusion points for different series lengths
- Avoid over-extending beyond natural story boundaries
- Consider reader fatigue and market saturation


## Success Criteria

- Validated series readiness for extension
- Generated high-quality extension plan (>=95 score)
- Successfully integrated extension with existing series
- Updated all project metadata and documentation
- Prepared clear path for writing extended books
- Maintained series consistency and quality standards
[FILE MAY BE TRUNCATED - PLEASE VERIFY]
