---
description: Continue writing the next chapter or resume current chapter
argument-hint: <chapter_number>
---

# Continue Chapter Writing

## Execution Steps

### 1. Identify What to Continue

**Determine which chapter to work on:**

1. **Get current project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - Extract project_name from JSON

2. **Load project metadata:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Extract progress information

3. **Load entity dictionary and genre:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{project_name}/shared`
   - Set entity_dict_path: `.claude/data/projects/{project_name}/shared/entity_dictionary.yaml`
   - Auto-create entity dictionary if missing using entity-dictionary-creator
   - Get current_book from project.json (default: 1)
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/bible.yaml`
   - Detect genre from Bible content

4. **Get current book and chapter progress:**
   - Extract current_book from project["progress"]["current_book"] (default: 1)
   - Extract current_chapter from project["progress"]["current_chapter"]
   - Extract completed_chapters from project["progress"]["completed_chapters"]

5. **Check current chapter status (with validation):**
   - Set chapter_path: `.claude/data/projects/{project_name}/book_{current_book}/chapters/ch{NNN}/`
   - Try Read tool: `{chapter_path}/meta.json`
   - **CRITICAL**: If resuming existing chapter, verify content.md exists:
     * Use Read tool: `{chapter_path}/content.md` 
     * If content.md missing, STOP with error: "Cannot resume chapter - content.md not found at {chapter_path}"
   - If meta.json exists:
     * If meta["status"] != "completed":
       - Set action = "resume"
       - Set target_chapter = current_chapter
       - **Validate**: Ensure content.md exists before proceeding
     * Otherwise:
       - Set action = "new"
       - Set target_chapter = current_chapter + 1
   - If meta.json doesn't exist:
     * Set action = "new"
     * Set target_chapter = current_chapter if > 0, else 1

### 2. Load Context

**Load necessary context for writing:**

1. **Load Bible:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/bible.yaml`
   - Store Bible content for reference

2. **Load project context:**
   - Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/context/characters.json`
   - Store shared context data

3. **Load previous chapter (if applicable):**
   - If target_chapter > 1:
     * Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/chapters/ch{NNN}/content.md`
     * Use Read tool: `.claude/data/projects/{project_name}/book_{current_book}/chapters/ch{NNN}/meta.json`
     * Store as prev_chapter and prev_meta
   - Otherwise:
     * Set prev_chapter = None

### 3. Resume or Start Chapter

**Either resume an incomplete chapter or start a new one:**

**If action == "resume":**

1. **Load existing content:**
   - Use Read tool: `{chapter_path}/content.md`
   - Use Read tool: `{chapter_path}/meta.json`
   - Store as existing_content and existing_meta

2. **Display resume status:**
   - Display: "📝 继续写作第 {target_chapter} 章"
   - Display: "已有内容: {word_count} 字"
   - Display: "场景进度: {scenes_count}/4 场景"

3. **Identify remaining work:**
   - Analyze existing_meta["scenes"] to find what's missing
   - Create list of remaining_scenes to generate

4. **Pre-scene entity validation:**
   - Use Task tool with subagent_type: "entity-validator"
   - Validate existing content and planned scenes against entity dictionary
   - Block continuation if critical naming violations found

5. **Generate remaining scenes:**
   - For each scene_type in remaining_scenes:
     * Use Task tool with subagent_type: "scene-generator"
     * Prompt: "继续第{target_chapter}章，生成{scene_type}场景
       - 已有内容：{existing_content}
       - Entity dictionary: {path} 确保命名一致
       - 类型：{genre}，遵循类型惯例
       - 质量目标：95+分
       - STRICTLY follow entity dictionary naming rules"
     * Append generated scene to existing_content
     * Use Write tool: `{chapter_path}/content.md` with updated content
     * Update existing_meta:
       - Add scene_type to scenes list
       - Update modified timestamp
       - Update word_count
     * Use Write tool: `{chapter_path}/meta.json` with updated metadata
     * Updates will be handled by unified-update-pipeline after quality check

**If action == "new":**

1. **Display new chapter start:**
   - Display: "✨ 开始创作第 {target_chapter} 章"

2. **Plan chapter with director:**
   - Use Task tool with subagent_type: "director"
   - Prompt: "为第{target_chapter}章制定计划
     - Bible：{bible}
     - 前章概要：{prev_summary or '无'}
     - Entity Dictionary: {path}
     - Genre: {genre}
     - Quality requirement: 95+"

3. **Execute chapter generation:**
   - Invoke /novel:chapter-start command with target_chapter
   - This reuses existing chapter-start logic

### 4. Update Project Status

**Update project tracking after chapter work:**

1. **Update project metadata:**
   - Set project["progress"]["current_chapter"] = target_chapter
   - If action == "new" AND chapter completed:
     * Increment project["progress"]["completed_chapters"]
   - Calculate total word count across all chapters
   - Set project["progress"]["total_words"] = calculated total
   - Set project["last_modified"] = current timestamp

2. **Save project metadata:**
   - Use Write tool: `.claude/data/projects/{project_name}/project.json`
   - Write updated project object as JSON

3. **Final context integration:**
   - After quality check >= 95, run: /novel:unified-update-pipeline
   - Prompt: "Final integration for chapter {target_chapter} completion/continuation"
   - Update all project context files with comprehensive changes
   - Set context["current_chapter"] = target_chapter
   - Set context["last_activity"] = "Chapter {target_chapter} - {action}"
   - Use Write tool: `.claude/data/projects/{project_name}/context/characters.json`
   - Write updated context as JSON

## Success Output

### For Resuming Chapter:
```
📝 继续写作《{project_name}》第 {target_chapter} 章

已完成: {completed_scenes}/4 场景
已有字数: {existing_words} 字

正在生成剩余场景...
[x] 场景 {scene_name} 生成完成

章节完成！
总字数: {total_words} 字
质量分: {quality_score}/100

下一步:
- /novel:quality-check {target_chapter} - 质量检查
- /novel:chapter-continue - 继续下一章
```

### For New Chapter:
```
✨ 开始创作《{project_name}》第 {target_chapter} 章

📊 当前进度: {completed_chapters}/{total_chapters} 章完成
📖 前情提要: {prev_summary}

正在制定章节计划...
正在生成章节内容...

[x] 第 {target_chapter} 章创作完成！
字数: {word_count}
质量分: {quality_score}/100

下一步:
- /novel:quality-check {target_chapter} - 质量检查
- /novel:chapter-continue - 继续下一章
- /novel:status - 查看项目状态
```

