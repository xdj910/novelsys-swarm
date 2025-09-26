---
name: knowledge-base-init
description: Initialize and update the Claude Code knowledge base with official documentation
argument-hint: "[topic]"
---

# Knowledge Base Initialization Command

Initialize or update the local knowledge base with official Claude Code documentation.

## Usage

Without arguments - Initialize core documentation:
```bash
claude knowledge-base-init
``

With specific topic:
``bash
claude knowledge-base-init sub-agents
claude knowledge-base-init commands
claude knowledge-base-init hooks
``

## What It Does

1. Creates necessary directory structure
2. Fetches official documentation from Anthropic
3. Creates index file with timestamps
4. Updates existing documents if older than 24 hours

## Process

The command delegates to the knowledge-base-updater agent to:
- Check existing knowledge base structure
- Fetch and save documentation
- Manage cache timestamps
- Create searchable index

This follows Claude Code's command-agent separation pattern where commands delegate to agents.

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/knowledge-base/index.json` (existing documentation index)
  - `.claude/knowledge-base/timestamps.json` (cache timestamps)
  - `.claude/knowledge-base/docs/*.md` (cached documentation)

- **Writes to**:
  - `.claude/knowledge-base/index.json` (updated index)
  - `.claude/knowledge-base/timestamps.json` (updated timestamps)
  - `.claude/knowledge-base/docs/*.md` (fetched documentation)
  - `.claude/knowledge-base/cache/*.json` (processed content cache)