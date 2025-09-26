# CLAUDE.md - NOVELSYS-SWARM Project Memory v6.7 RECURSION-SAFE + TRIGGER-WORD-AWARE + COORDINATOR-TOOL-RESTRICTED

## CRITICAL UNICODE RESTRICTION

**ALL system components (commands, coordinators, agents, scripts) MUST NOT contain ANY Unicode characters:**
- NO emojis, special arrows, checkmarks, crosses, or any non-ASCII symbols
- Windows encoding errors occur with Unicode: 'charmap' codec can't encode character
- Use ASCII-only alternatives:
  - Instead of checkmark/cross: use YES/NO or [x]/[ ]
  - Instead of arrows: use -> or |
  - Instead of emojis: use text descriptions
  - Instead of special symbols: use standard ASCII characters

## Critical Discovery: The Truth About Recursion (2025-09-12)

### Core Truth: Root Cause of Recursion
```yaml
Recursion crash pattern:
  Wrong: Subagent(with Task) -> Task -> Another Subagent -> Task -> CRASH
  Root cause: Coordinators are subagents, giving them Task causes recursion

Correct architecture:
  Main Claude: Only orchestrator with Task tool
  Coordinators: No Task tool, only return execution plans
  Agents: No Task tool, only execute single tasks
  Result: Recursion impossible!
```

### Complete Five-Layer Architecture
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

### Why File System Layer is Critical
```python
# Without file system = recursion crash
Agent A(Task) -> Agent B(Task) -> Agent C -> CRASH

# With file system = recursion impossible
Agent A -> Write -> file.json
                      |
Agent B -> Read -> file.json -> Write -> result.json
```
File I/O breaks the synchronous call chain!

## Key Rules to Prevent Recursion

### Tool Configuration Rules
```yaml
Main Claude:
  tools: [all tools including Task]

Coordinators:
  tools: [Read, Write, Grep]  # NEVER Task or Bash! Planning only.

Agents:
  tools: [only task-specific, NEVER Task]
  # Available tools: Read, Write, Edit, Bash, Grep, WebSearch, WebFetch, Glob, etc.
  # Choose ANY tools needed - ONLY restriction is NO Task tool
```

### Call Pattern Rules
- Correct: Main Claude -> Task -> Subagent
- Wrong: Subagent -> Task -> Another Subagent (recursion!)

### Coordinator Rules
- Only return JSON execution plans
- Never execute Task calls
- Never attempt to call other agents
- Use natural language to describe requirements, not Task() pseudocode

## NEW: Coordinator Tool Restriction Discovery (2025-09-26)

### Real-World Problem: Coordinator Self-Execution
**NOVELSYS-SWARM Discovery**: When coordinators have Bash tool, they self-execute instead of planning:

```yaml
Problem Pattern:
  Coordinator with Bash -> Tries to run commands directly
  Result: Bypasses Main Claude orchestration
  Impact: Breaks architectural separation, causes confusion

Example Violation:
  Step 3: "Run bash command to create directory structure"
  Wrong: Coordinator executes directly
  Correct: Plan specifies agents to create structure
```

### Three-Layer Prevention Strategy

#### Layer 1: Tool Restriction (Physical Prevention)
```yaml
Coordinator Tools:
  ALLOWED: [Read, Write, Grep]
  FORBIDDEN: [Bash, Task]

Why Bash is Forbidden:
  - Read: Gather context for planning (safe)
  - Write: Create JSON plans (safe)
  - Grep: Search content for planning (safe)
  - Bash: Enables self-execution (DANGEROUS!)
```

#### Layer 2: Architectural Role Clarity
```yaml
Coordinator Role:
  - Strategic planning brain
  - Context analysis and decisions
  - JSON plan generation
  - NO direct execution

Agent Role:
  - Tactical execution hands
  - Single-task specialists
  - Direct file/system operations
  - CAN have Bash for execution
```

#### Layer 3: Documentation Enforcement
```yaml
Templates Specify:
  - Coordinator templates: Explicit tool restrictions
  - Architecture docs: Explain why separation matters
  - Best practices: Clear role boundaries
  - Training examples: Show correct patterns
```

### Official vs NOVELSYS-SWARM Standards
```yaml
Official Claude Code:
  - No special "coordinator" category defined
  - Tools assigned based on component purpose
  - Generic subagent model

NOVELSYS-SWARM Custom Architecture:
  - Distinct coordinator role created through convention
  - Tool restrictions enforced for role separation
  - Three-layer prevention strategy
  - Proven through production experience
```

### Historical Context: Why This Rule Exists
```yaml
Timeline:
  2025-09-12: Discovered recursion prevention
  2025-09-15: Implemented coordinator/agent separation
  2025-09-26: Identified coordinator self-execution problem

Root Cause:
  Coordinators with Bash try to "help" by executing
  This breaks the clean separation we need
  Tool restriction physically prevents this
```

