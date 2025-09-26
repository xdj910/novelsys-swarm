# NOVELSYS-SWARM 完整系统流程图

## 系统架构总览

```mermaid
graph TB
    subgraph "Command Layer (22个命令)"
        CMD[Commands<br/>纯委托,无业务逻辑]
    end
    
    subgraph "Coordinator Layer (17个协调器)"
        COORD[Coordinators<br/>业务编排与协调]
    end
    
    subgraph "Agent Layer (70个代理)"
        AGENT[Agents<br/>具体任务执行]
    end
    
    subgraph "Data Layer (文件系统)"
        DATA[File System<br/>带缓存和锁机制]
    end
    
    CMD -->|调用Task工具| COORD
    COORD -->|协调多个| AGENT
    AGENT -->|读写操作| DATA
    
    style CMD fill:#e1f5fe
    style COORD fill:#fff3e0
    style AGENT fill:#f3e5f5
    style DATA fill:#e8f5e9
```

## 核心流程详解

### 1. 章节生成流程 (复杂度: 8.7/10)

```mermaid
graph LR
    subgraph "命令层"
        CS[chapter-start]
    end
    
    subgraph "协调器层"
        CSC[chapter-start-coordinator]
        DIR[director]
    end
    
    subgraph "12步增强管道"
        EV[1.entity-validator<br/>实体验证]
        OG[2.outline-generator<br/>大纲生成]
        SG[3.scene-generator<br/>场景生成]
        CP[4.character-psychology<br/>角色深化]
        DM[5.dialogue-master<br/>对话优化]
        WB[6.world-building<br/>世界构建]
        CLP[7.clue-planter<br/>线索植入]
        CG[8.continuity-guard<br/>连续性检查]
        PC[9.prose-craft<br/>文笔润色]
        EW[10.emotion-weaver<br/>情感编织]
        CR[11.conflict-resolver<br/>冲突解决]
        QS[12.quality-scorer<br/>质量评分]
    end
    
    subgraph "数据层"
        BIBLE[(Bible缓存)]
        ENTITY[(实体字典<br/>带文件锁)]
        CHAPTER[(章节文件)]
        QUALITY[(质量报告)]
    end
    
    CS -->|委托| CSC
    CSC -->|协调| DIR
    DIR -->|顺序执行| EV
    EV -->|验证| ENTITY
    EV --> OG
    OG --> SG
    SG --> CP
    CP --> DM
    DM --> WB
    WB --> CLP
    CLP --> CG
    CG --> PC
    PC --> EW
    EW --> CR
    CR --> QS
    QS -->|<95分重试| DIR
    QS -->|≥95分| CHAPTER
    
    BIBLE -.->|读取| EV
    BIBLE -.->|验证| CG
    ENTITY -.->|锁定更新| CSC
    
    style CS fill:#e3f2fd
    style CSC fill:#fff9c4
    style QS fill:#ffccbc
```

### 2. 质量检查流程 (完全并行化)

```mermaid
graph TB
    subgraph "命令"
        QCI[quality-check-individual]
    end
    
    subgraph "协调器"
        QCIC[quality-check-individual-coordinator]
    end
    
    subgraph "5个并行验证器"
        BCV[bible-compliance-validator<br/>Bible合规性]
        CVC[character-voice-cross-validator<br/>角色声音一致性]
        CFV[cross-chapter-flow-validator<br/>跨章节流畅性]
        PA[pacing-analyzer<br/>节奏分析]
        PHD[plot-hole-detector<br/>情节漏洞检测]
    end
    
    subgraph "聚合"
        AGG[质量聚合器<br/>多维度评分]
    end
    
    QCI -->|委托| QCIC
    QCIC -->|并行执行| BCV
    QCIC -->|并行执行| CVC
    QCIC -->|并行执行| CFV
    QCIC -->|并行执行| PA
    QCIC -->|并行执行| PHD
    
    BCV -->|分数| AGG
    CVC -->|分数| AGG
    CFV -->|分数| AGG
    PA -->|分数| AGG
    PHD -->|分数| AGG
    
    AGG -->|综合评分| REPORT[质量报告<br/>≥95分通过]
    
    style QCI fill:#e1f5fe
    style QCIC fill:#fff3e0
    style AGG fill:#c8e6c9
```

### 3. 系统健康检查流程 (5阶段15代理)

