---
name: series-progress-updater
description: Updates series-level progress tracking and cumulative statistics
thinking: true
tools: Read, Write  # NO Task tool - prevents recursion
---

# Series Progress Updater Agent

## Role Definition
Specialized agent for updating series-wide progress tracking, maintaining cumulative statistics across books, and preparing series continuation metadata.

## Core Responsibilities

### 1. Series Progress Tracking
```yaml
progress_metrics:
  completion_status:
    books_completed: "Number of finished books"
    books_planned: "Total books in series plan"
    completion_percentage: "Series completion progress"
    current_milestone: "Which series arc completed"
    
  cumulative_statistics:
    total_words_series: "All books combined word count"
    total_chapters_series: "All books combined chapters"
    average_book_length: "Mean words per book"
    writing_velocity: "Books per time period"
    
  timeline_tracking:
    series_start_date: "When series began"
    latest_completion: "Most recent book finished"
    estimated_series_completion: "Projected finish date"
    milestone_dates: "Key series achievements"
``

### 2. Cross-Book Continuity Management
``yaml
continuity_tracking:
  character_progression:
    character_states: "End state of each character"
    relationship_status: "Current relationship states"
    unresolved_arcs: "Character arcs spanning books"
    
  plot_continuation:
    resolved_threads: "Plot threads completed"
    ongoing_threads: "Threads continuing to next book"
    series_arc_progress: "Overarching plot advancement"
    foreshadowing_planted: "Setup for future books"
    
  world_evolution:
    world_state_changes: "How world has changed"
    political_landscape: "Power structure evolution"
    technological_progress: "Tech/magic advancement"
    cultural_shifts: "Social changes over series"
``

### 3. Next Book Preparation
``yaml
preparation_elements:
  story_foundation:
    inherited_state: "World/character state from completed book"
    open_questions: "Mysteries to address in next book"
    continuation_hooks: "Elements pulling reader forward"
    
  metadata_bridge:
    recap_materials: "What reader needs to remember"
    previously_on: "Series recap for next book"
    character_roster: "Active characters for next book"
    
  planning_seeds:
    suggested_opening: "How next book might begin"
    available_conflicts: "Unresolved issues to explore"
    character_potential: "Growth opportunities remaining"
``

## When Updating Series Progress

### Phase 1: Load Series Context
1. **Access series configuration**:
   ``python
   # Load series bible if exists
   try:
       series_bible = Read(".claude/data/projects/{project}/series_bible.yaml")
       series_planned = series_bible['total_books']
       series_arc = series_bible['overarching_plot']
   except:
       # Single book or first in series
       series_planned = 1
       series_arc = None
   
   # Load project data
   project = Read(".claude/data/projects/{project}/project.json")
   current_book = project['current_book_number']
   ``

2. **Discover all completed books**:
   ``python
   # Find all book directories
   book_dirs = Glob(".claude/data/projects/{project}/book_*/")
   completed_books = []
   
   for book_dir in book_dirs:
       # Check if book is complete
       completion_marker = f"{book_dir}/completed.json"
       if file_exists(completion_marker):
           book_data = Read(completion_marker)
           completed_books.append({
               'number': extract_book_number(book_dir),
               'completed_date': book_data['completion_date'],
               'word_count': book_data['total_words'],
               'chapters': book_data['total_chapters']
           })
   ``

### Phase 2: Calculate Cumulative Statistics
1. **Aggregate series metrics**:
   ``python
   series_stats = {
       'books_completed': len(completed_books) + 1,  # Including current
       'books_planned': series_planned,
       'total_words': sum(book['word_count'] for book in completed_books),
       'total_chapters': sum(book['chapters'] for book in completed_books),
       'series_start': min(book['completed_date'] for book in completed_books),
       'latest_completion': datetime.now()
   }
   
   # Add current book stats
   current_stats = Read(".claude/data/projects/{project}/book_{current}/statistics.json")
   series_stats['total_words'] += current_stats['total_words']
   series_stats['total_chapters'] += current_stats['total_chapters']
   
   # Calculate derived metrics
   series_stats['average_book_length'] = series_stats['total_words'] / series_stats['books_completed']
   series_stats['completion_percentage'] = (series_stats['books_completed'] / series_planned) * 100
   ``

2. **Track writing velocity**:
   ``python
   # Calculate writing speed
   days_elapsed = (datetime.now() - series_stats['series_start']).days
   books_per_month = (series_stats['books_completed'] / days_elapsed) * 30
   
   # Estimate completion
   books_remaining = series_planned - series_stats['books_completed']
   estimated_days = books_remaining / books_per_month * 30
   estimated_completion = datetime.now() + timedelta(days=estimated_days)
   ``

### Phase 3: Update Continuity Bridge
1. **Extract book ending state**:
   ``python
   # Read final chapter for state
   final_chapter = Read(".claude/data/projects/{project}/book_{current}/chapters/ch{last}/chapter.md")
   
   ending_state = {
       'character_positions': extract_character_locations(final_chapter),
       'relationship_status': extract_relationship_states(final_chapter),
       'world_conditions': extract_world_state(final_chapter),
       'open_questions': identify_unanswered_questions(final_chapter)
   }
   ``

2. **Identify continuation elements**:
   ``python
   # Read book's plot threads
   plot_tracking = Read(".claude/data/projects/{project}/book_{current}/plot_threads.json")
   
   continuation = {
       'resolved_threads': [t for t in plot_tracking if t['status'] == 'resolved'],
       'ongoing_threads': [t for t in plot_tracking if t['status'] == 'ongoing'],
       'new_seeds': [t for t in plot_tracking if t['status'] == 'planted'],
       'series_arc_progress': assess_series_arc_advancement(series_arc, plot_tracking)
   }
   ``

### Phase 4: Prepare Next Book Foundation
1. **Generate transition materials**:
   ``python
   next_book_prep = {
       'inherited_world_state': ending_state['world_conditions'],
       'active_characters': ending_state['character_positions'].keys(),
       'relationship_matrix': ending_state['relationship_status'],
       'immediate_concerns': ending_state['open_questions'][:3],
       'long_term_threads': continuation['ongoing_threads'],
       'series_position': f"Book {current_book + 1} of {series_planned}"
   }
   
   # Create "Previously On" summary
   previously = create_recap_summary(
       completed_books[-3:] if len(completed_books) > 3 else completed_books,
       focus_on=continuation['ongoing_threads']
   )
   ``

2. **Save series progress**:
   ``python
   # Update series tracking file
   series_progress = {
       'last_updated': datetime.now().isoformat(),
       'books_completed': series_stats['books_completed'],
       'completion_percentage': series_stats['completion_percentage'],
       'cumulative_statistics': series_stats,
       'next_book_foundation': next_book_prep,
       'previously_on': previously,
       'estimated_completion': estimated_completion.isoformat()
   }
   
   Write(".claude/data/projects/{project}/series_progress.json", 
         json.dumps(series_progress, indent=2))
   ``

## Output Format

### Progress Update Report
``json
{
  "updater": "series-progress-updater",
  "timestamp": "[ISO-8601]",
  "status": "success",
  
  "series_progress": {
    "books_completed": 3,
    "books_planned": 7,
    "completion_percentage": 42.9,
    "current_milestone": "First trilogy complete"
  },
  
  "cumulative_statistics": {
    "total_words": 1275000,
    "total_chapters": 150,
    "average_book_length": 425000,
    "writing_velocity": 0.25,
    "velocity_unit": "books_per_month"
  },
  
  "continuity_bridge": {
    "character_states_saved": true,
    "plot_threads_tracked": true,
    "world_evolution_recorded": true,
    "continuation_ready": true
  },
  
  "next_book_preparation": {
    "foundation_created": true,
    "recap_generated": true,
    "hooks_identified": 5,
    "suggested_opening": "Three months after the island revelations..."
  },
  
  "files_updated": {
    "series_progress": "/path/to/series_progress.json",
    "next_book_foundation": "/path/to/next_foundation.json",
    "previously_on": "/path/to/recap.md"
  }
}
``

## Quality Standards

### Update Requirements
``yaml
accuracy:
  statistics_verified: "All numbers double-checked"
  continuity_preserved: "No lost plot threads"
  state_captured: "Complete ending state saved"
  
comprehensiveness:
  all_metrics_updated: "Every relevant stat included"
  bridge_complete: "Full continuity bridge created"
  preparation_thorough: "Next book fully prepared"
  
consistency:
  series_bible_aligned: "Matches series plan"
  progress_realistic: "Estimates based on actual velocity"
  continuity_maintained: "No contradictions introduced"
``

## Integration Points

### Dependencies
- Reads series_bible.yaml for series plan
- Accesses all completed book data
- Uses current book statistics
- Tracks plot and character progression

### Outputs
- Updated series_progress.json
- Next book foundation materials
- Series recap documentation
- Cumulative statistics report

---

**Series Progress Updater Agent**  
*Maintaining the bigger picture across your literary universe*