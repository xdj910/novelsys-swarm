#!/bin/bash

# SubagentStop Hook: Capture and learn from Subagent outputs
# 在Subagent完成后捕获其输出并更新共享记忆
# 实现跨会话的知识积累和模式学习

# 设置项目根目录
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"

# 获取当前活动的项目（书籍）
active_project=""
for proj_dir in "$PROJECT_ROOT/.claude/data/projects"/*/; do
    if [[ -d "$proj_dir" ]]; then
        active_project=$(basename "$proj_dir")
        break
    fi
done

if [[ -z "$active_project" ]]; then
    echo "[WARNING] No active project found" >&2
    exit 0
fi

# 为每本书创建独立的learning和context目录
project_dir="$PROJECT_ROOT/.claude/data/projects/$active_project"
project_context_dir="$project_dir/context"
project_learning_dir="$project_dir/learning"
mkdir -p "$project_context_dir"
mkdir -p "$project_learning_dir"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 解析输入
subagent_type=$(echo "$input" | jq -r '.subagent_type // empty' 2>/dev/null)
task_description=$(echo "$input" | jq -r '.description // empty' 2>/dev/null)
result=$(echo "$input" | jq -r '.result // empty' 2>/dev/null)

# Fallback解析
[[ -z "$subagent_type" ]] && subagent_type=$(echo "$input" | grep -o '"subagent_type"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

timestamp=$(date '+%Y-%m-%d %H:%M:%S')
today=$(date '+%Y%m%d')

# 记录Subagent活动
echo "[$timestamp] Subagent completed: $subagent_type" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
echo "  Task: $task_description" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"

# 更新该agent的记忆文件（项目特定）
agent_memory="$project_context_dir/memory_${subagent_type}.json"

# 检查生成的文件
generated_files=$(cd "$PROJECT_ROOT" && git status --porcelain 2>/dev/null | grep "^A\|^??" | cut -c4-)

if [[ -n "$generated_files" ]]; then
    echo "  Generated files:" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
    echo "$generated_files" | sed 's/^/    /' >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
fi

# 分析Subagent的输出模式
case "$subagent_type" in
    
    "scene-generator"|"director")
        # 创作类agent - 保存生成模式
        pattern_file="$project_learning_dir/writing_patterns.json"
        
        # 统计新生成内容的特征
        if [[ -n "$generated_files" ]]; then
            for file in $generated_files; do
                if [[ "$file" == *"content.md" ]]; then
                    # 分析写作风格
                    word_count=$(wc -w "$PROJECT_ROOT/$file" 2>/dev/null | cut -d' ' -f1)
                    dialogue_lines=$(grep -c '^[[:space:]]*".*"' "$PROJECT_ROOT/$file" 2>/dev/null)
                    scene_breaks=$(grep -c '^---$\|^##' "$PROJECT_ROOT/$file" 2>/dev/null)
                    
                    # 保存模式
                    if [[ ! -f "$pattern_file" ]]; then
                        echo '{"patterns":[]}' > "$pattern_file"
                    fi
                    
                    jq --arg time "$timestamp" \
                       --arg wc "$word_count" \
                       --arg dl "$dialogue_lines" \
                       --arg sb "$scene_breaks" \
                       '.patterns += [{
                           "timestamp": $time,
                           "word_count": ($wc | tonumber),
                           "dialogue_lines": ($dl | tonumber),
                           "scene_breaks": ($sb | tonumber)
                       }] | .patterns = (.patterns | .[-10:])' "$pattern_file" > "$pattern_file.tmp"
                    
                    mv "$pattern_file.tmp" "$pattern_file"
                    
                    echo "  Writing pattern: ${word_count}w, ${dialogue_lines} dialogues, ${scene_breaks} scenes" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
                fi
            done
        fi
        ;;
        
    "quality-scorer")
        # 质量评分agent - 学习评分模式
        quality_history="$project_learning_dir/quality_history.json"
        
        # 查找新的质量检查文件
        quality_files=$(echo "$generated_files" | grep "quality_check.json")
        
        for qfile in $quality_files; do
            if [[ -f "$PROJECT_ROOT/$qfile" ]]; then
                score=$(jq -r '.overall_score // 0' "$PROJECT_ROOT/$qfile" 2>/dev/null)
                
                if [[ ! -f "$quality_history" ]]; then
                    echo '{"scores":[]}' > "$quality_history"
                fi
                
                jq --arg time "$timestamp" \
                   --arg score "$score" \
                   --arg file "$qfile" \
                   '.scores += [{
                       "timestamp": $time,
                       "score": ($score | tonumber),
                       "file": $file
                   }] | .scores = (.scores | .[-20:])' "$quality_history" > "$quality_history.tmp"
                
                mv "$quality_history.tmp" "$quality_history"
                
                # 计算平均分和趋势
                avg_score=$(jq '[.scores[].score] | add/length' "$quality_history" 2>/dev/null)
                echo "  Quality score: $score (avg: $avg_score)" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
            fi
        done
        ;;
        
    "entity-dictionary-manager"|"character-*")
        # 实体管理类agent - 跟踪实体变化
        entity_log="$project_learning_dir/entity_changes.log"
        
        entity_files=$(echo "$generated_files" | grep -E "entity|character|bible")
        if [[ -n "$entity_files" ]]; then
            echo "[$timestamp] Entity updates by $subagent_type:" >> "$entity_log"
            echo "$entity_files" | sed 's/^/  /' >> "$entity_log"
            
            # 统计实体数量
            entity_dict="$project_dir/shared/entity_dictionary.yaml"
            if [[ -f "$entity_dict" ]]; then
                character_count=$(grep -c "^  - name:" "$entity_dict" 2>/dev/null || echo "0")
                location_count=$(grep -c "^  - location:" "$entity_dict" 2>/dev/null || echo "0")
                echo "  Entity count: $character_count characters, $location_count locations" >> "$entity_log"
            fi
        fi
        ;;
        
    *)
        # 默认处理 - 通用日志
        echo "  Generic task completed" >> "$PROJECT_ROOT/.claude/logs/subagent-activity.log"
        ;;
esac

# 更新agent的记忆
if [[ ! -f "$agent_memory" ]]; then
    echo '{"last_run":"","notes":[],"statistics":{}}' > "$agent_memory"
fi

# 添加新的记忆条目
note="Task: $task_description (completed: $timestamp)"
if [[ -n "$generated_files" ]]; then
    files_count=$(echo "$generated_files" | wc -l)
    note="$note - Generated $files_count files"
fi

jq --arg time "$timestamp" \
   --arg note "$note" \
   '.last_run = $time | 
    .notes += [$note] | 
    .notes = (.notes | .[-10:]) |
    .statistics.total_runs = ((.statistics.total_runs // 0) + 1) |
    .statistics.last_files_generated = ($ARGS.named.files // "")' \
   --arg files "$generated_files" \
   "$agent_memory" > "$agent_memory.tmp"

mv "$agent_memory.tmp" "$agent_memory"

# 生成日报汇总
# 项目特定的日报
daily_report="$project_dir/logs/daily_agent_report_$today.md"
mkdir -p "$project_dir/logs"
if [[ ! -f "$daily_report" ]]; then
    cat > "$daily_report" << EOF
# Daily Subagent Activity Report
Date: $(date '+%Y-%m-%d')

## Subagent Sessions
EOF
fi

cat >> "$daily_report" << EOF

### $timestamp - $subagent_type
- **Task**: $task_description
- **Files Generated**: $(echo "$generated_files" | wc -l)
- **Status**: Completed
EOF

if [[ -n "$generated_files" ]]; then
    echo "- **Output Files**:" >> "$daily_report"
    echo "$generated_files" | sed 's/^/  - /' >> "$daily_report"
fi

# 计算今日统计
total_sessions=$(grep -c "^###" "$daily_report" 2>/dev/null || echo "0")
echo "" >> "$daily_report"
echo "---" >> "$daily_report"
echo "**Total Sessions Today**: $total_sessions" >> "$daily_report"

# 用户友好提示
echo "📊 Subagent $subagent_type completed. Session logged and patterns learned."

# 可选：如果检测到质量问题，发出警告
if [[ "$subagent_type" == "quality-scorer" ]]; then
    latest_score=$(jq -r '.scores[-1].score // 0' "$project_learning_dir/quality_history.json" 2>/dev/null)
    if [[ "$latest_score" -lt 95 ]]; then
        echo "⚠️ Warning: Quality score $latest_score is below threshold (95)"
    fi
fi

# 成功退出
exit 0