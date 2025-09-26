# Article Production Workflow - Complete Master Document
*Authoritative operational and technical reference for the NOVELSYS-SWARM Article system*

## Document Status
- **Version**: 3.0
- **Updated**: 2025-09-21
- **Status**: Primary Reference Document with User Materials Integration
- **Supersedes**: ARTICLE_WORKFLOW.md v2.1

## CRITICAL CITATION FORMAT REQUIREMENTS

**ALL CONTENT MUST USE INLINE HYPERLINK CITATIONS:**

### Required Format:
```markdown
[descriptive text](https://exact-url.com)
```

### Examples:
```markdown
When [MIT researchers discovered](https://mit.edu/ai-study-2024) that 82% of medical AI tools fail,
it sent shockwaves through the industry. This finding aligns with [Gartner's earlier prediction](https://www.gartner.com/en/newsroom/press-releases/2024-01-ai-predictions)
about AI project failures.

The AI healthcare market reached [$21.1 billion in 2024](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-healthcare-market)
according to Grand View Research.
```

### FORBIDDEN Formats:
- ❌ Reference lists: `[1] MIT Study 2024`
- ❌ Footnotes: `According to research¹`
- ❌ Bibliography sections
- ❌ Endnotes

### Quality Standards for Citations:
- **Descriptive links**: Links must describe the source, not just say "here" or "this"
- **Direct URLs**: All links must be complete, working URLs
- **Source year**: Include (Source, Year) when relevant for important data
- **English only**: All content and citations must be in English

## Overview
This document is the complete master document for the article production system, containing technical specifications, operational processes, real examples, and execution details with **mandatory inline hyperlink citation format** and **user materials integration**.

## Architecture Implementation

**Technical Architecture**: See [ARTICLE_SYSTEM_ARCHITECTURE.md](ARTICLE_SYSTEM_ARCHITECTURE.md) for complete technical specifications.

**Architecture Status**: This workflow document describes the business process. The technical implementation follows NOVELSYS-SWARM's 5-layer architecture as specified in ARTICLE_SYSTEM_ARCHITECTURE.md.

**Key Components**:
- Commands: art.md, art-brainstorm.md (delegation only)
- Coordinator: art-workflow-coordinator.md (returns JSON plans, NO Task)
- Agents: 9 specialized agents (single responsibility, NO Task)
- Execution: Phase-based with Main Claude orchestration

## Core Principles
- **Quality over quantity** - Every article meets defined standards
- **Research-driven** - All content supported by data and analysis with inline citations
- **Human-in-the-loop** - Critical decisions made by humans
- **Systematic approach** - Repeatable, measurable processes
- **Platform optimization** - Content customized for each platform
- **Citation compliance** - All sources use inline hyperlink format
- **User materials integration** - Leverage user research when available

## Quick Start

**For Implementers**: Start with [ARTICLE_SYSTEM_ARCHITECTURE.md](ARTICLE_SYSTEM_ARCHITECTURE.md) for technical implementation details.

