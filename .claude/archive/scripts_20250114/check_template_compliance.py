#!/usr/bin/env python3
"""
Check all commands, coordinators, and agents for template compliance
Based on the new templates in .claude/templates/
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class TemplateComplianceChecker:
    def __init__(self):
        self.base_dir = Path('..')
        self.commands_dir = self.base_dir / 'commands'
        self.agents_dir = self.base_dir / 'agents'
        self.report = []
        
    def extract_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter"""
        try:
            content = file_path.read_text(encoding='utf-8')
            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx != -1:
                    yaml_content = content[3:end_idx]
                    return yaml.safe_load(yaml_content) or {}
            return {}
        except Exception as e:
            return {}
    
    def count_lines(self, file_path: Path) -> int:
        """Count lines in file"""
        try:
            return len(file_path.read_text(encoding='utf-8').splitlines())
        except:
            return 0
            
    def check_commands(self) -> List[Dict]:
        """Check command compliance with template"""
        issues = []
        print("\n=== Checking Commands ===")
        
        for file_path in self.commands_dir.rglob('*.md'):
            relative_path = file_path.relative_to(self.commands_dir)
            name = file_path.stem
            lines = self.count_lines(file_path)
            frontmatter = self.extract_frontmatter(file_path)
            
            problems = []
            
            # Check line count (HARD LIMIT: 100)
            if lines > 100:
                problems.append(f"[ERROR] OVER LENGTH: {lines} lines (max 100)")
                
            # Check for 'name' field in frontmatter (should not exist)
            if 'name' in frontmatter:
                problems.append("[ERROR] Has 'name' field in frontmatter (should be removed)")
                
            # Check required fields
            if 'description' not in frontmatter:
                problems.append("[ERROR] Missing 'description' in frontmatter")
                
            if problems:
                issues.append({
                    'file': str(relative_path),
                    'lines': lines,
                    'problems': problems
                })
                print(f"  [FAIL] {relative_path}: {lines} lines")
                for p in problems:
                    print(f"     {p}")
            else:
                print(f"  [OK] {relative_path}: {lines} lines")
                
        return issues
        
    def check_coordinators(self) -> List[Dict]:
        """Check coordinator compliance with template"""
        issues = []
        print("\n=== Checking Coordinators ===")
        
        for file_path in self.agents_dir.glob('*-coordinator.md'):
            name = file_path.stem
            lines = self.count_lines(file_path)
            frontmatter = self.extract_frontmatter(file_path)
            
            problems = []
            
            # Check line count (target 150-200, max 250)
            if lines > 250:
                problems.append(f"[WARNING] Over recommended length: {lines} lines (max 250)")
                
            # Check tools configuration
            tools = frontmatter.get('tools', '')
            if isinstance(tools, str):
                tools_list = [t.strip() for t in tools.split(',')]
            else:
                tools_list = tools if isinstance(tools, list) else []
                
            # Check for Task tool (CRITICAL: must not have)
            if 'Task' in tools_list or 'task' in str(tools).lower():
                problems.append("[CRITICAL] Has Task tool (causes recursion!)")
                
            # Check required tools
            if not tools:
                problems.append("[ERROR] No tools specified (should have Read, Write, Bash, Grep)")
                
            if problems:
                issues.append({
                    'file': name,
                    'lines': lines,
                    'tools': tools,
                    'problems': problems
                })
                print(f"  [FAIL] {name}: {lines} lines")
                for p in problems:
                    print(f"     {p}")
            else:
                print(f"  [OK] {name}: {lines} lines, tools: {tools}")
                
        return issues
        
    def check_agents(self) -> List[Dict]:
        """Check agent compliance with template"""
        issues = []
        print("\n=== Checking Agents ===")
        
        # Skip coordinators and templates
        skip_patterns = ['coordinator', 'TEMPLATE', 'BASE_AGENT']
        
        for file_path in self.agents_dir.glob('*.md'):
            name = file_path.stem
            
            # Skip coordinators and templates
            if any(pattern in name for pattern in skip_patterns):
                continue
                
            lines = self.count_lines(file_path)
            frontmatter = self.extract_frontmatter(file_path)
            
            problems = []
            
            # Check line count (target <200, max 500 for complex)
            if lines > 500:
                problems.append(f"[WARNING] Very long: {lines} lines (max 500)")
            elif lines > 200:
                # OK for complex agents, just note it
                pass
                
            # Check tools configuration
            tools = frontmatter.get('tools', '')
            if isinstance(tools, str):
                tools_list = [t.strip() for t in tools.split(',')]
            else:
                tools_list = tools if isinstance(tools, list) else []
                
            # Check for Task tool (CRITICAL: must not have)
            if 'Task' in tools_list or 'task' in str(tools).lower():
                problems.append("[CRITICAL] Has Task tool (violates single responsibility!)")
                
            if problems:
                issues.append({
                    'file': name,
                    'lines': lines,
                    'tools': tools,
                    'problems': problems
                })
                print(f"  [FAIL] {name}: {lines} lines")
                for p in problems:
                    print(f"     {p}")
            else:
                # Only show first 20 OK agents to avoid clutter
                if len([i for i in issues if 'problems' not in i]) < 20:
                    print(f"  [OK] {name}: {lines} lines")
                    
        return issues
        
    def generate_report(self) -> str:
        """Generate compliance report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n" + "="*60)
        print("TEMPLATE COMPLIANCE CHECK")
        print("="*60)
        
        command_issues = self.check_commands()
        coordinator_issues = self.check_coordinators()
        agent_issues = self.check_agents()
        
        # Generate summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        print(f"\n[Commands] {len(command_issues)} need fixes")
        if command_issues:
            print("  Priority fixes (over 100 lines):")
            for issue in command_issues:
                if issue['lines'] > 100:
                    print(f"    - {issue['file']}: {issue['lines']} lines")
                    
        print(f"\n[Coordinators] {len(coordinator_issues)} need fixes")
        if coordinator_issues:
            print("  CRITICAL fixes (have Task tool):")
            for issue in coordinator_issues:
                if any('Task tool' in p for p in issue['problems']):
                    print(f"    - {issue['file']}: HAS TASK TOOL!")
                    
        print(f"\n[Agents] {len(agent_issues)} need fixes")
        if agent_issues:
            print("  CRITICAL fixes (have Task tool):")
            for issue in agent_issues:
                if any('Task tool' in p for p in issue['problems']):
                    print(f"    - {issue['file']}: HAS TASK TOOL!")
                    
        # Save detailed report
        report_path = Path('..') / '..' / 'report' / f'template_compliance_{timestamp}.json'
        report_data = {
            'timestamp': timestamp,
            'summary': {
                'commands_needing_fixes': len(command_issues),
                'coordinators_needing_fixes': len(coordinator_issues),
                'agents_needing_fixes': len(agent_issues),
                'total_issues': len(command_issues) + len(coordinator_issues) + len(agent_issues)
            },
            'command_issues': command_issues,
            'coordinator_issues': coordinator_issues,
            'agent_issues': agent_issues
        }
        
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n[Report] Detailed report saved to: {report_path}")
        
        # Priority action items
        print("\n" + "="*60)
        print("PRIORITY ACTIONS")
        print("="*60)
        
        print("\n1. Fix commands over 100 lines (delegate to coordinators)")
        print("2. Remove Task tool from any coordinators/agents")
        print("3. Add proper tools config to coordinators (Read, Write, Bash, Grep)")
        print("4. Ensure agents follow single responsibility principle")
        
        return str(report_path)

if __name__ == '__main__':
    checker = TemplateComplianceChecker()
    report_file = checker.generate_report()
    print(f"\n[COMPLETE] Template compliance check complete!")