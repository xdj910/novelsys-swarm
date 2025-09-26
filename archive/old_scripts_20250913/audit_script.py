#!/usr/bin/env python3
"""
NOVELSYS-SWARM System Audit Script
Comprehensive audit of commands, agents, and coordinators
"""

import os
import re
from pathlib import Path

def count_lines(file_path):
    """Count non-empty lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len([line for line in f if line.strip()])
    except:
        return 0

def check_tools_config(content):
    """Check if file has tools configuration and what tools are specified"""
    tools_match = re.search(r'tools:\s*\[(.*?)\]', content, re.DOTALL)
    if tools_match:
        tools_str = tools_match.group(1)
        tools = [tool.strip().strip('"\'') for tool in tools_str.split(',')]
        return tools
    return None

def has_task_tool(content):
    """Check if file has Task tool in tools configuration"""
    tools = check_tools_config(content)
    if tools:
        return 'Task' in tools
    return False

def check_data_io_section(content):
    """Check if file has proper Data I/O documentation"""
    return '## Data I/O' in content or '### Data I/O' in content

def check_path_format(content):
    """Check for path format issues"""
    issues = []

    # Check for double backticks
    if '``' in content:
        issues.append('double_backticks')

    # Check for mixed status messages with paths
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '`' in line and ('status' in line.lower() or 'message' in line.lower()):
            if line.count('`') > 2:  # More than just path backticks
                issues.append('mixed_status_messages')
                break

    return issues

def check_json_plan_return(content):
    """Check if coordinator returns JSON plan"""
    return 'JSON' in content and ('plan' in content.lower() or 'execution' in content.lower())

def audit_file(file_path, file_type):
    """Audit a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return {'error': 'Cannot read file'}

    result = {
        'path': file_path,
        'line_count': count_lines(file_path),
        'has_data_io': check_data_io_section(content),
        'path_issues': check_path_format(content),
        'tools': check_tools_config(content),
        'has_task_tool': has_task_tool(content)
    }

    if file_type == 'coordinator':
        result['returns_json_plan'] = check_json_plan_return(content)

    return result

def main():
    base_dir = Path('D:/NOVELSYS-SWARM/.claude')

    # Audit commands
    commands_dir = base_dir / 'commands'
    commands = []
    for cmd_file in commands_dir.rglob('*.md'):
        commands.append(audit_file(cmd_file, 'command'))

    # Audit agents (excluding coordinators)
    agents_dir = base_dir / 'agents'
    agents = []
    coordinators = []

    for agent_file in agents_dir.glob('*.md'):
        if 'coordinator' in agent_file.name:
            coordinators.append(audit_file(agent_file, 'coordinator'))
        elif agent_file.name not in ['BASE_AGENT_TEMPLATE.md', 'AGENT_SAVE_INSTRUCTION.md']:
            agents.append(audit_file(agent_file, 'agent'))

    # Print results
    print("=== COMMANDS AUDIT ===")
    print(f"Total commands: {len(commands)}")
    for cmd in commands:
        print(f"\nFile: {os.path.basename(cmd['path'])}")
        print(f"  Lines: {cmd['line_count']}")
        print(f"  Has Data I/O: {cmd['has_data_io']}")
        print(f"  Path issues: {cmd['path_issues']}")
        print(f"  Tools: {cmd['tools']}")
        print(f"  Has Task tool: {cmd['has_task_tool']}")

    print("\n\n=== AGENTS AUDIT ===")
    print(f"Total agents: {len(agents)}")
    agent_issues = {'task_tool': 0, 'no_tools': 0, 'path_issues': 0, 'no_data_io': 0}
    for agent in agents:
        if agent['has_task_tool']:
            agent_issues['task_tool'] += 1
            print(f"ISSUE - Agent has Task tool: {os.path.basename(agent['path'])}")
        if not agent['tools']:
            agent_issues['no_tools'] += 1
        if agent['path_issues']:
            agent_issues['path_issues'] += 1
        if not agent['has_data_io']:
            agent_issues['no_data_io'] += 1

    print(f"Agent issues summary:")
    print(f"  Has Task tool: {agent_issues['task_tool']}")
    print(f"  No tools config: {agent_issues['no_tools']}")
    print(f"  Path issues: {agent_issues['path_issues']}")
    print(f"  No Data I/O: {agent_issues['no_data_io']}")

    print("\n\n=== COORDINATORS AUDIT ===")
    print(f"Total coordinators: {len(coordinators)}")
    coord_issues = {'task_tool': 0, 'wrong_tools': 0, 'no_json_plan': 0, 'path_issues': 0}
    for coord in coordinators:
        if coord['has_task_tool']:
            coord_issues['task_tool'] += 1
            print(f"CRITICAL - Coordinator has Task tool: {os.path.basename(coord['path'])}")
        if coord['tools'] and not all(tool in ['Read', 'Write', 'Bash', 'Grep'] for tool in coord['tools']):
            coord_issues['wrong_tools'] += 1
        if not coord.get('returns_json_plan', False):
            coord_issues['no_json_plan'] += 1
        if coord['path_issues']:
            coord_issues['path_issues'] += 1

    print(f"Coordinator issues summary:")
    print(f"  Has Task tool: {coord_issues['task_tool']}")
    print(f"  Wrong tools: {coord_issues['wrong_tools']}")
    print(f"  No JSON plan: {coord_issues['no_json_plan']}")
    print(f"  Path issues: {coord_issues['path_issues']}")

if __name__ == '__main__':
    main()