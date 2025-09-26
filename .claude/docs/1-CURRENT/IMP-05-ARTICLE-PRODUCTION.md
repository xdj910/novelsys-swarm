# IMP-05-ARTICLE-PRODUCTION - 理性AI文章生产系统集成

## 系统整合架构

### 核心理念
将"理性AI"文章作为一种特殊的创作类型，复用现有基础设施，扩展专门功能。

```
现有系统                     新增组件
---------                   ---------
/brainstorm
    ↓
project-manager
    ↓
brainstorm-coordinator → [Article Mode] → article-coordinator
    ↓                                          ↓
Research Agents ←────────────────────→ Article Production Agents
(复用现有6个)                           (新增4个)
```

## 文章项目结构

```
.claude/data/projects/{timestamp}_ai_article_{topic}/
├── project.json                    # 项目元数据
├── strategy/
│   ├── content_strategy.md        # 100篇战略（全局共享）
│   └── author_voice.md            # 作者声纹（全局共享）
├── brainstorm/
│   ├── session_state.json         # 头脑风暴记录
│   └── topic_proposal.json        # 主题提案
├── research/
│   ├── trends/                    # trend-analyzer 输出
│   ├── competitors/               # competitor-scanner 输出
│   ├── cases/                     # 案例收集（新）
│   │   ├── case_001.json
│   │   └── sources.json          # 来源追踪
│   └── keywords/                  # SEO研究
├── drafts/
│   ├── v1_draft.md               # 初稿
│   ├── v2_edited.md              # 修改稿
│   └── final.md                  # 终稿
├── quality/
│   ├── score.json                # 质量评分
│   ├── plagiarism_check.json    # 原创性检查
│   └── seo_analysis.json        # SEO分析
├── visuals/
│   ├── prompts.json              # Nano Banana 提示词
│   ├── cover.png                 # 封面图
│   └── illustrations/            # 内文配图
└── published/
    ├── medium.md                 # Medium版本
    ├── substack.md               # Substack版本
    ├── vocal.md                  # Vocal版本
    └── metrics.json              # 发布后追踪
```

## 工作流集成

### Phase 1: 项目初始化（复用现有）
```yaml
触发: /brainstorm
执行:
  1. project-manager 创建项目
  2. 选择类型: "Article (理性AI系列)"
  3. brainstorm-coordinator 引导主题选择
  4. 基于战略文档验证主题
```

### Phase 2: 研究阶段（混合模式）
```yaml
复用现有agents:
  - trend-analyzer: 分析相关趋势
  - competitor-scanner: 竞品文章分析

新增agent调用:
  - case-collector: 收集真实案例
    输入: 主题关键词
    输出: cases/*.json
```

### Phase 3: 写作阶段（新增）
```yaml
新增agents:
  - article-writer: 基于模板和案例撰写
    输入: 案例+大纲+声纹
    输出: drafts/v1_draft.md

  - quality-checker: 多维度质量检测
    输入: draft.md
    输出: quality/score.json
```

### Phase 4: 视觉阶段（新增）
```yaml
新增agent:
  - visual-creator: 生成Nano Banana提示词
    输入: 文章主题+风格指南
    输出: visuals/prompts.json
    注: 实际图片生成在Main Claude执行
```

### Phase 5: 发布阶段（新增）
```yaml
新增agent:
  - publisher: 多平台适配
    输入: final.md + 平台要求
    输出: published/*.md
```

## 新增 Agents 设计

### 1. article-coordinator
```yaml
位置: .claude/agents/article-coordinator.md
职责: 协调文章生产全流程
工具: Read, Write, Bash, Grep
输出: JSON执行计划
```

### 2. case-collector
```yaml
位置: .claude/agents/case-collector.md
职责: 搜集和验证真实案例
工具: WebSearch, WebFetch, Read, Write
特性:
  - 交叉验证来源
  - 去重检查
  - 引用标注
```

### 3. article-writer
```yaml
位置: .claude/agents/article-writer.md
职责: 基于框架撰写文章
工具: Read, Write
特性:
  - 遵循声纹模板
  - 整合案例数据
  - SEO优化
```

