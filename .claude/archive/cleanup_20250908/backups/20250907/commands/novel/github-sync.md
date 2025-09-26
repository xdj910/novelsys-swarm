---
description: Sync chapter content to GitHub Issues
argument-hint: <chapter_number> or "all"
---

# GitHub Sync Command

Sync chapter content to GitHub Issues: **$ARGUMENTS** (chapter number or 'all')

## v2.5 GitHub Integration

### Core Concept
Transform GitHub Issues into persistent novel database:
- Issue #1: Bible Definition
- Issue #2: Chapter 1
- Issue #3: Chapter 2
- ...each chapter becomes a tracked Issue

### Sync Modes

#### Incremental Sync (default)
```bash
# Smart differential sync
/novel:github-sync 3

# Only sync changed content
- Calculates diff since last sync
- Uploads only modified sections
- Preserves GitHub API quota
```

#### Full Sync
```bash
# Complete chapter replacement
/novel:github-sync 3 --full

# Complete content upload
- Replaces entire Issue content
- Used for major rewrites
- Higher API usage
```

#### Batch Sync
```bash
# Sync multiple chapters
/novel:github-sync 1,2,3,4,5
/novel:github-sync all

# Mass synchronization
- Parallel upload processing
- Progress tracking
- Error recovery
```

## Issue Structure

### Chapter Issue Format
```markdown
# 第X章: [章节标题]

## 大纲
[章节大纲内容]

## 内容
[完整章节内容]

## 元数据
- 字数: 3500
- 质量分: 92
- 版本: v2.3
- 最后更新: 2025-01-30

## 生成报告
### Stream执行结果
- Character Psychology: 95分
- Narrative Structure: 92分
- World Building: 93分
- Prose Craft: 91分
- Continuity Guard: 99分
- Foreshadowing: 100分
- Dialogue Master: 94分
- Emotion Weaver: 90分

### 质量分析
[质量分析详情]
```

## Execution Flow

### 1. Pre-sync Validation
```bash
# Check GitHub CLI authentication
auth_status=$(gh auth status 2>&1)
if [[ $auth_status == *"not logged"* ]]; then
    echo "[ ] Error: GitHub CLI not authenticated. Run: gh auth login"
    exit 1
fi

# Get repository info
repo_url=$(git remote get-url origin 2>/dev/null || echo "")
if [[ -z "$repo_url" ]]; then
    echo "[ ] Error: No Git repository found. Initialize with: git init && git remote add origin <URL>"
    exit 1
fi

# Get current project
# Use Read tool: `.claude/data/context/current_project.json`
# If no "project" field exists:
#   Display: "[ ] Error: No active project. Use /novel:project-new to create one."
#   Stop execution
# Extract project_name from the JSON
```

### 2. Content Preparation

**Determine what to sync:**
- If ARGUMENTS == "all":
  * Use Glob tool: `.claude/data/projects/{project}/chapters/*/content.md`
  * Use Read tool: `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
  * Set sync_type to "full"
- Otherwise:
  * Parse chapter_num from ARGUMENTS
  * Set chapters to single chapter path: `.claude/data/projects/{project}/chapters/ch{chapter_num:03d}/content.md`
  * Set sync_type to "incremental"

**Load project metadata:**
- Use Read tool: `.claude/data/projects/{project}/project.json`

### 3. GitHub Operations

**If sync_type equals "full":**
1. **Sync Bible as Issue #1:**
   - Use Read tool: `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
   - Store as bible_content
   
2. **Check if Issue #1 exists:**
   - Use Bash tool: `gh issue view 1 --json state 2>/dev/null`
   - Store result to determine if issue exists
   
3. **If Issue #1 does NOT exist:**
   - Use Bash tool to create Issue #1:
   ```bash
   gh issue create \
       --title "📖 Series Bible: {project}" \
       --body-file ".claude/data/projects/{project}/book_{current_book}/bible.yaml" \
       --label "bible,novel"
   ```
   
4. **If Issue #1 exists:**
   - Use Bash tool to update it:
   ```bash
   gh issue edit 1 \
       --body-file ".claude/data/projects/{project}/book_{current_book}/bible.yaml"
   ```

