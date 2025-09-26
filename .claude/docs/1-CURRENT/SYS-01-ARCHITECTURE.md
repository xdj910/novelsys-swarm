# SYS-01-ARCHITECTURE - System Architecture Overview
*Based on CLAUDE.md v6.6 Standards*

## Five-Layer Architecture (Recursion-Safe)

```
User Input
    |
Command Layer (<100 lines, pure delegation)
    |
Main Claude (only orchestrator with Task)
    |-> Task -> Coordinator (returns plan, no Task)
    |-> Task -> Agents (execute tasks, no Task)
              |
================================
    File System / Data Layer
    (Key to preventing recursion: file communication, not function calls)
================================
```

## Critical Rules (From CLAUDE.md)

### 1. NO Unicode Characters
- ALL components use ASCII only
- No emojis, special arrows, checkmarks
- Windows compatibility requirement

### 2. Recursion Prevention
```yaml
Correct:
  Main Claude: Has Task tool
  Coordinators: NO Task tool (returns JSON plans)
  Agents: NO Task tool (execute single tasks)

Wrong (causes recursion):
  Coordinator with Task -> Agent with Task -> CRASH
```

### 3. Tool Distribution
```yaml
Main Claude:
  tools: [all tools including Task]

Coordinators:
  tools: [Read, Write, Bash, Grep]  # NEVER Task!

Agents:
  tools: [only task-specific, NEVER Task]
```

## Research System Architecture

### Components (7 Total)
```
1 Coordinator + 6 Agents:
├── research-coordinator (orchestrates progressive exploration)
├── trend-analyzer (market trends)
├── competitor-scanner (competition analysis)
├── audience-profiler (reader demographics)
├── voice-analyzer (writing style analysis)
├── topic-explorer (theme research)
└── bible-generator (synthesis to 7 documents)
```

### Data Flow
```
Natural Language Input
    ↓
Main Claude (detects triggers)
    ↓
research-coordinator (suggests 1-2 next steps)
    ↓
User Choice
    ↓
Execute Selected Agent
    ↓
Generate Research JSON (5 types)
    ↓
bible-generator
    ↓
7 Production Documents
```

## PROACTIVE Agent Triggering

### How It Works
```python
# Main Claude detects trigger words
if "I want to write" in conversation:
    Task -> research-coordinator

if "market trends" in conversation:
    Task -> trend-analyzer

# No commands needed!
```

### Trigger Examples
- "I want to write" -> research-coordinator
- "what's popular" -> trend-analyzer
- "competitors" -> competitor-scanner
- "target readers" -> audience-profiler
- "writing style" -> voice-analyzer
- "story ideas" -> topic-explorer

## File System Communication

### Why File System Prevents Recursion
```python
# Without file system = recursion crash
Agent A(Task) -> Agent B(Task) -> CRASH

# With file system = no recursion
Agent A -> Write -> file.json
                      |
Agent B -> Read -> file.json
```

### Standard File Structure
```
knowledge_base/
├── trends/
│   └── trend_analysis_[timestamp].json
├── competitors/
│   └── [niche]_[timestamp].json
├── audience/
│   └── audience_profile_[timestamp].json
├── voice/
│   └── comprehensive_voice_analysis_[timestamp].json
├── topics/
│   └── topic_analysis_[timestamp].json
└── bible/
    ├── series_bible.yaml
    ├── VOICE_STYLE_GUIDE.md
    ├── VOICE_CONSISTENCY_CHECKLIST.md
    └── [4 more documents]
```

## Progressive Exploration Pattern

### Old vs New Approach
```yaml
OLD (Batch):
  Run ALL agents -> Overwhelming results

NEW (Progressive):
  Suggest 1-2 steps -> User chooses -> Execute -> Feedback -> Next step
```

### Implementation
- Coordinator analyzes state
- Returns JSON plan with options
- Main Claude presents choices
- User maintains control
- Infinite revision loops supported

## Human Review Integration

### Review Gates
1. After each research agent
2. Before bible generation
3. After document creation
4. Support partial regeneration

### Implementation Pattern
```yaml
Human-in-Loop (Verified):
  Display results
  "1) Approve  2) Modify"
  If modify: collect feedback -> regenerate
  Loop until approved
```

## Error Handling

### Trigger Word Safety
```yaml
Problem: Some file names trigger Task tool errors
Solution: Use descriptive language, not exact file names

WRONG: "analyze system_scan.json"
RIGHT: "analyze scan data in report directory"
```

### Large File Handling
```yaml
Chunked Reading Pattern:
  chunk_size = 2000 lines
  Read with offset + limit
  Process chunks sequentially
```

## System Status

### Implemented ✓
- All 7 research components
- PROACTIVE triggering
- Progressive exploration
- 5 JSON -> 7 document synthesis
- Human review capability

### Verified ✓
- No recursion risks
- Windows compatibility
- Large file handling
- Trigger word safety

## References
- CLAUDE.md v6.6 - System authority
- Template system in .claude/templates/
- Test validations in CLAUDE.md section "System Test Validation Status"