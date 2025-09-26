# NOVELSYS-SWARM Data Directory

## Overview
Centralized data storage for all content types in the NOVELSYS-SWARM writing system.

## Directory Structure
```
.claude/data/
├── README.md                 # This file
├── registry.json            # Central registry for all article types and tracking
│
├── blog_posts/              # Type 1: Blog Posts
├── articles/                # Type 2: Articles
├── short_stories/          # Type 3: Short Stories
├── novels/                 # Type 4: Novels
├── series/                 # Type 5: Series
└── projects/               # Project management (separate system)
```

## Content Types

### 1. Blog Posts (500-3,000 words)
- **Purpose**: Quick thoughts, tips, updates
- **Location**: `blog_posts/`
- **Structure**: Lightweight, timestamp-based

### 2. Articles (2,000-10,000 words)
- **Purpose**: In-depth analysis, tutorials
- **Location**: `articles/`
- **Example**: AI Realist series
- **Structure**: Strategy-driven, multi-platform

### 3. Short Stories (5,000-20,000 words)
- **Purpose**: Complete narratives
- **Location**: `short_stories/`
- **Structure**: Concept + drafts

### 4. Novels (50,000-120,000 words)
- **Purpose**: Full-length books
- **Location**: `novels/`
- **Structure**: Bible + chapters

### 5. Series (Multiple books)
- **Purpose**: Connected stories
- **Location**: `series/`
- **Structure**: Series bible + individual books

## Common Structure Pattern

All content types follow this pattern:
```
{content_type}/
├── README.md                # Type documentation
├── {specific_content}/      # Individual items
│   ├── README.md           # Item documentation
│   ├── {strategy_layer}/   # strategy/bible/concept
│   └── {content_layer}/    # posts/articles/chapters
```

### Naming Conventions
- **Strategy Layer**:
  - Blog/Article → `strategy/`
  - Story → `concept/`
  - Novel/Series → `bible/`

- **Content Layer**:
  - Blog → `posts/`
  - Article → `articles/`
  - Story/Novel → `drafts/` or `chapters/`
  - Series → `books/`

## Registry System

The `registry.json` file provides centralized tracking for articles:

- **Article type definitions** - All registered types and configurations
- **Current work status** - Active articles in progress
- **Statistics tracking** - Historical production metrics
- **Brainstorming status** - Setup completion for each type

Note: Only articles use the registry system currently. Other content types have individual tracking methods.

## Workflow Integration

### Entry Points
1. **Brainstorming**: `/brainstorm` → Checks registry → Routes to type
2. **Direct Creation**: Type-specific commands
3. **Project Management**: Via `projects/` system

### Status Flow
```
Planning → Researching → Writing → Reviewing → Publishing
```

Each phase updates the registry automatically.

## Adding New Content Types

To add a new content type:

1. Create directory: `{content_type}/`
2. Add `{content_type}/README.md`
3. Define strategy layer
4. Register in `registry/content_types.json`
5. Update this README

## Core Commands

### Available Commands
- `/brainstorm` - Start any content type (interactive brainstorming)
- `/continue` - Continue most recent work

### Testing Commands
- `/architecture-test` - Validate system architecture
- `/parallel-test` - Test parallel execution
- `/human-in-loop-test` - Test human interaction workflow
- `/multi-coordinator-test` - Test multi-coordinator collaboration
- `/python-pipeline-test` - Test Python pipeline

## Available Research Agents

- **Market Research**: `trend-analyzer`, `competitor-scanner`, `topic-explorer`
- **Audience Research**: `audience-profiler`
- **Content Development**: `voice-analyzer`, `visual-creator`

## Production Phases

All content progresses through:
1. `planning` - Initial concept
2. `researching` - Gathering information
3. `drafting` - Writing content
4. `reviewing` - Quality check
5. `visual_production` - Image creation (if needed)
6. `publishing` - Platform optimization
7. `published` - Complete

## Best Practices

1. **Always start with strategy** - Define direction before content
2. **Use timestamps** - `{timestamp}_{slug}` for uniqueness
3. **Update registry** - Track all status changes
4. **Document everything** - README at each level

## Quick Navigation

### Article System
- **Article workflow?** → [articles/ARTICLE_WORKFLOW.md](articles/ARTICLE_WORKFLOW.md)
- **Platform optimization?** → [articles/PLATFORM_OPTIMIZATION_STRATEGY.md](articles/PLATFORM_OPTIMIZATION_STRATEGY.md)
- **Registry system?** → [articles/registry.json](articles/registry.json)
- **Working on AI Realist?** → [articles/ai_realist/](articles/ai_realist/)

### Other Content Types
- **Starting a novel?** → [novels/README.md](novels/README.md)
- **Checking article status?** → [articles/registry.json](articles/registry.json)
- **Managing projects?** → [projects/](projects/)

---

*System Version: 3.2 | Updated: 2025-01-18 | Status: Active*