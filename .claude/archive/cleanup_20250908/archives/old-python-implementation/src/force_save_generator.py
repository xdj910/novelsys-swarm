#!/usr/bin/env python3
"""
Force Save Generator - Makes agents ACTUALLY save files
Version: 7.0 - Ultra explicit save instructions
"""

def generate_outline_prompt(chapter_num, project):
    """Generate outline prompt that FORCES saving"""
    return f"""You are bible-architect creating outline for chapter {chapter_num}.

STEP 1: READ THESE FILES
- data/projects/{project}/bible.yaml
- data/projects/{project}/chapters/ch{chapter_num-1:03d}/content.md (if exists)
- .claude/agents/shared/entity_dictionary.yaml

STEP 2: CREATE OUTLINE
Generate a JSON outline with:
- chapter: {chapter_num}
- title: "Chapter Title"
- scenes: [3-5 scene objects]
- character_arcs: {{}}
- plot_advancement: "how story moves forward"

STEP 3: MANDATORY SAVE ACTION
YOU MUST DO THIS - IT IS NOT OPTIONAL:

1. First, create the outline content as a JSON string
2. Then execute this EXACT command:

Write("data/projects/{project}/chapters/ch{chapter_num:03d}/outline.json", <your_outline_json>)

YOU MUST USE THE Write TOOL. This is MANDATORY.
If you do not use Write tool, the task FAILS.

CONFIRMATION REQUIRED:
After using Write tool, you must say:
"File saved to data/projects/{project}/chapters/ch{chapter_num:03d}/outline.json"

DO NOT JUST RETURN THE CONTENT.
YOU MUST USE Write TOOL TO SAVE IT.
THIS IS THE MOST IMPORTANT PART OF YOUR TASK."""

def generate_draft_prompt(chapter_num, project):
    """Generate draft prompt that FORCES saving"""
    return f"""You are scene-generator writing chapter {chapter_num}.

STEP 1: READ THE OUTLINE
Read: data/projects/{project}/chapters/ch{chapter_num:03d}/outline.json
If this file doesn't exist, STOP and report the error.

STEP 2: READ CONTEXT
- data/projects/{project}/bible.yaml
- .claude/agents/shared/entity_dictionary.yaml

STEP 3: WRITE THE CHAPTER
Generate 3000-5000 words following the outline.
Start with: "Chapter {chapter_num}: [Title from outline]"

STEP 4: MANDATORY SAVE ACTION
THIS IS NOT OPTIONAL - YOU MUST DO THIS:

Use the Write tool to save your chapter:
Write("data/projects/{project}/chapters/ch{chapter_num:03d}/draft_v1.md", <your_chapter_text>)

YOU MUST USE Write TOOL.
DO NOT SKIP THIS STEP.
THE TASK FAILS IF YOU DON'T SAVE.

Confirm by saying: "Chapter saved to draft_v1.md" """

print("Force Save Generator Ready")
print("This version makes saving MANDATORY and EXPLICIT")