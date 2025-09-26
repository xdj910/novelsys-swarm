---
description: Generate next book in series
---

# Next Book Generation Command

Automatically generate the next book in a series by detecting current state, planning book transitions, and creating book-specific bible and outline.

## MANDATORY WORKFLOW

### Step 1: Validate Current Project State

1. **Check for active project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - If no project found: Display "[ ] Error: No active project. Use /novel:project-new to create a project first."
   - Extract project_name from current["project"]
   - Confirm: "[x] Active project identified: {project_name}"

2. **Load project metadata:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Extract project type, series information, and current status
   - If project.type != "series": Offer series conversion or exit
   - Confirm: "[x] Project metadata loaded"

3. **Validate series readiness:**
   - Check if series_bible_created: true
   - If false: Display "[ ] Error: Series Bible not found. Create series bible first using /novel:project-new or /novel:bible-create"
   - **CRITICAL**: Use Read tool: `.claude/data/projects/{project_name}/series_bible.yaml`
   - If series_bible.yaml missing, STOP with error: "[ ] Error: Cannot create next book - Series Bible not found or incomplete"
   - **Validate Series Bible completeness:**
     * Check has series_metadata section with title, genre, target_audience
     * Check has author_voice_signature section  
     * Check has universe section with core world rules
     * If missing key sections, STOP with error: "[ ] Error: Series Bible incomplete - missing required sections"
   - Confirm: "[x] Series Bible validated and complete"

### Step 2: Detect Current Series State

1. **Analyze existing books:**
   - Use Glob tool: `.claude/data/projects/{project_name}/book_*/bible.yaml`
   - Count existing book bibles to determine current book count
   - Identify highest book number completed
   - Confirm: "[x] Current series state: {completed_books} books exist"

2. **Determine next book number:**
   - Calculate next_book_number = highest_existing + 1
   - Verify this doesn't exceed planned books from series bible
   - If exceeds plan: Suggest using /novel:extend-series first
   - Confirm: "[x] Next book will be Book {next_book_number}"

3. **Check previous book completion status:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/project.json` or similar
   - Check if previous book meets minimum completion criteria
   - If incomplete: Warn user and offer to continue anyway or finish previous book first
   - Confirm: "[x] Previous book status checked"

### Step 3: Plan Book Transition

1. **Extract previous book end state:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/bible.yaml`
   - Extract character states, unresolved threads, and world status
   - Identify elements that carry forward to next book
   - Confirm: "[x] Previous book end state analyzed"

2. **Consult Series Bible for next book:**
   - Use Read tool: `.claude/data/projects/{project_name}/series_bible.yaml`
   - Extract book_{next_book_number} summary from appropriate phase
   - Identify threads to open, close, and continue
   - Extract planned character development for this book
   - Confirm: "[x] Series Bible guidance for Book {next_book_number} loaded"

3. **Conduct transition mini-brainstorm:**
   - Ask focused questions about book transition:

   **Time Gap Question:**
   "How much time has passed since Book {current} ended?"
   - Options: Immediate continuation/Days/Weeks/Months/Years
   - Default: Based on series bible if specified

   **Opening Situation:**
   "Where do we find the characters as Book {next_book_number} begins?"
   - Character locations and states
   - Changed relationships or circumstances
   - New challenges or opportunities

   **Central Conflict:**
   "What is the main conflict/mystery for Book {next_book_number}?"
   - New case/problem or continuation of existing
   - How it connects to overarching series mystery
   - Personal stakes for main characters

   **Thread Management:**
   "Which plot threads from previous books should be addressed?"
   - Threads to resolve in this book
   - Threads to develop further
   - New threads to introduce

4. **Generate book transition document:**
   - Compile transition planning into structured format
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/transition_plan.yaml`
   - Include time gap, character changes, conflict setup, and thread status
   - Confirm: "[x] Book transition plan created"

### Step 3.5: Validate Transition Continuity

**Ensure transition maintains series continuity:**

1. **Use Task tool with:**
   - subagent_type: "transition-continuity-reviewer"
   - description: "Validate Book {next_book_number} transition"
   - prompt: """
     Review transition continuity from Book {current} to Book {next_book_number}
     - Previous book: book_{current}/
     - Transition plan: book_{next_book_number}/transition_plan.yaml
     - Series Bible: series_bible.yaml
     - Save review to: book_{next_book_number}/transition_review.json
     - Minimum score required: 90
     """

2. **Read review results:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{next_book_number}/transition_review.json`
   - Extract overall_score and critical_issues
   - If score < 90:
     * Display: "[ ] Error: Transition needs revision (score: {score}/100)"
     * Display critical issues and suggested fixes
     * Ask user to revise transition plan
     * Return to Step 3.3
   - Else:
     * Display: "[x] Transition continuity verified ({score}/100)"

### Step 3.6: Book N Specific Brainstorming

**Gather Book {next_book_number} specific information:**

1. **Book role questions:**
   - "How does Book {next_book_number} advance the series arc?"
   - "What new elements are introduced?"
   - "Which threads from previous books are resolved?"
   
