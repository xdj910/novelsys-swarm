#!/usr/bin/env python3
"""
Fix JSON code block formatting in coordinator files.
Changes ``json to ```json for proper markdown rendering.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

class JSONBlockFixer:
    def __init__(self):
        self.base_dir = Path("D:/NOVELSYS-SWARM")
        self.agents_dir = self.base_dir / ".claude/agents"
        self.backup_dir = self.base_dir / f".claude/backup/json_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.fixes_made = 0
        self.files_fixed = []

    def fix_json_blocks(self, content: str) -> tuple[str, int]:
        """Fix JSON code blocks in content."""
        # Pattern to match ``json (should be ```json)
        pattern = r'``json\b'
        replacement = '```json'

        # Count occurrences
        count = len(re.findall(pattern, content))

        # Replace all occurrences
        fixed_content = re.sub(pattern, replacement, content)

        return fixed_content, count

    def process_file(self, file_path: Path) -> bool:
        """Process a single file."""
        try:
            # Read file
            content = file_path.read_text(encoding='utf-8')

            # Fix JSON blocks
            fixed_content, fix_count = self.fix_json_blocks(content)

            if fix_count > 0:
                # Create backup
                backup_path = self.backup_dir / file_path.relative_to(self.base_dir)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)

                # Write fixed content
                file_path.write_text(fixed_content, encoding='utf-8')

                print(f"  Fixed {fix_count} JSON blocks in: {file_path.name}")
                self.fixes_made += fix_count
                self.files_fixed.append(file_path.name)
                return True

            return False

        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
            return False

    def run(self):
        """Run the JSON block fixer."""
        print("=" * 60)
        print("JSON Code Block Fixer")
        print("=" * 60)
        print(f"Scanning for ``json blocks to fix...")
        print()

        # Find coordinator files
        coordinator_files = list(self.agents_dir.glob("*coordinator*.md"))

        print(f"Found {len(coordinator_files)} coordinator files")
        print()

        # Process each file
        for file_path in coordinator_files:
            self.process_file(file_path)

        # Summary
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Files fixed: {len(self.files_fixed)}")
        print(f"Total fixes: {self.fixes_made}")

        if self.files_fixed:
            print(f"Backup created at: {self.backup_dir}")
            print("\nFiles fixed:")
            for name in sorted(self.files_fixed):
                print(f"  - {name}")
        else:
            print("No fixes needed!")

        return self.fixes_made > 0

if __name__ == "__main__":
    fixer = JSONBlockFixer()
    fixer.run()