### Coordinator JSON Plan Best Practices
1. **Never use Read tool on directories** - Will fail with EISDIR error
2. **Generate actual timestamps** - Don't use placeholders like {timestamp}
3. **Don't include file validation** - Assume paths are valid
4. **Coordinator should generate timestamps**:
   ```javascript
   // In coordinator's plan generation:
   const timestamp = new Date().toISOString().replace(/[-:T]/g, '').slice(0,14);
   // Result: "20250914151203"
   ```
5. **No bash tasks in JSON plans** - Main Claude cannot execute bash from JSON
6. **Use relative paths** - Let agents handle path resolution

### Windows Path Handling Rules (CRITICAL)
```yaml
Problem: Backslashes in Bash commands are escape characters

WRONG (will fail):
  Bash: ls -la "D:\NOVELSYS-SWARM\.claude\testing\*.json"
  # \N, \. are interpreted as escape sequences

CORRECT approaches:
  1. Relative paths (BEST):
     Bash: ls -la .claude/testing/*.json

  2. Forward slashes:
     Bash: ls -la "D:/NOVELSYS-SWARM/.claude/testing/*.json"

  3. Double backslashes (less readable):
     Bash: ls -la "D:\\NOVELSYS-SWARM\\.claude\\testing\\*.json"

Golden Rule: Always use relative paths when possible
```

## Architecture Layers

### Commands Layer (User Interface)
- **Unicode**: MUST NOT contain any Unicode characters
- **Length**: <100 lines TARGET (business completeness takes priority)
- **Acceptable range**: 50-120 lines when business context requires
- **Content**: Delegation with necessary business context
- **Pattern**: Declarative, preserving critical workflow information
- **Example**: "Use the chapter-start-coordinator subagent to orchestrate..."
- **Current status**: All commands within acceptable range (max 97 lines)

### Main Claude Layer (Central Orchestrator)
- **Tools**: All tools including Task
- **Role**: Read Command, decide execution strategy, translate plans to safe prompts
- **Pattern**: Parallel/serial scheduling of subagents
- **Key**: Only entity that can call subagents
- **Hidden responsibility**: Avoid trigger words when calling Task tool (e.g., transform file names to descriptions)

### Coordinators Layer (Planning)
- **Unicode**: MUST NOT contain any Unicode characters
- **Location**: MUST be in `.claude/agents/` folder (Claude Code requirement)
- **Length**: <250 lines optimal
- **Tools**: Read, Write, Grep (NO Task or Bash!)
- **Role**: Analyze requirements, return JSON execution plan
- **Output**: Mandatory JSON format execution plan
- **Key**: Are subagents (special type), cannot call other subagents
- **Critical**: Tool restriction prevents self-execution (learned 2025-09-26)
- **Status**: All 21 coordinators correctly return JSON plans (verified 2025-09-13)

### Agents Layer (Task Execution)
- **Unicode**: MUST NOT contain any Unicode characters
- **Length**: <500 lines complex, <200 lines preferred
- **Tools**: Only task-specific (NO Task!)
  - Must include all tools needed for the task
  - Common combinations: Read+Write, Read+Write+Bash, Read+Glob+Grep
  - Write tool automatically creates directories (no separate mkdir needed)
- **Role**: Execute single specific task
- **Communication**: Only through file system
- **Key**: Focus on execution, not coordination
- **Issues found**: Most agents correct, few over-length

### Data/File System Layer (Communication Foundation)
- **Purpose**: Key layer preventing recursion
- **Pattern**: File I/O replaces function calls
- **Benefits**: Supports parallelism, debuggable, no recursion
- **Principles**: Atomic operations, clear ownership

## Execution Patterns

### Parallel Execution
```python
Main Claude:
  Task -> Agent A
  Task -> Agent B  # Execute simultaneously
  Task -> Agent C
```

### Serial Execution
```python
Main Claude:
  Task -> Agent A -> wait
  Task -> Agent B -> wait
  Task -> Agent C
```

### Hybrid Mode
```python
Main Claude:
  Phase 1: Task -> [A, B, C] parallel
  Wait for all to complete
  Phase 2: Task -> D serial
  Phase 3: Task -> [E, F] parallel
```

### Multi-Coordinator Pattern (Tested & Verified)
```python
Main Claude:
  Phase 1: Task -> Coordinator A (returns plan)
           Execute agents from Plan A
           Save outputs to files

  Phase 2: Task -> Coordinator B (uses Phase 1 outputs)
           Execute agents from Plan B
           Final results

Key: Coordinators communicate through Main Claude + file system
```

### Sequential Pipeline Pattern (Tested & Verified)
```python
Main Claude:
  Stage 1: Task -> Generator Agent -> output1.json
  Verify: Check output1.json exists

  Stage 2: Task -> Transformer Agent(reads output1) -> output2.json
  Verify: Check output2.json exists

  Stage 3: Task -> Analyzer Agent(reads output2) -> final.json

Key: Each stage validates previous output before proceeding
```

