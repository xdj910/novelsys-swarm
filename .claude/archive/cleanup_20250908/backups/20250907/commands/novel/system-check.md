---
description: Run comprehensive system health check
---

# System Health Check

Performs deep system analysis through a coordinator agent that manages parallel execution of specialized checkers.

## Cross-Platform Compatibility Note
All shell commands in this check use POSIX-compatible syntax to work across Windows (Git Bash), macOS, and Linux.
- Uses `ls` instead of `dir` for file listing
- Uses forward slashes `/` for paths
- Includes `2>/dev/null` for error suppression
- See `.claude/docs/cross-platform-shell-guide.md` for details

## Purpose

Map complete system relationships ("blood vessel diagram") and detect all potential issues:
- Command  ->  Agent  ->  Agent dependencies
- Context setup and file prerequisites
- System triggers and execution flows
- File I/O consistency
- Claude Code compliance
- Resource utilization

## MANDATORY WORKFLOW

**CRITICAL: Throughout this workflow, you will see {TIMESTAMP_VALUE} placeholders. You MUST replace ALL occurrences with the actual timestamp generated in Step 1 (e.g., "20250906_160000"). This ensures all components use the same timestamp.**

### Step 1: Initialize Health Check Environment

1. **Create report directory and timestamp:**
   - Use Bash tool: `date +%Y%m%d_%H%M%S`
   - Store the output as TIMESTAMP_VALUE (e.g., "20250906_160000")
   - Use Bash tool: `mkdir -p .claude/report/{TIMESTAMP_VALUE}` (replace {TIMESTAMP_VALUE} with actual value)
   - Remember this TIMESTAMP_VALUE for all subsequent steps
   - Confirm: "[x] Report directory initialized: .claude/report/{TIMESTAMP_VALUE}"
   - Confirm: "[x] All reports will be saved in timestamped folder"

2. **Create temp directory for flow analysis:**
   - Use Bash tool: `mkdir -p .claude/temp/flow_{TIMESTAMP_VALUE}` (use the value from Step 1)
   - Confirm: "[x] Temp directory created for flow analysis"

3. **Log initiation:**
   - Use Bash tool:
   ```bash
   echo "=== System Health Check Started ==="
   echo "Timestamp: {TIMESTAMP_VALUE}"
   echo "Reports directory: .claude/report/{TIMESTAMP_VALUE}/"
   echo "Temp directory: .claude/temp/flow_{TIMESTAMP_VALUE}/"
   echo "Starting 4-phase system analysis..."
   ```
   (Replace all {TIMESTAMP_VALUE} with the actual timestamp from step 1)

### Step 2: Launch 6 System Checkers in PARALLEL (Phase 1)

**CRITICAL: Execute ALL 6 system checkers in PARALLEL**

When you reach this step, you MUST:
1. Display: "⏳ Launching 6 parallel system checkers..."
2. Use Task tool 6 times in a SINGLE message
3. Each Task call must use a different checker agent
4. **CRITICAL**: In each Task's prompt, replace ALL {TIMESTAMP_VALUE} placeholders with the actual timestamp from Step 1

**The 6 system checker agents to launch (ALL in parallel):**

1. **dependency-mapper**: Map all system dependencies
   - Collect all agent files from `.claude/agents/*.md`
   - Map command  ->  agent usage patterns
   - Map agent  ->  agent call patterns
   - Identify missing and orphan agents
   - Generate dependency relationship map

2. **consistency-validator**: Check naming and path consistency
   - Validate naming conventions across files
   - Check path patterns and hardcoded values
   - Verify reference consistency

3. **filesystem-auditor**: Audit filesystem design
   - Validate filesystem structure
   - Check I/O operations and path consistency
   - Verify directory structures

4. **context-inspector**: Analyze context dependencies
   - Analyze command context requirements
   - Map agent context prerequisites
   - Track context data flow chains
   - Generate context flow diagrams

5. **compliance-checker**: Check Claude Code compliance
   - Validate agent YAML frontmatter
   - Check name/filename consistency
   - Verify Claude Code specification compliance

6. **resource-analyzer**: Analyze resource utilization
   - Find unused/orphan agents and components
   - Check resource utilization patterns
   - Verify configuration consistency

**IMPORTANT EXECUTION NOTES:**
- You MUST launch ALL 6 agents in ONE message with 6 Task tool calls
- Do NOT skip any agents - all 6 are required
- Each agent receives timestamp directly in their prompt (no file reading needed)
- All reports save to `.claude/report/{TIMESTAMP_VALUE}/{agent-name}_report.json`

**Example Task Structure:**
Each Task should specify:
- subagent_type: "agent-name"
- description: "Brief description"
- prompt: "Detailed instructions (use the Instructions below, replacing {TIMESTAMP_VALUE} with actual timestamp)"

**Detailed instructions for each of the 6 agents:**

