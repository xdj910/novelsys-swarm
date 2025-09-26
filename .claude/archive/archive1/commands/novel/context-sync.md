---
description: Synchronize context with quality-gated learning
argument-hint: '[section] e.g., "characters", "world", "plot", or "all"'
---

# Context Synchronization

Synchronizing context with quality-gated learning from high-scoring chapters: **$ARGUMENTS**

## Description

This command performs intelligent context synchronization, learning only from chapters that meet quality thresholds. It maintains entity dictionary consistency and updates various context dimensions.

## Quality Gates

Learning only occurs from chapters meeting ALL criteria:
- Quality score >= 95
- Bible compliance = 100%
- No critical issues
- Entity consistency validated

Sync blocks if any chapter scores < 90 (quality risk).

## Execution

Delegating to context sync coordinator:

Use the context-sync-coordinator subagent to synchronize context with quality validation using these instructions:

Perform quality-gated context synchronization for the current project.

Sync Target: '$ARGUMENTS' (if specified)
- 'characters': Update character context only
- 'world': Update world-building context
- 'plot': Update plot progression
- 'all' or none: Full synchronization

Workflow:
1. Validate project and entity dictionary
2. Scan quality reports for all chapters
3. Identify eligible chapters (score >=95)
4. Block if any chapter <90
5. Extract entities from eligible chapters
6. Update entity dictionary
7. Synchronize specified context dimensions
8. Generate learning report

Quality Requirements:
- Only learn from chapters scoring >=95
- Halt if any chapter scores <90
- Need minimum 3 eligible chapters

Update:
- Entity dictionary with new/evolved entities
- Character development context
- World-building context
- Plot progression context

Provide comprehensive sync report with metrics.

## Sync Targets

- **Characters**: Character states, relationships, development
- **World**: Locations, rules, culture, technology
- **Plot**: Active threads, progression, pacing
- **All**: Complete context synchronization

## Process Includes

1. **Quality Validation**: Check all chapter scores
2. **Entity Extraction**: Identify story elements
3. **Dictionary Updates**: Maintain consistency

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

4. **Context Synchronization**: Update relevant dimensions
5. **Learning Report**: Track what was learned

## Output

- Quality summary with eligible/blocked chapters
- Entity discovery metrics
- Context update confirmation
- Recommendations for improvement

## Usage Examples

- `/novel:context-sync` - Full sync of all contexts
- `/novel:context-sync characters` - Update character context only
- `/novel:context-sync world` - Update world-building context
- `/novel:context-sync plot` - Update plot progression

## Next Steps

After successful sync:
- **If entities added**: Review entity dictionary for consistency
- **If sync blocked**: Run `/novel:quality-check-individual` on low-scoring chapters
- **Continue writing**: `/novel:next-chapter` with enriched context
- **Check impact**: `/novel:status` to see updated statistics
- **Fix issues**: `/novel:smart-fix` for chapters below 95 score