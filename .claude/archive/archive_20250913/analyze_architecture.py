#!/usr/bin/env python3
"""
Analyze NOVELSYS-SWARM three-layer architecture
Automatically scans all commands, coordinators, and agents
Generates timestamped architecture report
"""

import os
import shutil
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple

class ArchitectureAnalyzer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.commands_dir = base_dir / "commands"
        self.agents_dir = base_dir / "agents"
        self.report_dir = base_dir.parent / "report"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Storage for analysis results
        self.commands: Dict[str, Dict] = {}
        self.coordinators: Set[str] = set()
        self.agents: Set[str] = set()
        self.unmapped_agents: Set[str] = set()
        
    def scan_all_commands(self) -> None:
        """Scan all command files recursively"""
        print("Scanning for commands...")
        
        # Scan root level commands
        for file in self.commands_dir.glob("*.md"):
            if file.is_file():
                self.analyze_command(file, "root")
        
        # Scan subdirectories (like novel/)
        for subdir in self.commands_dir.iterdir():
            if subdir.is_dir():
                for file in subdir.glob("*.md"):
                    if file.is_file():
                        self.analyze_command(file, subdir.name)
    
    def analyze_command(self, command_file: Path, category: str) -> None:
        """Analyze a single command file to extract coordinator and agents"""
        command_name = command_file.stem
        print(f"  Analyzing command: {command_name} ({category})")
        
        content = command_file.read_text(encoding='utf-8')
        
        # Initialize command entry
        self.commands[command_name] = {
            "file": str(command_file.relative_to(self.base_dir)),
            "category": category,
            "coordinator": None,
            "agents": [],
            "directly_called_agents": []
        }
        
        # Pattern to find coordinator references
        coordinator_patterns = [
            r'Use the ([a-z-]+)-coordinator subagent',
            r'([a-z-]+)-coordinator',
            r'coordinator:\s*([a-z-]+)-coordinator'
        ]
        
        for pattern in coordinator_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                coordinator_name = f"{matches[0]}-coordinator"
                self.commands[command_name]["coordinator"] = coordinator_name
                self.coordinators.add(coordinator_name)
                break
        
        # Pattern to find directly called agents (without coordinator)
        agent_patterns = [
            r'Use the ([a-z-]+) subagent',
            r'Use the ([a-z-]+) agent',
            r'agent:\s*([a-z-]+)'
        ]
        
        for pattern in agent_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if not match.endswith('-coordinator'):
                    self.commands[command_name]["directly_called_agents"].append(match)
                    self.agents.add(match)
    
    def scan_all_coordinators(self) -> None:
        """Scan coordinator files to find their agent dependencies"""
        print("\nScanning coordinators for agent dependencies...")
        
        for command_name, command_info in self.commands.items():
            if command_info["coordinator"]:
                coordinator_file = self.agents_dir / f"{command_info['coordinator']}.md"
                if coordinator_file.exists():
                    self.analyze_coordinator(coordinator_file, command_name)
                else:
                    print(f"  Warning: Coordinator file not found: {command_info['coordinator']}.md")
    
    def analyze_coordinator(self, coordinator_file: Path, command_name: str) -> None:
        """Analyze a coordinator file to extract agent calls"""
        print(f"  Analyzing coordinator: {coordinator_file.stem}")
        
        content = coordinator_file.read_text(encoding='utf-8')
        
        # More precise patterns to find agent invocations in coordinators
        agent_patterns = [
            r'Use the ([a-z][a-z0-9-]+) subagent',  # Must start with letter
            r'Use the ([a-z][a-z0-9-]+) agent',
            r'([a-z][a-z0-9-]+-specialist) subagent',  # Full specialist name
            r'agent:\s*([a-z][a-z0-9-]+)',
            r'"([a-z][a-z0-9-]+-specialist)"',  # Quoted specialist names
            r'`([a-z][a-z0-9-]+-specialist)`'   # Backticked specialist names
        ]
        
        found_agents = set()
        for pattern in agent_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up agent name
                agent_name = match.lower().replace(' ', '-')
                # Validate agent name (must be reasonable length and format)
                if (not agent_name.endswith('-coordinator') and 
                    not agent_name.startswith('the-') and
                    len(agent_name) > 3 and  # Minimum reasonable length
                    len(agent_name) < 50 and  # Maximum reasonable length
                    not any(word in agent_name for word in ['any', 'each', 'appropriate', 'between', 'corresponding', 'calling'])):
                    found_agents.add(agent_name)
                    self.agents.add(agent_name)
        
        self.commands[command_name]["agents"] = sorted(list(found_agents))
    
    def scan_all_agents(self) -> None:
        """Scan agents directory to find all available agents"""
        print("\nScanning all available agents...")
        
        all_agent_files = set()
        for file in self.agents_dir.glob("*.md"):
            if file.is_file() and not file.name.endswith('.bak'):
                agent_name = file.stem
                all_agent_files.add(agent_name)
        
        # Find unmapped agents (not used by any command)
        used_agents = set()
        for cmd_info in self.commands.values():
            if cmd_info["coordinator"]:
                used_agents.add(cmd_info["coordinator"])
            used_agents.update(cmd_info["agents"])
            used_agents.update(cmd_info["directly_called_agents"])
        
        self.unmapped_agents = all_agent_files - used_agents
        print(f"  Found {len(all_agent_files)} total agents")
        print(f"  {len(self.unmapped_agents)} agents not mapped to any command")
    
    def create_organized_folders(self, output_dir: Path) -> None:
        """Create organized folder structure for each command"""
        print(f"\nCreating organized folders in {output_dir}...")
        
        for command_name, command_info in self.commands.items():
            command_folder = output_dir / command_name
            command_folder.mkdir(exist_ok=True)
            
            copied_files = []
            
            # Copy command file
            if command_info["category"] == "root":
                src = self.commands_dir / f"{command_name}.md"
            else:
                src = self.commands_dir / command_info["category"] / f"{command_name}.md"
            
            if src.exists():
                dest = command_folder / f"{command_name}.md"
                shutil.copy2(src, dest)
                copied_files.append(f"{command_name}.md")
            
            # Copy coordinator if exists
            if command_info["coordinator"]:
                src = self.agents_dir / f"{command_info['coordinator']}.md"
                if src.exists():
                    dest = command_folder / f"{command_info['coordinator']}.md"
                    shutil.copy2(src, dest)
                    copied_files.append(f"{command_info['coordinator']}.md")
            
            # Copy all associated agents
            all_agents = command_info["agents"] + command_info["directly_called_agents"]
            for agent_name in all_agents:
                src = self.agents_dir / f"{agent_name}.md"
                if src.exists():
                    dest = command_folder / f"{agent_name}.md"
                    shutil.copy2(src, dest)
                    copied_files.append(f"{agent_name}.md")
            
            # Create structure file for this command
            self.create_command_structure_file(command_folder, command_name, command_info, copied_files)
            
            print(f"  Created {command_name}/ with {len(copied_files)} files")
    
    def create_command_structure_file(self, folder: Path, command_name: str, info: Dict, files: List[str]) -> None:
        """Create STRUCTURE.md for a single command folder"""
        
        content = f"# {command_name} - Three Layer Architecture\n\n"
        content += f"## Command Layer\n"
        content += f"- **File**: {command_name}.md\n"
        content += f"- **Category**: {info['category']}\n"
        content += f"- **Type**: {'Coordinator-based' if info['coordinator'] else 'Direct execution'}\n\n"
        
        if info["coordinator"]:
            content += f"## Coordinator Layer\n"
            content += f"- **File**: {info['coordinator']}.md\n"
            content += f"- **Role**: Orchestrates execution flow\n"
            content += f"- **Managed Agents**: {len(info['agents'])}\n\n"
        
        all_agents = info["agents"] + info["directly_called_agents"]
        if all_agents:
            content += f"## Agent Layer ({len(all_agents)} agents)\n"
            for agent in sorted(all_agents):
                if agent + ".md" in files:
                    content += f"- {agent} ✓\n"
                else:
                    content += f"- {agent} ⚠️ (file not found)\n"
        else:
            content += f"## Agent Layer\n"
            content += f"- No specialized agents (direct execution)\n"
        
        content += f"\n## Execution Flow\n"
        if info["coordinator"]:
            content += f"1. User invokes: `/{info['category']}:{command_name}` (or `/:{command_name}` if root)\n"
            content += f"2. Command delegates to: `{info['coordinator']}`\n"
            content += f"3. Coordinator orchestrates: {len(info['agents'])} specialized agents\n"
        else:
            content += f"1. User invokes: `/{info['category']}:{command_name}` (or `/:{command_name}` if root)\n"
            content += f"2. Command executes directly"
            if info["directly_called_agents"]:
                content += f" using {len(info['directly_called_agents'])} agents\n"
            else:
                content += "\n"
        
        content += f"\n## Files in this folder\n"
        for file in sorted(files):
            content += f"- {file}\n"
        
        structure_file = folder / "STRUCTURE.md"
        structure_file.write_text(content, encoding='utf-8')
    
    def generate_report(self) -> str:
        """Generate comprehensive architecture report"""
        
        report = f"# NOVELSYS-SWARM Architecture Analysis Report\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Executive Summary
        report += f"## Executive Summary\n"
        report += f"- **Total Commands**: {len(self.commands)}\n"
        report += f"- **Total Coordinators**: {len(self.coordinators)}\n"
        report += f"- **Total Agents**: {len(self.agents)}\n"
        report += f"- **Unmapped Agents**: {len(self.unmapped_agents)}\n\n"
        
        # Commands by Category
        report += f"## Commands by Category\n"
        categories = {}
        for cmd_name, cmd_info in self.commands.items():
            cat = cmd_info["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(cmd_name)
        
        for cat in sorted(categories.keys()):
            report += f"\n### {cat} ({len(categories[cat])} commands)\n"
            for cmd in sorted(categories[cat]):
                coordinator = self.commands[cmd]["coordinator"]
                agent_count = len(self.commands[cmd]["agents"] + self.commands[cmd]["directly_called_agents"])
                if coordinator:
                    report += f"- **{cmd}** → {coordinator} → {agent_count} agents\n"
                else:
                    report += f"- **{cmd}** → {agent_count} agents (direct)\n"
        
        # Three-Layer Architecture Details
        report += f"\n## Three-Layer Architecture Mapping\n"
        
        for cmd_name in sorted(self.commands.keys()):
            cmd_info = self.commands[cmd_name]
            report += f"\n### {cmd_name}\n"
            report += f"- **Category**: {cmd_info['category']}\n"
            report += f"- **Command**: {cmd_info['file']}\n"
            
            if cmd_info["coordinator"]:
                report += f"- **Coordinator**: {cmd_info['coordinator']}.md\n"
                report += f"- **Agents via Coordinator** ({len(cmd_info['agents'])}):\n"
                for agent in sorted(cmd_info['agents']):
                    report += f"  - {agent}\n"
            
            if cmd_info["directly_called_agents"]:
                report += f"- **Directly Called Agents** ({len(cmd_info['directly_called_agents'])}):\n"
                for agent in sorted(cmd_info["directly_called_agents"]):
                    report += f"  - {agent}\n"
            
            if not cmd_info["coordinator"] and not cmd_info["directly_called_agents"]:
                report += f"- **Execution**: Direct (no agents)\n"
        
        # Unmapped Agents
        if self.unmapped_agents:
            report += f"\n## Unmapped Agents ({len(self.unmapped_agents)})\n"
            report += "These agents exist but are not referenced by any command:\n"
            for agent in sorted(self.unmapped_agents):
                report += f"- {agent}\n"
        
        # Statistics
        report += f"\n## Architecture Statistics\n"
        
        # Commands with/without coordinators
        with_coordinator = sum(1 for c in self.commands.values() if c["coordinator"])
        without_coordinator = len(self.commands) - with_coordinator
        report += f"\n### Command Distribution\n"
        report += f"- Commands with coordinators: {with_coordinator} ({with_coordinator*100//len(self.commands)}%)\n"
        report += f"- Commands without coordinators: {without_coordinator} ({without_coordinator*100//len(self.commands)}%)\n"
        
        # Agent usage statistics
        agent_usage = {}
        for cmd_info in self.commands.values():
            for agent in cmd_info["agents"] + cmd_info["directly_called_agents"]:
                agent_usage[agent] = agent_usage.get(agent, 0) + 1
        
        report += f"\n### Most Used Agents\n"
        sorted_agents = sorted(agent_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        for agent, count in sorted_agents:
            report += f"- {agent}: used by {count} commands\n"
        
        # Complexity Analysis
        report += f"\n### Complexity Analysis\n"
        complexity_stats = []
        for cmd_name, cmd_info in self.commands.items():
            total_agents = len(cmd_info["agents"] + cmd_info["directly_called_agents"])
            complexity_stats.append((cmd_name, total_agents))
        
        complexity_stats.sort(key=lambda x: x[1], reverse=True)
        
        report += f"\n#### Most Complex Commands (by agent count)\n"
        for cmd, count in complexity_stats[:5]:
            report += f"- {cmd}: {count} agents\n"
        
        report += f"\n#### Simplest Commands\n"
        for cmd, count in complexity_stats[-5:]:
            report += f"- {cmd}: {count} agents\n"
        
        return report
    
    def save_report(self, report: str) -> Path:
        """Save report to timestamped file"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = self.report_dir / f"architecture_analysis_{self.timestamp}.md"
        report_file.write_text(report, encoding='utf-8')
        
        # Also save as latest for easy access
        latest_file = self.report_dir / "architecture_analysis_latest.md"
        latest_file.write_text(report, encoding='utf-8')
        
        return report_file
    
    def save_json_data(self) -> Path:
        """Save raw analysis data as JSON"""
        data = {
            "timestamp": self.timestamp,
            "commands": self.commands,
            "coordinators": sorted(list(self.coordinators)),
            "agents": sorted(list(self.agents)),
            "unmapped_agents": sorted(list(self.unmapped_agents))
        }
        
        json_file = self.report_dir / f"architecture_data_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return json_file
    
    def run_analysis(self, create_folders: bool = True) -> Tuple[Path, Path]:
        """Run complete analysis"""
        print("="*60)
        print("NOVELSYS-SWARM Architecture Analyzer")
        print("="*60)
        
        # Scan everything
        self.scan_all_commands()
        self.scan_all_coordinators()
        self.scan_all_agents()
        
        # Generate report
        report = self.generate_report()
        report_file = self.save_report(report)
        json_file = self.save_json_data()
        
        print(f"\n[OK] Analysis complete!")
        print(f"Report saved to: {report_file}")
        print(f"JSON data saved to: {json_file}")
        
        # Optionally create organized folders
        if create_folders:
            output_dir = self.base_dir / f"organized_{self.timestamp}"
            self.create_organized_folders(output_dir)
            print(f"Organized folders created in: {output_dir}")
        
        return report_file, json_file


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze NOVELSYS-SWARM architecture")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(r"D:\NOVELSYS-SWARM\.claude\ForReview"),
        help="Base directory containing commands and agents folders"
    )
    parser.add_argument(
        "--no-folders",
        action="store_true",
        help="Skip creating organized folders"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Override output directory for organized folders"
    )
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = ArchitectureAnalyzer(args.base_dir)
    
    # Override output directory if specified
    if args.output_dir:
        analyzer.report_dir = args.output_dir
    
    report_file, json_file = analyzer.run_analysis(create_folders=not args.no_folders)
    
    # Display summary
    print("\n" + "="*60)
    print("ANALYSIS SUMMARY")
    print("="*60)
    print(f"Commands analyzed: {len(analyzer.commands)}")
    print(f"Coordinators found: {len(analyzer.coordinators)}")
    print(f"Agents mapped: {len(analyzer.agents)}")
    print(f"Unmapped agents: {len(analyzer.unmapped_agents)}")
    
    # Show unmapped agents if any
    if analyzer.unmapped_agents:
        print("\nUnmapped agents (not used by any command):")
        for agent in sorted(analyzer.unmapped_agents)[:10]:
            print(f"  - {agent}")
        if len(analyzer.unmapped_agents) > 10:
            print(f"  ... and {len(analyzer.unmapped_agents) - 10} more")


if __name__ == "__main__":
    main()