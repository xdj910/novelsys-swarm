# Agent Directory Handling Standards

## Critical Rule: NEVER Read Directories

### ❌ Wrong (causes EISDIR error)
```python
Read("knowledge_base/trends")  # This is a directory!
Read(output_directory)        # Will fail if it's a directory
```

### ✅ Correct Directory Operations

#### Check directory contents:
```bash
# Use Bash for directory operations
ls knowledge_base/trends/
find knowledge_base -name "*.json" -type f
```

#### Create directories:
```bash
mkdir -p knowledge_base/trends
```

#### Read specific files only:
```python
Read("knowledge_base/trends/specific_file.json")  # File, not directory
```

#### Write files (auto-creates directories):
```python
Write("knowledge_base/trends/output.json", content)  # Automatically creates path
```

## Standard Agent Directory Handling Pattern

### Step 1: Prepare Output (if needed)
```yaml
Do NOT validate directories with Read
Instead use:
  - Write tool creates directories automatically
  - Bash commands for directory checks
  - Generate unique timestamps for filenames
```

### Step 2: Read Existing Research (if needed)
```python
# Find existing files first
files = Bash("find knowledge_base -name '*.json' -type f")
for file in files:
    data = Read(file)  # Read specific files, not directories
```

### Step 3: Save Results
```python
# Write automatically creates directory structure
Write("knowledge_base/category/filename_timestamp.json", results)
```

## Applied to All Research Agents

This standard has been applied to:
- ✅ trend-analyzer.md (fixed Validate Output Directory)
- ✅ topic-explorer.md (fixed Validate Output Directory)
- ✅ competitor-scanner.md (no issues found)
- ✅ audience-profiler.md (no issues found)
- ✅ voice-analyzer.md (no issues found)
- ✅ bible-generator.md (correctly uses Bash find)

## Key Points for Agents

1. **Never Read directories** - only Read specific files
2. **Use Bash for directory operations** - ls, find, mkdir
3. **Write creates paths automatically** - no need to pre-create
4. **Generate unique filenames** - avoid overwrites
5. **Handle missing files gracefully** - check before Reading

This prevents EISDIR errors and ensures robust directory handling.