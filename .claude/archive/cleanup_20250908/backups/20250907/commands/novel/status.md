---
description: Show detailed status of current project
---

# Project Status Report

## Execution Steps

### 1. Get Current Project

**Load current project information:**
- Use Read tool: `.claude/data/context/current_project.json`
- If no project found:
  * Display: "[ ] Error: No active project. Use /novel:project-new to create a new project."
  * Stop execution
- Extract project_name from current["project"]

### 2. Load Project Data

**Load all project-related data:**
- Use Read tool: `.claude/data/projects/{project_name}/project.json` -> project
- Use Read tool: `.claude/data/projects/{project_name}/series_bible.yaml` -> series_bible (if exists)
- Extract current_book from project["progress"]["current_book"] (default: 1)
- Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/bible.yaml` -> bible
- Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/context/characters.json` -> context
- Use Glob tool: `.claude/data/projects/{project_name}/book_{current_book}/chapters/*/content.md` -> chapters

### 3. Calculate Statistics

**Calculate various project statistics:**

1. **Progress calculation:**
   - If total_chapters > 0:
     * progress_pct = (completed_chapters / total_chapters) x 100
   - Otherwise: progress_pct = 0

2. **Time calculations:**
   - created_date = project["created"]
   - last_modified = project.get("last_modified", created_date)
   - days_active = calculate days from created to now

3. **Average words per chapter:**
   - If completed_chapters > 0:
     * avg_words = total_words / completed_chapters
   - Otherwise: avg_words = 0

4. **Estimated completion:**
   - If completed_chapters > 0 AND days_active > 0:
     * chapters_per_day = completed_chapters / days_active
     * remaining_chapters = total - completed
     * If chapters_per_day > 0:
       - days_to_complete = remaining / chapters_per_day
     * Otherwise: days_to_complete = "未知"
   - Otherwise: days_to_complete = "未知"

### 4. Get Recent Activity

**Find recently modified chapters:**

1. **Initialize empty recent_chapters list**

2. **For each chapter_file in chapters:**
   - Use Read tool on meta.json (replace content.md with meta.json)
   - Extract metadata
   - Add to recent_chapters with:
     * number: chapter_number
     * title: title or "第{number}章"
     * modified: modification date
     * status: chapter status
     * words: word_count

3. **Sort and limit results:**
   - Sort by "modified" field (newest first)
   - Take only first 3 chapters

## Output Format

```
╔════════════════════════════════════════════════════════════╗
║                    项目状态报告                              ║
╚════════════════════════════════════════════════════════════╝

📖 项目名称: {project_name}
📚 类型: {project.type} | 体裁: {bible.genre}
📅 创建时间: {created_date}
⏱️ 活跃天数: {days_active}天

进度概览
────────────────────────────────────────────────────────────
章节进度: ████████░░ {progress_pct:.1f}%
         {project.progress.completed_chapters}/{project.progress.total_chapters} 章完成

字数统计: {project.progress.total_words:,} 字
         平均每章 {avg_words:.0f} 字

当前章节: 第 {project.progress.current_chapter} 章
状态: {project.status}

预计完成: {days_to_complete} 天后

质量指标
────────────────────────────────────────────────────────────
平均质量分: {project.quality_metrics.average_score}/100
一致性: {project.quality_metrics.consistency}/100
上次检查: {project.quality_metrics.last_check}

最近活动
────────────────────────────────────────────────────────────
{recent_chapters[0]:
    状态: {status} | {words}字 | {modified}
}

Bible概要
────────────────────────────────────────────────────────────
主角: {bible.characters.protagonists[0].name if protagonists else "未设定"}
背景: {bible.world_building.setting}
核心冲突: {bible.plot_structure.central_conflict}

下一步建议
────────────────────────────────────────────────────────────
{智能推荐基于当前状态:
}

💡 快捷命令:
* /novel:next-chapter        写下一章
* /novel:quality-check       质量检查
* /novel:project-list        查看所有项目
* /novel:next                智能推荐
```