## Table of Contents
1. [Phase 0: System Initialization](#phase-0-system-initialization)
2. [Phase 1: Brainstorming & Setup](#phase-1-brainstorming--setup)
3. [Phase 2: Article Initiation](#phase-2-article-initiation)
4. [Phase 3A: User Materials Processing](#phase-3a-user-materials-processing)
5. [Phase 3B: Research Collection](#phase-3b-research-collection)
6. [Phase 4: Content Creation](#phase-4-content-creation)
7. [Phase 5: Quality Review](#phase-5-quality-review)
8. [Phase 6: Revision Cycle](#phase-6-revision-cycle)
9. [Phase 7: Visual Production](#phase-7-visual-production)
10. [Phase 8: Platform Optimization](#phase-8-platform-optimization)
11. [Phase 9: Publishing](#phase-9-publishing)
12. [Complete Timeline](#complete-timeline)
13. [Agent Specifications](#agent-specifications)
14. [Quality Standards](#quality-standards)
15. [File Specifications](#file-specifications)
16. [Status Codes](#status-codes)
17. [Error Handling](#error-handling)

---

## Phase 0: System Initialization

### Purpose
Ensure the article system is properly configured before creating any articles. This is one-time system preparation.

### Trigger Conditions
- First time using the article system
- Or when adding new article types

### Detailed Process

**Step 1: Check Registry existence**
  - Verify .claude/data/articles/registry.json exists
  - If it doesn't exist, needs to be created

**Step 2: Initialize Registry file**
  If file doesn't exist, create basic structure:
  ```json
  {
    "version": "1.0",
    "article_types": {},
    "global_stats": {}
  }
  ```

**Step 3: Register article type**
  If it's a new type, add to registry.json's article_types:
  ```json
  {
    "type_id": {  // e.g. "ai_realist"
      "name": "Type Name",  // e.g. "AI Realist"
      "description": "Type description",
      "status": "active",
      "created": "ISO_DATE",
      "config": {
        "word_count": 2000,  // Target word count
        "platforms": ["Medium", "Substack", "ElevenReader"],  // 3 platforms
        "target_audience": "Target description"
      },
      "brainstorming_status": {
        "completed": false,  // Initially false
        "ready_for_creation": false  // Need brainstorming first
      },
      "current_work": {
        "article_id": null,
        "status": "none",
        "phase": "none"
      },
      "statistics": {
        "articles_created": 0,
        "articles_completed": 0,
        "total_words": 0,
        "avg_quality_score": 0
      }
    }
  }
  ```

### Success Criteria
- ✅ registry.json exists and is valid
- ✅ Article type registered
- ✅ Brainstorming status shows ready_for_creation: false
- ✅ Ready to proceed to Phase 1

---

## Phase 1: Brainstorming & Setup

### Purpose
Establish content strategy, voice guidelines, and platform optimization strategy for the article type.

### Trigger Conditions
- brainstorming_status.ready_for_creation = false
- New article type needs strategy development

### Interactive Process
This phase requires human input to establish:

**Strategic Foundation Questions:**
1. **Target Audience Definition**
   - Who are we writing for?
   - What are their pain points?
   - What level of expertise do they have?
   - What platforms do they prefer?

2. **Value Proposition Clarification**
   - What unique perspective do we offer?
   - What problems do we solve?
   - What outcomes do readers achieve?
   - How do we differentiate from competitors?

3. **Voice and Tone Establishment**
   - What personality does our content have?
   - How formal or casual should we be?
   - What emotions do we want to evoke?
   - What language patterns define our style?

4. **Content Distribution Strategy**
   - Which platforms are primary/secondary?
   - What content formats work best?
   - How do we optimize for each platform?
   - What engagement strategies do we use?

5. **Publishing Platform Priorities**
   - Medium optimization requirements
   - Substack newsletter approach
   - ElevenReader community focus
   - Cross-platform consistency needs

### Expected Deliverables

**strategy_v1.0.md** - Complete content strategy including:
- Target audience profiles
- Content positioning and differentiation
- Value proposition framework
- Success metrics and goals
- Competitive landscape analysis

**voice_guide.md** - Detailed voice and style guide:
- Tone characteristics and examples
- Language patterns and vocabulary
- Do's and don'ts for style
- Example passages demonstrating voice
- Audience communication preferences

**PLATFORM_OPTIMIZATION_STRATEGY.md** - Platform-specific guidelines:
- Medium: SEO, formatting, engagement tactics
- Substack: Newsletter structure, community building
- ElevenReader: Discovery optimization, reader experience
- Cross-platform consistency requirements

**README.md** - Article type overview and quick reference

### Success Criteria
- ✅ All strategy documents created and complete
- ✅ Voice guide provides clear direction (≥85% clarity)
- ✅ Platform strategy covers all target platforms
- ✅ Human approval of strategy completeness
- ✅ Registry updated: ready_for_creation = true

---

## Phase 2: Article Initiation

### Purpose
Create article folder structure and initialize tracking for a specific article topic.

### Execution
**Agent**: art-article-initiator
**Automatic Registry Update**: art-registry-updater after completion

### Process
**Step 1: Generate Article ID**
```
Format: YYYYMMDD_HHMMSS_{topic_slug}
Example: 20250120_140000_ai_medical_risks
```

**Step 2: Create Folder Structure**
```
{article_type}/content/{article_id}/
├── metadata.json
├── user_materials/ (new - user drop zone)
├── processed/ (new - analyzed user content)
├── agent_outputs/ (new - replaces research/)
├── drafts/ (ready for Phase 4)
├── reports/ (ready for Phase 5)
├── visuals/ (ready for Phase 7)
└── published/ (ready for Phase 8)
```

**Step 3: Initialize metadata.json**
```json
{
  "article_id": "20250120_140000_ai_medical_risks",
  "topic": "AI Medical Diagnosis Risks",
  "type": "warning",
  "created": "2025-01-20T14:00:00Z",
  "status": "initiated",
  "phase": "user_materials_check",
  "target_word_count": 2000,
  "user_materials": {
    "has_materials": false,
    "priority_files": [],
    "processed": false
  },
  "progress": {
    "user_materials": {"status": "pending", "materials_count": 0},
    "research": {"status": "pending", "agents_completed": 0},
    "writing": {"status": "pending", "draft_version": 0},
    "quality_review": {"status": "pending", "score": null},
    "revision": {"status": "pending", "cycles": 0},
    "visual_production": {"status": "pending"},
    "platform_optimization": {"status": "pending"},
    "publishing": {"status": "pending"}
  },
  "citation_requirements": {
    "format": "inline_hyperlinks_only",
    "language": "English_only",
    "minimum_sources": 10,
    "no_reference_lists": true
  }
}
```

**Step 4: Update Registry**
- Set current_work.article_id
- Set current_work.status = "initiated"
- Set current_work.phase = "user_materials_check"

### Success Criteria
- ✅ Folder structure created correctly with new 3-folder system
- ✅ metadata.json initialized with user materials tracking
- ✅ Registry updated with current work
- ✅ Ready to proceed to Phase 3A (User Materials Check)

---

## Phase 3A: User Materials Processing

### Purpose
Analyze and process user-provided materials to extract insights for integration with agent research.

### Trigger Conditions
- User has placed materials in user_materials/ folder
- Or user indicates they have materials to contribute

### Execution Strategy
**Agent**: materials-processor (if materials exist)
**Output**: processed/materials_insights.md

### Process

**Step 1: User Materials Detection**
- Check user_materials/ folder for content
- Identify files with priority prefixes (PRIORITY_, CORE_, SUPP_)
- Catalog available materials by type and priority

**Step 2: Materials Analysis**
- Read and analyze all user materials
- Extract key themes, insights, and data points
- Identify unique perspectives and expert knowledge
- Map materials to article relevance and value

**Step 3: Insights Generation**
Create comprehensive materials_insights.md with:
- Executive summary of user materials
- Key themes and insights extracted
- Relevant data points and statistics
- Expert perspectives and unique angles
- Recommendations for integration with agent research

### Materials Processing Standards

**Priority System Processing:**
```yaml
PRIORITY_ files:
  - Processed first and given highest weight
  - Key insights featured prominently
  - Direct integration into research guidance

CORE_ files:
  - Secondary priority, substantial integration
  - Core themes incorporated into research strategy
  - Important data points extracted and verified

SUPP_ files:
  - Supporting materials for context
  - Background information and additional perspectives
  - Used to enrich and validate other sources
```

**Output Requirements:**
```yaml
processed/materials_insights.md:
  executive_summary:
    - 3-5 key insights from user materials
    - Primary themes and unique perspectives
    - Integration recommendations for research agents

  prioritized_insights:
    - High priority findings (from PRIORITY_ files)
    - Core themes (from CORE_ files)
    - Supporting context (from SUPP_ files)

  research_guidance:
    - Specific areas for agent investigation
    - Gaps where additional research needed
    - Unique angles to explore further

  data_extraction:
    - Statistics and data points from materials
    - Expert quotes and attributions
    - Sources for fact-checking and verification
```

### Success Criteria
- ✅ All user materials analyzed and cataloged
- ✅ materials_insights.md created with comprehensive analysis
- ✅ Priority system applied correctly
- ✅ Integration guidance provided for research agents
- ✅ Ready to proceed to Phase 3B (Research Collection)

### Fallback for No User Materials
If no user materials provided:
- Skip Phase 3A
- Proceed directly to Phase 3B
- Research agents operate with pure agent-generated research
- System maintains backward compatibility

---

## Phase 3B: Research Collection

### Purpose
Gather comprehensive research foundation using 4 specialized research agents in parallel, with integration of user materials insights when available.

### Execution Strategy
**Parallel Agent Execution** - All 4 agents run simultaneously for efficiency:

#### Agent 1: art-trend-researcher
**Responsibility**: Market trends and emerging patterns
**Output**: `agent_outputs/trends.md`
**Requirements**:
- Minimum 5 major trends identified
- Minimum 10 relevant statistics with inline hyperlinks
- Data recency within 12 months preferred
- **Citation format**: Inline hyperlinks only `[descriptive text](https://url.com)`
- **Language**: English only
- **Materials Integration**: Reference processed/materials_insights.md if available

**Example Output Format**:
```markdown
# Market Trends Analysis: AI Medical Diagnosis

## User Materials Integration
*Based on processed/materials_insights.md analysis:*
- Key user insight: Focus on regulatory compliance challenges
- Priority area identified: FDA approval processes
- User data point: 67% implementation delay rate

## Major Trends
### 1. Regulatory Tightening
The [FDA increased AI oversight by 340%](https://fda.gov/ai-oversight-2024) in 2024
according to their latest report. This aligns with user-provided insights about
[regulatory compliance challenges affecting implementation timelines](processed/materials_insights.md).
```

#### Agent 2: art-audience-analyst
**Responsibility**: Target audience psychology and needs
**Output**: `agent_outputs/audience.md`
**Requirements**:
- Minimum 5 core pain points identified
- Detailed demographic and psychographic analysis
- Content consumption patterns documented
- **Citation format**: Inline hyperlinks only `[descriptive text](https://url.com)`
- **Language**: English only
- **Materials Integration**: Leverage user audience insights when available

#### Agent 3: art-competitor-scanner
**Responsibility**: Competitive landscape analysis
**Output**: `agent_outputs/competitors.md`
**Requirements**:
- Minimum 5 competitor analyses
- Minimum 3 significant content gaps identified
- Differentiation opportunities mapped
- **Citation format**: Inline hyperlinks only `[descriptive text](https://url.com)`
- **Language**: English only
- **Materials Integration**: Consider user competitive intelligence

#### Agent 4: art-topic-explorer
**Responsibility**: Deep topic exploration and expert perspectives
**Output**: `agent_outputs/topic.md`
**Requirements**:
- Minimum 10 subtopics explored
- Minimum 5 expert opinions gathered
- Comprehensive topic coverage achieved
- **Citation format**: Inline hyperlinks only `[descriptive text](https://url.com)`
- **Language**: English only
- **Materials Integration**: Build on user expert knowledge and insights

### Quality Checkpoints
After all 4 agents complete:
- ✅ All research files exist and are complete
- ✅ Minimum requirements met for each file
- ✅ Citation format compliance: all sources use inline hyperlinks
- ✅ Language compliance: all content in English
- ✅ User materials integration: insights properly incorporated
- ✅ Cross-reference validation: consistent facts across files

### Success Criteria
- ✅ All 4 research files completed in agent_outputs/
- ✅ Minimum data requirements met (trends: 5+, statistics: 10+, pain points: 5+, etc.)
- ✅ All citations use proper inline hyperlink format
- ✅ User materials insights integrated where available
- ✅ Ready to proceed to Phase 4 (Content Creation)

---

## Phase 4: Content Creation

### Purpose
Transform research into compelling, well-structured article using the article writer agent.

### Execution Strategy
**Single Agent Execution** - art-article-writer processes all research:

#### Input Materials
- `agent_outputs/trends.md` - Market intelligence and statistics
- `agent_outputs/audience.md` - Reader psychology and needs
- `agent_outputs/competitors.md` - Differentiation opportunities
- `agent_outputs/topic.md` - Expert insights and comprehensive coverage
- `processed/materials_insights.md` - User insights and unique perspectives (if available)
- `strategy/strategy_v1.0.md` - Content positioning
- `strategy/voice_guide.md` - Voice and style requirements
- `metadata.json` - Article specifications

#### Writing Requirements
**Structure Standards**:
- Compelling title optimized for target audience
- Engaging introduction with hook (statistic or insight)
- 3-5 main sections with clear subheadings
- Logical flow from problem to solution
- Strong conclusion with actionable takeaways

**Content Standards**:
- **Word count**: 2000 ±10% (1800-2200 acceptable)
- **Data integration**: Minimum 10 statistics with inline hyperlinks
- **Expert insights**: 3-5 expert perspectives included
- **Voice consistency**: ≥90% alignment with voice guide
- **Citation format**: All sources use inline hyperlinks `[descriptive text](https://url.com)`
- **Language**: English only, professional American English standard
- **User materials integration**: Incorporate unique insights from processed/materials_insights.md

**Citation Integration Examples**:
```markdown
When [MIT researchers discovered](https://mit.edu/ai-study-2024) that 82% of medical AI tools fail,
it sent shockwaves through the industry. This finding aligns with [user-provided case study data](processed/materials_insights.md)
showing similar failure rates in real-world implementations.

The stakes are enormous. The AI healthcare market reached [$21.1 billion in 2024](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-healthcare-market)
according to Grand View Research, with [McKinsey projecting 45% annual growth](https://www.mckinsey.com/industries/healthcare/our-insights/transforming-healthcare-with-ai)
through 2028.
```

#### Output Specifications
**File**: `drafts/v1_draft.md`
**Format**: Complete article with:
- Title and subtitle
- Introduction with compelling hook
- Main content sections
- Conclusion with clear takeaways
- All sources properly cited with inline hyperlinks
- User insights seamlessly integrated

### Quality Checkpoints
- ✅ Word count within target range (1800-2200)
- ✅ All structural elements present
- ✅ Minimum 10 statistics integrated with inline citations
- ✅ Voice guide compliance verified
- ✅ Citation format compliance: no reference lists, only inline hyperlinks
- ✅ English language standard maintained
- ✅ User materials insights effectively integrated

### Success Criteria
- ✅ Complete article draft created
- ✅ All content requirements met
- ✅ Research properly integrated with inline citations
- ✅ User materials insights seamlessly incorporated
- ✅ Ready to proceed to Phase 5 (Quality Review)

---

## Phase 5: Quality Review

### Purpose
Comprehensive quality assessment using parallel fact-checking and quality scoring agents.

### Execution Strategy
**Parallel Agent Execution** - Both quality agents run simultaneously:

#### Agent 1: art-fact-checker
**Responsibility**: Factual accuracy and source verification
**Input**: `drafts/v1_draft.md` + agent_outputs files + processed/materials_insights.md for cross-reference
**Output**: `reports/fact_check.md`

**Verification Standards**:
- **100% Accuracy Requirement**: All verifiable claims must be accurate
- **Source Verification**: All citations checked for credibility and currency
- **Cross-reference Check**: Claims validated against research sources and user materials
- **Citation Format Verification**: Confirm all sources use inline hyperlinks
- **Pass/Fail Determination**: Required for proceeding to next phase

#### Agent 2: art-quality-scorer
**Responsibility**: Multi-dimensional quality assessment
**Input**: `drafts/v1_draft.md` + strategy documents + processed/materials_insights.md
**Output**: `reports/quality_score.md`

**Scoring Dimensions** (100 points total):
- **Content Excellence** (25 points): Research integration, structure, insights
- **Strategic Alignment** (25 points): Voice compliance, audience fit, positioning
- **Engagement Factor** (25 points): Hook effectiveness, readability, CTA quality
- **Technical Quality** (15 points): Grammar, formatting, citation quality
- **Innovation** (10 points): Unique perspective, competitive differentiation

### Human Decision Point
After both reports complete, human review required:

**Decision Options**:
1. **Approve** - Proceed to Phase 7 (Visual Production)
2. **Minor Revisions** - Small fixes, then proceed
3. **Major Revisions** - Return to Phase 4 (Rewriting)
4. **Research Issues** - Return to Phase 3B (Additional Research)

### Success Criteria
- ✅ Fact-check: PASS status (no critical errors)
- ✅ Quality score: ≥70/100 minimum
- ✅ Citation compliance: 100% inline hyperlink format
- ✅ User materials integration assessment completed
- ✅ Human approval to proceed
- ✅ Ready for Phase 6 (Revision) or Phase 7 (Visual Production)

---

## Phase 6: Revision Cycle

### Purpose
Human-in-loop revision process based on quality review feedback.

### Trigger Conditions
- Quality review identifies improvement opportunities
- Human reviewer requests changes
- Fact-check requires corrections

### Revision Process

**Step 1: Review Analysis**
- Read both quality reports thoroughly
- Identify priority improvements (high/medium/low impact)
- Determine revision scope (minor fixes vs major rewrite)

**Step 2: Revision Execution**
Based on scope:

**Minor Revisions** (direct editing):
- Fix factual errors identified in fact-check
- Correct citation format issues
- Adjust word count if significantly off target
- Improve specific sections flagged in quality review

**Major Revisions** (re-run art-article-writer):
- Provide specific guidance based on quality feedback
- Include targeted improvements for low-scoring dimensions
- Maintain citation format requirements
- Preserve user materials integration
- Update draft version (v2_draft.md, v3_draft.md, etc.)

**Step 3: Re-evaluation**
- Re-run quality review agents if major changes made
- Verify citation format compliance maintained
- Confirm improvements address identified issues

### Citation Format During Revisions
**CRITICAL**: All revisions must maintain inline hyperlink format:
- ✅ Preserve existing inline citations: `[descriptive text](https://url.com)`
- ✅ Convert any accidentally created footnotes to inline format
- ❌ Never add reference lists or bibliography sections
- ❌ Never use footnote numbering systems

### Success Criteria
- ✅ All identified issues addressed
- ✅ Citation format compliance maintained (100% inline hyperlinks)
- ✅ Quality improvements implemented
- ✅ User materials integration preserved
- ✅ Human approval for final version
- ✅ Ready to proceed to Phase 7 (Visual Production)

---

## Phase 7: Visual Production

### Purpose
Create comprehensive visual asset specifications and AI generation prompts.

### Execution Strategy
**Single Agent**: art-visual-designer

#### Input Requirements
- `drafts/final.md` - Approved article content
- Article metadata for context

#### Visual Requirements
**Hero Image**:
- Concept aligned with article theme
- Professional, eye-catching design
- Optimized for all 3 platforms
- Complete AI generation prompt

**Supporting Images** (minimum 2):
- Illustrate key concepts from article
- Break up text for better readability
- Platform-appropriate specifications
- Complete AI generation prompts

**Platform Specifications**:
- **Medium**: 1200×630px hero, 800×400px supporting
- **Substack**: 1200×600px hero, 600×300px supporting
- **ElevenReader**: Platform-specific requirements

#### Output Specifications
**File**: `visuals/visual_production_guide.md`
**Contents**:
- Hero image concept and detailed prompt
- Supporting image concepts and prompts
- Platform-specific size requirements
- Style guidelines and consistency notes
- Alternative concept suggestions

### Human Task
After guide completion:
1. Review visual concepts for brand alignment
2. Generate images using provided AI prompts
3. Save images in `visuals/images/` folder
4. Verify platform size requirements met

### Success Criteria
- ✅ Visual production guide completed
- ✅ All required images conceptualized
- ✅ Platform specifications included
- ✅ AI prompts ready for generation
- ✅ Ready to proceed to Phase 8 (Platform Optimization)

---

## Phase 8: Platform Optimization

### Purpose
Create platform-specific versions optimized for each target platform while maintaining citation format.

### Execution Strategy
**Single Agent**: art-platform-optimizer

#### Input Requirements
- `drafts/final.md` - Approved article content
- `strategy/PLATFORM_OPTIMIZATION_STRATEGY.md` - Platform guidelines
- `visuals/visual_production_guide.md` - Image specifications
- `strategy/voice_guide.md` - Brand consistency requirements

#### Platform Optimization Requirements

**Medium Version** (`published/medium.md`):
- SEO-optimized title and subtitle
- Scannable format with clear subheadings
- Strategic bold text and blockquotes
- 7-12 minute read length optimal
- **Citation format**: Inline hyperlinks optimized for Medium

**Substack Version** (`published/substack.md`):
- Newsletter format with personal touch
- Email-friendly line breaks and formatting
- Community-building elements
- Subject line optimization
- **Citation format**: Email-compatible inline links

**ElevenReader Version** (`published/elevenreader.md`):
- Reader-centric discovery optimization
- Community engagement elements
- Platform-native formatting
- **Citation format**: Platform-optimized inline hyperlinks

#### Citation Format Consistency
**CRITICAL REQUIREMENT**: All platform versions must maintain inline hyperlink format across all versions.

### Quality Standards
**Platform Compliance**:
- ✅ 100% platform policy compliance
- ✅ Optimal formatting for each platform
- ✅ SEO optimization appropriate to platform
- ✅ Visual content placement optimized

**Citation Format Standards**:
- ✅ All sources maintain inline hyperlink format across platforms
- ✅ No reference lists in any version
- ✅ Descriptive link text preserved
- ✅ Platform-specific link optimization applied

### Success Criteria
- ✅ All 3 platform versions completed
- ✅ Platform-specific optimization applied
- ✅ Citation format compliance maintained (100% inline hyperlinks)
- ✅ Brand voice consistency across versions
- ✅ Ready to proceed to Phase 9 (Publishing)

---

## Phase 9: Publishing

### Purpose
Deploy content to all target platforms and update tracking systems.

### Manual Publishing Process
Each platform requires manual publishing with platform-specific steps:

**Medium Publishing**:
1. Login to Medium account
2. Create new story
3. Copy content from `published/medium.md`
4. Upload hero image and supporting images
5. Add tags: Technology, Healthcare, AI (platform appropriate)
6. Set publication settings
7. Publish article
8. Copy URL for tracking

**Substack Publishing**:
1. Login to Substack dashboard
2. Create new post
3. Copy content from `published/substack.md`
4. Upload images with proper alt-text
5. Preview email version
6. Schedule or publish immediately
7. Copy URL for tracking

**ElevenReader Publishing**:
1. Login to ElevenReader platform
2. Create new article
3. Copy content from `published/elevenreader.md`
4. Upload optimized images
5. Set community tags and categories
6. Publish article
7. Copy URL for tracking

### Registry Update
After all platforms published, update registry.json:
```json
{
  "current_work": {
    "article_id": null,  // Clear current work
    "status": "none",
    "phase": "none"
  },
  "statistics": {
    "articles_completed": "+1",  // Increment
    "total_words": "+article_word_count",
    "avg_quality_score": "recalculate"
  },
  "articles": {
    "20250120_140000_ai_medical_risks": {
      "status": "published",
      "completion_date": "ISO_DATE",
      "user_materials_used": true,
      "platforms": {
        "medium": {
          "published": true,
          "url": "https://medium.com/@author/article-url",
          "publish_date": "ISO_DATE"
        },
        "substack": {
          "published": true,
          "url": "https://newsletter.substack.com/p/article-url",
          "publish_date": "ISO_DATE"
        },
        "elevenreader": {
          "published": true,
          "url": "https://elevenreader.com/articles/article-url",
          "publish_date": "ISO_DATE"
        }
      },
      "final_stats": {
        "word_count": 2150,
        "quality_score": 87,
        "fact_check_status": "PASS",
        "citation_compliance": "100% inline hyperlinks",
        "user_materials_integration": "successfully_integrated"
      }
    }
  }
}
```

### Success Criteria
- ✅ Article published on all 3 platforms
- ✅ All URLs recorded for tracking
- ✅ Registry completely updated
- ✅ Statistics incremented
- ✅ User materials usage tracked
- ✅ Ready for new article creation

---

## Complete Timeline

### Estimated Time Investment
```yaml
Phase 0 (System Init): 15 minutes (one-time)
Phase 1 (Brainstorming): 60-90 minutes (per article type)
Phase 2 (Article Init): 5 minutes
Phase 3A (User Materials): 20-30 minutes (if materials provided)
Phase 3B (Research): 45-60 minutes (parallel agents)
Phase 4 (Writing): 30-45 minutes
Phase 5 (Quality Review): 20-30 minutes (parallel)
Phase 6 (Revision): 15-60 minutes (varies by scope)
Phase 7 (Visual): 20-30 minutes + human image generation
Phase 8 (Platform Optimization): 30-45 minutes
Phase 9 (Publishing): 30-45 minutes manual work

Total per article: 4-7 hours (including human tasks and user materials)
```

### Parallel Processing Opportunities
- **User Materials + Research**: Materials processing can overlap with research prep
- **Research Phase**: All 4 agents run simultaneously
- **Quality Review**: Fact-checker and quality scorer run simultaneously
- **Image Generation**: Can be done during optimization phase
- **Multiple Articles**: Research can overlap between articles

---

## Agent Specifications

### Research Agents (Phase 3B)

#### art-trend-researcher
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5-20241022

Responsibilities:
  - Research current market trends
  - Identify emerging patterns
  - Collect relevant statistics
  - Analyze trend impacts
  - Integrate user materials insights

Requirements:
  - Minimum 5 trends identified
  - Minimum 10 statistics with inline hyperlink citations
  - Data recency within 12 months
  - Citation format: [descriptive text](https://url.com) only
  - Language: English only
  - Check processed/materials_insights.md for user perspectives

Output:
  - agent_outputs/trends.md with comprehensive trend analysis
  - All sources cited with inline hyperlinks
  - User insights integrated where relevant
```

#### art-audience-analyst
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch
Model: claude-haiku-3-5-20241022

Responsibilities:
  - Profile target audience
  - Identify pain points and needs
  - Map content preferences
  - Analyze engagement patterns
  - Incorporate user audience insights

Requirements:
  - Minimum 5 pain points identified
  - Detailed demographic analysis
  - Behavioral pattern documentation
  - Citation format: [descriptive text](https://url.com) only
  - Language: English only
  - Reference processed/materials_insights.md for user audience data

Output:
  - agent_outputs/audience.md with comprehensive audience analysis
  - All research cited with inline hyperlinks
  - User insights on audience behavior integrated
```

#### art-competitor-scanner
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5-20241022

Responsibilities:
  - Analyze competitive landscape
  - Identify content gaps
  - Map differentiation opportunities
  - Assess competitive positioning
  - Consider user competitive intelligence

Requirements:
  - Minimum 5 competitor analyses
  - Minimum 3 content gaps identified
  - Differentiation strategy recommendations
  - Citation format: [descriptive text](https://url.com) only
  - Language: English only
  - Integrate user competitive insights from processed/materials_insights.md

Output:
  - agent_outputs/competitors.md with competitive analysis
  - All sources cited with inline hyperlinks
  - User competitive intelligence incorporated
```

#### art-topic-explorer
```yaml
Type: Research Agent
Tools: Read, Write, WebSearch, WebFetch
Model: claude-haiku-3-5-20241022

Responsibilities:
  - Deep dive topic exploration
  - Gather expert perspectives
  - Map subtopic relationships
  - Comprehensive coverage analysis
  - Build on user expert knowledge

Requirements:
  - Minimum 10 subtopics explored
  - Minimum 5 expert perspectives
  - Comprehensive topic coverage
  - Citation format: [descriptive text](https://url.com) only
  - Language: English only
  - Reference processed/materials_insights.md for user expert insights

Output:
  - agent_outputs/topic.md with comprehensive topic analysis
  - All expert sources cited with inline hyperlinks
  - User expert knowledge and insights integrated
```

### Content Creation Agent

#### art-article-writer
```yaml
Type: Content Agent
Tools: Read, Write
Model: claude-sonnet-4-20250514

Responsibilities:
  - Transform research into article
  - Maintain voice consistency
  - Integrate data strategically
  - Create compelling narrative
  - Seamlessly incorporate user materials insights

Requirements:
  - Word count: 2000 ±10%
  - Structure: Title, intro, 3+ sections, conclusion
  - Data integration: Minimum 10 statistics with inline citations
  - Voice consistency: ≥90% match to guide
  - Citation format: [descriptive text](https://url.com) only
  - Language: English only
  - User materials integration: Incorporate processed/materials_insights.md

Input Requirements:
  - All agent_outputs files (trends, audience, competitors, topic)
  - processed/materials_insights.md (if available)
  - Strategy documents (strategy, voice guide)
  - Article metadata

Output:
  - drafts/v1_draft.md with complete article
  - All sources cited with inline hyperlinks
  - User insights seamlessly integrated
```

### Quality Review Agents

#### art-fact-checker
```yaml
Type: Quality Agent
Tools: Read, Write, WebSearch
Model: claude-haiku-3-5-20241022

Responsibilities:
  - Verify all factual claims
  - Check data accuracy
  - Validate sources
  - Identify logical inconsistencies
  - Confirm citation format compliance
  - Cross-reference with user materials

Requirements:
  - 100% accuracy standard
  - Source credibility verification
  - Pass/fail determination
  - Citation format verification: inline hyperlinks only
  - User materials cross-reference for validation

Input Requirements:
  - Article draft
  - agent_outputs files for cross-reference
  - processed/materials_insights.md for additional validation

Output:
  - reports/fact_check.md with detailed verification report
  - Pass/fail status with specific issues
  - Citation format compliance assessment
  - User materials validation status
```

#### art-quality-scorer
```yaml
Type: Quality Agent
Tools: Read, Write
Model: claude-sonnet-4-20250514

Responsibilities:
  - Multi-dimensional quality assessment
  - Voice alignment evaluation
  - Engagement potential scoring
  - Technical quality review
  - User materials integration assessment

Scoring Dimensions:
  - Content Excellence (25 points)
  - Strategic Alignment (25 points)
  - Engagement Factor (25 points)
  - Technical Quality (15 points)
  - Innovation (10 points)

Requirements:
  - Minimum score: 70/100 for pass
  - Citation format assessment included
  - Specific improvement recommendations
  - User materials integration evaluation

Output:
  - reports/quality_score.md with dimensional breakdown
  - Improvement recommendations prioritized
  - Citation format compliance evaluation
  - User materials integration assessment
```

---

## File Specifications

### Updated Naming Conventions
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
  - materials_insights.md (user materials analysis)

Images:
  - hero.jpg (main image)
  - support{n}.jpg (supporting)
  - platform_{name}.jpg (specific)
```

### Required Folder Structure (Updated)
```
{article_type}/
├── strategy/
│   ├── strategy_v*.md
│   ├── voice_guide.md
│   └── PLATFORM_OPTIMIZATION_STRATEGY.md
├── README.md
└── content/
    └── {timestamp}_{slug}/
        ├── metadata.json
        ├── user_materials/     # NEW: User drop zone
        ├── processed/          # NEW: Analyzed user content
        │   └── materials_insights.md
        ├── agent_outputs/      # NEW: System research (replaces research/)
        │   ├── trends.md
        │   ├── audience.md
        │   ├── competitors.md
        │   └── topic.md
        ├── drafts/
        │   ├── v1_draft.md
        │   ├── v2_draft.md (if revised)
        │   └── final.md
        ├── reports/
        │   ├── fact_check.md
        │   ├── quality_score.md
        │   └── review_summary.md
        ├── visuals/
        │   ├── visual_production_guide.md
        │   └── images/
        │       ├── hero.jpg
        │       └── support*.jpg
        └── published/
            ├── medium.md
            ├── substack.md
            └── elevenreader.md
```

---

## Version History

- v1.0 (2025-01-18): Initial workflow documentation
- v2.0 (2025-01-19): Complete master document with technical specifications
- v2.1 (2025-09-20): Inline Citation Format Requirements Added
- v3.0 (2025-09-21): **User Materials Integration System Added** - 3-folder structure (user_materials/, processed/, agent_outputs/), materials-processor agent, priority system, backward compatibility maintained
- Created by: NOVELSYS-SWARM System
- Status: Active Production Document with User Materials Integration

---

## Related Documentation

- **Technical Architecture** → [ARTICLE_SYSTEM_ARCHITECTURE.md](ARTICLE_SYSTEM_ARCHITECTURE.md)
- **Quality Standards** → [ARTICLE_IO_STANDARDS.md](ARTICLE_IO_STANDARDS.md)
- **Platform Optimization** → [PLATFORM_OPTIMIZATION_STRATEGY.md](PLATFORM_OPTIMIZATION_STRATEGY.md)
- **System Overview** → [README.md](README.md)

---

*This is the authoritative source for Article production workflow with mandatory inline hyperlink citation format and user materials integration. All agents and commands must reference this document for operational procedures, technical specifications, and citation requirements.*