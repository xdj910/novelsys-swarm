---
description: Complete and archive the current book
---

# Complete and Archive Book

## Execution Steps

### 1. Verify Current Project

**Load current project information:**
- Use Read tool: `.claude/data/context/current_project.json`
- Extract project_name from current["project"]

**Load project metadata:**
- Use Read tool: `.claude/data/projects/{project_name}/project.json`
- Store as project data

**Verify completion status:**
- If completed_chapters < total_chapters:
  * Calculate remaining chapters: total - completed
  * Display: "WARNING:️ Warning: X chapters not yet completed"
  * Display prompt: "是否仍要完成这本书？(部分完成)"
  * Wait for user confirmation

### 2. [ENHANCED] Final Quality Validation

**Load enhanced context:**
- Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/shared`
- Set entity_dict_path to ".claude/data/projects/{project_name}/shared/entity_dictionary.yaml"
- Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/bible.yaml`
- Extract project_genre from bible data

**Display validation message:**
- Print: "🔍 Running final quality validation with v2.0 system..."

**Run comprehensive quality check:**
- Use Task tool with quality-scorer agent
- Provide prompt: "Final quality assessment for complete book"
- Include genre and entity dictionary path in prompt
- Specify 95+ standard requirement
- Store result as final_quality

**Check quality threshold:**
- If final_quality score < 95:
  * Display warning with actual score
  * Suggest: "Consider running /novel:smart-fix all before completing"

### 3. Merge All Chapters

**Find all chapter files:**
- Use Glob tool: `.claude/data/projects/{project_name}/chapters/*/content.md`
- Sort chapters list to ensure correct order

**Initialize full book content:**
- Create empty full_book list

**Add book title and metadata:**
- Append title: "# {project_name}"
- Append author: "作者：AI创作助手"
- Append creation period: "创作时间：{created} - {current_timestamp}"
- Append total words: "总字数：{total_words}"
- Append separator: "---"

**Add table of contents:**
- Append "## 目录" header
- For each chapter file (numbered 1, 2, 3...):
  * Use Read tool on meta.json file (replace content.md with meta.json)
  * Extract title from metadata
  * Append: "{number}. {title or '第{number}章'}"
- Append separator: "---"

**Add all chapters:**
- For each chapter file:
  * Use Read tool on content.md file
  * Use Read tool on corresponding meta.json file
  * Append chapter header: "## {title or '第{chapter_number}章'}"
  * Append chapter content
  * Append separator: "---"

**Join all parts:**
- Combine all full_book list items into single full_book_text string

### 4. Generate Book Summary

**Create comprehensive summary:**
- Use Task tool with quality-scorer agent
- Provide prompt: "为完整作品生成总结"
- Include first 5000 characters of full_book_text
- Include project_genre and entity_dict_path
- Specify 95+ quality standard
- Store result as book_summary

### 5. Create Archive

**Create archive directory:**
- Generate archive_name: "{project_name}_{current_timestamp}"
- Set archive_path: ".claude/data/completed/{archive_name}"
- Use Bash tool: `mkdir -p {archive_path}`

**Save full book:**
- Use Write tool: `{archive_path}/full_book.md`
- Write full_book_text content

**Save metadata:**
- Build metadata object with:
  * title: project_name
  * type: project type
  * genre: from bible or "未分类"
  * completed_date: current_timestamp
  * creation_period: start, end, calculated days
  * statistics: chapters, words, averages, quality score
  * summary: book_summary
- Use Write tool: `{archive_path}/metadata.json`

**Copy Bible for reference:**
- Use Bash tool: `cp .claude/data/projects/{project_name}/book_{current_book}/bible.yaml {archive_path}/`

**Generate statistics report:**
- Build statistics object with:
  * creation_timeline: analyze creation timeline
  * quality_progression: analyze quality progression
  * word_count_by_chapter: analyze word distribution
  * character_appearances: analyze character usage
- Use Write tool: `{archive_path}/statistics.json`

### 6. Export in Multiple Formats

**Export as PDF:**
- Use Bash tool: `pandoc {archive_path}/full_book.md -o {archive_path}/full_book.pdf`
- If command fails, display: "PDF导出不可用"

**Export as EPUB:**
- Use Bash tool: `pandoc {archive_path}/full_book.md -o {archive_path}/full_book.epub`
- If command fails, display: "EPUB导出不可用"

**Create plain text version:**
- Remove markdown formatting from full_book_text
- Use Write tool: `{archive_path}/full_book.txt`
- Write plain text content

### 7. Update Project Status

**Mark project as completed:**
- Update project data:
  * status: "completed"
  * completed_date: current_timestamp
  * archive_path: archive_path
- Use Write tool: `.claude/data/projects/{project_name}/project.json`

**Clear current project (optional):**
- Create new current project data:
  * project: null
  * previous_project: project_name
  * completed_at: current_timestamp
- Use Write tool: `.claude/data/context/current_project.json`

## Success Output

```
🎉 恭喜！《{project_name}》已完成并归档！

📊 作品统计
===========================================================
📖 标题: {project_name}
📚 体裁: {genre}
📅 创作周期: {creation_days} 天
   开始: {created_date}
   完成: {completed_date}

章节: {completed_chapters}/{total_chapters} 章
字数: {total_words:,} 字
平均每章: {avg_words:,.0f} 字
质量评分: {quality_score}/100

📁 归档位置
===========================================================
{archive_path}/
+-- full_book.md       (Markdown版本)
+-- full_book.txt      (纯文本版本)
+-- full_book.pdf      (PDF版本 - 如可用)
+-- full_book.epub     (EPUB版本 - 如可用)
+-- metadata.json      (元数据)
+-- statistics.json    (统计分析)
+-- bible.yaml         (创作Bible - from book_{current_book}/)

📝 作品概要
---------------------------------------------------------
{book_summary[:500]}...

💡 下一步建议
---------------------------------------------------------
1. /novel:project-new [新项目名] - 开始新的创作项目
2. /novel:project-list - 查看所有项目
3. 在 {archive_path} 查看完整作品

🎊 祝贺完成创作！
```