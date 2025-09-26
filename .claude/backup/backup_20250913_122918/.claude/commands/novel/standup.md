---
description: Generate project status report
argument-hint: '[report_type] e.g., "brief", "detailed", "executive", "blocked", or "agents"'
---

# Project Status Report

Generating intelligent status report with type: **$ARGUMENTS**

## Description

This command generates comprehensive project status reports with multi-dimensional analysis. It provides:

- Progress tracking across all dimensions
- Quality metrics and trends
- Agent utilization matrix
- Blocking issues and risks
- Actionable recommendations

## Execution

Delegating to standup coordinator for comprehensive analysis:

Use the standup-coordinator subagent to generate a project status report with these instructions:

Generate a comprehensive status report for the current novel project.

Report Type: '$ARGUMENTS' (if specified)
- 'brief' or 'daily': Quick daily standup format
- 'detailed' or 'progress': Comprehensive analysis
- 'executive': High-level dashboard
- 'blocked': Focus on impediments
- 'agents': Agent utilization analysis
- none: Default to detailed report

Analyze:
1. Project progress (Bible, chapters, quality)
2. System health and agent status
3. Quality metrics and trends
4. Blocking issues and risks
5. Optimization opportunities

Generate insights:
- Critical issues requiring immediate attention
- Progress against timeline
- Quality achievement rates
- Resource utilization efficiency

Provide:
- Executive summary
- Detailed status by dimension
- Prioritized recommendations
- Agent activity matrix

Format appropriately based on report type requested.

## Report Types

- **Brief/Daily**: Quick standup format with key metrics
- **Detailed/Progress**: Comprehensive multi-dimensional analysis  
- **Executive**: High-level dashboard for stakeholders
- **Blocked**: Focus on impediments and resolution paths
- **Agents**: Detailed agent performance and utilization

## Output Includes

- 📈 Executive summary with health score
- 📊 Progress dashboard with metrics
- 🔍 Detailed analysis by dimension
- WARNING:️ Issues and risk assessment
- 💡 Optimization opportunities
- 🎯 Prioritized action items
- 📋 Agent status matrix

## Usage Examples

- `/novel:standup` - Full detailed report
- `/novel:standup brief` - Quick daily standup
- `/novel:standup executive` - Management dashboard
- `/novel:standup blocked` - Focus on blockers
- `/novel:standup agents` - Agent utilization analysis