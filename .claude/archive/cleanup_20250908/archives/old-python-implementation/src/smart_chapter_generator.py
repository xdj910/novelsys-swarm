#!/usr/bin/env python3
"""
Smart Chapter Generator with Explicit Save Instructions
Version: 5.0 - Fixes agent save issues
"""

import json
import os
from pathlib import Path
from datetime import datetime

def get_current_project():
    """Get current project name"""
    current_project_file = Path("data/context/current_project.json")
    if current_project_file.exists():
        with open(current_project_file, 'r') as f:
            return json.load(f).get('project', 'test_project')
    return 'test_project'

def generate_task_prompt(stage, chapter_num, project_name, previous_file=None):
    """Generate explicit prompts that force agents to save files"""
    
    base_path = f"data/projects/{project_name}/chapters/ch{chapter_num:03d}"
    
    prompts = {
        "outline": f"""You are bible-architect generating an outline for chapter {chapter_num}.

STEP 1: Read these files to understand context:
- Bible: data/projects/{project_name}/bible.yaml
- Previous chapter (if exists): data/projects/{project_name}/chapters/ch{chapter_num-1:03d}/content.md
- Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml

STEP 2: Generate a detailed outline with:
- 3-5 scenes with descriptions
- Key plot points to accomplish
- Character development goals
- Emotional arc progression
- Foreshadowing elements

STEP 3: MANDATORY - Save your outline:
Use the Write tool to save your outline as JSON to this exact path:
{base_path}/outline.json

The JSON format should be:
{{
    "chapter": {chapter_num},
    "title": "Chapter Title Here",
    "scenes": [
        {{"number": 1, "description": "...", "location": "...", "characters": [...], "plot_points": [...]}}
    ],
    "character_arcs": {{"character_name": "development"}},
    "emotional_arc": ["opening_mood", "development", "climax", "resolution"],
    "foreshadowing": ["element1", "element2"],
    "word_target": 4000
}}

YOU MUST USE Write TOOL TO SAVE THE FILE. Do not just return the content.
Confirm the save by saying "Outline saved to {base_path}/outline.json" """,

        "draft": f"""You are scene-generator creating the initial draft for chapter {chapter_num}.

STEP 1: Read the outline you'll follow:
Read from: {base_path}/outline.json

STEP 2: Read context files:
- Bible: data/projects/{project_name}/bible.yaml  
- Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml
- Previous chapter ending: data/projects/{project_name}/chapters/ch{chapter_num-1:03d}/content.md

STEP 3: Generate the complete chapter narrative:
- Start with: "Chapter {chapter_num}: [Title from outline]"
- Write 3000-5000 words of story
- Follow the outline's scenes precisely
- Use only approved entity names from the dictionary
- This is creative writing - write the actual story, not summaries

STEP 4: MANDATORY - Save your draft:
Use the Write tool to save the complete chapter to:
{base_path}/draft_v1.md

YOU MUST USE Write TOOL. Confirm by saying "Draft saved to {base_path}/draft_v1.md" """,

        "character": f"""You are character-psychologist enhancing character depth.

STEP 1: Read the current draft:
Read from: {base_path}/draft_v1.md

STEP 2: Read character context:
- Bible: data/projects/{project_name}/bible.yaml (for character backgrounds)
- Character states: data/projects/{project_name}/context/characters.json

STEP 3: Enhance the draft by adding:
- Internal thoughts and motivations
- Emotional reactions and body language
- Character-specific mannerisms
- Deeper relationship dynamics
- Psychological authenticity

STEP 4: MANDATORY - Save enhanced version:
Use the Write tool to save to:
{base_path}/draft_v2.md

YOU MUST USE Write TOOL. Confirm save.""",

        "dialogue": f"""You are dialogue-master-specialist polishing dialogue.

STEP 1: Read current draft:
Read from: {base_path}/draft_v2.md

STEP 2: Read character voices from Bible:
data/projects/{project_name}/bible.yaml

STEP 3: Improve all dialogue:
- Make each character's voice distinct
- Add natural speech patterns
- Include subtext and tensions
- Improve dialogue tags

STEP 4: MANDATORY - Save improved version:
Use the Write tool to save to:
{base_path}/draft_v3.md

YOU MUST USE Write TOOL.""",

        "world": f"""You are world-builder enriching the setting.

STEP 1: Read current draft:
Read from: {base_path}/draft_v3.md

STEP 2: Read world context:
- Bible: data/projects/{project_name}/bible.yaml
- World details: data/projects/{project_name}/context/world.json

STEP 3: Add rich world details:
- All five senses
- Cultural elements
- Weather and atmosphere
- Spatial descriptions

STEP 4: MANDATORY - Save enriched version:
Use Write tool to save to:
{base_path}/draft_v4.md""",

        "continuity": f"""You are continuity-guard-specialist validating consistency.

STEP 1: Read current draft:
Read from: {base_path}/draft_v4.md

STEP 2: Read validation resources:
- Entity Dictionary: .claude/agents/shared/entity_dictionary.yaml
- Previous chapters for timeline
- Bible for facts

STEP 3: Check and fix:
- Timeline consistency
- Character knowledge boundaries
- Physical continuity
- Entity name consistency

STEP 4: MANDATORY - Save validated version:
Use Write tool to save to:
{base_path}/draft_v5.md""",

        "prose": f"""You are prose-craft-specialist polishing prose.

STEP 1: Read current draft:
Read from: {base_path}/draft_v5.md

STEP 2: Enhance literary quality:
- Vary sentence structure
- Use vivid verbs
- Add imagery
- Improve flow

STEP 3: MANDATORY - Save polished version:
Use Write tool to save to:
{base_path}/draft_v6.md""",

        "logic": f"""You are plot-hole-detector checking logic.

STEP 1: Read current draft:
Read from: {base_path}/draft_v6.md

STEP 2: Read Bible for genre:
data/projects/{project_name}/bible.yaml

STEP 3: Fix any plot holes or logic issues

STEP 4: MANDATORY - Save final chapter:
Use Write tool to save to:
{base_path}/content.md""",

        "score": f"""You are quality-scorer evaluating the chapter.

STEP 1: Read final chapter:
Read from: {base_path}/content.md

STEP 2: Score these dimensions (0-100):
- Overall quality
- Character development  
- Plot advancement
- Prose quality
- Dialogue authenticity
- World building
- Emotional impact
- Consistency

STEP 3: MANDATORY - Save quality report:
Use Write tool to save report as JSON to:
{base_path}/quality_report.json

Format:
{{
    "overall_score": 85,
    "dimensions": {{
        "character_development": 90,
        "plot_advancement": 85,
        "prose_quality": 88,
        "dialogue_authenticity": 92,
        "world_building": 80,
        "emotional_impact": 87,
        "consistency": 95
    }},
    "strengths": ["Great character moments", "Strong dialogue"],
    "weaknesses": ["Needs more sensory details"],
    "recommendations": ["Add more world-building in scene 2"]
}}"""
    }
    
    return prompts.get(stage, "")

