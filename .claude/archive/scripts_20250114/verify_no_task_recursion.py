#!/usr/bin/env python3
"""
Verify that no agents have Task tool to prevent recursion.
Final validation after all fixes applied.
"""

import os
import re
from pathlib import Path

def check_agent(filepath):
    """Check agent for tools configuration and Task presence."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract tools configuration
    tools_match = re.search(r'^tools:\s*(.+)$', content, re.MULTILINE)
    
    if not tools_match:
        return 'NO_TOOLS', None
    
    tools_line = tools_match.group(1)
    
    # Check if Task is in tools (case-sensitive), but ignore comments
    # Split by # to ignore comments
    tools_part = tools_line.split('#')[0].strip()
    
    # Check if Task is actually in the tools list
    if 'Task' in tools_part:
        return 'HAS_TASK', tools_line
    
    return 'SAFE', tools_line

def main():
    agents_dir = Path('.claude/agents')
    
    all_agents = list(agents_dir.glob('*.md'))
    
    print("=" * 70)
    print("RECURSION SAFETY VERIFICATION REPORT")
    print("=" * 70)
    print(f"\nTotal agent files: {len(all_agents)}")
    
    no_tools = []
    has_task = []
    safe = []
    
    for agent in sorted(all_agents):
        status, tools = check_agent(agent)
        
        if status == 'NO_TOOLS':
            no_tools.append(agent.name)
        elif status == 'HAS_TASK':
            has_task.append((agent.name, tools))
        else:
            safe.append(agent.name)
    
    # Report results
    print(f"\n[SAFE] Agents with tools configured (no Task): {len(safe)}")
    if len(safe) <= 10:
        for name in safe[:10]:
            print(f"  - {name}")
    
    if no_tools:
        print(f"\n[WARNING] Agents without tools configuration: {len(no_tools)}")
        for name in no_tools[:10]:
            print(f"  - {name}")
        if len(no_tools) > 10:
            print(f"  ... and {len(no_tools) - 10} more")
    
    if has_task:
        print(f"\n[CRITICAL] Agents with Task tool (RECURSION RISK): {len(has_task)}")
        for name, tools in has_task:
            print(f"  - {name}")
            print(f"    Tools: {tools}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if has_task:
        print("[FAILED] System has recursion vulnerabilities!")
        print(f"  - {len(has_task)} agents can cause recursion crashes")
        print("  - Immediate fix required")
        return 1
    elif no_tools:
        print("[WARNING] System may have undefined behavior")
        print(f"  - {len(no_tools)} agents lack explicit tools configuration")
        print("  - Could inherit default tools")
        return 2
    else:
        print("[SUCCESS] System is recursion-safe!")
        print(f"  - All {len(all_agents)} agents properly configured")
        print("  - No Task tool found in any subagent")
        print("  - Ready for stable operation")
        return 0
    
    # Check specific patterns
    print("\n" + "=" * 70)
    print("PATTERN ANALYSIS")
    print("=" * 70)
    
    coordinators = [a for a in all_agents if 'coordinator' in a.name.lower()]
    specialists = [a for a in all_agents if 'specialist' in a.name.lower()]
    
    print(f"Coordinators: {len(coordinators)} found")
    coord_safe = all(check_agent(c)[0] != 'HAS_TASK' for c in coordinators)
    print(f"  Status: {'SAFE - No Task tools' if coord_safe else 'DANGEROUS - Has Task'}")
    
    print(f"\nSpecialists: {len(specialists)} found")
    spec_safe = all(check_agent(s)[0] != 'HAS_TASK' for s in specialists)
    print(f"  Status: {'SAFE - No Task tools' if spec_safe else 'DANGEROUS - Has Task'}")

if __name__ == '__main__':
    exit(main())