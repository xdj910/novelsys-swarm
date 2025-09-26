# AI Realist Article Production System
*Complete documentation for AI Realist article series*

## Overview
AI Realist is a 2000-word article series providing skeptical B2B AI analysis for decision makers. This document contains the complete workflow, structure, and guidelines.

## Core Principle
**One article at a time** - No bulk planning, focus on current piece

## New Timestamp-Based Structure

### Article Creation
When starting a new AI Realist article:
```
System generates: content/20250118_143022_topic_slug/
                  └── metadata.json (initialized)
```

### Complete Article Directory
```
.claude/data/articles/ai_realist/
├── strategy/                          # Shared across all articles
│   ├── strategy_v1.1.md
│   └── voice_guide.md
│
└── content/                           # All articles here
    └── 20250118_143022_ai_risks/     # Timestamp_slug format
        ├── metadata.json              # Article tracking
        ├── research/                  # This article's research
        │   ├── trends.md
        │   ├── audience_notes.md
        │   └── competitor_analysis.md
        ├── drafts/                    # Version history
        │   ├── v1_draft.md
        │   ├── v2_draft.md
        │   └── final.md              # Approved version
        ├── reports/                   # Quality check reports
        │   ├── fact_check_report.md  # Fact verification results
        │   ├── quality_score_report.md # Quality assessment
        │   ├── revision_log.json     # Revision history
        │   └── final_approval.md     # Approval documentation
        ├── visuals/                   # Visual production
        │   ├── visual_production_guide.md
        │   ├── prompts.txt
        │   └── images/               # Generated images
        └── published/                 # Platform versions
            ├── medium.md
            ├── beehiiv.md
            ├── substack.md
            └── elevenreader.md
```

## Updated Pipeline

### PROCESS (Single Article Pipeline)

```
1. Article Initiation
   User: Start AI Realist article on [topic]
   System: Creates content/20250118_143022_topic_slug/
           Initializes metadata.json
           Updates registry/production_status.json

2. Research Phase
   Agents write to: {timestamp}/research/
   - trend-analyzer → trends.md
   - audience-profiler → audience_notes.md
   - competitor-scanner → competitor_analysis.md

3. Writing Phase
   Input: Pull from {timestamp}/research/
          Apply strategy/voice_guide.md
          Follow strategy/strategy_v*.md
   Output: {timestamp}/drafts/v1_draft.md

4. Quality Review Phase (Parallel)
   article-fact-checker:
   - Verifies facts and data accuracy
   - Checks source validity
   - Output: reports/fact_check_report.md

   article-quality-scorer:
   - Evaluates readability and structure
   - Checks strategy alignment
   - Scores multiple dimensions
   - Output: reports/quality_score_report.md

5. Human Review & Revision
   User reviews reports → Decision:
   - Approve → Continue to Visual Production
   - Revise → Create v2_draft.md → Repeat Quality Review
   - Final approval → drafts/final.md + reports/final_approval.md

6. Visual Production
   visual-creator reads: drafts/final.md
   visual-creator writes: visuals/visual_production_guide.md
   Human: Copy prompts → Gemini web
          Save images → visuals/images/

7. Platform Optimization
   See: .claude/data/articles/PLATFORM_OPTIMIZATION_STRATEGY.md
   Output: published/{platform}.md for each target platform

8. Publishing & Registry Update
   Update: registry.json
     - Clear current_work status
     - Update article statistics
     - Update global statistics
```

## Metadata.json Structure