2. **Book plot questions:**
   - "What is the main conflict specific to Book {next_book_number}?"
   - "How does it open (considering the transition)?"
   - "What are the major plot points?"
   - "How does it end (resolution vs cliffhanger)?"

3. **Character questions:**
   - "Which new characters appear?"
   - "How do existing characters develop?"
   - "What relationships change?"

4. **Save Book N brainstorming:**
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/book_brainstorming.yaml`
   - Format similar to Book 1 brainstorming structure
   - Confirm: "[x] Book {next_book_number} brainstorming saved"

### Step 3.7: Check Book N Brainstorming Completeness

**Validate Book N brainstorming has sufficient information:**

1. **Use Task tool with:**
   - subagent_type: "brainstorming-completeness-checker"
   - description: "Check Book {next_book_number} brainstorming"
   - prompt: """
     Check completeness of book brainstorming
     - File: .claude/data/projects/{project_name}/book_{next_book_number}/book_brainstorming.yaml
     - Type: book
     - Minimum threshold: 80%
     - Save report to: .claude/data/projects/{project_name}/book_{next_book_number}/book_brainstorming_completeness.json
     """

2. **Handle incompleteness:**
   - If < 80%: Ask follow-up questions and update brainstorming
   - Confirm: "[x] Book {next_book_number} brainstorming {completeness}% complete"

### Step 4: Generate Book-Specific Bible

1. **Create book directory structure:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/book_{next_book_number}`
   - Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/book_{next_book_number}/chapters`
   - Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/book_{next_book_number}/context`
   - Confirm: "[x] Book {next_book_number} directory structure created"

2. **Generate Book Bible using series context:**
   - Use Task tool with:
     * subagent_type: "bible-architect"
     * description: "Generate Book {next_book_number} Bible"
     * prompt: """
       Create Book {next_book_number} Bible for series project '{project_name}'

       SERIES_AWARE_MODE: true

       Context Files to Read:
       - Series Bible: .claude/data/projects/{project_name}/series_bible.yaml
       - Previous Book Bible: .claude/data/projects/{project_name}/book_{current}/bible.yaml
       - Transition Plan: .claude/data/projects/{project_name}/book_{next_book_number}/transition_plan.yaml
       - Original Brainstorming: .claude/data/projects/{project_name}/brainstorming_results.yaml

       Instructions:
       - Use Series Bible as foundation for world, characters, and voice
       - Apply transition plan for book-specific changes
       - Focus on Book {next_book_number} specific plot and character development
       - Maintain consistency with established series elements
       - Include all standard bible sections adapted for this book

       Save to: .claude/data/projects/{project_name}/book_{next_book_number}/bible.yaml
       """
   - Confirm: "[x] Book Bible generation initiated"

3. **Quality review Book Bible:**
   - Use Task tool with:
     * subagent_type: "bible-reviewer"
     * description: "Review Book {next_book_number} Bible"
     * prompt: """
       Review Book Bible quality for Book {next_book_number} of project '{project_name}'

       Files to Review:
       - Book Bible: .claude/data/projects/{project_name}/book_{next_book_number}/bible.yaml
       - Series Bible: .claude/data/projects/{project_name}/series_bible.yaml
       - Previous Book: .claude/data/projects/{project_name}/book_{current}/bible.yaml

       Focus Areas:
       - Consistency with series bible and previous book
       - Quality of book-specific elements
       - Character development continuity
       - Plot integration with series arc

       Save review to: .claude/data/projects/{project_name}/book_{next_book_number}/bible_review.json
       """
   - Confirm: "[x] Book Bible quality review initiated"

### Step 5: Generate Book Outline

1. **Create book outline:**
   - Use Task tool with:
     * subagent_type: "book-outline-architect"
     * description: "Generate Book {next_book_number} Outline"
     * prompt: """
       Create detailed outline for Book {next_book_number} of series project '{project_name}'

       Context Files:
       - Book Bible: .claude/data/projects/{project_name}/book_{next_book_number}/bible.yaml
       - Series Bible: .claude/data/projects/{project_name}/series_bible.yaml
       - Transition Plan: .claude/data/projects/{project_name}/book_{next_book_number}/transition_plan.yaml

       Generate complete chapter-by-chapter outline following book bible specifications.
       Ensure chapters flow logically and serve both book-specific and series-wide narrative needs.

       Save to: .claude/data/projects/{project_name}/book_{next_book_number}/outline.yaml
       """
   - Confirm: "[x] Book outline generation initiated"

2. **Review book outline quality:**
   - Use Task tool with:
     * subagent_type: "book-outline-reviewer"
     * description: "Review Book {next_book_number} Outline"
     * prompt: """
       Review outline quality for Book {next_book_number} of project '{project_name}'

       Files to Review:
       - Outline: .claude/data/projects/{project_name}/book_{next_book_number}/outline.yaml
       - Book Bible: .claude/data/projects/{project_name}/book_{next_book_number}/bible.yaml
       - Series Bible: .claude/data/projects/{project_name}/series_bible.yaml

       Ensure outline serves both standalone book needs and series continuity.

       Save review to: .claude/data/projects/{project_name}/book_{next_book_number}/outline_review.json
       """
   - Confirm: "[x] Book outline quality review initiated"