### Human-in-Loop Pattern (Tested & Verified, Updated v6.5)
```python
Main Claude:
  Stage 1: Task -> Content Draft Agent -> draft.json
           Display draft with standard options:
           "1) Approve  2) Modify"
           "Enter choice [1/2]:"

  Human Decision Point:
    If choice = 1: Continue to next stage
    If choice = 2: Collect feedback -> regenerate -> display again
    (Infinite modify loop until user chooses Approve)

  Stage 2: Task -> Content Enhancer Agent -> enhanced.json
           Display with same standard choice format

  Human Decision Point:
    Same pattern - numeric choice, modify until satisfied

Key: Simplified two-option format with numeric input
Verified: approve/modify flows with infinite revision capability
Pattern: Display -> Choice[1/2] -> [Continue OR Modify->Loop]
```

### Coordinator JSON Plan Best Practices (Lessons Learned)

When coordinators return JSON execution plans:

1. **Use actual values, not placeholders**:
   ```json
   WRONG: "path": ".claude/report/{timestamp}/output.json"
   RIGHT: "path": ".claude/report/20250114_153045/output.json"
   ```

2. **No bash tasks in plans** (Main Claude cannot execute):
   ```json
   WRONG: {"type": "bash", "command": "mkdir -p directory"}
   RIGHT: Let agents handle directory creation with Write tool
   ```

3. **Agent task structure**:
   ```json
   {
     "agent": "system-scanner",
     "inputs": {
       "output_path": ".claude/report/20250114_153045/scan.json"
     }
   }
   ```

4. **Coordinator should generate timestamps**:
   ```python
   # In coordinator thinking/logic:
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   # Use this actual timestamp in all paths
   ```

### Advanced I/O Patterns (Tested & Verified)

#### Atomic Write Pattern (File Lock Mechanism)
```python
# Tested & Verified: Prevents corruption during concurrent writes
Agent writes:
  1. Write(content -> file.tmp)  # Write to temp file
  2. Bash("mv file.tmp file")    # Atomic rename (OS-level)

Key: mv operation is atomic at OS level, prevents partial writes
Verified: No corruption even with parallel writers
```

#### Producer-Consumer Pattern
```python
Main Claude:
  Task -> Producer Agent -> shared_queue.json (append mode)
  Task -> Consumer Agent -> reads shared_queue.json

Key: Atomic writes prevent corruption
Verified: Queue integrity maintained under load
```

#### Shared Reference Pattern
```python
Main Claude:
  Task -> Reference Creator -> reference.json
  Task -> [Reader A, Reader B, Reader C] parallel

Key: Multiple readers, single writer
Verified: No read conflicts with concurrent access
```

#### Version Control Pattern
```python
Main Claude:
  Task -> Writer Agent -> data.v1.json
  Task -> Updater Agent -> data.v2.json (preserves v1)
  Task -> Merger Agent -> data.final.json

Key: Version history preserved
Verified: All versions recoverable, no data loss
```

#### PDF-to-Markdown Workflow Pattern (Integrated)
```python
User Request: "Process PDFs to standardized markdown"

Main Claude:
  Task -> art-materials-processor (file1.pdf) | parallel
  Task -> art-materials-processor (file2.pdf) | parallel

Agent Workflow (Integrated):
  1. MinerU Pipeline AUTO extraction -> {name}_original.md
  2. Automatic markdown cleaning (Pattern 1-17) -> {name}.md
  3. Agent reads BOTH markdown files completely
  4. Intelligent semantic integrity verification (LLM-based)
  5. Auto-delete {name}_original.md if integrity verified
  6. Keep both if content loss detected

Final Output per PDF:
  - {name}_origin.pdf (source backup)
  - {name}.md (cleaned, verified markdown)
  - images/ (extracted images)

Key: Direct agent invocation with integrated cleaning and LLM-based integrity verification
Verified: Handles Unicode paths, parallel processing, automatic cleanup, semantic verification
Note: pdf-to-markdown-coordinator archived (2025-09-26) - no longer needed with integrated workflow
```

## Common Errors and Fixes

