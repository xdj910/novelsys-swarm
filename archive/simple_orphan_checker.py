#!/usr/bin/env python3
"""
Simple Orphan Checker - Direct verification
Check each of the 19 reported orphans manually with direct grep
"""

import subprocess
import os
from pathlib import Path

def run_grep(pattern, path=".claude"):
    """Run grep and return results"""
    try:
        result = subprocess.run(
            ["grep", "-r", "-i", pattern, path],
            capture_output=True,
            text=True,
            cwd="."
        )
        return result.stdout.strip()
    except:
        return ""

def check_component_usage(component_name):
    """Check if component is used anywhere"""

    # Check in all agents and coordinators
    agents_usage = run_grep(component_name, ".claude/agents")
    commands_usage = run_grep(component_name, ".claude/commands")

    # Filter out self-references
    agents_lines = [line for line in agents_usage.split('\n') if line and component_name not in line.split(':')[0]]
    commands_lines = [line for line in commands_usage.split('\n') if line and component_name not in line.split(':')[0]]

    return {
        'agents_usage': agents_lines,
        'commands_usage': commands_lines,
        'is_orphan': len(agents_lines) == 0 and len(commands_lines) == 0
    }

# List of reported orphans
orphans = [
    # Coordinators
    "chapter-planning-coordinator",

    # Agents
    "author-voice-signature-specialist",
    "bible-cache-updater",
    "book-outline-reviewer",
    "brainstorming-completeness-validator",
    "clue-integration-specialist",
    "context-validator",
    "current-project-updater",
    "emotional-trigger-specialist",
    "humanization-specialist",
    "humor-injection-specialist",
    "knowledge-base-updater",
    "novel-quality-process-analyzer",
    "report-deduplication-specialist",
    "series-bible-architect",
    "test-rejection-logger-agent",
    "test-state-updater-agent",
    "world-building-specialist",
    "world-clue-specialist"
]

print("Simple Orphan Verification")
print("=" * 40)

true_orphans = []
false_positives = []

for component in orphans:
    print(f"\nChecking: {component}")
    result = check_component_usage(component)

    if result['is_orphan']:
        print(f"  [TRUE ORPHAN] - no usage found")
        true_orphans.append(component)
    else:
        print(f"  [FALSE POSITIVE] - found usage:")
        if result['agents_usage']:
            print(f"    Agents usage: {len(result['agents_usage'])} references")
            for usage in result['agents_usage'][:3]:  # Show first 3
                print(f"      {usage}")
        if result['commands_usage']:
            print(f"    Commands usage: {len(result['commands_usage'])} references")
            for usage in result['commands_usage'][:3]:  # Show first 3
                print(f"      {usage}")
        false_positives.append(component)

print(f"\n" + "=" * 40)
print(f"VERIFICATION SUMMARY")
print(f"=" * 40)
print(f"Reported orphans: {len(orphans)}")
print(f"True orphans: {len(true_orphans)}")
print(f"False positives: {len(false_positives)}")
print(f"Accuracy: {len(true_orphans)/len(orphans)*100:.1f}%")

if false_positives:
    print(f"\nFALSE POSITIVES FOUND:")
    for fp in false_positives:
        print(f"  - {fp}")

if true_orphans:
    print(f"\nTRUE ORPHANS CONFIRMED:")
    for orphan in true_orphans:
        print(f"  - {orphan}")