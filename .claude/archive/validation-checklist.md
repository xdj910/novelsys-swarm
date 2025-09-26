# NOVELSYS-SWARM Validation Checklist
*Version 1.0 - 2025-09-11*

## 🚀 Pre-Flight Checklist (Before Any Major Operation)

### System Readiness
- [ ] Current project set: `cat .claude/data/context/current_project.json`
- [ ] Bible files valid: `yamllint .claude/data/projects/*/bible.yaml`
- [ ] Entity dictionary exists: `ls .claude/data/projects/*/shared/entity_dictionary.yaml`
- [ ] Settings configured: `cat .claude/settings.local.json | grep deny`

### Environment Check
- [ ] CLAUDECODE=1 confirmed: `echo $CLAUDECODE`
- [ ] No Python scripts: `ls *.py 2>/dev/null | wc -l` (should be 0)
- [ ] Claude directory exists: `ls -la .claude/`

## 📝 Component Creation Checklist

### Creating New Coordinator
- [ ] Name follows pattern: `{task}-coordinator.md`
- [ ] YAML frontmatter includes `thinking` keyword
- [ ] Execution Model section present
- [ ] No Python references (`grep -c "python" {file}` should be 0)
- [ ] Task tool usage documented
- [ ] Path handling considers spaces
- [ ] Variable syntax correct ($ARGUMENTS vs {variable})
- [ ] Error handling complete
- [ ] Line count < 850

### Creating New Agent
- [ ] YAML frontmatter complete (name, description)
- [ ] Thinking directive for complex agents
- [ ] No hardcoded absolute paths
- [ ] File-based communication only
- [ ] British English enforced (for content agents)
- [ ] Atomic file operations used
- [ ] No Python execution
- [ ] Clear input/output specification

### Creating New Command
- [ ] Line count < 150 (or uses coordinator)
- [ ] Pure delegation pattern
- [ ] Single Task call to coordinator/agent
- [ ] No business logic
- [ ] Clear argument handling
- [ ] No step-by-step execution

## 🔍 Pipeline Validation Checklist

### Before Chapter Generation
- [ ] Run: `/novel:bible-view` - Verify Bible content
- [ ] Check: Entity dictionary has all main characters
- [ ] Verify: Project uses British English
- [ ] Confirm: No spaces in critical paths or properly quoted

### During Chapter Generation
- [ ] Monitor: Version files being created (v01-v10)
- [ ] Watch for: Python execution errors (should be blocked)
- [ ] Check: Each step completes before next begins
- [ ] Verify: No steps skipped

### After Chapter Generation
- [ ] All 10 version files exist
- [ ] quality_report.json created
- [ ] Score >= 95 achieved
- [ ] content.md is final v10 version
- [ ] Entity validation passed

## 🛡️ Security & Safety Checklist

### Code Safety
- [ ] No `python claude_subagents.py` anywhere
- [ ] No hardcoded passwords/keys
- [ ] No shell injection vulnerabilities
- [ ] Paths properly quoted/escaped

### Data Integrity
- [ ] Atomic writes with .tmp files
- [ ] File locks for concurrent access
- [ ] Backup before major changes
- [ ] Version control for rollback

## 🎯 Quality Validation Checklist

### Run Claude-Code-Expert
```bash
# Full system audit
Task(
    subagent_type="claude-code-expert",
    description="Full compliance audit",
    prompt="Audit all coordinators and agents for compliance"
)
```

### Check Critical Scores
- [ ] Python execution detection: 1.0 (no Python)
- [ ] Pipeline integrity: > 0.8
- [ ] Path handling: > 0.9
- [ ] Bash block density: > 0.8
- [ ] Entity validation: 1.0

### Manual Verification
- [ ] Coordinator execution model clear
- [ ] No fallback mechanisms
- [ ] Mandatory execution requirements present
- [ ] Checkpoints at steps 3, 5, 7, 9
- [ ] Error handling comprehensive

## 📊 Performance Checklist

### Optimization Targets
- [ ] Commands < 150 lines
- [ ] Coordinators < 850 lines
- [ ] Agents < 500 lines
- [ ] User interactions minimized (<=3 for new project)
- [ ] Parallel execution where possible

### Cache Utilization
- [ ] Bible cache active
- [ ] Context files up-to-date
- [ ] Shared context reduces I/O
- [ ] No redundant file reads

## 🔄 Post-Issue Checklist

### After Encountering Problems
- [ ] Document error pattern
- [ ] Update troubleshooting guide
- [ ] Add detection rule to claude-code-expert
- [ ] Update CLAUDE.md if systematic issue
- [ ] Create test case for regression
- [ ] Share learning with team

### Validation After Fix
- [ ] Problem no longer reproducible
- [ ] No new issues introduced
- [ ] Documentation updated
- [ ] Detection rules catch similar issues
- [ ] Clean test run completed

## 📅 Regular Maintenance Checklist

### Daily
- [ ] Check system health: `/novel:system-check`
- [ ] Verify current project correct
- [ ] Review any error logs

### Weekly
- [ ] Run full claude-code-expert audit
- [ ] Clean up temp files
- [ ] Update entity dictionary if needed
- [ ] Review and merge any updates

### Per Project
- [ ] Validate Bible quality scores
- [ ] Check entity consistency
- [ ] Verify British English throughout
- [ ] Ensure all version files generated
- [ ] Archive completed chapters

## 🚦 Quick Status Checks

```bash
# System ready?
echo "CLAUDECODE: $CLAUDECODE"

# Project set?
cat .claude/data/context/current_project.json | grep current_project

# Bible valid?
head -5 .claude/data/projects/*/book_1/bible.yaml

# Entity dictionary OK?
grep "maria_santana" .claude/data/projects/*/shared/entity_dictionary.yaml

# No Python scripts?
find . -name "*.py" 2>/dev/null | head -5

# Version files complete?
ls .claude/data/projects/*/book_*/chapters/*/versions/v*.md | wc -l
```

## [x] Final Sign-Off

Before declaring system ready:
- [ ] All checklists above completed
- [ ] Test chapter generation successful
- [ ] Quality score >= 95 achieved
- [ ] No Python execution errors
- [ ] No path handling errors
- [ ] All 10 pipeline steps executed
- [ ] Documentation current
- [ ] Team briefed on changes

---
*Use this checklist before, during, and after operations to ensure system reliability*