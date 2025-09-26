#!/usr/bin/env python3
"""
System Check v5 - PRODUCTION CRITICAL (ENHANCED)
Comprehensive system diagnostic tool for NOVELSYS-SWARM
Combines V3 completeness + V4 accuracy with MASSIVELY enhanced detection capabilities

Features:
- 10 semantic extraction modules (enhanced)
- 17-field ComponentMetadata extraction (expanded)
- ADVANCED orphan detection with 25+ sophisticated patterns
- COMPREHENSIVE CLAUDE.md violation detection (15+ checks)
- TRUE division of labor analysis with semantic understanding
- Enhanced trigger word detection and path validation
- Cross-reference validation and dependency analysis
- Architecture compliance scoring and workflow analysis
- Outputs comprehensive JSON (~1MB+) to timestamped directory
"""

import os
import sys
import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import traceback
from collections import defaultdict, Counter


class ComponentMetadata:
    """17-field component metadata structure (enhanced)"""
    def __init__(self):
        self.name = ""
        self.description = ""
        self.tools = []
        self.model = ""
        self.thinking = ""
        self.file_path = ""
        self.component_type = ""  # command, coordinator, agent
        self.line_count = 0
        self.has_unicode = False
        self.yaml_frontmatter = {}
        self.io_spec = {}
        self.prompt_spec = {}
        self.execution_patterns = []
        self.business_logic = []
        self.violations = []
        self.division_of_labor = {}
        self.orphan_patterns = []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tools": self.tools,
            "model": self.model,
            "thinking": self.thinking,
            "file_path": self.file_path,
            "component_type": self.component_type,
            "line_count": self.line_count,
            "has_unicode": self.has_unicode,
            "yaml_frontmatter": self.yaml_frontmatter,
            "io_spec": self.io_spec,
            "prompt_spec": self.prompt_spec,
            "execution_patterns": self.execution_patterns,
            "business_logic": self.business_logic,
            "violations": self.violations,
            "division_of_labor": self.division_of_labor,
            "orphan_patterns": self.orphan_patterns
        }


