# NOVELSYS-SWARM 真实架构理解

## 核心认知：这是一个命令驱动系统

### 系统本质
```
NOVELSYS-SWARM = .claude目录下的命令定义集合
执行者 = Claude (我)
触发方式 = 用户输入命令
```

## 真实的执行流程

### 1. 命令定义（已存在）
```yaml
位置: D:/NOVELSYS-SWARM/.claude/commands/novel/*.md
内容: 每个.md文件定义一个命令的执行流程

例如 chapter-start.md:
---
name: chapter-start
description: Launch parallel swarm generation
tools: [Read, Write, Task, TodoWrite, Bash]
---
# 具体执行步骤...
```

### 2. 用户触发
```bash
用户输入: /novel:chapter-start 1
```

### 3. Claude执行（我的工作）
```python
# 我做的事：
1. 读取命令定义：Read(".claude/commands/novel/chapter-start.md")
2. 解析参数：chapter_number = 1
3. 执行定义的步骤：
   - 加载Bible：Read("data/bibles/series_bible.yaml")
   - 创建工作目录：Bash("mkdir -p data/chapters/ch001")
   - 调用SubAgent：Task(subagent_type="outline-creator", ...)
   - 保存结果：Write("data/chapters/ch001/chapter.md", content)
```

### 4. SubAgent（通过Task工具）
```yaml
SubAgent定义: .claude/agents/*.md
调用方式: Task工具
执行者: 还是Claude，但是独立的上下文

流程:
1. 我调用：Task(subagent_type="scene-generator", prompt="...")
2. 新的Claude实例读取：.claude/agents/generation/scene-generator.md
3. 执行任务并返回结果
4. 我处理返回的结果
```

## 持久化的真实实现

### 谁在使用持久化？
- **Claude（我）**：直接读写文件
- **不是后台服务**：没有daemon进程
- **不是数据库**：就是文件系统

### 如何持久化？
```python
# Bible保存
bible_data = {...}
Write("data/bibles/series_bible.yaml", yaml.dump(bible_data))

# 章节保存
chapter_content = "第一章内容..."
Write("data/chapters/ch001/chapter.md", chapter_content)

# 上下文更新
context = json.load(Read("data/context/current.json"))
context["last_chapter"] = 1
Write("data/context/current.json", json.dumps(context))
```

## "并行"的真实含义

### 不是真并行
```python
# 错误理解：
async def parallel_generation():
    await asyncio.gather(
        agent1.generate(),  # [ ] 没有独立的agent进程
        agent2.generate(),  # [ ] 不能真正并行
    )
```

### 实际的"并行"
```python
# 正确理解：顺序调用多个SubAgent，然后合并结果

# Step 1: 生成多个独立部分
scene1 = Task(subagent_type="scene-generator", prompt="生成开场")
scene2 = Task(subagent_type="scene-generator", prompt="生成发展")
scene3 = Task(subagent_type="scene-generator", prompt="生成高潮")

# Step 2: 智能合并
merged = Task(
    subagent_type="stream-integrator",
    prompt=f"合并场景：{scene1}, {scene2}, {scene3}"
)

# Step 3: 保存结果
Write("data/chapters/ch001/chapter.md", merged)
```

## 命令系统的实际能力

### [x] 能做到的
1. **结构化流程**：通过命令定义复杂的生成流程
2. **专业分工**：不同SubAgent处理不同任务
3. **持久化存储**：所有内容保存为文件
4. **质量控制**：通过多轮验证确保质量
5. **上下文管理**：通过文件系统维护状态

### [ ] 做不到的
1. **真正的并行执行**：所有操作都是顺序的
2. **后台服务**：没有持续运行的进程
3. **实时协作**：SubAgent之间不能直接通信
4. **跨会话记忆**：除非写入文件

## 优化后的实施方案

### 1. 完善命令定义
```yaml
需要的命令:
/novel:bible-create     # 创建Bible
/novel:chapter-start    # 生成章节
/novel:quality-check    # 质量检查
/novel:context-sync     # 同步上下文
/novel:export          # 导出作品
```

### 2. 实现核心Python模块
```python
# src/core/bible_manager.py
class BibleManager:
    """Bible的CRUD操作"""
    def create(self, name, genre): ...
    def load(self, name): ...
    def update(self, name, changes): ...
    def validate(self, bible): ...

# src/core/chapter_generator.py  
class ChapterGenerator:
    """章节生成逻辑"""
    def generate(self, chapter_num, bible): ...
    def validate(self, chapter): ...
    def save(self, chapter): ...

# 这些会被命令通过Bash("python src/xxx.py")调用
```

### 3. 优化SubAgent定义
```yaml
# .claude/agents/generation/outline-creator.md
---
name: outline-creator
tools: [Read, Write]
---
你是大纲创建专家。
输入：Bible + 章节号
输出：详细的章节大纲

执行步骤：
1. 分析Bible理解整体框架
2. 确定本章在整体中的位置
3. 创建5-7个场景的大纲
4. 返回结构化的大纲数据
```

### 4. 建立文件结构
```
D:/NOVELSYS-SWARM/
+-- .claude/
|   +-- commands/       # 命令定义
|   +-- agents/         # SubAgent定义
|   +-- context/        # 上下文模板
+-- src/
|   +-- core/           # Python实现
+-- data/
|   +-- bibles/         # Bible存储
|   +-- chapters/       # 章节存储
|   +-- context/        # 运行时上下文
+-- templates/          # 模板文件
```

## 实际使用流程

### 创建小说
```bash
用户: /novel:bible-create "都市悬疑"
Claude: 
  1. 读取bible-create.md命令定义
  2. 交互式收集信息
  3. 调用SubAgent完善设定
  4. 保存Bible文件
  5. 初始化项目结构
```

### 生成章节
```bash
用户: /novel:chapter-start 1
Claude:
  1. 读取chapter-start.md命令定义
  2. 加载Bible和上下文
  3. 调用多个SubAgent生成场景
  4. 合并场景为章节
  5. 保存章节文件
  6. 更新上下文
```

## 核心洞察

1. **NOVELSYS-SWARM不是程序，是命令集合**
2. **执行者永远是Claude（我）**
3. **"并行"是逻辑并行，不是物理并行**
4. **持久化就是文件读写**
5. **SubAgent是独立的Claude实例，通过Task调用**

这才是系统的真实面貌！