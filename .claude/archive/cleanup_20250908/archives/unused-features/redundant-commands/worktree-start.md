---
name: worktree-start
description: Create isolated Git worktrees for parallel chapter generation like CCMP
tools:
  - Bash
  - Read
  - Write
  - Task
---

# Novel Worktree Start Command

Create isolated Git worktrees for parallel chapter generation: **$ARGUMENTS** (chapter number or range)

## CCMP Worktree Architecture for Novels

### Revolutionary Parallel Chapter Generation
```bash
# CCMP模式适配到小说创作
主仓库 NOVELSYS-SWARM/
+-- worktree-ch01/          # Agent群体1 创作第1章
+-- worktree-ch02/          # Agent群体2 创作第2章  
+-- worktree-ch03/          # Agent群体3 创作第3章
+-- worktree-integration/   # 最终整合和质量检查

# 12个Agent可以在3个不同章节上并行工作
# 完全隔离，零冲突，最后统一合并
```

### Worktree Creation Protocol
```python
async def create_chapter_worktree(chapter_number):
    """Create isolated worktree for chapter generation"""
    
    worktree_config = {
        "worktree_name": f"worktree-ch{chapter_number:02d}",
        "branch_name": f"chapter-{chapter_number}",
        "base_branch": "main",
        "context_isolation": True,
        "agent_allocation": {
            "primary_agents": 8,      # 核心创作Agent
            "support_agents": 4,      # 质量和优化Agent
            "coordinator": 1          # worktree内协调Agent
        }
    }
    
    # 创建独立工作空间
    worktree_path = f"../novel-ch{chapter_number:02d}/"
    
    commands = [
        f"git worktree add {worktree_path} -b {worktree_config['branch_name']}",
        f"cd {worktree_path}",
        f"cp -r .claude/context/ .claude/context-ch{chapter_number}/",
        f"echo 'CHAPTER_{chapter_number}_WORKSPACE' > .worktree-id"
    ]
    
    # [ENHANCED] 准备章节特定上下文
    chapter_context = await prepare_chapter_context(chapter_number)
    
    # Load entity dictionary and genre for this worktree
    entity_dict_path = ".claude/agents/shared/entity_dictionary.yaml"
    bible = Read(f"data/projects/{project_name}/bible.yaml")
    project_genre = detect_genre_from_bible(bible)
    
    # Copy enhanced context to worktree
    enhanced_context = {
        "entity_dictionary": entity_dict_path,
        "genre": project_genre,
        "quality_threshold": 95,
        "chapter_context": chapter_context
    }
    
    await setup_worktree_context(worktree_path, enhanced_context)
    
    return ChapterWorktreeResult(
        worktree_path=worktree_path,
        branch_name=worktree_config['branch_name'],
        context_ready=True,
        agent_allocation=worktree_config['agent_allocation']
    )
```

## Worktree Agent Coordination

### Independent Agent Ecosystems
```yaml
chapter_01_worktree:
  location: "../novel-ch01/"
  branch: "chapter-1"  
  agents:
    - outline-creator      # 章节结构
    - character-psychologist  # 角色发展
    - scene-painter        # 场景描写
    - dialogue-specialist  # 对话创作
    - emotion-weaver      # 情感编织
    - mystery-architect   # 推理设计
    - quality-coordinator # 内部质量管理
  isolation: "完全独立，不影响其他章节"
  
chapter_02_worktree:  
  location: "../novel-ch02/"
  branch: "chapter-2"
  agents: [同上配置]
  context: "基于ch01的最终状态"
  
integration_worktree:
  location: "../novel-integration/"  
  branch: "integration"
  purpose: "跨章节一致性检查和最终合并"
  agents:
    - consistency-guardian
    - bible-compliance-checker
    - cross-chapter-validator
```

### Context Inheritance Strategy
```python
async def setup_worktree_context(worktree_path, chapter_number):
    """Setup chapter-specific context in worktree"""
    
    context_strategy = {
        "inherit_from_main": [
            "series_bible.yaml",           # 核心Bible不变
            ".claude/context/series-bible.md",
            ".claude/context/character-profiles.md",
            ".claude/context/world-building.md"
        ],
        
        "chapter_specific": [
            f".claude/context/chapter-{chapter_number}-outline.md",
            f".claude/context/chapter-{chapter_number}-progress.md", 
            f".claude/books/current-series/chapters/ch{chapter_number}/"
        ],
        
        "worktree_isolation": [
            # 这些文件在worktree内可以随意修改
            "output/current_chapter.md",
            "temp/agent_outputs/",
            "logs/worktree_generation.log"
        ]
    }
    
    # 复制继承上下文
    for file_pattern in context_strategy["inherit_from_main"]:
        await copy_context_to_worktree(file_pattern, worktree_path)
    
    # 创建章节专用上下文
    await create_chapter_specific_context(worktree_path, chapter_number)
    
    return ContextSetupResult(
        inherited_files=len(context_strategy["inherit_from_main"]),
        chapter_files=len(context_strategy["chapter_specific"]),
        isolation_complete=True
    )
```

