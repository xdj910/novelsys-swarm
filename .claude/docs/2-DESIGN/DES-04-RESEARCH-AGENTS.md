# MVP Research Agents - 核心六剑客

## Phase 1: MVP必需的6个Agents

### 1. trend-analyzer (趋势分析师)
**触发词**: "什么火", "流行", "趋势", "热门"
**核心功能**: 市场大盘扫描
**典型输出**:
```json
{
  "trending_up": ["Mystery +45%", "Romance +23%"],
  "trending_down": ["SciFi -12%"],
  "emerging": ["Climate Fiction +156%"]
}
```

### 2. competitor-scanner (竞品侦察兵)
**触发词**: "竞争", "已经有", "别人写过"
**核心功能**: 找出市场空白
**典型输出**:
```markdown
## Top 10 Tropical Mysteries
1. Death in Paradise - 250k sales
2. Island Secrets - 180k sales
...
## Market Gap
- No cozy mystery with cooking theme in tropical setting
```

### 3. audience-profiler (读者画像师)
**触发词**: "谁会看", "读者", "受众", "目标人群"
**核心功能**: 精准定位读者
**典型输出**:
```yaml
demographics:
  age: 25-45
  gender: 70% female
  location: US suburban
preferences:
  chapter_length: 2000-3000 words
  violence_level: minimal
  humor: essential
```

### 4. voice-analyzer (声纹分析师)
**触发词**: "写作风格", "怎么写", "什么语气"
**核心功能**: 分析成功作品的声纹，提供3个选项
**典型输出**:
```yaml
option_1:
  name: "Warm Island Friend"
  sample: "I never expected to find..."
  market_fit: 65%
option_2:
  name: "British Observer"
  sample: "One simply doesn't expect..."
  market_fit: 23%
```

### 5. topic-explorer (主题研究员)
**触发词**: "是什么", "不了解", "给我介绍"
**核心功能**: 深度知识研究
**典型输出**:
```markdown
## Cozy Mystery Essentials
- Definition: Light mystery with amateur sleuth
- Key elements: Community, minimal violence, hobby/craft
- Reader expectations: Puzzle-solving, comfort reading
```

### 6. bible-generator (圣经编撰者)
**触发词**: "生成bible", "创建大纲", "开始写作"
**核心功能**: 综合所有研究生成项目圣经
**特殊性**: 读取所有knowledge_base文件，不做WebSearch
**典型输出**:
```yaml
project_bible:
  genre: "Cozy Mystery"
  setting: "Tropical Island"
  voice: "Warm conversational"
  target_audience: "US women 25-45"
  unique_angle: "Cooking + Mystery"
  research_backed: true
```

## 为什么是这6个？

### 覆盖完整创作决策链
```
市场方向 → trend-analyzer
竞争分析 → competitor-scanner
读者定位 → audience-profiler
风格确定 → voice-analyzer
知识补充 → topic-explorer
最终整合 → bible-generator
```

### 对话中的自然触发流
```
"想写小说" → "什么火？" → trend-analyzer
"Mystery不错" → "会不会太多人写？" → competitor-scanner
"有市场空白" → "谁会看这类书？" → audience-profiler
"了解读者了" → "用什么风格写？" → voice-analyzer
"选好风格了" → "生成bible吧" → bible-generator
```

## Phase 2: 可选增强Agents (未来)

### 7. keyword-researcher (SEO优化师)
- 在已经确定写什么之后才需要
- 帮助提高发现率

### 8. pricing-advisor (定价顾问)
- 在作品完成后才需要
- 分析同类作品定价

### 9. cover-trend-analyzer (封面趋势分析)
- 在进入出版阶段才需要
- 视觉营销支持

### 10. review-sentiment-analyzer (评论情感分析)
- 在作品发布后才需要
- 持续改进参考

## 实施优先级

### 第一批实现 (Week 1)
1. trend-analyzer - 最常用，入口级
2. competitor-scanner - 验证可行性
3. topic-explorer - 知识支撑

### 第二批实现 (Week 2)
4. audience-profiler - 精准定位
5. voice-analyzer - 风格确定
6. bible-generator - 最终整合

## 技术实现要点

### 1. 所有研究agents共同特征
```yaml
tools: Read, Write, WebSearch, WebFetch
model: claude-sonnet-4-20250514  # 复杂研究需要
thinking: |
  Multi-stage research with 2-4 searches
  Save structured data to knowledge_base
  Return concise summary to Main Claude
```

### 2. bible-generator特殊性
```yaml
tools: Read, Write  # 不需要WebSearch
model: claude-sonnet-4-20250514
thinking: |
  Read all files in knowledge_base
  Synthesize into coherent bible
  Ensure all decisions are research-backed
```

### 3. 文件命名规范
```
knowledge_base/
  /20250115_100000_trend_analysis.json
  /20250115_101500_competitor_scan.md
  /20250115_103000_audience_profile.yaml
  /20250115_104500_voice_options.yaml
  /20250115_110000_topic_research.md
  /20250115_120000_project_bible.yaml  # 最终输出
```

## 用户体验设计

### 不需要用户记住agent名字
用户只需要自然对话：
- "什么火" → 系统自动调用trend-analyzer
- "有人写过吗" → 系统自动调用competitor-scanner
- 用户甚至不知道有agents在工作

### 智能并行提升效率
```python
# 用户说："我想写tropical cozy mystery，可行吗？"
# Main Claude并行调用：
- trend-analyzer("cozy mystery trends")
- competitor-scanner("tropical mystery competition")
- audience-profiler("cozy mystery readers")
# 3个agents同时工作，效率提升3倍
```

### 渐进式知识构建
每次对话都在丰富knowledge_base：
```
对话1 → 添加trends.json
对话2 → 添加competitors.md
对话3 → 添加audience.yaml
...
最终 → bible.yaml (包含所有智慧)
```

## 成功标准

1. **用户无感知**: 不知道agents存在，只感觉AI很专业
2. **决策有据**: 每个建议都有数据支撑
3. **快速收敛**: 3-5轮对话就能确定方向
4. **可执行输出**: bible.yaml可直接指导创作

---

*6个agents，刚好够用，不多不少。*