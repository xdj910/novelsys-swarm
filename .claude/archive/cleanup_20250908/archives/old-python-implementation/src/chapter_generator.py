#!/usr/bin/env python3
"""
Chapter Generator - Automated Sequential Pipeline
Version: 3.0
Purpose: Generate novel chapters through 9-stage enhancement pipeline
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ChapterGenerator:
    def __init__(self, project_name: str, chapter_num: int):
        self.project_name = project_name
        self.chapter_num = chapter_num
        self.project_path = Path(f"data/projects/{project_name}")
        self.chapter_path = self.project_path / f"chapters/ch{chapter_num:03d}"
        self.entity_dict_path = Path(".claude/agents/shared/entity_dictionary.yaml")
        
        # Create chapter directory
        self.chapter_path.mkdir(parents=True, exist_ok=True)
        
        # Track generation progress
        self.generation_log = {
            "chapter": chapter_num,
            "project": project_name,
            "start_time": datetime.now().isoformat(),
            "stages": []
        }
    
    def load_resources(self) -> Dict[str, Any]:
        """Load all necessary resources for chapter generation"""
        resources = {}
        
        # Load Bible
        bible_path = self.project_path / "bible.yaml"
        if bible_path.exists():
            with open(bible_path, 'r', encoding='utf-8') as f:
                import yaml
                resources['bible'] = yaml.safe_load(f)
        
        # Load Entity Dictionary
        if self.entity_dict_path.exists():
            with open(self.entity_dict_path, 'r', encoding='utf-8') as f:
                import yaml
                resources['entity_dict'] = yaml.safe_load(f)
        
        # Load previous chapter if exists
        prev_chapter_path = self.project_path / f"chapters/ch{self.chapter_num-1:03d}/content.md"
        if prev_chapter_path.exists():
            with open(prev_chapter_path, 'r', encoding='utf-8') as f:
                resources['previous_chapter'] = f.read()
        
        # Load character states
        char_states_path = self.project_path / "context/characters.json"
        if char_states_path.exists():
            with open(char_states_path, 'r', encoding='utf-8') as f:
                resources['character_states'] = json.load(f)
        
        # Load world context
        world_path = self.project_path / "context/world.json"
        if world_path.exists():
            with open(world_path, 'r', encoding='utf-8') as f:
                resources['world_context'] = json.load(f)
        
        return resources
    
    def generate_stage_prompt(self, stage: str, resources: Dict, previous_draft: str = None) -> str:
        """Generate specific prompt for each stage"""
        
        prompts = {
            "outline": f"""
You are bible-architect. Create a detailed outline for chapter {self.chapter_num}.

CONTEXT:
- Bible: {json.dumps(resources.get('bible', {}), indent=2)}
- Previous chapter ending: {resources.get('previous_chapter', 'First chapter')[-500:] if resources.get('previous_chapter') else 'First chapter'}
- Entity Dictionary available for consistent naming

GENERATE:
1. Scene-by-scene breakdown (3-5 scenes)
2. Key plot points to accomplish
3. Character development goals
4. Emotional arc
5. Foreshadowing elements

OUTPUT FORMAT:
Create a structured JSON outline and use Write tool to save it to:
{self.chapter_path}/outline.json

The JSON should have this structure:
{{
    "chapter_number": {self.chapter_num},
    "title": "Chapter Title",
    "scenes": [
        {{"scene": 1, "description": "...", "plot_points": [...], "characters": [...]}}
    ],
    "character_arcs": {{}},
    "emotional_progression": [],
    "foreshadowing": [],
    "word_target": 4000
}}
""",

            "draft": f"""
You are scene-generator. Generate the complete initial draft for chapter {self.chapter_num}.

INPUTS:
- Outline: Read from {self.chapter_path}/outline.json
- Bible: Available for reference
- Entity Dictionary: Use approved name variations from {self.entity_dict_path}
- Previous chapter ending: {resources.get('previous_chapter', '')[-500:] if resources.get('previous_chapter') else 'First chapter'}

REQUIREMENTS:
- Follow the outline precisely
- 3000-5000 words total
- Natural scene transitions
- Use only approved entity variations
- Maintain consistency with previous chapter

GENERATE:
Write complete chapter narrative starting with "Chapter {self.chapter_num}: [Title]"
This is creative writing, not analysis. Generate the actual story.

