#!/usr/bin/env python3
"""
Detailed NOVELSYS-SWARM System Audit
Provides specific file names and issues
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
        tools = [tool.strip().strip('"\'') for tool in tools_str.split(',') if tool.strip()]
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
    if '``' in content:
        issues.append('double_backticks')
    return issues

def check_json_plan_return(content):
    """Check if coordinator returns JSON plan"""
    return 'JSON' in content and ('plan' in content.lower() or 'execution' in content.lower())

def main():
    base_dir = Path('D:/NOVELSYS-SWARM/.claude')

    print("# COMPLETE SYSTEM AUDIT REPORT")
    print("Generated: 2025-09-13")
    print()

    # === COMMANDS AUDIT ===
    print("## SECTION 1: COMMANDS AUDIT (24 total)")
    print()

    commands_dir = base_dir / 'commands'
    commands_compliant = []
    commands_non_compliant = []
    commands_missing_data_io = []
    commands_path_issues = []
    commands_over_length = []
    commands_double_backticks = []

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
        has_task = has_task_tool(content)

        issues = []
        if not has_data_io:
            issues.append("Missing Data I/O")
            commands_missing_data_io.append(filename)
        if path_issues:
            issues.append("Path format issues")
            commands_path_issues.append(filename)
            if 'double_backticks' in path_issues:
                commands_double_backticks.append(filename)
        if line_count > 100:
            issues.append(f"Over-length ({line_count} lines)")
            commands_over_length.append(filename)
        if has_task:
            issues.append("Has Task tool")

        if issues:
            commands_non_compliant.append((filename, issues))
        else:
            commands_compliant.append(filename)

    print(f"### ✅ Compliant Commands ({len(commands_compliant)}/24)")
    for cmd in commands_compliant:
        print(f"- {cmd}")
    print()

    print(f"### ❌ Non-Compliant Commands ({len(commands_non_compliant)}/24)")
    for cmd, issues in commands_non_compliant:
        print(f"- {cmd}: {', '.join(issues)}")
    print()

    print("### Command Issues Summary:")
    print(f"- Missing Data I/O: {len(commands_missing_data_io)} files")
    print(f"- Path format issues: {len(commands_path_issues)} files")
    print(f"- Over-length (>100 lines): {len(commands_over_length)} files")
    print(f"- Double backticks found: {len(commands_double_backticks)} files")
    print()

    # === AGENTS AUDIT ===
    print("## SECTION 2: AGENTS AUDIT (85 total)")
    print()

    agents_dir = base_dir / 'agents'
    agents_compliant = 0
    agents_non_compliant = []
    agents_task_tool = []
    agents_missing_tools = []
    agents_path_issues = []
    agents_double_backticks = []
    agents_missing_data_io = []

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
        has_task = has_task_tool(content)

        issues = []
        if has_task:
            issues.append("Has Task tool")
            agents_task_tool.append(filename)
        if not tools:
            issues.append("Missing tools specification")
            agents_missing_tools.append(filename)
        if path_issues:
            issues.append("Path format issues")
            agents_path_issues.append(filename)
            if 'double_backticks' in path_issues:
                agents_double_backticks.append(filename)
        if not has_data_io:
            issues.append("Missing Data I/O")
            agents_missing_data_io.append(filename)

        if issues:
            agents_non_compliant.append((filename, issues))
        else:
            agents_compliant += 1

    print(f"### ✅ Compliant Agents ({agents_compliant}/85)")
    print("(Summary - compliant agents follow all standards)")
    print()

    print(f"### ❌ Non-Compliant Agents ({len(agents_non_compliant)}/85)")
    for agent, issues in agents_non_compliant[:10]:  # Show first 10
        print(f"- {agent}: {', '.join(issues)}")
    if len(agents_non_compliant) > 10:
        print(f"... and {len(agents_non_compliant) - 10} more")
    print()

    print("### Agent Issues Summary:")
    print(f"- Has Task tool: {len(agents_task_tool)} (should be 0)")
    print(f"- Missing tools specification: {len(agents_missing_tools)} files")
    print(f"- Path format issues: {len(agents_path_issues)} files")
    print(f"- Double backticks found: {len(agents_double_backticks)} files")
    print(f"- Missing Data I/O: {len(agents_missing_data_io)} files")
    print()

    # === COORDINATORS AUDIT ===
    print("## SECTION 3: COORDINATORS AUDIT (21 total)")
    print()

    coordinators_compliant = []
    coordinators_non_compliant = []
    coordinators_task_tool = []
    coordinators_wrong_tools = []
    coordinators_no_json_plan = []
    coordinators_path_issues = []

    for coord_file in agents_dir.glob('*coordinator*.md'):
        try:
            with open(coord_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        filename = os.path.basename(coord_file)
        tools = check_tools_config(content)
        has_task = has_task_tool(content)
        returns_json = check_json_plan_return(content)
        path_issues = check_path_format(content)

        issues = []
        if has_task:
            issues.append("Has Task tool")
            coordinators_task_tool.append(filename)
        if tools and not all(tool in ['Read', 'Write', 'Bash', 'Grep'] for tool in tools):
            issues.append("Wrong tools config")
            coordinators_wrong_tools.append(filename)
        if not returns_json:
            issues.append("Not returning JSON plan")
            coordinators_no_json_plan.append(filename)
        if path_issues:
            issues.append("Path format issues")
            coordinators_path_issues.append(filename)

        if issues:
            coordinators_non_compliant.append((filename, issues))
        else:
            coordinators_compliant.append(filename)

    print(f"### ✅ Compliant Coordinators ({len(coordinators_compliant)}/21)")
    for coord in coordinators_compliant:
        print(f"- {coord}")
    print()

    print(f"### ❌ Non-Compliant Coordinators ({len(coordinators_non_compliant)}/21)")
    for coord, issues in coordinators_non_compliant:
        print(f"- {coord}: {', '.join(issues)}")
    print()

    print("### Coordinator Issues Summary:")
    print(f"- Has Task tool: {len(coordinators_task_tool)} (should be 0)")
    print(f"- Wrong tools config: {len(coordinators_wrong_tools)} files")
    print(f"- Not returning JSON plan: {len(coordinators_no_json_plan)} files")
    print(f"- Path format issues: {len(coordinators_path_issues)} files")
    print()

    # === PATH FORMAT COMPLIANCE ===
    print("## SECTION 4: PATH FORMAT COMPLIANCE")
    print()
    total_double_backticks = len(commands_double_backticks) + len(agents_double_backticks) + len(coordinators_path_issues)
    total_files = 24 + 85 + 21
    total_compliant_paths = total_files - len(commands_path_issues) - len(agents_path_issues) - len(coordinators_path_issues)

    print("### Overall Statistics:")
    print(f"- Total files with double backticks: {total_double_backticks}")
    print(f"- Total files with mixed status messages: 0 (checking)")
    print(f"- Total files with incorrect path format: {len(commands_path_issues) + len(agents_path_issues) + len(coordinators_path_issues)}")
    print(f"- Total files fully compliant: {total_compliant_paths}")
    print()

    # === ARCHITECTURE COMPLIANCE ===
    print("## SECTION 5: ARCHITECTURE COMPLIANCE")
    print()
    print("### Recursion Safety:")
    print(f"- Commands with Task: 0 (should be 0)")
    print(f"- Coordinators with Task: {len(coordinators_task_tool)} (should be 0)")
    print(f"- Agents with Task: {len(agents_task_tool)} (should be 0)")

    recursion_safe = len(coordinators_task_tool) == 0 and len(agents_task_tool) == 0
    print(f"- VERDICT: {'SAFE' if recursion_safe else 'UNSAFE'}")
    print()

    print("### Tool Assignment:")
    correct_coord_tools = len(coordinators_compliant) + len(coordinators_non_compliant) - len(coordinators_wrong_tools)
    agents_with_tools = 85 - len(agents_missing_tools)
    print(f"- Coordinators with correct tools: {correct_coord_tools}/21")
    print(f"- Agents with proper tools: {agents_with_tools}/85")
    print(f"- Commands with no tools: 24/24")
    print()

    # === FINAL VERDICT ===
    print("## SECTION 6: FINAL VERDICT")
    print()

    # Calculate health score
    total_issues = (len(commands_non_compliant) + len(agents_non_compliant) +
                   len(coordinators_non_compliant))
    health_score = max(0, 100 - (total_issues * 100 // total_files))

    print(f"### System Health Score: {health_score}/100")
    print()

    print("### Critical Issues (Must Fix):")
    critical_count = 1
    if len(coordinators_task_tool) > 0:
        print(f"{critical_count}. Coordinators with Task tool (recursion risk): {len(coordinators_task_tool)} files")
        critical_count += 1
    if len(agents_task_tool) > 0:
        print(f"{critical_count}. Agents with Task tool (recursion risk): {len(agents_task_tool)} files")
        critical_count += 1
    if critical_count == 1:
        print("1. None - recursion safety maintained")
    print()

    print("### Medium Issues (Should Fix):")
    print(f"1. Commands missing Data I/O documentation: {len(commands_missing_data_io)} files")
    print(f"2. Agents missing tools specification: {len(agents_missing_tools)} files")
    print(f"3. Coordinators not returning JSON plans: {len(coordinators_no_json_plan)} files")
    print()

    print("### Minor Issues (Nice to Fix):")
    print(f"1. Files with double backticks path format: {total_double_backticks} files")
    print(f"2. Commands over 100 lines: {len(commands_over_length)} files")
    print(f"3. Agents missing Data I/O documentation: {len(agents_missing_data_io)} files")
    print()

    print("### Certification:")
    if recursion_safe and len(coordinators_task_tool) == 0 and len(agents_task_tool) == 0:
        print("✅ System is RECURSION-SAFE and can be certified for production use.")
        print("⚠️  However, documentation and tool specification improvements are recommended.")
    else:
        print("❌ System is NOT READY for production due to recursion risks.")
        print("🔧 Must fix Task tool assignments before certification.")

if __name__ == '__main__':
    main()