#!/usr/bin/env python3
"""
Enhanced Chapter Generator with Full Context for Each Agent
Version: 6.0 - Every agent gets complete context
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class EnhancedChapterGenerator:
    """Generator with comprehensive context for each agent"""
    
    def __init__(self, chapter_num: int):
        self.chapter_num = chapter_num
        self.project_name = self.get_current_project()
        self.base_path = f"data/projects/{self.project_name}/chapters/ch{chapter_num:03d}"
        
        # Core context files that EVERY agent should read
        self.core_context = {
            "bible": f"data/projects/{self.project_name}/bible.yaml",
            "entity_dict": ".claude/agents/shared/entity_dictionary.yaml",
            "previous_chapter": f"data/projects/{self.project_name}/chapters/ch{chapter_num-1:03d}/content.md",
            "character_states": f"data/projects/{self.project_name}/context/characters.json",
            "world_context": f"data/projects/{self.project_name}/context/world.json",
            "plot_progress": f"data/projects/{self.project_name}/context/plot.json"
        }
        
        # Create chapter directory
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
    
    def get_current_project(self) -> str:
        """Get current project name"""
        current_project_file = Path("data/context/current_project.json")
        if current_project_file.exists():
            with open(current_project_file, 'r') as f:
                return json.load(f).get('project', 'test_project')
        return 'test_project'
    
    def generate_core_context_instructions(self) -> str:
        """Generate instructions for reading core context files"""
        return f"""
MANDATORY CONTEXT FILES TO READ FIRST:
1. Bible (complete project reference): {self.core_context['bible']}
2. Entity Dictionary (naming consistency): {self.core_context['entity_dict']}
3. Previous Chapter (continuity): {self.core_context['previous_chapter']}
4. Character States (current development): {self.core_context['character_states']}
5. World Context (setting details): {self.core_context['world_context']}
6. Plot Progress (story advancement): {self.core_context['plot_progress']}

Read ALL these files to understand the complete context before proceeding."""
    
    def generate_task_prompt(self, stage: str, previous_draft: str = None) -> str:
        """Generate prompts with FULL context for each agent"""
        
        prompts = {
            "outline": f"""You are bible-architect creating the outline for chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

ADDITIONAL CONTEXT:
- We are at chapter {self.chapter_num} of the series
- Check plot progress to see what needs to happen next
- Ensure continuity with previous chapter's ending

YOUR TASK:
1. Analyze all context files thoroughly
2. Generate a detailed outline that advances the plot appropriately
3. Include 3-5 scenes with:
   - Scene descriptions and locations
   - Characters involved
   - Plot points to accomplish
   - Emotional beats
   - Foreshadowing elements

OUTPUT STRUCTURE:
{{
    "chapter": {self.chapter_num},
    "title": "Meaningful Chapter Title",
    "theme": "Central theme of this chapter",
    "scenes": [
        {{
            "number": 1,
            "location": "Where it happens",
            "time": "When it happens",
            "characters": ["List of characters present"],
            "description": "What happens in this scene",
            "plot_points": ["Key events"],
            "emotional_tone": "Mood and atmosphere",
            "foreshadowing": ["Elements to plant"]
        }}
    ],
    "character_arcs": {{
        "character_name": "Their development in this chapter"
    }},
    "plot_advancement": "How this moves the overall story forward",
    "word_target": 4000
}}

CRITICAL ACTION: Use Write tool to save your outline to:
{self.base_path}/outline.json

YOU MUST SAVE THE FILE. Confirm with "Outline saved to {self.base_path}/outline.json" """,

            "draft": f"""You are scene-generator writing the full chapter {self.chapter_num} narrative.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Chapter Outline: {self.base_path}/outline.json (READ THIS FIRST)
- Previous Chapter Ending: {self.core_context['previous_chapter']} (last 500 words for continuity)

YOUR TASK:
1. Read ALL context files, especially the outline
2. Write the complete chapter narrative (3000-5000 words)
3. Start with: "Chapter {self.chapter_num}: [Title from outline]"
4. Follow the outline's scenes precisely
5. Use ONLY approved entity names from the dictionary
6. Maintain consistency with:
   - Character voices from Bible
   - World details from context
   - Plot progression
   - Previous chapter's ending

WRITING REQUIREMENTS:
- This is creative fiction writing, not a summary
- Show don't tell
- Include dialogue, action, and description
- Natural scene transitions
- Emotional depth
- Sensory details

CRITICAL ACTION: Use Write tool to save complete chapter to:
{self.base_path}/draft_v1.md

YOU MUST SAVE THE FILE using Write tool.""",

            "character": f"""You are character-psychologist enhancing character depth in chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v1.md (READ THIS - your working file)
- Chapter Outline: {self.base_path}/outline.json (understand intended character arcs)

YOUR TASK:
1. Read the current draft thoroughly
2. Cross-reference with character information from Bible and character states
3. Enhance the draft by adding:
   - Internal thoughts and motivations (based on character psychology from Bible)
   - Emotional reactions true to each character's personality
   - Character-specific mannerisms and speech patterns
   - Body language and nonverbal communication
   - Relationship dynamics based on their history
   - Psychological authenticity