| Error | Consequence | Fix |
|-------|-------------|-----|
| Unicode in any component | Windows encoding errors | Remove all Unicode, use ASCII only |
| Coordinator has Task tool | Recursion crash | Remove Task, keep only Read/Write/Grep |
| Coordinator has Bash tool | Self-execution instead of planning | Remove Bash, coordinators plan only |
| Coordinator empty tools config | May inherit Task | Explicitly declare tools: Read, Write, Grep |
| Command over 120 lines | May lack focus | Balance delegation vs necessary context |
| Agent hardcoded paths | Inflexible | Receive paths from Main Claude |
| Direct file write | Corruption risk | Write .tmp first, then atomic rename |
| Coordinator attempts execution | Architecture violation | Only return plan, don't execute |
| Command loses business context | Main Claude confusion | Preserve critical workflow steps |
| Read tool on directory | EISDIR error | Use Bash ls for directories, Read only for files |
| JSON without UTF-8 encoding | UnicodeDecodeError | Always use encoding='utf-8' when reading JSON |
| Timestamp placeholders in plans | Main Claude can't resolve | Coordinator must generate actual timestamps |
| Wrong script version in agent | Missing features/bugs | Verify agent uses latest script version |
| Coordinator uses placeholders | Paths not resolved | Replace {timestamp} with actual values in JSON |
| Agent missing required tools | Cannot complete task | Ensure agents have all needed tools (Read, Write, Bash, etc.) |
| Coordinator includes bash tasks | Main Claude cannot execute | Remove bash tasks from coordinator plans |
| Colon in YAML frontmatter | "mapping values are not allowed here" | Quote value or replace `:` with `-` |
| Special chars in YAML | YAML parsing errors | Quote entire value or use literal block `\|` |
| Large file exceeds Read limit | Tool fails, partial data | Use chunked reading: offset + limit parameters |
| File over 256KB in agent | Cannot read complete file | Implement sequential chunking with 2000-line chunks |
| Task tool "Prompt too long" | Not actually prompt length issue | Avoid trigger words like "system_scan.json" in prompts |

## Task Tool Trigger Word Discovery (2025-09-14)

### Critical Finding: Hidden File Name Processing
**Problem**: Task tool fails with "Prompt is too long" error even when prompt is short (~200 chars)

### Root Cause
Task tool has hidden file name/path processing that triggers on certain patterns:
- **Trigger words**: `system_scan.json`, `.claude` paths, specific filenames
- **Additional triggers**: Any .json/.yaml files over 100KB, nested path patterns
- **Behavior**: Appears to attempt loading/validating files mentioned in prompts
- **Impact**: Large files (1MB+) cause token limit exceeded errors
- **Hidden behavior**: Auto-loads referenced files for validation/context

### Symptoms vs Reality
```yaml
What you see:
  Error: "Prompt is too long"
  Assumption: Agent file or prompt is too large

What's actually happening:
  Task tool detected a trigger word
  Attempted to load 1MB+ file into context
  Exceeded internal token limits
```

### Solution Pattern
```yaml
WRONG (triggers error):
  prompt: "Analyze system_scan.json"
  prompt: "Process .claude/report/xxx/system_scan.json"

CORRECT (avoids trigger):
  prompt: "Analyze scan data in report directory"
  prompt: "Process the scan file in report/xxx/ folder"
```

### Implementation Fix
1. **Coordinator level**: Return directory + type instead of full paths
   ```json
   // Instead of:
   "input_path": ".claude/report/xxx/system_scan.json"

   // Use:
   "report_directory": ".claude/report/xxx",
   "scan_type": "system"
   ```

2. **Agent level**: Construct paths internally
   ```python
   # Agent builds path to avoid trigger in Main Claude prompt
   scan_file = f"{report_directory}/system_scan.json"
   ```

### Why "Sometimes Works, Sometimes Fails"
- **Works**: When prompt accidentally avoids trigger words
- **Fails**: When prompt contains exact file names
- **File size factor**: Small files might not trigger the issue

### Debugging Method That Found This
1. Binary search with progressively shorter prompts
2. Controlled variable testing (removing path elements)
3. Found that specific words trigger the error
4. Confirmed by testing different file names

### Key Lesson
> "Error messages are clues, not truth" - The actual problem may be completely different from what the error suggests

### Ideal Knowledge Transfer Architecture

```
Knowledge Sources:
    CLAUDE.md (Global Rules)
         |
    TRIGGER-WORD-PATTERNS.md (Specific Patterns)
         |
    Command Files (Execution Warnings)
         ↓
    Main Claude (Apply All Rules)
         ↓
    [Transform Dangerous Prompts]
         ↓
    Safe Task Calls to Agents

Protection Layers:
1. Documentation Layer: CLAUDE.md + Pattern Guide
2. Command Layer: Explicit warnings in execution
3. Coordinator Layer: Return safe formats
4. Main Claude Layer: Transform prompts
5. Agent Layer: Defensive input handling
```

## Tool Selection Principles (CRITICAL CLARIFICATION)

### Available Tools for Agents
```yaml
ANY tool except Task is valid:
  - Read, Write, Edit: File operations and content modification
  - Bash, Grep, Glob: System operations and search
  - WebSearch, WebFetch: Internet research
  - Other tools as needed for specific functionality

ONLY Forbidden Tool:
  - Task: NEVER in subagents (prevents recursion crash)

Selection Criteria:
  - Choose tools based on agent's actual functionality requirements
  - Edit tool is equally valid as Write tool for content modification
  - Don't restrict to "common combinations" - use what the agent needs

Common Patterns (EXAMPLES, not requirements):
  - Content Editors: [Read, Edit] or [Read, Write, Edit]
  - File Processors: [Read, Write, Bash]
  - Content Analyzers: [Read, Grep] or [Read, Write, Grep]
  - Research Agents: [Read, Write, WebSearch, WebFetch]
  - System Managers: [Read, Write, Edit, Bash, Grep]

KEY PRINCIPLE: Tool selection should match agent functionality, not follow arbitrary patterns
```

