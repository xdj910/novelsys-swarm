---
name: t1-ttd-article
description: "Create high-quality articles using TTD-DR methodology with three-dimensional quality assessment"
argument-hint: '[inspiration] <mode>'
---

# T1-TTD Article Creation System

IMPORTANT: Avoid file names in Task prompts to prevent trigger word errors.

Orchestrate the T1-TTD article creation workflow using the advanced TTD-DR methodology with automatic status management and corrected human collaboration patterns.

## Input Processing
The user input can be any form of inspiration:
- Text descriptions ("I saw an interesting discussion about...")
- File paths (research papers, documents)
- URLs (articles, social media posts)
- Raw ideas or observations

## Workflow Orchestration
Use the t1-ttd-article-coordinator subagent to orchestrate the complete workflow.
The coordinator will analyze the inspiration and return a comprehensive execution plan with status tracking integration.

## Quality Standards
- Target: Tier A quality in all three dimensions
- Accuracy: 95%+ verified statements
- Insight: Synthetic level analysis with cross-domain connections
- Originality: <0.5 similarity score with novel concept combinations

## Status Management
The system provides comprehensive status tracking:
- Real-time progress visibility
- Quality progression monitoring
- Checkpoint detection tracking
- Automatic recovery from interruptions

## Human Collaboration (CORRECTED)
The system includes optional human-AI collaboration checkpoints:
- Agents detect checkpoint conditions
- Agents return checkpoint data to Main Claude
- Main Claude handles ALL human interaction
- Options presented: numerical choices (1/2/3)
- User decisions processed by Main Claude only

## Output Delivery
Final deliverables include:
- Complete article with quality certification
- Multi-platform versions (Medium, Substack, ElevenReader)
- Transparent quality assessment report
- Complete status and quality progression audit trail