IMPORTANT:
- Each character should feel distinct and consistent
- Their reactions should align with their established traits
- Show character growth that builds on previous chapters

CRITICAL ACTION: Use Write tool to save enhanced version to:
{self.base_path}/draft_v2.md""",

            "dialogue": f"""You are dialogue-master-specialist perfecting dialogue in chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v2.md (your working file)
- Bible: Pay special attention to character voice profiles

YOUR TASK:
1. Read the current draft and all context
2. Focus on the voice_profile section in Bible for each character
3. Polish all dialogue to ensure:
   - Each character has a distinct voice (vocabulary, rhythm, style)
   - Speech patterns match their background and personality
   - Natural interruptions and incomplete sentences where appropriate
   - Subtext and unspoken tensions
   - Culturally appropriate expressions
   - Age-appropriate language
   - Relationship dynamics reflected in how they address each other

REFERENCE Entity Dictionary for:
- How characters address each other (formal vs informal)
- Progression of familiarity over time
- Nicknames and variations

CRITICAL ACTION: Use Write tool to save improved version to:
{self.base_path}/draft_v3.md""",

            "world": f"""You are world-builder enriching the setting of chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v3.md
- Bible: Focus on universe/world_building sections
- World Context: Check for established locations and details

YOUR TASK:
1. Read all context to understand the world
2. Enrich the draft with:
   - Sensory details (all five senses in each scene)
   - Weather and atmospheric conditions
   - Cultural elements specific to the setting
   - Architecture and spatial descriptions
   - Flora, fauna, and environmental details
   - Time of day and lighting
   - Background sounds and activity
   - Smells and textures
   - Temperature and physical sensations

CONSISTENCY CHECK:
- Ensure all additions align with established world rules
- Maintain consistency with previous descriptions of locations
- Respect the genre conventions

CRITICAL ACTION: Use Write tool to save enriched version to:
{self.base_path}/draft_v4.md""",

            "continuity": f"""You are continuity-guard-specialist validating chapter {self.chapter_num} consistency.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v4.md
- ALL previous chapters for timeline and events
- Entity Dictionary for reference consistency

YOUR TASK:
1. Read the draft and ALL context files
2. Validate and fix:

TIMELINE CONSISTENCY:
- Event sequences align with established timeline
- Time of day/season progression is logical
- Character ages and time references are accurate

CHARACTER KNOWLEDGE:
- Characters only know what they've learned
- No impossible knowledge (unless justified)
- Information flow is tracked properly

PHYSICAL CONTINUITY:
- Injuries persist appropriately
- Object locations are consistent
- Travel times are realistic
- Weather continuity with previous scenes

ENTITY REFERENCES:
- All names match Entity Dictionary
- Reference evolution is natural (formal → informal)
- No unauthorized variations

PLOT CONSISTENCY:
- Events align with established facts
- No contradictions with previous chapters
- Foreshadowing from earlier chapters acknowledged

CRITICAL ACTION: Use Write tool to save validated version to:
{self.base_path}/draft_v5.md""",

            "prose": f"""You are prose-craft-specialist polishing the prose of chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v5.md
- Bible: Note the style guidelines and tone

YOUR TASK:
1. Read the draft and understand the intended style from Bible
2. Enhance literary quality:

SENTENCE LEVEL:
- Vary sentence structure and length
- Eliminate redundant words
- Replace weak verbs with strong ones
- Remove unnecessary adverbs
- Active voice where appropriate

PARAGRAPH LEVEL:
- Improve flow between paragraphs
- Ensure each paragraph has a purpose
- Vary paragraph lengths for rhythm

LITERARY DEVICES:
- Add metaphors and similes where appropriate
- Enhance imagery and symbolism
- Strengthen chapter opening hook
- Create memorable closing line

SHOW DON'T TELL:
- Convert exposition to action/dialogue
- Use specific details instead of generalizations
- Let readers infer emotions from behavior

CRITICAL ACTION: Use Write tool to save polished version to:
{self.base_path}/draft_v6.md""",

            "logic": f"""You are plot-hole-detector ensuring logical consistency in chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Current Draft: {self.base_path}/draft_v6.md
- Bible: Note the genre and its conventions
- Entity Dictionary: For fact-checking

YOUR TASK:
1. Read everything and check for:

PLOT LOGIC:
- Events follow cause and effect
- Character motivations make sense
- No unexplained coincidences (unless genre-appropriate)
- Problems have logical solutions

GENRE CONSIDERATIONS:
- Apply genre-specific logic standards
- Cozy mystery: community responses are acceptable
- Hard sci-fi: science must be plausible
- Fantasy: magic system rules must be consistent

CHARACTER BEHAVIOR:
- Actions align with established personalities
- Decisions are motivated properly
- Skills match backgrounds

WORLD CONSISTENCY:
- Technology/magic rules followed
- Social structures respected
- Economic realities considered

If you find issues, FIX them in the text, don't just note them.

CRITICAL ACTION: Use Write tool to save final chapter to:
{self.base_path}/content.md""",

            "score": f"""You are quality-scorer evaluating chapter {self.chapter_num}.

