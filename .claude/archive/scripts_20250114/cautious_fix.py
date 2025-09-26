#!/usr/bin/env python3
"""
Cautious Fix Script for NOVELSYS-SWARM
This script carefully fixes issues with proper backup and verification
"""

import re
from pathlib import Path
import json
import shutil
from datetime import datetime

class CautiousFixer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.agents_dir = self.base_dir / '.claude' / 'agents'
        self.commands_dir = self.base_dir / '.claude' / 'commands'
        self.backup_dir = self.base_dir / '.claude' / 'backup' / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.fixes_log = []
        self.dry_run = True  # Start with dry run

    def backup_file(self, file_path: Path) -> Path:
        """Create backup of file before modification"""
        relative_path = file_path.relative_to(self.base_dir)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path

    def fix_double_backticks_carefully(self, content: str) -> tuple[str, list]:
        """Fix double backticks with detailed tracking"""
        fixes = []
        lines = content.split('\n')
        fixed_lines = []

        for line_num, line in enumerate(lines, 1):
            # Check for path with double backticks at end
            if '`' in line:
                # Pattern: `path`` at end of line
                pattern = r'`([^`]+)``(\s*$|[\s,\)])'
                match = re.search(pattern, line)
                if match:
                    fixes.append({
                        'line': line_num,
                        'original': line,
                        'issue': 'double backtick at end'
                    })
                    line = re.sub(pattern, r'`\1`\2', line)

                # Pattern: standalone `` that should be ```
                if line.strip() == '``':
                    fixes.append({
                        'line': line_num,
                        'original': line,
                        'issue': 'standalone double backtick'
                    })
                    line = '```'

            fixed_lines.append(line)

        return '\n'.join(fixed_lines), fixes

    def add_command_data_io(self, file_path: Path, content: str) -> tuple[str, bool]:
        """Add Data I/O section to command if missing"""
        if '## Data I/O' in content or '### Data I/O' in content:
            return content, False  # Already has Data I/O

        # Find a good place to insert Data I/O section
        lines = content.split('\n')
        insert_index = -1

        # Look for common sections to insert before
        for i, line in enumerate(lines):
            if line.startswith('## ') and 'process' in line.lower():
                insert_index = i + 5  # After process section
                break

        if insert_index == -1:
            # Insert at end of file
            insert_index = len(lines) - 1

        # Generate Data I/O based on command name
        command_name = file_path.stem
        data_io_section = self.generate_command_data_io(command_name)

        # Insert the section
        lines.insert(insert_index, data_io_section)

        return '\n'.join(lines), True

    def generate_command_data_io(self, command_name: str) -> str:
        """Generate appropriate Data I/O section based on command name"""
        # Common patterns for different command types
        if 'bible' in command_name:
            return """
## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/bible.yaml`
  - `.claude/data/context/current_project.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/bible.yaml`
  - `.claude/data/projects/{project}/bible_backup.yaml`
"""
        elif 'chapter' in command_name:
            return """
## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/outline.json`
  - `.claude/data/projects/{project}/book_{N}/bible.yaml`
  - `.claude/data/context/current_project.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/content.md`
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/meta.json`
"""
        elif 'quality' in command_name:
            return """
## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/*/content.md`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/quality_report.json`
  - `.claude/data/projects/{project}/book_{N}/quality_scores.json`
"""
        else:
            return """
## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`
"""

    def analyze_file(self, file_path: Path) -> dict:
        """Analyze a file for issues"""
        issues = {
            'path': str(file_path.relative_to(self.base_dir)),
            'double_backticks': 0,
            'missing_data_io': False,
            'fixes_needed': []
        }

        try:
            content = file_path.read_text(encoding='utf-8')

            # Check for double backticks
            if '``' in content:
                _, fixes = self.fix_double_backticks_carefully(content)
                issues['double_backticks'] = len(fixes)
                issues['fixes_needed'].extend(fixes)

            # Check for Data I/O in commands
            if 'commands' in str(file_path):
                if '## Data I/O' not in content and '### Data I/O' not in content:
                    issues['missing_data_io'] = True

            return issues
        except Exception as e:
            issues['error'] = str(e)
            return issues

    def fix_file(self, file_path: Path, issues: dict) -> dict:
        """Fix issues in a file"""
        result = {
            'file': str(file_path.relative_to(self.base_dir)),
            'backed_up': False,
            'fixed': False,
            'changes': []
        }

        if not issues['double_backticks'] and not issues.get('missing_data_io'):
            return result  # No fixes needed

        try:
            # Read current content
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Create backup first
            if not self.dry_run:
                backup_path = self.backup_file(file_path)
                result['backed_up'] = True
                result['backup_path'] = str(backup_path)

            # Apply fixes
            if issues['double_backticks'] > 0:
                content, fixes = self.fix_double_backticks_carefully(content)
                result['changes'].append(f"Fixed {len(fixes)} double backticks")

            if issues.get('missing_data_io') and 'commands' in str(file_path):
                content, added = self.add_command_data_io(file_path, content)
                if added:
                    result['changes'].append("Added Data I/O section")

            # Write back if changed
            if content != original_content:
                if not self.dry_run:
                    file_path.write_text(content, encoding='utf-8')
                result['fixed'] = True

            return result

        except Exception as e:
            result['error'] = str(e)
            return result

    def run(self, dry_run=True):
        """Run the cautious fixer"""
        self.dry_run = dry_run

        print("="*60)
        print(f"CAUTIOUS FIXER - {'DRY RUN' if dry_run else 'ACTUAL FIX'}")
        print("="*60)

        # Collect all files
        all_files = []

        if self.agents_dir.exists():
            all_files.extend([f for f in self.agents_dir.glob('*.md')
                            if not f.name.startswith('BASE_')
                            and not f.name.startswith('AGENT_SAVE')])

        if self.commands_dir.exists():
            all_files.extend(self.commands_dir.rglob('*.md'))

        print(f"\nAnalyzing {len(all_files)} files...")

        # Analyze all files first
        issues_found = []
        for file_path in all_files:
            issues = self.analyze_file(file_path)
            if issues['double_backticks'] > 0 or issues.get('missing_data_io'):
                issues_found.append((file_path, issues))

        print(f"\nFound issues in {len(issues_found)} files")

        if not issues_found:
            print("No issues found!")
            return

        # Show summary
        print("\nISSUES SUMMARY:")
        total_double_backticks = sum(i[1]['double_backticks'] for i in issues_found)
        total_missing_io = sum(1 for i in issues_found if i[1].get('missing_data_io'))

        print(f"  - Double backticks: {total_double_backticks} instances")
        print(f"  - Missing Data I/O: {total_missing_io} files")

        if dry_run:
            print("\nDRY RUN - Showing what would be fixed:")
            for file_path, issues in issues_found[:5]:  # Show first 5
                print(f"\n{file_path.name}:")
                if issues['double_backticks']:
                    print(f"  - Would fix {issues['double_backticks']} double backticks")
                if issues.get('missing_data_io'):
                    print(f"  - Would add Data I/O section")

            if len(issues_found) > 5:
                print(f"\n... and {len(issues_found) - 5} more files")

            print("\n" + "="*60)
            print("To apply fixes, run with dry_run=False")
        else:
            print(f"\nCreating backup in: {self.backup_dir}")

            # Apply fixes
            fixed_count = 0
            for file_path, issues in issues_found:
                result = self.fix_file(file_path, issues)
                if result['fixed']:
                    fixed_count += 1
                    print(f"[FIXED] {file_path.name}: {', '.join(result['changes'])}")

            print(f"\n{fixed_count} files fixed")
            print(f"Backup saved to: {self.backup_dir}")

            # Save report
            report_path = self.base_dir / '.claude' / 'report' / 'cautious_fix_report.json'
            report_path.parent.mkdir(parents=True, exist_ok=True)

            with open(report_path, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'dry_run': dry_run,
                    'files_analyzed': len(all_files),
                    'files_with_issues': len(issues_found),
                    'files_fixed': fixed_count,
                    'backup_dir': str(self.backup_dir) if not dry_run else None
                }, f, indent=2)

            print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    import sys

    fixer = CautiousFixer()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        print("Applying fixes with full backup...")
        fixer.run(dry_run=False)
    else:
        print("Starting with DRY RUN to preview changes...")
        fixer.run(dry_run=True)
        print("\nTo apply fixes, run with: python cautious_fix.py --fix")