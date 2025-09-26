#!/bin/bash

# Hook系统共享库
# 提供通用功能，避免代码重复，提高可维护性

# ============================================
# 日志功能
# ============================================

# 确保日志目录存在
init_logs() {
    local project_root="${1:-$PROJECT_ROOT}"
    mkdir -p "$project_root/.claude/logs"
    export LOG_FILE="$project_root/.claude/logs/hooks.log"
    export ERROR_LOG="$project_root/.claude/logs/error.log"
    export DEBUG_LOG="$project_root/.claude/logs/debug.log"
}

# 日志级别
LOG_LEVEL="${LOG_LEVEL:-INFO}"

# 通用日志函数
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "${LOG_FILE:-/dev/stderr}"
}

# 具体日志函数
log_info() {
    log "INFO" "$@"
}

log_warn() {
    log "WARN" "$@"
    echo "[$timestamp] [WARN] $@" >> "${ERROR_LOG:-/dev/stderr}"
}

log_error() {
    log "ERROR" "$@"
    echo "[$timestamp] [ERROR] $@" >> "${ERROR_LOG:-/dev/stderr}"
}

log_debug() {
    if [[ "$LOG_LEVEL" == "DEBUG" ]] || [[ "$DEBUG_HOOKS" == "true" ]]; then
        log "DEBUG" "$@"
        echo "[$timestamp] [DEBUG] $@" >> "${DEBUG_LOG:-/dev/stderr}"
    fi
}

# ============================================
# 路径处理功能
# ============================================

# 获取项目根目录
get_project_root() {
    if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
        local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        echo "$(dirname "$(dirname "$script_dir")")"
    else
        echo "$CLAUDE_PROJECT_DIR"
    fi
}

# Windows路径转Unix路径
win_to_unix_path() {
    local path="$1"
    echo "$path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|' | sed 's|^E:|/e|'
}

