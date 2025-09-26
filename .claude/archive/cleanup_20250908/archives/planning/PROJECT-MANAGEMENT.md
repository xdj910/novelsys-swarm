# NOVELSYS-SWARM 项目管理系统设计

## 核心问题与解决方案

### 1. 如何保存第一本书？

**问题**：完成一本书后如何归档和保存？

**解决方案**：
```bash
# 完成当前书籍
/novel:book-complete "都市悬疑" 

# 系统自动：
1. 将所有章节合并为完整作品
2. 生成目录和元数据
3. 归档到 data/completed/都市悬疑/
4. 生成完成报告
```

### 2. 如何开始新的第二个小说项目？

**问题**：如何管理多个小说项目？

**解决方案**：
```bash
# 创建新项目
/novel:project-new "科幻冒险"

# 切换项目
/novel:project-switch "科幻冒险"

# 系统维护当前项目指针
data/context/current_project.json
```

### 3. 如何继续一本书的第二章节？

**问题**：如何恢复之前的创作状态？

**解决方案**：
```bash
# 查看当前进度
/novel:status

# 继续下一章
/novel:chapter-continue  # 自动识别下一章

# 或指定章节
/novel:chapter-start 2
```

### 4. 如何查询创作状态？

**问题**：如何知道有哪些项目，进度如何？

**解决方案**：
```bash
# 查看所有项目
/novel:project-list

# 查看项目详情
/novel:project-info "都市悬疑"

# 生成进度报告
/novel:progress-report
```

## 数据结构设计

### 项目组织结构
```
data/
+-- projects/                      # 所有项目
|   +-- 都市悬疑/                 # 项目1
|   |   +-- project.json          # 项目元数据
|   |   +-- bible.yaml            # 项目Bible
|   |   +-- chapters/             # 章节内容
|   |   |   +-- ch001/
|   |   |   |   +-- content.md    # 章节内容
|   |   |   |   +-- meta.json     # 章节元数据
|   |   |   |   +-- scenes/       # 场景文件
|   |   |   +-- ch002/
|   |   +-- context/              # 项目上下文
|   |       +-- characters.json   # 角色状态
|   |       +-- plot.json         # 情节进度
|   |       +-- world.json        # 世界设定
|   |
|   +-- 科幻冒险/                 # 项目2
|       +-- ...
|
+-- current/                       # 当前活动项目（软链接）
|    ->  projects/都市悬疑/
|
+-- completed/                     # 已完成项目
|   +-- 项目名_20250129/
|       +-- full_book.md          # 完整作品
|       +-- metadata.json         # 元数据
|       +-- statistics.json       # 统计信息
|
+-- workspace/                     # 工作区
    +-- temp/                      # 临时文件
```

### 项目元数据 (project.json)
```json
{
  "name": "都市悬疑",
  "type": "standalone",  // standalone/series
  "genre": "mystery",
  "status": "in_progress",  // planning/in_progress/completed
  "created": "2025-01-29T10:00:00",
  "last_modified": "2025-01-29T15:30:00",
  "progress": {
    "total_chapters": 20,
    "completed_chapters": 5,
    "current_chapter": 6,
    "total_words": 15000,
    "completion_percentage": 25
  },
  "quality_metrics": {
    "average_score": 92,
    "consistency": 95,
    "last_check": "2025-01-29T15:00:00"
  }
}
```

### 章节元数据 (meta.json)
```json
{
  "chapter_number": 1,
  "title": "迷雾初现",
  "status": "completed",  // draft/review/completed
  "created": "2025-01-29T10:00:00",
  "modified": "2025-01-29T12:00:00",
  "word_count": 3000,
  "quality_score": 91,
  "scenes": ["opening", "development", "climax", "resolution"],
  "characters": ["张三", "李四"],
  "location": "城市办公楼",
  "summary": "主角初次遭遇神秘事件..."
}
```

## 命令实现

### /novel:project-new
```yaml
# .claude/commands/novel/project-new.md
---
name: project-new
description: Create new novel project
tools: [Write, Bash, Task]
---

1. 创建项目目录结构
2. 初始化project.json
3. 创建空Bible模板
4. 设置为当前项目
5. 返回项目创建成功
```

### /novel:project-switch
```yaml
# .claude/commands/novel/project-switch.md
---
name: project-switch
description: Switch active project
tools: [Read, Write, Bash]
---

1. 验证项目存在
2. 保存当前项目状态
3. 更新current软链接
4. 加载新项目上下文
5. 显示项目信息
```

