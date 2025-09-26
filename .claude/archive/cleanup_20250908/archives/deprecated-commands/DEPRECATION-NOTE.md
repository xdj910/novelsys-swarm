# Deprecated Commands Archive

## chapter-continue.md
- **Deprecated Date**: 2025-09-04
- **Reason**: Overly complex with unnecessary "resume" logic
- **Replaced By**: `/novel:next-chapter`
- **Migration**: 
  - All references in active commands updated
  - Agent references updated
  - Documentation to be updated separately

## Why Deprecated?

The `chapter-continue` command had complex logic to handle "resuming" partially written chapters. However, in practice:
- Chapters are generated atomically (all or nothing)
- There's no real scenario where a chapter is "half written"
- The complexity added confusion without benefit

## New Simplified Flow

```bash
# Old (complex)
/novel:chapter-continue  # Had to figure out if resuming or starting new

# New (simple)
/novel:next-chapter      # Always starts the next chapter
```