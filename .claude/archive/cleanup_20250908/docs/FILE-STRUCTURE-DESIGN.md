# NOVELSYS-SWARM 文件结构设计 v2.0

> 基于小说类型的智能文件组织系统

## 核心设计原则

1. **类型优先**: 先确定小说类型，再决定文件结构
2. **层级清晰**: 项目  ->  系列/单本  ->  书籍  ->  章节
3. **上下文隔离**: 每个项目独立的上下文空间
4. **版本追踪**: 所有内容版本化管理

## 文件结构模式

### 模式1: 系列小说 (Series)
```
projects/
+-- mystery-series/                    # 系列根目录
    +-- .project-type                   # 标识: "series"
    +-- series.yaml                     # 系列元数据
    +-- series-bible.json               # 系列总Bible（跨书籍共享）
    +-- characters/                     # 系列级角色库
    |   +-- protagonists.json
    |   +-- recurring.json
    |   +-- relationships.json
    +-- worldbuilding/                  # 系列级世界观
    |   +-- locations.json
    |   +-- timeline.json
    |   +-- rules.json
    |
    +-- book-01-温泉谜案/               # 第一本
    |   +-- book.yaml                   # 书籍元数据
    |   +-- book-bible.json             # 本书专用Bible（继承系列Bible）
    |   +-- outline.json                # 本书大纲
    |   +-- chapters/
    |   |   +-- ch001/
    |   |   |   +-- chapter.json        # 章节内容
    |   |   |   +-- scenes.json         # 场景分解
    |   |   |   +-- notes.md            # 创作笔记
    |   |   |   +-- versions/           # 版本历史
    |   |   +-- ch002/
    |   |   +-- ...
    |   +-- exports/                     # 导出版本
    |   |   +-- draft-v1.0.docx
    |   |   +-- final-v1.0.epub
    |   +-- quality/                     # 质量报告
    |       +-- quality-report.json
    |
    +-- book-02-雪山密室/               # 第二本
    |   +-- book.yaml
    |   +-- book-bible.json             # 继承并扩展系列Bible
    |   +-- outline.json
    |   +-- chapters/
    |   +-- ...
    |
    +-- .claude/                        # 系列级Claude配置
        +-- context/                     # 持久化上下文
        +-- memory/                      # Agent记忆
```

### 模式2: 单本小说 (Standalone)
```
projects/
+-- the-last-sunset/                    # 单本小说根目录
    +-- .project-type                   # 标识: "standalone"
    +-- book.yaml                       # 书籍元数据
    +-- bible.json                      # 独立Bible
    +-- outline.json                    # 大纲
    +-- characters/                     # 角色设定
    |   +-- main.json
    |   +-- supporting.json
    +-- worldbuilding/                  # 世界观设定
    |   +-- setting.json
    +-- chapters/
    |   +-- ch001/
    |   |   +-- chapter.json
    |   |   +-- scenes.json
    |   |   +-- versions/
    |   +-- ch002/
    |   +-- ...
    +-- exports/
    |   +-- manuscript.docx
    +-- .claude/
        +-- context/
```

### 模式3: 短篇集 (Collection)
```
projects/
+-- midnight-tales/                     # 短篇集根目录
    +-- .project-type                   # 标识: "collection"
    +-- collection.yaml                 # 合集元数据
    +-- collection-theme.json           # 合集主题/风格
    +-- stories/
    |   +-- 01-first-snow/              # 第一个故事
    |   |   +-- story.yaml
    |   |   +-- story.json             # 完整故事内容
    |   |   +-- characters.json
    |   |   +-- versions/
    |   +-- 02-last-train/              # 第二个故事
    |   |   +-- ...
    |   +-- ...
    +-- exports/
    |   +-- collection.epub
    +-- .claude/
```

### 模式4: 连载小说 (Serial)
```
projects/
+-- web-serial-cultivation/             # 连载小说根目录
    +-- .project-type                   # 标识: "serial"
    +-- serial.yaml                     # 连载元数据
    +-- bible.json                      # 总Bible（动态更新）
    +-- arcs/                           # 故事弧
    |   +-- arc-01-foundation/
    |   |   +-- arc.yaml
    |   |   +-- chapters/              # 1-50章
    |   |   +-- arc-bible.json
    |   +-- arc-02-growth/
    |   |   +-- chapters/              # 51-150章
    |   |   +-- arc-bible.json
    |   +-- ...
    +-- daily-updates/                  # 日更管理
    |   +-- schedule.yaml
    +-- .claude/
```

## 项目初始化流程

```yaml
project_initialization:
  step_1_type_selection:
    prompt: "选择小说类型"
    options:
      - series          # 系列小说
      - standalone      # 单本小说
      - collection      # 短篇集
      - serial          # 连载小说
  
  step_2_structure_creation:
    series:
      - create_series_structure()
      - init_series_bible()
      - setup_character_library()
    standalone:
      - create_book_structure()
      - init_standalone_bible()
    collection:
      - create_collection_structure()
      - init_theme_config()
    serial:
      - create_serial_structure()
      - init_arc_system()
  
  step_3_context_initialization:
    - setup_claude_context()
    - configure_agents()
    - init_quality_standards()
```

## 文件命名规范

### 系列小说
```
{series-name}/
  book-{number:02d}-{title}/
    chapters/
      ch{number:03d}/
        chapter.json
```

### 单本小说
```
{book-title}/
  chapters/
    ch{number:03d}/
      chapter.json
```

### 短篇集
```
{collection-name}/
  stories/
    {number:02d}-{story-title}/
      story.json
```

## 上下文继承链

### 系列小说的上下文继承
```
Series Bible (根)
     v  继承
Book Bible (扩展)
     v  继承
Chapter Context (具体)
     v  继承
Scene Context (细节)
```

### 优先级规则
1. 更具体的上下文覆盖通用上下文
2. 本书设定优先于系列设定
3. 当前章节上下文优先于历史上下文

## 版本控制策略

```yaml
version_control:
  bible_versions:
    - major: 结构性改变
    - minor: 内容扩展
    - patch: 错误修正
  
  chapter_versions:
    - draft: 初稿
    - revised: 修订版
    - final: 定稿
    - published: 发布版
  
  backup_strategy:
    - auto_save: 每5分钟
    - version_snapshot: 每次重大修改
    - daily_backup: 每日备份
```

## 质量追踪

每个层级都有质量追踪：
```yaml
quality_tracking:
  series_level:
    - bible_consistency: 98%
    - world_coherence: 95%
  
  book_level:
    - plot_integrity: 95%
    - character_development: 93%
  
  chapter_level:
    - scene_quality: 90%
    - dialogue_authenticity: 92%
```

## 导出管理

```yaml
export_formats:
  drafts:
    - markdown
    - docx
  
  review:
    - pdf
    - html
  
  publication:
    - epub
    - mobi
    - pdf
  
  special:
    - screenplay  # 剧本格式
    - audiobook   # 有声书脚本
```

## 实现优先级

1. **Phase 1**: 实现系列小说和单本小说结构
2. **Phase 2**: 添加短篇集支持
3. **Phase 3**: 添加连载小说支持
4. **Phase 4**: 完善版本控制和导出功能

这样的结构设计确保了：
- [x] 不同类型小说有合适的组织方式
- [x] 上下文和Bible正确继承
- [x] 文件不会混乱堆积
- [x] 便于版本管理和质量追踪
- [x] 支持多种导出格式