**For each chapter file in chapters list:**
1. **Extract chapter number from filename**
2. **Calculate issue_num:** chapter_num + 1 (Issue #2 is Chapter 1)
3. **Read chapter data:**
   - Use Read tool on chapter file for content
   - Use Read tool on corresponding meta.json file
    
4. **Create temp file with formatted content:**
   - Use Write tool to `.claude/temp/chapter_sync.md` with:
   ```markdown
   # [Chapter title from meta or 'Chapter N']
   
   **Status**: [status from meta or 'draft']
   **Word Count**: [word_count from meta or 0]
   **Quality Score**: [quality_score from meta or 'N/A']
   
   ---
   
   [chapter content]
   ```

5. **Check if issue exists:**
   - Use Bash tool: `gh issue view {issue_num} --json state 2>/dev/null`
   - Store result to check existence

6. **If issue does NOT exist:**
   - Use Bash tool to create new issue:
   ```bash
   gh issue create \
       --title "📚 Chapter {chapter_num}: {title from meta}" \
       --body-file ".claude/temp/chapter_sync.md" \
       --label "chapter,novel"
   ```

7. **If issue exists:**
   - Use Bash tool to update it:
   ```bash
   gh issue edit {issue_num} --body-file ".claude/temp/chapter_sync.md"
   ```

### 4. Local State Update
```yaml
tracking:
```

## Error Handling

### Network Issues
```bash
# Retry mechanism
Max retries: 3
Backoff: exponential (1s, 2s, 4s)
Timeout: 30s per operation
```

### API Limits
```bash
# Rate limit handling
GitHub API: 5000/hour
Issues API: 100/hour
Intelligent queuing
```

### Content Conflicts
```bash
# Conflict resolution
Detect remote changes
Offer merge options
Backup local content
```

## Integration Points

### Stream Coordinator
**Automatic sync after chapter completion:**
- When chapter generation completes successfully
- Automatically trigger GitHub sync
- Use incremental mode by default
- Preserve chapter content in GitHub Issue

## Usage Examples

### Basic Chapter Sync
```bash
# Sync chapter 3 with incremental mode
/novel:github-sync 3

# Response: "第3章同步完成 增量模式 +247字"
```

### Batch Operations
```bash
# Sync chapters 1-5
/novel:github-sync 1-5

# Sync all chapters
/novel:github-sync all --progress
```

### Advanced Options
```bash
# Force full sync
/novel:github-sync 3 --full --force

# Sync with custom commit message
/novel:github-sync 3 --message "Major revision after editor feedback"

# Dry run to preview changes
/novel:github-sync 3 --dry-run
```

## Configuration

### Required Settings
```yaml
github:
  token: $GITHUB_TOKEN
  repository: "username/novel-project"
  default_labels: ["chapter", "content"]
  sync_mode: "incremental"
```

### Optional Settings
```yaml
sync:
  auto_sync: true
  batch_size: 5
  timeout: 30
  max_retries: 3
  backup_local: true
```

---

**GitHub Sync Command** - v2.5核心功能  
*将每个章节持久化为GitHub Issue，实现跨会话记忆*

## Actual Implementation

### Execute GitHub Sync

**Parse and validate arguments:**
1. Get chapters to sync from $ARGUMENTS
2. Default to "all" if not specified
3. Parse range syntax (e.g., "1-5")
4. Parse list syntax (e.g., "1,3,5")

**Check GitHub CLI authentication:**
1. Use Bash tool: `gh auth status`
2. Check if authenticated:
   - If not logged in:
     * Display: "[ ] Error: GitHub CLI not authenticated. Run: gh auth login"
     * Stop execution
   - If gh not found:
     * Display: "[ ] Error: GitHub CLI not installed. Install from: https://cli.github.com/"
     * Stop execution

**Check Git repository:**
1. Use Bash tool: `git remote get-url origin`
2. Validate repository:
   - If no remote found:
     * Display: "[ ] Error: No Git repository found. Initialize with:"
     * Display: "git init && git remote add origin <URL>"
     * Stop execution
   - If successful: Store repository URL

**Get current project:**
1. Use Read tool: `.claude/data/context/current_project.json`
2. Parse JSON to get project name
3. If no project found:
   - Display: "[ ] Error: No active project. Use /novel:project-new to create one."
   - Stop execution

**Load project paths:**
- Project path: `.claude/data/projects/{project}`
- Bible path: `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
- Chapters path: `.claude/data/projects/{project}/chapters`

**Display sync header:**
- Show decorative box: "📤 GitHub Issues Sync"
- Display: "Project: {project}"
- Display: "Repository: {repository_name}"
- Initialize sync_count = 0
- Initialize error_count = 0

**Sync Bible as Issue #1:**

1. **Check if should sync Bible:**
   - If chapters_to_sync is "all" AND book_{current_book}/bible.yaml exists:
     * Display: "📖 Syncing Series Bible..."
     * Continue with sync

2. **Check if Issue #1 exists:**
   - Use Bash tool: `gh issue view 1 --json state`
   - If command fails: Issue doesn't exist
   - If command succeeds: Issue exists

3. **Create new Bible Issue (if doesn't exist):**
   - Use Read tool on `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
   - Create formatted content:
     * Header: "# 📖 Series Bible: {project}"
     * Body: Bible content
     * Footer: "*Synced at {timestamp}*"
   - Use Write tool: `.claude/temp/bible_issue.md` with formatted content
   - Use Bash tool: `gh issue create --title "📖 Series Bible: {project}" --body-file .claude/temp/bible_issue.md --label "bible,novel"`
   - If successful:
     * Display: "[x] Bible synced as Issue #1"
     * Increment sync_count
   - If failed:
     * Display: "[ ] Error: Failed to create Bible issue - {error}"
     * Increment error_count

4. **Update existing Bible Issue (if exists):**
   - Use Read tool on `.claude/data/projects/{project}/book_{current_book}/bible.yaml`
   - Use Write tool: `.claude/temp/bible_update.md` with Bible content
   - Use Bash tool: `gh issue edit 1 --body-file .claude/temp/bible_update.md`
   - If successful:
     * Display: "[x] Bible updated in Issue #1"
     * Increment sync_count
   - If failed:
     * Display: "[ ] Error: Failed to update Bible - {error}"
     * Increment error_count

**Determine which chapters to sync:**

1. **If syncing all chapters:**
   - Use Glob tool: `.claude/data/projects/{project}/chapters/ch*`
   - Get all chapter directories
   - Sort by chapter number

2. **If syncing specific chapter(s):**
   - Parse $ARGUMENTS value
   - If single number (e.g., "3"):
     * Create path: `.claude/data/projects/{project}/chapters/ch{NNN}`
   - If range (e.g., "1-5"):
     * Parse start and end numbers
     * Create list of paths for each chapter in range
   - If comma-separated (e.g., "1,3,5"):
     * Parse individual numbers
     * Create list of paths
   - If invalid format:
     * Display: "[ ] Error: Invalid chapter specification - {input}"
     * Stop execution

**Sync each chapter:**

1. **Display sync progress:**
   - Display: "📚 Syncing {count} chapters..."

2. **For each chapter directory:**
   - Check if directory exists
   - If not, skip to next chapter
   
3. **Process chapter:**
   - Extract chapter number from directory name (e.g., "ch001"  ->  1)
   - Calculate issue number: chapter_num + 1 (Issue #2 is Chapter 1)
   - Set content path: `{ch_dir}/content.md`
   - Set meta path: `{ch_dir}/meta.json`
   
4. **Check content exists:**
   - If content.md doesn't exist:
     * Display: "⏭️ Chapter {num}: No content to sync"
     * Skip to next chapter
   
5. **Read chapter data:**
   - Use Read tool on content file to get chapter content
   - Check if meta.json file exists:
     * If exists: Use Read tool on meta.json to get metadata
     * If not exists: Use empty metadata {}
   
   **Create formatted issue content:**
   - Format markdown content with:
     * Title: from meta['title'] or default "Chapter N"
     * Status: from meta['status'] or 'draft'
     * Word Count: from meta['word_count'] or count words in content
     * Quality Score: from meta['quality_score'] or 'N/A'
     * Last Updated: current timestamp
     * Full chapter content
     * Metadata section with stream scores, generation time, agents used
     * Footer with sync timestamp
   
   - Use Write tool to save formatted content to `.claude/temp/chapter_{ch_num}.md`
    
8. **Check if issue exists:**
   - Use Bash tool: `gh issue view {issue_num} --json state`
   - If command fails: Issue doesn't exist, create it
   - If command succeeds: Issue exists, update it

9. **Create new issue (if doesn't exist):**
   - Get chapter title from metadata or use default
   - Use Bash tool: `gh issue create --title "📚 Chapter {num}: {title}" --body-file .claude/temp/chapter_{num}.md --label "chapter,novel"`
   - If successful:
     * Display: "[x] Chapter {num}: Created as Issue #{issue_num}"
     * Increment sync_count
   - If failed:
     * Display: "[ ] Error: Chapter {num} - Failed to create"
     * Increment error_count

10. **Update existing issue (if exists):**
    - Use Bash tool: `gh issue edit {issue_num} --body-file .claude/temp/chapter_{num}.md`
    - If successful:
      * Display: "[x] Chapter {num}: Updated Issue #{issue_num}"
      * Increment sync_count
    - If failed:
      * Display: "[ ] Error: Chapter {num} - Failed to update"
      * Increment error_count

**Display sync summary:**

1. **Show summary header:**
   - Display decorative box with "📊 Sync Summary"

2. **Show sync statistics:**
   - Display: "Successfully Synced: {sync_count} items"
   - Display: "Failed: {error_count} items"

3. **Show helpful commands:**
   - Display: "View issues online:"
   - Display: "  gh issue list --label novel"
   - Display: "View specific chapter:"
   - Display: "  gh issue view [issue_number]"

4. **Show recommendations:**
   - Display: "Next sync recommendation:"
   - Display: "  After completing next chapter or major revisions"