#!/bin/bash

# Hook System Compatibility Test
# Tests both official Claude Code standards and NOVELSYS-SWARM functionality

echo "🔧 NOVELSYS-SWARM Hook System Compatibility Test"
echo "================================================"

# 设置测试环境
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export CLAUDE_PROJECT_DIR="$PROJECT_ROOT"
export DEBUG_HOOKS="true"
export NOVELSYS_DEBUG="true"

# 测试文件
test_log="$PROJECT_ROOT/.claude/logs/compatibility-test.log"
mkdir -p "$PROJECT_ROOT/.claude/logs"

echo "Starting compatibility test at $(date)" > "$test_log"

# ==================== Test 1: Official Configuration ====================
echo
echo "📋 Test 1: Official Configuration Validation"

settings_file="$PROJECT_ROOT/.claude/settings.json"
if [[ -f "$settings_file" ]]; then
    echo "✅ Official settings.json exists"
    
    # 验证JSON格式
    if jq empty "$settings_file" 2>/dev/null; then
        echo "✅ Valid JSON format"
    else
        echo "❌ Invalid JSON format"
    fi
    
    # 检查必要字段
    schema=$(jq -r '.$schema // empty' "$settings_file" 2>/dev/null)
    if [[ "$schema" == "https://json.schemastore.org/claude-code-settings.json" ]]; then
        echo "✅ Official schema reference present"
    else
        echo "⚠️ Missing official schema reference"
    fi
    
    # 检查hook配置
    post_hooks=$(jq -r '.hooks.PostToolUse | length' "$settings_file" 2>/dev/null)
    if [[ "$post_hooks" -gt 0 ]]; then
        echo "✅ PostToolUse hooks configured ($post_hooks hooks)"
    else
        echo "❌ No PostToolUse hooks found"
    fi
    
    # 检查超时设置
    timeout_set=$(jq -r '.hooks.PostToolUse[0].hooks[0].timeout // empty' "$settings_file" 2>/dev/null)
    if [[ -n "$timeout_set" ]]; then
        echo "✅ Timeout settings configured (${timeout_set}s)"
    else
        echo "⚠️ No timeout settings"
    fi
    
else
    echo "❌ Official settings.json missing"
fi

# ==================== Test 2: Extended Configuration ====================
echo
echo "📋 Test 2: Extended Configuration"

config_file="$PROJECT_ROOT/.claude/hook-config.json"
if [[ -f "$config_file" ]] && jq empty "$config_file" 2>/dev/null; then
    echo "✅ Extended hook-config.json valid"
    
    mode=$(jq -r '.system.mode' "$config_file" 2>/dev/null)
    echo "✅ System mode: $mode"
    
    version=$(jq -r '.system.version' "$config_file" 2>/dev/null)
    echo "✅ System version: $version"
else
    echo "❌ Extended configuration missing or invalid"
fi

# ==================== Test 3: Hook Executable Tests ====================
echo
echo "📋 Test 3: Hook Executable Tests"

hooks_dir="$PROJECT_ROOT/.claude/hooks"
if [[ -d "$hooks_dir" ]]; then
    echo "✅ Hooks directory exists"
    
    # 测试关键hooks
    critical_hooks=("master-hook.sh" "output-validator.sh" "session-tracker.sh" "project-stats-updater.sh")
    
    for hook in "${critical_hooks[@]}"; do
        hook_path="$hooks_dir/$hook"
        if [[ -f "$hook_path" ]]; then
            echo "✅ $hook exists"
            
            # 检查执行权限
            if [[ -x "$hook_path" ]]; then
                echo "  ✅ Executable"
            else
                echo "  ⚠️ Not executable, fixing..."
                chmod +x "$hook_path"
            fi
            
            # 检查shebang
            first_line=$(head -1 "$hook_path")
            if [[ "$first_line" == "#!/bin/bash" ]]; then
                echo "  ✅ Valid shebang"
            else
                echo "  ❌ Invalid shebang: $first_line"
            fi
        else
            echo "❌ $hook missing"
        fi
    done
