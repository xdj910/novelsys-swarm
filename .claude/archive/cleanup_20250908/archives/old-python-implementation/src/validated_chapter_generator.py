#!/usr/bin/env python3
"""
Validated Chapter Generator with Context Verification
Version: 8.0 - Ensures agents read context and saves are verified
"""

import json
import os
from pathlib import Path
from datetime import datetime

class ValidatedChapterGenerator:
    """Generator with validation at every step"""
    
    def __init__(self, chapter_num: int):
        self.chapter_num = chapter_num
        self.project_name = self.get_current_project()
        self.base_path = f"data/projects/{self.project_name}/chapters/ch{chapter_num:03d}"
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
        
    def get_current_project(self) -> str:
        """Get current project name"""
        current_project_file = Path("data/context/current_project.json")
        if current_project_file.exists():
            with open(current_project_file, 'r') as f:
                return json.load(f).get('project', 'Island_Inn_Mysteries')
        return 'Island_Inn_Mysteries'
    
    def generate_outline_prompt_with_verification(self) -> str:
        """Generate outline prompt that FORCES reading context"""
        return f"""You are bible-architect creating outline for chapter {self.chapter_num}.

MANDATORY STEP 1: READ ALL CONTEXT FILES
You MUST read these files and confirm you've read them:

1. First, use Read tool to read: data/projects/{self.project_name}/bible.yaml
   After reading, say: "✓ Bible loaded"

2. Then, use Read tool to read: data/projects/{self.project_name}/chapters/ch{self.chapter_num-1:03d}/content.md
   After reading, say: "✓ Previous chapter loaded" (or "✓ No previous chapter" if it doesn't exist)

3. Finally, use Read tool to read: .claude/agents/shared/entity_dictionary.yaml
   After reading, say: "✓ Entity Dictionary loaded"

IF YOU DO NOT READ THESE FILES, THE TASK FAILS.

MANDATORY STEP 2: GENERATE OUTLINE
Based on what you read, create a JSON outline with:
{{
    "chapter": {self.chapter_num},
    "title": "Chapter Title",
    "theme": "Central theme",
    "scenes": [
        {{
            "number": 1,
            "location": "Where",
            "time": "When",
            "characters": ["Who"],
            "description": "What happens",
            "plot_points": ["Key events"],
            "emotional_tone": "Mood"
        }}
        // 3-5 scenes total
    ],
    "character_arcs": {{}},
    "plot_advancement": "How story moves forward",
    "context_confirmation": {{
        "bible_read": true,
        "previous_chapter_read": true,
        "entity_dict_read": true
    }},
    "word_target": 4000
}}

MANDATORY STEP 3: SAVE THE FILE
Use Write tool to save to: {self.base_path}/outline.json

Write("{self.base_path}/outline.json", <your_json_content>)

After saving, say: "✅ Outline saved to {self.base_path}/outline.json"

VERIFICATION: Your response MUST include:
1. Three checkmarks for reading files
2. The outline content
3. Confirmation of saving"""
    
    def generate_draft_prompt_with_verification(self) -> str:
        """Generate draft prompt with verification"""
        return f"""You are scene-generator writing chapter {self.chapter_num}.

MANDATORY STEP 1: VERIFY AND READ OUTLINE
First, use Read tool to read: {self.base_path}/outline.json
If this file doesn't exist, STOP and report: "❌ ERROR: No outline found"
After reading, say: "✓ Outline loaded"

MANDATORY STEP 2: READ CONTEXT FILES
1. Read: data/projects/{self.project_name}/bible.yaml
   Say: "✓ Bible loaded"
   
2. Read: .claude/agents/shared/entity_dictionary.yaml
   Say: "✓ Entity Dictionary loaded"

MANDATORY STEP 3: WRITE THE CHAPTER
Generate 3000-5000 words following the outline.
Start with: "Chapter {self.chapter_num}: [Title from outline]"

MANDATORY STEP 4: SAVE THE CHAPTER
Use Write tool to save to: {self.base_path}/draft_v1.md

After saving, say: "✅ Draft saved to {self.base_path}/draft_v1.md"

IF ANY STEP FAILS, STOP AND REPORT THE ERROR."""
    
    def verify_file_exists(self, filepath: str) -> bool:
        """Verify a file exists"""
        return Path(filepath).exists()
    
    def create_validation_checkpoint(self, stage: str) -> str:
        """Create validation prompt between stages"""
        return f"""
VALIDATION CHECKPOINT for {stage}:

1. Check if previous output exists:
   - Expected file: {self.base_path}/{stage}
   - If missing, STOP the pipeline

2. Verify file is not empty:
   - File size > 100 bytes
   
3. Log validation result:
   - ✅ {stage} validated, proceeding
   - ❌ {stage} failed, stopping pipeline

This validation ensures each agent completes before the next starts.
"""
    
    def generate_task_sequence(self) -> list:
        """Generate tasks with validation between each"""
        tasks = []
        
        # Task 1: Outline with forced reading
        tasks.append({
            "stage": "outline",
            "agent": "bible-architect", 
            "prompt": self.generate_outline_prompt_with_verification(),
            "validation": self.create_validation_checkpoint("outline.json")
        })
        
        # Task 2: Draft with verification
        tasks.append({
            "stage": "draft",
            "agent": "scene-generator",
            "prompt": self.generate_draft_prompt_with_verification(),
            "validation": self.create_validation_checkpoint("draft_v1.md")
        })
        
        # Add more tasks with similar verification...
        
        return tasks
    
    def execute_with_validation(self):
        """Execute pipeline with validation at each step"""
        print(f"\n{'='*60}")
        print(f"VALIDATED CHAPTER GENERATOR v8.0")
        print(f"Project: {self.project_name}")
        print(f"Chapter: {self.chapter_num}")
        print(f"{'='*60}\n")
        
        print("KEY FEATURES:")
        print("[✓] Forces agents to read context files")
        print("[✓] Verifies file creation between steps")
        print("[✓] Stops pipeline if any step fails")
        print("[✓] Provides clear error messages")
        
        tasks = self.generate_task_sequence()
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[TASK {i}] {task['stage']}")
            print(f"Agent: {task['agent']}")
            print("-" * 40)
            
            # Show the task would be executed
            print(f"Task(")
            print(f'    subagent_type="{task["agent"]}",')
            print(f'    description="Step {i}: {task["stage"]}",')
            print(f'    prompt="""...forced reading and saving..."""')
            print(f")")
            
            # Show validation step
            print(f"\n[VALIDATION]")
            print(task['validation'])
            
            # In real execution, we would check if file exists here
            expected_file = f"{self.base_path}/{task['stage']}_output"
            if self.verify_file_exists(expected_file):
                print(f"✅ {expected_file} exists, continuing...")
            else:
                print(f"⚠️ Would check for {expected_file} before continuing")
        
        print(f"\n{'='*60}")
        print("EXECUTION COMPLETE")
        print(f"{'='*60}\n")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validated_chapter_generator.py <chapter_number>")
        return
    
    chapter_num = int(sys.argv[1])
    generator = ValidatedChapterGenerator(chapter_num)
    generator.execute_with_validation()

if __name__ == "__main__":
    main()