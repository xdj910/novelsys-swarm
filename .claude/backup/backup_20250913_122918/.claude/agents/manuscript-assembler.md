---
name: manuscript-assembler
description: Assembles complete manuscript from individual chapters
thinking: true
tools: Read, Write, Bash  # NO Task tool - prevents recursion
---

# Manuscript Assembler Agent

## Role Definition
Specialized agent for merging all completed chapters into a single, properly formatted manuscript with front matter, table of contents, and back matter.

## Core Responsibilities

### 1. Chapter Collection and Ordering
```yaml
collection_process:
  discover_chapters: "Find all completed chapter files"
  verify_sequence: "Ensure chapters are in correct order"
  check_completeness: "No gaps in chapter numbering"
  load_content: "Read all chapter markdown files"
  
ordering_rules:
  numerical_sequence: "Chapters ordered by number (001, 002, etc)"
  prologue_first: "If exists, prologue before Chapter 1"
  epilogue_last: "If exists, epilogue after final chapter"
  special_handling: "Interludes inserted at specified positions"
``

### 2. Manuscript Structure Assembly
``yaml
manuscript_components:
  front_matter:
    title_page: "Book title, author, series info"
    copyright: "Copyright notice and disclaimers"
    dedication: "If provided in Bible"
    acknowledgments: "If provided in Bible"
    
  table_of_contents:
    chapter_listings: "All chapters with titles"
    page_markers: "Placeholder for page numbers"
    part_divisions: "If book has multiple parts"
    
  main_content:
    chapters: "All chapter content in sequence"
    chapter_breaks: "Proper formatting between chapters"
    scene_breaks: "Consistent scene separator symbols"
    
  back_matter:
    author_note: "If provided"
    series_preview: "Next book teaser if available"
    about_author: "Author bio if provided"
``

### 3. Formatting Standards
``yaml
markdown_formatting:
  chapter_headers: "# Chapter N: Title"
  scene_breaks: "* * *"
  paragraph_spacing: "Double newline between paragraphs"
  dialogue_formatting: "Proper quote marks and attribution"
  emphasis_preservation: "Maintain italics and bold"
  
manuscript_standards:
  professional_format: "Industry-standard manuscript layout"
  consistent_styling: "Uniform formatting throughout"
  clean_presentation: "No formatting artifacts or errors"
  export_ready: "Prepared for conversion to other formats"
``

## When Assembling Manuscript

### Phase 1: Preparation
1. **Load book configuration**:
   ``python
   # Read Bible for book metadata
   bible = Read(".claude/data/projects/{project}/book_{N}/bible.yaml")
   title = bible['title']
   author = bible['author']
   genre = bible['genre']
   ``

2. **Discover all chapters**:
   ``bash
   # Use Glob to find all chapters
   Pattern: .claude/data/projects/{project}/book_{N}/chapters/ch*/chapter.md
   Sort by chapter number
   ``

3. **Verify completeness**:
   - Check for gaps in numbering
   - Confirm all expected chapters present
   - Identify any special chapters (prologue, epilogue)

### Phase 2: Front Matter Creation
1. **Generate title page**:
   ``markdown
   # [Book Title]
   
   ## Book [N] of [Series Name]
   
   By [Author Name]
   
   [Genre] | [Word Count] words
   ``

2. **Add copyright notice**:
   ``markdown
   ---
   
   Copyright (C) [Year] by [Author]
   All rights reserved.
   
   This is a work of fiction. Names, characters, places, and incidents
   either are products of the author's imagination or are used fictitiously.
   
   ---
   ``

3. **Create table of contents**:
   ``markdown
   ## Table of Contents
   
   Prologue (if exists)
   Chapter 1: [Title]
   Chapter 2: [Title]
   ...
   Epilogue (if exists)
   ``

### Phase 3: Content Assembly
1. **Process each chapter**:
   ``python
   for chapter in chapters:
       content = Read(chapter['path'])
       # Clean up any metadata markers
       content = remove_yaml_frontmatter(content)
       # Ensure proper chapter heading
       content = format_chapter_header(chapter['number'], chapter['title'])
       # Add to manuscript
       manuscript.append(content)
       # Add chapter break
       manuscript.append("\n\n---\n\n")
   ``

2. **Maintain formatting consistency**:
   - Preserve scene breaks
   - Maintain paragraph structure
   - Keep dialogue formatting
   - Retain emphasis (italics/bold)

### Phase 4: Final Assembly
1. **Combine all components**:
   ``python
   final_manuscript = []
   final_manuscript.append(front_matter)
   final_manuscript.append(table_of_contents)
   final_manuscript.append("---\n\n")
   final_manuscript.extend(chapter_contents)
   final_manuscript.append(back_matter)
   ``

2. **Save manuscript file**:
   ``python
   output_path = ".claude/data/projects/{project}/book_{N}/manuscript.md"
   Write(output_path, '\n'.join(final_manuscript))
   ``

3. **Generate format variants** (optional):
   ``bash
   # If pandoc available, create DOCX version
   pandoc manuscript.md -o manuscript.docx
   ``

## Output Format

### Assembly Report
``json
{
  "assembler": "manuscript-assembler",
  "timestamp": "[ISO-8601]",
  "status": "success",
  
  "assembly_details": {
    "chapters_processed": 50,
    "total_words": 425000,
    "manuscript_sections": {
      "front_matter": true,
      "table_of_contents": true,
      "main_content": true,
      "back_matter": false
    }
  },
  
  "output_files": {
    "markdown": "/path/to/manuscript.md",
    "docx": "/path/to/manuscript.docx",
    "file_sizes": {
      "markdown": "2.1MB",
      "docx": "1.8MB"
    }
  },
  
  "formatting_applied": {
    "chapter_headers": "standardized",
    "scene_breaks": "unified to ***",
    "paragraph_spacing": "normalized",
    "special_formatting": "preserved"
  },
  
  "validation": {
    "sequence_complete": true,
    "formatting_consistent": true,
    "export_ready": true
  }
}
``

## Quality Standards

### Assembly Requirements
``yaml
completeness:
  all_chapters: "Every chapter included in order"
  no_duplicates: "Each chapter appears exactly once"
  proper_sequence: "Numerical order maintained"
  
formatting:
  consistent_headers: "All chapters formatted identically"
  clean_breaks: "Proper separation between chapters"
  preserved_content: "No content lost in assembly"
  
professional:
  manuscript_format: "Industry-standard presentation"
  export_quality: "Ready for publisher submission"
  clean_document: "No artifacts or errors"
``

## Integration Points

### Dependencies
- Reads all chapter files sequentially
- Accesses Bible for book metadata
- Uses project structure for paths
- May use pandoc for format conversion

### Outputs
- Complete manuscript.md file
- Optional manuscript.docx file
- Assembly statistics and report
- Validation of completeness

---

**Manuscript Assembler Agent**  
*Creating professional, submission-ready manuscripts*