### Step 6: Update Project Metadata

1. **Update project tracking:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Increment books_completed or books_in_progress
   - Update current_book to {next_book_number}
   - Add book generation timestamp
   - Use Write tool: `.claude/data/projects/{project_name}/project.json`
   - Confirm: "[x] Project metadata updated"

2. **Update current project context:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - Update to reflect new current book if needed
   - Use Write tool: `.claude/data/context/current_project.json`
   - Confirm: "[x] Current project context updated"

### Step 7: Initialize Book Context (Inherit from Previous Book)

1. **Read previous book's final context state:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/context/characters.json`
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/context/plot.json`
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/context/world.json`
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current}/context/quality.json`
   - Confirm: "[x] Previous book context loaded"

2. **Transform context based on transition plan:**
   - **Character context:**
     * Apply time gap changes (age progression, skill development)
     * Update relationships based on transition plan
     * Reset chapter-specific tracking while keeping character knowledge
     * Add new characters from Book N brainstorming
   
   - **Plot context:**
     * Carry forward unresolved threads
     * Archive completed threads from previous book
     * Initialize new Book N plot threads
     * Reset chapter progression tracking
   
   - **World context:**
     * Apply time-based world changes
     * Update locations based on transition
     * Inherit established world rules and systems
     * Add new locations from Book N planning
   
   - **Quality context:**
     * Reset chapter quality scores
     * Maintain series-level quality patterns
     * Initialize Book N quality tracking

3. **Save transformed context for Book N:**
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/context/characters.json`
     * Include inherited character states with transition updates
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/context/plot.json`
     * Include carried threads and new book threads
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/context/world.json`
     * Include evolved world state
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/context/quality.json`
     * Fresh quality tracking for new book
   - Confirm: "[x] Book {next_book_number} context initialized with inherited state"

4. **Create transition summary document:**
   - Use Write tool: `.claude/data/projects/{project_name}/book_{next_book_number}/context/inherited_state.yaml`
   - Document what was inherited vs what changed
   - Track continuity elements for reference
   - Confirm: "[x] Context inheritance documented"

## Error Handling and Edge Cases

### Series Conversion Offer
If project is standalone but user wants next book:
```
"This project was created as standalone. Options:
1. Convert to series and create Book 2
2. Create new related series project
3. Cancel - use different project

Choose option (1-3):"
```

If option 1 selected, guide through quick series conversion using existing agents.

### Completion Warnings
If previous book isn't sufficiently complete:
```
"Book {current} appears incomplete ({completion_percentage}% done).
Options:
1. Continue with Book {next_book_number} anyway
2. Complete Book {current} first (/novel:next-chapter)
3. Cancel

Choose option (1-3):"
```

### Extension Needed
If trying to exceed planned series length:
```
"Series was planned for {planned_books} books, but you're requesting Book {next_book_number}.
Use /novel:extend-series to plan additional books first, then return to create Book {next_book_number}."
```

## Success Output

```
[x] Book {next_book_number} created successfully!

📚 Series: {project_name}
📖 Book {next_book_number}: {book_title}
🎯 Genre: {genre}

📋 Generated Components:
   [x] Book {next_book_number} Bible (quality score: {score}/100)
   [x] Book {next_book_number} Outline ({chapter_count} chapters)
   [x] Transition planning from Book {current}
   [x] Book-specific context initialized

📁 Book Structure:
.claude/data/projects/{project_name}/book_{next_book_number}/
+-- bible.yaml                 [x] Book-specific bible
+-- outline.yaml               [x] Chapter outline
+-- transition_plan.yaml       [x] Transition planning
+-- bible_review.json          [x] Quality review
+-- outline_review.json        [x] Structure review
+-- chapters/                  📝 Ready for chapter generation
+-- context/                   🧠 Book context (inherited & transformed)
    +-- characters.json        [x] Inherited with transitions applied
    +-- plot.json             [x] Threads carried forward
    +-- world.json            [x] World state evolved
    +-- quality.json          [x] Fresh quality tracking
    +-- inherited_state.yaml  [x] Inheritance documentation

💡 Next Steps:
   1. /novel:chapter-start 1 - Begin writing first chapter of Book {next_book_number}
   2. /novel:status - Check overall series progress
   3. Review Book Bible: cat .claude/data/projects/{project_name}/book_{next_book_number}/bible.yaml
```


## Success Criteria

- Validated current project state and series readiness
- Successfully detected next book number and transition needs
- Generated comprehensive book-specific bible and outline
- Updated all project metadata and context appropriately
- Provided clear guidance for next steps in the writing process
[FILE MAY BE TRUNCATED - PLEASE VERIFY]
