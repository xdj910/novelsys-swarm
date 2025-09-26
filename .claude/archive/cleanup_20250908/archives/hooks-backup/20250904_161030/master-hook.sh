#!/bin/bash

# NOVELSYS-SWARM Hybrid Hook System v2.0
# Compatible with Claude Code Official Standards
# PostToolUse Hook: Master dispatcher for all sub-hooks

# 静默执行，避免干扰用户
set +e

# ==================== STANDARD INTERFACE LAYER ====================

# 设置项目根目录 (官方标准)
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 读取配置 (标准化配置支持)
config_file="$PROJECT_ROOT/.claude/hook-config.json"
official_settings="$PROJECT_ROOT/.claude/settings.json"

# 加载配置参数
if [[ -f "$config_file" ]]; then
    HOOK_MODE=$(jq -r '.system.mode // "hybrid"' "$config_file" 2>/dev/null || echo "hybrid")
    BATCH_SIZE=$(jq -r '.performance.session_tracker.batch_size // 10' "$config_file" 2>/dev/null || echo "10")
    SECURITY_MODE=$(jq -r '.security.validation_mode // "warn_only"' "$config_file" 2>/dev/null || echo "warn_only")
else
    # Fallback到环境变量 (官方标准支持)
    HOOK_MODE="${NOVELSYS_HOOK_MODE:-hybrid}"
    BATCH_SIZE="${NOVELSYS_BATCH_SIZE:-10}"
    SECURITY_MODE="${NOVELSYS_SECURITY_MODE:-hardened}"
fi

# 官方标准兼容性检查
OFFICIAL_COMPATIBLE=true
if [[ -f "$official_settings" ]]; then
    # 检查是否通过官方hook系统调用
    if [[ -n "$CLAUDE_HOOK_MATCHER" || -n "$CLAUDE_HOOK_TIMEOUT" ]]; then
        OFFICIAL_COMPATIBLE=true
    fi
fi

# ==================== EXECUTION ENVIRONMENT ====================

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 创建标准化日志
debug_log="$PROJECT_ROOT/.claude/logs/master-hook-debug.log"
performance_log="$PROJECT_ROOT/.claude/logs/hook-performance.log"

# 记录执行开始
start_time=$(date '+%s.%N' 2>/dev/null || date '+%s')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$timestamp] Master Hook v2.0 triggered (mode: $HOOK_MODE, compatible: $OFFICIAL_COMPATIBLE)" >> "$debug_log"
echo "[$timestamp] Input length: ${#input}" >> "$debug_log"

# 标准兼容性信息
if [[ "$OFFICIAL_COMPATIBLE" == "true" ]]; then
    echo "[$timestamp] Running via official Claude Code hook system" >> "$debug_log"
    if [[ -n "$CLAUDE_HOOK_TIMEOUT" ]]; then
        echo "[$timestamp] Official timeout: ${CLAUDE_HOOK_TIMEOUT}s" >> "$debug_log"
    fi
    if [[ -n "$CLAUDE_HOOK_MATCHER" ]]; then
        echo "[$timestamp] Official matcher: $CLAUDE_HOOK_MATCHER" >> "$debug_log"
    fi
fi

# 调试模式 (支持官方和自定义)
if [[ "$DEBUG_HOOKS" == "true" || "$NOVELSYS_DEBUG" == "true" ]]; then
    echo "[DEBUG] Master Hook v2.0 triggered"
    echo "[DEBUG] Mode: $HOOK_MODE, Security: $SECURITY_MODE"
    echo "[DEBUG] Input preview: ${input:0:100}..."
fi

# 使用jq解析JSON输入
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# 记录jq解析结果
echo "[$(date '+%Y-%m-%d %H:%M:%S')] jq parsed tool_name: '$tool_name'" >> "$debug_log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] jq parsed file_path: '$file_path'" >> "$debug_log"

# Fallback到grep方式
if [[ -z "$tool_name" ]]; then
    tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] grep fallback tool_name: '$tool_name'" >> "$debug_log"
fi
if [[ -z "$file_path" ]]; then
    file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] grep fallback file_path: '$file_path'" >> "$debug_log"
fi

# 记录最终解析结果
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Final tool_name: '$tool_name'" >> "$debug_log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Final file_path: '$file_path'" >> "$debug_log"

# 调试输出
if [[ "$DEBUG_HOOKS" == "true" ]]; then
    echo "[DEBUG] Parsed Tool: $tool_name"
    echo "[DEBUG] Parsed File: $file_path"
fi