```mermaid
graph TB
    subgraph "Phase 0: 初始化"
        INIT[生成时间戳<br/>创建报告目录]
    end
    
    subgraph "Phase 1: 构建共享上下文"
        CB[context-builder<br/>一次扫描所有文件<br/>生成context.json]
    end
    
    subgraph "Phase 2: 基础分析 (6并行)"
        DM[dependency-mapper]
        CV[consistency-validator]
        FA[filesystem-auditor]
        CI[context-inspector]
        CC[compliance-checker]
        RA[resource-analyzer]
    end
    
    subgraph "Phase 3: 流程分析 (2并行)"
        CFM[command-flow-mapper]
        FDG[flow-diagram-generator]
    end
    
    subgraph "Phase 4: 安全分析"
        FDT[file-dependency-tracer]
        CLA[conditional-logic-analyzer]
        PSV[parallel-safety-validator<br/>带缓解检查]
    end
    
    subgraph "Phase 5: 合规分析 (3并行)"
        CCE1[claude-code-expert<br/>命令合规]
        CCE2[claude-code-expert<br/>代理合规]
        CCE3[claude-code-expert<br/>架构合规]
    end
    
    subgraph "Phase 6: 最终评估"
        NQPA[novel-quality-process-auditor<br/>小说能力评估]
        SHR[system-health-reporter<br/>生成最终报告]
    end
    
    INIT --> CB
    CB -->|context.json| DM
    CB -->|context.json| CV
    CB -->|context.json| FA
    CB -->|context.json| CI
    CB -->|context.json| CC
    CB -->|context.json| RA
    
    DM --> CFM
    CV --> CFM
    FA --> CFM
    CI --> CFM
    CC --> CFM
    RA --> CFM
    
    CFM --> FDG
    FDG --> FDT
    FDG --> CLA
    FDT --> PSV
    CLA --> PSV
    
    PSV --> CCE1
    PSV --> CCE2
    PSV --> CCE3
    
    CCE1 --> NQPA
    CCE2 --> NQPA
    CCE3 --> NQPA
    
    NQPA --> SHR
    SHR --> FINAL[系统健康报告<br/>89/100分]
    
    style CB fill:#ffeb3b
    style PSV fill:#ff9800
    style SHR fill:#4caf50
```

### 4. 数据流与优化

```mermaid
graph LR
    subgraph "Bible缓存流 (30-50%提速)"
        B1[bible.yaml]
        B2[bible-cache-manager]
        B3[cached_bible.json]
        B4[所有validators]
        
        B1 -->|首次读取| B2
        B2 -->|生成缓存| B3
        B3 -->|快速访问| B4
        B2 -.->|哈希验证| B1
    end
    
    subgraph "实体字典流 (带锁保护)"
        E1[entity_dictionary.yaml]
        E2[.lock文件<br/>60秒超时]
        E3[entity-validator]
        E4[entity-dictionary-updater]
        
        E3 -->|读取验证| E1
        E4 -->|获取锁| E2
        E2 -->|原子写入| E1
        E2 -->|释放锁| E2
    end
    
    subgraph "共享上下文 (80-95% I/O减少)"
        C1[全系统文件]
        C2[context-builder<br/>一次扫描]
        C3[context.json]
        C4[13个分析agents]
        
        C1 -->|2.3秒扫描| C2
        C2 -->|生成| C3
        C3 -->|复用| C4
    end
    
    style B3 fill:#e1f5fe
    style E2 fill:#ffccbc
    style C3 fill:#c8e6c9
```

### 5. 并发控制矩阵

```mermaid
graph TB
    subgraph "互斥组合 (不能并行)"
        M1[chapter-start + next-chapter<br/>章节编号竞争]
        M2[project-switch + 任何命令<br/>状态切换冲突]
        M3[context-sync + unified-update<br/>文件写入冲突]
    end
    
    subgraph "需要协调 (带锁保护)"
        C1[chapter-start + unified-update<br/>实体字典锁]
        C2[smart-fix + smart-fix-cross<br/>章节锁]
    end
    
    subgraph "安全并行 (可同时执行)"
        S1[所有只读命令<br/>status, bible-view, project-list]
        S2[系统分析命令<br/>flow-mapping, system-check]
        S3[不同项目的操作]
    end
    
    style M1 fill:#ffcdd2
    style C1 fill:#fff9c4
    style S1 fill:#c8e6c9
```

## 关键性能指标

| 指标 | 值 | 说明 |
|------|-----|------|
| **架构合规度** | 96/100 | Claude Code完美实现 |
| **并行安全分** | 72/100 | 从31分大幅提升 |
| **I/O减少** | 80-95% | 通过共享上下文 |
| **Bible缓存提速** | 30-50% | 验证速度提升 |
| **质量检查加速** | 4x | 并行执行 |
| **章节生成时间** | 3-5分钟 | 12步管道 |
| **系统检查时间** | 5-10分钟 | 15个代理 |
| **生产就绪度** | 89/100 | A-级别 |

## 执行时间估算

- **简单命令** (<1秒): bible-view, status, project-list
- **中等命令** (10-30秒): bible-create, entity-update
- **复杂命令** (1-2分钟): quality-check, unified-update
- **重型命令** (3-5分钟): chapter-start, next-chapter
- **系统命令** (5-10分钟): system-check

## 数据存储结构

```
.claude/
├── data/
│   ├── projects/{project}/
│   │   ├── book_{N}/
│   │   │   ├── bible.yaml
│   │   │   ├── chapters/
│   │   │   │   └── ch{NNN}/
│   │   │   │       ├── content.md
│   │   │   │       └── quality_report.json
│   │   │   └── bible_cache.json
│   │   └── shared/
│   │       ├── entity_dictionary.yaml
│   │       └── .entity_dictionary.lock
│   └── context/
│       ├── {agent}_context.json
│       └── bible_cache_{project}_book{N}.json
└── report/
    └── YYYYMMDD_HHMMSS/
        ├── context.json
        ├── *_report.json (15个)
        └── system_health_report.md
```

---

*基于2025-09-09 v4.0系统健康报告生成*