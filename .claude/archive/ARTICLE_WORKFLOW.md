# Complete Article Production Workflow
*Master operational document for the NOVELSYS-SWARM Article system*

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 0: System Initialization](#phase-0-system-initialization)
4. [Phase 1: Brainstorming & Setup](#phase-1-brainstorming--setup)
5. [Phase 2: Article Initiation](#phase-2-article-initiation)
6. [Phase 3: Research Collection](#phase-3-research-collection)
7. [Phase 4: Content Creation](#phase-4-content-creation)
8. [Phase 5: Quality Review](#phase-5-quality-review)
9. [Phase 6: Revision Cycle](#phase-6-revision-cycle)
10. [Phase 7: Visual Production](#phase-7-visual-production)
11. [Phase 8: Platform Optimization](#phase-8-platform-optimization)
12. [Phase 9: Publishing](#phase-9-publishing)
13. [Agent Specifications](#agent-specifications)
14. [Quality Standards](#quality-standards)
15. [File Specifications](#file-specifications)
16. [Status Codes](#status-codes)
17. [Error Handling](#error-handling)

---

## Overview

The Article Production Workflow is a systematic process for creating high-quality, research-backed articles from conception to publication. The system supports multiple article types, with AI Realist as the flagship implementation.

### Core Principles
- **Quality over quantity** - Every article meets defined standards
- **Research-driven** - All content backed by data and analysis
- **Human-in-the-loop** - Critical decisions remain with humans
- **Systematic approach** - Repeatable, measurable process
- **Platform optimization** - Content tailored for each platform

### Workflow Architecture
```
Brainstorming → Research → Writing → Review → Revision → Visuals → Optimization → Publishing
     ↑                                              ↓
     └──────────── Quality Gate (iterate) ──────────┘
```

---

## Prerequisites

### System Requirements
```yaml
Required Components:
  Registry:
    - .claude/data/articles/registry.json

  Agents:
    Research:
      - art-trend-researcher
      - art-audience-analyst
      - art-competitor-scanner
      - art-topic-explorer
    Writing:
      - art-article-writer
    Quality:
      - art-fact-checker
      - art-quality-scorer
    Visual:
      - art-visual-designer
    Optimization:
      - art-platform-optimizer
```

### Initial Setup Checklist
- [ ] Registry file exists at `.claude/data/articles/registry.json`
- [ ] All required agents are installed in `.claude/agents/`
- [ ] Article type folder exists (e.g., `ai_realist/`)

---

## Phase 0: System Initialization

### Purpose
Ensure the article system is properly configured before any creation begins.

### Trigger
First time using the article system or adding a new article type.

### Process
```yaml
Step 1: Check Registry Existence
  Action: Verify .claude/data/articles/registry.json exists
  If not: Create registry file

Step 2: Initialize Registry File
  Create if missing: registry.json with structure:
    {
      "version": "1.0",
      "article_types": {},
      "global_stats": {}
    }

Step 3: Register Article Type
  If new type:
    Add to registry.json -> article_types:
    {
      "type_id": {
        "name": "Type Name",
        "description": "Type description",
        "status": "active",
        "created": "ISO_DATE",
        "config": {
          "word_count": 2000,
          "platforms": ["Medium", "Vocal", "Substack", "ElevenReader"],
          "target_audience": "Target description"
        },
        "brainstorming_status": {
          "completed": false,
          "ready_for_creation": false
        },
        "current_work": {
          "article_id": null,
          "status": "not_started"
        },
        "statistics": {
          "total_articles": 0,
          "total_words": 0
        }
      }
    }
```

### Output
- Configured registry.json file
- Registered article type
- Ready for brainstorming

### Success Criteria
- Registry.json exists and is valid JSON
- Article type is registered
- No file permission errors

---

## Phase 1: Brainstorming & Setup

### Purpose
Establish the strategic foundation for an article type (one-time setup per type).

### Trigger
`brainstorming_status.ready_for_creation = false` for selected article type

### Process
```yaml
Step 1: Entry Point
  User initiates article creation process
  System checks registry for available types

Step 2: Type Selection
  If types exist:
    Display: "1) AI Realist 2) Create New Type"
  User selects type

Step 3: Check Brainstorming Status
  Read: registry.json
  Check: article_types.{type}.brainstorming_status.ready_for_creation

Step 4: If Not Ready - Execute Brainstorming
  Interactive Questions:
    1. Target Audience
       "Who is your primary reader?"
       Store: audience_profile

    2. Content Strategy
       "What value do you provide?"
       "What's your unique angle?"
       Store: value_proposition

    3. Voice & Tone
       "How should articles sound?"
       "Formal/Casual? Expert/Approachable?"
       Store: voice_characteristics

    4. Content Mix
       "What types of articles?"
       "What percentage of each?"
       Store: content_distribution

    5. Publishing Strategy
       "Which platforms?"
       "Publishing frequency?"
       Store: publishing_plan

Step 5: Generate Strategy Documents
  Create:
    {type}/strategy/strategy_v1.0.md
    {type}/strategy/voice_guide.md
    {type}/README.md

Step 6: Update Registry
  Update registry.json:
    Set: article_types.{type}.brainstorming_status.ready_for_creation = true
    Set: article_types.{type}.brainstorming_status.completed = true
    Add: strategy_path, voice_guide_path, readme_path
```

### Output Documents

#### strategy_v1.0.md Structure
```markdown
# [Type Name] Content Strategy

## Mission Statement
[One paragraph defining the purpose]

## Target Audience
- Primary: [Detailed persona]
- Secondary: [If applicable]
- Pain Points: [What problems do they have]
- Goals: [What do they want to achieve]

## Value Proposition
- Unique Angle: [What makes this different]
- Core Benefits: [What readers gain]
- Differentiators: [vs. competition]

## Content Distribution
- Type A: 50% - [Description]
- Type B: 30% - [Description]
- Type C: 20% - [Description]

## Success Metrics
- Engagement: [How measured]
- Growth: [Targets]
- Quality: [Standards]

## Editorial Guidelines
- Topics to Cover: [List]
- Topics to Avoid: [List]
- Fact-Checking Requirements: [Standards]
```

#### voice_guide.md Structure
```markdown
# Voice & Style Guide

## Voice Characteristics
- Personality: [3-5 traits]
- Expertise Level: [Expert/Intermediate/Accessible]
- Emotional Tone: [Analytical/Empathetic/Motivational]

## Writing Style
- Sentence Structure: [Simple/Complex/Varied]
- Paragraph Length: [Short/Medium/Long]
- Technical Terms: [How to handle]
- Examples: [Frequency and type]

## Language Patterns
### Do Use:
- [Pattern 1 with example]
- [Pattern 2 with example]

### Don't Use:
- [Anti-pattern 1]
- [Anti-pattern 2]

## Sample Passages
[2-3 example paragraphs in the target voice]
```

### Success Criteria
- All strategy documents created
- registry.json updated with document paths
- brainstorming_status.ready_for_creation = true

---

## Phase 2: Article Initiation

### Purpose
Begin creation of a specific article within an established type.

### Trigger
User provides specific article topic/direction after brainstorming is complete.

### Entry Commands
```
/art [topic] - Smart routing based on available types
/art - Continue current work or show menu
```

### Process
```yaml
Step 1: Topic Specification
  User: /art "AI hallucinations in healthcare"
  System:
    - Check registry for article types
    - If only 1 type → use it
    - If multiple → let user choose
    - Capture topic and generate slug

Step 2: Generate Unique Identifier
  Format: {timestamp}_{slug}
  Example: 20250118_143022_ai_hallucinations

Step 3: Create Article Structure
  Create folders:
    {type}/content/{timestamp}_{slug}/
    ├── metadata.json
    ├── research/
    ├── drafts/
    ├── reports/
    ├── visuals/
    └── published/

Step 4: Initialize Metadata
  Create metadata.json:
    {
      "id": "{timestamp}_{slug}",
      "type": "{article_type}",
      "subtype": "{warning|analysis|solution}",
      "title": null,
      "topic": "{user_provided_topic}",
      "slug": "{generated_slug}",
      "status": "initiated",
      "phase": "research",
      "created": "ISO_TIMESTAMP",
      "last_modified": "ISO_TIMESTAMP",
      "word_count": {
        "target": 2000,
        "current": 0
      },
      "phases": {
        "research": {"completed": false, "timestamp": null},
        "first_draft": {"completed": false, "timestamp": null},
        "quality_review": {"completed": false, "timestamp": null},
        "revision": {"completed": false, "timestamp": null},
        "final_approval": {"completed": false, "timestamp": null},
        "visuals": {"completed": false, "timestamp": null},
        "published": {"completed": false, "timestamp": null}
      }
    }

Step 5: Update Production Status
  Update registry.json:
    article_types.{type}.current_work = {
      "article_id": "{timestamp}_{slug}",
      "title": null,
      "status": "researching",
      "phase": "research",
      "path": "{type}/content/{timestamp}_{slug}/",
      "started": "ISO_TIMESTAMP"
    }
```

### Output
- Article folder structure created
- Metadata initialized
- registry.json updated with current work
- Ready for research phase

### Success Criteria
- Unique folder created
- Valid metadata.json
- registry.json shows active article

---

## Phase 3: Research Collection

### Purpose
Gather comprehensive information to inform article writing.

### Trigger
Article status = "initiated", phase = "research"

### Process
```yaml
Step 1: Launch Research Agents (Parallel)
  Execute simultaneously:

  art-trend-researcher:
    Input: "{topic} in {target_audience} context"
    Task: "Analyze current trends, emerging patterns, and market dynamics"
    Output: research/trends.md
    Intelligence: "Auto-detects completeness and suggests areas to expand"

  art-audience-analyst:
    Input: "{topic} for {target_audience}"
    Task: "Deep dive into audience needs, pain points, and expectations"
    Output: research/audience_notes.md
    Intelligence: "Evaluates profile depth and identifies missing insights"

  art-competitor-scanner:
    Input: "{topic} competitive landscape"
    Task: "Analyze existing content, identify gaps, find opportunities"
    Output: research/competitor_analysis.md
    Intelligence: "Highlights differentiation opportunities"

  art-topic-explorer:
    Input: "{topic} comprehensive exploration"
    Task: "Research subtopics, related concepts, expert opinions"
    Output: research/topic_research.md
    Intelligence: "Assesses topic coverage and suggests depth areas"

Step 2: Research Synthesis
  After all complete:
    Create: research/research_summary.md
    Content:
      - Key findings from each source
      - Identified angles
      - Recommended focus areas
      - Data points to include
      - Sources to cite

Step 3: Update Status
  metadata.json:
    - phases.research.completed = true
    - phases.research.timestamp = now
    - status = "researched"
    - phase = "writing"

  registry.json:
    - article_types.{type}.current_work.phase = "writing"
    - article_types.{type}.current_work.status = "researched"
```

### Research Output Standards

#### trends.md Structure
```markdown
# Market & Trend Analysis

## Current Trends
- Trend 1: [Description + Data]
- Trend 2: [Description + Data]

## Emerging Patterns
- Pattern 1: [What's changing]
- Pattern 2: [What's developing]

## Market Dynamics
- Growth areas: [List]
- Declining areas: [List]
- Opportunities: [List]

## Relevant Statistics
- [Stat 1 with source]
- [Stat 2 with source]
```

#### audience_notes.md Structure
```markdown
# Audience Analysis

## Primary Audience Profile
- Demographics: [Details]
- Psychographics: [Details]
- Current Knowledge Level: [Assessment]

## Pain Points
1. [Pain point + why it matters]
2. [Pain point + why it matters]

## Information Needs
- Must know: [List]
- Want to know: [List]
- Surprised by: [List]

## Preferred Content Style
- Format preferences: [Details]
- Depth expectations: [Details]
- Example preferences: [Details]
```

### Success Criteria
- All 4 research files created
- Research summary synthesized
- Metadata updated
- Phase transition to "writing"

---

## Phase 4: Content Creation

### Purpose
Transform research into a complete first draft.

### Trigger
Article phase = "writing"

### Process
```yaml
Step 1: Article Writer Execution
  Agent: art-article-writer

  Inputs:
    - All files from research/
    - strategy/strategy_v*.md
    - strategy/voice_guide.md
    - metadata.json (for topic, type, word count)

  Task Prompt:
    "Create a {word_count}-word article on {topic} for {target_audience}.

     Follow these guidelines:
     1. Use the voice and style from voice_guide.md
     2. Incorporate research findings from research/ folder
     3. Structure as {subtype} article type
     4. Include relevant data and examples
     5. Maintain flow and readability
     6. Add compelling introduction and conclusion
     7. Use subheadings for structure
     8. Include actionable insights

     Output complete article to drafts/v1_draft.md"

Step 2: Structural Validation
  Check v1_draft.md for:
    - Word count (±10% of target)
    - Heading structure
    - Introduction present
    - Conclusion present
    - Paragraph distribution

Step 3: Update Metadata
  metadata.json:
    - word_count.current = [actual count]
    - phases.first_draft.completed = true
    - phases.first_draft.timestamp = now
    - status = "drafted"
    - phase = "quality_review"

  registry.json:
    - article_types.{type}.current_work.phase = "quality_review"
    - article_types.{type}.current_work.status = "drafted"
```

### Article Structure Template
```markdown
# [Compelling Title]

[Strong hook - 2-3 sentences that grab attention]

## Introduction
[Set up the problem/opportunity - 150-200 words]

## [Main Point 1 Heading]
[Content with examples and data - 400-500 words]

## [Main Point 2 Heading]
[Content with examples and data - 400-500 words]

## [Main Point 3 Heading]
[Content with examples and data - 400-500 words]

## [Practical Application Heading]
[How to apply this information - 300-400 words]

## Conclusion
[Summarize and call to action - 150-200 words]

---
*Key Takeaways:*
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]
```

### Success Criteria
- v1_draft.md created
- Word count within range
- Follows structure template
- Incorporates research
- Matches voice guide

---

## Phase 5: Quality Review

### Purpose
Comprehensive evaluation of article quality and accuracy.

### Trigger
Article phase = "quality_review"

### Process
```yaml
Step 1: Launch Quality Agents (Parallel)

  art-fact-checker:
    Input: drafts/v1_draft.md + research/

    Tasks:
      1. Verify all statistics and data points
      2. Check source validity
      3. Confirm logical consistency
      4. Identify unsupported claims
      5. Flag potential inaccuracies

    Output: reports/fact_check_report.md
    Intelligence: "Identifies critical vs minor issues, suggests corrections"

  art-quality-scorer:
    Input: drafts/v1_draft.md + strategy/ + voice_guide.md

    Tasks:
      1. Score readability (Flesch-Kincaid)
      2. Evaluate structure and flow
      3. Check voice alignment
      4. Assess value delivery
      5. Rate engagement potential
      6. Verify strategic alignment

    Output: reports/quality_score_report.md
    Intelligence: "Provides specific improvement recommendations"

Step 2: Generate Consolidated Report
  Create: reports/review_summary.md

  Content:
    ## Review Summary
    - Overall Score: [X/100]
    - Fact Check: [Pass/Fail + issues]
    - Quality Score: [Breakdown by dimension]
    - Recommended Actions: [Prioritized list]
    - Critical Issues: [Must fix]
    - Suggestions: [Nice to have]

Step 3: Update Status
  metadata.json:
    - phases.quality_review.completed = true
    - phases.quality_review.timestamp = now
    - status = "reviewed"
    - phase = "revision_decision"

  registry.json:
    - article_types.{type}.current_work.phase = "revision_decision"
    - article_types.{type}.current_work.status = "reviewed"
```

### Fact Check Report Structure
```markdown
# Fact Check Report

## Summary
- Status: [PASS/FAIL/CONDITIONAL]
- Critical Issues: [Count]
- Minor Issues: [Count]

## Critical Issues
1. [Issue description]
   - Location: [Line/Paragraph]
   - Problem: [What's wrong]
   - Recommendation: [How to fix]

## Data Verification
| Claim | Source | Status | Notes |
|-------|--------|--------|-------|
| [Data point] | [Source] | ✓/✗ | [Comments] |

## Logical Consistency
- [Any logical flaws found]

## Recommendations
1. [Priority fix 1]
2. [Priority fix 2]
```

### Quality Score Report Structure
```markdown
# Quality Assessment Report

## Overall Score: [X/100]

## Dimension Scores
- Readability: [X/20]
  - Flesch-Kincaid Score: [X]
  - Sentence Variety: [Good/Fair/Poor]
  - Paragraph Flow: [Good/Fair/Poor]

- Structure: [X/20]
  - Logical Organization: [X/10]
  - Heading Effectiveness: [X/10]

- Voice Alignment: [X/20]
  - Matches Guide: [X%]
  - Consistency: [Good/Fair/Poor]

- Value Delivery: [X/20]
  - Actionable Insights: [Count]
  - Unique Perspectives: [Yes/No]
  - Research Integration: [Good/Fair/Poor]

- Engagement: [X/20]
  - Hook Strength: [Strong/Medium/Weak]
  - Narrative Flow: [Good/Fair/Poor]
  - Conclusion Impact: [Strong/Medium/Weak]

## Strengths
- [What works well]

## Areas for Improvement
- [What needs work]

## Recommendations
1. [Specific improvement 1]
2. [Specific improvement 2]
```

### Success Criteria
- Both review reports generated
- Consolidated summary created
- Clear pass/fail determination
- Specific actionable feedback

---

## Phase 6: Revision Cycle

### Purpose
Iterative improvement based on quality review feedback.

### Trigger
User reviews reports and decides to revise.

### Process
```yaml
Step 1: Human Decision Point
  System: Display reports/review_summary.md

  Options:
    1. Approve → Skip to Phase 7
    2. Minor Revisions → Quick fixes
    3. Major Revisions → Substantial rewrite
    4. Reject → Archive and restart

Step 2: If Revisions Needed

  Minor Revisions Path:
    - User or agent makes specific fixes
    - Create: drafts/v2_draft.md
    - Run fact-checker only
    - If pass → Approve

  Major Revisions Path:
    - Return to art-article-writer with:
      - Original v1_draft.md
      - Review reports
      - Specific revision instructions
    - Create: drafts/v2_draft.md
    - Full quality review cycle
    - May iterate to v3, v4...

Step 3: Final Approval
  When approved:
    - Copy latest draft to drafts/final.md
    - Create: reports/final_approval.md
    - Content:
      - Approval timestamp
      - Final scores
      - Revision count
      - Sign-off note

Step 4: Update Metadata
  metadata.json:
    - phases.revision.completed = true
    - phases.final_approval.completed = true
    - status = "approved"
    - phase = "visual_production"

  registry.json:
    - article_types.{type}.current_work.phase = "visual_production"
    - article_types.{type}.current_work.status = "approved"
```

### Revision Log Structure
Create/Update: reports/revision_log.json
```json
{
  "revisions": [
    {
      "version": "v2",
      "timestamp": "ISO_TIMESTAMP",
      "trigger": "fact_check_failure",
      "changes": [
        "Fixed statistical error in paragraph 3",
        "Updated source reference"
      ],
      "reviewer": "human"
    }
  ],
  "total_revisions": 1,
  "final_version": "v2"
}
```

### Success Criteria
- final.md exists
- All critical issues resolved
- Quality score ≥ threshold
- Human approval documented

---

## Phase 7: Visual Production

### Purpose
Generate images and visual assets for the article.

### Trigger
Article phase = "visual_production"

### Process
```yaml
Step 1: Visual Creator Execution
  Agent: art-visual-designer
  Input: drafts/final.md

  Task:
    1. Analyze article content
    2. Identify visual opportunities
    3. Generate image concepts
    4. Create detailed prompts for each image
    5. Specify platform requirements

  Output: visuals/visual_production_guide.md

Step 2: Visual Guide Structure
  # Visual Production Guide

  ## Article Summary
  [Brief context for visual creation]

  ## Image Requirements
  Total Images Needed: [3-5]

  ### Hero Image (Main/Feature)
  - Purpose: [Grab attention, convey main theme]
  - Concept: [Detailed description]
  - Style: [Photorealistic/Illustration/Abstract]
  - Mood: [Professional/Dramatic/Optimistic]
  - Color Palette: [Specific colors]

  Platform Specifications:
  - Medium: 1400x933px
  - Vocal: 1920x1200px
  - Substack: 1456x816px

  Gemini/Banana Prompt:
  "[Complete generation prompt]"

  ### Supporting Image 1
  [Same structure]

  ### Supporting Image 2
  [Same structure]

Step 3: Human Image Generation
  - Copy prompts to Gemini/Banana
  - Generate images
  - Save to visuals/images/
  - Name: hero.jpg, support1.jpg, etc.

Step 4: Update Metadata
  metadata.json:
    - phases.visuals.completed = true
    - status = "visuals_complete"
    - phase = "platform_optimization"

  registry.json:
    - article_types.{type}.current_work.phase = "platform_optimization"
    - article_types.{type}.current_work.status = "visuals_complete"
```

### Success Criteria
- Visual guide created
- All prompts generated
- Images saved (human task)
- Metadata updated

---

## Phase 8: Platform Optimization

### Purpose
Adapt content for specific platform requirements.

### Trigger
Article phase = "platform_optimization"

### Process
```yaml
Step 1: Platform Adaptation
  Use art-platform-optimizer agent with:
    Input: drafts/final.md
    Strategy: PLATFORM_OPTIMIZATION_STRATEGY.md

  The agent will create optimized versions for each platform:
    - Medium (published/medium.md)
    - Substack (published/substack.md)
    - Vocal (published/vocal.md)
    - ElevenReader (published/elevenreader.md)

  See PLATFORM_OPTIMIZATION_STRATEGY.md for detailed optimization rules

Step 2: Platform Checklist
  Each version must have:
    - [ ] Platform-specific title optimization
    - [ ] Proper image placement markers
    - [ ] Platform tags/categories
    - [ ] Optimized meta description
    - [ ] Platform-specific CTAs
    - [ ] Formatting adjustments
    - [ ] Length considerations

Step 3: Update Metadata
  metadata.json:
    - phases.platform_optimization.completed = true
    - status = "ready_to_publish"
    - phase = "publishing"

  registry.json:
    - article_types.{type}.current_work.phase = "publishing"
    - article_types.{type}.current_work.status = "ready_to_publish"
```

### Platform Optimization Details

For complete platform-specific optimization rules, templates, and best practices, see:
**[PLATFORM_OPTIMIZATION_STRATEGY.md](PLATFORM_OPTIMIZATION_STRATEGY.md)**

This document contains:
- Platform-specific title formulas
- Content structure requirements
- Algorithm priorities
- Engagement optimization strategies
- Dynamic update protocols

#### Quick Example - Medium Optimization
```markdown
# [SEO-Optimized Title]

![Hero Image](image_url)
*[Image caption with context]*

[Hook paragraph - strong and immediate]

## [First Section Title]
[Content...]

> [Pull quote for emphasis]

## [Continue sections...]

---

## Key Takeaways
- [Bullet point 1]
- [Bullet point 2]

**What's your experience with [topic]? Share in the comments.**

---
*[Author bio and credentials]*

Tags: #tag1 #tag2 #tag3 #tag4 #tag5
```

### Success Criteria
- All 4 platform versions created
- Platform-specific optimizations applied
- Ready for publishing

---

## Phase 9: Publishing

### Purpose
Finalize and track article publication.

### Trigger
User publishes article on platforms.

### Process
```yaml
Step 1: Pre-Publication Checklist
  Verify:
    - [ ] final.md exists
    - [ ] All platform versions ready
    - [ ] Images prepared
    - [ ] Quality approved
    - [ ] Metadata current

Step 2: Publication Tracking
  User publishes on each platform
  Update metadata.json:
    {
      "platforms": {
        "medium": {
          "published": true,
          "date": "ISO_DATE",
          "url": "https://medium.com/...",
          "stats": {
            "initial_views": 0
          }
        },
        "vocal": {
          "published": true,
          "date": "ISO_DATE",
          "url": "https://vocal.media/...",
          "stats": {
            "initial_reads": 0
          }
        },
        "substack": {
          "published": true,
          "date": "ISO_DATE",
          "url": "https://substack.com/...",
          "stats": {
            "initial_subscribers_sent": 0
          }
        },
        "elevenreader": {
          "published": true,
          "date": "ISO_DATE",
          "url": "https://elevenreader.com/...",
          "stats": {
            "initial_reads": 0
          }
        }
      }
    }

Step 3: Update Registry

  Update registry.json:
    Clear current_work:
      article_types.{type}.current_work = {
        "article_id": null,
        "status": "not_started"
      }

    Update statistics:
      article_types.{type}.statistics.total_articles += 1
      article_types.{type}.statistics.total_words += word_count
      article_types.{type}.statistics.platforms_published.{platform} += 1
      article_types.{type}.statistics.last_published = "ISO_DATE"

    Update global stats:
      global_stats.total_articles += 1
      global_stats.total_words += word_count
      global_stats.last_activity = "ISO_TIMESTAMP"

Step 4: Archive and Complete
  - phases.published.completed = true
  - status = "published"
  - phase = "complete"
```

### Success Criteria
- Article published on all platforms
- URLs recorded
- Registry fully updated
- Statistics incremented

---

## Agent Specifications

### Research Agents

#### art-trend-researcher
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Analyze current trends and patterns
  - Identify emerging developments
  - Collect relevant statistics
  - Map market dynamics

Intelligence Features:
  - Auto-assess coverage completeness
  - Suggest expansion areas
  - Highlight critical trends

Output:
  - trends.md with minimum 5 trends, 10 statistics
```

#### art-audience-analyst
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Profile target audience
  - Identify pain points and needs
  - Map content preferences
  - Analyze engagement patterns

Intelligence Features:
  - Evaluate profile depth
  - Identify missing insights
  - Suggest research areas

Output:
  - audience_notes.md with minimum 5 pain points
```

#### art-competitor-scanner
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Analyze competing content
  - Identify content gaps
  - Find differentiation opportunities
  - Benchmark quality standards

Intelligence Features:
  - Highlight unique opportunities
  - Assess competitive advantage
  - Suggest positioning

Output:
  - competitor_analysis.md with minimum 5 analyses
```

#### art-topic-explorer
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Deep dive into topic
  - Map subtopics and relationships
  - Collect expert opinions
  - Identify controversies

Intelligence Features:
  - Assess topic comprehensiveness
  - Suggest depth areas
  - Flag knowledge gaps

Output:
  - topic_research.md with minimum 10 subtopics
```

### Writing and Quality Agents

#### art-article-writer
```yaml
Type: Writing Agent
Tools: Read, Write
Model: claude-sonnet-4 (for quality)

Responsibilities:
  - Transform research into cohesive article
  - Apply voice and style guidelines
  - Structure content effectively
  - Integrate data and examples
  - Meet word count requirements

Input Requirements:
  - All research files
  - Strategy documents
  - Voice guide
  - Article metadata

Output:
  - Complete article draft
  - Proper markdown formatting
  - Word count within ±10% of target
```

#### art-fact-checker
```yaml
Type: Quality Agent
Tools: Read, Write, WebSearch
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Verify all factual claims
  - Check data accuracy
  - Validate sources
  - Identify logical inconsistencies
  - Flag unsupported statements

Input Requirements:
  - Article draft
  - Research files for cross-reference

Output:
  - Detailed fact-check report
  - Pass/Fail determination
  - Specific issues with locations
```

#### art-quality-scorer
```yaml
Type: Quality Agent
Tools: Read, Write
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Score readability metrics
  - Evaluate structure and flow
  - Check voice alignment
  - Assess value delivery
  - Measure engagement potential

Input Requirements:
  - Article draft
  - Strategy documents
  - Voice guide

Output:
  - Multi-dimensional quality scores
  - Specific improvement recommendations
  - Overall quality rating
```

### Visual and Optimization Agents

#### art-visual-designer
```yaml
Type: Visual Agent
Tools: Read, Write
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Analyze article for visual opportunities
  - Design image concepts
  - Create AI generation prompts
  - Specify platform requirements

Intelligence Features:
  - Identify key visual moments
  - Ensure style consistency
  - Suggest enhancement opportunities

Output:
  - visual_production_guide.md with prompts
  - Hero image + minimum 2 supporting images
```

#### art-platform-optimizer
```yaml
Type: Optimization Agent
Tools: Read, Write
Model: claude-haiku-3-5 (for speed)

Responsibilities:
  - Adapt content for each platform
  - Optimize titles and structure
  - Apply platform-specific formatting
  - Add engagement elements

Intelligence Features:
  - Platform algorithm optimization
  - Engagement prediction
  - SEO enhancement

Output:
  - Platform-specific versions (medium.md, substack.md, vocal.md, elevenreader.md)
  - Each optimized for platform requirements
```

---

## Quality Standards

### Minimum Acceptable Criteria
```yaml
Content Quality:
  - Fact Check: PASS (no critical errors)
  - Quality Score: ≥ 70/100
  - Readability: Flesch-Kincaid 8-12
  - Word Count: Target ±10%

Structure:
  - Clear introduction
  - Logical flow
  - Strong conclusion
  - Proper headings

Research Integration:
  - Minimum 3 data points
  - At least 2 examples
  - Source attribution

Voice Alignment:
  - Consistent tone
  - Matches guide ≥80%
  - Appropriate for audience
```

### Excellence Criteria
```yaml
Content Quality:
  - Quality Score: ≥ 85/100
  - Zero fact issues
  - Compelling narrative

Value Delivery:
  - 5+ actionable insights
  - Unique perspective
  - Clear takeaways

Engagement:
  - Strong hook
  - Quotable sections
  - Discussion worthy
```

---

## File Specifications

### Naming Conventions
```yaml
Timestamps: YYYYMMDD_HHMMSS
Slugs: lowercase_underscore_separated

Folders:
  - {timestamp}_{slug}/

Files:
  - v{n}_draft.md (iterations)
  - final.md (approved version)
  - *_report.md (quality reports)
  - *_guide.md (instructions)

Images:
  - hero.jpg (main image)
  - support{n}.jpg (supporting)
  - platform_{name}.jpg (specific)
```

### Required Folder Structure
```
{article_type}/
├── strategy/
│   ├── strategy_v*.md
│   └── voice_guide.md
├── README.md
└── content/
    └── {timestamp}_{slug}/
        ├── metadata.json
        ├── research/
        │   ├── trends.md
        │   ├── audience_notes.md
        │   ├── competitor_analysis.md
        │   ├── topic_research.md
        │   └── research_summary.md
        ├── drafts/
        │   ├── v1_draft.md
        │   ├── v2_draft.md (if revised)
        │   └── final.md
        ├── reports/
        │   ├── fact_check_report.md
        │   ├── quality_score_report.md
        │   ├── review_summary.md
        │   ├── revision_log.json
        │   └── final_approval.md
        ├── visuals/
        │   ├── visual_production_guide.md
        │   ├── prompts.txt
        │   └── images/
        │       ├── hero.jpg
        │       └── support*.jpg
        └── published/
            ├── medium.md
            ├── vocal.md
            ├── substack.md
            └── elevenreader.md
```

---

## Status Codes

### Article Status Values
```yaml
initiated: Article folder created, ready for research
researching: Research agents active
researched: Research complete, ready for writing
drafting: Article being written
drafted: First draft complete
reviewing: Quality review in progress
reviewed: Review complete, awaiting decision
revising: Revision in progress
approved: Final approval given
visual_production: Creating visual assets
visuals_complete: Images ready
optimizing: Platform versions being created
ready_to_publish: All versions ready
publishing: Publication in progress
published: Article live on platforms
```

### Phase Values
```yaml
research: Gathering information
writing: Creating content
quality_review: Checking quality
revision_decision: Awaiting human decision
revision: Implementing changes
visual_production: Creating images
platform_optimization: Adapting for platforms
publishing: Going live
complete: Fully published
```

---

## Error Handling

### Common Issues and Solutions

#### Research Phase Failures
```yaml
Issue: Agent timeout
Solution:
  1. Retry individual agent
  2. Use cached partial results
  3. Proceed with available research

Issue: Insufficient research
Solution:
  1. Run additional targeted research
  2. Augment with manual research
  3. Narrow topic scope
```

#### Writing Phase Failures
```yaml
Issue: Word count significantly off
Solution:
  1. If too long: Request condensation
  2. If too short: Request expansion
  3. Manual adjustment acceptable

Issue: Voice mismatch
Solution:
  1. Re-run with stronger voice guide emphasis
  2. Manual voice adjustment
  3. Update voice guide for clarity
```

#### Quality Review Failures
```yaml
Issue: Repeated quality failures
Solution:
  1. Return to research phase
  2. Revise strategy alignment
  3. Consider topic pivot

Issue: Fact check critical errors
Solution:
  1. Must fix before proceeding
  2. Provide correct sources
  3. Remove unsupported claims
```

### Recovery Procedures
```yaml
At any phase failure:
  1. Save current state
  2. Log error in metadata
  3. Attempt recovery
  4. If unrecoverable:
     - Archive attempt
     - Restart from last good phase
     - Update registry accordingly
```

---


---

## Workflow Optimization Tips

### Batch Operations
- Run research for multiple topics simultaneously
- Process revisions in batches
- Generate visuals for multiple articles together

### Quality Shortcuts
- Create topic templates for common article types
- Build a library of proven introductions/conclusions
- Maintain a style phrase bank

### Time Savers
- Pre-research trending topics weekly
- Keep updated competitor analysis
- Maintain running statistics dashboard

### Continuous Improvement
- Review quality scores trends
- Update strategy based on performance
- Refine voice guide with successful examples
- Archive best practices

---

## Appendix A: Example Article Lifecycle

### Real Example: AI Hallucinations in Healthcare
```yaml
Day 1 - Morning:
  09:00 - /brainstorm → Article → AI Realist
  09:30 - Topic: "AI hallucinations in healthcare"
  09:31 - Folder: 20250118_093100_ai_healthcare_risks/
  09:32 - Research agents launched (parallel)
  10:15 - Research complete, summary generated

Day 1 - Afternoon:
  14:00 - Article-writer begins
  15:30 - v1_draft.md complete (2,047 words)
  15:31 - Quality review launched
  16:00 - Reviews complete:
          - Fact check: FAIL (2 critical issues)
          - Quality score: 72/100

Day 2 - Morning:
  09:00 - Review reports, decide to revise
  09:30 - Fix fact issues, improve flow
  10:30 - v2_draft.md complete
  10:31 - Re-run fact checker only
  10:45 - Fact check: PASS
  10:46 - Approve → final.md

Day 2 - Afternoon:
  14:00 - Visual-creator generates prompts
  14:30 - Human creates images in Banana
  15:30 - Platform versions created
  16:00 - Published on all platforms
  16:15 - Registry updated, complete
```

---

## Appendix B: Quality Score Rubric

### Scoring Breakdown (100 points total)

#### Readability (20 points)
- Flesch-Kincaid 8-10: 20 pts
- Flesch-Kincaid 11-12: 15 pts
- Flesch-Kincaid 13-14: 10 pts
- Flesch-Kincaid >14: 5 pts

#### Structure (20 points)
- Perfect flow: 20 pts
- Minor issues: 15 pts
- Needs improvement: 10 pts
- Poor structure: 5 pts

#### Voice Alignment (20 points)
- 90-100% match: 20 pts
- 80-89% match: 15 pts
- 70-79% match: 10 pts
- <70% match: 5 pts

#### Value Delivery (20 points)
- Exceptional value: 20 pts
- Strong value: 15 pts
- Adequate value: 10 pts
- Limited value: 5 pts

#### Engagement (20 points)
- Highly engaging: 20 pts
- Good engagement: 15 pts
- Moderate engagement: 10 pts
- Low engagement: 5 pts

---

## Appendix C: Registry JSON Schemas

### article_types.json
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "types": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["name", "description", "status", "brainstorming_status"],
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"},
          "status": {"enum": ["active", "inactive", "archived"]},
          "brainstorming_status": {
            "type": "object",
            "properties": {
              "completed": {"type": "boolean"},
              "outputs": {"type": "object"},
              "ready_for_creation": {"type": "boolean"}
            }
          }
        }
      }
    }
  }
}
```

---

## Version History

- v1.0 (2025-01-18): Initial complete workflow documentation
- Created by: NOVELSYS-SWARM System
- Status: Active Production Document

---

*This is the authoritative source for Article production workflow. All agents and commands should reference this document for operational procedures.*