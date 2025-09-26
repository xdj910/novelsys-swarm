#!/usr/bin/env python3
"""
Deep analysis of architecture report to find hidden issues.
"""

import json
from pathlib import Path
from collections import defaultdict

def analyze_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    issues = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    # 1. Check commands
    print("=" * 70)
    print("COMMAND ANALYSIS")
    print("=" * 70)
    
    for cmd_name, cmd_data in data.get('commands', {}).items():
        # Check for missing tools configuration
        if not cmd_data.get('tools'):
            print(f"[INFO] {cmd_name}: No tools (correct for commands)")
        
        # Check for coordinator references
        if cmd_data.get('coordinator'):
            print(f"[COORD] {cmd_name} -> {cmd_data['coordinator']}")
        
        # Check dependencies
        deps = cmd_data.get('dependencies', [])
        if len(deps) > 3:
            issues['medium'].append(f"Command {cmd_name} has {len(deps)} dependencies")
        
        # Check I/O patterns
        io_spec = cmd_data.get('io_specification', {})
        writes = io_spec.get('writes', [])
        if len(writes) > 5:
            issues['high'].append(f"Command {cmd_name} writes to {len(writes)} locations")
    
    # 2. Check agents
    print("\n" + "=" * 70)
    print("AGENT ANALYSIS")
    print("=" * 70)
    
    agents_with_task = []
    agents_no_tools = []
    agents_complex_deps = []
    agents_multiple_writes = []
    
    for agent_name, agent_data in data.get('agents', {}).items():
        tools = agent_data.get('tools', [])
        
        # Check for Task tool
        if 'Task' in tools:
            agents_with_task.append(agent_name)
            issues['critical'].append(f"Agent {agent_name} has Task tool!")
        
        # Check for missing tools
        if not tools:
            agents_no_tools.append(agent_name)
        
        # Check dependencies
        deps = agent_data.get('dependencies', [])
        if len(deps) > 5:
            agents_complex_deps.append((agent_name, len(deps)))
            issues['high'].append(f"Agent {agent_name} has {len(deps)} dependencies")
        
        # Check I/O patterns
        io_spec = agent_data.get('io_specification', {})
        writes = io_spec.get('writes', [])
        reads = io_spec.get('reads', [])
        
        if len(writes) > 3:
            agents_multiple_writes.append((agent_name, len(writes)))
            issues['medium'].append(f"Agent {agent_name} writes to {len(writes)} locations")
        
        # Check for potential file corruption patterns
        file_patterns = io_spec.get('file_patterns', [])
        for pattern in file_patterns:
            if '.tmp' not in pattern and 'versions/' not in pattern:
                if any(w in pattern for w in ['chapter', 'bible', 'outline']):
                    if agent_name not in ['bible-architect', 'scene-generator', 'outline-generator']:
                        issues['high'].append(f"Agent {agent_name} directly writes critical file: {pattern}")
    
    # 3. Check for circular dependencies
    print("\n" + "=" * 70)
    print("DEPENDENCY ANALYSIS")
    print("=" * 70)
    
    # Build dependency graph
    dep_graph = {}
    for agent_name, agent_data in data.get('agents', {}).items():
        dep_graph[agent_name] = agent_data.get('dependencies', [])
    
    # Find cycles
    def find_cycles(graph):
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                # Found cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor in graph:  # Only follow if neighbor is also an agent
                    dfs(neighbor, path + [node])
            
            rec_stack.remove(node)
        
        for node in graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    cycles = find_cycles(dep_graph)
    if cycles:
        for cycle in cycles:
            issues['critical'].append(f"Circular dependency: {' -> '.join(cycle)}")
    
    # 4. Check for consistency issues
    print("\n" + "=" * 70)
    print("CONSISTENCY ANALYSIS")
    print("=" * 70)
    
    # Check coordinators
    coordinators = [a for a in data.get('agents', {}).keys() if 'coordinator' in a]
    for coord in coordinators:
        coord_data = data['agents'][coord]
        if 'Task' in coord_data.get('tools', []):
            issues['critical'].append(f"Coordinator {coord} has Task tool (recursion risk!)")
    
    # Check for agents that both read and write same file types
    for agent_name, agent_data in data.get('agents', {}).items():
        io_spec = agent_data.get('io_specification', {})
        patterns = io_spec.get('file_patterns', [])
        
        read_patterns = set()
        write_patterns = set()
        
        for pattern in patterns:
            # Simplified pattern matching
            if 'chapter' in pattern:
                if any(r in str(io_spec.get('reads', [])) for r in ['chapter', 'ch']):
                    read_patterns.add('chapter')
                if any(w in str(io_spec.get('writes', [])) for w in ['chapter', 'ch']):
                    write_patterns.add('chapter')
        
        overlap = read_patterns & write_patterns
        if overlap and agent_name not in ['scene-generator', 'quality-scorer']:
            issues['medium'].append(f"Agent {agent_name} both reads and writes: {overlap}")
    
    # 5. Summary statistics
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    
    print(f"Total commands: {len(data.get('commands', {}))}")
    print(f"Total agents: {len(data.get('agents', {}))}")
    print(f"Agents with Task tool: {len(agents_with_task)}")
    print(f"Agents without tools config: {len(agents_no_tools)}")
    print(f"Agents with 5+ dependencies: {len(agents_complex_deps)}")
    print(f"Circular dependencies found: {len(cycles)}")
    
    # 6. Report issues
    print("\n" + "=" * 70)
    print("ISSUES FOUND")
    print("=" * 70)
    
    for severity in ['critical', 'high', 'medium', 'low']:
        if issues[severity]:
            print(f"\n[{severity.upper()}] ({len(issues[severity])} issues)")
            for issue in issues[severity][:10]:  # Show first 10
                print(f"  - {issue}")
            if len(issues[severity]) > 10:
                print(f"  ... and {len(issues[severity]) - 10} more")
    
    return issues

if __name__ == '__main__':
    report_path = Path('report/architecture_io_20250912_125514.json')
    if report_path.exists():
        issues = analyze_report(report_path)
        
        # Count total issues
        total = sum(len(v) for v in issues.values())
        print(f"\n" + "=" * 70)
        print(f"TOTAL ISSUES: {total}")
        print("=" * 70)
        
        if issues['critical']:
            print("\n[FAIL] System has critical issues that need immediate attention!")
            exit(1)
        elif issues['high']:
            print("\n[WARNING] System has high-priority issues to address")
            exit(2)
        else:
            print("\n[OK] No critical issues found")
            exit(0)
    else:
        print(f"Report not found: {report_path}")
        exit(1)