#!/bin/bash

# PostToolUse Hook: Incremental Project Statistics Updater
# 增量更新项目统计信息，避免每次重新计算全部数据

# 设置项目根目录
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"
mkdir -p "$PROJECT_ROOT/.claude/stats"
mkdir -p "$PROJECT_ROOT/.claude/stats/cache"

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

# 检查是否需要更新统计信息
should_update=false
update_type=""
affected_project=""
affected_book=""
affected_chapter=""

if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    # 分析文件路径，提取项目/书籍/章节信息
    if [[ "$file_path" =~ .claude/data/projects/([^/\\]+)/book_([0-9]+)/chapters/ch([0-9]+)/ ]]; then
        affected_project="${BASH_REMATCH[1]}"
        affected_book="${BASH_REMATCH[2]}"
        affected_chapter="${BASH_REMATCH[3]}"
        
        # 章节内容变化
        if [[ "$file_path" == */content.md ]]; then
            should_update=true
            update_type="content"
        # 质量检查完成
        elif [[ "$file_path" == */quality_check.json ]]; then
            should_update=true
            update_type="quality"
        fi
        
    elif [[ "$file_path" =~ .claude/data/projects/([^/\\]+)/book_([0-9]+)/ ]]; then
        affected_project="${BASH_REMATCH[1]}"
        affected_book="${BASH_REMATCH[2]}"
        
        # Bible文件更新
        if [[ "$file_path" == */bible.yaml || "$file_path" == */bible.yml ]]; then
            should_update=true
            update_type="bible"
        # Book Outline文件更新
        elif [[ "$file_path" == */outline.yaml || "$file_path" == */book_outline.yaml ]]; then
            should_update=true
            update_type="outline"
        fi
        
    elif [[ "$file_path" =~ .claude/data/projects/([^/\\]+)/ ]]; then
        affected_project="${BASH_REMATCH[1]}"
        
        # Series Bible文件更新
        if [[ "$file_path" == */series_bible.yaml || "$file_path" == */series_bible.yml ]]; then
            should_update=true
            update_type="series_bible"
        fi
    fi
fi

