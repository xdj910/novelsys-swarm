# 📋 完整修复清单

## 总计：22个命令文件，17个使用Agent，需要修复15个

### [x] 已完成集成 (2个)
1. **context-sync.md** - [x] 完全集成
2. **quality-check-individual.md** - WARNING:️ 部分集成（需小修复）

### [ ] 需要修复的命令 (15个)

#### 🔴 优先级1：内容生成类 (5个)
这些命令会创建新内容，必须使用增强系统避免产生错误：

1. **chapter-start.md** - 生成新章节
   - 需要：entity dictionary, genre awareness, 95+ quality
   
2. **chapter-continue.md** - 续写章节
   - 需要：entity dictionary, genre awareness, 95+ quality
   
3. **parallel-generate.md** - 并行生成
   - 需要：entity dictionary, genre awareness, 修改92 -> 95
   
4. **next.md** - 生成下一段内容
   - 需要：entity dictionary, genre awareness, 95+ quality
   
5. **bible-create.md** - 创建Bible
   - 需要：初始化entity dictionary, 设置genre

#### 🟡 优先级2：质量检查类 (4个)
这些命令检查内容质量，必须理解变体：

6. **smart-fix.md** - 智能修复
   - 需要：entity dictionary避免"修复"正确变体
   
7. **smart-fix-cross.md** - 跨章节修复
   - 需要：entity dictionary理解演变
   
8. **quality-check-cross.md** - 跨章节检查
   - 需要：entity dictionary理解参考演变
   
9. **quality-check-individual.md** - 个别检查（小修复）
   - 需要：修复格式问题，添加entity dict到quality-scorer

#### 🟢 优先级3：项目管理类 (3个)

10. **project-new.md** - 新建项目
    - 需要：初始化entity dictionary和genre standards
    
11. **book-complete.md** - 完成书籍
    - 需要：最终质量检查用enhanced system
    
12. **worktree-start.md** - 开始工作树
    - 需要：加载project的entity dictionary

#### 🔵 优先级4：其他工具类 (3个)

13. **system-test.md** - 系统测试
    - 需要：测试enhanced features
    
14. **standup.md** - 站会报告
    - 需要：报告learning progress
    
15. **smart-defaults.md** - 智能默认值
    - 需要：基于genre设置默认值

### ⚪ 不需要修改 (5个)
这些命令不直接处理内容，不需要entity dictionary：

1. **init.md** - 初始化系统（不涉及具体内容）
2. **project-list.md** - 列出项目（只是列表）
3. **project-switch.md** - 切换项目（只是切换）
4. **github-sync.md** - GitHub同步（只是版本控制）
5. **firewall-mode.md** - 防火墙模式（只是设置）
6. **status.md** - 状态查询（只是查询）

## 📊 修复统计

- **总命令数**: 22个
- **使用Agent的**: 17个
- **已集成**: 2个
- **需要修复**: 15个
- **不需修改**: 5个

## 🎯 修复策略

### 标准修复模板
每个需要修复的命令都应该：

**Command integration specialist:**
1. Load entity dictionary manager:
   - Import EntityDictionaryManager from entity_dictionary_manager
   - Create dict_manager instance for variation handling
2. Detect project characteristics:
   - Call detect_project_genre() to identify project type
   - Store genre for context-aware processing
3. Prepare enhanced context information:
   - Create entity_dict_info with smart variation handling instruction
   - Format genre_context with detected genre and standards
   - Set quality_standard to maintain 95+ score threshold
4. Configure Task for agent execution:
   - Set subagent_type to appropriate agent name
   - Combine task_description with all context information
   - Format complete prompt with entity_dict_info, genre_context, and quality_standard
5. Return properly configured Task object for enhanced processing

### 批量修复顺序
1. **第一批**：5个生成命令（最紧急）
2. **第二批**：4个质量命令
3. **第三批**：3个项目管理
4. **第四批**：3个工具类

## WARNING:️ 风险评估

如果不修复这15个命令：
- 生成命令会创建"错误"内容
- 检查命令会标记假阳性
- 修复命令会破坏好内容
- 系统无法学习和改进

**建议：立即开始修复第一批（生成命令）**