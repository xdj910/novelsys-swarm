#!/bin/bash

# PostToolUse Hook: Auto-trigger context learning from high-quality chapters
# 使用jq进行精确JSON解析，符合Claude Code官方规范

# 设置项目根目录 (根据Claude Code官方文档)
# CLAUDE_PROJECT_DIR应该由Claude Code自动设置
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    # Fallback: 使用脚本所在位置推导项目根目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    echo "[WARNING] CLAUDE_PROJECT_DIR not set, using fallback: $PROJECT_ROOT" >&2
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保日志目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 使用jq进行JSON解析 (已安装jq-1.8.1)
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# Fallback到grep (如jq意外失败)
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# 调试日志 (简化版)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] tool='$tool_name', path='$(basename "$file_path")'" >> "$PROJECT_ROOT/.claude/logs/hook-debug.log"

# 检查是否是quality_check.json写入操作
if [[ "$tool_name" == "Write" && "$file_path" == *"quality_check.json" ]]; then
    
    # 验证文件存在并解析分数
    if [[ -f "$file_path" ]]; then
        # 使用jq解析质量分数 (jq-1.8.1)
        score=$(jq -r '.overall_score // empty' "$file_path" 2>/dev/null)
        [[ -z "$score" ]] && score=$(grep -o '"overall_score"[[:space:]]*:[[:space:]]*[0-9]*' "$file_path" | grep -o '[0-9]*$' 2>/dev/null)
        
        if [[ -n "$score" && "$score" =~ ^[0-9]+$ && "$score" -ge 95 ]]; then
            # 提取章节号
            chapter_dir=$(dirname "$file_path")
            chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
            
            # 记录高质量检测
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] High-quality chapter $chapter_num detected (Score: $score)" >> "$PROJECT_ROOT/.claude/logs/auto-learning.log"
            
            # 设置学习触发标记 (供Claude读取)
            {
                echo "TRIGGER_CONTEXT_SYNC=true"
                echo "CHAPTER_FOR_LEARNING=$chapter_num" 
                echo "QUALITY_SCORE=$score"
                echo "DETECTED_AT=$(date '+%Y-%m-%d %H:%M:%S')"
            } >> "$PROJECT_ROOT/.claude/logs/pending-actions.log"
            
            # 输出用户友好提示到stdout
            echo "🎯 High-quality chapter $chapter_num detected (Score: $score)"
            echo "📚 Ready for context learning - run /novel:context-sync when convenient"
            
        elif [[ -n "$score" && "$score" =~ ^[0-9]+$ ]]; then
            # 记录低质量分数
            chapter_dir=$(dirname "$file_path")
            chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Chapter $chapter_num below learning threshold (Score: $score < 95)" >> "$PROJECT_ROOT/.claude/logs/auto-learning.log"
        fi
    fi
fi

# 返回成功退出码 (符合官方规范)
exit 0