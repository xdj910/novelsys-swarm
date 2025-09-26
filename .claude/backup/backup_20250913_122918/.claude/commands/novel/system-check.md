---
description: Run comprehensive system health check using specialized coordinator
---

# System Health Check

Performs deep multi-phase system analysis through coordinated execution of 15 agent invocations across 14 specialized agents.

## Purpose

Comprehensive health assessment covering:
- System dependencies and relationships
- Execution flow analysis and safety validation
- Claude Code compliance verification
- Novel creation capability assessment
- Resource utilization and optimization opportunities

## Description

This command initiates a comprehensive system health check that analyzes all aspects of the NOVELSYS-SWARM system through coordinated execution of specialized agents.

## Execution

Delegating to system-check-coordinator:

Use the system-check-coordinator subagent to orchestrate a comprehensive 5-phase system health check with these instructions:

Execute complete system health analysis through 5 distinct phases:
- Phase 1: Foundation Analysis (6 parallel system checkers)
- Phase 2: Flow Analysis (2 parallel execution mappers)
- Phase 3: Safety Analysis (2 parallel analyzers, then 1 validator)
- Phase 4: Compliance Analysis (3 Claude Code expert reviews)
- Phase 5: Capability & Reporting (assessment and final report)

Generate timestamped reports in .claude/report/{timestamp}/ directory.
Ensure all 15 agent invocations execute successfully and produce comprehensive health assessment.

## Expected Output

The coordinator will:
1. Generate unique timestamp for this check
2. Create report directory: `.claude/report/YYYYMMDD_HHMMSS/`
3. Execute 14 specialized agents (15 invocations) across 5 phases
4. Generate individual agent reports
5. Create aggregated system health report
6. Display summary with health score and recommendations

## Report Contents

- **Individual Reports** (15 JSON/MD files)
- **System Flow Diagram** (visual architecture map)
- **Final Health Report** (comprehensive assessment)
- **Health Score** (0-100 with breakdown)
- **Priority Recommendations** (actionable improvements)

## Report Location

All reports saved to: `.claude/report/YYYYMMDD_HHMMSS/`

View the main report: `system_health_report.md`

## Notes

- Execution time: ~5-10 minutes
- Requires all checker agents to be present
- Continues even if individual checks fail
- Provides partial assessment if components are missing

## Next Steps

After system check completes:
- **Score 95+**: System optimal, continue normal operations
- **Score 85-94**: Review recommendations, run suggested fixes
- **Score <85**: Address critical issues before continuing
- Review detailed report: Check `system_health_report.md`
- Fix issues: Follow priority recommendations in report
- Re-run check: `/novel:system-check` after fixes