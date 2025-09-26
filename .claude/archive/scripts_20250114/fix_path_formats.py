#!/usr/bin/env python3
"""
Fix Path Format Issues in NOVELSYS-SWARM Documentation

This script:
1. Fixes double backtick issues (`path`` -> `path`)
2. Removes status messages from path lists
3. Standardizes path format across all components
"""

import re
from pathlib import Path
import json

class PathFormatFixer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent  # Go up to NOVELSYS-SWARM
        self.agents_dir = self.base_dir / '.claude' / 'agents'
        self.commands_dir = self.base_dir / '.claude' / 'commands'
        self.fixes_applied = []

    def fix_double_backticks(self, content: str) -> tuple[str, int]:
        """Fix double backtick issues in paths"""
        # Pattern to find paths with double backticks at the end
        pattern = r'`([^`]+)``'
        fixes = 0

        def replacer(match):
            nonlocal fixes
            fixes += 1
            return f'`{match.group(1)}`'

        fixed_content = re.sub(pattern, replacer, content)
        return fixed_content, fixes

    def remove_status_messages(self, content: str) -> tuple[str, int]:
        """Remove status messages mixed with paths"""
        fixes = 0
        lines = content.split('\n')
        fixed_lines = []

        # Status message patterns to remove from path lists
        status_patterns = [
            r'^.*✓.*$',  # Checkmark status
            r'^.*✅.*$',  # Green checkmark
            r'^.*❌.*$',  # X mark
            r'^.*CRITICAL:.*$',  # Critical messages
            r'^.*WARNING:.*$',  # Warning messages
            r'^.*ERROR:.*$',  # Error messages
            r'^.*Success.*$',  # Success messages
        ]

        in_path_section = False

        for line in lines:
            # Detect if we're in a path listing section
            if 'Reads from:' in line or 'Writes to:' in line or 'File patterns:' in line:
                in_path_section = True
                fixed_lines.append(line)
                continue
            elif line.strip() and not line.startswith('  ') and not line.startswith('-'):
                in_path_section = False

            # If in path section, check for status messages
            if in_path_section and line.strip().startswith('-'):
                # Extract the path part
                path_match = re.search(r'`([^`]+)`', line)
                if path_match:
                    # Check if line contains status message
                    is_status = False
                    for pattern in status_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            is_status = True
                            fixes += 1
                            # Keep only the path part
                            fixed_lines.append(f'  - `{path_match.group(1)}`')
                            break

                    if not is_status:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines), fixes

    def clean_json_pollution(self, content: str) -> tuple[str, int]:
        """Remove JSON fragments from path documentation"""
        fixes = 0
        lines = content.split('\n')
        fixed_lines = []

        in_path_section = False

        for line in lines:
            # Detect if we're in a path listing section
            if 'Reads from:' in line or 'Writes to:' in line:
                in_path_section = True
                fixed_lines.append(line)
                continue
            elif line.strip() and not line.startswith('  ') and not line.startswith('-'):
                in_path_section = False

            # Skip JSON-like lines in path sections
            if in_path_section and line.strip().startswith('-'):
                # Check for JSON patterns
                if any(pattern in line for pattern in ['{', '}', '"agent":', '"phase":', '"description":']):
                    fixes += 1
                    continue  # Skip this line

            fixed_lines.append(line)

        return '\n'.join(fixed_lines), fixes

    def process_file(self, file_path: Path) -> dict:
        """Process a single file and apply fixes"""
        result = {
            'file': str(file_path.relative_to(self.base_dir)),
            'double_backticks': 0,
            'status_messages': 0,
            'json_pollution': 0,
            'total_fixes': 0
        }

        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Apply fixes
            content, fixes1 = self.fix_double_backticks(content)
            result['double_backticks'] = fixes1

            content, fixes2 = self.remove_status_messages(content)
            result['status_messages'] = fixes2

            content, fixes3 = self.clean_json_pollution(content)
            result['json_pollution'] = fixes3

            result['total_fixes'] = fixes1 + fixes2 + fixes3

            # Write back if changes were made
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied.append(result)

            return result

        except Exception as e:
            result['error'] = str(e)
            return result

    def run(self):
        """Run the fixer on all agent and coordinator files"""
        print("="*60)
        print("PATH FORMAT FIXER FOR NOVELSYS-SWARM")
        print("="*60)

        all_files = []

        # Collect all .md files from agents directory
        if self.agents_dir.exists():
            all_files.extend(self.agents_dir.glob('*.md'))

        # Collect all .md files from commands directory
        if self.commands_dir.exists():
            for cmd_file in self.commands_dir.rglob('*.md'):
                all_files.append(cmd_file)

        print(f"\nFound {len(all_files)} files to process")

        # Process each file
        for file_path in all_files:
            result = self.process_file(file_path)
            if result['total_fixes'] > 0:
                print(f"\n[FIXED] {file_path.name}:")
                if result['double_backticks'] > 0:
                    print(f"  - Double backticks: {result['double_backticks']}")
                if result['status_messages'] > 0:
                    print(f"  - Status messages: {result['status_messages']}")
                if result['json_pollution'] > 0:
                    print(f"  - JSON pollution: {result['json_pollution']}")

        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total files processed: {len(all_files)}")
        print(f"Files with fixes: {len(self.fixes_applied)}")

        total_double = sum(f['double_backticks'] for f in self.fixes_applied)
        total_status = sum(f['status_messages'] for f in self.fixes_applied)
        total_json = sum(f['json_pollution'] for f in self.fixes_applied)

        print(f"\nTotal fixes applied:")
        print(f"  - Double backticks fixed: {total_double}")
        print(f"  - Status messages removed: {total_status}")
        print(f"  - JSON pollution cleaned: {total_json}")
        print(f"  - TOTAL: {total_double + total_status + total_json}")

        # Save report
        report_path = self.base_dir / '.claude' / 'report' / 'path_format_fixes.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump({
                'summary': {
                    'files_processed': len(all_files),
                    'files_fixed': len(self.fixes_applied),
                    'double_backticks': total_double,
                    'status_messages': total_status,
                    'json_pollution': total_json,
                    'total_fixes': total_double + total_status + total_json
                },
                'details': self.fixes_applied
            }, f, indent=2)

        print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    fixer = PathFormatFixer()
    fixer.run()