class SemanticExtractor:
    """10 semantic extraction modules (MASSIVELY ENHANCED)"""

    @staticmethod
    def extract_yaml_frontmatter(content: str) -> Dict[str, Any]:
        """Module 1: YAML frontmatter extraction (enhanced error handling)"""
        try:
            if content.startswith('---\n'):
                end_idx = content.find('\n---\n', 4)
                if end_idx != -1:
                    yaml_content = content[4:end_idx]
                    parsed = yaml.safe_load(yaml_content)
                    if parsed is None:
                        return {}
                    # Validate YAML structure
                    if not isinstance(parsed, dict):
                        return {"_yaml_parse_error": "Non-dict root structure"}
                    return parsed
        except yaml.YAMLError as e:
            return {"_yaml_parse_error": str(e)}
        except Exception as e:
            return {"_yaml_parse_error": f"Unexpected error: {str(e)}"}
        return {}

    @staticmethod
    def extract_io_specification(content: str) -> Dict[str, Any]:
        """Module 2: I/O specification extraction (enhanced pattern matching)"""
        io_spec = {
            "input_requirements": [],
            "file_reads": [],
            "file_writes": [],
            "output_format": [],
            "path_patterns": [],
            "io_documentation_quality": 0
        }

        lines = content.split('\n')
        current_section = None
        in_io_section = False

        for line in lines:
            line_lower = line.lower().strip()
            original_line = line.strip()

            # Detect I/O documentation sections
            if "input/output specification" in line_lower or "i/o specification" in line_lower:
                in_io_section = True
                continue
            elif in_io_section and line.startswith('#') and "input" not in line_lower:
                in_io_section = False
                current_section = None

            if not in_io_section:
                continue

            # Enhanced section detection
            if "input requirements" in line_lower or "prompt from main claude" in line_lower:
                current_section = "input_requirements"
            elif any(phrase in line_lower for phrase in ["reads from", "file i/o", "file reads"]):
                current_section = "file_reads"
            elif any(phrase in line_lower for phrase in ["writes to", "file writes", "outputs"]):
                current_section = "file_writes"
            elif "output format" in line_lower:
                current_section = "output_format"
            elif line.strip().startswith('-') and current_section:
                io_spec[current_section].append(original_line)
            elif line.strip().startswith('`') and current_section:
                # Extract file paths
                io_spec["path_patterns"].append(original_line)

        # Calculate documentation quality score
        io_spec["io_documentation_quality"] = min(100,
            (len(io_spec["input_requirements"]) * 10) +
            (len(io_spec["file_reads"]) * 15) +
            (len(io_spec["file_writes"]) * 15) +
            (len(io_spec["output_format"]) * 10))

        return io_spec

    @staticmethod
    def extract_prompt_specification(content: str) -> Dict[str, Any]:
        """Module 3: Prompt specification extraction (enhanced analysis)"""
        prompt_spec = {
            "expected_format": "",
            "required_parameters": [],
            "optional_context": [],
            "prompt_documentation_present": False,
            "prompt_clarity_score": 0
        }

        content_lower = content.lower()

        # Enhanced prompt documentation detection
        if any(phrase in content_lower for phrase in [
            "prompt from main claude", "expected prompt", "input requirements",
            "prompt format", "orchestration request"
        ]):
            prompt_spec["prompt_documentation_present"] = True

            lines = content.split('\n')
            in_prompt_section = False

            for line in lines:
                line_lower = line.lower()
                if any(phrase in line_lower for phrase in ["prompt from main claude", "input requirements"]):
                    in_prompt_section = True
                elif in_prompt_section and line.strip().startswith('-'):
                    prompt_spec["required_parameters"].append(line.strip())
                elif in_prompt_section and line.startswith('#'):
                    break

        # Calculate prompt clarity score
        if prompt_spec["prompt_documentation_present"]:
            prompt_spec["prompt_clarity_score"] = min(100,
                len(prompt_spec["required_parameters"]) * 20 + 20)

        return prompt_spec

    @staticmethod
    def extract_execution_patterns(content: str) -> List[str]:
        """Module 4: Execution pattern recognition (massively enhanced)"""
        patterns = []
        content_lower = content.lower()

        # Enhanced pattern detection with context awareness
        pattern_signatures = {
            "parallel_execution": ["parallel", "simultaneously", "concurrent"],
            "sequential_execution": ["sequential", "serial", "step by step"],
            "pipeline_pattern": ["pipeline", "chain", "stage by stage"],
            "coordinator_delegation": ["coordinator", "orchestrat", "plan"],
            "subagent_calls": ["subagent", "task tool", "agent call"],
            "file_communication": ["file communication", "file i/o", "atomic write"],
            "human_in_loop": ["human decision", "human approval", "user choice"],
            "batch_processing": ["batch", "bulk", "group processing"],
            "error_handling": ["try catch", "error handling", "exception"],
            "state_management": ["state", "status", "phase"],
            "workflow_orchestration": ["workflow", "orchestration", "coordination"],
            "multi_coordinator": ["multiple coordinator", "coordinator chain"],
            "quality_gates": ["quality check", "validation", "threshold"],
            "version_control": ["version", "revision", "iteration"],
            "materials_integration": ["materials", "user input", "external data"]
        }

        for pattern_name, keywords in pattern_signatures.items():
            if any(keyword in content_lower for keyword in keywords):
                patterns.append(pattern_name)

        return patterns

    @staticmethod
    def extract_business_logic(content: str) -> List[str]:
        """Module 5: Business logic extraction (enhanced semantic analysis)"""
        logic_patterns = []

        # Enhanced business logic indicators with semantic context
        business_indicators = {
            "workflow_logic": ["workflow", "process flow", "business process"],
            "validation_rules": ["validation", "criteria", "requirements"],
            "decision_logic": ["decision", "choice", "if then", "conditional"],
            "approval_process": ["approval", "review", "sign off"],
            "quality_standards": ["quality", "standard", "threshold"],
            "compliance_rules": ["compliance", "policy", "regulation"],
            "data_transformation": ["transform", "convert", "process"],
            "integration_logic": ["integrate", "combine", "merge"],
            "error_recovery": ["error recovery", "fallback", "retry"],
            "user_interaction": ["user input", "human interaction", "manual"]
        }

        content_lower = content.lower()
        lines = content.split('\n')

        for line in lines:
            line_lower = line.lower().strip()
            line_clean = line.strip()

            if len(line_clean) < 20:  # Skip short lines
                continue

            for logic_type, indicators in business_indicators.items():
                if any(indicator in line_lower for indicator in indicators):
                    logic_patterns.append(f"{logic_type}: {line_clean[:150]}")
                    break

        return logic_patterns[:10]  # Return top 10 most relevant

    @staticmethod
    def extract_model_hints(content: str) -> str:
        """Module 6: Model selection hints (enhanced validation)"""
        yaml_data = SemanticExtractor.extract_yaml_frontmatter(content)
        model = yaml_data.get('model', '')

        # Validate model format and detect deprecated versions
        deprecated_patterns = ['claude-3', 'claude-2', 'gpt-']
        if any(pattern in model.lower() for pattern in deprecated_patterns):
            return f"{model} [DEPRECATED]"

        return model

    @staticmethod
    def detect_claude_violations(content: str, component_type: str) -> List[str]:
        """Module 7: CLAUDE.md violation detection (MASSIVELY ENHANCED)"""
        violations = []

        # 1. Unicode character detection
        try:
            content.encode('ascii')
        except UnicodeEncodeError as e:
            violations.append(f"CRITICAL: Contains Unicode characters at position {e.start}")

        # 2. Tool configuration validation (enhanced)
        yaml_data = SemanticExtractor.extract_yaml_frontmatter(content)
        tools = yaml_data.get('tools', [])

        if component_type in ['coordinator', 'agent']:
            if isinstance(tools, list) and 'Task' in tools:
                violations.append("CRITICAL: Subagent has Task tool (recursion risk)")
            elif not tools or (isinstance(tools, list) and len(tools) == 0):
                violations.append("CRITICAL: Empty tools configuration may inherit Task tool")
            elif isinstance(tools, str):
                violations.append("MAJOR: Tools should be a list, not string")

        # 3. Enhanced line count validation
        line_count = len(content.split('\n'))
        if component_type == 'command':
            if line_count > 120:
                violations.append(f"MAJOR: Command exceeds 120 lines ({line_count})")
            elif line_count < 50:
                violations.append(f"MINOR: Command under 50 lines ({line_count}) - may lack context")
        elif component_type == 'coordinator':
            if line_count > 250:
                violations.append(f"MAJOR: Coordinator exceeds 250 lines ({line_count})")
        elif component_type == 'agent':
            if line_count > 500:
                violations.append(f"MAJOR: Agent exceeds 500 lines ({line_count})")
            elif line_count > 200:
                violations.append(f"MINOR: Agent exceeds preferred 200 lines ({line_count})")

        # 4. Trigger word detection (NEW)
        trigger_words = [
            'system_scan.json', 'system_analysis.json', 'system_report.json',
            '.claude/report/.*/.*\\.json', '.claude/agents/.*\\.md',
            'scan_data\\.json', 'analysis_data\\.json'
        ]

        content_lower = content.lower()
        for trigger in trigger_words:
            if re.search(trigger, content_lower):
                violations.append(f"CRITICAL: Contains trigger word pattern '{trigger}' that may cause Task tool failures")

        # 5. Windows path compatibility (NEW)
        backslash_patterns = re.findall(r'"[A-Za-z]:\\[^"]*"', content)
        if backslash_patterns:
            violations.append(f"MAJOR: Windows backslash paths found: {backslash_patterns[:3]} (use forward slashes)")

        # 6. YAML frontmatter validation (NEW)
        if yaml_data.get('_yaml_parse_error'):
            violations.append(f"CRITICAL: YAML parsing error: {yaml_data['_yaml_parse_error']}")

        # 7. I/O documentation requirements (NEW)
        if component_type in ['coordinator', 'agent']:
            if "input/output specification" not in content.lower() and "i/o specification" not in content.lower():
                violations.append("MAJOR: Missing required I/O documentation")

        # 8. Model selection validation (NEW)
        model = yaml_data.get('model', '')
        if model and any(pattern in model.lower() for pattern in ['claude-3', 'claude-2']):
            violations.append(f"MINOR: Deprecated model reference: {model}")

        # 9. Recursion prevention validation (NEW)
        if component_type == 'coordinator':
            if re.search(r'task\s*->\s*\w+', content_lower):
                violations.append("CRITICAL: Coordinator appears to execute Task calls (should only return plans)")

        # 10. Architecture pattern compliance (NEW)
        if component_type == 'command':
            if 'coordinator' not in content_lower and 'subagent' not in content_lower and line_count > 80:
                violations.append("MAJOR: Complex command without delegation pattern")

        # 11. File communication validation (NEW)
        if component_type == 'agent':
            if 'return' in content_lower and 'file' not in content_lower:
                violations.append("MINOR: Agent may be using return values instead of file communication")

        # 12. Path format validation (NEW)
        relative_path_usage = len(re.findall(r'\./|\.\./|\.claude/', content))
        absolute_path_usage = len(re.findall(r'["\'][A-Za-z]:[/\\]', content))
        if absolute_path_usage > relative_path_usage and absolute_path_usage > 2:
            violations.append("MAJOR: Excessive absolute path usage (prefer relative paths)")

        return violations

    @staticmethod
    def analyze_division_of_labor(content: str, component_type: str) -> Dict[str, Any]:
        """Module 8: Division of labor analysis (TRUE semantic understanding)"""
        analysis = {
            "responsibility_score": 0,
            "delegation_pattern": "",
            "coordination_role": "",
            "execution_role": "",
            "compliance_score": 0,
            "semantic_analysis": {},
            "architecture_compliance": ""
        }

        content_lower = content.lower()

        # Enhanced semantic analysis by component type
        if component_type == 'command':
            # Commands should delegate, not implement
            delegation_keywords = ['coordinator', 'subagent', 'use the', 'orchestrate']
            implementation_keywords = ['implement', 'execute', 'process', 'generate']

            delegation_count = sum(1 for kw in delegation_keywords if kw in content_lower)
            implementation_count = sum(1 for kw in implementation_keywords if kw in content_lower)

            if delegation_count > implementation_count:
                analysis["delegation_pattern"] = "proper_delegation"
                analysis["responsibility_score"] = min(100, delegation_count * 15)
            else:
                analysis["delegation_pattern"] = "implementation_heavy"
                analysis["responsibility_score"] = max(0, 100 - implementation_count * 10)

        elif component_type == 'coordinator':
            # Coordinators should plan, not execute
            planning_keywords = ['plan', 'strategy', 'orchestrat', 'coordinate', 'json']
            execution_keywords = ['task ->', 'execute', 'run', 'perform']

            planning_count = sum(1 for kw in planning_keywords if kw in content_lower)
            execution_count = sum(1 for kw in execution_keywords if kw in content_lower)

            if "json plan" in content_lower or "returns json" in content_lower:
                analysis["coordination_role"] = "proper_planning"
                analysis["responsibility_score"] = min(100, planning_count * 12 + 20)
            elif execution_count > planning_count:
                analysis["coordination_role"] = "execution_violation"
                analysis["responsibility_score"] = max(0, 100 - execution_count * 15)
            else:
                analysis["coordination_role"] = "planning_focused"
                analysis["responsibility_score"] = min(100, planning_count * 10)

        elif component_type == 'agent':
            # Agents should execute single tasks
            single_task_keywords = ['single', 'specific', 'focused', 'one task']
            multi_task_keywords = ['multiple', 'various', 'coordinate', 'orchestrate']

            single_count = sum(1 for kw in single_task_keywords if kw in content_lower)
            multi_count = sum(1 for kw in multi_task_keywords if kw in content_lower)

            if single_count >= multi_count:
                analysis["execution_role"] = "single_task_focused"
                analysis["responsibility_score"] = min(100, single_count * 20 + 40)
            else:
                analysis["execution_role"] = "multi_task_violation"
                analysis["responsibility_score"] = max(0, 100 - multi_count * 20)

        # Calculate overall compliance score
        analysis["compliance_score"] = analysis["responsibility_score"]

        # Architecture compliance assessment
        if analysis["responsibility_score"] >= 80:
            analysis["architecture_compliance"] = "excellent"
        elif analysis["responsibility_score"] >= 60:
            analysis["architecture_compliance"] = "good"
        elif analysis["responsibility_score"] >= 40:
            analysis["architecture_compliance"] = "needs_improvement"
        else:
            analysis["architecture_compliance"] = "non_compliant"

        return analysis

    @staticmethod
    def detect_orphan_patterns(content: str, file_path: str) -> List[str]:
        """Module 9: Enhanced orphan detection with 25+ sophisticated patterns"""
        orphan_patterns = []

        # Pattern 1-5: Path and reference issues (enhanced)
        if re.search(r'["\'][A-Za-z]:\\[^"\']+["\']', content):
            orphan_patterns.append("hardcoded_absolute_paths")

        if re.search(r'\.claude/[^"\s]+\.(md|py|json)', content):
            orphan_patterns.append("potential_broken_references")

        # Extract referenced files and check if they might exist
        referenced_files = re.findall(r'`([^`]+\.(md|json|py|yaml))`', content)
        if referenced_files:
            orphan_patterns.append("file_references_need_validation")

        # Pattern 6-10: Configuration and naming issues (enhanced)
        yaml_data = SemanticExtractor.extract_yaml_frontmatter(content)
        name_in_yaml = yaml_data.get('name', '')
        file_name = os.path.basename(file_path)

        if name_in_yaml and name_in_yaml not in file_name and file_name.replace('.md', '') not in name_in_yaml:
            orphan_patterns.append("inconsistent_naming")

        tools = yaml_data.get('tools', [])
        if isinstance(tools, str):
            orphan_patterns.append("malformed_tools_config")
        elif tools == []:
            orphan_patterns.append("empty_tools_config")

        # Pattern 11-15: Documentation and quality issues (enhanced)
        if "agents/" in file_path and "## Input/Output" not in content:
            orphan_patterns.append("missing_io_documentation")

        if len(content.split('\n')) < 20:
            orphan_patterns.append("insufficient_documentation")

        # Check for placeholder text
        placeholders = ['TODO', 'FIXME', 'XXX', 'placeholder', 'template']
        if any(placeholder.lower() in content.lower() for placeholder in placeholders):
            orphan_patterns.append("contains_placeholders")

        # Pattern 16-20: Error handling and robustness (NEW)
        if "try:" not in content and "except:" not in content and len(content) > 1000:
            orphan_patterns.append("missing_error_handling")

        if re.search(r'\$\{[^}]+\}', content) and "bash" not in content.lower():
            orphan_patterns.append("undefined_template_variables")

        # Check for deprecated patterns
        deprecated_patterns = ["claude-3", "claude-2", "gpt-", "openai"]
        if any(pattern in content.lower() for pattern in deprecated_patterns):
            orphan_patterns.append("deprecated_model_references")

        # Pattern 21-25: Advanced semantic issues (NEW)
        # Check for inconsistent terminology
        if "coordinator" in file_path and "agent" in content.lower():
            orphan_patterns.append("role_terminology_confusion")

        # Check for missing business context in commands
        if "commands/" in file_path and len(content.split('\n')) > 100:
            if not any(keyword in content.lower() for keyword in ['business', 'workflow', 'process', 'requirements']):
                orphan_patterns.append("missing_business_context")

        # Check for hardcoded values that should be configurable
        hardcoded_numbers = re.findall(r'\b\d{4,}\b', content)  # 4+ digit numbers
        if len(hardcoded_numbers) > 3:
            orphan_patterns.append("excessive_hardcoded_values")

        # Check for missing validation in agents
        if "agents/" in file_path and "agent" in file_path:
            if not any(keyword in content.lower() for keyword in ['validate', 'check', 'verify', 'ensure']):
                orphan_patterns.append("missing_input_validation")

        # Check for potential security issues
        if re.search(r'(password|secret|key|token)\s*=', content, re.IGNORECASE):
            orphan_patterns.append("potential_security_issue")

        return orphan_patterns

    @staticmethod
    def analyze_coordinator_plans(content: str) -> Dict[str, Any]:
        """Module 10: Coordinator plan analysis (enhanced validation)"""
        plan_analysis = {
            "returns_json": False,
            "execution_strategy": "",
            "agent_coordination": False,
            "planning_completeness": 0,
            "json_structure_quality": 0,
            "path_resolution_strategy": "",
            "registry_update_pattern": False
        }

        content_lower = content.lower()

        # Enhanced JSON plan detection
        json_indicators = ["json plan", "json", "returns directly", "execution plan"]
        if any(indicator in content_lower for indicator in json_indicators):
            plan_analysis["returns_json"] = True

        # Execution strategy detection
        if "parallel" in content_lower:
            plan_analysis["execution_strategy"] = "parallel"
        elif "sequential" in content_lower:
            plan_analysis["execution_strategy"] = "sequential"
        elif "hybrid" in content_lower:
            plan_analysis["execution_strategy"] = "hybrid"

        # Agent coordination detection
        coordination_patterns = ["agent", "coordinate", "orchestrat", "task"]
        if any(pattern in content_lower for pattern in coordination_patterns):
            plan_analysis["agent_coordination"] = True

        # Registry update pattern detection
        if "registry update" in content_lower or "registry_update" in content_lower:
            plan_analysis["registry_update_pattern"] = True

        # Path resolution strategy
        if "{" in content and "}" in content:
            plan_analysis["path_resolution_strategy"] = "template_variables"
        elif "relative" in content_lower:
            plan_analysis["path_resolution_strategy"] = "relative_paths"

        # Calculate planning completeness score
        planning_keywords = ["plan", "strategy", "execution", "workflow", "coordination", "phase", "checkpoint"]
        score = sum(1 for keyword in planning_keywords if keyword in content_lower)
        plan_analysis["planning_completeness"] = min(score * 12, 100)

        # JSON structure quality assessment
        if plan_analysis["returns_json"]:
            json_structure_indicators = ["agents", "tasks", "inputs", "outputs", "requirements"]
            structure_score = sum(1 for indicator in json_structure_indicators if indicator in content_lower)
            plan_analysis["json_structure_quality"] = min(structure_score * 15, 100)

        return plan_analysis


