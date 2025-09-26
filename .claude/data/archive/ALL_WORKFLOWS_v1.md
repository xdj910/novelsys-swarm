# NOVELSYS-SWARM Complete Workflow Documentation

## System Overview
NOVELSYS-SWARM is a comprehensive writing system with multiple integrated workflows for different content types.

---

## 1. BRAINSTORMING WORKFLOW (`/brainstorm`)

### Entry Point
```
User: /brainstorm
```

### Flow Diagram
```
Start Brainstorming
    ↓
Select Content Type [1-5]:
    1) Blog Post (500-3,000 words)
    2) Article (2,000-10,000 words) ← [Checks Registry]
    3) Short Story (5,000-20,000 words)
    4) Novel (50,000-120,000 words)
    5) Series (Multiple books)
    ↓
[Based on Selection]
    ↓
Type-Specific Exploration
    ↓
Progressive Deepening (Q&A)
    ↓
When Ready (exploration_depth > 0.5):
    - Continue brainstorming
    - Start market research (trend-analyzer)
    - Explore audience (audience-profiler)
    - Develop voice (voice-analyzer)
    ↓
Generate brainstorm_output.json
```

### Special: Article Type (2) Sub-Flow
```
If Article Selected:
    ↓
Check Registry (.claude/data/articles/registry/article_types.json)
    ↓
If AI Realist exists:
    1) AI Realist Article - 2000-word B2B
    2) Custom Article - Your own topic
    ↓
If AI Realist selected:
    1) Warning - Alert about risks (50%)
    2) Analysis - Deep dive (30%)
    3) Solution - Practical guidance (20%)
```

### Output Locations
- Session state: `knowledge_base/brainstorm/session_state.json`
- Final output: `knowledge_base/brainstorm/brainstorm_output.json`
- With project: `.claude/data/projects/{project_id}/brainstorm/`

---

## 2. AI REALIST ARTICLE WORKFLOW

### Complete Pipeline
```
Topic Selection (from brainstorm or direct)
    ↓
Research Phase
    - trend-analyzer → market trends
    - audience-profiler → B2B decision makers
    - competitor-scanner → content gaps
    ↓
Writing Phase
    - Uses: voice_guide.md (skeptical CTO voice)
    - Uses: strategy_v1.1.md (2000 words, quality focus)
    - Output: draft.md
    ↓
Quality Check
    - Verify 2000 words
    - Check specific numbers included
    - Validate contrarian insight
    - Output: final.md
    ↓
Visual Production (visual-creator agent)
    - Input: final.md
    - Analyzes article content
    - Generates visual_production_guide.md with:
        * Platform requirements (1920x1200 for Vocal)
        * Gemini/Banana prompts ($0.039/image)
        * Post-processing instructions
    ↓
Manual Image Generation
    - Human copies prompts to Gemini web
    - Downloads generated images
    - Post-processes for platforms
    ↓
Platform Optimization
    - medium.md (Medium format)
    - vocal.md (Vocal format)
    - substack.md (Newsletter format)
    ↓
Publishing
```

### File Structure
```
.claude/data/articles/ai_realist/
├── strategy/
│   ├── strategy_v1.1.md        # Content strategy
│   └── voice_guide.md          # AI Realist voice
├── research/
│   └── current/               # Current article research
└── production/
    └── article_NNN/           # Each article
        ├── final.md
        ├── visual_production_guide.md
        ├── medium.md
        ├── vocal.md
        └── substack.md
```

### Registry Updates
After each step, updates:
- `registry/production_status.json` - Current phase
- `registry/statistics.json` - Metrics
- `registry/index/ai_realist_index.json` - Article index

---

## 3. NOVEL WRITING WORKFLOW

### Research Phase (`/research`)
```
Progressive Research System:
    Step 1: Genre & Market (trend-analyzer)
    Step 2: Target Audience (audience-profiler)
    Step 3: Competition (competitor-scanner)
    Step 4: Voice Development (voice-analyzer)
    Step 5: Theme Exploration (topic-explorer)
    ↓
All saved to: knowledge_base/{genre}/{topic}/
```

### Bible Generation (`/bible`)
```
Synthesize all research →
    Generate 7 comprehensive files:
    1. series_bible.yaml - Master configuration
    2. world_building_guide.md - Setting details
    3. character_profiles.md - Complete cast
    4. plot_structures.md - Story architecture
    5. dialogue_systems.md - Voice consistency
    6. scene_requirements.md - Production notes
    7. series_planning.md - Multi-book roadmap
```