### 4. quality-checker
```yaml
位置: .claude/agents/quality-checker.md
职责: 全方位质量检测
工具: Read, Write, Grep
检测项:
  - 原创性
  - 可读性
  - 数据准确性
  - SEO优化度
```

### 5. visual-creator
```yaml
位置: .claude/agents/visual-creator.md
职责: 设计视觉方案
工具: Read, Write
输出: Nano Banana提示词模板
```

## 命令扩展

### 增强 /brainstorm
```markdown
当选择 "Article" 类型时:
1. 子类型选择:
   - 理性AI系列
   - 通用博客
   - 深度分析

2. 如果选择"理性AI系列":
   - 自动加载战略文档
   - 检查主题是否重复
   - 建议下一个主题
```

### 新增 /article 命令
```markdown
专门的文章管理命令:
- /article new    - 创建新文章项目
- /article status - 查看所有文章状态
- /article check  - 运行质量检测
- /article publish - 执行发布流程
```

## 数据共享机制

### 全局战略库
```
.claude/strategy/
├── ai_realist/
│   ├── content_strategy.md      # 100篇战略
│   ├── author_voice.md          # 声纹定义
│   └── topics_tracker.json      # 已写主题
└── templates/
    ├── article_structure.md
    └── quality_rubric.md
```

### 防重复数据库
```json
{
  "articles_db": {
    "location": ".claude/strategy/ai_realist/articles_db.json",
    "structure": {
      "articles": [
        {
          "id": "001",
          "project_id": "20250117_ai_article_mcdonalds",
          "main_cases": ["McDonald's"],
          "keywords": ["AI失败", "餐饮"],
          "published": "2025-01-17"
        }
      ]
    }
  }
}
```

## 自动化可能

### 批量操作
```yaml
场景: 每周生产3-4篇
实现:
  1. 周一运行 trend-analyzer 获取热点
  2. 自动生成3个主题提案
  3. 人工确认后批量创建项目
  4. 并行执行研究阶段
```

### 模板化生产
```yaml
模板类型:
  - 案例分析型（McDonald's模板）
  - 数据对比型（ROI计算模板）
  - 指南型（5步框架模板）

自动匹配:
  根据主题自动选择模板
```

## 质量保证

### 三层审核
```yaml
Layer 1 - 自动检测:
  - quality-checker agent
  - 原创性 > 80%
  - 可读性 > 60

Layer 2 - AI审核:
  - 让 claude-code-expert audit
  - 检查论据充分性
  - 验证数据准确性

Layer 3 - 人工确认:
  - 最终审稿
  - 品牌一致性
  - 发布批准
```

## 迭代优化

### 数据驱动改进
```yaml
收集数据:
  - 每篇文章的表现指标
  - 读者反馈分析
  - A/B测试结果

优化方向:
  - 高表现主题 → 深挖系列
  - 低表现主题 → 分析原因
  - 调整内容策略
```

## 实施步骤

### Phase 1: 基础搭建（Week 1）
1. 创建 article-coordinator
2. 创建 case-collector
3. 扩展 /brainstorm 支持Article类型
4. 建立全局战略库

### Phase 2: 核心功能（Week 2）
1. 创建 article-writer
2. 创建 quality-checker
3. 集成现有研究agents
4. 测试完整流程

### Phase 3: 增强功能（Week 3）
1. 创建 visual-creator
2. 添加 /article 命令
3. 实现批量操作
4. 优化自动化

## 成功标准

### 系统层面
- ✅ 完整流程可运行
- ✅ 质量稳定可控
- ✅ 生产效率提升50%
- ✅ 零内容重复

### 业务层面
- ✅ 每周稳定产出3-4篇
- ✅ 平均阅读时间>4分钟
- ✅ 订阅转化>5%
- ✅ 形成品牌认知

---

这个集成方案：
1. 最大化复用现有组件
2. 最小化新增复杂度
3. 保持架构一致性
4. 支持未来扩展