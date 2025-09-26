#!/bin/bash

# PreToolUse Hook: Dynamic Subagent Context Enhancer
# 在调用Subagent前动态注入项目特定上下文
# 确保每个Subagent获得最相关的工作环境信息

# 设置项目根目录
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保日志目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 解析输入
tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
subagent_type=$(echo "$input" | jq -r '.tool_input.subagent_type // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$subagent_type" ]] && subagent_type=$(echo "$input" | grep -o '"subagent_type"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# 检查是否是Task工具(调用Subagent)
if [[ "$tool_name" == "Task" ]] && [[ -n "$subagent_type" ]]; then
    
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
    
    # 为每本书创建独立的context目录
    project_context_dir="$PROJECT_ROOT/.claude/data/projects/$active_project/context"
    mkdir -p "$project_context_dir"
    
    context_file="$project_context_dir/current_context.md"
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[INFO] Preparing context for subagent: $subagent_type in project: $active_project" >&2
    
    # 生成动态上下文文档
    cat > "$context_file" << EOF
# Dynamic Context for $subagent_type
Generated: $timestamp

## 🎯 Current Project State

### Active Project: $active_project
Project Path: $PROJECT_ROOT/.claude/data/projects/$active_project

### Recent Changes (Last 5 commits)
$(cd "$PROJECT_ROOT" && git log --oneline -5 2>/dev/null || echo "Git not initialized")

### Current Branch
$(cd "$PROJECT_ROOT" && git branch --show-current 2>/dev/null || echo "main")

### Modified Files
$(cd "$PROJECT_ROOT" && git status --porcelain 2>/dev/null | head -10 || echo "No changes")

## 📊 Project Statistics

### Chapter Progress
$(find "$PROJECT_ROOT/.claude/data/projects/$active_project/chapters" -name "content.md" 2>/dev/null | wc -l || echo "0") chapters created

### Quality Metrics
$(jq -r '.project_stats | "Words: \(.total_words // 0) | Chapters: \(.completed_chapters // 0)/\(.total_chapters // 0) | Avg Quality: \(.average_quality_score // 0)"' "$PROJECT_ROOT/.claude/stats/project_stats.json" 2>/dev/null || echo "No statistics available")

### Recent Errors/Warnings
$(tail -10 "$PROJECT_ROOT/.claude/logs/error.log" 2>/dev/null || echo "No errors logged")

## 🔧 Subagent-Specific Context

EOF

    # 根据不同的Subagent类型添加特定上下文
    case "$subagent_type" in
        
        "scene-generator"|"director")
            # 创作类agent需要最新的故事上下文
            echo "### Recent Story Content" >> "$context_file"
            echo '```' >> "$context_file"
            find "$PROJECT_ROOT/.claude/data/projects/$active_project/chapters" -name "content.md" -type f -exec ls -t {} \; 2>/dev/null | head -1 | xargs tail -50 2>/dev/null >> "$context_file"
            echo '```' >> "$context_file"
            
            echo "### Available Characters" >> "$context_file"
            if [[ -f "$PROJECT_ROOT/.claude/data/projects/$active_project/shared/entity_dictionary.yaml" ]]; then
                grep -E "^\s+- name:" "$PROJECT_ROOT/.claude/data/projects/$active_project/shared/entity_dictionary.yaml" 2>/dev/null | head -10 >> "$context_file"
            fi
            ;;
            
        "quality-scorer"|"bible-compliance-validator")
            # 质量检查类agent需要标准和规则
            echo "### Quality Standards" >> "$context_file"
            echo "- Minimum quality score: 95" >> "$context_file"
            echo "- Required elements: Plot consistency, Character development, Dialogue quality" >> "$context_file"
            
            echo "### Recent Quality Scores" >> "$context_file"
            find "$PROJECT_ROOT/.claude/data/projects/$active_project/chapters" -name "quality_check.json" -exec jq -r '"\(.chapter // "?"): \(.overall_score // 0)"' {} \; 2>/dev/null | tail -5 >> "$context_file"
            ;;
            
        "continuity-guard-specialist"|"plot-hole-detector")
            # 连贯性检查类agent需要历史信息
            echo "### Plot Threads Tracking" >> "$context_file"
            echo "Active plot threads that need resolution:" >> "$context_file"
            
            # 列出所有章节的主要事件
            echo "### Chapter Events Summary" >> "$context_file"
            find "$PROJECT_ROOT/.claude/data/projects/$active_project/chapters" -name "meta.json" -exec jq -r '"\nChapter \(.chapter_number // "?"): \(.word_count // 0) words, \(.estimated_scenes // 0) scenes"' {} \; 2>/dev/null | head -10 >> "$context_file"
            ;;
            
        "entity-dictionary-manager"|"character-*")
            # 角色管理类agent需要实体信息
            echo "### Entity Dictionary Status" >> "$context_file"
            entity_dict="$PROJECT_ROOT/.claude/data/projects/$active_project/shared/entity_dictionary.yaml"
            if [[ -f "$entity_dict" ]]; then
                echo "Location: $entity_dict" >> "$context_file"
                echo "Size: $(wc -l < "$entity_dict") lines" >> "$context_file"
                echo "Last modified: $(stat -c %y "$entity_dict" 2>/dev/null || stat -f %Sm "$entity_dict" 2>/dev/null)" >> "$context_file"
            else
                echo "Entity dictionary not found - will need to create one" >> "$context_file"
            fi
            ;;
            
        *)
            # 默认上下文
            echo "### Working Directory" >> "$context_file"
            echo "$PROJECT_ROOT" >> "$context_file"
            
            echo "### Available Tools" >> "$context_file"
            echo "- Read, Write, Edit, MultiEdit for file operations" >> "$context_file"
            echo "- Bash for command execution" >> "$context_file"
            echo "- Task for creating sub-agents" >> "$context_file"
            ;;
    esac
    
    # 添加共享记忆部分
    echo "" >> "$context_file"
    echo "## 💾 Shared Memory" >> "$context_file"
    echo "" >> "$context_file"
    
    # 检查是否有该agent的历史记录
    agent_memory="$project_context_dir/memory_${subagent_type}.json"
    if [[ -f "$agent_memory" ]]; then
        echo "### Previous Session Notes" >> "$context_file"
        jq -r '.notes[]' "$agent_memory" 2>/dev/null | tail -5 >> "$context_file"
    fi
    
    # 添加系统提示
    echo "" >> "$context_file"
    echo "## ⚠️ Important Reminders" >> "$context_file"
    echo "" >> "$context_file"
    echo "1. Always read required files before processing" >> "$context_file"
    echo "2. Maintain consistency with existing content" >> "$context_file"
    echo "3. Follow the project's established patterns" >> "$context_file"
    echo "4. Save your work frequently" >> "$context_file"
    echo "5. Report any issues or conflicts found" >> "$context_file"
    
    # 记录上下文生成
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generated context for $subagent_type ($(wc -l < "$context_file") lines)" >> "$PROJECT_ROOT/.claude/logs/context-generation.log"
    
    # 可选：显示简短提示给用户
    echo "📋 Enhanced context prepared for $subagent_type agent"
fi

# 成功退出
exit 0