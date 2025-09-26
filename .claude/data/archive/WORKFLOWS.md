# NOVELSYS-SWARM Workflows Documentation
*Updated: 2025-01-18 - Unified Content Structure*

## System Overview
NOVELSYS-SWARM provides integrated workflows for 5 content types with unified structure.

## Content Type Workflows

### 1. Blog Posts (500-3,000 words)
```
/brainstorm → Blog Post → Topic
→ Quick draft in blog_posts/posts/{timestamp}/
→ Light review → Publish
```

### 2. Articles (2,000-10,000 words)
```
/brainstorm → Article → Check Registry
→ If AI Realist: Choose angle (Warning/Analysis/Solution)
→ Research → Draft → Visual Production → Publish
Location: articles/{series_name}/articles/{timestamp}/
```

### 3. Short Stories (5,000-20,000 words)
```
/brainstorm → Short Story → Genre
→ Concept development → Character building
→ Draft → Revisions → Final
Location: short_stories/{story_name}/
```

### 4. Novels (50,000-120,000 words)
```
/brainstorm → Novel → Genre
→ Progressive research → Bible generation
→ Chapter planning → Progressive writing
Location: novels/{novel_name}/
```

### 5. Series (Multiple books)
```
/brainstorm → Series → Type
→ Series architecture → Master bible
→ Individual book planning
Location: series/{series_name}/
```

## Core Commands

### Content Creation
- `/brainstorm` - Start any content type
- `/research` - Progressive research system
- `/bible` - Generate project bible

### Project Management
- `/project-create [name]` - Create standalone project
- `/project-list` - List all projects
- `/project-status` - Check project status
- `/project-continue` - Resume work

### System Testing
- `/architecture-test` - Validate system architecture
- `/parallel-test` - Test parallel execution
- `/io-patterns-test` - Test I/O patterns

## Data Locations

### Unified Structure
```
.claude/data/
├── registry/           # Central tracking
├── blog_posts/        # Blog content
├── articles/          # Article series
├── short_stories/     # Story projects
├── novels/           # Novel projects
├── series/           # Multi-book series
└── projects/         # Standalone projects
```

### Registry Files
- `registry/content_types.json` - All content types
- `registry/production_status.json` - Current work
- `registry/statistics.json` - Metrics
- `registry/index/*.json` - Content indexes

## Research Agents

### Market Research
- `trend-analyzer` - Market trends and gaps
- `competitor-scanner` - Competition analysis
- `topic-explorer` - Theme discovery

### Audience Research
- `audience-profiler` - Target reader analysis

### Content Development
- `voice-analyzer` - Voice and style development
- `visual-creator` - Image prompt generation

## Workflow Integration Points

### Brainstorming → Content
1. Brainstorm-coordinator checks registry
2. Offers available types/series
3. Routes to appropriate workflow

### Content → Registry
1. Each new item creates timestamp folder
2. Updates production_status.json
3. Updates type index on completion

### Research → Content
Research outputs saved to:
- Articles: `{timestamp}/research/`
- Stories: `{story}/concept/`
- Novels: `{novel}/bible/`

## Quality Standards

### All Content Types Must Have
1. **README.md** - Documentation
2. **Strategy Layer** - Direction/concept/bible
3. **Content Layer** - Actual writing
4. **Registry Entry** - Status tracking

### Naming Conventions
- Timestamp folders: `{YYYYMMDD_HHMMSS}_{slug}`
- Example: `20250118_143022_ai_risks/`

## Status Tracking

### Production Phases
1. `planning` - Initial concept
2. `researching` - Gathering information
3. `drafting` - Writing content
4. `reviewing` - Quality check
5. `visual_production` - Image creation (if needed)
6. `publishing` - Platform optimization
7. `published` - Complete

### Registry Updates
Status changes immediately update:
- `production_status.json` - Current state
- Type index - Historical record
- `statistics.json` - Metrics

## Platform-Specific Notes

### AI Realist Articles
- 2000 words exactly
- Visual production guide via visual-creator
- Manual Gemini image generation
- Platform versions: Medium, Vocal, Substack

### Novel Projects
- Progressive research workflow
- Bible generation with 7 documents
- Chapter-by-chapter tracking

## Archive Location
Legacy files moved to: `.claude/data/archive/`

---

*See also:*
- [Data Structure Overview](.claude/data/README.md)
- [Registry Documentation](.claude/data/registry/README.md)
- [AI Realist Workflow](.claude/data/articles/ai_realist/README.md)