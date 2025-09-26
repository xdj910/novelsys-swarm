# Windows Safety Test

## Test 1: Safe File Counting
Instead of: `ls -1 .claude/agents/*.md | wc -l`
Use: Glob tool with pattern `.claude/agents/*.md` and count results

## Test 2: Safe Directory Scanning  
Instead of: `find /c/ -name "*.md"`
Use: Glob tool with pattern `.claude/**/*.md`

## Test 3: Safe File Search
Instead of: `find . -type f -name "*.yaml"`
Use: Glob tool with pattern `.claude/**/*.yaml`

## Critical Rules Added:
1. NEVER use find command
2. NEVER scan outside project directory
3. ALWAYS use Glob/Grep tools
4. NEVER use ls with pipes
5. NEVER access /c/ or C:\ directly

## Modified Agents:
- system-check-coordinator: Added Windows safety rules to all 15 agent prompts
- All Phase 1-5 agents: Explicit instructions to use Glob/Grep only
- No Bash file operations except for timestamp and directory creation