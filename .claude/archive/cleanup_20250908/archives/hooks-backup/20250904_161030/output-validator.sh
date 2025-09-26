#!/bin/bash

# PostToolUse Hook: Output Validator (Warning-Only Mode)
# 检测Subagent输出问题但不自动修复
# 发现问题时警告用户，让质量控制系统处理

# 设置项目根目录
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"
mkdir -p "$PROJECT_ROOT/.claude/validation"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 解析输入
tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# 将Windows路径转换为Unix路径
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 只处理Write操作的重要文件
if [[ "$tool_name" == "Write" ]] && [[ -f "$unix_path" ]]; then
    
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    validation_log="$PROJECT_ROOT/.claude/logs/output-validation.log"
    file_name=$(basename "$unix_path")
    
    # 收集发现的问题
    issues=()
    warnings=()
    
    # 检测常见问题（不修复）
    case "$file_name" in
        
        "content.md")
            # 章节内容文件验证
            
            # 1. 检查是否被截断（没有合理结尾）
            if [[ -s "$unix_path" ]]; then
                last_line=$(tail -1 "$unix_path" 2>/dev/null)
                word_count=$(wc -w < "$unix_path" 2>/dev/null || echo "0")
                
                # 检查章节是否看起来不完整
                if [[ "$word_count" -gt 100 ]] && [[ ! "$last_line" =~ (\*End.*Chapter.*\*|续|\.\.\.|\.|!|\?|\"|\') ]]; then
                    issues+=("TRUNCATED: Chapter may be incomplete (ends abruptly)")
                fi
                
                # 检查字数是否异常少
                if [[ "$word_count" -lt 50 ]]; then
                    warnings+=("SHORT: Chapter is very short ($word_count words)")
                fi
            fi
            
            # 2. 检查编码问题
            if grep -q '[âêîôû]' "$unix_path" 2>/dev/null; then
                issues+=("ENCODING: Possible UTF-8 encoding issues detected")
            fi
            
            # 3. 检查章节标题
            first_line=$(head -1 "$unix_path" 2>/dev/null)
            if [[ ! "$first_line" =~ ^#.*Chapter ]]; then
                warnings+=("FORMAT: Missing chapter header")
            fi
            
            # 4. 检查过多空行
            empty_line_count=$(grep -c '^$' "$unix_path" 2>/dev/null || echo "0")
            total_lines=$(wc -l < "$unix_path" 2>/dev/null || echo "1")
            if [[ "$empty_line_count" -gt 0 ]] && [[ $((empty_line_count * 3)) -gt "$total_lines" ]]; then
                warnings+=("FORMAT: Excessive blank lines detected")
            fi
            ;;
            
        "meta.json"|"quality_check.json"|"outline.json")
            # JSON文件验证
            
            # 1. 检查JSON语法
            if ! jq empty "$unix_path" 2>/dev/null; then
                issues+=("SYNTAX: Invalid JSON format")
                
                # 检查常见错误
                if grep -q ',\s*[}\]]' "$unix_path" 2>/dev/null; then
                    issues+=("SYNTAX: Trailing commas detected")
                fi
                
                if grep -q '"[^"]*$' "$unix_path" 2>/dev/null; then
                    issues+=("SYNTAX: Unclosed quotes detected")
                fi
            fi
            
            # 2. 检查必要字段（针对特定文件）
            if [[ "$file_name" == "meta.json" ]] && jq empty "$unix_path" 2>/dev/null; then
                if ! jq -e '.chapter_number' "$unix_path" >/dev/null 2>&1; then
                    warnings+=("MISSING: chapter_number field missing")
                fi
                if ! jq -e '.word_count' "$unix_path" >/dev/null 2>&1; then
                    warnings+=("MISSING: word_count field missing")
                fi
            fi
            
            if [[ "$file_name" == "quality_check.json" ]] && jq empty "$unix_path" 2>/dev/null; then
                if ! jq -e '.overall_score' "$unix_path" >/dev/null 2>&1; then
                    warnings+=("MISSING: overall_score field missing")
                fi
            fi
            ;;
            
        "bible.yaml"|"bible.yml")
            # Bible文件验证
            
            # 使用Python检查YAML语法
            if command -v python3 >/dev/null 2>&1; then
                yaml_check=$(python3 -c "
import yaml
import sys
try:
    with open('$unix_path', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        print('INVALID_STRUCTURE')
    elif not data.get('title'):
        print('MISSING_TITLE')
    elif not data.get('characters'):
        print('MISSING_CHARACTERS')
    else:
        print('VALID')
except yaml.YAMLError as e:
    print(f'YAML_ERROR: {e}')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null)
                
                case "$yaml_check" in
                    *YAML_ERROR*)
                        issues+=("SYNTAX: YAML parsing error - $yaml_check")
                        ;;
                    *INVALID_STRUCTURE*)
                        issues+=("STRUCTURE: Bible file is not a valid dictionary")
                        ;;
                    *MISSING_TITLE*)
                        warnings+=("MISSING: title field missing in Bible")
                        ;;
                    *MISSING_CHARACTERS*)
                        warnings+=("MISSING: characters section missing in Bible")
                        ;;
                esac
            fi
            ;;
            
        "entity_dictionary.yaml"|"entity_dictionary.yml")
            # 实体字典验证
            
            # 检查文件是否为空
            if [[ ! -s "$unix_path" ]]; then
                issues+=("EMPTY: Entity dictionary file is empty")
            fi
            ;;
    esac
    
    # 通用检查：文件截断检测
    if [[ -f "$unix_path" ]]; then
        # 获取文件最后几个字符
        last_chars=$(tail -c 20 "$unix_path" 2>/dev/null)
        
        # 检查是否以不完整的句子结尾（针对文本文件）
        if [[ "$file_name" =~ \.(md|yaml|yml|json)$ ]]; then
            if [[ "$last_chars" =~ [a-zA-Z0-9]$ ]] && [[ ! "$last_chars" =~ [\.!?\"\'}\])]$ ]]; then
                warnings+=("TRUNCATION: File may have been truncated")
            fi
        fi
    fi
    
    # 报告问题
    has_issues=false
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo "🚨 Critical issues detected in $(basename "$file_path"):"
        printf '   ❌ %s\n' "${issues[@]}"
        has_issues=true
        
        # 记录到日志
        echo "[$timestamp] CRITICAL issues in $unix_path:" >> "$validation_log"
        printf '  - %s\n' "${issues[@]}" >> "$validation_log"
    fi
    
    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo "⚠️  Potential issues in $(basename "$file_path"):"
        printf '   ⚠️  %s\n' "${warnings[@]}"
        has_issues=true
        
        # 记录到日志
        echo "[$timestamp] Warnings for $unix_path:" >> "$validation_log"
        printf '  - %s\n' "${warnings[@]}" >> "$validation_log"
    fi
    
    if [[ "$has_issues" == "true" ]]; then
        # 创建验证报告
        validation_report="$PROJECT_ROOT/.claude/validation/validation_$(date +%Y%m%d_%H%M%S).txt"
        cat > "$validation_report" << EOF
Output Validation Report
========================
Time: $timestamp
File: $unix_path
Tool: $tool_name

Critical Issues:
$(printf '%s\n' "${issues[@]}" | sed 's/^/  - /')

Warnings:
$(printf '%s\n' "${warnings[@]}" | sed 's/^/  - /')

Recommendation:
$(if [[ ${#issues[@]} -gt 0 ]]; then
    echo "  ❌ File has critical issues - recommend regeneration via quality system"
    echo "  💡 Try: /quality-check-individual or regenerate the content"
else
    echo "  ⚠️  File has minor issues but may be usable"
    echo "  💡 Review the file and regenerate if necessary"
fi)

Note: This hook only detects issues. Use the quality system to regenerate content.
EOF
        
        # 用户提示
        if [[ ${#issues[@]} -gt 0 ]]; then
            echo "💡 Recommendation: Run quality check or regenerate this file"
        else
            echo "💡 File is usable but may need minor review"
        fi
        
    else
        # 文件验证通过
        echo "✅ Output validation passed for $(basename "$file_path")"
        echo "[$timestamp] Validation passed: $unix_path" >> "$validation_log"
    fi
fi

# 成功退出
exit 0
[FILE MAY BE TRUNCATED - PLEASE VERIFY]
