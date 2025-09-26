#!/usr/bin/env python3
"""
Chapter Generation Runner for Claude Code Integration
This script is designed to be called by Claude Code's Task tool
"""

import json
import sys
from pathlib import Path

def create_task_calls():
    """
    Generate the actual Task tool calls that Claude Code will execute
    This returns the prompts that need to be sent to each agent
    """
    
    # Read current project
    current_project_path = Path("data/context/current_project.json")
    if current_project_path.exists():
        with open(current_project_path, 'r') as f:
            current_project = json.load(f).get('project')
    else:
        print("[ERROR] No current project set. Use /novel:project-switch first")
        return None
    
    if len(sys.argv) < 2:
        print("[ERROR] Chapter number required")
        return None
    
    chapter_num = int(sys.argv[1])
    project_path = Path(f"data/projects/{current_project}")
    chapter_path = project_path / f"chapters/ch{chapter_num:03d}"
    
    # Create directory
    chapter_path.mkdir(parents=True, exist_ok=True)
    
    # Generate task sequence
    tasks = []
    
    # Stage 1: Outline
    tasks.append({
        "stage": "1. Generate Outline",
        "agent": "bible-architect",
        "description": f"Generate outline for chapter {chapter_num}",
        "prompt": f"""Create detailed outline for chapter {chapter_num} of {current_project}.

Read these resources:
1. Bible: data/projects/{current_project}/bible.yaml
2. Previous chapter (if exists): data/projects/{current_project}/chapters/ch{chapter_num-1:03d}/content.md
3. Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml

Generate a structured outline with:
- 3-5 scenes with descriptions
- Key plot points
- Character development goals
- Emotional arc
- Foreshadowing elements

IMPORTANT: After creating the outline, use the Write tool to save it as JSON to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/outline.json

Format:
{{
    "chapter": {chapter_num},
    "title": "Chapter Title",
    "scenes": [...],
    "character_arcs": {{}},
    "emotional_progression": [...],
    "word_target": 4000
}}"""
    })
    
    # Stage 2: Initial Draft
    tasks.append({
        "stage": "2. Generate Initial Draft",
        "agent": "scene-generator",
        "description": f"Generate chapter {chapter_num} initial draft",
        "prompt": f"""Generate the complete initial draft for chapter {chapter_num}.

First, read the outline from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/outline.json
Also read Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml

Generate 3000-5000 words of narrative following the outline.
This is creative writing - generate the actual story, not analysis.

Start with: "Chapter {chapter_num}: [Title from outline]"

IMPORTANT: After generating, use Write tool to save the complete chapter to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v1.md"""
    })
    
    # Stage 3: Character Enhancement
    tasks.append({
        "stage": "3. Enhance Characters",
        "agent": "character-psychologist",
        "description": "Deepen character psychology",
        "prompt": f"""Enhance character depth in the chapter draft.

Read the current draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v1.md

ENHANCE:
- Add internal thoughts and motivations
- Deepen emotional reactions
- Add character-specific mannerisms
- Strengthen relationships

IMPORTANT: Save enhanced version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v2.md"""
    })
    
    # Stage 4: Dialogue Polish
    tasks.append({
        "stage": "4. Polish Dialogue",
        "agent": "dialogue-master-specialist",
        "description": "Polish dialogue authenticity",
        "prompt": f"""Polish all dialogue in the chapter.

Read current draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v2.md

IMPROVE:
- Make each voice distinct
- Add natural speech patterns
- Layer in subtext
- Improve dialogue tags

IMPORTANT: Save improved version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v3.md"""
    })
    
    # Stage 5: World Building
    tasks.append({
        "stage": "5. Enrich World",
        "agent": "world-builder",
        "description": "Add atmospheric details",
        "prompt": f"""Enrich world-building and atmosphere.

Read current draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v3.md

ADD:
- Sensory details (all five senses)
- Cultural elements
- Environmental atmosphere
- Spatial descriptions

IMPORTANT: Save enriched version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v4.md"""
    })
    
    # Stage 6: Continuity Check
    tasks.append({
        "stage": "6. Validate Continuity",
        "agent": "continuity-guard-specialist",
        "description": "Check and fix continuity",
        "prompt": f"""Validate continuity and fix issues.

Read current draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v4.md
Read Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml

CHECK & FIX:
- Timeline consistency
- Character knowledge boundaries
- Physical continuity
- Entity reference consistency

IMPORTANT: Save validated version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v5.md"""
    })
    
    # Stage 7: Prose Polish
    tasks.append({
        "stage": "7. Polish Prose",
        "agent": "prose-craft-specialist",
        "description": "Enhance literary quality",
        "prompt": f"""Polish the literary quality.

Read current draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v5.md

IMPROVE:
- Sentence variety
- Vivid verbs
- Metaphors and imagery
- Paragraph flow
- Show don't tell

IMPORTANT: Save polished version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v6.md"""
    })
    
    # Stage 8: Logic Check
    tasks.append({
        "stage": "8. Check Logic",
        "agent": "plot-hole-detector",
        "description": "Detect and fix plot issues",
        "prompt": f"""Check for plot holes and logic issues.

Read draft from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/draft_v6.md
Consider genre conventions from Bible.

IDENTIFY & FIX:
- Logic flaws
- Plot contradictions
- Character inconsistencies

IMPORTANT: Save final version using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/content.md"""
    })
    
    # Stage 9: Quality Score
    tasks.append({
        "stage": "9. Score Quality",
        "agent": "quality-scorer",
        "description": "Score chapter quality",
        "prompt": f"""Score the final chapter quality.

Read chapter from: data/projects/{current_project}/chapters/ch{chapter_num:03d}/content.md

Score (0-100):
- Overall quality
- Character development
- Plot advancement
- Prose quality
- Dialogue authenticity
- World building
- Emotional impact
- Consistency

IMPORTANT: Save quality report using Write tool to:
data/projects/{current_project}/chapters/ch{chapter_num:03d}/quality_report.json

Format:
{{
    "overall_score": 0-100,
    "dimensions": {{...}},
    "strengths": [...],
    "weaknesses": [...]
}}"""
    })
    
    return tasks


def main():
    """Output the task sequence for Claude Code to execute"""
    
    tasks = create_task_calls()
    if not tasks:
        return
    
    print("\n" + "="*60)
    print("CHAPTER GENERATION TASK SEQUENCE")
    print("="*60)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n[Task {i}/9] {task['stage']}")
        print(f"Agent: {task['agent']}")
        print(f"Description: {task['description']}")
        print("-" * 40)
        print("Prompt:")
        print(task['prompt'][:200] + "...")
        
    print("\n" + "="*60)
    print("Execute these tasks sequentially using Task tool")
    print("Each agent will save its output automatically")
    print("="*60)
    
    # Save task sequence for reference
    output_path = Path(".claude/src/last_generation_tasks.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)
    
    print(f"\nTask sequence saved to: {output_path}")


if __name__ == "__main__":
    main()