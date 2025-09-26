---
description: Audit novel creation process to evaluate 95-point quality achievement capability
argument-hint: [timestamp] - Optional timestamp of system-check report (e.g., 20250906_174550)
---

# Novel Process Audit

You audit the NOVELSYS-SWARM novel creation process to identify bottlenecks preventing 95-point quality achievement and provide actionable improvements.

## Execution Flow

### Step 1: Parse Arguments and Determine Timestamp

1. **Check for provided timestamp:**
   - If `$ARGUMENTS` is provided: Store as AUDIT_TIMESTAMP
   - If empty: Find latest report
   
2. **Find latest report (if no argument):**
   - Use Bash tool: `ls -1d .claude/report/[0-9]* 2>/dev/null | sort -r | head -1`
   - If output is empty: Display "[ ] No system-check reports found. Please run: /system-check"
   - If found: Use Bash tool: `basename [found_path]` to extract timestamp
   - Store result as AUDIT_TIMESTAMP

3. **Validate timestamp format (if provided):**
   - Use Bash tool: `echo "$ARGUMENTS" | grep -E "^[0-9]{8}_[0-9]{6}$" >/dev/null && echo "valid" || echo "invalid"`
   - If invalid: Display "[ ] Invalid timestamp format. Expected: YYYYMMDD_HHMMSS"

### Step 2: Verify Required Files Exist

1. **Check report directory:**
   - Use Bash tool: `test -d .claude/report/$AUDIT_TIMESTAMP && echo "exists" || echo "missing"`
   - If missing: Display "[ ] Report directory not found: .claude/report/$AUDIT_TIMESTAMP/"
   - List available timestamps if directory missing

2. **Verify critical files:**
   ```bash
   # Check each required file
   test -f .claude/report/$AUDIT_TIMESTAMP/system_health_report.md || echo "Missing: system_health_report.md"
   test -f .claude/report/$AUDIT_TIMESTAMP/dependency-mapper_report.json || echo "Missing: dependency-mapper_report.json"
   test -f .claude/temp/flow_$AUDIT_TIMESTAMP/chapter-start.json || echo "Missing: chapter-start.json"
   ```
   - If any missing: Display warning but continue

### Step 3: Verify Key Files Exist

1. **Check critical analysis files:**
   ```bash
   # Verify system health report
   test -f .claude/report/$AUDIT_TIMESTAMP/system_health_report.md || echo "Warning: Missing system_health_report.md"
   
   # Verify flow analysis
   test -f .claude/temp/flow_$AUDIT_TIMESTAMP/chapter-start.json || echo "Warning: Missing chapter-start.json"
   ```

2. **Count available reports:**
   - Use Bash tool: `ls -1 .claude/report/$AUDIT_TIMESTAMP/*.json 2>/dev/null | wc -l`
   - Display: "Found {count} analysis reports in timestamp directory"

### Step 4: Prepare Context for Agent

1. **Gather basic statistics:**
   - Use Bash tool: `find .claude/data/projects -name "quality_report.json" 2>/dev/null | wc -l`
   - Store as chapters_generated_count

2. **Prepare paths for agent:**
   - Report directory: `.claude/report/{AUDIT_TIMESTAMP}/`
   - Flow directory: `.claude/temp/flow_{AUDIT_TIMESTAMP}/`
   - Data directory: `.claude/data/`

### Step 5: Launch Process Auditor Agent

Use Task tool with:
- **subagent_type**: "novel-quality-process-auditor"
- **description**: "Audit novel creation process"
- **prompt**: 
```
Audit the novel creation process for 95-point quality achievement.

Paths for your analysis:
- System reports: .claude/report/{AUDIT_TIMESTAMP}/
- Flow analysis: .claude/temp/flow_{AUDIT_TIMESTAMP}/
- Project data: .claude/data/

Key files to analyze:
1. System health: .claude/report/{AUDIT_TIMESTAMP}/system_health_report.md
2. Dependencies: .claude/report/{AUDIT_TIMESTAMP}/dependency-mapper_report.json
3. Resource usage: .claude/report/{AUDIT_TIMESTAMP}/resource-analyzer_report.json
4. Chapter flow: .claude/temp/flow_{AUDIT_TIMESTAMP}/chapter-start.json
5. Quality flow: .claude/temp/flow_{AUDIT_TIMESTAMP}/quality-check-individual.json
6. Bible flow: .claude/temp/flow_{AUDIT_TIMESTAMP}/bible-create.json

Existing chapters found: {chapters_generated_count}

Please:
1. Read and analyze the above reports
2. Identify why system cannot achieve 95-point quality
3. Find specific bottlenecks in creation process
4. Compare with bestseller standards
5. Generate actionable improvements

Save your comprehensive report to: .claude/report/{AUDIT_TIMESTAMP}/novel_process_audit.md
```

### Step 6: Display Results

1. **Confirm report generation:**
   - Use Bash tool: `test -f .claude/report/$AUDIT_TIMESTAMP/novel_process_audit.md && echo "[x] Audit complete" || echo "[ ] Report generation failed"`

2. **Display summary:**
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   [x] Novel Process Audit Complete
   
   Report: .claude/report/{AUDIT_TIMESTAMP}/novel_process_audit.md
   
   Key Findings:
   - Current capability: {extracted_score}/100
   - Distance to goal: {95 - extracted_score} points
   - Top bottleneck: {main_issue}
   
   Review the report for detailed improvement recommendations.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

## Error Handling

### No Reports Found
```
[ ] No system-check reports found
   
   Please run: /system-check
   Then run: /novel-process-audit
```

### Invalid Timestamp
```
[ ] Invalid timestamp: {provided_timestamp}

Available reports:
- 20250906_174550
- 20250906_173631
- [other timestamps]

Usage: /novel-process-audit [timestamp]
```

### Incomplete Report Data
```
WARNING:️ Warning: Some system-check data is missing
   
   Missing files:
   - {list of missing files}
   
   Audit will continue with available data.
   For complete analysis, run: /system-check
```

## Success Criteria

- Correctly handles both with and without timestamp argument
- Gracefully handles missing or incomplete data
- Launches novel-quality-process-auditor with comprehensive context
- Generates actionable report at correct location
- Provides clear feedback to user

## Important Notes

- Focus on process and system capabilities, not content quality
- Emphasize actionable improvements over theoretical analysis
- Report should be immediately useful for improving the system
- Keep user informed of progress throughout execution