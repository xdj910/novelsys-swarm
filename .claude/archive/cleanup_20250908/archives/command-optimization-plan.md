# 命令系统优化方案

## 当前问题分析
1. 命令名称过长（parallel-quality-check）
2. 功能重复（quality-check vs parallel-quality-check）
3. 缺少章节完成后的智能提示
4. 用户需要记忆太多命令

## 核心命令简化方案

### 生成类命令（4个）
```yaml
/novel:ch N          # 开始第N章生成 (原chapter-start)
/novel:cont          # 继续当前章节 (原chapter-continue) 
/novel:bible         # 创建/更新Bible (原bible-create)
/novel:done          # 完成整书 (原book-complete)
```

### 质量检查命令（3个）
```yaml
/novel:fix [chapters]    # 单章节检查+修复 (新设计，原phase1)
/novel:review [chapters] # 跨章节整体检查 (新设计，原phase2)  
/novel:check [chapters]  # 智能检查（自动判断用fix还是review）
```

### 项目管理命令（5个）
```yaml
/novel:new NAME      # 创建新项目 (原project-new)
/novel:switch NAME   # 切换项目 (原project-switch)
/novel:list          # 项目列表 (原project-list)
/novel:st            # 项目状态 (原status)
/novel:next          # 智能下一步建议 (已存在，需增强)
```

## 归档命令列表（8个）

移至 `.claude/commands/archived/`:
- system-test.md  ->  开发调试用
- worktree-start.md  ->  高级功能，很少使用  
- context-sync.md  ->  自动化，无需手动触发
- firewall-mode.md  ->  默认启用
- github-sync.md  ->  自动化
- smart-defaults.md  ->  设置类，不常用
- standup.md  ->  项目管理，可选
- parallel-generate.md  ->  与chapter-start功能重复

## 智能提示增强

### 章节完成后自动提示
```python
# 在chapter-start命令末尾添加
def suggest_next_action(chapter_num, generation_result):
    if generation_result.success:
        print(f"[x] Chapter {chapter_num} generated successfully!")
        print(f"")
        print(f"🤖 Next suggested actions:")
        print(f"  /novel:fix {chapter_num}     # Check and fix this chapter")
        print(f"  /novel:ch {chapter_num + 1}  # Start next chapter")  
        print(f"  /novel:next                  # Get intelligent recommendations")
    else:
        print(f"[ ] Chapter {chapter_num} generation had issues.")
        print(f"")
        print(f"🤖 Recommended action:")
        print(f"  /novel:cont                  # Continue/retry this chapter")
```

### 质量检查后智能提示  
```python
def suggest_after_quality_check(phase, results):
    if phase == "fix" and results.all_passed:
        print("🤖 All chapters passed individual checks!")
        print("  /novel:review all           # Run cross-chapter validation")
        
    elif phase == "review" and results.all_passed:
        print("🤖 All quality checks passed!")
        print("  /novel:next                 # See what to work on next")
        
    elif results.has_failures:
        failed_chapters = results.get_failed_chapters()
        print(f"🤖 Some chapters need fixes:")
        print(f"  /novel:fix {','.join(failed_chapters)}  # Fix specific chapters")
```

## 实施优先级

### 高优先级（立即实施）
1. 创建简化命令的软链接/别名
2. 增强chapter-start的完成提示
3. 分离quality-check为fix和review命令

### 中优先级（本周内）
4. 归档不常用命令
5. 更新文档和帮助信息
6. 增强/novel:next的智能程度

### 低优先级（有时间再做）
7. 命令自动完成功能
8. 使用统计和智能推荐优化