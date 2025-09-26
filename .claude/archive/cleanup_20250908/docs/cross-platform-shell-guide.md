# Cross-Platform Shell Command Guide

## 问题背景
在Windows系统使用Git Bash时，某些Windows命令会被误解或导致意外行为：
- `dir /B` 中的 `/B` 被解释为路径，可能扫描C盘
- Windows特定命令在Unix-like环境下不可用
- 路径分隔符差异（`\` vs `/`）

## 最佳实践

### 1. 文件列表操作

[ ] **避免使用（Windows特定）：**
```bash
dir /B *.md
dir /B ".claude\commands\novel\*.md" | find /c ".md"
```

[x] **推荐使用（跨平台）：**
```bash
# 列出文件
ls *.md
ls -1 .claude/commands/novel/*.md

# 计数文件
ls -1 .claude/commands/novel/*.md | wc -l

# 或使用 find
find .claude/commands/novel -name "*.md" -type f | wc -l
```

### 2. 路径操作

[ ] **避免：**
```bash
# Windows风格路径
.claude\commands\novel\*.md
{project_root}/
```

[x] **推荐：**
```bash
# Unix风格路径（Git Bash自动转换）
.claude/commands/novel/*.md
/d/NOVELSYS-SWARM/

# 或使用引号处理空格
"D:/NOVELSYS-SWARM/My Documents/"
```

### 3. 文件测试

[x] **跨平台兼容：**
```bash
# 测试文件存在
test -f "file.txt" && echo "exists"
[ -f "file.txt" ] && echo "exists"

# 测试目录存在
test -d "directory" && echo "exists"
[ -d "directory" ] && echo "exists"
```

### 4. 文本搜索

[ ] **避免（Windows）：**
```bash
find "pattern" file.txt
findstr "pattern" file.txt
```

[x] **推荐（跨平台）：**
```bash
grep "pattern" file.txt
# 或使用 ripgrep（更快）
rg "pattern" file.txt
```

### 5. 环境变量

[x] **跨平台：**
```bash
# 设置变量
export VAR="value"

# 使用变量
echo "$VAR"
echo "${VAR}_suffix"
```

### 6. 条件执行

[x] **跨平台：**
```bash
# AND 操作
command1 && command2

# OR 操作
command1 || command2

# 条件判断
if [ condition ]; then
    command
fi
```

### 7. 文件计数示例

**完整的跨平台文件计数方案：**
```bash
# 方法1：使用 ls 和 wc
count=$(ls -1 .claude/commands/novel/*.md 2>/dev/null | wc -l)

# 方法2：使用 find
count=$(find .claude/commands/novel -name "*.md" -type f 2>/dev/null | wc -l)

# 方法3：使用 glob 和数组（Bash特定）
files=(.claude/commands/novel/*.md)
count=${#files[@]}

# 显示结果
echo "Found $count markdown files"
```

### 8. 错误处理

[x] **推荐：**
```bash
# 重定向错误到null
command 2>/dev/null

# 检查命令成功
if command; then
    echo "Success"
else
    echo "Failed"
fi

# 使用退出码
command
if [ $? -eq 0 ]; then
    echo "Success"
fi
```

### 9. 平台检测

**检测运行环境：**
```bash
# 检测操作系统
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Windows (Git Bash/Cygwin)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux"
fi

# 或使用 uname
case "$(uname -s)" in
    MINGW*|CYGWIN*) echo "Windows";;
    Darwin) echo "macOS";;
    Linux) echo "Linux";;
esac
```

### 10. 安全实践

[x] **始终使用：**
```bash
# 引号包裹变量（防止空格问题）
"$variable"
"${array[@]}"

# 使用 -- 分隔选项和参数
grep -- "$pattern" file.txt

# 检查变量是否为空
if [ -z "$var" ]; then
    echo "Variable is empty"
fi
```

## 系统检查命令优化

### 原始问题命令：
```bash
dir /B ".claude\commands\novel\*.md" | find /c ".md"
```

### 修正后的跨平台版本：
```bash
# 选项1：简单计数
ls -1 .claude/commands/novel/*.md 2>/dev/null | wc -l

# 选项2：带验证的计数
if [ -d ".claude/commands/novel" ]; then
    count=$(ls -1 .claude/commands/novel/*.md 2>/dev/null | wc -l)
    echo "Found $count command files"
else
    echo "Commands directory not found"
fi

# 选项3：使用find（更可靠）
find .claude/commands/novel -maxdepth 1 -name "*.md" -type f | wc -l
```

## 总结

1. **优先使用POSIX兼容命令**（ls, grep, find, test）
2. **使用正斜杠路径**（`/`而非`\`）
3. **添加错误处理**（`2>/dev/null`）
4. **测试跨平台兼容性**
5. **避免Windows特定命令**（dir, findstr, etc.）

这样可以确保命令在Windows (Git Bash)、macOS和Linux上都能正常工作。