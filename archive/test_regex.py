#!/usr/bin/env python3
import re

# Test the regex patterns
subagent_call = re.compile(r'use\s+the\s+([a-z-]+(?:-coordinator|-specialist)?)\s+subagent', re.IGNORECASE)

test_strings = [
    "Use the system-check-coordinator subagent to orchestrate comprehensive system analysis:",
    "Use the next-chapter-coordinator subagent to generate the next sequential chapter",
    "Use the chapter-start-coordinator subagent to generate chapter",
    "Use the project-new-coordinator subagent to create a new novel project"
]

print("Testing regex patterns:")
for test in test_strings:
    match = subagent_call.search(test)
    if match:
        print(f"[MATCH]: '{test}' -> '{match.group(1)}'")
    else:
        print(f"[NO MATCH]: '{test}'")