#!/bin/bash

# PostToolUse Hook: Optimized Writing Session Tracker
# 批量更新模式：减少频繁的I/O操作，提升性能

# 设置项目根目录
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"
mkdir -p "$PROJECT_ROOT/.claude/sessions"
mkdir -p "$PROJECT_ROOT/.claude/sessions/temp"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 解析输入
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# Convert Windows paths to Unix paths for compatibility
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 当前时间和日期
current_time=$(date '+%Y-%m-%d %H:%M:%S')
current_timestamp=$(date '+%s')
session_date=$(date '+%Y%m%d')

# 会话文件路径
session_file="$PROJECT_ROOT/.claude/sessions/session_$session_date.json"
temp_log="$PROJECT_ROOT/.claude/sessions/temp/operations_$session_date.log"
batch_trigger="$PROJECT_ROOT/.claude/sessions/temp/batch_trigger_$session_date.flag"

# 检查是否是写作相关操作
if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    # 初始化会话文件 (如果不存在)
    if [[ ! -f "$session_file" ]]; then
        cat > "$session_file" << EOF
{
  "session_date": "$session_date",
  "session_start": "$current_time",
  "last_activity": "$current_time",
  "total_operations": 0,
  "files_modified": [],
  "word_changes": {},
  "chapters_worked_on": [],
  "session_stats": {
    "total_words_added": 0,
    "total_words_removed": 0,
    "net_word_change": 0,
    "files_created": 0,
    "files_edited": 0,
    "chapters_touched": 0
  }
}
EOF
        echo "📝 Started new writing session for $(date '+%Y-%m-%d')"
    fi
    
    # 检测文件类型和操作类型
    file_type="other"
    operation_details=""
    word_change=0
    chapter_num=""
    
    if ([[ "$file_path" == */content.md ]] || [[ "$file_path" == *\\content.md ]]); then
        file_type="chapter_content"
        
        # 提取章节号
        if ([[ "$file_path" == */chapters/ch*/content.md ]] || [[ "$file_path" == *\\chapters\\ch*\\content.md ]]); then
            chapter_dir=$(dirname "$unix_path")
            chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
            operation_details="Chapter $chapter_num content"
            
            # 计算字数变化（简化版本）
            if [[ -f "$unix_path" ]]; then
                current_words=$(wc -w "$unix_path" 2>/dev/null | cut -d' ' -f1 || echo "0")
                if [[ "$tool_name" == "Write" ]]; then
                    word_change="$current_words"
                fi
            fi
        fi
    elif ([[ "$file_path" == */meta.json ]] || [[ "$file_path" == *\\meta.json ]]); then
        file_type="metadata"
        operation_details="Chapter metadata"
    elif ([[ "$file_path" == *bible.yaml ]] || [[ "$file_path" == *\\bible.yaml ]]) || ([[ "$file_path" == *bible.yml ]] || [[ "$file_path" == *\\bible.yml ]]); then
        file_type="bible"
        operation_details="Series Bible"
    elif ([[ "$file_path" == */quality_check.json ]] || [[ "$file_path" == *\\quality_check.json ]]); then
        file_type="quality_report"
        operation_details="Quality assessment"
    elif [[ "$file_path" == *.md ]]; then
        file_type="documentation"
        operation_details="Documentation"
    else
        operation_details="Other file: $(basename "$file_path")"
    fi
    
    # 轻量级记录：写入临时日志而不是立即更新JSON
    cat >> "$temp_log" << EOF
