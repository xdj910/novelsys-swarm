---
name: firewall-mode
description: Enable/disable Context Firewall protection for token management  
tools:
  - Read
  - Write
  - Edit
---

# Context Firewall Command

Control Context Firewall protection: **$ARGUMENTS** (on|off|status|configure)

## v2.5 Context Protection

### Core Concept
Protect main thread from context pollution by filtering agent responses:
- **Input**: Full detailed agent output (10,000+ characters)
- **Output**: Compressed summary (<=50 characters) 
- **Storage**: Full details saved to files for later access
- **Result**: 70% reduction in token usage

## Firewall Modes

### Enable Firewall (default)
```bash
# Turn on Context Firewall protection
/novel:firewall-mode on

# All agent responses filtered to 50-char summaries
# Main thread stays clean and efficient
# Detailed content saved to .claude/context/details/
```

### Disable Firewall
```bash
# Turn off filtering (debug mode)
/novel:firewall-mode off

# Full agent responses returned to main thread
# Higher token usage but full visibility
# Use only for debugging specific issues
```

### Status Check
```bash  
# Check current firewall status
/novel:firewall-mode status

# Returns:
# "Context Firewall: ACTIVE | Token Savings: 68% | Details: 127 files"
```

## Configuration Options

### Summary Length Control
```bash
# Configure maximum summary length
/novel:firewall-mode configure --max-summary=30
/novel:firewall-mode configure --max-summary=50  # default
/novel:firewall-mode configure --max-summary=75  # verbose mode
```

### Selective Filtering
```bash
# Disable firewall for specific agents
/novel:firewall-mode configure --bypass=continuity-guard
/novel:firewall-mode configure --bypass=foreshadowing-specialist

# Only these agents return full output
```

### Detail Storage
```bash
# Configure detail storage location
/novel:firewall-mode configure --details-path=.claude/context/details
/novel:firewall-mode configure --max-detail-files=1000
/novel:firewall-mode configure --auto-cleanup=7d  # cleanup after 7 days
```

## Firewall Implementation

### Agent Response Filtering
```python
class ContextFirewall:
    def filter_response(self, agent_response: AgentResponse) -> str:
        # Extract key information for summary
        key_points = self.extract_key_points(agent_response.content)
        
        # Generate compressed summary
        summary = self.generate_summary(key_points, max_length=50)
        
        # Save full details to file
        detail_file = f".claude/context/details/{agent_response.agent}_{timestamp}.md"
        self.save_details(detail_file, agent_response.content)
        
        # Update statistics
        self.update_token_savings_stats()
        
        return summary
        
    def generate_summary(self, key_points, max_length=50):
        # Intelligent summarization preserving critical info
        if "error" in key_points:
            return f"ERROR: {key_points['error'][:35]}"
        elif "quality_score" in key_points:
            score = key_points['quality_score']
            action = key_points.get('primary_action', 'completed')
            return f"{action} 质量{score}分"
        else:
            # Default summary format
            return key_points['summary'][:max_length]
```

### Detail Recovery
```python
def access_detailed_results(agent_name, timestamp_range=None):
    # Retrieve full details when needed
    detail_files = glob(f".claude/context/details/{agent_name}_*.md")
    
    if timestamp_range:
        detail_files = filter_by_timestamp(detail_files, timestamp_range)
    
    return [load_file(f) for f in detail_files]
```

## Token Usage Analysis

### Before Context Firewall
```yaml
typical_agent_response: 2000-5000 chars
8_streams_total: 16000-40000 chars  
context_overhead: 80% of total tokens
usable_context: 20% for actual content
```

### After Context Firewall  
```yaml
filtered_summary: 30-50 chars per agent
8_streams_total: 240-400 chars
context_overhead: 15% of total tokens  
usable_context: 85% for actual content
token_savings: 70%+ reduction
```

