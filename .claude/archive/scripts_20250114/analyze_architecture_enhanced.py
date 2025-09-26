#!/usr/bin/env python3
"""
Enhanced NOVELSYS-SWARM Architecture Analyzer
Extracts tools, thinking patterns, and context from all components
Generates comprehensive architecture report with deep insights
"""

import os
import yaml
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any

class EnhancedArchitectureAnalyzer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.commands_dir = base_dir / "commands"
        self.agents_dir = base_dir / "agents"
        self.report_dir = base_dir.parent / "report"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Storage for analysis results
        self.commands: Dict[str, Dict] = {}
        self.coordinators: Dict[str, Dict] = {}
        self.agents: Dict[str, Dict] = {}
        self.unmapped_agents: Set[str] = set()
        
    def extract_yaml_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown files"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for YAML frontmatter
            if content.startswith('---'):
                # Find the closing ---
                end_idx = content.find('---', 3)
                if end_idx != -1:
                    yaml_content = content[3:end_idx]
                    try:
                        return yaml.safe_load(yaml_content) or {}
                    except yaml.YAMLError:
                        return {}
            return {}
        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")
            return {}
    
    def extract_component_info(self, file_path: Path) -> Dict[str, Any]:
        """Extract comprehensive information from a component file"""
        info = {
            'file': str(file_path.relative_to(self.base_dir)),
            'name': file_path.stem,
            'tools': [],
            'thinking': None,
            'description': None,
            'allowed_tools': [],
            'core_responsibility': None,
            'execution_model': None
        }
        
        # Extract YAML frontmatter
        frontmatter = self.extract_yaml_frontmatter(file_path)
        
        # Get basic info from frontmatter
        if 'tools' in frontmatter:
            tools_str = frontmatter['tools']
            if isinstance(tools_str, str):
                # Parse tools string (e.g., "Read, Write, Bash")
                info['tools'] = [t.strip() for t in tools_str.split(',')]
            elif isinstance(tools_str, list):
                info['tools'] = tools_str
        
        if 'thinking' in frontmatter:
            info['thinking'] = frontmatter['thinking']
        
        if 'description' in frontmatter:
            info['description'] = frontmatter['description']
        
        if 'allowed-tools' in frontmatter:
            allowed = frontmatter['allowed-tools']
            if isinstance(allowed, str):
                info['allowed_tools'] = [t.strip() for t in allowed.split(',')]
            elif isinstance(allowed, list):
                info['allowed_tools'] = allowed
        
        # Extract additional context from content
        content = file_path.read_text(encoding='utf-8')
        
        # Extract Core Responsibility section
        core_resp_match = re.search(r'## Core Responsibility\s*\n(.*?)(?=\n##|\n#|\Z)', content, re.DOTALL)
        if core_resp_match:
            info['core_responsibility'] = core_resp_match.group(1).strip()[:500]  # Limit length
        
        # Extract Execution Model section
        exec_model_match = re.search(r'## Execution Model\s*\n(.*?)(?=\n##|\n#|\Z)', content, re.DOTALL)
        if exec_model_match:
            info['execution_model'] = exec_model_match.group(1).strip()[:500]
        
        return info
    
    def scan_all_commands(self) -> None:
        """Scan all command files recursively with enhanced info extraction"""
        print("Scanning for commands with enhanced analysis...")
        
        # Scan root level commands
        for file in self.commands_dir.glob("*.md"):
            if file.is_file():
                self.analyze_command_enhanced(file, "root")
        
        # Scan subdirectories (like novel/)
        for subdir in self.commands_dir.iterdir():
            if subdir.is_dir():
                for file in subdir.glob("*.md"):
                    if file.is_file():
                        self.analyze_command_enhanced(file, subdir.name)
    
    def analyze_command_enhanced(self, command_file: Path, category: str) -> None:
        """Analyze command with enhanced info extraction"""
        command_name = command_file.stem
        print(f"  Analyzing command: {command_name} ({category})")
        
        # Extract comprehensive info
        cmd_info = self.extract_component_info(command_file)
        cmd_info['category'] = category
        cmd_info['coordinator'] = None
        cmd_info['agents'] = []
        cmd_info['directly_called_agents'] = []
        
        content = command_file.read_text(encoding='utf-8')
        
        # Find coordinator references
        coordinator_patterns = [
            r'Use the ([a-z-]+)-coordinator subagent',
            r'([a-z-]+)-coordinator',
            r'coordinator:\s*([a-z-]+)-coordinator'
        ]
        
        for pattern in coordinator_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                coordinator_name = f"{matches[0]}-coordinator"
                cmd_info['coordinator'] = coordinator_name
                break
        
        # Find directly called agents
        agent_patterns = [
            r'Use the ([a-z][a-z0-9-]+) subagent',
            r'Use the ([a-z][a-z0-9-]+) agent',
        ]
        
        for pattern in agent_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if not match.endswith('-coordinator'):
                    cmd_info['directly_called_agents'].append(match)
        
        self.commands[command_name] = cmd_info
    
    def scan_all_coordinators(self) -> None:
        """Scan coordinator files with enhanced analysis"""
        print("\nScanning coordinators with enhanced analysis...")
        
        for command_name, command_info in self.commands.items():
            if command_info['coordinator']:
                coordinator_file = self.agents_dir / f"{command_info['coordinator']}.md"
                if coordinator_file.exists():
                    self.analyze_coordinator_enhanced(coordinator_file, command_name)
    
    def analyze_coordinator_enhanced(self, coordinator_file: Path, command_name: str) -> None:
        """Analyze coordinator with enhanced info extraction"""
        coordinator_name = coordinator_file.stem
        print(f"  Analyzing coordinator: {coordinator_name}")
        
        # Extract comprehensive info
        coord_info = self.extract_component_info(coordinator_file)
        
        content = coordinator_file.read_text(encoding='utf-8')
        
        # Find agent invocations - First check JSON structures
        found_agents = set()
        
        # Look for agents in JSON plan structures
        json_agent_pattern = r'"agent"\s*:\s*"([^"]+)"'
        json_matches = re.findall(json_agent_pattern, content)
        for match in json_matches:
            agent_name = match.strip()
            if (not agent_name.endswith('-coordinator') and 
                len(agent_name) > 3 and
                len(agent_name) < 50):
                found_agents.add(agent_name)
        
        # Also check for traditional patterns
        agent_patterns = [
            r'Use the ([a-z][a-z0-9-]+) subagent',
            r'([a-z][a-z0-9-]+-specialist) subagent',
            r'"([a-z][a-z0-9-]+-specialist)"',
            r'`([a-z][a-z0-9-]+-specialist)`'
        ]
        
        for pattern in agent_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                agent_name = match.lower().replace(' ', '-')
                # Validate agent name
                if (not agent_name.endswith('-coordinator') and 
                    not agent_name.startswith('the-') and
                    len(agent_name) > 3 and
                    len(agent_name) < 50 and
                    not any(word in agent_name for word in ['any', 'each', 'appropriate', 'between'])):
                    found_agents.add(agent_name)
        
        coord_info['manages_agents'] = sorted(list(found_agents))
        self.coordinators[coordinator_name] = coord_info
        
        # Update command info with agents
        self.commands[command_name]['agents'] = coord_info['manages_agents']
    
    def scan_all_agents(self) -> None:
        """Scan all agents with enhanced info extraction"""
        print("\nScanning all agents with enhanced analysis...")
        
        for file in self.agents_dir.glob("*.md"):
            if file.is_file() and not file.name.endswith('.bak'):
                agent_name = file.stem
                print(f"  Analyzing agent: {agent_name}")
                
                # Extract comprehensive info
                agent_info = self.extract_component_info(file)
                self.agents[agent_name] = agent_info
        
        # Find unmapped agents
        used_agents = set()
        for cmd_info in self.commands.values():
            if cmd_info['coordinator']:
                used_agents.add(cmd_info['coordinator'])
            used_agents.update(cmd_info['agents'])
            used_agents.update(cmd_info['directly_called_agents'])
        
        all_agents = set(self.agents.keys())
        self.unmapped_agents = all_agents - used_agents
        
        print(f"  Total agents analyzed: {len(self.agents)}")
        print(f"  Unmapped agents: {len(self.unmapped_agents)}")
    
    def analyze_tool_usage(self) -> Dict[str, Any]:
        """Analyze tool usage patterns across the system"""
        tool_stats = {
            'most_common_tools': {},
            'tool_by_component_type': {
                'commands': {},
                'coordinators': {},
                'agents': {}
            },
            'components_with_bash': [],
            'components_with_task': [],
            'components_with_thinking': []
        }
        
        # Analyze commands
        for cmd_name, cmd_info in self.commands.items():
            for tool in cmd_info.get('tools', []):
                tool_stats['tool_by_component_type']['commands'][tool] = \
                    tool_stats['tool_by_component_type']['commands'].get(tool, 0) + 1
                tool_stats['most_common_tools'][tool] = \
                    tool_stats['most_common_tools'].get(tool, 0) + 1
            
            if 'Bash' in cmd_info.get('tools', []):
                tool_stats['components_with_bash'].append(f"cmd:{cmd_name}")
            if 'Task' in cmd_info.get('tools', []) or 'Task' in cmd_info.get('allowed_tools', []):
                tool_stats['components_with_task'].append(f"cmd:{cmd_name}")
            if cmd_info.get('thinking'):
                tool_stats['components_with_thinking'].append(f"cmd:{cmd_name}")
        
        # Analyze coordinators
        for coord_name, coord_info in self.coordinators.items():
            for tool in coord_info.get('tools', []):
                tool_stats['tool_by_component_type']['coordinators'][tool] = \
                    tool_stats['tool_by_component_type']['coordinators'].get(tool, 0) + 1
                tool_stats['most_common_tools'][tool] = \
                    tool_stats['most_common_tools'].get(tool, 0) + 1
            
            if 'Bash' in coord_info.get('tools', []):
                tool_stats['components_with_bash'].append(f"coord:{coord_name}")
            if 'Task' in coord_info.get('tools', []) or 'Task' in coord_info.get('allowed_tools', []):
                tool_stats['components_with_task'].append(f"coord:{coord_name}")
            if coord_info.get('thinking'):
                tool_stats['components_with_thinking'].append(f"coord:{coord_name}")
        
        # Analyze agents
        for agent_name, agent_info in self.agents.items():
            for tool in agent_info.get('tools', []):
                tool_stats['tool_by_component_type']['agents'][tool] = \
                    tool_stats['tool_by_component_type']['agents'].get(tool, 0) + 1
                tool_stats['most_common_tools'][tool] = \
                    tool_stats['most_common_tools'].get(tool, 0) + 1
            
            if 'Bash' in agent_info.get('tools', []):
                tool_stats['components_with_bash'].append(f"agent:{agent_name}")
            if 'Task' in agent_info.get('tools', []) or 'Task' in agent_info.get('allowed_tools', []):
                tool_stats['components_with_task'].append(f"agent:{agent_name}")
            if agent_info.get('thinking'):
                tool_stats['components_with_thinking'].append(f"agent:{agent_name}")
        
        return tool_stats
    
    def generate_enhanced_report(self) -> str:
        """Generate comprehensive enhanced architecture report"""
        
        tool_stats = self.analyze_tool_usage()
        
        report = f"# NOVELSYS-SWARM Enhanced Architecture Analysis Report\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Executive Summary
        report += f"## Executive Summary\n"
        report += f"- **Total Commands**: {len(self.commands)}\n"
        report += f"- **Total Coordinators**: {len(self.coordinators)}\n"
        report += f"- **Total Agents**: {len(self.agents)}\n"
        report += f"- **Unmapped Agents**: {len(self.unmapped_agents)}\n"
        report += f"- **Components with Thinking**: {len(tool_stats['components_with_thinking'])}\n"
        report += f"- **Components with Bash**: {len(tool_stats['components_with_bash'])}\n\n"
        
        # Tool Usage Analysis
        report += f"## Tool Usage Analysis\n\n"
        
        report += f"### Most Common Tools Overall\n"
        sorted_tools = sorted(tool_stats['most_common_tools'].items(), key=lambda x: x[1], reverse=True)
        for tool, count in sorted_tools[:10]:
            report += f"- **{tool}**: used {count} times\n"
        
        report += f"\n### Tool Distribution by Component Type\n"
        for comp_type, tools in tool_stats['tool_by_component_type'].items():
            if tools:
                report += f"\n#### {comp_type.capitalize()}\n"
                sorted_comp_tools = sorted(tools.items(), key=lambda x: x[1], reverse=True)
                for tool, count in sorted_comp_tools:
                    report += f"- {tool}: {count} components\n"
        
        # Commands with Enhanced Info and Call Chain
        report += f"\n## Commands Analysis with Full Call Chain (血脉关系)\n"
        
        for cmd_name in sorted(self.commands.keys()):
            cmd_info = self.commands[cmd_name]
            report += f"\n### 🔗 {cmd_name}\n"
            report += f"- **Category**: {cmd_info['category']}\n"
            report += f"- **File**: {cmd_info['file']}\n"
            
            if cmd_info.get('description'):
                report += f"- **Description**: {cmd_info['description']}\n"
            
            if cmd_info.get('tools'):
                report += f"- **Tools**: {', '.join(cmd_info['tools'])}\n"
            
            if cmd_info.get('thinking'):
                report += f"- **Has Thinking Pattern**: Yes\n"
                report += f"  - Preview: {cmd_info['thinking'][:100]}...\n"
            
            # Show complete call chain
            report += f"\n#### 📊 Complete Call Chain (调用链路):\n"
            report += f"```\n"
            report += f"User → /{cmd_info['category']}:{cmd_name}\n"
            report += f"  ↓\n"
            report += f"Main Claude (orchestrator with Task tool)\n"
            
            if cmd_info['coordinator']:
                report += f"  ↓ [Task]\n"
                report += f"  {cmd_info['coordinator']} (coordinator)\n"
                
                # Show coordinator tools
                if cmd_info['coordinator'] in self.coordinators:
                    coord_tools = self.coordinators[cmd_info['coordinator']].get('tools', [])
                    if coord_tools:
                        report += f"    Tools: [{', '.join(coord_tools)}]\n"
                    report += f"    ↓ [Returns JSON plan]\n"
                    report += f"  Main Claude executes plan\n"
                    
                    # Show agents that will be called
                    if cmd_info['agents']:
                        report += f"    ↓ [Task calls to agents]\n"
                        for i, agent in enumerate(cmd_info['agents'][:10]):
                            if agent in self.agents:
                                agent_tools = self.agents[agent].get('tools', [])
                                if i < len(cmd_info['agents']) - 1:
                                    report += f"    ├─→ {agent} [{', '.join(agent_tools) if agent_tools else 'No tools'}]\n"
                                else:
                                    report += f"    └─→ {agent} [{', '.join(agent_tools) if agent_tools else 'No tools'}]\n"
                        if len(cmd_info['agents']) > 10:
                            report += f"    └─→ ... and {len(cmd_info['agents']) - 10} more agents\n"
            
            elif cmd_info['directly_called_agents']:
                report += f"  ↓ [Task]\n"
                for agent in cmd_info['directly_called_agents'][:5]:
                    if agent in self.agents:
                        agent_tools = self.agents[agent].get('tools', [])
                        report += f"  → {agent} [{', '.join(agent_tools) if agent_tools else 'No tools'}]\n"
            else:
                report += f"  ↓ [Direct execution]\n"
                report += f"  → Uses tools directly\n"
            
            report += f"```\n"
        
        # Coordinators Analysis
        report += f"\n## Coordinators Analysis (Enhanced)\n"
        
        for coord_name in sorted(self.coordinators.keys()):
            coord_info = self.coordinators[coord_name]
            report += f"\n### {coord_name}\n"
            
            if coord_info.get('description'):
                report += f"- **Description**: {coord_info['description']}\n"
            
            if coord_info.get('tools'):
                report += f"- **Tools**: {', '.join(coord_info['tools'])}\n"
            
            if coord_info.get('thinking'):
                report += f"- **Thinking Pattern**: Yes\n"
                report += f"  - Preview: {coord_info['thinking'][:150]}...\n"
            
            if coord_info.get('manages_agents'):
                report += f"- **Manages**: {len(coord_info['manages_agents'])} agents\n"
        
        # Agents with Thinking Patterns
        report += f"\n## Agents with Advanced Capabilities\n"
        
        thinking_agents = [name for name, info in self.agents.items() if info.get('thinking')]
        bash_agents = [name for name, info in self.agents.items() if 'Bash' in info.get('tools', [])]
        
        report += f"\n### Agents with Thinking Patterns ({len(thinking_agents)})\n"
        for agent in sorted(thinking_agents)[:10]:
            agent_info = self.agents[agent]
            report += f"- **{agent}**\n"
            if agent_info.get('tools'):
                report += f"  - Tools: {', '.join(agent_info['tools'])}\n"
            thinking = agent_info.get('thinking', '')
            if isinstance(thinking, str) and thinking:
                report += f"  - Thinking: {thinking[:100]}...\n"
            elif thinking:
                report += f"  - Thinking: Present\n"
        
        report += f"\n### Agents with Bash Access ({len(bash_agents)})\n"
        for agent in sorted(bash_agents)[:10]:
            report += f"- {agent}\n"
        
        # Complete System Blood Lineage (系统血脉图谱)
        report += f"\n## 🩸 Complete System Blood Lineage (系统血脉图谱)\n"
        report += f"\n### Layer Architecture (层级架构)\n"
        report += f"```\n"
        report += f"┌─────────────────────────────────────────────┐\n"
        report += f"│         USER INTERFACE LAYER                │\n"
        report += f"│         Commands: {len(self.commands):3} files                 │\n"
        report += f"├─────────────────────────────────────────────┤\n"
        report += f"│         ORCHESTRATION LAYER                 │\n"
        report += f"│         Main Claude (with Task tool)        │\n"
        report += f"├─────────────────────────────────────────────┤\n"
        report += f"│         PLANNING LAYER                      │\n"
        report += f"│         Coordinators: {len(self.coordinators):3} components        │\n"
        report += f"│         Tools: Read, Write, Bash, Grep      │\n"
        report += f"│         (NO Task tool - prevents recursion) │\n"
        report += f"├─────────────────────────────────────────────┤\n"
        report += f"│         EXECUTION LAYER                     │\n"
        report += f"│         Agents: {len(self.agents):3} specialized tools      │\n"
        report += f"│         Tools: Task-specific only           │\n"
        report += f"│         (NO Task tool - single responsibility)│\n"
        report += f"├─────────────────────────────────────────────┤\n"
        report += f"│         DATA/FILE SYSTEM LAYER              │\n"
        report += f"│         Communication via file I/O          │\n"
        report += f"│         (Prevents recursion, enables parallel)│\n"
        report += f"└─────────────────────────────────────────────┘\n"
        report += f"```\n"
        
        # Recursion Safety Check
        report += f"\n### 🛡️ Recursion Safety Analysis\n"
        if tool_stats['components_with_task']:
            report += f"⚠️ WARNING: {len(tool_stats['components_with_task'])} components have Task tool:\n"
            for comp in tool_stats['components_with_task'][:10]:
                report += f"  - {comp}\n"
            if len(tool_stats['components_with_task']) > 10:
                report += f"  - ... and {len(tool_stats['components_with_task']) - 10} more\n"
        else:
            report += f"✅ SAFE: No coordinators or agents have Task tool (recursion impossible)\n"
        
        # Architecture Insights
        report += f"\n## Architecture Insights\n"
        
        # Calculate percentages
        total_components = len(self.commands) + len(self.coordinators) + len(self.agents)
        thinking_pct = len(tool_stats['components_with_thinking']) * 100 // total_components if total_components > 0 else 0
        bash_pct = len(tool_stats['components_with_bash']) * 100 // total_components if total_components > 0 else 0
        
        report += f"\n### Capability Distribution\n"
        report += f"- Components with Thinking: {thinking_pct}%\n"
        report += f"- Components with Bash: {bash_pct}%\n"
        report += f"- Components with Task: {len(tool_stats['components_with_task'])}\n"
        
        # Unmapped Agents Summary
        if self.unmapped_agents:
            report += f"\n## Unmapped Agents ({len(self.unmapped_agents)})\n"
            for agent in sorted(self.unmapped_agents)[:20]:
                if agent in self.agents:
                    agent_info = self.agents[agent]
                    tools_str = f" (Tools: {', '.join(agent_info['tools'])})" if agent_info.get('tools') else ""
                    report += f"- {agent}{tools_str}\n"
        
        return report
    
    def save_enhanced_report(self, report: str) -> Path:
        """Save enhanced report"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = self.report_dir / f"architecture_enhanced_{self.timestamp}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # Also save as latest
        latest_file = self.report_dir / "architecture_enhanced_latest.md"
        latest_file.write_text(report, encoding='utf-8')
        
        return report_file
    
    def save_enhanced_json(self) -> Path:
        """Save enhanced JSON data"""
        data = {
            "timestamp": self.timestamp,
            "commands": self.commands,
            "coordinators": self.coordinators,
            "agents": self.agents,
            "unmapped_agents": sorted(list(self.unmapped_agents)),
            "tool_analysis": self.analyze_tool_usage()
        }
        
        json_file = self.report_dir / f"architecture_enhanced_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return json_file
    
    def run_enhanced_analysis(self) -> Tuple[Path, Path]:
        """Run complete enhanced analysis"""
        print("="*60)
        print("NOVELSYS-SWARM Enhanced Architecture Analyzer")
        print("="*60)
        
        # Scan everything with enhanced extraction
        self.scan_all_commands()
        self.scan_all_coordinators()
        self.scan_all_agents()
        
        # Generate enhanced report
        report = self.generate_enhanced_report()
        report_file = self.save_enhanced_report(report)
        json_file = self.save_enhanced_json()
        
        print(f"\n[OK] Enhanced analysis complete!")
        print(f"Enhanced report saved to: {report_file}")
        print(f"Enhanced JSON saved to: {json_file}")
        
        # Show summary
        tool_stats = self.analyze_tool_usage()
        print(f"\n=== ENHANCED ANALYSIS SUMMARY ===")
        print(f"Commands analyzed: {len(self.commands)}")
        print(f"Coordinators analyzed: {len(self.coordinators)}")
        print(f"Agents analyzed: {len(self.agents)}")
        print(f"Components with thinking: {len(tool_stats['components_with_thinking'])}")
        print(f"Components with Bash access: {len(tool_stats['components_with_bash'])}")
        
        return report_file, json_file


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced NOVELSYS-SWARM architecture analyzer")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(r"D:\NOVELSYS-SWARM\.claude\ForReview"),
        help="Base directory containing commands and agents folders"
    )
    
    args = parser.parse_args()
    
    # Run enhanced analysis
    analyzer = EnhancedArchitectureAnalyzer(args.base_dir)
    report_file, json_file = analyzer.run_enhanced_analysis()
    
    print("\nUse the enhanced report to understand:")
    print("- Tool usage patterns across components")
    print("- Which components have thinking capabilities")
    print("- Bash access distribution")
    print("- Complete component relationships with context")


if __name__ == "__main__":
    main()