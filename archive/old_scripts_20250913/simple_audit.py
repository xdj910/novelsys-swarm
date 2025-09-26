#!/usr/bin/env python3
"""
Simple NOVELSYS-SWARM System Audit
ASCII-only output for Windows compatibility
"""

import os
import re
from pathlib import Path

def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len([line for line in f if line.strip()])
    except:
        return 0

def check_tools_config(content):
    tools_match = re.search(r'tools:\s*\[(.*?)\]', content, re.DOTALL)
    if tools_match:
        tools_str = tools_match.group(1)
        tools = [tool.strip().strip('"\'') for tool in tools_str.split(',') if tool.strip()]
        return tools
    return None

def has_task_tool(content):
    tools = check_tools_config(content)
    if tools:
        return 'Task' in tools
    return False

def check_data_io_section(content):
    return '## Data I/O' in content or '### Data I/O' in content

def check_path_format(content):
    issues = []
    if '``' in content:
        issues.append('double_backticks')
    return issues

def check_json_plan_return(content):
    return 'JSON' in content and ('plan' in content.lower() or 'execution' in content.lower())

def main():
    base_dir = Path('D:/NOVELSYS-SWARM/.claude')

    print("=== COMMANDS DETAILED AUDIT ===")
    commands_dir = base_dir / 'commands'
    cmd_missing_data_io = []
    cmd_path_issues = []
    cmd_over_length = []

    for cmd_file in commands_dir.rglob('*.md'):
        try:
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        filename = os.path.basename(cmd_file)
        line_count = count_lines(cmd_file)
        has_data_io = check_data_io_section(content)
        path_issues = check_path_format(content)

        if not has_data_io:
            cmd_missing_data_io.append(filename)
        if path_issues:
            cmd_path_issues.append(filename)
        if line_count > 100:
            cmd_over_length.append(filename)

    print(f"Commands missing Data I/O ({len(cmd_missing_data_io)}/24):")
    for cmd in cmd_missing_data_io:
        print(f"  - {cmd}")

    print(f"\nCommands with path issues ({len(cmd_path_issues)}/24):")
    for cmd in cmd_path_issues:
        print(f"  - {cmd}")

    print(f"\nCommands over 100 lines ({len(cmd_over_length)}/24):")
    for cmd in cmd_over_length:
        print(f"  - {cmd}")

    print("\n=== AGENTS DETAILED AUDIT ===")
    agents_dir = base_dir / 'agents'
    agent_missing_tools = []
    agent_missing_data_io = []
    agent_path_issues = []

    for agent_file in agents_dir.glob('*.md'):
        if 'coordinator' in agent_file.name or agent_file.name in ['BASE_AGENT_TEMPLATE.md', 'AGENT_SAVE_INSTRUCTION.md']:
            continue

        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        filename = os.path.basename(agent_file)
        has_data_io = check_data_io_section(content)
        path_issues = check_path_format(content)
        tools = check_tools_config(content)

        if not tools:
            agent_missing_tools.append(filename)
        if path_issues:
            agent_path_issues.append(filename)
        if not has_data_io:
            agent_missing_data_io.append(filename)

    print(f"Agents missing tools config ({len(agent_missing_tools)}/85):")
    for i, agent in enumerate(agent_missing_tools):
        if i < 10:
            print(f"  - {agent}")
        elif i == 10:
            print(f"  ... and {len(agent_missing_tools) - 10} more")

    print(f"\nAgents with path issues ({len(agent_path_issues)}/85):")
    for i, agent in enumerate(agent_path_issues):
        if i < 10:
            print(f"  - {agent}")
        elif i == 10:
            print(f"  ... and {len(agent_path_issues) - 10} more")

    print("\n=== COORDINATORS DETAILED AUDIT ===")
    coord_no_json = []
    coord_path_issues = []

    for coord_file in agents_dir.glob('*coordinator*.md'):
        try:
            with open(coord_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        filename = os.path.basename(coord_file)
        returns_json = check_json_plan_return(content)
        path_issues = check_path_format(content)

        if not returns_json:
            coord_no_json.append(filename)
        if path_issues:
            coord_path_issues.append(filename)

    print(f"Coordinators not returning JSON plan ({len(coord_no_json)}/21):")
    for coord in coord_no_json:
        print(f"  - {coord}")

    print(f"\nCoordinators with path issues ({len(coord_path_issues)}/21):")
    for coord in coord_path_issues:
        print(f"  - {coord}")

if __name__ == '__main__':
    main()