After generating, use Write tool to save the complete chapter to:
{self.chapter_path}/draft_v1.md
""",

            "character": f"""
You are character-psychologist. Enhance character depth in the draft.

CURRENT DRAFT: Read from {self.chapter_path}/draft_v1.md
CHARACTER STATES: {json.dumps(resources.get('character_states', {}), indent=2)}

ENHANCE:
- Add internal thoughts and motivations
- Deepen emotional reactions and body language
- Add character-specific mannerisms
- Strengthen relationship dynamics
- Show character growth

Read the draft, enhance it, then use Write tool to save enhanced version to:
{self.chapter_path}/draft_v2.md
""",

            "dialogue": f"""
You are dialogue-master-specialist. Polish all dialogue in the chapter.

CURRENT DRAFT: Read from {self.chapter_path}/draft_v2.md
BIBLE CHARACTER VOICES: Reference character speech patterns from bible

IMPROVE:
- Make each character's voice distinct
- Add natural speech patterns and interruptions
- Layer in subtext and unspoken tensions
- Improve dialogue tags and actions
- Remove stilted or unnatural phrases

Read the draft, improve all dialogue, then use Write tool to save to:
{self.chapter_path}/draft_v3.md
""",

            "world": f"""
You are world-builder. Enrich the world-building and atmosphere.

CURRENT DRAFT: Read from {self.chapter_path}/draft_v3.md
WORLD CONTEXT: {json.dumps(resources.get('world_context', {}), indent=2)}

ADD:
- Rich sensory details (all five senses)
- Cultural elements and local color
- Environmental atmosphere and weather
- Spatial descriptions and geography
- Time of day and seasonal markers

Read the draft, enrich world details, then use Write tool to save to:
{self.chapter_path}/draft_v4.md
""",

            "continuity": f"""
You are continuity-guard-specialist. Validate and fix continuity issues.

CURRENT DRAFT: Read from {self.chapter_path}/draft_v4.md
ENTITY DICTIONARY: Read from {self.entity_dict_path}
PREVIOUS CHAPTERS: Reference for timeline and events