## Parallel Execution Benefits

### Zero-Conflict Collaboration
```yaml
traditional_approach:
  problem: "多个Agent修改同一文件  ->  冲突"
  solution: "串行执行，等待前一个完成"
  efficiency: "低效率，浪费并行潜力"

ccmp_worktree_approach:
  innovation: "每章独立文件系统视图"  
  advantage: "完全并行，零冲突可能"
  efficiency: "3-5章同时创作，效率提升500%+"
  
scaling_potential:
  current: "1章节 = 30分钟"
  worktree: "3章节并行 = 35分钟总时间"
  improvement: "从30分钟/章  ->  12分钟/章"
```

### Resource Optimization
```python
async def optimize_worktree_resources():
    """Optimize resource allocation across worktrees"""
    
    resource_allocation = {
        "memory_per_worktree": "2GB",
        "agents_per_worktree": "8-12",
        "max_parallel_worktrees": "3-5",
        "context_window_budget": "分配给每个worktree独立预算"
    }
    
    # 动态负载均衡
    active_worktrees = await get_active_worktrees()
    
    for worktree in active_worktrees:
        workload = await assess_worktree_workload(worktree)
        
        if workload.overloaded:
            # 减少该worktree的并发Agent数
            await reduce_worktree_agents(worktree, target=6)
            
        elif workload.underutilized:
            # 增加Agent数以提升效率
            await increase_worktree_agents(worktree, target=10)
    
    return ResourceOptimizationResult(
        total_worktrees=len(active_worktrees),
        total_agents=sum(w.agent_count for w in active_worktrees),
        optimization_actions=self.optimization_log
    )
```

## Worktree Integration Protocol

### Final Integration Strategy
```bash
# 所有章节完成后，统一集成
/novel:worktree-merge all

# 执行流程：
# 1. 验证所有worktree的质量标准
# 2. 检查跨章节一致性
# 3. 解决潜在冲突
# 4. 合并到主分支
# 5. 清理worktree环境
```

### Integration Quality Gates
```python
async def validate_worktree_integration():
    """Validate all worktrees before integration"""
    
    integration_checks = [
        {
            "check": "individual_quality",
            "requirement": "每个章节质量>=95分",
            "validator": "chapter_quality_validator"
        },
        
        {
            "check": "cross_chapter_consistency", 
            "requirement": "角色行为一致性>=98%",
            "validator": "consistency_guardian"
        },
        
        {
            "check": "narrative_continuity",
            "requirement": "情节连贯性>=95%",
            "validator": "plot_continuity_checker"  
        },
        
        {
            "check": "bible_compliance",
            "requirement": "Bible遵循度=100%",
            "validator": "bible_compliance_enforcer"
        }
    ]
    
    validation_results = []
    
    for check in integration_checks:
        result = await execute_integration_check(check)
        validation_results.append(result)
        
        # 任何检查失败都阻止集成
        if not result.passed:
            return IntegrationValidationResult(
                status="BLOCKED",
                failed_check=check["check"],
                required_fixes=result.required_actions,
                can_proceed=False
            )
    
    return IntegrationValidationResult(
        status="APPROVED",
        all_checks_passed=True,
        integration_ready=True,
        quality_score=calculate_overall_quality(validation_results)
    )
```

## Usage Examples

### Creating Multiple Chapter Worktrees
```bash
# 创建单章节worktree
/novel:worktree-start 1

# 创建多章节并行worktrees  
/novel:worktree-start 1-3

# 检查worktree状态
/novel:worktree-status

# 合并完成的worktrees
/novel:worktree-merge 1,2,3
```

### Advanced Worktree Operations
```bash
# 在特定worktree中工作
cd ../novel-ch01/
/novel:chapter-start 1  # 在隔离环境中生成

# 跨worktree一致性检查
/novel:worktree-sync-check

# 清理完成的worktrees
/novel:worktree-cleanup completed
```

This Git worktree approach enables true parallel novel generation, allowing multiple agent swarms to work on different chapters simultaneously without conflicts, dramatically improving efficiency while maintaining quality.