# Context Firewall Template

## Agent输出规范

### 所有Agent必须遵循的输出格式

```yaml
output_format:
  summary: 
    max_length: 50
    content: "[核心结论，50字以内]"
    
  detail_file:
    path: ".claude/context/details/{agent_name}_{timestamp}.md"
    content: "[完整分析内容，无字数限制]"
    
  index_entry:
    id: "{task_id}"
    agent: "{agent_name}"
    summary: "{50字摘要}"
    detail_path: "{详细文件路径}"
    timestamp: "{ISO8601时间}"
    tags: [相关标签列表]
```

### 示例输出

```markdown
## 摘要（返回给主线程）
Ch3评分92/100:心理描写优秀,对话需改进,时间线有冲突

## 详细内容（保存到文件）
[保存到: .claude/context/details/quality_scorer_ch03_20250831.md]
完整的10,000字分析报告...
```

### Context Firewall执行流程

1. **Agent执行任务**  ->  生成完整分析
2. **Firewall压缩**  ->  提取50字核心摘要
3. **详细存储**  ->  完整内容保存到文件
4. **索引更新**  ->  记录到index.json
5. **返回摘要**  ->  主线程只接收50字

### Token节省计算

```yaml
传统方式:
  单Agent输出: ~10,000 tokens
  11章节x4 agents: 440,000 tokens
  
Firewall方式:
  单Agent摘要: ~50 tokens
  11章节x4 agents: 2,200 tokens
  节省: 99.5% (仅摘要部分)
  
实际节省（含必要上下文）:
  约70%总体Token节省
```