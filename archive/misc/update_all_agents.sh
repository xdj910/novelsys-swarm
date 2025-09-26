#!/bin/bash

# Update all agents with anti-script instruction
echo "Updating all agents to prevent Python script creation..."

# Get list of agents without the instruction
agents_to_update=$(find .claude/agents -name "*.md" -type f -exec grep -L "DO NOT CREATE PYTHON SCRIPTS" {} \;)

updated_count=0
skipped_count=0

for agent in $agents_to_update; do
    agent_name=$(basename "$agent")
    
    # Skip BASE_AGENT_TEMPLATE and AGENT_SAVE_INSTRUCTION as they are special
    if [[ "$agent_name" == "BASE_AGENT_TEMPLATE.md" ]] || [[ "$agent_name" == "AGENT_SAVE_INSTRUCTION.md" ]]; then
        echo "⏭️  Skipping special file: $agent_name"
        ((skipped_count++))
        continue
    fi
    
    # Check if file has a yaml header (starts with ---)
    if head -1 "$agent" | grep -q "^---"; then
        # Find the end of yaml header and the first heading
        yaml_end_line=$(grep -n "^---$" "$agent" | sed -n '2p' | cut -d: -f1)
        
        if [ -n "$yaml_end_line" ]; then
            # Create temp file with the instruction inserted after yaml header
            temp_file="${agent}.tmp"
            
            # Copy yaml header
            head -n "$yaml_end_line" "$agent" > "$temp_file"
            
            # Add blank line and the instruction
            echo "" >> "$temp_file"
            echo "## CRITICAL: DO NOT CREATE PYTHON SCRIPTS" >> "$temp_file"
            echo "" >> "$temp_file"
            echo "You must DIRECTLY perform your task and save the result." >> "$temp_file"
            echo "DO NOT create Python scripts or any executable files." >> "$temp_file"
            echo "DO NOT use programming languages as an intermediary step." >> "$temp_file"
            echo "Simply read the required files, execute your task, and save the output directly." >> "$temp_file"
            
            # Add the rest of the file
            tail -n +$((yaml_end_line + 1)) "$agent" >> "$temp_file"
            
            # Replace original file
            mv "$temp_file" "$agent"
            
            echo "✅ Updated: $agent_name"
            ((updated_count++))
        else
            echo "⚠️  Could not find yaml end for: $agent_name"
        fi
    else
        # No yaml header, add instruction at the beginning
        temp_file="${agent}.tmp"
        
        echo "## CRITICAL: DO NOT CREATE PYTHON SCRIPTS" > "$temp_file"
        echo "" >> "$temp_file"
        echo "You must DIRECTLY perform your task and save the result." >> "$temp_file"
        echo "DO NOT create Python scripts or any executable files." >> "$temp_file"
        echo "DO NOT use programming languages as an intermediary step." >> "$temp_file"
        echo "Simply read the required files, execute your task, and save the output directly." >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$agent" >> "$temp_file"
        
        mv "$temp_file" "$agent"
        
        echo "✅ Updated (no yaml): $agent_name"
        ((updated_count++))
    fi
done

echo ""
echo "========================================="
echo "Update Complete!"
echo "Updated: $updated_count agents"
echo "Skipped: $skipped_count special files"
echo "========================================="