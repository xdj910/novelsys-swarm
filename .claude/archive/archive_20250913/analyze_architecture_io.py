#!/usr/bin/env python3
"""
Ultra-Enhanced NOVELSYS-SWARM Architecture Analyzer
Extracts tools, thinking, context, AND input/output specifications
Generates comprehensive architecture report with I/O flow analysis
"""

import os
import yaml
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any

class IOArchitectureAnalyzer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.commands_dir = base_dir / "commands"
        self.agents_dir = base_dir / "agents"
        self.report_dir = base_dir / "report"
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
            
            if content.startswith('---'):
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
    
    def extract_io_specifications(self, content: str) -> Dict[str, Any]:
        """Extract input/output specifications from file content"""
        io_spec = {
            'inputs': [],
            'outputs': [],
            'reads': [],
            'writes': [],
            'file_patterns': []
        }
        
        # Extract READ/Input patterns
        read_patterns = [
            r'(?:MUST )?[Rr]ead (?:the )?([^\n]+)',
            r'Input:?\s*([^\n]+)',
            r'Reads?:?\s*([^\n]+)',
            r'Load (?:the )?([^\n]+)',
            r'Get (?:the )?([^\n]+) from ([^\n]+)'
        ]
        
        for pattern in read_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                # Clean up the match
                match = match.strip()
                if match and not match.startswith('#') and len(match) < 200:
                    io_spec['reads'].append(match)
        
        # Extract WRITE/Output patterns
        write_patterns = [
            r'(?:MUST )?[Ww]rite (?:to )?([^\n]+)',
            r'Output:?\s*([^\n]+)',
            r'Writes?:?\s*([^\n]+)',
            r'Save (?:to )?([^\n]+)',
            r'Create (?:the )?([^\n]+)',
            r'Generate (?:the )?([^\n]+)'
        ]
        
        for pattern in write_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                match = match.strip()
                if match and not match.startswith('#') and len(match) < 200:
                    io_spec['writes'].append(match)
        
        # Extract specific file paths
        file_patterns = [
            r'`([^`]+\.(?:yaml|json|md|txt))`',
            r'"([^"]+\.(?:yaml|json|md|txt))"',
            r'\.claude/[^\s\)]+',
            r'Path:\s*([^\n]+)',
            r'File:\s*([^\n]+)',
            r'Location:\s*([^\n]+)'
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if match and len(match) < 200:
                    io_spec['file_patterns'].append(match)
        
        # Extract structured I/O from sections
        input_section = re.search(r'## (?:INPUTS?|INPUT FILES?|REQUIRED FILES?)\s*\n(.*?)(?=\n##|\n#|\Z)', 
                                 content, re.DOTALL | re.IGNORECASE)
        if input_section:
            lines = input_section.group(1).strip().split('\n')
            for line in lines[:10]:  # Limit to first 10 lines
                if line.strip() and not line.startswith('#'):
                    io_spec['inputs'].append(line.strip())
        
        output_section = re.search(r'## (?:OUTPUTS?|OUTPUT FILES?|GENERATED FILES?)\s*\n(.*?)(?=\n##|\n#|\Z)', 
                                   content, re.DOTALL | re.IGNORECASE)
        if output_section:
            lines = output_section.group(1).strip().split('\n')
            for line in lines[:10]:
                if line.strip() and not line.startswith('#'):
                    io_spec['outputs'].append(line.strip())
        
        # Extract workflow steps that mention I/O
        workflow_section = re.search(r'## (?:WORKFLOW|PROCESS|STEPS?|MANDATORY WORKFLOW)\s*\n(.*?)(?=\n##|\n#|\Z)', 
                                     content, re.DOTALL | re.IGNORECASE)
        if workflow_section:
            workflow_content = workflow_section.group(1)
            
            # Find step-based I/O
            step_patterns = [
                r'STEP \d+:?\s*([^\n]+)',
                r'\d+\.\s*\*?\*?([^\n]+)',
                r'Phase \d+:?\s*([^\n]+)'
            ]
            
            for pattern in step_patterns:
                matches = re.findall(pattern, workflow_content)
                for match in matches[:5]:  # Limit steps
                    if 'read' in match.lower() or 'load' in match.lower():
                        io_spec['reads'].append(f"Step: {match}")
                    elif 'write' in match.lower() or 'save' in match.lower() or 'create' in match.lower():
                        io_spec['writes'].append(f"Step: {match}")
        
        # Deduplicate and clean
        for key in io_spec:
            if isinstance(io_spec[key], list):
                # Remove duplicates while preserving order
                seen = set()
                cleaned = []
                for item in io_spec[key]:
                    if item not in seen and item:
                        seen.add(item)
                        cleaned.append(item[:150])  # Truncate long items
                io_spec[key] = cleaned[:10]  # Limit to 10 items per category
        
        return io_spec
    
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
            'execution_model': None,
            'io_specification': {},
            'dependencies': []
        }
        
        # Extract YAML frontmatter
        frontmatter = self.extract_yaml_frontmatter(file_path)
        
        # Get basic info from frontmatter
        if 'tools' in frontmatter:
            tools_str = frontmatter['tools']
            if isinstance(tools_str, str):
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
        
        # Extract from content
        content = file_path.read_text(encoding='utf-8')
        
        # Extract I/O specifications
        info['io_specification'] = self.extract_io_specifications(content)
        
        # Extract Core Responsibility
        core_resp_match = re.search(r'## Core Responsibility\s*\n(.*?)(?=\n##|\n#|\Z)', content, re.DOTALL)
        if core_resp_match:
            info['core_responsibility'] = core_resp_match.group(1).strip()[:500]
        
        # Extract Execution Model
        exec_model_match = re.search(r'## Execution Model\s*\n(.*?)(?=\n##|\n#|\Z)', content, re.DOTALL)
        if exec_model_match:
            info['execution_model'] = exec_model_match.group(1).strip()[:500]
        
        # Extract dependencies (other agents mentioned)
        agent_mentions = re.findall(r'(?:Use the |call |invoke |delegate to )([a-z][a-z0-9-]+)(?:-specialist|-coordinator| subagent| agent)?', 
                                   content, re.IGNORECASE)
        info['dependencies'] = list(set(agent_mentions))[:10]  # Limit to 10
        
        return info
    
    def scan_all_components(self) -> None:
        """Scan all components with enhanced I/O extraction"""
        print("Scanning all components with I/O analysis...")
        
        # Scan commands (recursively including all subdirectories)
        print("\n1. Scanning commands...")
        for file in self.commands_dir.rglob("*.md"):
            if file.is_file():
                # Determine category based on path
                rel_path = file.relative_to(self.commands_dir)
                category = str(rel_path.parent) if rel_path.parent != Path('.') else "root"
                self.analyze_command_io(file, category)
        
        # Scan all agents (recursively including all subdirectories)
        print("\n2. Scanning agents and coordinators...")
        for file in self.agents_dir.rglob("*.md"):
            if file.is_file() and not file.name.endswith('.bak'):
                agent_name = file.stem
                print(f"  Analyzing: {agent_name}")
                
                # Extract comprehensive info
                agent_info = self.extract_component_info(file)
                
                # Determine if it's a coordinator
                if agent_name.endswith('-coordinator'):
                    self.coordinators[agent_name] = agent_info
                else:
                    self.agents[agent_name] = agent_info
        
        print(f"\nTotal commands: {len(self.commands)}")
        print(f"Total coordinators: {len(self.coordinators)}")
        print(f"Total agents: {len(self.agents)}")
    
    def analyze_command_io(self, command_file: Path, category: str) -> None:
        """Analyze command with I/O extraction"""
        command_name = command_file.stem
        print(f"  Analyzing command: {command_name}")
        
        # Extract comprehensive info
        cmd_info = self.extract_component_info(command_file)
        cmd_info['category'] = category
        cmd_info['coordinator'] = None
        cmd_info['managed_agents'] = []
        
        content = command_file.read_text(encoding='utf-8')
        
        # Find coordinator references
        coordinator_patterns = [
            r'Use the ([a-z-]+)-coordinator subagent',
            r'([a-z-]+)-coordinator'
        ]
        
        for pattern in coordinator_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                cmd_info['coordinator'] = f"{matches[0]}-coordinator"
                break
        
        self.commands[command_name] = cmd_info
    
    def analyze_io_flow(self) -> Dict[str, Any]:
        """Analyze I/O flow patterns across the system"""
        flow_analysis = {
            'common_inputs': {},
            'common_outputs': {},
            'file_types': {},
            'data_flow_patterns': [],
            'missing_specifications': []
        }
        
        # Analyze all I/O specifications
        all_components = {}
        all_components.update(self.commands)
        all_components.update(self.coordinators)
        all_components.update(self.agents)
        
        for name, info in all_components.items():
            io_spec = info.get('io_specification', {})
            
            # Check if I/O is specified
            if not any(io_spec.get(k) for k in ['reads', 'writes', 'inputs', 'outputs']):
                flow_analysis['missing_specifications'].append(name)
            
            # Count file patterns
            for pattern in io_spec.get('file_patterns', []):
                if '.' in pattern:
                    ext = pattern.split('.')[-1].lower()
                    if ext in ['yaml', 'json', 'md', 'txt']:
                        flow_analysis['file_types'][ext] = flow_analysis['file_types'].get(ext, 0) + 1
            
            # Analyze common inputs
            for read_item in io_spec.get('reads', []):
                key = read_item[:50]  # Truncate for grouping
                flow_analysis['common_inputs'][key] = flow_analysis['common_inputs'].get(key, 0) + 1
            
            # Analyze common outputs
            for write_item in io_spec.get('writes', []):
                key = write_item[:50]
                flow_analysis['common_outputs'][key] = flow_analysis['common_outputs'].get(key, 0) + 1
        
        return flow_analysis
    
    def generate_io_report(self) -> str:
        """Generate comprehensive I/O architecture report"""
        
        flow_analysis = self.analyze_io_flow()
        
        report = f"# NOVELSYS-SWARM I/O Architecture Analysis Report\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Executive Summary
        report += f"## Executive Summary\n"
        report += f"- **Total Commands**: {len(self.commands)}\n"
        report += f"- **Total Coordinators**: {len(self.coordinators)}\n"
        report += f"- **Total Agents**: {len(self.agents)}\n"
        report += f"- **Components with I/O specs**: {len(self.commands) + len(self.coordinators) + len(self.agents) - len(flow_analysis['missing_specifications'])}\n"
        report += f"- **Components missing I/O specs**: {len(flow_analysis['missing_specifications'])}\n\n"
        
        # File Type Distribution
        report += f"## File Type Usage\n"
        for ext, count in sorted(flow_analysis['file_types'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **.{ext}**: {count} references\n"
        
        # Common Input Patterns
        report += f"\n## Most Common Input Patterns\n"
        sorted_inputs = sorted(flow_analysis['common_inputs'].items(), key=lambda x: x[1], reverse=True)[:10]
        for pattern, count in sorted_inputs:
            report += f"- {pattern}: {count} components\n"
        
        # Common Output Patterns
        report += f"\n## Most Common Output Patterns\n"
        sorted_outputs = sorted(flow_analysis['common_outputs'].items(), key=lambda x: x[1], reverse=True)[:10]
        for pattern, count in sorted_outputs:
            report += f"- {pattern}: {count} components\n"
        
        # Detailed Component I/O
        report += f"\n## Component I/O Specifications\n"
        
        # Commands
        report += f"\n### Commands with I/O\n"
        for cmd_name in sorted(self.commands.keys()):
            cmd_info = self.commands[cmd_name]
            io_spec = cmd_info.get('io_specification', {})
            
            if any(io_spec.get(k) for k in ['reads', 'writes', 'inputs', 'outputs']):
                report += f"\n#### {cmd_name}\n"
                
                if io_spec.get('reads'):
                    report += f"**Reads:**\n"
                    for item in io_spec['reads'][:5]:
                        report += f"  - {item}\n"
                
                if io_spec.get('writes'):
                    report += f"**Writes:**\n"
                    for item in io_spec['writes'][:5]:
                        report += f"  - {item}\n"
                
                if cmd_info.get('coordinator'):
                    report += f"**Delegates to:** {cmd_info['coordinator']}\n"
        
        # Coordinators
        report += f"\n### Coordinators with I/O\n"
        for coord_name in sorted(self.coordinators.keys()):
            coord_info = self.coordinators[coord_name]
            io_spec = coord_info.get('io_specification', {})
            
            report += f"\n#### {coord_name}\n"
            
            if coord_info.get('tools'):
                report += f"**Tools:** {', '.join(coord_info['tools'])}\n"
            
            if io_spec.get('reads'):
                report += f"**Reads:**\n"
                for item in io_spec['reads'][:5]:
                    report += f"  - {item}\n"
            
            if io_spec.get('writes'):
                report += f"**Writes:**\n"
                for item in io_spec['writes'][:5]:
                    report += f"  - {item}\n"
            
            if coord_info.get('dependencies'):
                report += f"**Orchestrates:** {', '.join(coord_info['dependencies'][:5])}\n"
        
        # Key Agents with I/O
        report += f"\n### Key Agents with I/O\n"
        
        # Filter agents with significant I/O
        agents_with_io = []
        for agent_name, agent_info in self.agents.items():
            io_spec = agent_info.get('io_specification', {})
            io_count = len(io_spec.get('reads', [])) + len(io_spec.get('writes', []))
            if io_count > 0:
                agents_with_io.append((agent_name, agent_info, io_count))
        
        # Sort by I/O complexity
        agents_with_io.sort(key=lambda x: x[2], reverse=True)
        
        for agent_name, agent_info, _ in agents_with_io[:20]:  # Top 20
            io_spec = agent_info.get('io_specification', {})
            
            report += f"\n#### {agent_name}\n"
            
            if agent_info.get('description'):
                report += f"*{agent_info['description'][:100]}*\n"
            
            if agent_info.get('tools'):
                report += f"**Tools:** {', '.join(agent_info['tools'])}\n"
            
            if io_spec.get('reads'):
                report += f"**Reads:**\n"
                for item in io_spec['reads'][:3]:
                    report += f"  - {item}\n"
            
            if io_spec.get('writes'):
                report += f"**Writes:**\n"
                for item in io_spec['writes'][:3]:
                    report += f"  - {item}\n"
            
            if io_spec.get('file_patterns'):
                report += f"**File Patterns:**\n"
                for pattern in io_spec['file_patterns'][:3]:
                    report += f"  - `{pattern}`\n"
        
        # Data Flow Insights
        report += f"\n## Data Flow Insights\n"
        
        # Identify common file paths
        common_paths = {}
        for comp_info in list(self.agents.values()) + list(self.coordinators.values()):
            for pattern in comp_info.get('io_specification', {}).get('file_patterns', []):
                if '.claude' in pattern:
                    path_parts = pattern.split('/')
                    if len(path_parts) > 2:
                        base_path = '/'.join(path_parts[:3])
                        common_paths[base_path] = common_paths.get(base_path, 0) + 1
        
        report += f"\n### Common Data Paths\n"
        for path, count in sorted(common_paths.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- `{path}/...`: {count} references\n"
        
        # Components missing I/O specs
        if flow_analysis['missing_specifications']:
            report += f"\n### Components Missing I/O Specifications ({len(flow_analysis['missing_specifications'])})\n"
            for name in flow_analysis['missing_specifications'][:20]:
                report += f"- {name}\n"
        
        return report
    
    def save_io_report(self, report: str) -> Path:
        """Save I/O report"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = self.report_dir / f"architecture_io_{self.timestamp}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # Also save as latest
        latest_file = self.report_dir / "architecture_io_latest.md"
        latest_file.write_text(report, encoding='utf-8')
        
        return report_file
    
    def save_io_json(self) -> Path:
        """Save I/O JSON data"""
        data = {
            "timestamp": self.timestamp,
            "commands": self.commands,
            "coordinators": self.coordinators,
            "agents": self.agents,
            "io_flow_analysis": self.analyze_io_flow()
        }
        
        json_file = self.report_dir / f"architecture_io_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return json_file
    
    def run_io_analysis(self) -> Tuple[Path, Path]:
        """Run complete I/O analysis"""
        print("="*60)
        print("NOVELSYS-SWARM I/O Architecture Analyzer")
        print("="*60)
        
        # Scan everything with I/O extraction
        self.scan_all_components()
        
        # Generate I/O report
        report = self.generate_io_report()
        report_file = self.save_io_report(report)
        json_file = self.save_io_json()
        
        print(f"\n[OK] I/O analysis complete!")
        print(f"I/O report saved to: {report_file}")
        print(f"I/O JSON saved to: {json_file}")
        
        # Show summary
        flow_analysis = self.analyze_io_flow()
        print(f"\n=== I/O ANALYSIS SUMMARY ===")
        print(f"Components analyzed: {len(self.commands) + len(self.coordinators) + len(self.agents)}")
        print(f"Components with I/O specs: {len(self.commands) + len(self.coordinators) + len(self.agents) - len(flow_analysis['missing_specifications'])}")
        print(f"File types referenced: {len(flow_analysis['file_types'])}")
        print(f"Common input patterns: {len(flow_analysis['common_inputs'])}")
        print(f"Common output patterns: {len(flow_analysis['common_outputs'])}")
        
        return report_file, json_file


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="I/O Architecture Analyzer for NOVELSYS-SWARM")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(r"D:\NOVELSYS-SWARM\.claude"),
        help="Base directory containing commands and agents folders"
    )
    
    args = parser.parse_args()
    
    # Run I/O analysis
    analyzer = IOArchitectureAnalyzer(args.base_dir)
    report_file, json_file = analyzer.run_io_analysis()
    
    print("\nUse the I/O report to understand:")
    print("- What each component reads and writes")
    print("- Data flow patterns across the system")
    print("- File format usage and dependencies")
    print("- I/O specifications for each component")


if __name__ == "__main__":
    main()