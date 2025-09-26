#!/bin/bash

# PostToolUse Hook: Smart backup for critical project files
# 智能备份重要文件：Bible、章节内容、配置等

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

# Convert Windows paths to Unix paths for compatibility
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 检查是否是需要备份的文件类型
should_backup=false

# 定义需要备份的文件类型
if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    # Bible文件 (最高优先级)
    if ([[ "$file_path" == *bible.yaml ]] || [[ "$file_path" == *\\bible.yaml ]]) || ([[ "$file_path" == *bible.yml ]] || [[ "$file_path" == *\\bible.yml ]]); then
        should_backup=true
        backup_type="bible"
        
    # 章节内容文件 
    elif ([[ "$file_path" == */content.md ]] || [[ "$file_path" == *\\content.md ]]); then
        should_backup=true
        backup_type="content"
        
    # 项目配置文件
    elif ([[ "$file_path" == */project.json ]] || [[ "$file_path" == *\\project.json ]]); then
        should_backup=true
        backup_type="config"
        
    # Entity Dictionary (重要配置)
    elif ([[ "$file_path" == */entity_dictionary.yaml ]] || [[ "$file_path" == *\\entity_dictionary.yaml ]]); then
        should_backup=true
        backup_type="entity"
        
    # Context文件 (角色、世界、剧情)
    elif ([[ "$file_path" == */context/*.json ]] || [[ "$file_path" == *\\context\\*.json ]]); then
        should_backup=true  
        backup_type="context"
        
    # 质量检查结果 (保留历史记录)
    elif ([[ "$file_path" == */quality_check.json ]] || [[ "$file_path" == *\\quality_check.json ]]) || ([[ "$file_path" == */quality_report.json ]] || [[ "$file_path" == *\\quality_report.json ]]); then
        should_backup=true
        backup_type="quality"
    fi
fi

# 执行智能备份
if [[ "$should_backup" == "true" && -f "$unix_path" ]]; then
    
    # 创建按日期组织的备份目录
    backup_date=$(date +%Y%m%d)
    backup_time=$(date +%H%M%S)
    backup_dir="$PROJECT_ROOT/.claude/backups/$backup_date"
    
    # 确保备份目录存在
    mkdir -p "$backup_dir"
    
    # 生成备份文件名 (包含时间戳和类型)
    file_basename=$(basename "$file_path")
    file_extension="${file_basename##*.}"
    file_name_only="${file_basename%.*}"
    
    backup_filename="${file_name_only}_${backup_type}_${backup_time}.${file_extension}"
    backup_full_path="$backup_dir/$backup_filename"
    
    # 执行备份
    if cp "$unix_path" "$backup_full_path" 2>/dev/null; then
        
        # 获取文件大小 (用于日志)
        file_size=$(wc -c < "$unix_path" 2>/dev/null || echo "unknown")
        
        # 记录成功备份
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backed up $backup_type: $(basename "$file_path") (${file_size}b)" >> "$PROJECT_ROOT/.claude/logs/backup.log"
        
        # 用户提示 (简洁版)
        case "$backup_type" in
            "bible") echo "💾 Bible backed up automatically" ;;
            "content") chapter_num=$(echo "$unix_path" | grep -o 'ch[0-9]*' | sed 's/ch0*//'); echo "💾 Chapter $chapter_num content backed up" ;;
            "config") echo "💾 Project config backed up" ;;
            "entity") echo "💾 Entity dictionary backed up" ;;
            "context") context_type=$(basename "$file_path" .json); echo "💾 $context_type context backed up" ;;
            "quality") echo "💾 Quality report backed up" ;;
        esac
        
        # 清理旧备份 (保留最近7天) - 内联处理
        backup_root="$PROJECT_ROOT/.claude/backups"
        find "$backup_root" -type d -name "20*" -mtime +7 -exec rm -rf {} + 2>/dev/null
        
        # 记录清理操作 (每天只记录一次)
        cleanup_marker="$backup_root/.last_cleanup"
        today=$(date +%Y%m%d)
        
        if [[ ! -f "$cleanup_marker" ]] || [[ "$(cat "$cleanup_marker" 2>/dev/null)" != "$today" ]]; then
            echo "$today" > "$cleanup_marker"
            backup_size=$(du -sh "$backup_root" 2>/dev/null | cut -f1 || echo "unknown")
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleanup: keeping 7 days, total size: $backup_size" >> "$PROJECT_ROOT/.claude/logs/backup.log"
        fi
        
    else
        # 备份失败日志
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAILED backup of $backup_type: $(basename "$file_path")" >> "$PROJECT_ROOT/.claude/logs/backup.log"
    fi
    
fi

# 成功退出
exit 0