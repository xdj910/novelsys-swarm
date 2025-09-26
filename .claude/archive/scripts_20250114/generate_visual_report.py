#!/usr/bin/env python3
"""
NOVELSYS-SWARM Visual Architecture Report Generator
Generates comprehensive visual reports with ASCII art, charts, and Mermaid diagrams
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
import re

class VisualReportGenerator:
    def __init__(self, base_dir: Path = Path('..')):
        self.base_dir = base_dir
        self.commands_dir = base_dir / "commands"
        self.agents_dir = base_dir / "agents"
        self.data_dir = base_dir / "data"
        self.report_dir = base_dir.parent / "report"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Storage for analysis
        self.commands = {}
        self.coordinators = {}
        self.agents = {}
        self.call_chains = {}
        
    def load_architecture_data(self):
        """Load existing architecture analysis data"""
        # Try to find the latest architecture JSON
        json_files = list(Path('.').glob('report/architecture_enhanced_*.json'))
        if json_files:
            latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
            with open(latest_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.commands = data.get('commands', {})
                self.coordinators = data.get('coordinators', {})
                self.agents = data.get('agents', {})
                return True
        return False
    
    def generate_ascii_flow_diagram(self, command_name: str, cmd_info: Dict) -> str:
        """Generate ASCII art flow diagram for a command"""
        diagram = []
        
        # Header
        diagram.append(f"\n{'='*60}")
        diagram.append(f"Command: /{cmd_info.get('category', 'root')}:{command_name}")
        diagram.append(f"{'='*60}\n")
        
        # Start with user
        diagram.append("     [USER]")
        diagram.append("        |")
        diagram.append("        v")
        diagram.append(f"  /{cmd_info.get('category', 'root')}:{command_name}")
        diagram.append("        |")
        diagram.append("        v")
        diagram.append("  [Main Claude]")
        diagram.append("   (Orchestrator)")
        
        # Check if it has a coordinator
        if cmd_info.get('coordinator'):
            coord = cmd_info['coordinator']
            diagram.append("        |")
            diagram.append("    Task tool")
            diagram.append("        |")
            diagram.append("        v")
            diagram.append(f"  [{coord}]")
            
            # Get coordinator tools
            if coord in self.coordinators:
                tools = self.coordinators[coord].get('tools', [])
                if tools:
                    diagram.append(f"  Tools: {', '.join(tools[:4])}")
            
            diagram.append("        |")
            diagram.append("   JSON Plan")
            diagram.append("        |")
            diagram.append("        v")
            diagram.append("  [Main Claude]")
            diagram.append("   Executes Plan")
            
            # Show agents
            agents = cmd_info.get('agents', [])
            if agents:
                diagram.append("        |")
                diagram.append("    Parallel/Serial")
                diagram.append("        |")
                
                # Create agent tree
                for i, agent in enumerate(agents[:8]):  # Show max 8 agents
                    if i == 0:
                        diagram.append(f"        +----> [{agent}]")
                    elif i < len(agents) - 1:
                        diagram.append(f"        |----> [{agent}]")
                    else:
                        diagram.append(f"        +----> [{agent}]")
                
                if len(agents) > 8:
                    diagram.append(f"        +----> ... ({len(agents) - 8} more)")
        
        elif cmd_info.get('directly_called_agents'):
            # Direct agent calls
            agents = cmd_info['directly_called_agents']
            diagram.append("        |")
            diagram.append("    Task tool")
            diagram.append("        |")
            for agent in agents[:5]:
                diagram.append(f"        +----> [{agent}]")
        else:
            # Direct execution
            diagram.append("        |")
            diagram.append("  Direct Execution")
            diagram.append("   (Uses tools)")
        
        return '\n'.join(diagram)
    
    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram code for the entire architecture"""
        mermaid = ["```mermaid", "graph TB"]
        
        # Style definitions
        mermaid.append("    classDef userStyle fill:#e1f5fe,stroke:#01579b,stroke-width:2px")
        mermaid.append("    classDef commandStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px")
        mermaid.append("    classDef claudeStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:3px")
        mermaid.append("    classDef coordStyle fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px")
        mermaid.append("    classDef agentStyle fill:#fce4ec,stroke:#880e4f,stroke-width:1px")
        mermaid.append("")
        
        # User node
        mermaid.append("    User[User]:::userStyle")
        mermaid.append("")
        
        # Main Claude
        mermaid.append("    MainClaude[Main Claude<br/>Orchestrator with Task]:::claudeStyle")
        mermaid.append("")
        
        # Add commands and their chains
        for i, (cmd_name, cmd_info) in enumerate(list(self.commands.items())[:10]):  # Limit to 10 for readability
            cmd_id = f"cmd{i}"
            category = cmd_info.get('category', 'root')
            
            # Command node
            mermaid.append(f"    {cmd_id}[/{category}:{cmd_name}]:::commandStyle")
            mermaid.append(f"    User --> {cmd_id}")
            mermaid.append(f"    {cmd_id} --> MainClaude")
            
            # Coordinator
            if cmd_info.get('coordinator'):
                coord_id = f"coord{i}"
                coord_name = cmd_info['coordinator']
                mermaid.append(f"    {coord_id}[{coord_name}<br/>Coordinator]:::coordStyle")
                mermaid.append(f"    MainClaude -->|Task| {coord_id}")
                mermaid.append(f"    {coord_id} -->|JSON Plan| MainClaude")
                
                # Agents
                agents = cmd_info.get('agents', [])
                for j, agent in enumerate(agents[:3]):  # Show max 3 agents per coordinator
                    agent_id = f"agent{i}_{j}"
                    mermaid.append(f"    {agent_id}[{agent}]:::agentStyle")
                    mermaid.append(f"    MainClaude -->|Task| {agent_id}")
        
        mermaid.append("```")
        return '\n'.join(mermaid)
    
    def generate_statistics_charts(self) -> str:
        """Generate visual statistics charts using ASCII art"""
        charts = []
        
        # Tool usage bar chart
        charts.append("\n" + "="*60)
        charts.append("TOOL USAGE DISTRIBUTION")
        charts.append("="*60)
        
        tool_counts = {}
        for agent_info in self.agents.values():
            for tool in agent_info.get('tools', []):
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        # Sort by count
        sorted_tools = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Create bar chart
        max_count = max(tool_counts.values()) if tool_counts else 1
        for tool, count in sorted_tools[:10]:
            bar_width = int((count / max_count) * 40)
            bar = '█' * bar_width
            charts.append(f"{tool:15} {bar} {count}")
        
        # Component distribution pie chart (ASCII representation)
        charts.append("\n" + "="*60)
        charts.append("COMPONENT DISTRIBUTION")
        charts.append("="*60)
        
        total = len(self.commands) + len(self.coordinators) + len(self.agents)
        cmd_pct = int((len(self.commands) / total) * 100) if total > 0 else 0
        coord_pct = int((len(self.coordinators) / total) * 100) if total > 0 else 0
        agent_pct = int((len(self.agents) / total) * 100) if total > 0 else 0
        
        charts.append(f"""
        ╔════════════════════════════════════╗
        ║     SYSTEM COMPONENTS              ║
        ╠════════════════════════════════════╣
        ║ Commands      : {len(self.commands):3} ({cmd_pct:3}%) {'▓' * (cmd_pct // 5):<20} ║
        ║ Coordinators  : {len(self.coordinators):3} ({coord_pct:3}%) {'▒' * (coord_pct // 5):<20} ║
        ║ Agents        : {len(self.agents):3} ({agent_pct:3}%) {'░' * (agent_pct // 5):<20} ║
        ╚════════════════════════════════════╝
        """)
        
        # Thinking vs Non-thinking components
        thinking_count = sum(1 for a in self.agents.values() if a.get('thinking'))
        non_thinking = len(self.agents) - thinking_count
        
        charts.append("\n" + "="*60)
        charts.append("AGENT CAPABILITIES")
        charts.append("="*60)
        
        charts.append(f"""
        With Thinking    : {thinking_count:3} agents  [{'#' * (thinking_count // 3)}]
        Without Thinking : {non_thinking:3} agents  [{'.' * (non_thinking // 3)}]
        """)
        
        return '\n'.join(charts)
    
    def generate_dependency_matrix(self) -> str:
        """Generate a dependency matrix showing coordinator-agent relationships"""
        matrix = []
        
        matrix.append("\n" + "="*60)
        matrix.append("COORDINATOR-AGENT DEPENDENCY MATRIX")
        matrix.append("="*60)
        matrix.append("")
        
        # Create a simplified matrix for top coordinators
        top_coords = sorted(
            [(k, v) for k, v in self.coordinators.items() if v.get('manages_agents')],
            key=lambda x: len(x[1].get('manages_agents', [])),
            reverse=True
        )[:5]  # Top 5 coordinators by agent count
        
        if top_coords:
            # Header
            matrix.append("Coordinator" + " " * 25 + "Agents Managed")
            matrix.append("-" * 60)
            
            for coord_name, coord_info in top_coords:
                agents = coord_info.get('manages_agents', [])
                agent_count = len(agents)
                
                # Show coordinator name and count
                matrix.append(f"{coord_name[:30]:<30} [{agent_count:2}] {'█' * min(agent_count, 20)}")
                
                # Show first few agents
                for agent in agents[:3]:
                    matrix.append(f"  └─> {agent}")
                if len(agents) > 3:
                    matrix.append(f"  └─> ... and {len(agents) - 3} more")
                matrix.append("")
        
        return '\n'.join(matrix)
    
    def generate_call_depth_analysis(self) -> str:
        """Analyze and visualize call chain depths"""
        analysis = []
        
        analysis.append("\n" + "="*60)
        analysis.append("CALL CHAIN DEPTH ANALYSIS")
        analysis.append("="*60)
        analysis.append("")
        
        # Categorize by depth
        direct_exec = []
        single_agent = []
        coordinator_based = []
        
        for cmd_name, cmd_info in self.commands.items():
            if cmd_info.get('coordinator'):
                coordinator_based.append(cmd_name)
            elif cmd_info.get('directly_called_agents'):
                single_agent.append(cmd_name)
            else:
                direct_exec.append(cmd_name)
        
        analysis.append(f"Direct Execution (Depth 1): {len(direct_exec)} commands")
        for cmd in direct_exec[:3]:
            analysis.append(f"  • {cmd}")
        
        analysis.append(f"\nSingle Agent (Depth 2): {len(single_agent)} commands")
        for cmd in single_agent[:3]:
            analysis.append(f"  • {cmd}")
        
        analysis.append(f"\nCoordinator Pattern (Depth 3+): {len(coordinator_based)} commands")
        for cmd in coordinator_based[:5]:
            cmd_info = self.commands[cmd]
            agent_count = len(cmd_info.get('agents', []))
            analysis.append(f"  • {cmd} → {cmd_info.get('coordinator', 'N/A')} → {agent_count} agents")
        
        return '\n'.join(analysis)
    
    def generate_visual_report(self) -> str:
        """Generate complete visual report"""
        report = []
        
        # Header
        report.append("="*80)
        report.append("NOVELSYS-SWARM VISUAL ARCHITECTURE REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*80)
        
        # Load data
        if not self.load_architecture_data():
            # If no existing data, do basic scan
            self.scan_basic_structure()
        
        # Executive Summary with visual box
        report.append(f"""
╔══════════════════════════════════════════════════════════════╗
║                    EXECUTIVE SUMMARY                         ║
╠══════════════════════════════════════════════════════════════╣
║  Total Commands     : {len(self.commands):4}                                   ║
║  Total Coordinators : {len(self.coordinators):4}                                   ║
║  Total Agents       : {len(self.agents):4}                                   ║
║  Total Components   : {len(self.commands) + len(self.coordinators) + len(self.agents):4}                                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Layer Architecture
        report.append("""
┌───────────────────────────────────────────────────────────┐
│                  SYSTEM ARCHITECTURE                      │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │         1. USER INTERFACE LAYER                 │    │
│  │         Commands (Entry Points)                 │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────┐    │
│  │         2. ORCHESTRATION LAYER                  │    │
│  │         Main Claude (Task Tool Owner)           │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────┐    │
│  │         3. PLANNING LAYER                       │    │
│  │         Coordinators (JSON Planners)            │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────┐    │
│  │         4. EXECUTION LAYER                      │    │
│  │         Agents (Task Executors)                 │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────┐    │
│  │         5. DATA/FILE SYSTEM LAYER               │    │
│  │         Persistent Storage & Communication      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
└───────────────────────────────────────────────────────────┘
        """)
        
        # Add statistics charts
        report.append(self.generate_statistics_charts())
        
        # Add dependency matrix
        report.append(self.generate_dependency_matrix())
        
        # Add call depth analysis
        report.append(self.generate_call_depth_analysis())
        
        # Add sample flow diagrams
        report.append("\n" + "="*60)
        report.append("SAMPLE COMMAND FLOW DIAGRAMS")
        report.append("="*60)
        
        # Show flow for a few key commands
        sample_commands = ['chapter-start', 'book-complete', 'quality-check-individual']
        for cmd in sample_commands:
            if cmd in self.commands:
                report.append(self.generate_ascii_flow_diagram(cmd, self.commands[cmd]))
        
        # Add Mermaid diagram
        report.append("\n" + "="*60)
        report.append("MERMAID DIAGRAM CODE")
        report.append("(Copy to any Mermaid renderer for interactive visualization)")
        report.append("="*60)
        report.append(self.generate_mermaid_diagram())
        
        # Recursion safety check with visual indicator
        report.append("\n" + "="*60)
        report.append("RECURSION SAFETY CHECK")
        report.append("="*60)
        
        # Check for Task tool in coordinators/agents
        task_violations = []
        for coord_name, coord_info in self.coordinators.items():
            if 'Task' in coord_info.get('tools', []):
                task_violations.append(f"COORDINATOR: {coord_name}")
        
        for agent_name, agent_info in self.agents.items():
            if 'Task' in agent_info.get('tools', []):
                task_violations.append(f"AGENT: {agent_name}")
        
        if task_violations:
            report.append("""
        ╔══════════════════════════════════════╗
        ║  WARNING: RECURSION RISK DETECTED!   ║
        ╚══════════════════════════════════════╝
            """)
            for violation in task_violations[:10]:
                report.append(f"  [X] {violation}")
        else:
            report.append("""
        ╔══════════════════════════════════════╗
        ║  [OK] SYSTEM IS RECURSION-SAFE       ║
        ║  No Task tool in coordinators/agents ║
        ╚══════════════════════════════════════╝
            """)
        
        return '\n'.join(report)
    
    def scan_basic_structure(self):
        """Basic scan if no existing data"""
        # Scan commands
        for cmd_file in self.commands_dir.rglob('*.md'):
            name = cmd_file.stem
            self.commands[name] = {
                'file': str(cmd_file.relative_to(self.commands_dir)),
                'category': cmd_file.parent.name if cmd_file.parent != self.commands_dir else 'root'
            }
        
        # Scan agents (including coordinators)
        for agent_file in self.agents_dir.glob('*.md'):
            name = agent_file.stem
            if 'coordinator' in name:
                self.coordinators[name] = {'name': name}
            else:
                self.agents[name] = {'name': name}
    
    def save_report(self, content: str) -> Path:
        """Save the visual report"""
        self.report_dir.mkdir(exist_ok=True)
        
        # Save as markdown
        report_path = self.report_dir / f"visual_architecture_{self.timestamp}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Also save as latest
        latest_path = self.report_dir / "visual_architecture_latest.md"
        with open(latest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return report_path

def main():
    """Main entry point"""
    print("="*60)
    print("NOVELSYS-SWARM Visual Report Generator")
    print("="*60)
    
    generator = VisualReportGenerator()
    
    print("Generating visual architecture report...")
    report_content = generator.generate_visual_report()
    
    print("Saving report...")
    report_path = generator.save_report(report_content)
    
    print(f"\n[SUCCESS] Visual report generated successfully!")
    print(f"[REPORT] Report saved to: {report_path}")
    print(f"[REPORT] Also available at: report/visual_architecture_latest.md")
    
    print("\n" + "="*60)
    print("Report includes:")
    print("  - ASCII art architecture diagrams")
    print("  - Statistical charts and graphs")
    print("  - Dependency matrices")
    print("  - Flow diagrams for commands")
    print("  - Mermaid diagram code")
    print("  - Call depth analysis")
    print("  - Recursion safety verification")
    print("="*60)

if __name__ == '__main__':
    main()