1. **dependency-mapper**: Map all system dependencies  
   - Description: "Map all system dependencies"
   - Instructions: "You are analyzing NOVELSYS-SWARM dependencies. Follow these EXACT steps IN ORDER:
     
     STEP 1: Collect all agent files
     - Use Glob tool: `.claude/agents/*.md`
     - Extract filenames without .md extension
     - Create list: all_agent_files = [agent1, agent2, ...]
     - Exclude from list: base-agent-template, AGENT_SAVE_INSTRUCTION
     - Store count: total_agents = count of items in all_agent_files list
     
     STEP 2: Map command  ->  agent usage
     - Use Glob tool: `.claude/commands/novel/*.md`
     - For each command file: Use Grep tool with pattern: 'subagent_type[=:]\\s*\"([^\"]+)\"'
     - CRITICAL: This matches BOTH subagent_type=\"x\" AND subagent_type: \"x\"
     - Extract all agent names from matches
     - Store: command_dependencies[command_name] = [agent_list]
     - Create: agents_used_by_commands = unique list from all command_dependencies values
     
     STEP 3: Map agent  ->  agent calls
     - For each file in `.claude/agents/*.md`: Use Grep tool with pattern: 'subagent_type[=:]\\s*\"([^\"]+)\"'
     - If matches found, store: agent_dependencies[agent_name] = [called_agents]
     - Create: agents_called_by_agents = unique list from all agent_dependencies values
     
     STEP 4: Identify missing agents
     - Combine: all_referenced = unique(agents_used_by_commands + agents_called_by_agents)
     - For each agent in all_referenced: If agent NOT in all_agent_files: add to missing_agents
     - Filter out template references like \"agent-name\"
     
     STEP 5: Find orphan agents (MUST BE ACCURATE)
     - Combine: all_used = unique(agents_used_by_commands + agents_called_by_agents)
     - Initialize: orphan_agents = []
     - For each agent in all_agent_files: If agent NOT in all_used: add agent to orphan_agents
     - CRITICAL VALIDATION: If entity-validator is in command_dependencies values  ->  NOT orphan
     
     STEP 6: Generate report with exact structure
     - The timestamp for this run is: {TIMESTAMP_VALUE}
     - Create JSON with this EXACT structure: {\"report_timestamp\": \"{TIMESTAMP_VALUE}\", \"scan_timestamp\": \"{current ISO-8601 time}\", \"statistics\": {\"total_commands\": {count}, \"total_agents\": {count of all_agent_files}, \"agents_used_by_commands\": {count of agents_used_by_commands}, \"agents_called_by_agents\": {count of agents_called_by_agents}, \"orphan_agents_found\": {count of orphan_agents}, \"missing_agents_found\": {count of missing_agents}}, \"command_dependencies\": {command: [agents] mapping}, \"agent_dependencies\": {agent: [agents] mapping}, \"all_agents\": [complete list from STEP 1], \"agents_used_by_commands\": [list from STEP 2], \"agents_called_by_agents\": [list from STEP 3], \"orphan_agents\": [ONLY truly orphaned agents from STEP 5], \"missing_agents\": [list from STEP 4]}
     
     Use the timestamp {TIMESTAMP_VALUE} for your report
     Use the timestamp to name your report file.
     Save report to: .claude/report/{TIMESTAMP_VALUE}/dependency-mapper_report.json
     Example: .claude/report/20250903_220848/dependency-mapper_report.json"

2. **consistency-validator**: Check naming and path consistency
   - Description: "Check naming and path consistency"
   - Instructions: "Validate consistency across NOVELSYS-SWARM. Check naming conventions, path patterns, hardcoded values.
     Use the timestamp {TIMESTAMP_VALUE} for your report
     Use the timestamp to name your report file.
     Save report to: .claude/report/{TIMESTAMP_VALUE}/consistency-validator_report.json
     Example: .claude/report/20250903_220848/consistency-validator_report.json"

3. **filesystem-auditor**: Audit filesystem design  
   - Description: "Audit filesystem design"
   - Instructions: "Validate filesystem structure and I/O operations. Check path consistency and directory structure.
     Use the timestamp {TIMESTAMP_VALUE} for your report
     Use the timestamp to name your report file.
     Save report to: .claude/report/{TIMESTAMP_VALUE}/filesystem-auditor_report.json
     Example: .claude/report/20250903_220848/filesystem-auditor_report.json"

4. **compliance-checker**: Check Claude Code compliance
   - Description: "Check Claude Code compliance"
   - Instructions: "You are validating Claude Code compliance. Follow these EXACT steps:
     
     STEP 1: Check each agent file
     - Use Glob tool: `.claude/agents/*.md`
     - For each agent file: a) Extract filename: remove path and .md extension Example: .claude/agents/bible-architect.md  ->  bible-architect b) Use Read tool: read first 10 lines of file c) Extract 'name:' value from YAML (between --- markers) d) CRITICAL: Trim whitespace from both filename and name field e) Compare: if filename === name field  ->  PASS f) If different  ->  add to violations
     
     STEP 2: Validate YAML structure
     For each agent: Check has '---' at start and end of frontmatter, Check has 'name:' field, Check has 'description:' field, If missing  ->  add to violations
     
     STEP 3: Generate report
     - The timestamp for this run is: {TIMESTAMP_VALUE}
     - IMPORTANT: Only report ACTUAL mismatches
     - Example: if file=\"bible-architect.md\" and name=\"bible-architect\", this is CORRECT
     - Create JSON: {\"report_timestamp\": \"{TIMESTAMP_VALUE}\", \"scan_timestamp\": \"{current_time}\", \"statistics\": {\"agents_scanned\": {count}, \"total_violations\": {count}}, \"agent_violations\": [// ONLY include if name actually doesn't match filename], \"validation_notes\": \"Verified exact string matching with trimmed whitespace\"}
     
     Save to: .claude/report/{TIMESTAMP_VALUE}/compliance-checker_report.json"

5. **context-inspector**: Analyze context dependencies
   - Description: "Analyze context dependencies"  
   - Instructions: "You are analyzing context setup and prerequisites. Follow these steps:
     
     STEP 1: Analyze command context requirements
     - Use Glob tool: `.claude/commands/novel/*.md`
     - For each command: Extract initial Read operations (first 5 steps), Identify project.json, bible.yaml reads, Note what context files are required
     
     STEP 2: Analyze agent context requirements
     - Use Glob tool: `.claude/agents/*.md`
     - For each agent: Use Grep: 'Bible Reading Focus' with -A 10 for context, Extract what each agent needs from Bible, Identify required initial reads
     
     STEP 3: Map context flow
     - Track which commands create context files
     - Track which agents consume them
     - Identify context chains and dependencies
     
     STEP 4: Generate report
     - The timestamp for this run is: {TIMESTAMP_VALUE}
     - Create comprehensive JSON report with: command_context: prerequisites for each command, agent_context: Bible focus and required reads, context_chains: data flow through system, missing_validations: risky reads without checks
     
     Save to: .claude/report/{TIMESTAMP_VALUE}/context-inspector_report.json
     
     STEP 5: Generate Context Flow Diagram
     - Create visual representation of context flow in Markdown format
     - Show command  ->  context  ->  agent data flow
     - Map validation chains and prerequisite checks
     - Save to: .claude/report/{TIMESTAMP_VALUE}/context_flow_diagram.md
     - Use the same timestamp from Step 4"

6. **resource-analyzer**: Analyze resource utilization
   - Description: "Analyze resource utilization"
   - Instructions: "You are analyzing resource utilization. Follow these EXACT steps:
     
     STEP 1: Get all agent files
     - Use Glob tool: `.claude/agents/*.md`
     - Extract names (remove .md extension)
     - Exclude: \"base-agent-template\", \"AGENT_SAVE_INSTRUCTION\"
     - Store: all_agents = [list]
     
     STEP 2: Find ALL references to each agent
     For each agent in all_agents: Use Grep tool: pattern 'subagent_type[=:]\\s*\"{agent_name}\"' in .claude/commands/, Use Grep tool: pattern 'subagent_type[=:]\\s*\"{agent_name}\"' in .claude/agents/, CRITICAL: Pattern matches BOTH subagent_type=\"agent\" AND subagent_type: \"agent\", If ZERO matches in both: add to orphan_agents, If found: add to used_agents with location
     
     STEP 3: Verify each potential orphan (DOUBLE-CHECK)
     For each agent in orphan_agents: Use Grep tool again with pattern: agent_name in .claude/commands/novel/chapter-start.md, If found: REMOVE from orphan_agents, add to used_agents, Record confidence: HIGH if double-checked, MEDIUM if uncertain
     
     STEP 4: Generate report
     - The timestamp for this run is: {TIMESTAMP_VALUE}
     - Create JSON: {\"report_timestamp\": \"{TIMESTAMP_VALUE}\", \"scan_timestamp\": \"{current_time}\", \"statistics\": {\"total_agents\": {count}, \"orphan_agents\": {count}, \"total_hooks\": 0, \"unused_hooks\": 0}, \"orphan_agents\": [{\"file\": \"{name}.md\", \"confidence\": \"HIGH|MEDIUM\", \"reason\": \"No references found after double-check\"}], \"used_agents\": [list of agents that ARE referenced], \"verification_notes\": \"Double-checked all orphans with grep\"}
     
     Save to: .claude/report/{TIMESTAMP_VALUE}/resource-analyzer_report.json"

### Step 3: Wait for System Checkers to Complete

1. **Allow time for 6 system checkers to complete:**
   - Display: "⏳ 6 system checkers running in parallel..."
   - Use Bash tool: `sleep 10`  # Wait for 6 parallel system checkers
   - Display: "[x] System checkers phase complete"

2. **Verify system checker reports exist (MANDATORY):**
   - Use Bash tool: `PHASE1_SUCCESS=true; echo "=== Phase 1: System Checker Reports ==="; for agent in dependency-mapper consistency-validator filesystem-auditor context-inspector compliance-checker resource-analyzer; do if test -f ".claude/report/{TIMESTAMP_VALUE}/${agent}_report.json"; then echo "[x] ${agent} report exists"; else echo "[ ] Error: Missing ${agent} report"; PHASE1_SUCCESS=false; fi; done; if test -f ".claude/report/{TIMESTAMP_VALUE}/context_flow_diagram.md"; then echo "[x] Context flow diagram exists (from context-inspector)"; else echo "[ ] Error: Missing context_flow_diagram.md from context-inspector"; PHASE1_SUCCESS=false; fi; if [ "$PHASE1_SUCCESS" = false ]; then echo "[ ] Error: Phase 1 incomplete - cannot continue"; exit 1; else echo "[x] Phase 1 complete - all 6 checker reports and context diagram exist"; fi` (replace {TIMESTAMP_VALUE} with actual timestamp)

### Step 4: Dynamic Command Flow Analysis (Phase 2)

**Analyze execution flows for ALL commands with dynamic parallel execution:**

1. **Initialize flow analysis:**
   - Display: "=== Phase 2: Command Flow Analysis ==="
   - Display: "Using temp directory: .claude/temp/flow_{TIMESTAMP_VALUE}" (already created in Step 1)

2. **Scan and count all commands:**
   - Use Glob tool: `.claude/commands/novel/*.md`
   - Store the list of command files
   - Count total commands dynamically
   - Display: "Found {N} commands to analyze"

3. **Launch dynamic parallel command-flow-mappers:**
   
   **CRITICAL: You MUST launch ALL N command-flow-mapper agents in ONE message**
   
   For EACH command file found in step 2, include a Task call with:
   - **subagent_type**: "command-flow-mapper"
   - **description**: "Analyze {command-name} flow"
   - **prompt**: "Analyze the execution flow of this command.
     Command file: .claude/commands/novel/{command-name}.md
     Temp directory: .claude/temp/flow_{TIMESTAMP_VALUE}/
     
     Follow these steps:
     1. Read and parse the command file
     2. Extract all steps and agent calls (subagent_type patterns)
     3. For each agent found, read its file and find nested calls
     4. Build complete execution tree (max depth: 5)
     5. Calculate complexity metrics
     
     Save your analysis to: .claude/temp/flow_{TIMESTAMP_VALUE}/{command-name}.json
     Include: step breakdown, agent tree, complexity score, issues found"
   
   Display: "⏳ Launched {N} parallel flow mappers..."

4. **Wait and verify completion:**
   - Use Bash tool: `sleep 15`  # Wait for N parallel command mappers (typically 20+)
   - Verify completion with these separate commands:
     - Use Bash tool: `find .claude/commands/novel -name "*.md" -type f | wc -l`  # Count expected
     - Use Bash tool: `find .claude/temp/flow_{TIMESTAMP_VALUE} -name "*.json" -type f | wc -l`  # Count actual
     - Compare the counts and display status message

5. **Generate unified flow diagram:**
   
   Use Task tool with:
   - **subagent_type**: "flow-diagram-generator"
   - **description**: "Generate comprehensive flow diagram"
   - **prompt**: "Create a comprehensive system execution flow diagram.
     
     The timestamp for this run is: {TIMESTAMP_VALUE}
     Read ALL analysis reports from: .claude/temp/flow_{TIMESTAMP_VALUE}/*.json
     
     CRITICAL: You MUST include COMPLETE information from ALL JSON files:
     1. Full execution tree for EVERY command (not summaries)
     2. Complete agent dependency chains with depths
     3. All parallel/sequential execution patterns
     4. Every complexity metric and issue found
     5. Do NOT summarize or truncate any command's flow
     
     Build unified diagram showing:
     - Command Complexity Overview (grouped by high/medium/low)
     - COMPLETE Execution Flows for ALL commands (full trees)
     - Agent Dependency Graph (call frequencies, deep chains)
     - System-Wide Patterns (bottlenecks, unused agents)
     
     Include ASCII art visualizations and tree structures.
     Preserve ALL details from the individual JSON analyses.
     
     Save final report to: .claude/report/{TIMESTAMP_VALUE}/system_flow_diagram.md
     (The timestamp {TIMESTAMP_VALUE} has been provided above)"
   
   Display: "[x] Flow diagram generation complete"

6. **Verify flow diagram exists (MANDATORY):**
   - Use the TIMESTAMP value from Step 1
   - Use Bash tool: `if test -f .claude/report/{TIMESTAMP_VALUE}/system_flow_diagram.md; then echo "[x] Phase 2 complete - Flow diagram exists"; else echo "[ ] Error: Phase 2 incomplete - Flow diagram missing"; exit 1; fi`

### Step 5: Deep Execution Safety Analysis (Phase 2.5)

**Launch 3 parallel deep analyzers for execution safety:**

1. **Display phase initiation:**
   - Display: "=== Phase 2.5: Deep Execution Safety Analysis ==="
   - Display: "⏳ Launching 3 parallel safety analyzers..."
   - Display: "Analyzing file dependencies, conditional logic, and parallel safety..."

2. **Execute ALL 3 safety analyzers in PARALLEL (ONE message with 3 Task calls):**

   **Task 1 - File Dependency Tracer:**
   - subagent_type: "file-dependency-tracer"
   - description: "Trace file I/O dependencies"
   - prompt: "Analyze file dependencies for chapter-start command.
     
     Command file: .claude/commands/novel/chapter-start.md
     Report path: .claude/report/{TIMESTAMP_VALUE}/file-dependency-tracer_report.json
     
     CRITICAL TASKS:
     1. Extract ALL file read/write operations from each step
     2. Trace the evolution chain (draft_v1  ->  v2  ->  v3 etc)
     3. Build complete dependency graph showing which steps MUST be sequential
     4. Identify TRUE parallel opportunities (no shared files)
     5. Detect FALSE parallel claims from previous analyses
     
     Focus especially on:
     - Steps 4-7: Are they REALLY parallelizable?
     - Steps 13-14: Check conditional dependency
     - File transformation chains
     
     Save detailed analysis to the report path above."

   **Task 2 - Conditional Logic Analyzer:**
   - subagent_type: "conditional-logic-analyzer"
   - description: "Analyze conditional execution"
   - prompt: "Analyze conditional logic in chapter-start command.
     
     Command file: .claude/commands/novel/chapter-start.md
     Report path: .claude/report/{TIMESTAMP_VALUE}/conditional-logic-analyzer_report.json
     
     CRITICAL TASKS:
     1. Find ALL IF/THEN conditions and quality gates
     2. Map execution paths (success, failure, error)
     3. Identify conditional dependencies between steps
     4. Special focus on Step 13-14 relationship (score >= 95)
     5. Find all STOP conditions and early terminations
     
     Document how conditions affect parallelization possibilities.
     Save detailed analysis to the report path above."

   **Task 3 - Parallel Safety Validator:**
   - subagent_type: "parallel-safety-validator"
   - description: "Validate parallel execution safety"
   - prompt: "Validate ALL parallelization claims for chapter-start command.
     
     Command file: .claude/commands/novel/chapter-start.md
     Report path: .claude/report/{TIMESTAMP_VALUE}/parallel-safety-validator_report.json
     
     CRITICAL TASKS:
     1. Load file dependency analysis if available
     2. Load conditional logic analysis if available
     3. VALIDATE every parallel claim (especially Steps 4-7 and 13-14)
     4. Check for race conditions and file conflicts
     5. Provide DEFINITIVE verdict on what can ACTUALLY parallelize
     
     Be CONSERVATIVE - mark UNSAFE if any doubt exists.
     Previous analyses incorrectly claimed Steps 4-7 can parallelize.
     Save detailed validation to the report path above."

3. **Wait and verify completion:**
   - Display: "Waiting for safety analyzers to complete..."
   - Use Bash tool: `sleep 8`  # Wait for 3 parallel analyzers
   
4. **Verify safety analysis reports exist:**
   - Use Bash tool: `PHASE25_SUCCESS=true; echo "=== Verifying Phase 2.5 Reports ==="; for analyzer in file-dependency-tracer conditional-logic-analyzer parallel-safety-validator; do if test -f ".claude/report/{TIMESTAMP_VALUE}/${analyzer}_report.json"; then echo "[x] ${analyzer} report exists"; else echo "[ ] Warning: Missing ${analyzer} report"; PHASE25_SUCCESS=false; fi; done; if [ "$PHASE25_SUCCESS" = true ]; then echo "[x] Phase 2.5 complete - all safety analyses exist"; else echo "WARNING:️ Phase 2.5 partially complete - some analyses missing"; fi`

### Step 6: Claude Code Deep Compliance Analysis (Phase 3)

**Launch 3 parallel claude-code-expert compliance checkers:**

1. **Display phase initiation:**
   - Display: "=== Phase 3: Claude Code Deep Compliance Analysis ==="
   - Display: "⏳ Launching 3 parallel compliance analyzers..."

2. **Execute ALL 3 compliance checks in PARALLEL (ONE message with 3 Task calls):**

   **Task 1 - Commands Compliance:**
   - subagent_type: "claude-code-expert"
   - description: "Deep scan commands compliance"
   - prompt: "Execute deep compliance scan for NOVELSYS-SWARM commands.
     
     TARGET: .claude/commands/novel/*.md
     
     CHECKING:
     1. Variable format: Must be **$ARGUMENTS** not {$ARGUMENTS}
     2. Error message format: Must be '[ ] Error:' not standalone '[ ]'
     3. Warning format: Must be 'WARNING:️ Warning:' not standalone 'WARNING:️'
     4. Description field: 5-10 words, starts with verb, concise
     5. Argument-hint completeness and format
     6. Shell cross-platform compatibility (no Windows-specific commands)
     7. Python pseudo-code detection (commands should use instructional text)
     8. Task parallel execution patterns (all Tasks in one message)
     
     PROCESS:
     1. CRITICAL: Use this timestamp: {TIMESTAMP_VALUE}
     2. MUST use that exact timestamp for filename - DO NOT generate your own timestamp
     3. Scan each command file systematically
     4. Record all violations with file, line number, and fix
     5. Calculate compliance score (100 - violations*2)
     
     OUTPUT: .claude/report/{TIMESTAMP_VALUE}/claude-code-expert-commands_report.json
     EXAMPLE: .claude/report/20250906_122851/claude-code-expert-commands_report.json
     
     FORMAT:
     {
       'report_timestamp': '{TIMESTAMP_VALUE}',
       'scan_timestamp': '{current ISO time}',
       'files_scanned': {count},
       'total_violations': {count},
       'compliance_score': {0-100},
       'violations_by_type': {
         'variable_format': [{file, line, current, expected}],
         'error_format': [...],
         'python_code': [...],
         'shell_compatibility': [...]
       },
       'critical_issues': ['Python code in commands', 'Broken parallel patterns'],
       'recommendations': ['Fix all variable formats', 'Remove Python code']
     }"

   **Task 2 - Agents Compliance:**
   - subagent_type: "claude-code-expert"
   - description: "Deep scan agents compliance"
   - prompt: "Execute deep compliance scan for NOVELSYS-SWARM agents.
     
     TARGET: .claude/agents/*.md
     
     CHECKING:
     1. YAML frontmatter format and completeness
     2. Name field matches filename exactly
     3. Description format (proper triggers, concise)
     4. Proactive mode usage (only 1-3 agents should use)
     5. Tools field specification
     6. Variable references in agent content
     7. Error message formats in agent outputs
     
     PROCESS:
     1. CRITICAL: Use this timestamp: {TIMESTAMP_VALUE}
     2. MUST use that exact timestamp for filename - DO NOT generate your own timestamp  
     3. Scan each agent file systematically
     4. Verify YAML between --- markers
     5. Check name/filename consistency
     6. Count proactive agents (should be <=3)
     
     OUTPUT: .claude/report/{TIMESTAMP_VALUE}/claude-code-expert-agents_report.json
     EXAMPLE: .claude/report/20250906_122851/claude-code-expert-agents_report.json
     
     FORMAT:
     {
       'report_timestamp': '{TIMESTAMP_VALUE}',
       'scan_timestamp': '{current time}',
       'agents_scanned': {count},
       'total_violations': {count},
       'compliance_score': {0-100},
       'proactive_agents': {count},
       'violations': [
         {'file': 'agent.md', 'type': 'yaml_format', 'issue': '...', 'fix': '...'}
       ],
       'name_mismatches': [],
       'recommendations': []
     }"

   **Task 3 - Architecture Patterns:**
   - subagent_type: "claude-code-expert"
   - description: "Scan architecture patterns compliance"
   - prompt: "Execute architecture pattern compliance scan for NOVELSYS-SWARM.
     
     CHECKING:
     1. Parallel execution patterns (Task calls in single message)
     2. Agent call chains (depth, circular references)
     3. Hardcoded paths vs dynamic paths
     4. Cross-platform patterns
     5. Best practices adherence
     6. Resource efficiency patterns
     
     PROCESS:
     1. CRITICAL: Use this timestamp: {TIMESTAMP_VALUE}
     2. MUST use that exact timestamp for filename - DO NOT generate your own timestamp
     3. Analyze command  ->  agent  ->  agent chains
     4. Detect anti-patterns (sequential Tasks, deep nesting)
     5. Find hardcoded project paths
     6. Evaluate architecture score
     
     OUTPUT: .claude/report/{TIMESTAMP_VALUE}/claude-code-expert-architecture_report.json
     EXAMPLE: .claude/report/20250906_122851/claude-code-expert-architecture_report.json
     
     FORMAT:
     {
       'report_timestamp': '{TIMESTAMP_VALUE}',
       'scan_timestamp': '{current time}',
       'architecture_score': {0-100},
       'patterns_found': {
         'good_patterns': ['Proper Task parallelization', ...],
         'anti_patterns': ['Sequential Task calls', ...]
       },
       'hardcoded_paths': [{file, line, path}],
       'call_chain_issues': ['Circular: A -> B -> A', 'Deep: 7 levels'],
       'recommendations': ['Fix parallel patterns', 'Remove hardcoding']
     }"

3. **Wait for completion and verify (MANDATORY):**
   - Use Bash tool: `sleep 10`  # Wait for 3 parallel compliance checkers
   - Use Bash tool: `PHASE3_SUCCESS=true; echo "=== Phase 3: Deep Compliance Reports ==="; for report in claude-code-expert-commands claude-code-expert-agents claude-code-expert-architecture; do if test -f ".claude/report/{TIMESTAMP_VALUE}/${report}_report.json"; then echo "[x] ${report} report exists"; else echo "[ ] Error: Missing ${report} report"; PHASE3_SUCCESS=false; fi; done; if [ "$PHASE3_SUCCESS" = false ]; then echo "[ ] Error: Phase 3 incomplete - cannot generate final report"; echo "System check FAILED - missing critical compliance reports"; exit 1; fi; echo "[x] Phase 3 complete - all compliance reports generated"`

### Step 7: Novel Creation Capability Assessment (Phase 4)

**Evaluate system's readiness for 95-point quality novel creation:**

1. **Display phase initiation:**
   - Display: "=== Phase 4: Novel Creation Capability Assessment ==="
   - Display: "⏳ Analyzing system's ability to produce 95-point quality novels..."

2. **Launch novel quality process auditor (AFTER Phase 3 completes):**

Use Task tool with:
- **subagent_type**: "novel-quality-process-auditor"
- **description**: "Audit novel creation capability"
- **prompt**: "Evaluate NOVELSYS-SWARM's capability to produce 95-point quality novels.

  System report paths:
  - Main reports: .claude/report/{TIMESTAMP_VALUE}/
  - Flow analysis: .claude/temp/flow_{TIMESTAMP_VALUE}/
  - Project data: .claude/data/
  
  Key analysis files:
  - System health: (will be generated after this phase completes)
  - Dependencies: .claude/report/{TIMESTAMP_VALUE}/dependency-mapper_report.json
  - Resources: .claude/report/{TIMESTAMP_VALUE}/resource-analyzer_report.json
  - Chapter flow: .claude/temp/flow_{TIMESTAMP_VALUE}/chapter-start.json
  - Quality flow: .claude/temp/flow_{TIMESTAMP_VALUE}/quality-check-individual.json
  
  Analysis requirements:
  
  STEP 1: Detect System State
  - Check for existing projects in .claude/data/projects/
  - Check for generated chapters with quality reports
  - Determine current state:
    * not_started: No projects or chapters exist
    * test_phase: Test chapters exist from system testing
    * active_creation: Real novel generation in progress
  
  STEP 2: Evaluate Based on State
  
  For not_started state:
  - Assess system readiness and configuration
  - Review quality standards setup
  - Check agent capabilities
  - Report: System Ready/Not Ready for 95-point creation
  
  For test_phase state:
  - Analyze test chapter quality scores
  - Identify patterns in test results
  - Extract lessons from testing
  - Project capability for real creation
  
  For active_creation state:
  - Analyze actual quality scores achieved
  - Identify specific bottlenecks
  - Compare against 95-point target
  - Provide improvement roadmap
  
  STEP 3: Benchmark Against Standards
  - Compare with Western bestseller standards
  - Evaluate against Harry Potter/LOTR elements
  - Check Brandon Sanderson techniques
  - Assess Stephen King principles
  
  STEP 4: Generate Assessment Report
  
  Save comprehensive report to: .claude/report/{TIMESTAMP_VALUE}/novel_creation_capability.md
  
  Report structure:
  - System State: {not_started/test_phase/active_creation}
  - Readiness Assessment: {Ready/Not Ready with reasons}
  - Capability Projection: {expected quality range}
  - Gap Analysis: {distance to 95-point goal}
  - Improvement Roadmap: {specific actionable steps}
  - Success Probability: {percentage with confidence level}
  
  IMPORTANT: Do NOT report system failure for not_started state.
  Instead report: System configured and ready for novel creation."

3. **Wait for Phase 4 completion and verify (MANDATORY):**
   - Use Bash tool: `sleep 10`  # Wait for novel quality auditor
   - Use Bash tool: `if test -f .claude/report/{TIMESTAMP_VALUE}/novel_creation_capability.md; then echo "[x] Phase 4 complete - Novel capability assessed"; else echo "[ ] Error: Phase 4 incomplete - Capability assessment missing"; exit 1; fi`

### Step 8: Generate Final Aggregated Report

**PRE-CONDITION: Verify ALL 15 reports exist before proceeding:**

1. **Mandatory verification of all 15 prerequisite reports:**
   - Use Bash tool: `echo "=== Verifying all 15 required prerequisite reports ==="`
   - Use Bash tool: `ALL_PRESENT=true; MISSING_COUNT=0; for report in dependency-mapper_report.json consistency-validator_report.json filesystem-auditor_report.json context-inspector_report.json compliance-checker_report.json resource-analyzer_report.json context_flow_diagram.md system_flow_diagram.md file-dependency-tracer_report.json conditional-logic-analyzer_report.json parallel-safety-validator_report.json claude-code-expert-commands_report.json claude-code-expert-agents_report.json claude-code-expert-architecture_report.json novel_creation_capability.md; do if ! test -f ".claude/report/{TIMESTAMP_VALUE}/${report}"; then echo "[ ] Error: Missing required report: ${report}"; ALL_PRESENT=false; MISSING_COUNT=$((MISSING_COUNT + 1)); fi; done; echo "Total reports found: $((15 - MISSING_COUNT))/15"`
   - Use Bash tool: `if [ "$ALL_PRESENT" = false ]; then echo "[ ] FATAL: Cannot generate final report - missing dependencies"; echo "System check INCOMPLETE"; echo "System Check Failed at $(date)" > ".claude/report/{TIMESTAMP_VALUE}/INCOMPLETE_ERROR.txt"; echo "Run individual phase checks to diagnose" >> ".claude/report/{TIMESTAMP_VALUE}/INCOMPLETE_ERROR.txt"; exit 1; fi; echo "[x] All 15 prerequisite reports verified"; echo "⏳ Generating final aggregated report..."`

2. **Launch the final health report generator:**

When you reach this step, you MUST use Task tool with:
- **subagent_type**: "system-health-reporter"  
- **description**: "Aggregate results and generate final report"
- **prompt**: "You are generating the final health report. Follow these EXACT steps:
  
  STEP 1: Get timestamp
  - The timestamp for this run is: {TIMESTAMP_VALUE}
  - Store timestamp for use in filenames
  
  STEP 2: Read all checker reports and diagrams (15 total - MANDATORY)
  - Read: `.claude/report/{TIMESTAMP_VALUE}/dependency-mapper_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/consistency-validator_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/filesystem-auditor_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/context-inspector_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/compliance-checker_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/resource-analyzer_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/context_flow_diagram.md`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/system_flow_diagram.md`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/file-dependency-tracer_report.json` (NEW - Phase 2.5)
  - Read: `.claude/report/{TIMESTAMP_VALUE}/conditional-logic-analyzer_report.json` (NEW - Phase 2.5)
  - Read: `.claude/report/{TIMESTAMP_VALUE}/parallel-safety-validator_report.json` (NEW - Phase 2.5)
  - Read: `.claude/report/{TIMESTAMP_VALUE}/claude-code-expert-commands_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/claude-code-expert-agents_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/claude-code-expert-architecture_report.json`
  - Read: `.claude/report/{TIMESTAMP_VALUE}/novel_creation_capability.md` (MANDATORY)
  
  CRITICAL: If ANY report is missing:
  - Write error to: `.claude/report/{TIMESTAMP_VALUE}/INCOMPLETE_ERROR.txt`
  - List all missing reports
  - DO NOT generate health report
  - Return with error: 'System check incomplete - missing {N} reports'"
  
  STEP 3: Validate and reconcile data (CRITICAL)
  
  3.1 Missing Agents Validation:
  - If dependency-mapper says agent X is missing
  - But X appears in dependency-mapper's command_dependencies
  - Then X is NOT missing (remove from missing list)
  
  3.2 Orphan Agents Validation:
  - Compare dependency-mapper orphans vs resource-analyzer orphans
  - If counts differ significantly (>3 difference): Trust resource-analyzer (it double-checks), Note discrepancy in report
  - Final orphans = agents that BOTH reports agree are orphans
  
  3.3 Name Mismatch Validation:
  - Only include if compliance-checker reports with high confidence
  - Cross-reference with claude-code-expert-agents report
  - If both agree  ->  HIGH confidence
  - If only one reports  ->  MEDIUM confidence
  - Exclude common false positives (bible-architect, etc)
  
  3.4 Deep Compliance Validation (NEW):
  - Merge findings from compliance-checker and claude-code-expert reports
  - Priority: claude-code-expert findings (more detailed)
  - Check for Python pseudo-code (critical issue)
  - Verify Task parallel patterns
  - Validate variable formats across all files
  
  3.5 Parallel Safety Override (CRITICAL NEW):
  - Read parallel-safety-validator report (AUTHORITATIVE)
  - Read file-dependency-tracer report (file dependencies)
  - Read conditional-logic-analyzer report (conditional logic)
  - OVERRIDE any previous parallel claims with safety validator verdict:
    * If parallel-safety-validator says UNSAFE  ->  IT IS UNSAFE (no exceptions)
    * If file dependencies show chain (v1 -> v2 -> v3)  ->  MUST BE SEQUENTIAL
    * If conditional dependency exists  ->  CANNOT BE PARALLEL
  - Replace ALL parallel recommendations from Phase 1-3 with Phase 2.5 findings
  - Trust order: parallel-safety-validator > file-dependency-tracer > conditional-logic-analyzer > others
  - Document all overrides in report with evidence
  
  STEP 4: Calculate health score
  Base score = 100
  - Subtract 10 for each VERIFIED missing agent
  - Subtract 2 for each CONFIRMED orphan agent
  - Subtract 5 for each naming violation
  - Subtract 3 for hardcoded paths (if >50)
  - Subtract 15 for Python pseudo-code presence (CRITICAL)
  - Subtract 10 for broken Task parallel patterns
  - Subtract 5 for inconsistent variable formats
  - Subtract 3 for non-standard descriptions
  - Subtract 2 for each missing argument-hint
  
  Minimum score: 0 (cannot go negative)
  
  STEP 5: Generate report structure
  Create markdown with ENHANCED sections:
  - Report timestamp prominently at top
  - Executive Summary (key findings from all 15 reports)
  - System Health Score with detailed breakdown
  - Context Flow Visualization
  - System Execution Flows
  - Claude Code Deep Compliance Analysis (NEW section):
    * Commands Compliance ({score}/100)
    * Agents Compliance ({score}/100)
    * Architecture Patterns ({score}/100)
    * Critical violations (Python code, broken patterns)
  - Dependency Relationships (blood vessel diagram)
  - Issues by Category:
    * Critical Issues (Python code, broken parallelization)
    * Context Issues (missing prerequisites, broken chains)
    * System Issues (over-triggered, security concerns)
    * Dependency Issues (circular, missing)
    * Consistency Issues (naming, paths)
    * Compliance Issues (format violations)
  - Confidence indicator (HIGH if all 3 compliance reports agree)
  - When reports disagree, show all values with confidence levels
  - Recommendations prioritized by severity (Critical  ->  High  ->  Medium  ->  Low)
  
  STEP 6: Save reports
  - Save main report to: `.claude/report/{TIMESTAMP_VALUE}/system_health_report.md`
  
  IMPORTANT:
  - If agent appears in command_dependencies, it's NOT missing
  - If only one checker reports an issue, mark as \"Needs verification\"
  - Always show confidence level for findings"

### Step 9: Display Results

1. **Check if reports were generated:**
   - Use the TIMESTAMP value from Step 1
   - Use Bash tool: `test -f .claude/report/{TIMESTAMP_VALUE}/system_health_report.md && echo "[x] Main report exists" || echo "WARNING:️ Warning: Main report missing"`
   - Use Bash tool: `test -f .claude/report/{TIMESTAMP_VALUE}/system_flow_diagram.md && echo "[x] Flow diagram exists" || echo "WARNING:️ Warning: Flow diagram missing"`

2. **Display comprehensive report:**
   - Use the TIMESTAMP value from Step 1
   - Use Read tool: `.claude/report/{TIMESTAMP_VALUE}/system_health_report.md`
   - Show full content to user

3. **Quick summary for user:**
   ```
   === System Health Check Complete ===

   Phase 1: 6 system checkers - COMPLETE (6 JSON + 1 MD diagram)
   Phase 2: Flow mapping analysis - COMPLETE (1 MD diagram)
   Phase 3: Deep compliance analysis - COMPLETE (3 JSON)
   Phase 4: Novel capability assessment - COMPLETE (1 MD)
   
   Reports generated in: .claude/report/{TIMESTAMP_VALUE}/
   
   Prerequisite reports (12 total):
   - 9 JSON reports (6 system + 3 compliance)
   - 3 MD reports (context diagram, flow diagram, novel capability)
   
   Final report:
   - system_health_report.md (aggregated analysis)
   
   Total files: 13 (12 prerequisites + 1 final)
   
   Note: Analysis files preserved in .claude/temp/ for debugging
   All reports include timestamp for tracking
   ```

## Expected Output Structure

The coordinator will generate a report with:

```markdown
# NOVELSYS-SWARM System Health Report

Generated: {TIMESTAMP_VALUE}

## System Relationship Map (Blood Vessel Diagram)

[ASCII art showing complete dependency tree]

## Health Score: XX/100

## Critical Issues (Must Fix)
- [Issue 1 with specific fix]
- [Issue 2 with specific fix]

## Recommendations by Priority
...

## What's Working Well
...
```

## Error Handling

- If any phase fails: System check marked INCOMPLETE
- Missing reports logged to: .claude/report/{TIMESTAMP_VALUE}/INCOMPLETE_ERROR.txt
- No partial final report allowed - all 12 prerequisites required
- User must fix issues and re-run entire check
- Check individual JSON reports for debugging

## Success Criteria

- Phase 1: All 6 system checker reports + 1 context diagram generated [x]
- Phase 2: All command flows analyzed + 1 flow diagram generated [x]
- Phase 3: All 3 Claude Code compliance reports generated [x]
- Phase 4: Novel creation capability assessment generated [x]
- Total prerequisite reports: 12 (ALL MANDATORY)
- Final report: Generated ONLY if all 12 exist [x]
- Total files created: 13 (12 prerequisites + 1 final health report)
- Multi-dimensional assessment with technical and creative metrics
- Clear visualizations and actionable recommendations
- ANY missing report = SYSTEM CHECK FAILURE

## Notes

- Run weekly during development
- Run before major refactoring
- Run after adding new agents/commands
- All reports include timestamps for historical tracking
- Output directory: `.claude/report/` (flat structure)
- Total expected files: 13 (12 reports + 1 final health report)
- Consider archiving old reports periodically

### Step 10: Display Final Summary

Display completion message with multi-dimensional assessment:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[x] System Health Check Complete

Report saved to: .claude/report/{TIMESTAMP_VALUE}/

System Assessment:
+--------------------------------------+
| Technical Health:     {score}/100    |
| Creation Readiness:   {status}       |
| Content Status:      {state}         |
| Quality Capability:   {range}        |
+--------------------------------------+

View detailed reports in report directory.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```