#!/bin/bash

# PostToolUse Hook: Auto-update chapter metadata when content.md changes
# 自动更新章节元数据：字数、修改时间、场景统计等

# 设置项目根目录 (根据Claude Code官方文档)
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
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

# 使用jq解析JSON输入
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# 将Windows路径转换为Unix路径供bash使用
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 检查是否是章节内容写入操作 (支持Windows和Unix路径)
if [[ "$tool_name" == "Write" ]] && [[ "$file_path" == */content.md || "$file_path" == *\\content.md ]]; then
    
    # 验证这是章节目录中的content.md (支持Windows和Unix路径)
    if [[ "$file_path" == */chapters/ch*/content.md || "$file_path" == *\\chapters\\ch*\\content.md ]]; then
        
        chapter_dir=$(dirname "$unix_path")
        chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
        meta_file="$chapter_dir/meta.json"
        
        # 验证content.md文件存在
        if [[ -f "$unix_path" ]]; then
            
            # 计算字数 (使用wc -w)
            word_count=$(wc -w "$unix_path" 2>/dev/null | cut -d' ' -f1)
            [[ -z "$word_count" || "$word_count" == "0" ]] && word_count=$(wc -w < "$unix_path" 2>/dev/null || echo "0")
            
            # 计算字符数 (不含空格)
            char_count=$(tr -d ' \t\n\r' < "$unix_path" 2>/dev/null | wc -c || echo "0")
            
            # 分析场景数量 (基于章节分隔符或段落)
            scene_count=$(grep -c '^---$\|^##\|^\*\*\*$' "$unix_path" 2>/dev/null || echo "1")
            [[ "$scene_count" == "0" ]] && scene_count="1"
            
            # 检测对话行数 (以引号开头的行)
            dialogue_lines=$(grep -c '^[[:space:]]*".*"[[:space:]]*$\|^[[:space:]]*「.*」[[:space:]]*$' "$unix_path" 2>/dev/null || echo "0")
            
            # 获取当前时间戳
            current_time=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')
            
            # 检查meta.json是否存在
            if [[ -f "$meta_file" ]]; then
                
                # 使用jq更新现有meta.json
                jq --arg wc "$word_count" \
                   --arg cc "$char_count" \
                   --arg sc "$scene_count" \
                   --arg dl "$dialogue_lines" \
                   --arg time "$current_time" \
                   '. + {
                       "word_count": ($wc | tonumber),
                       "character_count": ($cc | tonumber), 
                       "estimated_scenes": ($sc | tonumber),
                       "dialogue_lines": ($dl | tonumber),
                       "last_modified": $time,
                       "auto_updated": true
                   }' "$meta_file" > "$meta_file.tmp" 2>/dev/null
                
                # 检查jq是否成功
                if [[ $? -eq 0 && -s "$meta_file.tmp" ]]; then
                    mv "$meta_file.tmp" "$meta_file"
                    
                    # 记录成功更新
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Updated meta for ch$chapter_num: ${word_count}w, ${scene_count}scenes" >> "$PROJECT_ROOT/.claude/logs/meta-updates.log"
                    
                    # 用户提示
                    echo "📊 Chapter $chapter_num metadata updated: $word_count words, $scene_count scenes"
                    
                else
                    # jq失败，清理临时文件
                    rm -f "$meta_file.tmp" 2>/dev/null
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to update meta for ch$chapter_num" >> "$PROJECT_ROOT/.claude/logs/meta-updates.log"
                fi
                
            else
                
                # 创建新的meta.json文件
                cat > "$meta_file" << EOF
{
  "chapter_number": $chapter_num,
  "word_count": $word_count,
  "character_count": $char_count,
  "estimated_scenes": $scene_count,
  "dialogue_lines": $dialogue_lines,
  "status": "in_progress",
  "created": "$current_time",
  "last_modified": "$current_time",
  "auto_updated": true,
  "auto_created": true
}
EOF
                
                # 记录创建新meta
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Created meta for ch$chapter_num: ${word_count}w" >> "$PROJECT_ROOT/.claude/logs/meta-updates.log"
                echo "📝 Created metadata for Chapter $chapter_num: $word_count words"
                
            fi
            
        fi
    fi
fi

# 成功退出
exit 0