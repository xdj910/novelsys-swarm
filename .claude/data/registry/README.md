# Registry System

## Overview
Central tracking system for all content types in NOVELSYS-SWARM.

## Structure
```
registry/
├── README.md                    # This file
├── content_types.json          # All registered content types
├── production_status.json      # Current work in progress
├── statistics.json            # Global metrics
└── index/                     # Historical records
    ├── blog_posts_index.json
    ├── articles_index.json
    ├── short_stories_index.json
    ├── novels_index.json
    └── series_index.json
```

## Core Files

### content_types.json
Registers all available content types and their configurations:
```json
{
  "blog_posts": {
    "status": "active",
    "word_range": [500, 3000],
    "typical_time": "1-2 days"
  },
  "articles": {
    "subtypes": {
      "ai_realist": { ... }
    }
  },
  ...
}
```

### production_status.json
Tracks all active work:
```json
{
  "blog_posts": {
    "current": null,
    "in_progress": 0
  },
  "articles": {
    "ai_realist": {
      "current_article": { ... }
    }
  },
  ...
}
```

### statistics.json
Global metrics and analytics:
```json
{
  "total_words_written": 0,
  "total_pieces": 0,
  "by_type": { ... },
  "productivity": { ... }
}
```

## Index Files

Each content type has an index tracking all items:

### Format
```json
{
  "type": "blog_posts",
  "items": [
    {
      "id": "20250118_143022_topic",
      "title": "Title",
      "status": "published",
      "word_count": 1500,
      "created": "2025-01-18",
      "path": "blog_posts/posts/20250118_143022_topic/"
    }
  ],
  "total": 0,
  "last_updated": "2025-01-18T10:00:00Z"
}
```

## Registry Operations

### 1. Register New Type
- Add to content_types.json
- Create index file
- Initialize in production_status.json

### 2. Create New Item
- Generate timestamp ID
- Add to appropriate index
- Update production_status

### 3. Update Status
- Modify production_status.json
- Update item in index
- Increment statistics

### 4. Complete Item
- Mark complete in index
- Clear from production_status
- Update statistics

## Integration Points

### With Brainstorm Coordinator
- Reads content_types.json for available types
- Updates production_status on start

### With Content Creation
- Each new item updates index
- Status changes update production_status

### With Commands
- Status commands read production_status
- List commands read indexes

## Best Practices

1. **Atomic Updates**: Use temp files for safety
2. **Timestamp IDs**: Always use for uniqueness
3. **Status Tracking**: Update immediately on changes
4. **Statistics**: Increment on completion only

## Quick Queries

- **What's in progress?** → production_status.json
- **How many articles written?** → articles_index.json
- **What types available?** → content_types.json
- **Global statistics?** → statistics.json

---

*Registry Version: 2.0 | Status: Active*