else
    echo "❌ Hooks directory missing"
fi

# ==================== Test 4: Hook Execution Tests ====================
echo
echo "📋 Test 4: Hook Execution Tests"

# 创建测试输入
test_input='{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/path/content.md",
    "content": "Test content"
  }
}'

echo "Testing master-hook.sh execution..."

# 测试master-hook执行
if [[ -f "$hooks_dir/master-hook.sh" ]]; then
    start_time=$(date '+%s')
    echo "$test_input" | timeout 30 bash "$hooks_dir/master-hook.sh" > /tmp/hook_test_output.log 2>&1
    exit_code=$?
    end_time=$(date '+%s')
    execution_time=$((end_time - start_time))
    
    if [[ $exit_code -eq 0 ]]; then
        echo "✅ master-hook.sh executed successfully (${execution_time}s)"
    else
        echo "❌ master-hook.sh failed with exit code $exit_code"
        echo "Output:"
        cat /tmp/hook_test_output.log | head -10
    fi
else
    echo "❌ master-hook.sh not found for testing"
fi

# ==================== Test 5: Environment Variable Tests ====================
echo
echo "📋 Test 5: Environment Variable Support"

# 测试官方环境变量
if [[ -n "$CLAUDE_PROJECT_DIR" ]]; then
    echo "✅ CLAUDE_PROJECT_DIR set: $CLAUDE_PROJECT_DIR"
else
    echo "⚠️ CLAUDE_PROJECT_DIR not set (using fallback)"
fi

# 测试扩展环境变量
if [[ -n "$NOVELSYS_HOOK_MODE" ]]; then
    echo "✅ NOVELSYS_HOOK_MODE set: $NOVELSYS_HOOK_MODE"
else
    echo "⚠️ NOVELSYS_HOOK_MODE not set (using default)"
fi

# ==================== Test 6: Performance Monitoring ====================
echo
echo "📋 Test 6: Performance Monitoring"

performance_log="$PROJECT_ROOT/.claude/logs/hook-performance.log"
if [[ -f "$performance_log" ]]; then
    echo "✅ Performance logging available"
    recent_entries=$(tail -5 "$performance_log" | wc -l)
    echo "  Recent entries: $recent_entries"
else
    echo "⚠️ No performance log found yet"
fi

# ==================== Test 7: Compatibility Mode Tests ====================
echo
echo "📋 Test 7: Compatibility Mode Tests"

# 模拟官方hook调用
export CLAUDE_HOOK_TIMEOUT="60"
export CLAUDE_HOOK_MATCHER="Write|Edit|MultiEdit"

echo "Testing with official environment variables..."
echo "$test_input" | timeout 10 bash "$hooks_dir/master-hook.sh" > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "✅ Compatible with official hook environment"
else
    echo "❌ Compatibility issues detected"
fi

unset CLAUDE_HOOK_TIMEOUT CLAUDE_HOOK_MATCHER

# ==================== Summary ====================
echo
echo "📋 Compatibility Test Summary"
echo "================================================"

# 检查日志文件
debug_log="$PROJECT_ROOT/.claude/logs/master-hook-debug.log"
if [[ -f "$debug_log" ]]; then
    recent_debug=$(tail -1 "$debug_log")
    echo "✅ Debug logging functional"
    echo "  Latest: $recent_debug"
fi

# 系统状态
echo "✅ Test completed at $(date)"
echo "📄 Full test log: $test_log"
echo "🔧 Debug log: $debug_log"
echo "📊 Performance log: $performance_log"

echo
echo "🎯 Recommendations:"
echo "1. Verify all ✅ items are working correctly"
echo "2. Address any ❌ critical issues"
echo "3. Monitor ⚠️ warnings for potential improvements"
echo "4. Run this test after hook system changes"

echo "Test completed successfully!" >> "$test_log"