# Blog Posts

## Overview
Quick-publish content for blogs and social media (500-3,000 words).

## Structure
```
blog_posts/
├── README.md            # This file
├── strategy/           # Publishing strategy
│   └── platforms.md    # Target platforms and schedule
└── posts/              # Individual blog posts
    └── {timestamp}_{slug}/
        ├── metadata.json
        ├── draft.md
        └── published.md
```

## Workflow
1. Quick brainstorm or direct write
2. Draft in `posts/{timestamp}/draft.md`
3. Light review
4. Publish to platforms
5. Archive in `published.md`

## Characteristics
- **Speed**: Same-day publish possible
- **Tone**: Casual, conversational
- **Research**: Minimal required
- **Images**: 1-2 simple images
- **Platforms**: Dev.to, Medium, personal blog

## Creating a Blog Post
```
/brainstorm → Blog Post → Topic
OR
Direct write to posts/{timestamp}/
```

## Registry Integration
All posts tracked in `/data/registry/index/blog_posts_index.json`