def main():
    """Generate clear instructions for chapter generation"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python smart_chapter_generator.py <chapter_number>")
        return
    
    chapter_num = int(sys.argv[1])
    project_name = get_current_project()
    
    print(f"\n{'='*60}")
    print(f"SMART CHAPTER GENERATOR v5.0")
    print(f"Project: {project_name}")
    print(f"Chapter: {chapter_num}")
    print(f"{'='*60}\n")
    
    # Task sequence with explicit save instructions
    tasks = [
        ("outline", "bible-architect", "Generate chapter outline"),
        ("draft", "scene-generator", "Write initial draft"),
        ("character", "character-psychologist", "Enhance characters"),
        ("dialogue", "dialogue-master-specialist", "Polish dialogue"),
        ("world", "world-builder", "Add world details"),
        ("continuity", "continuity-guard-specialist", "Validate continuity"),
        ("prose", "prose-craft-specialist", "Polish prose"),
        ("logic", "plot-hole-detector", "Check logic"),
        ("score", "quality-scorer", "Score quality")
    ]
    
    print("IMPORTANT: Each agent MUST save their output using Write tool\n")
    
    for i, (stage, agent, description) in enumerate(tasks, 1):
        print(f"\n{'='*40}")
        print(f"TASK {i}/9: {description}")
        print(f"Agent: {agent}")
        print(f"{'='*40}")
        
        prompt = generate_task_prompt(stage, chapter_num, project_name)
        
        # Output the Task call
        print(f"""
Task(
    subagent_type="{agent}",
    description="{description}",
    prompt=\"\"\"{prompt}\"\"\"
)
""")
        
        print(f"Expected output: {stage} saved to designated file")
    
    print(f"\n{'='*60}")
    print("EXECUTION NOTES:")
    print("1. Each agent MUST use Write tool to save")
    print("2. Confirm each file is created before proceeding")
    print("3. If agent doesn't save, retry with clearer instruction")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()