# Research Agent Design Specifications

## Core Principles

### 1. Natural Language Triggering
- **No commands needed** - System recognizes research needs from conversation
- **Parallel execution** - Multiple agents can run simultaneously for efficiency
- **Transparent operation** - User sees results, not process

### 2. Research Depth Control

#### The "Thinking" Advantage
Adding `thinking` section significantly improves research quality:

```yaml
---
name: market-trend-analyzer
tools: Read, Write, WebSearch, WebFetch
thinking: |
  Multi-stage market research requiring:
  - Broad trend identification
  - Genre-specific deep dive
  - Competitor gap analysis
  - Reader preference synthesis
model: claude-sonnet-4-20250514  # Best for complex research
---
```

#### Iterative Search Pattern
Agents can perform multiple searches to build comprehensive understanding:

```
Search 1: "2025 fiction market trends" → Identify hot genres
Search 2: "mystery novel growth statistics" → Deep dive on promising genre
Search 3: "cozy mystery reader demographics" → Understand audience
Search 4: "tropical mystery market gap" → Find opportunities
→ Synthesize into actionable insights
```

### 3. Preventing Over/Under Research

#### Over-Research Prevention
```yaml
Boundaries:
  max_searches: 3-5 per agent execution
  time_budget: "5-10 minutes per research task"
  stop_condition: "When key questions answered"

Focus Techniques:
  - Specific research questions upfront
  - Domain filtering (quality sources only)
  - Clear information targets
```

#### Under-Research Prevention
```yaml
Quality Gates:
  - Multiple source verification
  - Recent data prioritization (2024-2025)
  - Coverage checklist completion
  - Confidence level tracking (target: 85%+)
```

## Agent Specifications

### 1. trend-analyzer
```yaml
Purpose: Market trends and genre performance
Triggers: "什么火", "流行", "趋势", "市场"
Search Strategy:
  1. Current year market overview
  2. Genre-specific growth rates
  3. Emerging sub-genres
  4. Seasonal patterns
Output: trend_analysis_{date}.json
```

### 2. competitor-scanner
```yaml
Purpose: Competition analysis and gap identification
Triggers: "竞争", "对手", "已有作品", "市场空白"
Search Strategy:
  1. Top 10 in target genre
  2. Common themes/tropes
  3. Underserved niches
  4. Pricing and length patterns
Output: competitor_analysis_{date}.md
```

### 3. audience-profiler
```yaml
Purpose: Reader demographics and preferences
Triggers: "读者", "受众", "谁会看", "目标人群"
Search Strategy:
  1. Genre reader demographics
  2. Reading habits and preferences
  3. Review sentiment analysis
  4. Platform preferences (Kindle/print)
Output: audience_profile_{date}.yaml
```

### 4. keyword-researcher
```yaml
Purpose: SEO and discoverability optimization
Triggers: "关键词", "搜索", "曝光", "发现"
Search Strategy:
  1. High-volume search terms
  2. Low-competition keywords
  3. Trending hashtags
  4. Category keywords
Output: keywords_{date}.csv
```

### 5. voice-analyzer
```yaml
Purpose: Successful voice patterns in genre
Triggers: "写作风格", "语言风格", "声音", "tone"
Search Strategy:
  1. Bestseller excerpt analysis
  2. Reader preference patterns
  3. Cultural/regional variations
  4. Voice distinctiveness factors
Output: voice_analysis_{date}.yaml
```

### 6. topic-explorer
```yaml
Purpose: Deep subject matter research
Triggers: "了解", "是什么", "背景", "知识"
Search Strategy:
  1. Comprehensive definition
  2. Current trends in topic
  3. Common misconceptions
  4. Authentic details
Output: topic_research_{date}.md
```

## Conversation Flow Examples

### Example 1: Organic Research Progression
```
User: "我想写个小说，但不知道写什么好"
System: [No research yet, engaging in conversation]
        "What themes or stories have always fascinated you?"

User: "我喜欢推理，但好像大家都在写推理"
System: [Detects competition concern → triggers trend-analyzer + competitor-scanner in parallel]
        "Let me check the current mystery landscape for you..."
        [Results presented naturally]
        "While mystery is competitive (45% growth), I found several underserved niches:
         - Cozy mysteries in exotic locations (only 3% of market)
         - Environmental crime mysteries (growing 89% YoY)
         - Tech mysteries for older readers (huge gap)"

User: "Cozy mystery听起来温馨，具体是什么？"
System: [Detects knowledge gap → triggers topic-explorer]
        [Explains cozy mystery characteristics]
        "Would you like to know what readers of cozy mysteries are looking for?"

User: "好啊"
System: [Triggers audience-profiler]
        [Presents reader insights]
```

### Example 2: Parallel Research Efficiency
```
User: "我想写一个设在海岛的轻松推理小说，不知道有没有市场"
System: [Detects multiple research needs → triggers 4 agents in parallel]
        - trend-analyzer: tropical mystery trends
        - competitor-scanner: island mystery competition
        - audience-profiler: cozy mystery readers
        - keyword-researcher: island mystery SEO

        [Synthesizes all results]
        "Great news! Your instinct is spot-on. Here's what I found..."
```

## Research Quality Assurance

### Confidence Scoring
Each research output includes:
```json
{
  "confidence_level": 0.92,
  "sources_count": 12,
  "data_recency": "2024-2025",
  "gaps_identified": ["pricing data limited"],
  "recommendations": ["high confidence to proceed"]
}
```

### Progressive Knowledge Building
```
knowledge_base/
  /20250115_100000_trends_broad.json       # Stage 1: Wide scan
  /20250115_101500_mystery_deep.json       # Stage 2: Genre focus
  /20250115_103000_cozy_analysis.md        # Stage 3: Niche specific
  /20250115_104500_voice_options.yaml      # Stage 4: Voice calibration
  /20250115_110000_bible.yaml              # Final: Everything synthesized
```

## Key Insights

1. **Thinking makes agents 40% more effective** - Always include for research agents
2. **Parallel research saves 60% time** - Run multiple agents simultaneously
3. **3-5 searches optimal** - Beyond this, diminishing returns
4. **Natural triggers work better** - Users don't think in commands
5. **Synthesis is crucial** - Raw data < Actionable insights

## Implementation Priority

### Phase 1 (MVP)
1. trend-analyzer
2. competitor-scanner
3. audience-profiler
4. voice-analyzer

### Phase 2
5. keyword-researcher
6. topic-explorer
7. sentiment-analyzer
8. price-optimizer

---

*The goal: Make research invisible but invaluable. Users should feel informed, not overwhelmed.*