### Edit Tool Usage
```yaml
Edit Tool is VALID and USEFUL for:
  - Precise text replacements in markdown/code
  - Content modification with exact string matching
  - Iterative document processing
  - Fine-grained content transformations

Edit vs Bash for Text Processing:
  Use Edit when:
    - Precise string replacements needed
    - Text has normalized whitespace
    - Clean, exact matching required

  Use Bash when:
    - Bulk operations across files
    - Control characters or special whitespace
    - Pattern matching with regex
    - Binary data processing

Historical Note:
  Early documentation patterns (Read, Write, Bash, Grep) created
  false impression that Edit was "non-standard". This is incorrect.
  Edit tool has always been valid - it was just absent from examples.
```

## Python Script Integration Best Practices

### When to Use Python Scripts vs Agents
```yaml
Use Python Scripts for:
  - Bulk file operations (100x faster than individual Read calls)
  - Pattern matching across many files
  - Data transformation and aggregation
  - Systematic scanning and collection

Use Agents for:
  - Intelligent analysis and decision making
  - Context-aware processing
  - Report generation with insights
  - Workflow orchestration
```

### Script Design Principles
1. **No Unicode** - Use ASCII only for Windows compatibility
2. **UTF-8 encoding** - Always specify when reading/writing files
3. **Specific exceptions** - No bare except clauses
4. **Auto-generate paths** - Don't rely on passed parameters
5. **Modular design** - Single responsibility per script

### Large File Handling Patterns

#### Chunked Reading for Agents
When agents need to process large files (>256KB):

```python
# Complete chunked reading pattern (proven in system-analyzer)
total_lines = bash: wc -l {file_path}
chunk_size = 2000  # Lines per chunk (stays under tool limits)
offset = 0
all_data = []

while offset < total_lines:
    chunk = Read(file_path, offset=offset, limit=chunk_size)
    all_data.append(chunk)
    offset += chunk_size

# Process complete file content
process_combined_data(all_data)
```

#### When to Use Chunked Reading vs Python Scripts
```yaml
Use Chunked Reading (in agents):
  - Agent needs to process and analyze large files
  - Intelligent processing required on file content
  - File size 256KB - 2MB (manageable chunks)

Use Python Scripts (system-scanner pattern):
  - File collection and bulk processing
  - Files over 2MB or hundreds of files
  - Performance-critical scanning operations
  - Raw data extraction without analysis
```

#### Proven Success Pattern
System-check v2.0 demonstrates optimal hybrid approach:
1. **Python script**: Bulk data collection -> large JSON
2. **Chunked reading**: Agent processes large JSON intelligently
3. **Single output**: Processed results to next stage

**Key Benefits**:
- No data loss (complete file processing)
- Respects tool limits (2000-line chunks)
- Enables intelligent analysis of large datasets
- Pipeline efficiency (single read per stage)

## Golden Rules

1. **NO Unicode characters in any component (causes Windows errors)**
2. **Only Main Claude has Task tool**
3. **Coordinators return plans, don't execute (NO Bash tool!)**
4. **Agents execute tasks, don't coordinate**
5. **Use relative paths in Bash commands (Windows compatibility)**
6. **Commands delegate with necessary context**
7. **Business completeness > arbitrary line limits**
8. **File system is communication layer, prevents recursion**
9. **Paths resolved by Main Claude**
10. **No subagent calls subagent**
11. **Atomic writes: .tmp file + mv (prevents corruption)**
12. **Preserve critical business logic in commands when needed**
13. **Read tool only for files, Bash ls for directories**
14. **Always use UTF-8 encoding for JSON operations**
15. **Verify agents use latest script versions**
16. **Use chunked reading for large files: offset + limit with 2000-line chunks**
17. **Human-in-Loop uses simple choices: 1)Approve 2)Modify, numeric input not text**
18. **Avoid trigger words in Task prompts: Use descriptive language instead of exact file names**
19. **NEW: Coordinators forbidden Bash tool - prevents self-execution, maintains planning role**

## Reference Template Locations

- **Command template**: `.claude/templates/TEMPLATE_command.md`
- **Coordinator template**: `.claude/templates/TEMPLATE_coordinator.md`
- **Agent template**: `.claude/templates/TEMPLATE_agent.md`
- **Architecture doc**: `.claude/templates/ARCHITECTURE_data_layer.md`
- **Quick reference**: `.claude/templates/QUICK_REFERENCE.md`

## Validation Checklist

Before creating new components:
- [ ] NO Unicode characters anywhere in the file?
- [ ] YAML frontmatter has no unquoted colons in values?
- [ ] YAML string values with special chars are quoted?
- [ ] Coordinator has explicit tools config without Task OR Bash?
- [ ] Command under 100 lines?
- [ ] Agent does single task only?
- [ ] Uses file communication not return values?
- [ ] Paths passed from Main Claude not hardcoded?
- [ ] Write operations use atomic pattern (.tmp files)?

