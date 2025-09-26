---
name: quality-check
description: DEPRECATED - Use quality-check-individual and quality-check-cross instead
tools:
  - Read
  - Task
  - TodoWrite
  - Glob
---

# Quality Check Command [DEPRECATED]

WARNING:️ **THIS COMMAND IS DEPRECATED**

This command has been replaced by a cleaner two-phase approach:

1. **`/novel:quality-check-individual [chapters]`** - Phase 1: Check individual chapter quality
2. **`/novel:quality-check-cross [chapters]`** - Phase 2: Check cross-chapter relationships

**Why deprecated?**
- Mixed single-chapter and cross-chapter checks without clear separation
- Inefficient: Could run cross-chapter analysis on broken chapters
- Confusing: Users didn't know which phase was running
- Used outdated agent assignments (conflict-resolver for Bible checks)

**Migration guide:**
```bash
# Old way (deprecated):
/novel:quality-check 5

# New way (recommended):
/novel:quality-check-individual 5    # First: fix individual chapter
/novel:quality-check-cross 1-5       # Then: verify cross-chapter flow
```

---

## Legacy Implementation (Archived)

Run comprehensive quality validation for: **$ARGUMENTS** (chapter number or 'all')

## Validation Framework

### CCMP-Style Quality Gates
Execute 5-stage progressive validation:

**Stage 1: Foundation Check (80% threshold)**
- Bible compliance verification
- Character consistency validation  
- Basic plot coherence check
- World-building alignment

**Stage 2: Content Quality (85% threshold)**
- Writing quality assessment
- Dialogue naturalness evaluation
- Scene description effectiveness
- Pacing appropriateness

**Stage 3: Integration Quality (90% threshold)**
- Cross-chapter consistency
- Character development continuity
- Plot thread coherence
- Mystery element progression

**Stage 4: Excellence Quality (95% threshold)**
- Emotional impact assessment
- Atmospheric effectiveness
- Cultural authenticity
- Reader engagement prediction

**Stage 5: Mastery Quality (98% threshold)**
- Literary merit evaluation
- Innovation and creativity
- Memorable moment identification
- Long-term series impact

## Quality Validation Implementation

### Primary Validation Agents

**Step 1: Consistency Validation**

**Continuity Guard specialist:**
1. Read chapter content from .claude/data/projects/[project]/chapters/ch{chapter_num:03d}/content.md using Read tool
2. Analyze timeline continuity:
   - Verify dates, times, and event sequence consistency
   - Check logical chain integrity (cause-effect relationships, motivation reasonability)
   - Validate detail coherence (character positions, object states, environment descriptions)
3. Generate detailed consistency report marking all inconsistencies found
4. Return comprehensive validation results with specific locations of issues

**Step 2: Plot Hole Detection**

**Plot Hole Detector specialist:**
1. Read chapter content from .claude/data/projects/[project]/chapters/ch{chapter_num:03d}/content.md using Read tool
2. Identify plot integrity issues:
   - Logic flaws (unreasonable plot developments)
   - Causal chain breaks (mismatched causes and effects)
   - Information gaps (missing critical information)
   - Convenience problems (overly coincidental solutions)
3. Provide specific location and modification suggestions for each identified issue
4. Return detailed plot hole analysis with actionable recommendations

**Step 3: Bible Compliance Check**

**Conflict Resolver specialist:**
1. Read chapter content from .claude/data/projects/[project]/chapters/ch{chapter_num:03d}/content.md using Read tool
2. Read Bible file from .claude/data/projects/[project]/bible.yaml using Read tool
3. Cross-validate compliance across key aspects:
   - Character personality alignment with Bible definitions
   - World-building setting consistency
   - Magic/technology rule violations
   - Timeline accuracy
   - Geographic location correctness
4. Generate comprehensive compliance report including:
   - Overall compliance percentage
   - Specific violation items list
   - Severity level for each violation
   - Modification recommendations
5. Return detailed Bible compliance assessment based on actual file content

**Step 4: Overall Quality Scoring**

