#!/bin/bash

# PostToolUse Hook: Content formatter for markdown standardization
# 自动格式化章节内容：标题、对话、段落间距、标点符号
# 环境变量 HOOKS_WARNING_ONLY=true 时只输出警告而不修改文件

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

# 检查是否启用警告模式
WARNING_ONLY=${HOOKS_WARNING_ONLY:-false}

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 使用jq解析JSON输入
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# Convert Windows paths to Unix paths for compatibility
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 检查是否是需要格式化的markdown文件
if [[ "$tool_name" == "Write" && "$file_path" == *.md ]]; then
    
    # 主要针对章节内容文件
    if ([[ "$file_path" == */content.md ]] || [[ "$file_path" == *\\content.md ]]) || ([[ "$file_path" == */chapter*.md ]] || [[ "$file_path" == *\\chapter*.md ]]); then
        
        if [[ -f "$unix_path" ]]; then
            
            # 创建临时文件进行格式化
            temp_file="$unix_path.fmt.tmp"
            cp "$unix_path" "$temp_file"
            
            formatting_changes=()
            
            # 1. 标准化章节标题格式
            if sed -i 's/^#[[:space:]]*Chapter[[:space:]]*\([0-9]*\)[[:space:]]*$/# Chapter \1/I' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Standardized chapter title format")
            fi
            
            # 2. 标准化场景分隔符
            if sed -i 's/^[[:space:]]*---[[:space:]]*$/\n---\n/g' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Standardized scene separators")
            fi
            
            # 3. 修复中英文混合标点符号
            # 将英文引号改为中文引号 (在中文语境中)
            if sed -i 's/"\\([^"]*[\\u4e00-\\u9fff][^"]*\\)"/「\1」/g' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Fixed Chinese quotation marks")
            fi
            
            # 4. 标准化对话格式 - 确保对话前后有适当空行
            # 检测对话行 (以引号开头)
            if sed -i '/^[[:space:]]*[「"]/i\\' "$temp_file" 2>/dev/null && sed -i '/^[[:space:]]*[」"]/a\\' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Improved dialogue formatting")
            fi
            
            # 5. 修复段落间距 - 确保段落间有空行
            if sed -i '/^[[:space:]]*$/N;/^[[:space:]]*\\n[[:space:]]*$/d' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Normalized paragraph spacing")
            fi
            
            # 6. 移除行尾空白
            if sed -i 's/[[:space:]]*$//' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Removed trailing whitespace")
            fi
            
            # 7. 标准化中文标点符号
            # 中文句号
            if sed -i 's/\\([\\u4e00-\\u9fff]\\)\\./\1。/g' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Fixed Chinese punctuation")
            fi
            
            # 中文逗号
            if sed -i 's/\\([\\u4e00-\\u9fff]\\),/\1，/g' "$temp_file" 2>/dev/null; then
                formatting_changes+=("Fixed Chinese commas")
            fi
            
            # 8. 确保章节结尾格式统一
            if sed -i '$a\\n*End of Chapter*' "$temp_file" 2>/dev/null; then
                # 移除多余的结尾标记
                sed -i '/^*End of Chapter*$/N;/^*End of Chapter*\\n*End of Chapter*$/s/^*End of Chapter*\\n//' "$temp_file" 2>/dev/null
                formatting_changes+=("Standardized chapter ending")
            fi
            
            # 9. 修复Markdown标题层级
            # 确保只有一个H1标题（章节标题）
            h1_count=$(grep -c '^# ' "$temp_file" 2>/dev/null || echo "0")
            if [[ "$h1_count" -gt 1 ]]; then
                # 将第二个及以后的H1改为H2
                sed -i '2,$s/^# /## /' "$temp_file" 2>/dev/null
                formatting_changes+=("Fixed heading hierarchy")
            fi
            
            # 10. Windows换行符标准化 (如果需要)
            if command -v dos2unix >/dev/null 2>&1; then
                dos2unix "$temp_file" 2>/dev/null && formatting_changes+=("Normalized line endings")
            fi
            
            # 比较文件是否有实际变化
            if ! cmp -s "$unix_path" "$temp_file"; then
                
                if [[ "$WARNING_ONLY" == "true" ]]; then
                    # 警告模式：只输出警告，不修改文件
                    rm -f "$temp_file"
                    echo "⚠️  [WARNING] Content formatting issues detected in $(basename "$unix_path") - File not modified (HOOKS_WARNING_ONLY=true)"
                    for change in "${formatting_changes[@]}"; do
                        echo "   - Would fix: $change"
                    done
                    echo "   To apply these fixes, run with HOOKS_WARNING_ONLY=false"
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Formatting needed but skipped for: $(basename "$unix_path")" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
                    return 0
                fi
                
                # 有变化，应用格式化
                mv "$temp_file" "$unix_path"
                
                # 记录格式化操作
                chapter_num="unknown"
                if [[ "$unix_path" == */chapters/ch*/content.md ]]; then
                    chapter_dir=$(dirname "$unix_path")
                    chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
                fi
                
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Formatted chapter $chapter_num content:" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
                for change in "${formatting_changes[@]}"; do
                    echo "  - $change" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
                done
                
                # 用户提示
                if [[ ${#formatting_changes[@]} -gt 0 ]]; then
                    if [[ "$chapter_num" != "unknown" ]]; then
                        echo "📝 Chapter $chapter_num formatted: ${#formatting_changes[@]} improvements"
                    else
                        echo "📝 Content formatted: ${#formatting_changes[@]} improvements"
                    fi
                    
                    # 显示主要改进 (限制输出长度)
                    if [[ ${#formatting_changes[@]} -le 3 ]]; then
                        for change in "${formatting_changes[@]}"; do
                            echo "  ✓ $change"
                        done
                    else
                        echo "  ✓ ${formatting_changes[0]}"
                        echo "  ✓ ${formatting_changes[1]}"
                        echo "  ✓ ... and $((${#formatting_changes[@]} - 2)) more"
                    fi
                fi
                
            else
                # 没有变化，清理临时文件
                rm -f "$temp_file"
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] No formatting needed for: $(basename "$unix_path")" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
            fi
            
        fi
        
    # 处理其他markdown文件 (如README, 文档等)
    else
        
        if [[ -f "$unix_path" ]]; then
            # 轻量格式化：只处理基本问题
            temp_file="$unix_path.fmt.tmp"
            cp "$unix_path" "$temp_file"
            
            # 移除行尾空白
            sed -i 's/[[:space:]]*$//' "$temp_file" 2>/dev/null
            
            # 标准化标题格式 (确保#后有空格)
            sed -i 's/^#\\([^[:space:]]\\)/# \\1/' "$temp_file" 2>/dev/null
            
            if ! cmp -s "$unix_path" "$temp_file"; then
                if [[ "$WARNING_ONLY" == "true" ]]; then
                    # 警告模式：只输出警告，不修改文件
                    rm -f "$temp_file"
                    echo "⚠️  [WARNING] Light formatting issues detected in $(basename "$unix_path") - File not modified (HOOKS_WARNING_ONLY=true)"
                    echo "   To apply formatting fixes, run with HOOKS_WARNING_ONLY=false"
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Light formatting needed but skipped for: $(basename "$unix_path")" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
                    return 0
                fi
                
                mv "$temp_file" "$unix_path"
                echo "📝 Markdown file formatted: $(basename "$unix_path")"
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Light formatting applied to: $(basename "$unix_path")" >> "$PROJECT_ROOT/.claude/logs/formatting.log"
            else
                rm -f "$temp_file"
            fi
        fi
    fi
fi

# 成功退出
exit 0