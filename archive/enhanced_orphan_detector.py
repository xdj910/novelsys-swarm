#!/usr/bin/env python3
"""
Enhanced Orphan Component Detector v2.0
Eliminates false positives by comprehensive usage pattern recognition.

Based on manual verification findings:
- cozy-mystery-specialist: used via use_specialists array
- emotion-specialist: used via JSON execution plans
- emotion-weaver-specialist: referenced by book-pacing-analyzer
- book-pacing-analyzer: used by smart-fix-cross-coordinator

Usage patterns to detect:
1. JSON execution plans: "agent": "component-name"
2. Specialist arrays: use_specialists: ["component-name"]
3. Natural language: "use the component-name subagent"
4. Indirect references through other components
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class EnhancedOrphanDetector:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)

        # Component inventories
        self.commands: Dict[str, Path] = {}
        self.coordinators: Dict[str, Path] = {}
        self.agents: Dict[str, Path] = {}

        # Usage tracking
        self.coordinator_usage: Dict[str, Set[str]] = {}  # coordinator -> set of commands using it
        self.agent_usage: Dict[str, Set[str]] = {}        # agent -> set of coordinators using it

        # Pattern compilation for performance
        self.usage_patterns = {
            'json_agent': re.compile(r'"agent":\s*"([^"]+)"'),
            'use_specialists': re.compile(r'use_specialists:\s*\[([^\]]+)\]'),
            'specialist_item': re.compile(r'"([^"]+)"'),
            'subagent_call': re.compile(r'use\s+the\s+([a-z-]+(?:-coordinator|-specialist)?)\s+subagent', re.IGNORECASE),
            'coordinator_call': re.compile(r'([a-z-]+-coordinator)\s+(?:subagent|coordinator)', re.IGNORECASE),
            'specialist_call': re.compile(r'([a-z-]+-specialist)\s+(?:subagent|specialist)', re.IGNORECASE),
        }

    def scan_components(self):
        """Scan and inventory all system components"""
        print("Scanning system components...")

        # Scan commands
        commands_path = self.base_path / ".claude" / "commands"
        if commands_path.exists():
            for file in commands_path.glob("*.md"):
                name = file.stem
                self.commands[name] = file

        # Scan agents folder for coordinators and agents
        agents_path = self.base_path / ".claude" / "agents"
        if agents_path.exists():
            for file in agents_path.glob("*.md"):
                name = file.stem
                if name.endswith('-coordinator'):
                    self.coordinators[name] = file
                else:
                    self.agents[name] = file

        print(f"Found {len(self.commands)} commands, {len(self.coordinators)} coordinators, {len(self.agents)} agents")

    def extract_usage_from_content(self, content: str, source_type: str) -> Set[str]:
        """Extract all component usage from file content using comprehensive patterns"""
        usage = set()

        # Pattern 1: JSON execution plans - "agent": "component-name"
        for match in self.usage_patterns['json_agent'].finditer(content):
            agent_name = match.group(1)
            usage.add(agent_name)

        # Pattern 2: Specialist arrays - use_specialists: ["name1", "name2"]
        for match in self.usage_patterns['use_specialists'].finditer(content):
            specialists_content = match.group(1)
            for specialist_match in self.usage_patterns['specialist_item'].finditer(specialists_content):
                specialist_name = specialist_match.group(1)
                usage.add(specialist_name)

        # Pattern 3: Natural language subagent calls
        for match in self.usage_patterns['subagent_call'].finditer(content):
            component_name = match.group(1)
            usage.add(component_name)

        # Pattern 4: Explicit coordinator calls
        for match in self.usage_patterns['coordinator_call'].finditer(content):
            coordinator_name = match.group(1)
            usage.add(coordinator_name)

        # Pattern 5: Explicit specialist calls
        for match in self.usage_patterns['specialist_call'].finditer(content):
            specialist_name = match.group(1)
            usage.add(specialist_name)

        # Pattern 6: Direct name references (fallback pattern)
        # Look for component names in various contexts
        all_component_names = set(self.coordinators.keys()) | set(self.agents.keys())
        for component_name in all_component_names:
            # Escape hyphens for regex
            escaped_name = re.escape(component_name)
            # Look for the component name as a word boundary
            pattern = rf'\b{escaped_name}\b'
            if re.search(pattern, content, re.IGNORECASE):
                # Additional context check to avoid false positives from descriptions
                context_pattern = rf'(?:use|call|invoke|execute|run|agent|specialist|coordinator).*?\b{escaped_name}\b'
                if re.search(context_pattern, content, re.IGNORECASE | re.DOTALL):
                    usage.add(component_name)

        return usage

    def analyze_usage_patterns(self):
        """Analyze usage patterns across all components"""
        print("Analyzing usage patterns...")

        # Initialize usage tracking
        for coord in self.coordinators:
            self.coordinator_usage[coord] = set()
        for agent in self.agents:
            self.agent_usage[agent] = set()

        # Analyze command -> coordinator usage
        for command_name, command_path in self.commands.items():
            try:
                content = command_path.read_text(encoding='utf-8')
                used_components = self.extract_usage_from_content(content, 'command')

                for component in used_components:
                    if component in self.coordinators:
                        self.coordinator_usage[component].add(command_name)

            except Exception as e:
                print(f"Error reading command {command_name}: {e}")

        # Analyze coordinator -> agent usage
        for coordinator_name, coordinator_path in self.coordinators.items():
            try:
                content = coordinator_path.read_text(encoding='utf-8')
                used_components = self.extract_usage_from_content(content, 'coordinator')

                for component in used_components:
                    if component in self.agents:
                        self.agent_usage[component].add(coordinator_name)

            except Exception as e:
                print(f"Error reading coordinator {coordinator_name}: {e}")

        # Cross-reference: agents can also be used by other agents
        for agent_name, agent_path in self.agents.items():
            try:
                content = agent_path.read_text(encoding='utf-8')
                used_components = self.extract_usage_from_content(content, 'agent')

                for component in used_components:
                    if component in self.agents and component != agent_name:
                        self.agent_usage[component].add(agent_name)

            except Exception as e:
                print(f"Error reading agent {agent_name}: {e}")

    def find_orphan_components(self) -> Tuple[List[str], List[str]]:
        """Find orphan coordinators and agents"""
        orphan_coordinators = []
        orphan_agents = []

        # Find orphan coordinators (not called by any command)
        for coordinator in self.coordinators:
            if len(self.coordinator_usage[coordinator]) == 0:
                orphan_coordinators.append(coordinator)

        # Find orphan agents (not called by any coordinator or agent)
        for agent in self.agents:
            if len(self.agent_usage[agent]) == 0:
                orphan_agents.append(agent)

        return orphan_coordinators, orphan_agents

    def generate_detailed_report(self, orphan_coordinators: List[str], orphan_agents: List[str]):
        """Generate detailed analysis report"""
        total_coordinators = len(self.coordinators)
        total_agents = len(self.agents)
        total_orphans = len(orphan_coordinators) + len(orphan_agents)
        total_components = total_coordinators + total_agents

        orphan_rate = (total_orphans / total_components * 100) if total_components > 0 else 0

        report = f"""