CHECK & FIX:
- Timeline consistency (no paradoxes)
- Character knowledge boundaries (they only know what they've learned)
- Physical continuity (injuries, locations, objects)
- Entity reference consistency (use dictionary)
- Natural reference evolution (formal to informal progression)

Read the draft, fix any issues, then use Write tool to save to:
{self.chapter_path}/draft_v5.md
""",

            "prose": f"""
You are prose-craft-specialist. Polish the literary quality.

CURRENT DRAFT: Read from {self.chapter_path}/draft_v5.md

IMPROVE:
- Vary sentence structure and rhythm
- Use vivid verbs and eliminate weak adverbs
- Add metaphors and imagery
- Improve paragraph transitions
- Strengthen opening and closing lines
- Show don't tell

Read the draft, polish prose, then use Write tool to save to:
{self.chapter_path}/draft_v6.md
""",

            "logic": f"""
You are plot-hole-detector. Check for plot holes and logic issues.

FINAL DRAFT: Read from {self.chapter_path}/draft_v6.md
GENRE: {resources.get('bible', {}).get('metadata', {}).get('genre', 'general')}
ENTITY DICTIONARY: Reference for consistency

IDENTIFY & FIX:
- Logic flaws (considering genre conventions)
- Unresolved questions that should be answered
- Character behavior inconsistencies
- Plot contradictions

If you find issues, fix them. Then use Write tool to save final version to:
{self.chapter_path}/content.md
""",

            "score": f"""
You are quality-scorer. Score the final chapter quality.

CHAPTER: Read from {self.chapter_path}/content.md

SCORE these dimensions (0-100):
- Overall quality
- Character development
- Plot advancement  
- Prose quality
- Dialogue authenticity
- World building
- Emotional impact
- Consistency

Generate a detailed quality report and use Write tool to save it to:
{self.chapter_path}/quality_report.json

Format:
{{
    "overall_score": 0-100,
    "dimensions": {{
        "character_development": 0-100,
        "plot_advancement": 0-100,
        "prose_quality": 0-100,
        "dialogue_authenticity": 0-100,
        "world_building": 0-100,
        "emotional_impact": 0-100,
        "consistency": 0-100
    }},
    "strengths": [...],
    "weaknesses": [...],
    "recommendations": [...]
}}
"""
        }
        
        return prompts.get(stage, "")
    
    def execute_stage(self, stage_name: str, agent_type: str, prompt: str) -> bool:
        """Execute a single stage of the pipeline"""
        
        print(f"\n[Stage] {stage_name}")
        print(f"  Agent: {agent_type}")
        print(f"  Starting at: {datetime.now().strftime('%H:%M:%S')}")
        
        # Log stage start
        stage_info = {
            "stage": stage_name,
            "agent": agent_type,
            "start": datetime.now().isoformat()
        }
        
        # Here we would call the Task tool with the agent
        # For now, this is a placeholder showing the structure
        # In actual Claude Code execution, this would be:
        # Task(subagent_type=agent_type, description=f"Stage: {stage_name}", prompt=prompt)
        
        print(f"  [Prompt sent to {agent_type}]")
        print(f"  [Agent should save output automatically]")
        
        # Log stage completion
        stage_info["end"] = datetime.now().isoformat()
        stage_info["status"] = "completed"
        self.generation_log["stages"].append(stage_info)
        
        return True
    
    def run_pipeline(self):
        """Run the complete 9-stage pipeline"""
        
        print(f"\n{'='*60}")
        print(f"CHAPTER GENERATION PIPELINE v3.0")
        print(f"Project: {self.project_name}")
        print(f"Chapter: {self.chapter_num}")
        print(f"{'='*60}")
        
        # Load resources
        print("\n[Loading Resources]")
        resources = self.load_resources()
        print(f"  Bible: {'Loaded' if 'bible' in resources else 'Not found'}")
        print(f"  Entity Dictionary: {'Loaded' if 'entity_dict' in resources else 'Not found'}")
        print(f"  Previous Chapter: {'Loaded' if 'previous_chapter' in resources else 'N/A'}")
        
        # Pipeline stages
        stages = [
            ("1. Generate Outline", "bible-architect", "outline"),
            ("2. Generate Initial Draft", "scene-generator", "draft"),
            ("3. Enhance Characters", "character-psychologist", "character"),
            ("4. Polish Dialogue", "dialogue-master-specialist", "dialogue"),
            ("5. Enrich World Details", "world-builder", "world"),
            ("6. Validate Continuity", "continuity-guard-specialist", "continuity"),
            ("7. Polish Prose", "prose-craft-specialist", "prose"),
            ("8. Check Logic", "plot-hole-detector", "logic"),
            ("9. Score Quality", "quality-scorer", "score")
        ]
        
        # Execute each stage
        for stage_name, agent_type, prompt_key in stages:
            prompt = self.generate_stage_prompt(prompt_key, resources)
            success = self.execute_stage(stage_name, agent_type, prompt)
            
            if not success:
                print(f"\n[ERROR] Stage failed: {stage_name}")
                break
        
        # Save generation log
        self.generation_log["end_time"] = datetime.now().isoformat()
        log_path = self.chapter_path / "generation_log.json"
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.generation_log, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"PIPELINE COMPLETE")
        print(f"Output saved to: {self.chapter_path}")
        print(f"{'='*60}")
        
        # Check quality score
        quality_report_path = self.chapter_path / "quality_report.json"
        if quality_report_path.exists():
            with open(quality_report_path, 'r') as f:
                report = json.load(f)
                score = report.get('overall_score', 0)
                
                if score >= 95:
                    print(f"\n[SUCCESS] Quality Score: {score}/100")
                    print("[INFO] Chapter eligible for Entity Dictionary learning")
                elif score >= 90:
                    print(f"\n[WARNING] Quality Score: {score}/100")
                    print("[INFO] Consider running improvement iteration")
                else:
                    print(f"\n[ERROR] Quality Score: {score}/100")
                    print("[INFO] Manual review recommended")
        
        return True


def main():
    """Main entry point for command-line usage"""
    
    if len(sys.argv) < 3:
        print("Usage: python chapter_generator.py <project_name> <chapter_number>")
        print("Example: python chapter_generator.py 'Island Inn Mysteries' 5")
        sys.exit(1)
    
    project_name = sys.argv[1]
    chapter_num = int(sys.argv[2])
    
    # Check if project exists
    project_path = Path(f"data/projects/{project_name}")
    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_name}")
        sys.exit(1)
    
    # Run generator
    generator = ChapterGenerator(project_name, chapter_num)
    generator.run_pipeline()


if __name__ == "__main__":
    main()