# NOVELSYS-SWARM 使用指南

## 快速开始

### 1. 初始化系统
```bash
/novel:init
```
创建必要的目录结构和初始配置。

### 2. 创建新小说项目（一体化流程）
```bash
/novel:project-new "我的都市小说"
```

**自动执行以下步骤：**
1. 🧠 **头脑风暴收集信息**
   - 项目类型（系列/独立/短篇集/连载）
   - 小说类型和风格
   - 目标读者群体
   - 预计规模
   - 核心卖点

2. 📁 **创建智能项目结构**
   - 基础目录：chapters/, context/, scenes/
   - 系列小说额外：series_bible/, book_bibles/
   
3. 📝 **自动生成Bible**
   - 基于头脑风暴结果生成完整Bible
   - 保存到：`.claude/data/projects/我的都市小说/bible.yaml`

4. 🎯 **初始化上下文跟踪**
   - characters.json - 角色发展
   - plot.json - 剧情进展
   - world.json - 世界设定

### 3. 生成第一章
```bash
/novel:chapter-start 1
```
基于Bible生成第一章内容。

### 4. 继续写作
```bash
/novel:next-chapter
```
继续创作下一章。

## 项目管理

### 查看当前状态
```bash
/novel:status
```
显示当前项目进度和状态。

### 列出所有项目
```bash
/novel:project-list
```
查看所有创建的小说项目。

### 切换项目
```bash
/novel:project-switch "另一本小说"
```
切换到另一个项目继续创作。

### 完成归档
```bash
/novel:book-complete
```
将完成的小说归档到completed目录。

## 文件结构

每个项目的文件组织：
```
.claude/data/projects/[项目名]/
+-- project.json        # 项目元数据
+-- bible.yaml          # Bible配置
+-- chapters/           # 章节内容
|   +-- ch001/
|   |   +-- content.md  # 章节正文
|   |   +-- meta.json   # 章节元数据
|   +-- ch002/
+-- context/            # 上下文跟踪
|   +-- characters.json # 角色发展
|   +-- plot.json       # 剧情进展
|   +-- world.json      # 世界设定
+-- scenes/             # 场景素材
```

系列小说额外目录：
```
.claude/data/projects/[系列名]/
+-- series_bible/       # 系列总Bible
+-- book_bibles/        # 各本书Bible
+-- ...
```

## 命令列表

### 项目管理命令
- `/novel:init` - 初始化系统
- `/novel:project-new [名称]` - 创建新项目（含头脑风暴+Bible生成）
- `/novel:project-list` - 列出所有项目
- `/novel:project-switch [名称]` - 切换项目
- `/novel:status` - 查看状态
- `/novel:book-complete` - 完成归档

### 创作命令
- `/novel:chapter-start [章节号]` - 开始新章节
- `/novel:next-chapter` - 写下一章
- `/novel:bible-create` - 重新创建或更新Bible（可选）
- `/novel:bible-view` - 查看当前Bible内容

### 辅助命令
- `/novel:analyze` - 分析当前项目
- `/novel:backup` - 备份项目

## 工作流程示例

### 创建都市悬疑小说
```bash
# 1. 创建项目（一体化流程）
/novel:project-new "夜色迷城"
# 系统会自动询问：
# - 项目类型？选择：独立小说
# - 小说类型？输入：都市悬疑
# - 目标读者？选择：成人
# - 预计规模？输入：50章
# - 核心卖点？输入：连环谋杀案背后的惊天秘密
#  ->  自动生成Bible并初始化所有文件

# 2. 生成前三章
/novel:chapter-start 1
/novel:next-chapter
/novel:next-chapter

# 3. 查看进度
/novel:status
# 输出：3/50章完成

# 4. 继续创作...
```

### 管理多个项目
```bash
# 创建第一个项目（含Bible）
/novel:project-new "科幻世界"
#  ->  自动头脑风暴并生成Bible
/novel:chapter-start 1

# 创建第二个项目（含Bible）
/novel:project-new "古风传奇"
#  ->  自动头脑风暴并生成Bible
/novel:chapter-start 1

# 查看所有项目
/novel:project-list

# 切换回第一个项目
/novel:project-switch "科幻世界"
/novel:next-chapter
```

### 创建系列小说
```bash
# 1. 创建系列项目
/novel:project-new "修仙传奇"
# 选择项目类型：系列小说
#  ->  系统会创建series_bible和book_bibles目录

# 2. 开始第一本书
/novel:book-start "筑基之路"
#  ->  基于Series Bible创建Book Bible

# 3. 写作第一本
/novel:chapter-start 1
# ...完成第一本

# 4. 开始第二本书
/novel:book-start "金丹大道"
#  ->  继承第一本的角色发展和世界设定
```

## 注意事项

1. **Bible自动生成**：创建项目时自动生成Bible
2. **自动保存**：所有内容自动保存到项目目录
3. **上下文跟踪**：系统自动追踪角色和剧情发展
4. **质量控制**：每章生成后会进行质量评分

## 故障排除

### 找不到项目
确保先执行 `/novel:project-list` 查看项目名称。

### Bible需要更新
如需重新生成或更新Bible：`/novel:bible-create`

### 章节生成失败
检查：
1. 当前项目是否正确
2. Bible是否已创建
3. 章节号是否连续

## 高级功能

### 场景并行生成
系统自动将章节分解为场景，提高生成效率。

### 4-Stream架构
- 角色心理流
- 叙事结构流
- 世界构建流
- 文学技巧流

### 质量保证
- 自动连贯性检查
- Bible一致性验证
- 角色发展追踪

### Bible演化（系列小说）
```
Series Bible (总纲)
     v 
Book Bible (本书设定)
     v 
Chapter Context (章节上下文)
```

## 获取帮助

如有问题，请查看：
- 实施报告：`IMPLEMENTATION-COMPLETE.md`
- 架构文档：`.claude/docs/ARCHITECTURE.md`
- 命令定义：`.claude/commands/*.md`