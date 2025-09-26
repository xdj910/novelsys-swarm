---
description: Run comprehensive system health check and architecture analysis
---

# System Health Check

Performs complete system architecture analysis, compliance validation, and health assessment.

## Purpose

Generate comprehensive visibility into system architecture including:
- All components and their relationships with enhanced orphan detection (V5)
- Complete semantic extraction with 17-field metadata
- Comprehensive CLAUDE.md compliance validation
- System health metrics with accurate orphan analysis (8-pattern recognition)
- Complete I/O patterns, execution contexts, and business logic
- Actionable improvement recommendations

## Description

This command initiates a deep system analysis using V5 scanner that combines V3's complete semantic extraction (7 extractors) with V4's enhanced orphan detection (8-pattern recognition), providing full data completeness for downstream analysis while eliminating false positive orphan components.

## Execution

Use the system-check-coordinator subagent to orchestrate comprehensive system analysis:

Analyze system health requirements and create execution plan for three-phase analysis:
- Phase 1: Deep scanning with V5 scanner - complete semantic extraction (10 modules) + enhanced orphan detection (8-pattern recognition)
- Phase 2: Architecture analysis with full ComponentMetadata - I/O patterns, prompts, execution context, business logic, and compliance validation
- Phase 3: Comprehensive report generation with accurate metrics and actionable insights

Ensure proper data flow between agents and generate reports in .claude/report/{timestamp}/ directory.

IMPORTANT: When calling agents with Task tool, avoid using exact file names in prompts. Use descriptive language instead (e.g., "analyze scan data in report directory") to prevent trigger word issues that cause false "Prompt too long" errors.

## Expected Output

- **Scan data file**: Complete system metadata with 17-field ComponentMetadata and enhanced orphan detection (~1MB)
- **Analysis file**: Comprehensive analysis with relationships, compliance, and health metrics
- **Report file**: Human-readable markdown with visualizations and actionable recommendations
- Health score (0-100) with detailed violation breakdown and specific fixes

## Next Steps

After completion:
- Review system_report.md for complete findings
- Address critical violations immediately
- Follow prioritized recommendations
- Re-run after fixes to verify improvements