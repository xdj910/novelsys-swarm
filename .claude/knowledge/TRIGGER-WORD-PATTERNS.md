# Trigger Word Patterns - Task Tool Safety Guide

## Purpose
Document all known trigger words and patterns that cause Task tool issues, providing safe alternatives.

## Known Trigger Patterns

### File Names That Trigger Auto-Loading
| Trigger Pattern | Safe Alternative | Reason |
|----------------|------------------|---------|
| `system_scan.json` | "scan data file" | Large file auto-load |
| `.claude/` paths | "project directory" | Path validation attempt |
| `*.json` over 1MB | "data file" | Size limit exceeded |

### Safe Prompt Patterns

#### For File Processing
```yaml
UNSAFE:
  "Process system_scan.json"
  "Analyze .claude/report/xxx/system_scan.json"
  "Read the file at {exact_path}"

SAFE:
  "Process scan data in report directory"
  "Analyze files in the report folder"
  "Process the data file provided"
```

#### For Directory References
```yaml
UNSAFE:
  "Check .claude/agents/*.md files"
  "Process all files in .claude/report/"

SAFE:
  "Check agent definition files"
  "Process report directory contents"
```

## Implementation Guidelines

### For Commands
- Always include trigger word warning in execution section
- Use descriptive language instead of exact paths

### For Coordinators
- Return semantic descriptions, not file names
- Use type + directory pattern instead of full paths

### For Main Claude
- Check prompts for trigger patterns before Task calls
- Transform unsafe patterns to safe alternatives

### For Agents
- Construct file paths internally
- Never rely on exact file names in prompts

## Testing Checklist
Before deploying any new workflow:
- [ ] Check for hardcoded file names in prompts
- [ ] Test with large files (>1MB)
- [ ] Verify no `.claude/` paths in Task prompts
- [ ] Ensure agents build paths internally

## Future Discoveries
Add new trigger patterns here as discovered:
- Pattern: [to be added]
- Safe alternative: [to be added]
- Date discovered: [to be added]