{self.generate_core_context_instructions()}

SPECIFIC FILES FOR THIS TASK:
- Final Chapter: {self.base_path}/content.md
- Chapter Outline: {self.base_path}/outline.json (check if goals were met)
- Bible: Quality standards and expectations

YOUR TASK:
1. Read the final chapter and all context
2. Score these dimensions (0-100):

SCORING CRITERIA:
- Overall Quality: Holistic assessment
- Character Development: Growth and authenticity
- Plot Advancement: Story progression
- Prose Quality: Writing craftsmanship
- Dialogue Authenticity: Natural and distinct voices
- World Building: Rich and consistent setting
- Emotional Impact: Reader engagement
- Consistency: Continuity and logic
- Bible Compliance: Adherence to source material
- Entity Dictionary Compliance: Correct naming

DETAILED ANALYSIS:
- List 3-5 specific strengths with examples
- List 2-3 areas for improvement
- Provide actionable recommendations

OUTPUT FORMAT:
{{
    "overall_score": [0-100],
    "dimensions": {{
        "character_development": [0-100],
        "plot_advancement": [0-100],
        "prose_quality": [0-100],
        "dialogue_authenticity": [0-100],
        "world_building": [0-100],
        "emotional_impact": [0-100],
        "consistency": [0-100],
        "bible_compliance": [0-100],
        "entity_compliance": [0-100]
    }},
    "strengths": [
        "Specific example from text"
    ],
    "weaknesses": [
        "Specific area needing work"
    ],
    "recommendations": [
        "Actionable improvement suggestion"
    ],
    "chapter_goals_met": true/false,
    "ready_for_publication": true/false
}}

CRITICAL ACTION: Use Write tool to save report to:
{self.base_path}/quality_report.json"""
        }
        
        return prompts.get(stage, "")
    
    def generate_task_sequence(self) -> list:
        """Generate the complete task sequence with full context"""
        
        tasks = [
            ("outline", "bible-architect", "Generate comprehensive outline"),
            ("draft", "scene-generator", "Write complete chapter narrative"),
            ("character", "character-psychologist", "Deepen character authenticity"),
            ("dialogue", "dialogue-master-specialist", "Perfect character voices"),
            ("world", "world-builder", "Enrich world details"),
            ("continuity", "continuity-guard-specialist", "Validate all continuity"),
            ("prose", "prose-craft-specialist", "Polish literary quality"),
            ("logic", "plot-hole-detector", "Ensure logical consistency"),
            ("score", "quality-scorer", "Comprehensive quality evaluation")
        ]
        
        task_list = []
        for stage, agent, description in tasks:
            task_list.append({
                "stage": stage,
                "agent": agent,
                "description": description,
                "prompt": self.generate_task_prompt(stage)
            })
        
        return task_list
    
    def save_task_sequence(self):
        """Save the task sequence for reference"""
        tasks = self.generate_task_sequence()
        
        output_file = Path(f".claude/src/chapter_{self.chapter_num}_tasks.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "chapter": self.chapter_num,
                "project": self.project_name,
                "generated": datetime.now().isoformat(),
                "tasks": tasks
            }, f, indent=2)
        
        print(f"Task sequence saved to: {output_file}")
        return tasks
    
    def print_execution_plan(self):
        """Print the execution plan with full context"""
        tasks = self.save_task_sequence()
        
        print(f"\n{'='*60}")
        print(f"ENHANCED CHAPTER GENERATOR v6.0")
        print(f"Project: {self.project_name}")
        print(f"Chapter: {self.chapter_num}")
        print(f"{'='*60}\n")
        
        print("KEY IMPROVEMENT: Every agent gets COMPLETE context")
        print("Core files read by ALL agents:")
        for name, path in self.core_context.items():
            print(f"  - {name}: {path}")
        
        print(f"\n{'='*60}")
        print("EXECUTION SEQUENCE")
        print(f"{'='*60}")
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[TASK {i}/9] {task['description']}")
            print(f"Agent: {task['agent']}")
            print(f"Stage: {task['stage']}")
            print("-" * 40)
            # Print first 300 chars of prompt to show context inclusion
            print("Prompt preview:")
            print(task['prompt'][:300] + "...")
            print(f"Output: {self.base_path}/{task['stage']}_output")
        
        print(f"\n{'='*60}")
        print("EXECUTION NOTES:")
        print("1. Each agent reads ALL core context files")
        print("2. Each agent MUST save output using Write tool")
        print("3. Context accumulates through the pipeline")
        print("4. Final score must be >= 95 for success")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_chapter_generator.py <chapter_number>")
        print("Example: python enhanced_chapter_generator.py 13")
        return
    
    chapter_num = int(sys.argv[1])
    generator = EnhancedChapterGenerator(chapter_num)
    generator.print_execution_plan()
    
    print("\nTo execute these tasks:")
    print("1. Run each Task() call sequentially")
    print("2. Verify each output file is created")
    print("3. Check quality score at the end")
    
    print(f"\nTask file saved for reference: .claude/src/chapter_{chapter_num}_tasks.json")


if __name__ == "__main__":
    main()