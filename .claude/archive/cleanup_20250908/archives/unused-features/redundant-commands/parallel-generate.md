---
name: parallel-generate  
description: Generate chapters using 8-Stream parallel architecture
tools:
  - Task
  - Read  
  - Write
  - Bash
---

# Parallel Generate Command

Execute 8-Stream parallel chapter generation: **$ARGUMENTS** (chapter numbers or range)

## v2.5 Parallel Architecture

### 8-Stream Coordination
Execute all 8 streams simultaneously for maximum efficiency:

```yaml
stream_architecture:
  core_streams:
    - S1: Character Psychology Specialist
    - S2: Narrative Structure Specialist  
    - S3: World Building Specialist
    - S4: Prose Craft Specialist
  enhanced_streams:
    - S5: Continuity Guard Specialist
    - S6: Foreshadowing Specialist
    - S7: Dialogue Master Specialist
    - S8: Emotion Weaver Specialist
```

## Execution Modes

### Single Chapter (default)
```bash
# Generate single chapter with all 8 streams
/novel:parallel-generate 5

# Full parallel execution
- Launch 8 Stream agents simultaneously  
- Coordinate results through Parallel Coordinator
- Apply Context Firewall for clean output
- Auto-sync to GitHub Issue
```

### Multiple Chapters
```bash
# Generate multiple chapters in sequence
/novel:parallel-generate 3,4,5

# Chapter dependency handling
- Check foreshadowing dependencies
- Respect plot dependencies
- Execute in dependency order
- Parallel streams within each chapter
```

### Chapter Range
```bash
# Generate chapter range
/novel:parallel-generate 10-15

# Batch processing
- Process 6 chapters sequentially
- 8-stream parallel within each
- Progress tracking and reporting
- Error recovery per chapter
```

## Dynamic Agent Allocation

### Chapter Type Detection
```python
chapter_types = {
    "action": ["action-choreographer", "pacing-specialist"],
    "romance": ["romance-specialist", "emotion-amplifier"],
    "mystery": ["mystery-architect", "clue-tracker"],
    "dialogue": ["conversation-architect", "subtext-master"],
    "climax": ["climax-orchestrator", "tension-maximizer"]
}

def allocate_agents(chapter_outline):
    # Base 8 streams (always active)
    agents = BASE_8_STREAMS.copy()
    
    # Detect chapter type from outline
    chapter_type = detect_chapter_type(chapter_outline)
    
    # Add specialized agents
    if chapter_type in chapter_types:
        agents.extend(chapter_types[chapter_type])
    
    return agents  # Total: 8-15 agents
```

### Agent Coordination
```yaml
coordination_flow:
  1. analyze_chapter_requirements
  2. allocate_base_8_streams  
  3. detect_chapter_type
  4. add_specialized_agents
  5. execute_parallel_streams
  6. coordinate_results
  7. apply_context_firewall
  8. generate_summary_output
```

## Stream Execution Flow

### Phase 1: Initialization
```yaml
initialization:
  - Load Bible and context
  - Parse chapter outline
  - Detect dependencies
  - Allocate stream agents
  - Set quality targets
  - [ENHANCED] Load Entity Dictionary (.claude/agents/shared/entity_dictionary.yaml)
  - [ENHANCED] Detect project genre for context-aware generation
  - [ENHANCED] Initialize 95+ quality requirement
```

### Phase 2: Parallel Execution  
```yaml
parallel_execution:
  - Launch 8+ streams simultaneously
  - Monitor progress in real-time
  - Handle stream conflicts
  - Apply timeout protection
  - Collect intermediate results
```

### Phase 3: Coordination
```yaml
coordination:
  - Merge stream outputs
  - Resolve conflicts
  - Apply consistency checks
  - Run quality validation
  - Generate unified chapter
```

### Phase 4: Finalization
```yaml
finalization:
  - Apply Context Firewall
  - Generate 50-char summary
  - Save full content to files
  - Sync to GitHub Issue
  - Update project state
```

## Quality Control

### Stream Quality Targets
```yaml
quality_targets:
  S1_character: 95      # Character Psychology
  S2_narrative: 92      # Narrative Structure  
  S3_world: 93          # World Building
  S4_prose: 91          # Prose Craft
  S5_continuity: 99     # Continuity Guard
  S6_foreshadowing: 100 # Foreshadowing
  S7_dialogue: 94       # Dialogue Master
  S8_emotion: 90        # Emotion Weaver
  
overall_target: 95      # Minimum chapter quality for learning eligibility
```

### Iterative Improvement
```yaml  
iteration_strategy:
  first_pass: 85-87     # Base generation
  second_pass: 90-92    # Issue resolution
  third_pass: 95-98     # Polish and perfect
  
max_iterations: 3
quality_threshold: 95    # [ENHANCED] Raised to match learning requirement
```

### Protected Output
```python
def execute_with_firewall(chapter_num, outline, bible, entity_dict_path, genre):
    # [ENHANCED] Execute 8-stream parallel generation with context
    full_results = Task(
        subagent_type="novel-parallel-coordinator",
        prompt=f"Generate chapter {chapter_num} using 8-stream parallel architecture. "
               f"Bible: {bible}, Outline: {outline} "
               f"Entity Dictionary: {entity_dict_path} for consistent naming. "
               f"Genre: {genre} - apply appropriate conventions. "
               f"Quality requirement: 95+ for learning eligibility.",
        description=f"Generate chapter {chapter_num}"
    )
    
    # Apply Context Firewall
    summary = context_firewall.filter(full_results)
    
    # Save detailed results to files
    save_detailed_results(chapter_num, full_results)
    
    # Return only summary to main thread
    return summary  # "第X章完成 质量Y分 包含Z个场景"
```

## Error Handling

### Stream Failure Recovery
```yaml
failure_handling:
  - Individual stream timeout: 5min
  - Failed stream retry: 2 attempts
  - Partial failure: Continue with successful streams
  - Total failure: Restart with reduced complexity
```

### Dependency Conflicts
```yaml
conflict_resolution:
  - Priority matrix for stream conflicts
  - Continuity Guard has highest priority
  - Character consistency second priority
  - Narrative flow third priority
```

## Usage Examples

### Basic Generation
```bash
# Generate chapter 7 with full 8-stream parallel
/novel:parallel-generate 7

# Expected output (via Context Firewall):
# "第7章完成 质量93分 动作场景 新伏笔2个"
```

### Advanced Generation
```bash
# Generate with specific quality target
/novel:parallel-generate 12 --quality=95

# Generate with custom agent allocation
/novel:parallel-generate 8 --type=climax --agents=12
```

### Batch Processing
```bash
# Generate multiple chapters with progress
/novel:parallel-generate 15-20 --progress --parallel-chapters=2

# Expected output:
# "批量生成: 6章 平均质量94分 总时间18分钟"
```

## Integration Points

### GitHub Sync
Automatic sync after successful generation:
```python
if generation_result.quality >= quality_threshold:
    github_sync(chapter_num, mode="incremental")
```

### Dependency Manager
Respect plot and foreshadowing dependencies:
```python
execution_order = dependency_manager.get_execution_order(chapters)
for chapter in execution_order:
    parallel_generate(chapter)
```

---

**Parallel Generate Command** - v2.5核心功能  
*8-Stream并行架构 + Context Firewall + 动态Agent分配*