## Model Selection Guidelines (2025)

### Available Claude Models for Subagents

#### Claude 4 Series (Latest - Released 2025)
```yaml
Claude Opus 4.1: claude-opus-4-1-20250805
  - Alias: opus
  - Release: August 5, 2025
  - Use for: Critical quality checks, complex analysis, final validations
  - Best for: quality-scorer, final-quality-validator, critical coordinators
  - Cost: Highest, use sparingly for important tasks

Claude Opus 4: claude-opus-4-20250514
  - Alias: opus (when 4.1 not needed)
  - Release: May 22, 2025
  - Use for: Complex reasoning and analysis tasks
  - Cost: High tier

Claude Sonnet 4: claude-sonnet-4-20250514
  - Alias: sonnet
  - Release: May 22, 2025
  - Use for: Complex coordinators, advanced agents, general heavy lifting
  - Best for: Most coordinators, content generators, complex workflows
  - Cost: Moderate, good performance/cost balance
```

#### Claude 3.7 Series
```yaml
Claude Sonnet 3.7: claude-3-7-sonnet-20250219
  - Alias: claude-3-7-sonnet-latest
  - Release: February 24, 2025
  - Special: Hybrid AI reasoning with rapid/thoughtful response options
  - Use for: Advanced reasoning with flexible response modes
```

#### Claude 3.5 Series
```yaml
Claude Haiku 3.5: claude-3-5-haiku-20241022
  - Alias: haiku
  - Release: October 22, 2024
  - Use for: Simple agents, quick operations, status checks
  - Best for: file operations, simple validators, status reporters
  - Cost: Lowest, fastest response times

Claude Haiku 3: claude-3-haiku-20240307
  - Status: Legacy model, still available
```

### Model Configuration in YAML Frontmatter
```yaml
---
name: agent-name
description: Agent description
tools: Read, Write, Bash, Grep
model: sonnet  # Options below
---
```

#### Model Field Options
1. **Alias Names** (Recommended for simplicity):
   - `model: opus` - Uses latest Opus (currently 4.1)
   - `model: sonnet` - Uses latest Sonnet (currently 4.0)
   - `model: haiku` - Uses latest Haiku (currently 3.5)

2. **Full Model IDs** (For version-specific control):
   - `model: claude-opus-4-1-20250805`
   - `model: claude-sonnet-4-20250514`
   - `model: claude-3-5-haiku-20241022`

3. **Special Options**:
   - `model: inherit` - Uses same model as main conversation
   - (omit field) - Defaults to system default (usually Sonnet)

### Model Selection Strategy
```yaml
Default Strategy (Recommended):
  - Commands: No model specified (use system default)
  - Most Agents: No model specified (default sufficient)
  - Simple Agents: haiku (for speed)
  - Complex Coordinators: sonnet
  - Critical Quality: opus

NOVELSYS-SWARM Priorities by Agent Type:
  Coordinators: sonnet (complex planning)
  Quality Validators: opus (highest quality)
  Content Generators: sonnet (balanced)
  File Operations: haiku (speed optimized)
  Standard Operations: omit field (use default)

Cost-Performance Balance:
  1. Haiku 3.5: Fastest, cheapest, simple operations
  2. Sonnet 4: Balanced, most tasks
  3. Opus 4.1: Highest quality, use sparingly
```

### When to Specify Models
```yaml
Specify model when:
  YES - Need higher capability than default (complex coordinators)
  YES - Need faster response (simple file operations)
  YES - Need highest quality (final quality checks)

Don't specify when:
  NO - Default model is sufficient for the task
  NO - Unsure which model to use (default is safe)
  NO - Trying to optimize without measuring need
```

### Known Issues with Model Selection
```yaml
Model Inheritance Bug:
  - Issue: Subagents may not properly inherit configured model
  - Impact: May default to Sonnet 4 even with explicit configuration
  - Workaround: Use full model IDs for critical requirements
  - Status: Reported August 2025, may be resolved

Legacy Model Status:
  - Claude 3 Opus (2024-02-29): Deprecated June 30, 2025
  - Claude 3 Sonnet (2024-02-29): Retired July 21, 2025
  - Claude 2.1: Fully retired July 21, 2025
```

## YAML Frontmatter Standards

### Quick YAML Rules for .md Files
To prevent "mapping values are not allowed here" errors in Python scripts:

```yaml
---
name: component-name
description: "Use quotes if text contains: colons, @, #, or other special chars"
tools: Read, Write, Grep  # No Task or Bash tool for coordinators
thinking: Replace colons with dashes - or wrap entire value in quotes
---
```

**Common Fix**: If you see YAML parsing errors, either:
1. Replace `:` with `-` in the text
2. Wrap the entire value in quotes: `"text with: special chars"`
3. Use literal block for multi-line: `thinking: |` followed by indented lines