ENHANCED ORPHAN COMPONENT ANALYSIS REPORT v2.0
Generated: {Path.cwd()}
Timestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== SYSTEM OVERVIEW ===
Total Commands: {len(self.commands)}
Total Coordinators: {total_coordinators}
Total Agents: {total_agents}
Total Components: {total_components}

=== ORPHAN ANALYSIS ===
Orphan Coordinators: {len(orphan_coordinators)}
Orphan Agents: {len(orphan_agents)}
Total Orphans: {total_orphans}
Orphan Rate: {orphan_rate:.1f}%

=== EXECUTION CHAIN ANALYSIS ===
Architecture: User -> Command -> Coordinator -> Agent

Coordinator Usage (called by commands):
"""

        # Show coordinator usage details
        used_coordinators = 0
        for coordinator in sorted(self.coordinators.keys()):
            callers = self.coordinator_usage[coordinator]
            if callers:
                used_coordinators += 1
                report += f"  {coordinator}: called by {len(callers)} commands {sorted(callers)}\n"

        report += f"\nUsed Coordinators: {used_coordinators}/{total_coordinators}\n\n"

        # Show agent usage details
        used_agents = 0
        for agent in sorted(self.agents.keys()):
            callers = self.agent_usage[agent]
            if callers:
                used_agents += 1
                caller_list = sorted(callers)
                report += f"  {agent}: called by {len(callers)} components {caller_list}\n"

        report += f"\nUsed Agents: {used_agents}/{total_agents}\n\n"

        # List orphan components
        if orphan_coordinators:
            report += "=== ORPHAN COORDINATORS ===\n"
            for coord in sorted(orphan_coordinators):
                report += f"  - {coord} (no command calls this coordinator)\n"
            report += "\n"

        if orphan_agents:
            report += "=== ORPHAN AGENTS ===\n"
            for agent in sorted(orphan_agents):
                report += f"  - {agent} (no coordinator or agent calls this agent)\n"
            report += "\n"

        # Usage pattern detection summary
        report += "=== DETECTION PATTERNS USED ===\n"
        report += "1. JSON execution plans: \"agent\": \"component-name\"\n"
        report += "2. Specialist arrays: use_specialists: [\"component-name\"]\n"
        report += "3. Natural language: \"use the component-name subagent\"\n"
        report += "4. Explicit calls: coordinator/specialist mentions\n"
        report += "5. Direct references: component names in context\n"
        report += "6. Cross-references: agents calling other agents\n\n"

        if total_orphans == 0:
            report += "=== CONCLUSION ===\n"
            report += "EXCELLENT: No orphan components detected!\n"
            report += "All components are properly integrated into the execution chain.\n"
        else:
            report += "=== RECOMMENDATIONS ===\n"
            report += f"Review {total_orphans} orphan components for:\n"
            report += "- Unused legacy components (can be archived)\n"
            report += "- Missing integration (should be connected)\n"
            report += "- False positives (manual verification needed)\n"

        return report

    def run_analysis(self) -> str:
        """Run complete orphan analysis"""
        self.scan_components()
        self.analyze_usage_patterns()
        orphan_coordinators, orphan_agents = self.find_orphan_components()
        return self.generate_detailed_report(orphan_coordinators, orphan_agents)

def main():
    print("Enhanced Orphan Component Detector v2.0")
    print("Comprehensive usage pattern recognition to eliminate false positives")

    detector = EnhancedOrphanDetector()
    report = detector.run_analysis()

    # Save report
    timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f".claude/testing/enhanced_orphan_analysis_{timestamp}.md"

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {report_path}")
    print("\nSummary:")

    # Extract key metrics for summary
    lines = report.split('\n')
    for line in lines:
        if 'Total Orphans:' in line or 'Orphan Rate:' in line:
            print(f"  {line.strip()}")

    return report_path

if __name__ == "__main__":
    main()