**Quality Scorer specialist:**
1. Read chapter content from .claude/data/projects/[project]/chapters/ch{chapter_num:03d}/content.md using Read tool
2. Read Bible file from .claude/data/projects/[project]/bible.yaml as scoring reference using Read tool
3. Evaluate multiple quality dimensions (0-100 scale):
   - Character depth and development
   - Plot coherence
   - Writing quality
   - Emotional impact
   - Consistency
   - Bible compliance
   - Cultural authenticity
   - Mystery fairness
   - Atmosphere creation
   - Pacing control
4. Calculate weighted average score with detailed scoring rationale
5. Return comprehensive quality assessment with dimension-specific scores and justifications

### Agent职责分配

| Agent名称 | 实际Agent | 主要职责 |
|----------|----------|---------|
| 一致性检查 | continuity-guard-specialist | 时间线、逻辑链、细节连贯性 |
| 漏洞检测 | plot-hole-detector | 情节漏洞、因果断裂、信息缺失 |
| Bible合规 | conflict-resolver | Bible设定验证、规则冲突检测 |
| 综合评分 | quality-scorer | 多维度质量评分、总体评估 |

## Quality Scoring System

### Dimensional Scores (0-100)
```yaml
Quality_Dimensions:
  character_depth: 90+
  plot_coherence: 95+
  writing_quality: 90+
  emotional_impact: 85+
  consistency: 98+
  bible_compliance: 100
  cultural_authenticity: 90+
  mystery_fairness: 95+
  atmosphere: 85+
  pacing: 88+
```

### Composite Scoring
- **Weighted Average**: Based on dimension importance
- **Minimum Thresholds**: All dimensions must meet minimum
- **Excellence Bonus**: Exceptional dimensions boost overall score
- **Penalty System**: Critical failures reduce overall score

## Validation Cycles

### 30-Minute Quality Cycles
**Cycle 1 (0-30min): Foundation Validation**
- Run consistency-guardian and bible-compliance-checker
- Identify critical issues requiring immediate attention
- Generate fix priority list

**Cycle 2 (30-60min): Content Assessment**  
- Execute quality-scorer comprehensive analysis
- Run plot-hole-detector for logic verification
- Cross-validate findings between agents

**Cycle 3 (60-90min): Specialized Analysis**
- Launch emotional-impact-analyzer and cultural-authenticity-validator
- Execute mystery-fairness-evaluator for genre-specific checks
- Integrate all assessment results

**Cycle 4 (90-120min): Integration & Reporting**
- Consolidate all validator outputs
- Generate comprehensive quality report
- Provide specific improvement recommendations

## Output Reports

### Executive Summary
- Overall Quality Score: [0-100]
- Gate Compliance: [Stage level achieved]
- Critical Issues: [Count and severity]
- Recommendation Priority: [High/Medium/Low items]

### Detailed Analysis
```yaml
Dimensional_Breakdown:
  character_depth:
    score: 92
    strengths: ["Rich internal monologue", "Consistent behavior"]
    improvements: ["Deepen secondary character motivation"]
    
  plot_coherence:
    score: 89
    strengths: ["Logical progression", "Clear causality"]
    improvements: ["Strengthen middle act tension"]
```

### Agent-Specific Reports
- **consistency-guardian**: Consistency violations and fixes
- **plot-hole-detector**: Logic gaps and resolution suggestions  
- **quality-scorer**: Comprehensive scoring rationale
- **bible-compliance-checker**: Compliance status and corrections

### Action Plan
1. **Critical Fixes** (must address immediately)
2. **Quality Improvements** (should address before publication)
3. **Enhancement Opportunities** (nice-to-have improvements)
4. **Long-term Recommendations** (series-level suggestions)

## Context Integration

### Learning Integration
- Update agent memories with quality patterns
- Record successful techniques for replication
- Note common failure modes for avoidance
- Build predictive quality models

### Bible Updates
- Suggest Bible refinements based on quality findings
- Update quality standards based on achievements
- Refine agent parameters for better performance

Execute comprehensive quality validation with full CCMP rigor and agent coordination.