## I/O and Prompt Documentation Standards

### Agent I/O Requirements
All agents MUST document:
```yaml
Input Requirements:
  - Expected prompt format from Main Claude
  - Required parameters and file paths
  - Optional context information

File I/O Operations:
  - Reads from: Specific files with purpose
  - Writes to: Output files and formats
  - Temporary files: .tmp pattern for atomic ops

Output Format:
  - Return format to Main Claude
  - Success indicators
  - Error handling
```

### Coordinator Planning I/O
Coordinators MUST document:
```yaml
Input Requirements:
  - Orchestration requests from Main Claude
  - Required context for planning
  - Configuration dependencies

Planning I/O:
  - Reads from: Files needed for planning (READ-ONLY)
  - NEVER writes files: Coordinators only return plans

JSON Plan Response:
  - Returns plan DIRECTLY to Main Claude (not as file)
  - Structured execution plan in response text
  - Agent specifications with tasks
  - Path templates for Main Claude to resolve
```

### Command I/O Context
Commands SHOULD document:
```yaml
High-level I/O:
  - Overall operation file flow
  - User-visible input/output
  - Delegation chain effects
```

## Project Status (2025-09-26 v6.7)

- **Architecture understanding**: 100% (fully correct)
- **Recursion prevention**: Complete mechanism implemented (0 agents with Task tool)
- **Coordinator tool restriction**: NEW discovery and implementation
- **Self-execution prevention**: Three-layer strategy implemented
- **Documentation accuracy**: All errors corrected, latest findings integrated
- **I/O standardization**: Complete I/O and Prompt documentation framework
- **System components**: 24 commands, 21 coordinators, 80 agents (101 total in agents folder)
- **Templates complete**: All templates updated with I/O and Prompt standards (v6.3)
  - TEMPLATE_command.md - Business context + flexible line limits
  - TEMPLATE_coordinator.md - JSON planning + I/O documentation + Tool restrictions
  - TEMPLATE_agent.md - Single responsibility + comprehensive I/O specs
- **Support docs updated**: CLAUDE.md, claude-code-expert.md with latest standards
- **Execution patterns tested**: All 6 critical patterns verified and working
  - Architecture compliance test [PASS]
  - Parallel execution test [PASS]
  - Advanced I/O patterns test [PASS]
  - Python pipeline test [PASS]
  - Multi-coordinator test [PASS]
  - Human-in-loop test [PASS]
- **Windows compatibility**: 100% (path handling fixed and documented)
- **System stability**: 100% recursion-safe, production-ready
- **System-check**: Refactored v2.0 with comprehensive Python script backend
  - Fixed timestamp placeholder issues
  - Fixed agent tool configurations
  - Added system_check_v3.py with semantic extraction modules
  - Implemented chunked reading for large file processing (1MB+ JSON files)
  - **FIXED (2025-09-14)**: Task tool trigger word issue causing false "Prompt too long" errors
- **Human-in-Loop standardization**: Simple choice format (1/2) with infinite modify capability
- **NEW (2025-09-26)**: Coordinator tool restriction rationale and prevention strategy documented

## Path Format Standardization Rules

### File Path Documentation Standards
To maintain consistency and clarity in Data I/O documentation:

#### 1. Real File Paths
```yaml
Correct formats:
  - Static path: `path/to/file.md`
  - Dynamic path: `{project}/book_{N}/chapter.md`
  - Absolute path: `/absolute/path/to/file.yaml`
  - Relative path: `../relative/path/file.json`

Incorrect formats:
  - Double backtick: `path/to/file.md`` (WRONG)
  - No backticks: path/to/file.md (WRONG)
  - Mixed quotes: "path/to/file.md" (WRONG)
