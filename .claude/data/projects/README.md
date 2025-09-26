# Projects Directory

## Overview
Standalone project management system for complex writing projects that don't fit the standard content types.

## Purpose
While the main content types (blog_posts, articles, short_stories, novels, series) have their dedicated structures, the projects system handles:
- Cross-type projects
- Experimental formats
- Client projects
- Special collaborations

## Structure
```
projects/
├── README.md              # This file
├── index.json            # Project index
└── {timestamp}_{name}/   # Individual projects
    ├── project.json      # Project metadata
    ├── brainstorm/       # Brainstorming sessions
    ├── research/         # Research materials
    ├── bible/           # Project documentation
    ├── drafts/          # Work in progress
    └── notes/           # Miscellaneous notes
```

## Integration
Projects can be created via:
- `/project-create [name]`
- Through brainstorming when selecting custom options

## Relationship to Content Types
- **Complementary**: Projects system works alongside content types
- **Flexible**: Can combine multiple content types
- **Experimental**: For formats not yet standardized

## When to Use Projects vs Content Types

### Use Content Types When:
- Writing standard blog posts
- Creating article series (like AI Realist)
- Writing short stories, novels, or series
- Following established workflows

### Use Projects When:
- Combining multiple content types
- Experimenting with new formats
- Managing client work
- Need custom structure

## Status Tracking
Projects tracked separately in:
- `index.json` - Local project index
- Can optionally register in main registry

---

*Note: This is the legacy project system. Consider using the unified content types when possible.*