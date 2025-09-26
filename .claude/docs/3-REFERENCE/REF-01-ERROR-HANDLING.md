# Error Handling Strategy - 避免错误放大

## 核心原则：宁缺毋滥

**不要fallback到不准确的信息，宁可告诉用户需要其他方式研究。**

## 错误处理层级

### Level 1: 完全成功 ✅
```json
{
  "status": "success",
  "confidence": 0.9,
  "summary": "Found comprehensive data from 12 sources",
  "action": "proceed"
}
```

### Level 2: 部分成功 ⚠️
```json
{
  "status": "partial",
  "confidence": 0.6,
  "summary": "Found limited data from 3 sources",
  "missing": "Recent 2025 data unavailable",
  "action": "ask_user"  // 关键：让用户决定
}
```

### Level 3: 失败 ❌
```json
{
  "status": "failed",
  "confidence": 0,
  "error": "WebSearch returned no results",
  "action": "manual_needed"  // 不要猜测
}
```

## 关键设计：用户决策点

### 场景1：部分数据时询问用户
```
System: [trend-analyzer returns partial results]
        "I found some market data but it's from 2023-2024,
         missing recent 2025 trends.

         Options:
         1) Proceed with available data (may be outdated)
         2) You provide recent information manually
         3) Skip market research for now

         What would you prefer?"

User: "Let's proceed with what you have"
// OR
User: "I have a 2025 report, let me tell you..."
```

### 场景2：搜索失败时不要编造
```
System: [competitor-scanner fails]
        "I couldn't find competitor data for 'tropical cooking mysteries'.
         This could mean:
         - It's a truly unique niche (good!)
         - My search needs refinement
         - The data exists but isn't publicly available

         Would you like to:
         1) Try broader search terms
         2) Proceed without competitor data
         3) Provide known competitors manually?"
```

## Agent内部错误处理

### trend-analyzer示例
```python
def execute_research():
    results = []
    confidence = 0

    # Primary search
    try:
        primary = WebSearch("2025 fiction market trends")
        if primary and len(primary) > 5:
            results.extend(primary)
            confidence += 0.5
    except:
        pass  # Don't fail yet

    # Secondary search
    try:
        secondary = WebSearch("2024 publishing industry report")
        if secondary and len(secondary) > 3:
            results.extend(secondary)
            confidence += 0.3
    except:
        pass

    # Determine status
    if confidence >= 0.7:
        return {"status": "success", "confidence": confidence}
    elif confidence >= 0.3:
        return {"status": "partial", "confidence": confidence,
                "missing": "Recent comprehensive data"}
    else:
        return {"status": "failed", "confidence": 0,
                "reason": "Insufficient search results"}
```

## Main Claude的决策树

```python
def handle_agent_response(agent_result):
    if agent_result["status"] == "success":
        # 继续正常流程
        integrate_into_conversation(agent_result["summary"])

    elif agent_result["status"] == "partial":
        # 让用户知情并决定
        present_options_to_user(
            f"Found limited data (confidence: {agent_result['confidence']})",
            missing=agent_result.get("missing"),
            options=["proceed", "manual_input", "skip"]
        )

    else:  # failed
        # 不要假装有数据
        inform_user(
            "Unable to research this automatically.",
            suggest_alternatives=True
        )
```

## 防止错误传播

### 原则1：不传播低质量数据
```python
# WRONG - 错误放大
if market_data["confidence"] < 0.5:
    # 还是用这个数据生成建议
    generate_recommendations(market_data)  # 危险！

# CORRECT - 阻止传播
if market_data["confidence"] < 0.5:
    return {
        "status": "insufficient_data",
        "message": "Need better data before recommendations"
    }
```

### 原则2：标记数据质量
```yaml
# 在bible-generator中
project_bible:
  market_data:
    trends: "Mystery +45%"
    data_quality: "HIGH"  # 明确标记
    data_date: "2024-Q4"
    confidence: 0.9

  competitor_analysis:
    findings: "Limited data"
    data_quality: "LOW"  # 警告
    confidence: 0.3
    recommendation: "Conduct manual research"
```

### 原则3：级联质量检查
```python
# bible-generator的质量门槛
def generate_bible():
    quality_scores = {}

    # 检查每个数据源
    for source in ["trends", "competitors", "audience", "voice"]:
        data = read_knowledge_base(source)
        quality_scores[source] = data.get("confidence", 0)

    # 整体质量评估
    overall_quality = sum(quality_scores.values()) / len(quality_scores)

    if overall_quality < 0.6:
        return {
            "status": "incomplete",
            "message": "Research quality insufficient for reliable bible",
            "weak_areas": [k for k,v in quality_scores.items() if v < 0.5],
            "recommendation": "Improve weak areas before proceeding"
        }
```

## 用户体验设计

### 透明度优先
```
BAD: "Based on my research, tropical mysteries will definitely succeed!"
     (实际上只有30%置信度)

GOOD: "I found limited data on tropical mysteries (3 sources from 2023).
       The available data suggests potential, but I recommend
       additional manual research for confidence."
```

### 选项而非决定
```
BAD: System自动用低质量数据继续

GOOD: System: "Market data is incomplete. How would you like to proceed?
              1) Continue with limited data
              2) Provide additional information
              3) Skip this research step"
```

## 具体实施规则

### 1. WebSearch失败处理
```python
# 不要重试太多次
MAX_RETRIES = 2

# 不要降级到太宽泛的搜索
# WRONG
if specific_search_fails:
    search("books")  # 太宽泛，噪音太多

# CORRECT
if specific_search_fails:
    return failure_with_explanation
```

### 2. 数据时效性
```python
def assess_data_freshness(data_date):
    months_old = calculate_age(data_date)
    if months_old > 12:
        quality_penalty = 0.5
        warning = "Data may be outdated"
    elif months_old > 6:
        quality_penalty = 0.2
        warning = "Recent data preferred"
    else:
        quality_penalty = 0
        warning = None
    return quality_penalty, warning
```

### 3. 冲突数据处理
```python
# 如果不同源数据冲突
if source1_says_growing and source2_says_declining:
    # 不要随意选择一个
    return {
        "status": "conflicting_data",
        "conflict": "Growth trends disputed",
        "source1": {"trend": "up", "confidence": 0.7},
        "source2": {"trend": "down", "confidence": 0.6},
        "action": "require_user_judgment"
    }
```

## 黄金法则

1. **诚实 > 完整**: 宁可说"不知道"也不要猜测
2. **用户控制**: 让用户决定是否接受低质量数据
3. **质量标记**: 永远标明数据置信度
4. **阻止传播**: 低质量数据不能进入下游决策
5. **透明沟通**: 告诉用户数据的局限性

---

*记住：错误的确定性比诚实的不确定性危害更大。*