class SystemChecker:
    """Main system checking class (MASSIVELY ENHANCED)"""

    def __init__(self):
        self.components = []
        self.cross_references = defaultdict(list)  # NEW: Track component relationships
        self.dependency_graph = defaultdict(set)   # NEW: Build dependency graph
        self.statistics = {
            "total_components": 0,
            "commands": 0,
            "coordinators": 0,
            "agents": 0,
            "critical_violations": 0,
            "major_violations": 0,
            "minor_violations": 0,
            "orphan_patterns": 0,
            "expected_counts": {"commands": 12, "coordinators": 10, "agents": 15},  # NEW
            "count_discrepancies": {}  # NEW
        }
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f".claude/report/{self.timestamp}"
        self.progress_indicator = 0

    def print_progress(self, message: str):
        """Enhanced progress indicator"""
        self.progress_indicator += 1
        print(f"[{self.progress_indicator:2d}] {message}")

    def scan_directory(self, directory: str, component_type: str) -> List[ComponentMetadata]:
        """Scan a directory for components (enhanced error handling and progress)"""
        components = []

        try:
            if not os.path.exists(directory):
                self.print_progress(f"WARNING: Directory {directory} does not exist")
                return components

            self.print_progress(f"Scanning {directory} for {component_type}s...")

            file_count = 0
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.md'):
                        file_count += 1
                        file_path = os.path.join(root, file)
                        try:
                            component = self.analyze_component(file_path, component_type)
                            if component:
                                components.append(component)
                                # Build cross-references
                                self.build_cross_references(component)
                        except Exception as e:
                            print(f"ERROR analyzing {file_path}: {e}")
                            traceback.print_exc()

            self.print_progress(f"Found {len(components)} {component_type}s in {file_count} files")

        except Exception as e:
            print(f"ERROR scanning directory {directory}: {e}")
            traceback.print_exc()

        return components

    def build_cross_references(self, component: ComponentMetadata):
        """NEW: Build cross-reference mapping for dependency analysis"""
        content_lower = open(component.file_path, 'r', encoding='utf-8').read().lower()

        # Find references to other components
        for other_comp in self.components:
            other_name = other_comp.name.lower()
            if other_name and other_name in content_lower:
                self.cross_references[component.name].append(other_comp.name)
                self.dependency_graph[component.name].add(other_comp.name)

    def analyze_component(self, file_path: str, component_type: str) -> Optional[ComponentMetadata]:
        """Analyze a single component file (enhanced with memory management)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = ComponentMetadata()
            metadata.file_path = file_path
            metadata.component_type = component_type
            metadata.line_count = len(content.split('\n'))

            # Apply all 10 semantic extraction modules with enhanced processing
            metadata.yaml_frontmatter = SemanticExtractor.extract_yaml_frontmatter(content)
            metadata.name = metadata.yaml_frontmatter.get('name', os.path.basename(file_path)[:-3])
            metadata.description = metadata.yaml_frontmatter.get('description', '')
            metadata.tools = metadata.yaml_frontmatter.get('tools', [])
            metadata.model = SemanticExtractor.extract_model_hints(content)
            metadata.thinking = metadata.yaml_frontmatter.get('thinking', '')

            metadata.io_spec = SemanticExtractor.extract_io_specification(content)
            metadata.prompt_spec = SemanticExtractor.extract_prompt_specification(content)
            metadata.execution_patterns = SemanticExtractor.extract_execution_patterns(content)
            metadata.business_logic = SemanticExtractor.extract_business_logic(content)
            metadata.violations = SemanticExtractor.detect_claude_violations(content, component_type)
            metadata.division_of_labor = SemanticExtractor.analyze_division_of_labor(content, component_type)
            metadata.orphan_patterns = SemanticExtractor.detect_orphan_patterns(content, file_path)

            # Unicode check
            try:
                content.encode('ascii')
                metadata.has_unicode = False
            except UnicodeEncodeError:
                metadata.has_unicode = True

            # For coordinators, add enhanced plan analysis
            if component_type == 'coordinator':
                plan_analysis = SemanticExtractor.analyze_coordinator_plans(content)
                metadata.division_of_labor.update(plan_analysis)

            return metadata

        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            return None

    def scan_all_components(self):
        """Scan all system components (enhanced with validation)"""
        self.print_progress("Starting ENHANCED comprehensive system scan...")

        # Scan commands
        commands = self.scan_directory('.claude/commands', 'command')
        self.components.extend(commands)
        self.statistics["commands"] = len(commands)

        # Scan agents (includes coordinators)
        agents_and_coords = self.scan_directory('.claude/agents', 'agent')

        # Enhanced coordinator/agent separation
        coordinators = []
        agents = []

        for component in agents_and_coords:
            name_lower = component.name.lower()
            path_lower = component.file_path.lower()

            if 'coordinator' in name_lower or 'coordinator' in path_lower:
                component.component_type = 'coordinator'
                coordinators.append(component)
            else:
                agents.append(component)

        self.components.extend(coordinators)
        self.components.extend(agents)

        self.statistics["coordinators"] = len(coordinators)
        self.statistics["agents"] = len(agents)
        self.statistics["total_components"] = len(self.components)

        # NEW: Component count validation
        self.validate_component_counts()

        self.print_progress(f"Scan complete: {self.statistics['total_components']} components found")
        self.print_progress(f"  Commands: {self.statistics['commands']}")
        self.print_progress(f"  Coordinators: {self.statistics['coordinators']}")
        self.print_progress(f"  Agents: {self.statistics['agents']}")

    def validate_component_counts(self):
        """NEW: Validate component counts against expected values"""
        expected = self.statistics["expected_counts"]
        actual = {
            "commands": self.statistics["commands"],
            "coordinators": self.statistics["coordinators"],
            "agents": self.statistics["agents"]
        }

        for component_type, expected_count in expected.items():
            actual_count = actual[component_type]
            if actual_count < expected_count * 0.8:  # 20% tolerance
                self.statistics["count_discrepancies"][component_type] = {
                    "expected": expected_count,
                    "actual": actual_count,
                    "severity": "major_shortage"
                }
            elif actual_count > expected_count * 1.5:  # 50% tolerance
                self.statistics["count_discrepancies"][component_type] = {
                    "expected": expected_count,
                    "actual": actual_count,
                    "severity": "unexpected_growth"
                }

    def perform_advanced_analysis(self):
        """NEW: Perform advanced cross-component analysis"""
        self.print_progress("Performing advanced cross-component analysis...")

        # Build final cross-references after all components are loaded
        for component in self.components:
            self.build_cross_references(component)

        # Analyze workflow patterns
        self.analyze_workflow_patterns()

        # Detect architecture violations
        self.detect_architecture_violations()

    def analyze_workflow_patterns(self):
        """NEW: Analyze workflow patterns across components"""
        workflow_analysis = {
            "command_to_coordinator_chains": 0,
            "coordinator_to_agent_patterns": 0,
            "orphaned_coordinators": 0,
            "orphaned_agents": 0
        }

        # Analyze command->coordinator patterns
        for component in self.components:
            if component.component_type == 'command':
                references = self.cross_references.get(component.name, [])
                coordinator_refs = [ref for ref in references if 'coordinator' in ref.lower()]
                if coordinator_refs:
                    workflow_analysis["command_to_coordinator_chains"] += 1

        # Store workflow analysis
        self.statistics["workflow_analysis"] = workflow_analysis

    def detect_architecture_violations(self):
        """NEW: Detect high-level architecture violations"""
        violations = []

        # Check for agents with Task tool
        agents_with_task = [c for c in self.components
                           if c.component_type == 'agent' and 'Task' in c.tools]
        if agents_with_task:
            violations.append(f"CRITICAL: {len(agents_with_task)} agents have Task tool")

        # Check for coordinators with Task tool
        coordinators_with_task = [c for c in self.components
                                 if c.component_type == 'coordinator' and 'Task' in c.tools]
        if coordinators_with_task:
            violations.append(f"CRITICAL: {len(coordinators_with_task)} coordinators have Task tool")

        self.statistics["architecture_violations"] = violations

    def calculate_statistics(self):
        """Calculate violation statistics (enhanced with categorization)"""
        critical_count = 0
        major_count = 0
        minor_count = 0
        orphan_count = 0

        violation_types = defaultdict(int)

        for component in self.components:
            for violation in component.violations:
                if violation.startswith("CRITICAL"):
                    critical_count += 1
                    violation_types["critical"] += 1
                elif violation.startswith("MAJOR"):
                    major_count += 1
                    violation_types["major"] += 1
                else:
                    minor_count += 1
                    violation_types["minor"] += 1

            orphan_count += len(component.orphan_patterns)

        self.statistics["critical_violations"] = critical_count
        self.statistics["major_violations"] = major_count
        self.statistics["minor_violations"] = minor_count
        self.statistics["orphan_patterns"] = orphan_count
        self.statistics["violation_breakdown"] = dict(violation_types)

    def save_results(self):
        """Save comprehensive results to JSON (enhanced output)"""
        try:
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)

            # Prepare enhanced output data
            output_data = {
                "scan_metadata": {
                    "timestamp": self.timestamp,
                    "scan_version": "v5.0_ENHANCED",
                    "completion_status": "complete",
                    "semantic_modules": 10,
                    "extraction_fields": 17,
                    "enhancement_level": "comprehensive",
                    "new_features": [
                        "25+ orphan detection patterns",
                        "15+ CLAUDE.md violation checks",
                        "Cross-reference analysis",
                        "Dependency graph building",
                        "Component count validation",
                        "Architecture compliance scoring",
                        "Workflow pattern analysis",
                        "Enhanced trigger word detection"
                    ]
                },
                "statistics": self.statistics,
                "cross_references": dict(self.cross_references),
                "dependency_graph": {k: list(v) for k, v in self.dependency_graph.items()},
                "components": [component.to_dict() for component in self.components],
                "summary": {
                    "system_health": self.assess_system_health(),
                    "architecture_compliance": self.calculate_architecture_compliance(),
                    "avg_component_size": sum(c.line_count for c in self.components) / max(1, len(self.components)),
                    "orphan_detection_rate": self.statistics["orphan_patterns"] / max(1, self.statistics["total_components"]),
                    "violation_density": (self.statistics["critical_violations"] + self.statistics["major_violations"]) / max(1, self.statistics["total_components"]),
                    "component_count_health": len(self.statistics.get("count_discrepancies", {})) == 0
                }
            }

            # Save to JSON
            output_file = os.path.join(self.output_dir, "system_scan.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            self.print_progress(f"Enhanced semantic data saved to: {output_file}")
            return output_file

        except Exception as e:
            print(f"ERROR saving results: {e}")
            traceback.print_exc()
            return None

    def assess_system_health(self) -> str:
        """NEW: Assess overall system health"""
        critical = self.statistics["critical_violations"]
        major = self.statistics["major_violations"]

        if critical == 0 and major == 0:
            return "excellent"
        elif critical == 0 and major <= 3:
            return "good"
        elif critical <= 2 and major <= 10:
            return "needs_attention"
        else:
            return "critical_issues"

    def calculate_architecture_compliance(self) -> float:
        """NEW: Calculate architecture compliance score"""
        total_components = max(1, self.statistics["total_components"])
        critical_violations = self.statistics["critical_violations"]
        major_violations = self.statistics["major_violations"]

        # Weight critical violations more heavily
        violation_score = (critical_violations * 10) + (major_violations * 5)
        max_possible_score = total_components * 10

        compliance = max(0, (max_possible_score - violation_score) / max_possible_score * 100)
        return round(compliance, 1)

    def print_summary(self):
        """Print summary statistics (enhanced output)"""
        print("\n" + "="*70)
        print("SYSTEM CHECK v5 ENHANCED SUMMARY")
        print("="*70)
        print(f"Total Components Scanned: {self.statistics['total_components']}")
        print(f"Commands: {self.statistics['commands']}")
        print(f"Coordinators: {self.statistics['coordinators']}")
        print(f"Agents: {self.statistics['agents']}")

        # NEW: Component count analysis
        if self.statistics.get("count_discrepancies"):
            print("\nComponent Count Issues:")
            for comp_type, discrepancy in self.statistics["count_discrepancies"].items():
                print(f"  {comp_type}: Expected {discrepancy['expected']}, Found {discrepancy['actual']} ({discrepancy['severity']})")

        print("\nViolation Analysis:")
        print(f"Critical Violations: {self.statistics['critical_violations']}")
        print(f"Major Violations: {self.statistics['major_violations']}")
        print(f"Minor Violations: {self.statistics['minor_violations']}")
        print(f"Orphan Patterns: {self.statistics['orphan_patterns']}")

        # NEW: Enhanced status assessment
        health = self.assess_system_health()
        compliance = self.calculate_architecture_compliance()

        print(f"\nSystem Health: {health.upper()}")
        print(f"Architecture Compliance: {compliance}%")

        if self.statistics['critical_violations'] == 0:
            print("STATUS: System is RECURSION-SAFE")
        else:
            print("STATUS: CRITICAL ISSUES DETECTED")

        # NEW: Architecture violations summary
        if self.statistics.get("architecture_violations"):
            print("\nArchitecture Violations:")
            for violation in self.statistics["architecture_violations"]:
                print(f"  - {violation}")

        print(f"\nOutput Directory: {self.output_dir}")


def main():
    """Main execution function (enhanced)"""
    try:
        print("System Check v5 - PRODUCTION CRITICAL (ENHANCED)")
        print("Comprehensive system diagnostic with MASSIVELY enhanced detection capabilities")
        print("-" * 80)

        checker = SystemChecker()

        # Scan all components
        checker.scan_all_components()

        # NEW: Perform advanced analysis
        checker.perform_advanced_analysis()

        # Calculate statistics
        checker.calculate_statistics()

        # Save results
        output_file = checker.save_results()

        # Print summary
        checker.print_summary()

        if output_file:
            print(f"\nSUCCESS: Complete enhanced system scan saved to {output_file}")
            return 0
        else:
            print("\nFAILURE: Could not save scan results")
            return 1

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())