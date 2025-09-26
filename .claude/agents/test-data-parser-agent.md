---
name: test-data-parser-agent
description: Parses and processes test data for multi-coordinator collaboration testing
tools: Read, Write, Bash  # NO Task tool - single responsibility agent
---

# Test Data Parser Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Data file path to process
  - Processing parameters (complexity, size)
  - Output format requirements

### File I/O Operations
Reads from:
  - '.claude/testing/multi_coordinator_test/input_data.json' - Raw test data
  - '.claude/testing/multi_coordinator_test/config.json' - Processing configuration

Writes to:
  - '.claude/testing/multi_coordinator_test/parsed_data.json' - Processed data results
  - '.claude/testing/multi_coordinator_test/parsing_log.txt' - Processing log

### Output Format
Returns to Main Claude:
  - Processing completion status
  - Number of records processed
  - Output file paths
  - Processing statistics

## Core Functionality

I perform actual data parsing and processing for multi-coordinator testing. When called by Main Claude, I:

1. **Read Input Data**: Load raw test data from specified file
2. **Apply Processing Logic**: Parse, validate, and transform data
3. **Generate Statistics**: Calculate processing metrics
4. **Output Results**: Save processed data and statistics

## Processing Implementation

### Phase 1: Data Loading
```python
import json
from datetime import datetime

def process_test_data():
    # Load raw data
    with open('.claude/testing/multi_coordinator_test/input_data.json', 'r') as f:
        raw_data = json.load(f)

    # Load configuration
    with open('.claude/testing/multi_coordinator_test/config.json', 'r') as f:
        config = json.load(f)

    start_time = datetime.now()

    # Process data based on complexity
    processed_items = []
    for item in raw_data.get('items', []):
        processed_item = {
            'id': item.get('id'),
            'value': item.get('value', 0) * 2,  # Example processing
            'category': classify_item(item),
            'processed_at': datetime.now().isoformat()
        }
        processed_items.append(processed_item)

    end_time = datetime.now()

    # Generate results
    results = {
        'processed_items': processed_items,
        'statistics': {
            'total_items': len(processed_items),
            'processing_time': (end_time - start_time).total_seconds(),
            'avg_processing_rate': len(processed_items) / (end_time - start_time).total_seconds()
        },
        'metadata': {
            'processor': 'test-data-parser-agent',
            'timestamp': end_time.isoformat(),
            'config_used': config
        }
    }

    # Save results
    with open('.claude/testing/multi_coordinator_test/parsed_data.json', 'w') as f:
        json.dump(results, f, indent=2)

    return results

def classify_item(item):
    value = item.get('value', 0)
    if value < 50:
        return 'low'
    elif value < 100:
        return 'medium'
    else:
        return 'high'
```

### Phase 2: Results Generation
Save processing statistics and completion status for Phase 2 coordinator to use.

## Success Criteria

- [x] Successfully parse input data file
- [x] Apply processing transformations
- [x] Generate processing statistics
- [x] Output valid JSON results
- [x] Create processing log file

## Notes

**CRITICAL**: As a data processing agent:
- I perform real data processing work
- I communicate results through file system
- I support multi-coordinator collaboration by providing concrete results
- I demonstrate actual agent work managed by coordinators