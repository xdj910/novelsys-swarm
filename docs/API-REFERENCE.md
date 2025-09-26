# API 参考文档

> NOVELSYS-SWARM 2.5 完整API文档  
> Version: 2.5.0 | Updated: 2025-01-30

## 📋 目录

- [核心模块](#核心模块)
- [Stream API](#stream-api)
- [Agent API](#agent-api)
- [GitHub集成](#github集成)
- [依赖管理](#依赖管理)
- [配置API](#配置api)

## 🎯 核心模块

### context_firewall

#### AgentResponse

保护主线程的响应封装类。

**AgentResponse specialist:**

**Initialize agent response with context firewall protection:**
1. Accept summary parameter (50 character limit for thread safety)
2. Accept status parameter (success|partial|failed)
3. Accept optional details parameter (full content, not returned to main thread)
4. Accept optional metadata dictionary
5. Store all parameters securely within firewall boundaries

**Get safe summary information:**
1. Retrieve the stored summary
2. Truncate to maximum 50 characters for safety
3. Return the truncated summary string

**Check execution success status:**
1. Compare stored status against 'success' value
2. Return boolean result of comparison

**使用示例：**
**Usage example:**
1. Create AgentResponse with summary "第1章生成完成，质量评分95"
2. Set status to "success"
3. Include full chapter details in details parameter
4. Main thread safely retrieves only the summary via get_summary()
5. Output: "第1章生成完成，质量评分95"

### parallel_coordinator

#### NovelParallelCoordinator

8-Stream并行执行协调器。

**NovelParallelCoordinator specialist:**

**Execute single chapter in parallel streams:**
1. Accept chapter number as integer
2. Accept chapter outline as string
3. Accept bible dictionary with novel settings
4. Accept optional dependencies list of chapter numbers
5. Coordinate 8-Stream parallel execution for the chapter
6. Monitor quality scores across all streams
7. Aggregate results from all processing streams
8. Return dictionary containing:
   - content: Generated chapter content string
   - quality: Quality score as float
   - metadata: Processing metadata dictionary
   - streams: Individual stream results dictionary

**Execute multiple chapters in parallel batch:**
1. Accept chapters list of chapter numbers
2. Accept outlines dictionary mapping chapter numbers to outline strings
3. Accept bible dictionary with novel settings
4. Coordinate parallel execution across multiple chapters simultaneously
5. Manage resource allocation between concurrent chapter generations
6. Return dictionary mapping chapter numbers to their result dictionaries

**使用示例：**
**Usage example:**
1. Create NovelParallelCoordinator instance
2. For single chapter generation:
   - Call execute_chapter with chapter_num=1
   - Provide outline "主角初次觉醒量子意识"
   - Pass novel_bible settings
   - Await parallel stream processing
3. For batch parallel generation:
   - Call execute_parallel with chapters list [1, 2, 3]
   - Provide outlines dictionary mapping each chapter to its outline
   - Pass novel_bible settings
   - Await concurrent processing of all chapters

## 🌊 Stream API

### Stream基类

所有Stream的基础接口。

**BaseStream specialist:**

**Process content with contextual information:**
1. Accept content string as input
2. Accept context dictionary with processing information
3. Apply stream-specific processing logic (must be implemented by subclasses)
4. Return StreamResult object with processing outcomes

**Get stream processing weight:**
1. Retrieve the configured weight value for this stream
2. Return weight as float for coordinator balancing

### 8个核心Stream

**Eight core stream specialists available:**
- CharacterPsychologyStream: Enhances character psychological depth
- NarrativeStructureStream: Manages narrative structure flow
- WorldBuildingStream: Builds sensory world details
- ProseCraftStream: Optimizes prose craft quality
- ContinuityGuardStream: Guards story continuity
- ForeshadowingStream: Manages foreshadowing lifecycle
- DialogueMasterStream: Masters dialogue artistry
- EmotionWeaverStream: Weaves emotional resonance

**Usage example:**
1. Create CharacterPsychologyStream instance
2. Call process method with character dialogue scene content
3. Provide context dictionary with chapter number and character list
4. Await psychological depth enhancement processing
5. Receive enhanced content via StreamResult object

## 🤖 Agent API

### agent_type_mapper

动态Agent类型映射器。

**AgentTypeMapper specialist:**

**Chapter type to agent mapping configuration:**
- action: ['action-choreographer', 'pacing-specialist']
- dialogue: ['dialogue-enhancer', 'subtext-weaver']
- description: ['sensory-detail', 'atmosphere-builder']
- Additional 7 chapter types with corresponding agent assignments

**Get appropriate agents for chapter type:**
1. Accept chapter_type string parameter
2. Accept optional chapter_content for intelligent type detection
3. Look up chapter type in CHAPTER_TYPES mapping
4. Retrieve corresponding agent ID list for that chapter type
5. Return list of agent IDs suitable for processing that chapter type

**Automatically detect chapter type from content:**
1. Accept content string for analysis
2. Analyze content patterns, keywords, and structure
3. Apply intelligent classification algorithms
4. Return detected chapter type as string

**使用示例：**
**Usage example:**
1. Create AgentTypeMapper instance
2. For manual type specification:
   - Call get_agents_for_chapter with 'action' type
   - Receive agent list: ['action-choreographer', 'pacing-specialist', 'tension-maximizer']
3. For automatic detection:
   - Call auto_detect_type with chapter_content
   - Receive detected chapter type
   - Call get_agents_for_chapter with detected type
   - Receive appropriate agent list for that content

## 🔗 GitHub集成

### github_integration

GitHub Issues持久化接口。

**GitHubIntegration specialist:**

**Initialize GitHub integration:**
1. Accept repo_name string parameter
2. Accept optional token string for GitHub authentication
3. Set up GitHub API connection with provided credentials
4. Prepare repository management interface

**Create novel repository:**
1. Accept project_name string for the novel
2. Accept optional description string for repository
3. Create new GitHub repository with specified name
4. Configure repository settings for novel project
5. Return tuple containing:
   - Success boolean flag
   - Repository URL string (if success) or error message string (if failed)

**Synchronize chapter to GitHub issue:**
1. Accept chapter_num integer for chapter identification
2. Accept chapter_data dictionary with chapter content and metadata
3. Create or update GitHub issue for specified chapter
4. Upload chapter data to issue description and comments
5. Return boolean indicating synchronization success

**Retrieve chapter from GitHub issue:**
1. Accept chapter_num integer for chapter identification
2. Locate corresponding GitHub issue for that chapter
3. Parse chapter data from issue content
4. Return dictionary with chapter data or None if not found

**使用示例：**
**Usage example:**
1. Create GitHubIntegration instance with "my-novel" repository name
2. For repository creation:
   - Call create_novel_repo with project name "量子觉醒"
   - Provide description "一部科幻悬疑小说"
   - Receive success flag and repository URL or error message
3. For chapter synchronization:
   - Call sync_chapter_to_issue with chapter number 1
   - Provide chapter_data dictionary with content, quality score 95, and metadata
   - Receive boolean success confirmation
4. For chapter recovery:
   - Call get_chapter_from_issue with chapter number 1
   - Receive chapter dictionary with all stored data

## 📊 依赖管理

### dependency_manager

依赖图管理器。

**DependencyManager specialist:**

**Initialize dependency management system:**
1. Create directed graph using NetworkX for dependency tracking
2. Initialize empty foreshadowings dictionary for story element tracking
3. Set up dependency analysis capabilities

**Add chapter dependency relationship:**
1. Accept source chapter number (the prerequisite)
2. Accept target chapter number (the dependent chapter)
3. Accept dependency type string (plot|character|setting, defaults to 'plot')
4. Add directed edge to dependency graph
5. Store dependency type metadata for analysis

**Add foreshadowing relationship:**
1. Accept name string for the foreshadowing element
2. Accept setup_chapter number where foreshadowing is introduced
3. Accept payoff_chapter number where foreshadowing is resolved
4. Accept optional description string explaining the foreshadowing
5. Store foreshadowing relationship in tracking dictionary

**Calculate optimal execution order:**
1. Accept chapters list of chapter numbers to order
2. Perform topological sort on dependency graph
3. Consider all dependency types and relationships
4. Return ordered list of chapter numbers respecting all dependencies

**Detect circular dependencies:**
1. Analyze dependency graph for cycles
2. Identify any circular dependency chains
3. Return list of dependency cycles (each cycle as list of chapter numbers)

**使用示例：**
**Usage example:**
1. Create DependencyManager instance
2. For adding dependencies:
   - Add plot dependency: chapter 3 depends on chapter 1 plot elements
   - Add character dependency: chapter 3 depends on chapter 2 character development
3. For adding foreshadowing:
   - Create "神秘徽章" foreshadowing
   - Set setup in chapter 1, payoff in chapter 5
   - Describe: "主角在第1章发现的徽章将在第5章揭示真相"
4. For execution ordering:
   - Request order for chapters [1, 2, 3, 4, 5]
   - Receive dependency-sorted order: [1, 2, 3, 4, 5]

## ⚙️ 配置API

### 系统配置

**NovelConfig specialist:**

**Default system configuration values:**
- parallel_workers: 8 (number of parallel processing workers)
- use_firewall: True (enable context firewall protection)
- max_iterations: 3 (maximum quality improvement iterations)
- target_quality: 95 (target quality score threshold)
- auto_sync: False (automatic GitHub synchronization)
- sync_mode: 'incremental' (synchronization strategy)

**Get configuration value:**
1. Accept key string for configuration parameter name
2. Accept optional default value if key not found
3. Look up configuration value in system settings
4. Return configured value or provided default

**Set configuration value:**
1. Accept key string for configuration parameter name
2. Accept value of any type for the configuration
3. Update system configuration with new value
4. Persist configuration change

**Load configuration from file:**
1. Accept path string to configuration file
2. Read configuration file contents
3. Parse configuration format (JSON/YAML)
4. Update system configuration with file values

### 质量配置

**QualityConfig specialist:**

**Quality assessment dimensions configuration:**
- character_depth: weight 1.0, target 95 (character psychological development)
- plot_coherence: weight 1.2, target 99 (story logic consistency)
- prose_quality: weight 0.9, target 95 (writing craft excellence)
- setting_consistency: weight 0.8, target 98 (world-building coherence)
- emotional_resonance: weight 1.1, target 95 (reader emotional connection)
- dialogue_naturalness: weight 1.0, target 95 (conversation authenticity)
- foreshadowing_complete: weight 1.5, target 100 (setup-payoff completion)
- innovation: weight 0.7, target 90 (creative originality)

## 🔧 工具函数

### 增量同步

**IncrementalSync specialist:**

**Calculate content differences:**
1. Accept old_content string as baseline
2. Accept new_content string as updated version
3. Perform line-by-line and character-level difference analysis
4. Calculate change statistics and modification patterns
5. Return dictionary containing difference metrics and change details

**Determine optimal sync mode:**
1. Accept diff_size integer representing change magnitude
2. Analyze change size against predefined thresholds
3. Evaluate efficiency of different sync strategies
4. Return sync mode string: 'patch' (small changes), 'incremental' (medium changes), or 'full' (large changes)

**Create content patch:**
1. Accept old string as original content
2. Accept new string as updated content
3. Generate minimal patch representation of changes
4. Create unified diff format patch
5. Return patch string for efficient content updates

### 执行状态

**ExecutionStatus specialist:**

**Initialize execution tracking:**
1. Create empty statuses dictionary for task status storage
2. Create empty start_times dictionary for timing tracking
3. Prepare status monitoring infrastructure

**Update task execution status:**
1. Accept task_id string for task identification
2. Accept status string indicating current state
3. Accept optional progress float (0.0-1.0) for completion percentage
4. Accept optional message string for status details
5. Update statuses dictionary with new information
6. Record timestamp for status change

**Get execution status summary:**
1. Aggregate all current task statuses
2. Calculate overall progress metrics
3. Compile timing information and duration statistics
4. Return dictionary containing comprehensive status overview

**Export status to JSON format:**
1. Serialize all status and timing information
2. Format data as JSON string
3. Include timestamps and progress details
4. Return JSON string suitable for logging or API responses

## 📝 返回值规范

### 成功响应

**Success response format:**
- success: True (operation completed successfully)
- data: Dictionary containing specific operation results
- metadata: Dictionary containing:
  - timestamp: ISO format timestamp string
  - duration: Processing duration in seconds
  - version: System version string

### 错误响应

**Error response format:**
- success: False (operation failed)
- error: Dictionary containing:
  - code: Error code string (e.g., 'DEPENDENCY_CYCLE')
  - message: Human-readable error description
  - details: Dictionary with specific error information (e.g., cycle path)
- metadata: Dictionary containing:
  - timestamp: ISO format timestamp string

## 🔍 错误代码

| 代码 | 说明 | 处理建议 |
|-----|------|---------|
| DEPENDENCY_CYCLE | 循环依赖 | 移除部分依赖 |
| GITHUB_AUTH_FAILED | GitHub认证失败 | 运行gh auth login |
| QUALITY_TOO_LOW | 质量不达标 | 增加迭代次数 |
| PARALLEL_LIMIT | 并行数超限 | 减少并行任务 |
| FIREWALL_BLOCKED | 内容被防火墙拦截 | 检查内容长度 |

---

*完整示例代码请查看 `examples/` 目录*  
*最后更新: 2025-01-30*