### /novel:status
```yaml
# .claude/commands/novel/status.md
---
name: status
description: Show current project status
tools: [Read, Glob]
---

1. 读取当前项目
2. 显示项目基本信息
3. 显示进度统计
4. 显示最近活动
5. 推荐下一步操作
```

### /novel:project-list
```yaml
# .claude/commands/novel/project-list.md
---
name: project-list
description: List all projects
tools: [Glob, Read]
---

1. 扫描projects目录
2. 读取每个project.json
3. 生成项目列表：
   - 项目名
   - 状态
   - 进度
   - 最后修改时间
```

### /novel:progress-report
```yaml
# .claude/commands/novel/progress-report.md
---
name: progress-report
description: Generate detailed progress report
tools: [Read, Write, Task]
---

输出格式：
+========================================+
|         项目进度报告                    |
+========================================+
| 活动项目: 3                            |
| 已完成: 1                              |
| 总字数: 45,000                         |
+========================================+
| [都市悬疑] ████████░░ 80% (16/20章)    |
| [科幻冒险] ██░░░░░░░░ 20% (4/20章)     |
| [历史传奇] ██████░░░░ 60% (12/20章)    |
+========================================+
```

## 实际使用流程

### 场景1：开始第一本书
```bash
User: 我要写一本都市悬疑小说

Claude: 创建新项目...
/novel:project-new "都市悬疑"
 ->  项目创建成功

/novel:bible-create
 ->  Bible创建完成

/novel:chapter-start 1
 ->  第一章生成完成
```

### 场景2：保存并开始新书
```bash
User: 第一本书写完了，开始写科幻小说

Claude: 
/novel:book-complete
 ->  《都市悬疑》已归档到 completed/都市悬疑_20250129/

/novel:project-new "科幻冒险"
 ->  新项目创建成功，已切换
```

### 场景3：继续之前的书
```bash
User: 继续写都市悬疑的下一章

Claude:
/novel:project-switch "都市悬疑"
 ->  已切换到《都市悬疑》
 ->  当前进度：第5章已完成

/novel:chapter-continue
 ->  开始生成第6章...
```

### 场景4：查看所有项目状态
```bash
User: 我现在有哪些小说在写？

Claude:
/novel:project-list

📚 项目列表：
1. [进行中] 都市悬疑 - 5/20章 (25%) - 最后更新：2小时前
2. [进行中] 科幻冒险 - 2/15章 (13%) - 最后更新：昨天
3. [已完成] 历史传奇 - 20/20章 (100%) - 完成于：上周
4. [规划中] 爱情故事 - 0/0章 (0%) - 创建于：3天前
```

## 状态追踪系统

### 自动追踪的信息
1. **项目级别**
   - 创建时间
   - 最后修改
   - 总体进度
   - 质量评分

2. **章节级别**
   - 生成时间
   - 字数统计
   - 质量分数
   - 修改历史

3. **会话级别**
   - 当前项目
   - 当前章节
   - 最近操作
   - 下一步建议

### 进度计算公式
```python
def calculate_progress(project):
    # 基于章节完成度
    chapter_progress = completed_chapters / total_chapters * 100
    
    # 基于字数目标
    word_progress = current_words / target_words * 100
    
    # 综合进度
    overall = (chapter_progress * 0.7 + word_progress * 0.3)
    
    return {
        "chapter_progress": chapter_progress,
        "word_progress": word_progress,
        "overall": overall
    }
```

## 实施步骤

### Step 1: 创建项目管理命令（立即）
```bash
# 创建命令文件
touch .claude/commands/novel/project-new.md
touch .claude/commands/novel/project-switch.md
touch .claude/commands/novel/project-list.md
touch .claude/commands/novel/status.md
```

### Step 2: 实现项目目录结构（今天）
```python
# src/core/project_manager.py
class ProjectManager:
    def create_project(self, name, type="standalone"):
        # 创建目录结构
        # 初始化元数据
        # 设置为当前项目
        
    def switch_project(self, name):
        # 保存当前状态
        # 切换项目
        # 加载新状态
        
    def list_projects(self):
        # 扫描所有项目
        # 返回状态列表
        
    def get_status(self):
        # 返回当前项目详细状态
```

### Step 3: 集成到现有命令（本周）
修改现有命令，使其支持项目上下文：
- bible-create  ->  保存到当前项目
- chapter-start  ->  在当前项目中创建
- quality-check  ->  检查当前项目

## 优势

1. **清晰的项目隔离**：每个小说独立管理
2. **完整的状态追踪**：随时知道进度
3. **灵活的切换机制**：多项目并行创作
4. **持久化存储**：不会丢失任何工作
5. **进度可视化**：直观的进度报告

这套系统解决了所有提出的问题，让小说创作变得有序可控！