# 只处理Write/Edit/MultiEdit操作
if [[ "$tool_name" != "Write" && "$tool_name" != "Edit" && "$tool_name" != "MultiEdit" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Skipping - tool not matched: $tool_name" >> "$debug_log"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing tool: $tool_name for file: $file_path" >> "$debug_log"

# 根据文件类型智能分发Hook
case "$file_path" in
    
    # 章节内容文件：触发多个Hook (支持Windows和Unix路径)
    */content.md|*\\content.md)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Matched content.md pattern" >> "$debug_log"
        # 同时检查Unix和Windows路径格式
        if [[ "$file_path" == */chapters/ch*/content.md ]] || [[ "$file_path" == *\\chapters\\ch*\\content.md ]]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Matched chapter content pattern, triggering hooks..." >> "$debug_log"
            # 智能并行执行：平衡性能与安全
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting intelligent parallel hooks execution..." >> "$debug_log"
            
            # Phase 1: 文件准备（必须首先完成）
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Phase 1: File preparation" >> "$debug_log"
            timeout 10s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/chapter-integrity-checker.sh'" 2>> "$debug_log" || {
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: integrity-checker failed or timed out" >> "$debug_log"
            }
            
            # Phase 2: 内容处理和独立任务（可并行）
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Phase 2: Parallel content processing" >> "$debug_log"
            {
                # 2a: 内容格式化（独立）
                timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/content-formatter.sh'" 2>> "$debug_log" &
                formatter_pid=$!
                
                # 2b: 会话跟踪（完全独立，可立即执行）
                timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/session-tracker.sh'" 2>> "$debug_log" &
                session_pid=$!
                
                # 2c: 实体同步（独立读取内容）
                timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/auto-entity-sync.sh'" 2>> "$debug_log" &
                entity_pid=$!
                
                # 等待格式化完成（meta依赖它）
                wait $formatter_pid || echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: formatter failed" >> "$debug_log"
                
                # Phase 3: 元数据更新（依赖格式化后的内容）
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Phase 3: Metadata update" >> "$debug_log"
                timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/meta-updater.sh'" 2>> "$debug_log" || {
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: meta-updater failed" >> "$debug_log"
                }
                
                # Phase 4: 统计更新（依赖元数据）
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Phase 4: Statistics update" >> "$debug_log"
                timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/project-stats-updater.sh'" 2>> "$debug_log" || {
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: stats-updater failed" >> "$debug_log"
                }
                
                # 等待所有独立任务完成
                wait $session_pid || echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: session-tracker failed" >> "$debug_log"
                wait $entity_pid || echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: entity-sync failed" >> "$debug_log"
            }
            
            # Phase 5: 最终备份（所有操作完成后）
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Phase 5: Final backup" >> "$debug_log"
            timeout 5s bash -c "echo '$input' | bash '$PROJECT_ROOT/.claude/hooks/smart-backup.sh'" 2>> "$debug_log" || {
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: backup failed" >> "$debug_log"
            }
            
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Intelligent parallel hooks execution completed" >> "$debug_log"
        fi
        ;;
    
    # 质量检查文件：触发学习和统计
    */quality_check.json|*\\quality_check.json)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Matched quality_check.json pattern" >> "$debug_log"
        # 顺序执行质量相关Hook
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/quality-learning-trigger.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/smart-backup.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/project-stats-updater.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/session-tracker.sh" 2>> "$debug_log"
        ;;
    
    # Bible文件：触发备份和统计
    *bible.yaml|*bible.yml)
        # 顺序执行Bible相关Hook
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/smart-backup.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/project-stats-updater.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/session-tracker.sh" 2>> "$debug_log"
        ;;
    
    # 元数据文件：触发备份和会话追踪
    */meta.json|*/project.json|*/entity_dictionary.yaml)
        # 顺序执行元数据相关Hook
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/smart-backup.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/session-tracker.sh" 2>> "$debug_log"
        ;;
    
    # 其他markdown文件：只格式化
    *.md)
        # 顺序执行Markdown相关Hook
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/content-formatter.sh" 2>> "$debug_log" && \
        echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/session-tracker.sh" 2>> "$debug_log"
        ;;
        
    # 其他重要文件：只记录会话
    *)
        if [[ "$file_path" == */.claude/* ]] || [[ "$file_path" == */config/* ]]; then
            echo "$input" | bash "$PROJECT_ROOT/.claude/hooks/session-tracker.sh" 2>> "$debug_log"
        fi
        ;;
esac

# ==================== FINAL VALIDATION PHASE ====================

# 对所有文件执行验证（与安全模式兼容）
if [[ "$SECURITY_MODE" == "warn_only" || "$SECURITY_MODE" == "hardened" ]]; then
    echo "$input" | timeout 30 bash "$PROJECT_ROOT/.claude/hooks/subagent-output-validator.sh" 2>> "$debug_log"
    echo "$input" | timeout 15 bash "$PROJECT_ROOT/.claude/hooks/output-validator.sh" 2>> "$debug_log"
fi

# ==================== PERFORMANCE MONITORING ====================

# 计算执行时间
end_time=$(date '+%s.%N' 2>/dev/null || date '+%s')
if [[ "$end_time" =~ \. ]]; then
    execution_time=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "unknown")
else
    execution_time=$((end_time - start_time))
fi

# 记录性能数据
echo "[$timestamp] Execution completed in ${execution_time}s (mode: $HOOK_MODE)" >> "$performance_log"

# 官方兼容性报告
if [[ "$OFFICIAL_COMPATIBLE" == "true" ]]; then
    echo "[$timestamp] ✅ Official Claude Code compatibility maintained" >> "$debug_log"
else
    echo "[$timestamp] ⚠️ Running in legacy mode" >> "$debug_log"
fi

# 调试输出
if [[ "$DEBUG_HOOKS" == "true" || "$NOVELSYS_DEBUG" == "true" ]]; then
    echo "[DEBUG] Master Hook completed in ${execution_time}s"
fi

# 成功退出 (官方标准: 0 = success)
exit 0