${current_timestamp}|${current_time}|${tool_name}|${file_path}|${file_type}|${operation_details}|${word_change}|${chapter_num}
EOF
    
    # 简单的用户反馈
    if [[ "$word_change" -gt 0 ]]; then
        echo "📊 Session: +$word_change words ($operation_details)"
    else
        echo "📊 Session: $operation_details updated"
    fi
    
    # 检查是否需要批量更新
    # 条件：每10个操作 OR 距离上次更新超过5分钟 OR 特殊文件类型
    should_batch_update=false
    
    # 计算当前操作数
    if [[ -f "$temp_log" ]]; then
        operation_count=$(wc -l < "$temp_log" 2>/dev/null || echo "0")
        
        # 每10个操作触发批量更新
        if [[ "$operation_count" -ge 10 ]]; then
            should_batch_update=true
        fi
    fi
    
    # 检查时间间隔（如果存在批量触发标记文件）
    if [[ -f "$batch_trigger" ]]; then
        last_update=$(stat -c %Y "$batch_trigger" 2>/dev/null || echo "0")
        time_diff=$((current_timestamp - last_update))
        
        # 5分钟 = 300秒
        if [[ "$time_diff" -gt 300 ]]; then
            should_batch_update=true
        fi
    fi
    
    # 重要文件立即更新
    if [[ "$file_type" == "bible" || "$file_type" == "quality_report" ]]; then
        should_batch_update=true
    fi
    
    # 执行批量更新
    if [[ "$should_batch_update" == "true" ]]; then
        
        if [[ -f "$temp_log" ]]; then
            # 读取临时日志并批量更新会话文件
            total_new_operations=0
            new_files=()
            new_chapters=()
            total_word_change=0
            
            while IFS='|' read -r timestamp_val time_val tool_val file_val type_val details_val words_val chapter_val; do
                total_new_operations=$((total_new_operations + 1))
                
                # 收集唯一文件
                if [[ ! " ${new_files[@]} " =~ " ${file_val} " ]]; then
                    new_files+=("$file_val")
                fi
                
                # 收集章节号
                if [[ -n "$chapter_val" ]] && [[ ! " ${new_chapters[@]} " =~ " ${chapter_val} " ]]; then
                    new_chapters+=("$chapter_val")
                fi
                
                # 累积字数变化
                if [[ "$words_val" =~ ^-?[0-9]+$ ]]; then
                    total_word_change=$((total_word_change + words_val))
                fi
                
            done < "$temp_log"
            
            # 使用jq批量更新会话文件
            temp_session="$session_file.tmp"
            
            jq --arg last_activity "$current_time" \
               --arg new_ops "$total_new_operations" \
               --arg word_change "$total_word_change" \
               --argjson new_files "$(printf '%s\n' "${new_files[@]}" | jq -R . | jq -s .)" \
               --argjson new_chapters "$(printf '%s\n' "${new_chapters[@]}" | jq -R . | jq -s .)" \
               '. + {
                   "last_activity": $last_activity,
                   "total_operations": (.total_operations + ($new_ops | tonumber))
               } |
               .files_modified = (.files_modified + $new_files) | .files_modified |= unique |
               .chapters_worked_on = (.chapters_worked_on + $new_chapters) | .chapters_worked_on |= unique |
               .session_stats.net_word_change += ($word_change | tonumber) |
               .session_stats.files_created += ([$new_files[] | select(test("Write"))] | length) |
               .session_stats.files_edited = (.files_modified | length) |
               .session_stats.chapters_touched = (.chapters_worked_on | length)' \
               "$session_file" > "$temp_session" 2>/dev/null
            
            # 检查更新是否成功
            if [[ $? -eq 0 && -s "$temp_session" ]]; then
                mv "$temp_session" "$session_file"
                
                # 清空临时日志
                > "$temp_log"
                
                # 更新批量触发标记
                touch "$batch_trigger"
                
                # 记录批量更新
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Batch updated session: $total_new_operations operations, $total_word_change words" >> "$PROJECT_ROOT/.claude/logs/session-tracking.log"
                
                echo "📊 Batch update: $total_new_operations operations processed"
                
                # 生成会话摘要（每批量更新后）
                net_words=$(jq -r '.session_stats.net_word_change // 0' "$session_file" 2>/dev/null)
                total_ops=$(jq -r '.total_operations // 0' "$session_file" 2>/dev/null)
                chapters_count=$(jq -r '.session_stats.chapters_touched // 0' "$session_file" 2>/dev/null)
                
                daily_summary="$PROJECT_ROOT/.claude/sessions/daily_${session_date}.md"
                
                cat > "$daily_summary" << EOF
# Writing Session Summary - $(date '+%Y-%m-%d')

## Session Overview
- **Last Activity**: $current_time  
- **Total Operations**: $total_ops
- **Net Word Change**: $net_words words
- **Chapters Worked On**: $chapters_count

## Session Statistics
$(jq -r '
"- Files Edited: " + (.session_stats.files_edited | tostring) + "  
- Words Changed: " + (.session_stats.net_word_change | tostring) + "
- Chapters Touched: " + (.session_stats.chapters_touched | tostring)
' "$session_file" 2>/dev/null)

---
*Auto-generated by optimized session-tracker Hook*
EOF
                
            else
                # 批量更新失败，使用简单日志记录
                rm -f "$temp_session" 2>/dev/null
                echo "[$current_time] Batch update failed, logged $total_new_operations operations" >> "$PROJECT_ROOT/.claude/logs/session-simple.log"
            fi
        fi
    fi
fi

# 成功退出
exit 0