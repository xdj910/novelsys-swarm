# Claude Code Knowledge Base Cache Mechanism

## Overview

This document describes the caching mechanism for the Claude Code knowledge base system.

## Cache Implementation

### 1. Cache Validity Check

```python
# Pseudocode for cache validation
def is_cache_valid(document_path, max_age_hours=24):
    """Check if a cached document is still valid"""
    
    # Read index.json
    index = read_json(".claude/knowledge/index.json")
    
    # Check if document exists in index
    if document_path not in index["documents"]:
        return False
    
    # Get fetch timestamp
    fetched_str = index["documents"][document_path]["fetched"]
    fetched_time = parse_iso_timestamp(fetched_str)
    
    # Calculate age
    current_time = datetime.now(UTC)
    age = current_time - fetched_time
    
    # Check if within validity period
    return age.total_seconds() < (max_age_hours * 3600)
```

### 2. Fetch Decision Logic

```python
def should_fetch_document(doc_info, force_update=False):
    """Determine if a document should be fetched"""
    
    if force_update:
        return True
    
    doc_path = doc_info["path"]
    
    # Check if file exists
    if not file_exists(f".claude/knowledge/{doc_path}"):
        return True
    
    # Check cache validity
    if not is_cache_valid(doc_path):
        return True
    
    return False
```

### 3. Document Fetching Process

```python
def fetch_and_cache_document(doc_info):
    """Fetch a document and update cache"""
    
    # Fetch content
    content = WebFetch(doc_info["url"], 
                      "Extract complete documentation content")
    
    # Save to file
    file_path = f".claude/knowledge/{doc_info['path']}"
    write_file(file_path, content)
    
    # Update index
    update_index_entry(doc_info["path"], {
        "url": doc_info["url"],
        "fetched": datetime.now(UTC).isoformat(),
        "size": len(content),
        "hash": calculate_md5(content)
    })
    
    return True
```

## Cache Strategy

### 24-Hour Default Cache

- Documents are cached for 24 hours by default
- Configurable via `cache_validity_hours` in index.json
- Timestamp in ISO 8601 format for consistency

### Force Update Scenarios

1. **User Request**: `claude knowledge-base-init --force`
2. **Missing Document**: File doesn't exist locally
3. **Corrupt Cache**: Hash mismatch detected
4. **Manual Override**: Delete index.json to force full refresh

### Incremental Updates

- Only expired documents are fetched
- Valid cached documents are preserved
- Minimizes API calls and bandwidth

## File Structure

```
.claude/knowledge/
+-- index.json                    # Cache metadata and timestamps
+-- official-specs/               
|   +-- sub-agents.md            # Cached document
|   +-- commands.md              # Cached document
|   +-- [timestamp].backup/      # Backup of previous versions
+-- patterns/                     # Future: Best practices
+-- antipatterns/                # Future: Common mistakes
```

## Index.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["last_update", "cache_validity_hours", "documents"],
  "properties": {
    "last_update": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of last update"
    },
    "cache_validity_hours": {
      "type": "number",
      "minimum": 1,
      "maximum": 168,
      "default": 24,
      "description": "Hours before cache expires"
    },
    "documents": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["url", "fetched", "size"],
        "properties": {
          "url": {"type": "string", "format": "uri"},
          "fetched": {"type": "string", "format": "date-time"},
          "size": {"type": "integer", "minimum": 0},
          "hash": {"type": "string"},
          "version": {"type": "string"}
        }
      }
    }
  }
}
```

## Integration with Claude Code Expert

The claude-code-expert agent should:

1. **Check Cache First**:
   ```python
   if is_cache_valid(requested_doc):
       return read_cached_document(requested_doc)
   ```

2. **Trigger Update if Needed**:
   ```python
   if not is_cache_valid(requested_doc):
       Task("knowledge-base-manager", 
            "Fetch and cache document",
            f"Update {requested_doc}")
   ```

3. **Use Cached Content**:
   ```python
   content = read_file(f".claude/knowledge/{doc_path}")
   return analyze_documentation(content)
   ```

## Best Practices

### 1. Atomic Operations
- Write to `.tmp` file first
- Rename to final location
- Update index.json last

### 2. Error Recovery
- Keep previous version on fetch failure
- Validate content before saving
- Log errors for debugging

### 3. Performance Optimization
- Check cache before any fetch
- Batch multiple document fetches
- Use async operations where possible

### 4. Storage Management
- Compress old versions
- Limit backup history
- Monitor disk usage

## Command Line Usage

### Initialize/Update Knowledge Base
```bash
# Update expired documents only
claude knowledge-base-init

# Force update all documents
claude knowledge-base-init --force

# Update specific document
claude knowledge-base-init sub-agents

# Check cache status
claude knowledge-base-init --status
```

## Implementation Checklist

- [x] Create index.json schema
- [x] Design cache validation logic
- [x] Create knowledge-base-manager agent
- [x] Create knowledge-base-init command
- [ ] Implement actual fetching (requires system execution)
- [ ] Add backup mechanism
- [ ] Implement compression for old versions
- [ ] Add cache statistics reporting

## Future Enhancements

1. **ETag Support**: Check if document changed on server
2. **Differential Updates**: Fetch only changed sections
3. **Parallel Fetching**: Fetch multiple documents simultaneously
4. **Auto-refresh**: Background updates for frequently used docs
5. **Search Index**: Full-text search across all cached documents

---
*Cache Mechanism v1.0 - Ensuring fast and reliable access to Claude Code documentation*