Each article folder contains:
```json
{
  "id": "20250118_143022_ai_risks",
  "number": "001",
  "title": "When NOT to Use AI in Your Business",
  "slug": "ai_risks",
  "type": "warning",
  "status": "researching|drafting|reviewing|visual_production|published",
  "created": "2025-01-18T14:30:22Z",
  "last_modified": "2025-01-18T15:45:00Z",
  "word_count": {
    "current": 1847,
    "target": 2000
  },
  "phases": {
    "research": {
      "completed": true,
      "timestamp": "2025-01-18T14:45:00Z"
    },
    "first_draft": {
      "completed": true,
      "timestamp": "2025-01-18T15:30:00Z"
    },
    "revision": {
      "completed": false,
      "timestamp": null
    },
    "visuals": {
      "completed": false,
      "timestamp": null
    },
    "published": {
      "completed": false,
      "timestamp": null
    }
  },
  "platforms": {
    "medium": {
      "published": false,
      "url": null
    },
    "beehiiv": {
      "published": false,
      "url": null
    },
    "substack": {
      "published": false,
      "url": null
    }
  },
  "metrics": {
    "research_hours": 1.5,
    "writing_hours": 2.0,
    "revision_count": 2,
    "images_generated": 0,
    "image_cost": 0.0
  }
}
```

## Registry Integration

### Registry Updates at Each Phase

1. **Article Creation**:
   ```json
   // Update registry.json
   {
     "article_types": {
       "ai_realist": {
         "current_work": {
           "article_id": "20250118_143022_ai_risks",
           "title": "When NOT to Use AI",
           "status": "researching",
           "phase": "research",
           "started": "2025-01-18T14:30:22Z"
         }
       }
     }
   }
   ```

2. **Phase Transitions**:
   - Research complete → status: "drafting"
   - Draft complete → status: "reviewing"
   - Final approved → status: "visual_production"
   - Images ready → status: "publishing"
   - Published → status: "published"

3. **Completion**:
   - Update statistics in registry.json
   - Clear current_work in registry.json
   - Update global statistics

## Brainstorming Status

AI Realist requires initial brainstorming to create:
- `strategy/strategy_v*.md` - Overall content strategy
- `strategy/voice_guide.md` - Author voice and style guide
- `README.md` - Complete documentation

Once created, these are reused for all articles. The registry.json tracks:
```json
"article_types": {
  "ai_realist": {
    "brainstorming_status": {
      "completed": true,
      "ready_for_creation": true,
      "strategy_path": "ai_realist/strategy/strategy_v1.1.md",
      "voice_guide_path": "ai_realist/strategy/voice_guide.md"
    }
  }
}
```

If `false`, brainstorming runs first. If `true`, skip directly to article creation.

## Commands

### Start New Article
```
/art [topic]
智能路由：
  - 检查registry中的文章类型
  - 如果只有一个类型 → 直接使用
  - 如果有多个类型 → 让用户选择
  - 如果brainstorming未完成 → 先运行brainstorming
```

### Setup New Article Type
```
/art-brainstorm
  - 创建新文章类型
  - 运行战略设置流程
```

### Check Status
```
/art-status
Returns: Current article, phase, next steps
```

### Continue Work
```
/art
无参数时：
  - 如果有current_work → 继续当前文章
  - 如果无current_work → 显示选项菜单
```

## Quality Checkpoints

### Before Writing
- [ ] Article folder created with timestamp
- [ ] Research completed in article folder
- [ ] Angle matches content mix strategy
- [ ] Platform targets defined

### After Writing
- [ ] 2000 words achieved
- [ ] Voice guide compliance
- [ ] Specific numbers included
- [ ] Contrarian insight present
- [ ] Saved to drafts/final.md

### Before Publishing
- [ ] Visual guide generated
- [ ] Images created and saved
- [ ] Platform versions created
- [ ] Registry updated

## Benefits of New Structure

1. **Self-Contained**: Each article has everything in one folder
2. **Parallel Work**: Can work on multiple articles simultaneously
3. **Version History**: All drafts preserved
4. **Easy Archive**: Zip individual article folders
5. **Clear Progress**: Metadata tracks exact status
6. **No Conflicts**: Timestamp ensures uniqueness

## Migration from Old Structure

For existing articles in old structure:
1. Create new timestamp folder
2. Move files to appropriate subdirectories
3. Generate metadata.json from existing data
4. Update registry references

## What Changed

### OLD:
- Research in shared `/research/current/`
- Production in `/production/article_NNN/`
- Research cleared after each article

### NEW:
- Everything in `/content/{timestamp}_{slug}/`
- Research preserved with article
- Complete history maintained

This new structure provides better organization, allows parallel work, and maintains complete article history.