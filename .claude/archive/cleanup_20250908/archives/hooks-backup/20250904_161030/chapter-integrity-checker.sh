#!/bin/bash

# PostToolUse Hook: Chapter file integrity checker
# 检查章节文件结构完整性，自动修复缺失文件
# 环境变量 HOOKS_WARNING_ONLY=true 时只输出警告而不创建文件

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

# 警告模式处理函数
warn_instead_of_create() {
    local file_type="$1"
    local file_path="$2" 
    local description="$3"
    
    if [[ "$WARNING_ONLY" == "true" ]]; then
        echo "⚠️  [WARNING] Would create missing $file_type: $(basename "$file_path") - File not created (HOOKS_WARNING_ONLY=true)"
        echo "   Description: $description"
        echo "   To create this file, run with HOOKS_WARNING_ONLY=false"
        return 0  # Return success to indicate warning was handled
    fi
    return 1  # Return failure to indicate normal creation should proceed
}

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

# 检查是否是章节相关文件操作
if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    # 检查是否是章节目录中的文件
    if ([[ "$file_path" == */chapters/ch*/content.md ]] || [[ "$file_path" == *\\chapters\\ch*\\content.md ]]) || ([[ "$file_path" == */chapters/ch*/meta.json ]] || [[ "$file_path" == *\\chapters\\ch*\\meta.json ]]) || ([[ "$file_path" == */chapters/ch*/outline.json ]] || [[ "$file_path" == *\\chapters\\ch*\\outline.json ]]); then
        
        chapter_dir=$(dirname "$unix_path")
        chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
        current_time=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')
        
        # 定义必需文件
        content_file="$chapter_dir/content.md"
        meta_file="$chapter_dir/meta.json"
        outline_file="$chapter_dir/outline.json"
        
        issues_found=()
        fixes_applied=()
        
        # 如果是警告模式，只检查并输出警告
        if [[ "$WARNING_ONLY" == "true" ]]; then
            echo "⚠️  [WARNING] Chapter integrity check in warning mode - No files will be created/modified"
            missing_files=()
            [[ ! -f "$content_file" ]] && missing_files+=("content.md")
            [[ ! -f "$meta_file" ]] && missing_files+=("meta.json") 
            [[ ! -f "$outline_file" ]] && missing_files+=("outline.json")
            
            if [[ ${#missing_files[@]} -gt 0 ]]; then
                echo "   Missing files in chapter $chapter_num:"
                for file in "${missing_files[@]}"; do
                    echo "   - $file"
                done
                echo "   To create these files, run with HOOKS_WARNING_ONLY=false"
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Chapter $chapter_num integrity issues detected but skipped" >> "$PROJECT_ROOT/.claude/logs/integrity.log"
            else
                echo "   Chapter $chapter_num structure is complete"
            fi
            exit 0
        fi
        
        # 检查content.md
        if [[ ! -f "$content_file" ]]; then
            issues_found+=("Missing content.md")
            
            
            # 创建基础content.md模板
            cat > "$content_file" << EOF
# Chapter $chapter_num

*[Chapter content will be written here]*

## Scene 1

[Scene content...]

---

*End of Chapter $chapter_num*
EOF
            fixes_applied+=("Created content.md template")
        fi
        
        # 检查meta.json
        if [[ ! -f "$meta_file" ]]; then
            issues_found+=("Missing meta.json")
            
            # 计算现有内容字数 (如果content.md存在)
            word_count=0
            if [[ -f "$content_file" ]]; then
                word_count=$(wc -w "$content_file" 2>/dev/null | cut -d' ' -f1 || echo "0")
            fi
            
            # 创建meta.json
            cat > "$meta_file" << EOF
{
  "chapter_number": $chapter_num,
  "title": "Chapter $chapter_num",
  "status": "draft",
  "word_count": $word_count,
  "character_count": 0,
  "estimated_scenes": 1,
  "dialogue_lines": 0,
  "created": "$current_time",
  "last_modified": "$current_time",
  "auto_created": true,
  "integrity_check": true
}
EOF
            fixes_applied+=("Created meta.json with basic info")
            
        else
            # 验证meta.json格式
            if ! jq empty "$meta_file" 2>/dev/null; then
                issues_found+=("Invalid meta.json format")
                
                # 备份损坏的meta.json
                cp "$meta_file" "$meta_file.backup.$(date +%H%M%S)" 2>/dev/null
                
                # 重新创建
                cat > "$meta_file" << EOF
{
  "chapter_number": $chapter_num,
  "title": "Chapter $chapter_num", 
  "status": "needs_review",
  "word_count": 0,
  "character_count": 0,
  "estimated_scenes": 1,
  "dialogue_lines": 0,
  "created": "$current_time",
  "last_modified": "$current_time",
  "auto_repaired": true,
  "integrity_check": true
}
EOF
                fixes_applied+=("Repaired corrupted meta.json")
            fi
        fi
        
        # 检查outline.json (可选但推荐)
        if [[ ! -f "$outline_file" ]]; then
            # 只记录缺失，不自动创建 (outline需要人工设计)
            issues_found+=("Missing outline.json (optional)")
            
            # 创建基础outline模板
            cat > "$outline_file" << EOF
{
  "chapter_number": $chapter_num,
  "scenes": [
    {
      "scene_number": 1,
      "location": "TBD",
      "characters": [],
      "purpose": "TBD",
      "notes": "Auto-generated template"
    }
  ],
  "chapter_arc": "TBD",
  "key_events": [],
  "created": "$current_time",
  "auto_created": true,
  "template_version": "basic"
}
EOF
            fixes_applied+=("Created outline.json template")
        fi
        
        # 检查章节目录结构
        context_dir="$chapter_dir/context"
        if [[ ! -d "$context_dir" ]]; then
            mkdir -p "$context_dir"
            fixes_applied+=("Created context/ directory")
        fi
        
        # 验证文件权限 (Windows兼容)
        for check_file in "$content_file" "$meta_file" "$outline_file"; do
            if [[ -f "$check_file" && ! -r "$check_file" ]]; then
                issues_found+=("Unreadable: $(basename "$check_file")")
                # 尝试修复权限 (Windows下可能无效)
                chmod 644 "$check_file" 2>/dev/null && fixes_applied+=("Fixed permissions for $(basename "$check_file")")
            fi
        done
        
        # 记录检查结果
        if [[ ${#issues_found[@]} -gt 0 ]]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Chapter $chapter_num integrity check:" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
            
            for issue in "${issues_found[@]}"; do
                echo "  - ISSUE: $issue" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
            done
            
            for fix in "${fixes_applied[@]}"; do
                echo "  - FIXED: $fix" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
            done
            
            # 用户提示
            if [[ ${#fixes_applied[@]} -gt 0 ]]; then
                echo "🔧 Chapter $chapter_num integrity: fixed ${#fixes_applied[@]} issues"
                for fix in "${fixes_applied[@]}"; do
                    echo "  ✓ $fix"
                done
            fi
            
            remaining_issues=$((${#issues_found[@]} - ${#fixes_applied[@]}))
            if [[ "$remaining_issues" -gt 0 ]]; then
                echo "⚠️  Chapter $chapter_num: $remaining_issues issues need manual review"
            fi
        else
            # 一切正常
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Chapter $chapter_num: integrity OK" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
        fi
        
    # 检查Bible文件完整性
    elif ([[ "$file_path" == *bible.yaml ]] || [[ "$file_path" == *\\bible.yaml ]]) || ([[ "$file_path" == *bible.yml ]] || [[ "$file_path" == *\\bible.yml ]]); then
        
        if [[ -f "$unix_path" ]]; then
            # 验证YAML格式
            if ! python -c "import yaml; yaml.safe_load(open('$unix_path'))" 2>/dev/null; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Bible YAML format invalid: $unix_path" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
                echo "⚠️  Bible file has invalid YAML format - please check syntax"
            else
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bible file integrity OK: $(basename "$unix_path")" >> "$PROJECT_ROOT/.claude/logs/integrity-checks.log"
            fi
        fi
        
    fi
fi

# 成功退出
exit 0