```

#### 2. Inferred/Pattern Paths
```yaml
Format: [Description: pattern]
Examples:
  - [Bible files: series_bible.yaml, book_*/bible.yaml]
  - [Chapter files: chapters/*/content.md]
  - [Dynamic input paths]
```

#### 3. Status Messages
```yaml
DO NOT mix with file paths:
  WRONG: "File saved successfully to output.md"
  WRONG: "CRITICAL: Multiple writers detected"

Keep separate in documentation:
  CORRECT: Writes to: `output.md`
  CORRECT: Status: File saved successfully
```

#### 4. Path Variables
```yaml
Standard variables:
  {project} - Project name
  {N} or {book} - Book number
  {NNN} or {chapter} - Chapter number (padded)
  {timestamp} - ISO timestamp
  * - Wildcard for multiple items
```

## Naming Conventions and Key Consistency

### Dictionary/JSON Key Naming Rules
When converting pattern names or identifiers to dictionary keys:

```python
# CORRECT: Consistent conversion
pattern_name = "Producer-Consumer"
key = pattern_name.lower().replace(' ', '_').replace('-', '_')
# Result: "producer_consumer"

# WRONG: Inconsistent conversion
key1 = pattern_name.lower().replace(' ', '_')  # "producer-consumer"
key2 = pattern_name.lower().replace('-', '_')  # "producer_consumer"
# Mismatch causes KeyError!
```

### Standard Naming Conventions
```yaml
Component Names:
  - Agents: lowercase-hyphen-format (e.g., quality-scorer)
  - Coordinators: lowercase-hyphen-coordinator (e.g., chapter-start-coordinator)
  - Commands: lowercase-hyphen (e.g., architecture-test)

Dictionary Keys:
  - Convert to: lowercase_underscore_format
  - Replace both spaces AND hyphens with underscores
  - Be consistent across entire codebase

File Names:
  - Use underscores for Python files: io_pattern_test.py
  - Use hyphens for markdown files: architecture-test.md
  - Be consistent within each file type
```

### Key Conversion Pattern
Always use this pattern for consistent key conversion:
```python
def to_dict_key(name):
    """Convert any name to consistent dictionary key format"""
    return name.lower().replace(' ', '_').replace('-', '_')
```

## System Test Validation Status (2025-09-14)

### Successfully Tested & Verified Patterns
All critical execution patterns have been tested and verified:

1. **Architecture Test** (`/architecture-test`)
   - Verified: All components correctly configured without Task tool
   - Result: 100% recursion-safe architecture

2. **Parallel Execution Test** (`/parallel-test`)
   - Verified: True parallel execution of multiple agents
   - Result: No race conditions, proper file isolation

3. **I/O Patterns Test** (`/io-patterns-test`)
   - Verified: Atomic writes with file lock mechanism (.tmp + mv pattern)
   - Verified: Producer-Consumer, Shared Reference, Version Control patterns
   - Result: Zero corruption with concurrent writes, atomic operations confirmed

4. **Python Pipeline Test** (`/python-pipeline-test`)
   - Verified: Sequential 3-stage data processing pipeline
   - Result: 100% data integrity across stages

5. **Multi-Coordinator Test** (`/multi-coordinator-test`)
   - Verified: Single command orchestrating multiple coordinators
   - Result: Coordinators properly isolated, no direct calls

6. **Human-in-Loop Test** (`/human-in-loop-test`)
   - Verified: Human approval gates in workflow
   - Verified: Conditional execution based on user decisions
   - Verified: Workflow state management across approval points
   - Result: Successfully handles approve/reject/modify flows

### System Maintenance Notes
- **Commands**: Some exceed 100-line target (up to 224 lines) but remain functional with necessary business logic
- **Coordinators**: All 21 correctly return JSON plans without Task tool (verified)
- **NEW**: Coordinators now restricted from Bash tool to prevent self-execution
- **Agents**: Most follow single-responsibility pattern, few exceed length guidelines but functional
- **Documentation**: All path formats standardized, Windows compatibility documented

### System Validation Summary
- **Recursion Safety**: 100% verified
- **Windows Compatibility**: 100% verified (path handling fixed)
- **Execution Patterns**: All patterns tested and working
- **Architecture Compliance**: 100% verified
- **NEW: Self-Execution Prevention**: Tool restriction strategy implemented
- **Production Ready**: YES

---

## See Also - Documentation System

### Navigation & Overview
- **[SYSTEM_INDEX.md](SYSTEM_INDEX.md)** - Master documentation index and navigation guide
- **[.claude/templates/README.md](.claude/templates/README.md)** - Template system overview

### Quick References
- **[.claude/templates/QUICK_REFERENCE.md](.claude/templates/QUICK_REFERENCE.md)** - Rapid lookup for rules and patterns
- **[.claude/agents/claude-code-expert.md](.claude/agents/claude-code-expert.md)** - Live expert for troubleshooting

### Implementation Templates
- **[TEMPLATE_command.md](.claude/templates/TEMPLATE_command.md)** - Create new commands
- **[TEMPLATE_coordinator.md](.claude/templates/TEMPLATE_coordinator.md)** - Create new coordinators
- **[TEMPLATE_agent.md](.claude/templates/TEMPLATE_agent.md)** - Create new agents

### Deep Architecture Understanding
- **[ARCHITECTURE_data_layer.md](.claude/templates/ARCHITECTURE_data_layer.md)** - Why file system prevents recursion
- **[ARCHITECTURE_GOLD_STANDARD.md](.claude/templates/ARCHITECTURE_GOLD_STANDARD.md)** - Universal system design patterns from 6 proven tests

### Application Patterns
- **[NOVEL_SYSTEM_PATTERNS.md](.claude/NOVEL_SYSTEM_PATTERNS.md)** - Novel-specific implementation patterns

---

**Core reminder**: Coordinator is subagent -> Cannot have Task OR Bash -> Cannot call subagents OR self-execute -> No recursion, clean separation!

*Based on official documentation, community practices, actual testing, and NOVELSYS-SWARM production experience.*

**Document Version**: v6.7 | **Last Updated**: 2025-09-26 | **Status**: Production Ready + Coordinator Tool Restrictions Clarified