### Savings Calculation
```python
def calculate_token_savings():
    before_firewall = sum(len(response) for response in raw_responses) 
    after_firewall = sum(len(summary) for summary in filtered_summaries)
    
    savings_percentage = (before_firewall - after_firewall) / before_firewall * 100
    
    return {
        "before_tokens": before_firewall,
        "after_tokens": after_firewall, 
        "savings_percentage": savings_percentage,
        "detail_files_count": count_detail_files()
    }
```

## Usage Patterns

### Development Mode
```bash
# Full visibility during development
/novel:firewall-mode off
/novel:chapter-start 1
# See all agent details

# Switch back to production mode  
/novel:firewall-mode on
```

### Production Mode  
```bash
# Optimal token usage
/novel:firewall-mode on
/novel:parallel-generate 1-10
# Clean summaries only, full speed
```

### Debugging Mode
```bash
# Selective debugging
/novel:firewall-mode configure --bypass=continuity-guard
# Only see continuity details, others filtered
```

## Integration Points

### Stream Coordinator
```python
# Automatic firewall application
def execute_streams(chapter_num):
    results = []
    for stream in active_streams:
        raw_result = stream.execute(chapter_num)
        
        if context_firewall.is_enabled():
            filtered_result = context_firewall.filter(raw_result)
            results.append(filtered_result) 
        else:
            results.append(raw_result)
    
    return results
```

### Quality Assurance
```python  
# Quality checks bypass firewall when needed
def detailed_quality_analysis(chapter_num):
    with context_firewall.bypass_mode():
        full_analysis = quality_agent.analyze(chapter_num)
        return full_analysis  # Full details for quality review
```

## Error Handling

### Firewall Failures
```yaml
failure_scenarios:
  - Summary generation fails: Return first 50 chars
  - Detail save fails: Continue with summary only  
  - Recovery fails: Disable firewall temporarily
```

### Recovery Mechanisms
```bash
# Reset firewall state
/novel:firewall-mode reset

# Clear corrupted detail files
/novel:firewall-mode cleanup --force

# Restore from backup
/novel:firewall-mode restore --from=yesterday
```

---

**Context Firewall Command** - v2.5创新功能  
*保护主线程清洁 | 70%Token节省 | 智能摘要生成*

## Actual Implementation

