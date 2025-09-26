#!/usr/bin/env python3
"""
Fix coordinator recursion issue by adding explicit tools configuration.
This prevents coordinators from inheriting Task tool which causes recursion crashes.
"""

import os
import re
from pathlib import Path

def fix_coordinator(filepath):
    """Add explicit tools configuration to prevent Task inheritance."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has tools configuration
    if re.search(r'^tools:', content, re.MULTILINE):
        print(f"  [OK] {filepath.name} already has tools configured")
        return False
    
    # Find the end of frontmatter
    lines = content.split('\n')
    
    # Look for frontmatter section
    if lines[0] == '---':
        # Find closing ---
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                # Insert tools before closing ---
                lines.insert(i, 'tools: Read, Write, Bash, Grep  # NEVER include Task - prevents recursion')
                print(f"  [FIXED] {filepath.name} - added recursion-safe tools")
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                return True
    
    print(f"  [WARN] {filepath.name} - unexpected format, skipping")
    return False

def main():
    agents_dir = Path('.claude/agents')
    
    coordinators = list(agents_dir.glob('*coordinator*.md'))
    
    print(f"Found {len(coordinators)} coordinator files")
    print("=" * 50)
    
    fixed = 0
    for coord in coordinators:
        if fix_coordinator(coord):
            fixed += 1
    
    print("=" * 50)
    print(f"Fixed {fixed} coordinators")
    print(f"Skipped {len(coordinators) - fixed} (already configured or special)")
    
    # Special case: test-coordinator should only have Read
    test_coord = agents_dir / 'test-coordinator.md'
    if test_coord.exists():
        print("\nSpecial handling for test-coordinator:")
        with open(test_coord, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'tools: Read, Write, Bash, Grep' in content:
            content = content.replace(
                'tools: Read, Write, Bash, Grep  # NEVER include Task - prevents recursion',
                'tools: Read  # Minimal tools for test planning only'
            )
            with open(test_coord, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  [FIXED] Adjusted test-coordinator to minimal tools")

if __name__ == '__main__':
    main()