# NOVELSYS-SWARM 实际可行架构
*基于Claude Code能力边界的务实设计*

## 核心理解：Claude Code的真实能力

### 我（Claude）能做什么：
1. **直接文件操作**：Read/Write/Edit任何文件
2. **执行Python脚本**：通过Bash工具运行Python代码
3. **调用SubAgent**：通过Task工具启动专门的子代理
4. **持久化存储**：直接写YAML/JSON/MD文件到磁盘
5. **命令路由**：解析用户命令，执行对应操作

### 我不能做什么：
1. [ ] 运行独立的Agent服务（没有后台进程）
2. [ ] 维护内存数据库（每次对话都是新的）
3. [ ] 真正的并行执行（只能模拟）
4. [ ] 跨会话保持状态（除非写入文件）

## 重新设计：务实的NOVELSYS架构

### 1. 持久化方案（谁用？怎么用？）

```yaml
使用者: Claude（我）
方式: 直接文件操作

目录结构:
D:/NOVELSYS-SWARM/
  data/
    bibles/
      series_bible.yaml         # 系列Bible - 我直接Read/Write
      book_001_bible.yaml       # 书籍Bible - 我维护版本
    chapters/
      book_001/
        chapter_001.md          # 章节内容 - 我生成和保存
        chapter_001_meta.json   # 元数据 - 我记录状态
    context/
      current_context.json      # 当前上下文 - 我每次更新
      memory_bank.json          # 记忆库 - 我累积保存
    logs/
      generation_log.json       # 生成日志 - 我记录过程
```

### 2. 实际工作流程

```python
# 用户输入命令
User: "创建新小说Bible"

# Claude（我）的处理流程：
1. 读取模板：Read("templates/bible_template.yaml")
2. 交互式收集信息
3. 生成Bible：创建数据结构
4. 保存文件：Write("data/bibles/new_series.yaml")
5. 更新上下文：Edit("data/context/current_context.json")

# 如果需要复杂处理，调用SubAgent：
Task(
    subagent_type="bible-architect",
    prompt="基于用户需求细化Bible设置",
    description="细化Bible"
)
```

### 3. "并行"生成的实际实现

```python
# 不是真并行，而是智能分解+顺序执行+合并

async def generate_chapter_practical(chapter_num):
    """Claude实际执行的章节生成"""
    
    # 1. 读取Bible和上下文
    bible = yaml.load(Read("data/bibles/series_bible.yaml"))
    context = json.load(Read("data/context/current_context.json"))
    
    # 2. 分解场景（顺序执行，但独立生成）
    scenes = []
    for scene_id in ["opening", "development", "climax", "resolution"]:
        # 调用SubAgent生成场景
        scene = Task(
            subagent_type="scene-generator",
            prompt=f"生成{scene_id}场景，基于Bible：{bible}",
            description=f"生成{scene_id}"
        )
        scenes.append(scene)
        
        # 立即保存（增量持久化）
        Write(f"data/chapters/temp/scene_{scene_id}.md", scene)
    
    # 3. 智能合并
    merged = Task(
        subagent_type="stream-integrator",  
        prompt=f"合并场景：{scenes}",
        description="合并场景"
    )
    
    # 4. 保存最终章节
    Write(f"data/chapters/book_001/chapter_{chapter_num:03d}.md", merged)
    
    # 5. 更新上下文
    context["last_chapter"] = chapter_num
    Write("data/context/current_context.json", json.dumps(context))
```

### 4. SubAgent的实际使用

```yaml
SubAgent定义位置:
  .claude/agents/*.md          # Agent定义文件

调用方式:
  - Claude读取定义：Read(".claude/agents/bible-architect.md")
  - 通过Task工具调用：Task(subagent_type="bible-architect", ...)
  - SubAgent返回结果
  - Claude处理并保存结果

SubAgent类型:
  1. 分析型：bible-architect, scene-analyzer
  2. 生成型：chapter-generator, dialogue-specialist
  3. 优化型：quality-scorer, pacing-optimizer
  4. 验证型：consistency-guardian
```

### 5. 命令系统（用户界面）

```python
# 用户通过命令与系统交互
可用命令:
  /bible-create [名称]        # 创建新Bible
  /chapter-generate [编号]    # 生成章节
  /scene-analyze [章节]       # 分析场景
  /quality-check              # 质量检查
  /export [格式]              # 导出作品

实现方式:
  1. Claude解析命令
  2. 读取相关文件
  3. 执行Python脚本或调用SubAgent
  4. 保存结果到文件
  5. 向用户报告完成
```

## 关键洞察：简化但有效

### 放弃的复杂特性：
- [ ] 真正的多Agent并行（改为：顺序执行+智能合并）
- [ ] 内存数据库（改为：JSON文件缓存）
- [ ] 后台服务（改为：按需执行）
- [ ] 复杂的进程间通信（改为：文件共享）

### 保留的核心价值：
- [x] Bible驱动的一致性
- [x] 场景分解与组合
- [x] 质量验证机制
- [x] 上下文持久化
- [x] SubAgent专业分工

## 实施步骤（真正可执行）

### Step 1: 建立数据目录结构
```bash
# Claude执行
mkdir -p data/bibles data/chapters data/context data/logs
```

### Step 2: 创建核心命令脚本
```python
# src/commands/bible_create.py
def create_bible(name, genre, setting):
    """Claude调用的Bible创建函数"""
    bible = {
        "name": name,
        "genre": genre,
        "setting": setting,
        "characters": {},
        "world": {},
        "created": datetime.now().isoformat()
    }
    
    # 保存到文件
    with open(f"data/bibles/{name}.yaml", "w") as f:
        yaml.dump(bible, f)
    
    return bible
```

### Step 3: 实现简化的生成流程
```python
# src/core/simple_generator.py
class SimpleChapterGenerator:
    """Claude直接调用的章节生成器"""
    
    def generate(self, chapter_num):
        # 1. 加载Bible
        bible = self.load_bible()
        
        # 2. 生成场景（顺序）
        scenes = []
        for scene_type in ["opening", "development", "climax"]:
            scene = self.generate_scene(scene_type, bible)
            scenes.append(scene)
        
        # 3. 合并成章节
        chapter = "\n\n".join(scenes)
        
        # 4. 保存
        self.save_chapter(chapter_num, chapter)
        
        return chapter
```

### Step 4: 设置SubAgent配置
```yaml
# .claude/agents/scene-generator.md
---
name: scene-generator
tools: [Read, Write]
---
你是场景生成专家。根据提供的Bible和场景类型，生成对应的场景内容。

输入：
- Bible内容
- 场景类型（opening/development/climax/resolution）
- 前置场景（如果有）

输出：
- 生成的场景文本（500-800字）
- 场景元数据（人物、地点、情绪）
```

## 成功标准（务实版）

### 可验证的目标：
1. **今天**：能创建和保存Bible文件
2. **本周**：能生成单个章节并保存
3. **下周**：能生成完整的3章短篇
4. **本月**：质量评分系统运作

### 放弃的目标：
- [ ] 实时多Agent协作
- [ ] 真正的并行处理
- [ ] 复杂的状态机
- [ ] 分布式架构

## 总结：少即是多

**核心哲学**：
- 利用Claude Code的文件操作能力
- 通过文件系统实现持久化
- 用SubAgent实现专业分工
- 顺序执行+智能合并替代并行
- 简单可靠胜过复杂易错

**实际能做到的**：
1. 创建结构化的Bible
2. 基于Bible生成一致的章节
3. 保存所有生成内容
4. 追踪生成历史
5. 保证质量标准

这才是Claude Code环境下真正可行的架构！