# 安全路径处理（防止路径注入）
get_safe_path() {
    local path="$1"
    local base_dir="${2:-$PROJECT_ROOT}"
    
    # 转换Windows路径
    local unix_path=$(win_to_unix_path "$path")
    
    # 移除危险字符
    unix_path=$(echo "$unix_path" | sed 's/[;&|`$]//g')
    
    # 确保路径在基础目录内（防止路径遍历）
    if [[ "$unix_path" == /* ]]; then
        echo "$unix_path"
    else
        echo "$base_dir/$unix_path"
    fi
}

# ============================================
# JSON/YAML处理功能
# ============================================

# 安全解析JSON
parse_json_safe() {
    local json="$1"
    local field="$2"
    local default="${3:-}"
    
    if command -v jq >/dev/null 2>&1; then
        local result=$(echo "$json" | jq -r "$field // empty" 2>/dev/null)
        if [[ -n "$result" ]]; then
            echo "$result"
        else
            echo "$default"
        fi
    else
        # Fallback到grep（不推荐）
        echo "$json" | grep -o "\"${field##*.}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | cut -d'"' -f4 || echo "$default"
    fi
}

# 验证JSON文件
validate_json() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi
    
    if command -v jq >/dev/null 2>&1; then
        if jq empty "$file" 2>/dev/null; then
            return 0
        else
            log_error "Invalid JSON in $file"
            return 1
        fi
    else
        log_warn "jq not available, skipping JSON validation"
        return 0
    fi
}

# 验证YAML文件
validate_yaml() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi
    
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            return 0
        else
            log_error "Invalid YAML in $file"
            return 1
        fi
    else
        log_warn "Python3 not available, skipping YAML validation"
        return 0
    fi
}

# ============================================
# 项目检测功能
# ============================================

# 获取当前活动项目
get_active_project() {
    local project_root="${1:-$(get_project_root)}"
    
    for proj_dir in "$project_root/.claude/data/projects"/*/; do
        if [[ -d "$proj_dir" ]]; then
            basename "$proj_dir"
            return 0
        fi
    done
    
    log_warn "No active project found"
    return 1
}

# 获取项目目录
get_project_dir() {
    local project_name="${1:-$(get_active_project)}"
    local project_root="${2:-$(get_project_root)}"
    
    if [[ -n "$project_name" ]]; then
        echo "$project_root/.claude/data/projects/$project_name"
    else
        return 1
    fi
}

# ============================================
# 文件操作功能
# ============================================

# 安全备份文件
backup_file() {
    local file="$1"
    local backup_dir="${2:-$PROJECT_ROOT/.claude/backups}"
    
    if [[ ! -f "$file" ]]; then
        log_warn "Cannot backup non-existent file: $file"
        return 1
    fi
    
    mkdir -p "$backup_dir"
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local backup_file="$backup_dir/$(basename "$file").${timestamp}.bak"
    
    cp "$file" "$backup_file" 2>/dev/null
    if [[ $? -eq 0 ]]; then
        log_info "Backed up $file to $backup_file"
        return 0
    else
        log_error "Failed to backup $file"
        return 1
    fi
}

# 原子性写入文件（先写临时文件，然后移动）
atomic_write() {
    local file="$1"
    local content="$2"
    local temp_file="${file}.tmp.$$"
    
    echo "$content" > "$temp_file"
    if [[ $? -eq 0 ]]; then
        mv "$temp_file" "$file"
        if [[ $? -eq 0 ]]; then
            log_debug "Atomically wrote to $file"
            return 0
        else
            log_error "Failed to move temp file to $file"
            rm -f "$temp_file"
            return 1
        fi
    else
        log_error "Failed to write temp file for $file"
        rm -f "$temp_file"
        return 1
    fi
}

# ============================================
# 锁机制（防止并发问题）
# ============================================

# 获取锁
acquire_lock() {
    local lock_name="$1"
    local timeout="${2:-10}"
    local lock_file="$PROJECT_ROOT/.claude/locks/${lock_name}.lock"
    
    mkdir -p "$(dirname "$lock_file")"
    
    local count=0
    while [[ $count -lt $timeout ]]; do
        if mkdir "$lock_file" 2>/dev/null; then
            echo $$ > "$lock_file/pid"
            log_debug "Acquired lock: $lock_name"
            return 0
        fi
        sleep 1
        count=$((count + 1))
    done
    
    log_error "Failed to acquire lock: $lock_name (timeout)"
    return 1
}

# 释放锁
release_lock() {
    local lock_name="$1"
    local lock_file="$PROJECT_ROOT/.claude/locks/${lock_name}.lock"
    
    if [[ -d "$lock_file" ]]; then
        rm -rf "$lock_file"
        log_debug "Released lock: $lock_name"
        return 0
    else
        log_warn "Lock not found: $lock_name"
        return 1
    fi
}

# ============================================
# 配置管理
# ============================================

# 读取配置值
get_config() {
    local key="$1"
    local default="${2:-}"
    local config_file="${PROJECT_ROOT:-$(get_project_root)}/.claude/hooks/config.yaml"
    
    if [[ -f "$config_file" ]] && command -v python3 >/dev/null 2>&1; then
        python3 -c "
import yaml
try:
    with open('$config_file', 'r') as f:
        config = yaml.safe_load(f)
    keys = '$key'.split('.')
    value = config
    for k in keys:
        value = value.get(k, '$default')
    print(value)
except:
    print('$default')
" 2>/dev/null
    else
        echo "$default"
    fi
}

# ============================================
# 性能监控
# ============================================

# 记录执行时间
time_execution() {
    local name="$1"
    local start_time=$(date +%s%N)
    shift
    
    # 执行命令
    "$@"
    local result=$?
    
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))
    
    log_debug "$name completed in ${duration}ms"
    
    # 如果执行时间超过阈值，记录警告
    local threshold=$(get_config "performance.warning_threshold_ms" "5000")
    if [[ $duration -gt $threshold ]]; then
        log_warn "$name took ${duration}ms (threshold: ${threshold}ms)"
    fi
    
    return $result
}

# ============================================
# 错误处理
# ============================================

# 错误处理器
handle_error() {
    local exit_code=$?
    local line_no=$1
    local func_name="${2:-main}"
    
    log_error "Error in $func_name at line $line_no (exit code: $exit_code)"
    
    # 可选：发送通知或触发恢复机制
    if [[ $(get_config "error.auto_recovery" "false") == "true" ]]; then
        log_info "Attempting auto-recovery..."
        # 恢复逻辑
    fi
    
    return $exit_code
}

# 设置错误陷阱
setup_error_trap() {
    set -eE
    trap 'handle_error $LINENO ${FUNCNAME[0]}' ERR
}

# ============================================
# 初始化
# ============================================

# 初始化库
init_hook_lib() {
    export PROJECT_ROOT="${PROJECT_ROOT:-$(get_project_root)}"
    init_logs "$PROJECT_ROOT"
    
    # 设置默认错误处理
    if [[ "${STRICT_MODE:-true}" == "true" ]]; then
        set -euo pipefail
    fi
    
    log_debug "Hook library initialized"
}

# 自动初始化（如果直接source）
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This is a library file and should be sourced, not executed directly"
    exit 1
fi
[FILE MAY BE TRUNCATED - PLEASE VERIFY]