if [[ "$should_update" == "true" ]]; then
    
    current_time=$(date '+%Y-%m-%d %H:%M:%S')
    stats_file="$PROJECT_ROOT/.claude/stats/project_stats.json"
    temp_stats="$stats_file.tmp"
    
    # 增量更新统计信息
    case "$update_type" in
        
        "content")
            # 章节内容更新：只更新该章节的字数统计
            if [[ -f "$unix_path" ]]; then
                word_count=$(wc -w < "$unix_path" 2>/dev/null || echo "0")
                char_count=$(wc -c < "$unix_path" 2>/dev/null || echo "0")
                
                # 缓存该章节的统计信息
                chapter_cache="$PROJECT_ROOT/.claude/stats/cache/${affected_project}_book${affected_book}_ch${affected_chapter}.json"
                
                cat > "$chapter_cache" << EOF
{
    "project": "$affected_project",
    "book": "$affected_book", 
    "chapter": "$affected_chapter",
    "word_count": $word_count,
    "char_count": $char_count,
    "last_updated": "$current_time",
    "file_path": "$unix_path"
}
EOF
                
                # 更新用户反馈
                echo "📊 Stats: Chapter $affected_chapter updated ($word_count words)"
            fi
            ;;
            
        "quality")
            # 质量报告更新：只更新该章节的质量分数
            if [[ -f "$unix_path" ]] && jq empty "$unix_path" 2>/dev/null; then
                overall_score=$(jq -r '.overall_score // 0' "$unix_path" 2>/dev/null || echo "0")
                
                # 缓存该章节的质量信息
                quality_cache="$PROJECT_ROOT/.claude/stats/cache/${affected_project}_book${affected_book}_ch${affected_chapter}_quality.json"
                
                cat > "$quality_cache" << EOF
{
    "project": "$affected_project",
    "book": "$affected_book",
    "chapter": "$affected_chapter", 
    "overall_score": $overall_score,
    "last_updated": "$current_time",
    "file_path": "$unix_path"
}
EOF
                
                echo "📊 Stats: Chapter $affected_chapter quality score $overall_score"
            fi
            ;;
            
        "bible"|"outline"|"series_bible")
            # 非章节文件更新：记录更新时间但不做复杂计算
            meta_cache="$PROJECT_ROOT/.claude/stats/cache/${affected_project}_${update_type}.json"
            
            cat > "$meta_cache" << EOF
{
    "project": "$affected_project",
    "book": "${affected_book:-"series"}",
    "type": "$update_type",
    "last_updated": "$current_time",
    "file_path": "$unix_path"
}
EOF
            
            echo "📊 Stats: $update_type updated for $affected_project"
            ;;
    esac
    
    # 每15个增量更新后，或重要文件更新时，重新聚合统计信息
    should_aggregate=false
    
    # 检查缓存文件数量
    cache_count=$(find "$PROJECT_ROOT/.claude/stats/cache" -name "*.json" -type f 2>/dev/null | wc -l || echo "0")
    
    if [[ "$cache_count" -ge 15 ]]; then
        should_aggregate=true
    fi
    
    # 重要文件立即聚合
    if [[ "$update_type" == "series_bible" || "$update_type" == "bible" ]]; then
        should_aggregate=true
    fi
    
    # 执行聚合统计
    if [[ "$should_aggregate" == "true" ]]; then
        
        echo "📊 Aggregating project statistics..."
        
        # 聚合所有缓存文件的统计信息
        total_words=0
        total_chapters=0
        quality_scores=()
        projects_data="{}"
        
        # 处理章节内容缓存
        if compgen -G "$PROJECT_ROOT/.claude/stats/cache/*_ch*.json" > /dev/null 2>&1; then
            for cache_file in "$PROJECT_ROOT/.claude/stats/cache"/*_ch*.json; do
                if [[ -f "$cache_file" ]] && jq empty "$cache_file" 2>/dev/null; then
                    word_count=$(jq -r '.word_count // 0' "$cache_file" 2>/dev/null || echo "0")
                    if [[ "$word_count" =~ ^[0-9]+$ ]]; then
                        total_words=$((total_words + word_count))
                        total_chapters=$((total_chapters + 1))
                    fi
                fi
            done
        fi
        
        # 处理质量分数缓存
        if compgen -G "$PROJECT_ROOT/.claude/stats/cache/*_quality.json" > /dev/null 2>&1; then
            for quality_file in "$PROJECT_ROOT/.claude/stats/cache"/*_quality.json; do
                if [[ -f "$quality_file" ]] && jq empty "$quality_file" 2>/dev/null; then
                    score=$(jq -r '.overall_score // 0' "$quality_file" 2>/dev/null || echo "0")
                    if [[ "$score" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
                        quality_scores+=("$score")
                    fi
                fi
            done
        fi
        
        # 计算平均质量分数
        avg_quality=0
        if [[ ${#quality_scores[@]} -gt 0 ]]; then
            total_quality=0
            for score in "${quality_scores[@]}"; do
                total_quality=$(echo "$total_quality + $score" | bc 2>/dev/null || echo "$total_quality")
            done
            avg_quality=$(echo "scale=1; $total_quality / ${#quality_scores[@]}" | bc 2>/dev/null || echo "0")
        fi
        
        # 生成聚合统计报告
        cat > "$temp_stats" << EOF
{
    "last_updated": "$current_time",
    "aggregation_type": "incremental",
    "statistics": {
        "total_words": $total_words,
        "total_chapters": $total_chapters,
        "average_quality": $avg_quality,
        "quality_samples": ${#quality_scores[@]},
        "cache_files_processed": $cache_count
    },
    "performance": {
        "incremental_update": true,
        "full_scan_avoided": true,
        "cache_files_used": $cache_count
    }
}
EOF
        
        # 更新统计文件
        if jq empty "$temp_stats" 2>/dev/null; then
            mv "$temp_stats" "$stats_file"
            
            # 清空缓存文件（聚合完成后）
            rm -f "$PROJECT_ROOT/.claude/stats/cache"/*.json 2>/dev/null
            
            echo "📊 Project stats updated: $total_chapters chapters, $total_words words, avg quality ${avg_quality}"
            
            # 记录到日志
            echo "[$current_time] Incremental stats update: $total_chapters ch, $total_words words, ${#quality_scores[@]} quality scores" >> "$PROJECT_ROOT/.claude/logs/stats-update.log"
            
        else
            # 聚合失败，保留缓存文件
            rm -f "$temp_stats" 2>/dev/null
            echo "⚠️ Stats aggregation failed, keeping cache files"
        fi
    else
        # 不需要聚合，只是增量更新
        echo "📊 Incremental update cached ($cache_count pending aggregation)"
    fi
    
else
    # 不需要更新统计信息的文件
    if [[ "$tool_name" == "Write" && -n "$file_path" ]]; then
        echo "📊 Stats: File $(basename "$file_path") - no stats update needed"
    fi
fi

# 成功退出
exit 0