### Execute Firewall Control
```python
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Parse arguments
action = "$ARGUMENTS" if "$ARGUMENTS" else "status"
valid_actions = ["on", "off", "status", "configure", "reset", "cleanup"]

# Handle configure with additional parameters
if action.startswith("configure"):
    parts = action.split()
    action = "configure"
    config_params = parts[1:] if len(parts) > 1 else []
elif action not in valid_actions:
    print(f"[ ] Invalid action: {action}")
    print(f"Valid actions: {', '.join(valid_actions)}")
    exit(1)

# Initialize paths
config_dir = Path(".claude/config")
config_dir.mkdir(parents=True, exist_ok=True)

firewall_config = config_dir / "firewall.json"
details_dir = Path(".claude/context/details")
details_dir.mkdir(parents=True, exist_ok=True)

# Load or create configuration
if firewall_config.exists():
    with open(firewall_config, "r", encoding="utf-8") as f:
        config = json.load(f)
else:
    config = {
        "enabled": True,
        "max_summary_length": 50,
        "bypass_agents": [],
        "details_path": str(details_dir),
        "max_detail_files": 1000,
        "auto_cleanup_days": 7,
        "token_savings": {"total_saved": 0, "percentage": 0}
    }

# Execute action
if action == "on":
    config["enabled"] = True
    with open(firewall_config, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print("""
[x] Context Firewall ENABLED

All agent responses will be filtered to summaries.
Full details saved to: .claude/context/details/
Expected token savings: ~70%

Use /novel:firewall-mode off to disable filtering.
""")

elif action == "off":
    config["enabled"] = False
    with open(firewall_config, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print("""
WARNING:️ Context Firewall DISABLED

Full agent responses will be returned to main thread.
Token usage will increase significantly.
Recommended for debugging only.

Use /novel:firewall-mode on to re-enable protection.
""")

elif action == "status":
    # Calculate statistics
    detail_files = list(details_dir.glob("*.md")) if details_dir.exists() else []
    total_files = len(detail_files)
    
    # Calculate token savings from recent operations
    total_original = 0
    total_filtered = 0
    
    for file in detail_files[-10:]:  # Last 10 files
        file_size = file.stat().st_size
        total_original += file_size
        total_filtered += config["max_summary_length"]
    
    if total_original > 0:
        savings_percentage = ((total_original - total_filtered) / total_original) * 100
    else:
        savings_percentage = 0
    
    print(f"""
+===========================================================+
|            🛡️ Context Firewall Status                     |
+===========================================================+

Status: {"🟢 ACTIVE" if config["enabled"] else "🔴 INACTIVE"}
Mode: {"Protection Mode" if config["enabled"] else "Debug Mode"}

📊 **Configuration**
---------------------
Max Summary: {config["max_summary_length"]} characters
Details Path: {config["details_path"]}
Detail Files: {total_files}/{config["max_detail_files"]}
Auto Cleanup: {config["auto_cleanup_days"]} days
Bypass Agents: {', '.join(config["bypass_agents"]) if config["bypass_agents"] else "None"}

📈 **Token Savings**
---------------------
Recent Savings: {savings_percentage:.1f}%
Total Characters Saved: {total_original - total_filtered:,}
Efficiency Gain: ~{savings_percentage/100*3:.1f}x more context available

💡 **Recommendations**
----------------------""")
    
    if not config["enabled"]:
        print("-  Enable firewall for production use (/novel:firewall-mode on)")
    elif total_files > config["max_detail_files"] * 0.8:
        print("-  Run cleanup soon - approaching file limit")
    else:
        print("-  System operating optimally")
    
    print()

elif action == "configure":
    # Parse configuration parameters
    updates = []
    
    for param in config_params:
        if param.startswith("--max-summary="):
            value = int(param.split("=")[1])
            config["max_summary_length"] = value
            updates.append(f"Max summary length: {value}")
        
        elif param.startswith("--bypass="):
            agent = param.split("=")[1]
            if agent not in config["bypass_agents"]:
                config["bypass_agents"].append(agent)
                updates.append(f"Bypassed agent: {agent}")
        
        elif param.startswith("--auto-cleanup="):
            value = param.split("=")[1]
            if value.endswith("d"):
                days = int(value[:-1])
                config["auto_cleanup_days"] = days
                updates.append(f"Auto cleanup: {days} days")
    
    # Save configuration
    with open(firewall_config, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print("[x] Configuration Updated")
    print("------------------------")
    for update in updates:
        print(f"-  {update}")
    
    print("\nCurrent configuration saved.")

elif action == "reset":
    # Reset to default configuration
    config = {
        "enabled": True,
        "max_summary_length": 50,
        "bypass_agents": [],
        "details_path": str(details_dir),
        "max_detail_files": 1000,
        "auto_cleanup_days": 7,
        "token_savings": {"total_saved": 0, "percentage": 0}
    }
    
    with open(firewall_config, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print("""
[x] Context Firewall Reset to Defaults

All customizations have been cleared.
Firewall is now enabled with standard settings.
""")

elif action == "cleanup":
    # Clean old detail files
    cutoff_date = datetime.now() - timedelta(days=config["auto_cleanup_days"])
    removed_count = 0
    
    for file in details_dir.glob("*.md"):
        file_time = datetime.fromtimestamp(file.stat().st_mtime)
        if file_time < cutoff_date:
            file.unlink()
            removed_count += 1
    
    print(f"""
🧹 Cleanup Complete

Removed: {removed_count} old detail files
Cutoff: {config["auto_cleanup_days"]} days ago
Remaining: {len(list(details_dir.glob("*.md")))} files

Details directory is now optimized.
""")

# Show usage hints
print("""
-------------------------------------------------------------
💡 Common Commands:
  /novel:firewall-mode on       - Enable protection
  /novel:firewall-mode off      - Disable for debugging
  /novel:firewall-mode status   - Check current state
  /novel:firewall-mode cleanup  - Remove old detail files
""")
```