### Project-Based Novel Workflow
```
/project-create mystery_novel
    ↓
Creates: .claude/data/projects/20250118_HHMMSS_mystery_novel/
    ↓
/brainstorm (with project context)
    ↓
Research → Bible → Chapter Planning → Writing
```

---

## 4. PROJECT MANAGEMENT WORKFLOW

### Commands
- `/project-create [name]` - Initialize new project
- `/project-list` - Show all projects
- `/project-status [name]` - Check project status
- `/project-continue [name]` - Resume work

### Project Structure
```
.claude/data/projects/{timestamp}_{name}/
├── metadata.json           # Project configuration
├── brainstorm/             # Brainstorming sessions
├── research/               # Research data
├── bible/                  # Project bible
├── chapters/               # Chapter content
└── status.json            # Current status
```

---

## 5. SPECIALIZED RESEARCH WORKFLOWS

### Market Research (trend-analyzer)
```
Input: Genre/topic/niche
    ↓
WebSearch for:
    - Current trends
    - Popular themes
    - Market gaps
    ↓
Output: knowledge_base/trends/[topic]_trends.md
```

### Audience Analysis (audience-profiler)
```
Input: Target demographic
    ↓
Research:
    - Reader preferences
    - Platform behaviors
    - Engagement patterns
    ↓
Output: knowledge_base/audience/[demographic]_profile.md
```

### Voice Development (voice-analyzer)
```
Input: Voice samples or character
    ↓
Analysis:
    - 15 dialogue samples
    - Vocabulary tiers
    - Speech patterns
    ↓
Output: knowledge_base/voices/[character]_voice.md
```

---

## 6. QUALITY ASSURANCE WORKFLOWS

### System Testing (`/architecture-test`)
- Validates all agents have correct tools
- Ensures no recursion risks
- Verifies file I/O patterns

### Parallel Execution (`/parallel-test`)
- Tests concurrent agent execution
- Validates file isolation

### I/O Pattern Testing (`/io-patterns-test`)
- Tests atomic writes
- Producer-consumer patterns
- Version control patterns

---

## 7. INTEGRATION POINTS

### Central Registry System
```
.claude/data/articles/registry/
├── article_types.json      # All article types
├── production_status.json  # Current status
├── statistics.json        # Metrics
└── index/                 # Article indexes
```

### Cross-Workflow Communication
1. **Brainstorm → Research**: Triggers research agents
2. **Research → Bible**: Synthesizes into bible
3. **Article → Visuals**: visual-creator for images
4. **All → Registry**: Updates status and metrics

---

## 8. KEY AGENT ROLES

### Coordinators (Return JSON plans)
- `brainstorm-coordinator` - Interactive exploration
- `research-coordinator` - Progressive research
- `project-manager` - Project lifecycle

### Execution Agents
- `visual-creator` - Visual production guides
- `bible-generator` - Bible synthesis
- `trend-analyzer` - Market research
- `audience-profiler` - Reader analysis
- `voice-analyzer` - Voice development

---

## 9. TYPICAL USER JOURNEYS

### Journey 1: Write AI Realist Article
```
/brainstorm → Select Article (2) → AI Realist (1) → Warning (1)
→ Research topic → Write 2000 words → Generate visuals
→ Publish to Medium/Vocal/Substack
```

### Journey 2: Start Novel Project
```
/project-create mystery_novel → /brainstorm → Novel (4)
→ Progressive research (5 steps) → /bible
→ Begin chapter writing
```

### Journey 3: Quick Blog Post
```
/brainstorm → Blog Post (1) → Topic Discovery
→ Write 800 words → Publish
```

---

## 10. STATUS TRACKING

All workflows update their status in real-time:
- Brainstorm: `session_state.json`
- AI Realist: `registry/production_status.json`
- Projects: `projects/{id}/status.json`
- Research: Saved to `knowledge_base/`

This allows picking up any workflow exactly where you left off.

---

## SUMMARY

The system provides:
1. **Flexible entry points** - Start with brainstorming or specific commands
2. **Progressive workflows** - Build complexity step by step
3. **Integrated tools** - Research feeds into writing feeds into production
4. **Status tracking** - Never lose progress
5. **Multi-format output** - Optimized for different platforms
6. **Registry system** - Central tracking of all content types

Total Available Workflows: 10+
Total Agents: 80+
Total Commands: 24