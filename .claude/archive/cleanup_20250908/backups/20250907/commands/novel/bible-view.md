---
description: View and analyze project Bible content
argument-hint: [section]
---

# Bible View Command

Display the project Bible with formatting and optional section filtering.

## Command Usage

- `/novel:bible-view` - View entire Bible
- `/novel:bible-view characters` - View only characters section
- `/novel:bible-view plot` - View only plot section
- `/novel:bible-view world` - View only world/universe section

## Execution Steps

### Step 1: Identify Current Project

Read current project configuration:
- Use Read tool: `.claude/data/context/current_project.json`
- Extract the `project` field from the JSON

If no project found, display:
```
No active project. Use /novel:project-switch <project_name> first
```

### Step 2: Load Bible File

First get current book from project.json, then check if Bible exists using Read tool:
```
@.claude/data/projects/**$PROJECT_NAME**/project.json (get current_book, default: 1)
@.claude/data/projects/**$PROJECT_NAME**/book_{current_book}/bible.yaml
```

If file not found:
```
Bible not found for project: **$PROJECT_NAME**
Use /novel:bible-create to generate one
```

### Step 3: Parse and Display Bible

When this command runs, Claude will:
1. Use Read tool to read the Bible YAML file
2. Parse and format the content based on **$ARGUMENTS** (section filter)
3. Display formatted output with bilingual annotations

#### Full Bible Display (no arguments)
```
PROJECT BIBLE: [Project Name]
===============================================

📚 SERIES METADATA / 系列元数据
--------------------------------
Title: [Title in English]
标题: [中文标题]
Genre: Mystery/Thriller
类型: 悬疑/惊悚
Target: 50 chapters, 200,000 words
目标: 50章, 20万字

👥 CHARACTERS / 角色
--------------------------------
[Main Protagonist]
主角: [中文名]
- Role: [Description]
  角色: [描述]
- Personality: [Traits]
  性格: [特征]
- Background: [History]
  背景: [历史]

[Supporting Characters...]

🌍 UNIVERSE/WORLD / 世界设定
--------------------------------
Setting: [Location, Time Period]
场景: [地点, 时代]

Locations / 地点:
1. [Location Name] / [中文地名]
   - Description / 描述: [Details]
   - Significance / 重要性: [Plot relevance]

📖 PLOT STRUCTURE / 剧情结构
--------------------------------
Main Arc / 主线:
[Plot summary]
[中文剧情概要]

Key Events / 关键事件:
1. [Event] / [中文事件]
2. [Event] / [中文事件]

🎭 THEMES / 主题
--------------------------------
Core Themes / 核心主题:
- [Theme]: [Description]
  [中文主题]: [描述]

💬 VOICE PROFILE / 语言风格
--------------------------------
Narrative Style / 叙事风格:
- [Style description]
  [中文风格描述]

Character Speech / 角色语言:
- [Character]: [Speech pattern]
  [角色]: [说话方式]
```

#### Section Display (with argument)
Display only the requested section with bilingual headers.

### Step 4: Provide Analysis Summary

Use Task tool to analyze Bible completeness:
```
!bash -c "grep -c 'characters:' bible.yaml && grep -c 'universe:' bible.yaml && grep -c 'plot_structure:' bible.yaml"
```

Then display analysis summary:

```
📊 BIBLE ANALYSIS / Bible分析
-----------------------
Completeness / 完整度: 95%
Characters Defined / 已定义角色: 12
Locations Mapped / 已设定地点: 8
Plot Points / 剧情点: 24
Foreshadowing Setup / 伏笔设置: 15

WARNING:️ Warning: MISSING ELEMENTS:
- [Any missing required sections]
- [建议补充的部分]

💡 SUGGESTIONS / 建议:
1. Consider adding more supporting character backstories
   考虑增加更多配角背景故事
2. Expand world-building for key locations
   扩展关键地点的世界观设定
```

### Step 5: Display Navigation Options

Show available related commands:

```
📤 RELATED COMMANDS / 相关命令:
1. /novel:bible-create - Create or regenerate Bible
2. /novel:chapter-start 1 - Start writing with this Bible
3. /novel:status - View project status
4. /novel:project-switch - Switch to another project
```

## Bilingual Support Strategy

Since Bible is typically generated in English, provide:

1. **Inline Translation**: Key terms shown bilingually
2. **Section Headers**: Both English and Chinese
3. **Character Names**: Show both versions if applicable
4. **Quick Translation**: Offer command to generate full Chinese version


## Display Features

### Syntax Highlighting
- Use color codes for different sections
- Highlight missing or incomplete sections in yellow
- Mark validation errors in red

### Section Navigation
```
QUICK JUMP / 快速跳转:
[C]haracters | [P]lot | [W]orld | [T]hemes | [V]oice
[角]色 | [剧]情 | [世]界 | [主]题 | [语]言
```

### Search Within Bible
To search for specific terms in Bible:
```
!grep -i "**$ARGUMENTS**" .claude/data/projects/**$PROJECT_NAME**/book_{current_book}/bible.yaml
```

## Error Handling

- **No Bible**: Suggest `/novel:bible-create`
- **Corrupted Bible**: Offer to restore from backup
- **Invalid Section**: Show available sections
- **Language Issues**: Offer translation options

## Success Output Example

```
[x] Bible loaded successfully / Bible加载成功
📖 Displaying: Full Bible / 显示: 完整Bible
🌐 Language: English with Chinese annotations / 语言: 英文带中文注释

[Bible Content...]

💾 Last modified: 2024-01-15 14:30
📝 Next suggested action: /novel:chapter-start 1
```

## Notes

- Bible is the foundation document, always display clearly
- Bilingual support helps Chinese users understand English Bible
- Section filtering helps focus on specific aspects
- Analysis provides quick health check of Bible completeness
[FILE MAY BE TRUNCATED - PLEASE VERIFY]
