#!/usr/bin/env python3
"""
Fix all agents missing tools configuration to prevent potential Task inheritance.
Based on claude-code-expert audit findings.
"""

import os
import re
from pathlib import Path

# Agent type to tools mapping based on their purpose
AGENT_TOOLS_MAP = {
    # Specialists that need file operations
    'specialist': 'Read, Write',
    'generator': 'Read, Write', 
    'creator': 'Read, Write',
    'updater': 'Read, Write',
    'validator': 'Read, Grep',
    'reviewer': 'Read',
    'scorer': 'Read',
    'checker': 'Read, Grep',
    'analyzer': 'Read, Grep',
    'mapper': 'Read, Grep, Glob',
    'tracker': 'Read, Write',
    'detector': 'Read, Grep',
    'architect': 'Read, Write',
    'builder': 'Read, Write',
    'manager': 'Read, Write, Bash',
    'reporter': 'Read, Write',
    'auditor': 'Read, Grep, Glob',
    'tracer': 'Read, Write, Grep, Glob',
    'inspector': 'Read, Grep',
    'guard': 'Read, Write',
    'weaver': 'Read, Write',
    # Test agents - minimal tools
    'test': 'Read, Write',
    # Default for unmatched agents
    'default': 'Read, Write'
}

def determine_tools(filename, content):
    """Determine appropriate tools based on agent name and content."""
    name_lower = filename.lower()
    
    # Check for specific patterns in name
    for pattern, tools in AGENT_TOOLS_MAP.items():
        if pattern in name_lower:
            return tools
    
    # Check content for specific needs
    if 'WebSearch' in content or 'WebFetch' in content:
        return 'Read, Write, Grep, WebSearch, WebFetch'
    
    if 'Bash' in content or 'execute' in content or 'run' in content:
        return 'Read, Write, Bash'
    
    if 'grep' in content.lower() or 'search' in content:
        return 'Read, Write, Grep'
    
    return AGENT_TOOLS_MAP['default']

def fix_agent(filepath):
    """Add tools configuration to agent if missing."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip coordinators - they were already fixed
    if 'coordinator' in filepath.name.lower():
        return False, "Coordinator (already fixed)"
    
    # Check if already has tools configuration
    if re.search(r'^tools:', content, re.MULTILINE):
        return False, "Already has tools"
    
    # Determine appropriate tools
    tools = determine_tools(filepath.name, content)
    
    # Find the end of frontmatter
    lines = content.split('\n')
    
    # Look for frontmatter section
    if lines[0] == '---':
        # Find closing ---
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                # Insert tools before closing ---
                comment = "  # NO Task tool - prevents recursion" if tools != 'Read' else ""
                lines.insert(i, f'tools: {tools}{comment}')
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                return True, tools
    
    return False, "Unexpected format"

def main():
    agents_dir = Path('.claude/agents')
    
    all_agents = list(agents_dir.glob('*.md'))
    
    print(f"Total agent files found: {len(all_agents)}")
    print("=" * 60)
    
    fixed = []
    skipped = []
    errors = []
    
    for agent in all_agents:
        success, result = fix_agent(agent)
        
        if success:
            fixed.append((agent.name, result))
            print(f"  [FIXED] {agent.name:<40} tools: {result}")
        elif result == "Already has tools":
            skipped.append((agent.name, result))
        elif result == "Coordinator (already fixed)":
            skipped.append((agent.name, result))
        else:
            errors.append((agent.name, result))
            print(f"  [ERROR] {agent.name:<40} {result}")
    
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Fixed: {len(fixed)} agents")
    print(f"  Skipped: {len(skipped)} (already configured)")
    print(f"  Errors: {len(errors)}")
    
    if fixed:
        print(f"\nFixed agents by tools type:")
        tools_count = {}
        for name, tools in fixed:
            if tools not in tools_count:
                tools_count[tools] = 0
            tools_count[tools] += 1
        
        for tools, count in sorted(tools_count.items()):
            print(f"  {tools}: {count} agents")
    
    # Verify no agent has Task tool
    print("\n" + "=" * 60)
    print("Verification: Checking for Task tool...")
    
    task_found = []
    for agent in all_agents:
        with open(agent, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'^tools:.*Task', content, re.MULTILINE):
                task_found.append(agent.name)
    
    if task_found:
        print(f"  [WARNING] Found {len(task_found)} agents with Task tool:")
        for name in task_found:
            print(f"    - {name}")
    else:
        print("  [SUCCESS] No agents have Task tool - recursion safe!")

if __name__ == '__main__':
    main()