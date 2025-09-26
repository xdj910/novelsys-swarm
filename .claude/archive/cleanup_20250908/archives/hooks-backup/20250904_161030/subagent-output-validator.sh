#!/bin/bash

# PostToolUse Hook: Subagent Output Validator and Fixer  
# 验证和修复Subagent生成的文件，确保输出质量
# 特别关注过程文件的完整性和格式正确性
# 环境变量 HOOKS_WARNING_ONLY=true 时只输出警告而不自动修复文件

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

# 检查是否启用警告模式
WARNING_ONLY=${HOOKS_WARNING_ONLY:-false}

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 解析输入
tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // empty' 2>/dev/null)
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# 将Windows路径转换为Unix路径
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 检查是否是写入操作
if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    validation_log="$PROJECT_ROOT/.claude/logs/validation.log"
    
    # 获取文件扩展名和类型
    file_ext="${unix_path##*.}"
    file_name=$(basename "$unix_path")
    file_dir=$(dirname "$unix_path")
    
    # 标记是否需要验证
    needs_validation=false
    validation_type=""
    
    # 判断文件类型并设置验证规则
    case "$file_name" in
        
        "bible.yaml"|"bible.yml")
            needs_validation=true
            validation_type="bible"
            echo "[$timestamp] Validating Bible file: $unix_path" >> "$validation_log"
            ;;
            
        "entity_dictionary.yaml"|"entity_dictionary.yml")
            needs_validation=true
            validation_type="entity"
            echo "[$timestamp] Validating Entity Dictionary: $unix_path" >> "$validation_log"
            ;;
            
        "meta.json")
            needs_validation=true
            validation_type="meta"
            echo "[$timestamp] Validating Chapter Meta: $unix_path" >> "$validation_log"
            ;;
            
        "outline.json")
            needs_validation=true
            validation_type="outline"
            echo "[$timestamp] Validating Chapter Outline: $unix_path" >> "$validation_log"
            ;;
            
        "quality_check.json")
            needs_validation=true
            validation_type="quality"
            echo "[$timestamp] Validating Quality Check: $unix_path" >> "$validation_log"
            ;;
            
        "content.md")
            needs_validation=true
            validation_type="content"
            echo "[$timestamp] Validating Chapter Content: $unix_path" >> "$validation_log"
            ;;
            
        "*.json")
            needs_validation=true
            validation_type="json"
            echo "[$timestamp] Validating JSON file: $unix_path" >> "$validation_log"
            ;;
            
        "*.yaml"|"*.yml")
            needs_validation=true
            validation_type="yaml"
            echo "[$timestamp] Validating YAML file: $unix_path" >> "$validation_log"
            ;;
    esac
    
    # 执行验证
    if [[ "$needs_validation" == "true" ]] && [[ -f "$unix_path" ]]; then
        
        validation_passed=true
        error_messages=""
        
        case "$validation_type" in
            
            "json")
                # 验证JSON格式
                if ! jq empty "$unix_path" 2>/dev/null; then
                    validation_passed=false
                    error_messages="Invalid JSON syntax"
                    
                    if [[ "$WARNING_ONLY" == "true" ]]; then
                        # 警告模式：只输出警告，不修复文件
                        echo "⚠️  [WARNING] JSON syntax errors detected in $(basename "$unix_path") - File not repaired (HOOKS_WARNING_ONLY=true)"
                        echo "   Common issues: trailing commas, invalid syntax"
                        echo "   To auto-repair this file, run with HOOKS_WARNING_ONLY=false"
                        echo "[$timestamp] WARNING: JSON errors in $unix_path - repair skipped" >> "$validation_log"
                    else
                        # 尝试修复常见JSON错误
                        echo "[$timestamp] Attempting to fix JSON: $unix_path" >> "$validation_log"
                        
                        # 备份原文件
                        cp "$unix_path" "$unix_path.backup"
                        
                        # 修复常见问题：尾随逗号
                        sed -i 's/,\s*}/}/g' "$unix_path"
                        sed -i 's/,\s*]/]/g' "$unix_path"
                    fi
                    
                    # 再次验证（仅在非警告模式下）
                    if [[ "$WARNING_ONLY" != "true" ]]; then
                        if jq empty "$unix_path" 2>/dev/null; then
                            echo "[$timestamp] JSON auto-fixed: $unix_path" >> "$validation_log"
                            validation_passed=true
                        else
                            # 恢复原文件
                            mv "$unix_path.backup" "$unix_path"
                        echo "[$timestamp] JSON auto-fix failed: $unix_path" >> "$validation_log"
                    fi
                fi
                
                # 检查必要字段（针对特定JSON文件）
                if [[ "$validation_passed" == "true" ]]; then
                    case "$file_name" in
                        "meta.json")
                            # 检查必要字段
                            required_fields=("chapter_number" "word_count" "last_modified")
                            for field in "${required_fields[@]}"; do
                                if ! jq -e ".$field" "$unix_path" >/dev/null 2>&1; then
                                    error_messages="$error_messages\nMissing required field: $field"
                                    validation_passed=false
                                fi
                            done
                            ;;
                            
                        "quality_check.json")
                            # 检查质量分数范围
                            score=$(jq -r '.overall_score // 0' "$unix_path" 2>/dev/null)
                            if [[ "$score" -lt 0 || "$score" -gt 100 ]]; then
                                error_messages="$error_messages\nInvalid score range: $score"
                                validation_passed=false
                            fi
                            ;;
                    esac
                fi
                ;;
                
            "yaml")
                # 验证YAML格式（使用Python）
                if command -v python3 >/dev/null 2>&1; then
                    if ! python3 -c "import yaml; yaml.safe_load(open('$unix_path'))" 2>/dev/null; then
                        validation_passed=false
                        error_messages="Invalid YAML syntax"
                        echo "[$timestamp] YAML validation failed: $unix_path" >> "$validation_log"
                    fi
                fi
                ;;
                
            "content")
                # 验证章节内容
                if [[ -f "$unix_path" ]]; then
                    # 检查文件是否为空
                    if [[ ! -s "$unix_path" ]]; then
                        validation_passed=false
                        error_messages="Content file is empty"
                    else
                        # 检查基本结构
                        has_chapter_header=$(grep -c "^#\s*Chapter" "$unix_path" 2>/dev/null || echo "0")
                        word_count=$(wc -w < "$unix_path" 2>/dev/null || echo "0")
                        
                        if [[ "$has_chapter_header" -eq 0 ]]; then
                            # 尝试修复：添加章节标题
                            chapter_num=$(echo "$file_dir" | grep -o 'ch[0-9]\+' | sed 's/ch0*//')
                            if [[ -n "$chapter_num" ]]; then
                                # 在文件开头添加章节标题
                                echo -e "# Chapter $chapter_num\n\n$(cat "$unix_path")" > "$unix_path.tmp"
                                mv "$unix_path.tmp" "$unix_path"
                                echo "[$timestamp] Added missing chapter header: $unix_path" >> "$validation_log"
                            fi
                        fi
                        
                        if [[ "$word_count" -lt 50 ]]; then
                            error_messages="$error_messages\nContent too short: $word_count words"
                            echo "[$timestamp] Warning: Content very short ($word_count words): $unix_path" >> "$validation_log"
                        fi
                    fi
                fi
                ;;
                
            "bible")
                # 验证Bible文件结构
                if command -v python3 >/dev/null 2>&1; then
                    python3 -c "
