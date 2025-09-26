# Technical Implementation - Research Agent Architecture

## Critical Reality Check

### What We CAN Do (Technically Feasible)
1. **Subagents CAN use WebSearch** ✓
2. **Main Claude CAN trigger agents based on conversation** ✓
3. **Agents CAN save results to knowledge_base** ✓
4. **Multiple agents CAN run in parallel** ✓

### What We CANNOT Do (Technical Limitations)
1. **Subagents CANNOT understand conversation context** ✗
   - They only see the prompt Main Claude gives them
2. **Subagents CANNOT trigger other agents** ✗
   - No Task tool = no recursion
3. **Subagents CANNOT maintain conversation state** ✗
   - Each execution is stateless

## Actual Implementation Pattern

### How Natural Language Triggering REALLY Works

```python
# In Main Claude (has conversation context)
def process_user_message(user_input):
    # Main Claude analyzes user intent
    if "什么火" in user_input or "trending" in user_input:
        # Main Claude decides to research
        prompt = create_research_prompt("trend_analysis", context)
        result = Task(trend_analyzer, prompt)
        # Main Claude integrates result into conversation
        response = format_natural_response(result)

    # Main Claude maintains conversation flow
    return response
```

### Real Agent Implementation

#### trend-analyzer Agent
```yaml
---
name: trend-analyzer
description: Analyzes market trends for specified genre or general fiction market
tools: Read, Write, WebSearch, WebFetch
thinking: |
  I need to search for current market trends and save structured data.
  I should perform 2-3 searches to get comprehensive view.
model: claude-sonnet-4-20250514
---

## Core Responsibility
Search for market trends and save analysis to knowledge_base.

## Instructions

You will receive a prompt like:
"Research current fiction market trends, especially [GENRE if specified]"

### Step 1: Plan Research
Based on the prompt, determine:
- General market scan or specific genre?
- What year/timeframe to focus on?
- What metrics matter (growth %, revenue, units)?

### Step 2: Execute Searches
Perform 2-3 WebSearch queries:
1. "[current year] fiction market trends growth"
2. "[genre] book sales statistics [year]"
3. "emerging book genres [year] report"

### Step 3: Analyze Results
Extract key data points:
- Genre growth percentages
- Market size and trajectory
- Emerging opportunities
- Declining categories

### Step 4: Structure Output
Save to knowledge_base with timestamp:
```json
{
  "timestamp": "2025-01-15T10:00:00Z",
  "query_type": "market_trends",
  "genre_focus": "mystery",
  "findings": {
    "top_trending": [...],
    "growth_rates": {...},
    "opportunities": [...],
    "avoid": [...]
  },
  "confidence": 0.85,
  "sources": [...]
}
```

### Step 5: Return Summary
Return a brief summary to Main Claude (not the full JSON).
```

## Main Claude's Orchestration Role

### Pattern 1: Single Agent Trigger
```python
# User says: "什么类型的小说现在比较火？"

# Main Claude's internal process:
1. Recognize: User asking about trends
2. Decide: Need trend-analyzer
3. Craft prompt: "Research current fiction market trends for 2025"
4. Execute: Task(trend-analyzer, prompt)
5. Receive: Summary from agent
6. Present: Natural conversation response with insights
```

### Pattern 2: Parallel Multi-Agent
```python
# User says: "我想写tropical mystery，有市场吗？"

# Main Claude's internal process:
1. Recognize: Multiple research needs
2. Decide: Need trend + competitor + audience
3. Craft prompts:
   - "Research mystery genre trends, especially tropical settings"
   - "Analyze competition in tropical/island mystery niche"
   - "Profile readers who enjoy tropical/beach mysteries"
4. Execute parallel:
   - Task(trend-analyzer, prompt1)
   - Task(competitor-scanner, prompt2)
   - Task(audience-profiler, prompt3)
5. Synthesize: Combine all results
6. Present: Comprehensive market assessment
```

## Key Design Decisions

### 1. Main Claude as Conversation Manager
- **Maintains context** across entire conversation
- **Interprets intent** from natural language
- **Decides research needs** based on discussion
- **Crafts specific prompts** for agents
- **Synthesizes results** into natural responses

### 2. Agents as Specialized Workers
- **Receive specific prompts** (not conversation history)
- **Execute focused research** (2-5 searches)
- **Save structured data** to knowledge_base
- **Return summaries** to Main Claude

### 3. Knowledge Base as Memory
```
knowledge_base/
  /20250115_100000_trends.json       # From trend-analyzer
  /20250115_100100_competitors.md    # From competitor-scanner
  /20250115_100200_audience.yaml     # From audience-profiler
  /20250115_110000_synthesis.md      # Main Claude combines all
```

## Implementation Example: trend-analyzer

```markdown
---
name: trend-analyzer
description: Market trend research specialist
tools: Read, Write, WebSearch
thinking: |
  Execute strategic market research with 2-3 focused searches.
  Extract actionable data. Save structured results.
---

## Your Task
When prompted, research market trends for the specified genre or general fiction.

## Process

### Receive Input
You'll get prompts like:
- "Research current fiction market trends"
- "Research mystery genre trends for 2025"
- "Find trending subgenres in romance"

### Execute Research
```python
# Search 1: Broad market
search_1 = WebSearch("2025 fiction market trends report")

# Search 2: Specific genre if mentioned
if genre_specified:
    search_2 = WebSearch(f"{genre} book sales growth 2024-2025")

# Search 3: Opportunities
search_3 = WebSearch(f"emerging {genre} subgenres trending")
```

### Structure Findings
Create JSON with:
- Top 5 trending genres/subgenres
- Growth percentages
- Market gaps identified
- Reader demand indicators
- Confidence level (0-1)

### Save Results
Write to: `knowledge_base/trend_analysis_{timestamp}.json`

### Return Summary
Brief 2-3 sentence summary for Main Claude to use in conversation.
```

## Conversation Flow Reality

```
User: "我想写小说"
Main Claude: "What kind of story interests you?"

User: "不确定，什么比较火？"
Main Claude: [Recognizes trend question]
            [Calls: Task(trend-analyzer, "Research current fiction market trends")]
            [Receives summary]
            "Based on current market analysis, mystery is up 45%..."

User: "Mystery竞争会不会太激烈？"
Main Claude: [Recognizes competition concern]
            [Calls: Task(competitor-scanner, "Analyze mystery genre competition")]
            [Receives summary]
            "While competitive, I found underserved niches..."
```

## Technical Constraints & Solutions

### Constraint 1: Agents can't see conversation
**Solution**: Main Claude extracts context and creates focused prompts

### Constraint 2: Agents can't call each other
**Solution**: Main Claude orchestrates all agent calls

### Constraint 3: No shared memory between agents
**Solution**: File system (knowledge_base) for persistence

### Constraint 4: Agents are stateless
**Solution**: Each execution is self-contained with clear inputs/outputs

## This Design IS Feasible Because:

1. **Main Claude has all needed tools** (including Task)
2. **Agents have WebSearch** (confirmed available)
3. **File system enables persistence** (knowledge_base)
4. **Parallel execution works** (multiple Task calls)
5. **Clear separation of concerns** (conversation vs research)

## What This Means for User Experience

**User Sees**: Natural conversation with intelligent research
**User Doesn't See**: Agent orchestration, prompt crafting, file management
**Result**: Feels magical but is technically sound

---

*The key insight: Main Claude is the conductor, agents are the orchestra.*