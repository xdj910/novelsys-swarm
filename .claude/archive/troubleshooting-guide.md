# NOVELSYS-SWARM Troubleshooting Guide
*Last Updated: 2025-09-11*

## 🚨 Quick Diagnosis Flowchart

```
Error occurs
     v 
Is it Python execution error?
    YES  ->  Check Section 1
    NO  v 
Is it path/space error?
    YES  ->  Check Section 2
    NO  v 
Are pipeline steps missing?
    YES  ->  Check Section 3
    NO  v 
Is it entity/name error?
    YES  ->  Check Section 4
    NO  v 
Check Section 5 (General)
```

## Section 1: Python Execution Errors

### [ ] Error Pattern
```bash
Error: Permission to use Bash with command python claude_subagents.py
```

### [x] Solution Steps

1. **Immediate Fix**:
   ```python
   # Instead of Python execution, use Task tool directly:
   Task(
       subagent_type="agent-name",
       description="Brief description",
       prompt="Detailed instructions"
   )
   ```

2. **Verify settings.local.json**:
   ```json
   {
     "deny": [
       "Bash(python claude_subagents.py:*)"
     ]
   }
   ```

3. **Check coordinator/agent for Python references**:
   ```bash
   grep -r "python.*subagent" .claude/
   ```

4. **Remove any Python fallback code**

### 🔍 Root Cause
- Task tool internal fallback mechanism
- Legacy compatibility code
- System correctly blocks dangerous execution

## Section 2: Path and Space Errors

### [ ] Error Pattern
```bash
Error: /usr/bin/bash: eval: line 1: unexpected EOF while looking for matching `"'
```

### [x] Solution Steps

1. **Quote paths with spaces**:
   ```bash
   # Wrong:
   cd .claude/data/projects/Teide Cove Mysteries
   
   # Correct:
   cd ".claude/data/projects/Teide Cove Mysteries"
   ```

2. **Use forward slashes**:
   ```bash
   # Wrong (Windows backslash):
   .claude\data\projects\
   
   # Correct (cross-platform):
   .claude/data/projects/
   ```

3. **In agents/coordinators**:
   - Always use forward slashes
   - Quote all paths that might contain spaces
   - Test with project names containing spaces

### 🔍 Root Cause
- Windows path handling
- Unquoted spaces in project names
- Backslash vs forward slash confusion

## Section 3: Pipeline Steps Missing

### [ ] Error Pattern
- Only v01, v02, v10 files created
- v03-v09 missing
- 70% of pipeline skipped

### [x] Solution Steps

1. **Add mandatory execution requirements**:
   ```markdown
   ### WARNING:️ MANDATORY EXECUTION REQUIREMENTS
   
   **YOU MUST EXECUTE ALL 10 STEPS IN SEQUENCE. DO NOT SKIP ANY STEPS.**
   ```

2. **Add verification checkpoints**:
   ```markdown
   **EXECUTION CHECKPOINTS:**
   - After Step 3: Verify v01, v02, v03 all exist
   - After Step 5: Verify v04, v05 exist (midpoint)
   - After Step 7: Verify v06, v07 exist
   - After Step 9: Verify v08 (if genre), v09 exist
   - After Step 10: Verify complete pipeline v01-v10
   ```

3. **Implement failure protocol**:
   ```markdown
   If ANY validation fails:
   - STOP immediately with error report
   - Include: Step number, missing file, last successful step
   - DO NOT continue or skip ahead
   ```

4. **Test pipeline execution**:
   ```bash
   ls -la ".claude/data/projects/{project}/book_1/chapters/ch001/versions/"
   # Should show v01 through v10 files
   ```

### 🔍 Root Cause
- Weak execution requirements
- No intermediate validation
- Steps treated as optional

## Section 4: Entity/Name Errors

### [ ] Error Pattern
- Wrong character names (Sarah instead of María)
- Inconsistent entity references
- Bible violations

### [x] Solution Steps

1. **Verify entity dictionary**:
   ```bash
   cat .claude/data/projects/{project}/shared/entity_dictionary.yaml
   ```

2. **Check entity-validator recording**:
   ```yaml
   # Must include:
   validated_entities:
     - "María Dolores Santana"
     - "José Hernández"
     # etc.
   ```

3. **Ensure Bible compliance**:
   - All names must be English/Western
   - No Chinese characters or pinyin
   - British English spelling

4. **Fix outline-generator dependencies**:
   - Don't rely on missing files
   - Use Bible as primary source
   - No default templates

### 🔍 Root Cause
- Missing file dependencies
- Fallback to defaults
- Incomplete validation

## Section 5: General Issues

### Command Too Long (>200 lines)

**Solution**: Create a coordinator
```python
# In command file:
Task(
    subagent_type="new-coordinator",
    description="Coordinate complex task",
    prompt="..."
)
```

### Bash Code Block Overuse

**Solution**: Replace with prose
```markdown
# Instead of:
```bash
echo "Starting process..."
```

# Use:
**Progress:** "Starting process..."
```

### Variable Syntax Confusion

**Solution**: Follow conventions
```markdown
- User arguments: $ARGUMENTS
- Runtime variables: {variable}
- Environment: $ENVVAR
```

## 🛠️ Diagnostic Commands

### Check System Health
```bash
# Check all version files
ls -la .claude/data/projects/*/book_*/chapters/*/versions/

# Find Python references
grep -r "python.*subagent\|claude_subagents" .claude/

# Check path issues
find .claude -name "*.md" -exec grep -l "D:\\\\" {} \;

# Verify entity dictionary
cat .claude/data/projects/*/shared/entity_dictionary.yaml | head -20
```

### Validate Coordinator
```bash
# Check line count
wc -l .claude/agents/*coordinator*.md

# Count bash blocks
grep -c "```bash" .claude/agents/*coordinator*.md

# Check for Python
grep -n "python" .claude/agents/*coordinator*.md
```

## 📋 Prevention Checklist

Before running chapter generation:
- [ ] Entity dictionary exists and is correct
- [ ] Bible files are valid YAML
- [ ] No Python references in coordinators
- [ ] Paths are quoted if they contain spaces
- [ ] settings.local.json has deny rules

During development:
- [ ] Test with project names containing spaces
- [ ] Verify all 10 version files are created
- [ ] Check entity validation records
- [ ] Run claude-code-expert validation

After issues:
- [ ] Document new error patterns
- [ ] Update this guide
- [ ] Add detection rules to claude-code-expert
- [ ] Update CLAUDE.md if needed

## 🔗 Related Documentation

- [CLAUDE.md](./CLAUDE.md) - Project memory and rules
- [claude-code-expert.md](.claude/agents/claude-code-expert.md) - Validation agent
- [settings.local.json](.claude/settings.local.json) - Security rules

## 📞 Getting Help

1. Run diagnostics first
2. Check this guide
3. Use claude-code-expert for validation
4. Document new issues for future reference

---
*Remember: Most errors are caught by the safety systems - that's a good thing!*