import yaml
import sys

try:
    with open('$unix_path', 'r') as f:
        data = yaml.safe_load(f)
    
    # 检查必要的顶级键
    required_keys = ['title', 'characters', 'universe']
    missing = [k for k in required_keys if k not in data]
    
    if missing:
        print(f'Missing required sections: {missing}')
        sys.exit(1)
    
    # 检查characters结构
    if not isinstance(data.get('characters'), dict):
        print('Characters section must be a dictionary')
        sys.exit(1)
        
except Exception as e:
    print(f'Bible validation error: {e}')
    sys.exit(1)
" 2>&1
                    
                    if [[ $? -ne 0 ]]; then
                        validation_passed=false
                        error_messages="Bible structure validation failed"
                    fi
                fi
                ;;
                
            "entity")
                # 验证实体字典
                if [[ -f "$unix_path" ]]; then
                    # 检查YAML格式和基本结构
                    if command -v python3 >/dev/null 2>&1; then
                        python3 -c "
import yaml
import sys

try:
    with open('$unix_path', 'r') as f:
        data = yaml.safe_load(f)
    
    if not isinstance(data, dict):
        print('Entity dictionary must be a dictionary')
        sys.exit(1)
    
    # 检查是否有entities键
    if 'entities' not in data and 'characters' not in data:
        print('Must have entities or characters section')
        sys.exit(1)
        
except Exception as e:
    print(f'Entity dictionary validation error: {e}')
    sys.exit(1)
" 2>&1
                        
                        if [[ $? -ne 0 ]]; then
                            validation_passed=false
                            error_messages="Entity dictionary structure invalid"
                        fi
                    fi
                fi
                ;;
        esac
        
        # 记录验证结果
        if [[ "$validation_passed" == "true" ]]; then
            echo "[$timestamp] ✓ Validation passed: $unix_path" >> "$validation_log"
        else
            echo "[$timestamp] ✗ Validation failed: $unix_path" >> "$validation_log"
            echo "  Errors: $error_messages" >> "$validation_log"
            
            # 创建验证失败报告
            failure_report="$PROJECT_ROOT/.claude/validation/failure_$(date +%Y%m%d_%H%M%S).txt"
            cat > "$failure_report" << EOF
Validation Failure Report
========================
Time: $timestamp
File: $unix_path
Type: $validation_type
Session: $session_id

Errors:
$error_messages

File Content (first 50 lines):
$(head -50 "$unix_path" 2>/dev/null)

Recommendation:
Please review and fix the file manually or regenerate it.
EOF
            
            # 用户警告（但不阻塞）
            echo "⚠️ Validation warning for $file_name - see $failure_report for details" >&2
        fi
        
        # 特殊处理：如果是关键文件且验证失败，创建修复任务
        if [[ "$validation_passed" == "false" ]]; then
            case "$validation_type" in
                "bible"|"entity")
                    # 关键文件，需要立即修复
                    fix_task="$PROJECT_ROOT/.claude/validation/fix_required.txt"
                    echo "[$timestamp] CRITICAL: Fix required for $unix_path" >> "$fix_task"
                    ;;
            esac
        fi
    fi
fi

# 成功退出（不阻塞，只警告）
exit 0