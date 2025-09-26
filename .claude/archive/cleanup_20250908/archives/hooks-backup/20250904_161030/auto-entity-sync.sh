#!/bin/bash

# PostToolUse Hook: Auto Entity Dictionary synchronization
# 自动检测章节中的实体引用，同步到Entity Dictionary

# 设置项目根目录 (根据Claude Code官方文档)
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
    echo "[WARNING] CLAUDE_PROJECT_DIR not set, using fallback: $PROJECT_ROOT" >&2
else
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
fi

# 确保日志目录存在
mkdir -p "$PROJECT_ROOT/.claude/logs"

# 从stdin读取Claude Code提供的JSON输入
input=$(cat)

# 使用jq解析JSON输入
tool_name=$(echo "$input" | jq -r '.tool_name // .tool // .name // empty' 2>/dev/null)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .file_path // .path // empty' 2>/dev/null)

# Fallback到grep
[[ -z "$tool_name" ]] && tool_name=$(echo "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)
[[ -z "$file_path" ]] && file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 2>/dev/null)

# Convert Windows paths to Unix paths for compatibility
unix_path=$(echo "$file_path" | sed 's|\\|/|g' | sed 's|^D:|/d|' | sed 's|^C:|/c|')

# 检查是否是章节内容写入操作
if [[ "$tool_name" == "Write" || "$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
    
    if ([[ "$file_path" == */content.md ]] || [[ "$file_path" == *\\content.md ]]) && ([[ "$file_path" == */chapters/ch*/content.md ]] || [[ "$file_path" == *\\chapters\\ch*\\content.md ]]); then
        
        if [[ -f "$unix_path" ]]; then
            
            chapter_dir=$(dirname "$unix_path")
            chapter_num=$(basename "$chapter_dir" | sed 's/ch0*//')
            
            # 查找Entity Dictionary文件
            entity_dict=""
            
            # 搜索可能的Entity Dictionary位置
            for dict_path in \
                "$PROJECT_ROOT/.claude/data/projects/*/entity_dictionary.yaml" \
                "$PROJECT_ROOT/entity_dictionary.yaml" \
                "$PROJECT_ROOT/config/entity_dictionary.yaml" \
                "$PROJECT_ROOT/.claude/entity_dictionary.yaml"
            do
                if [[ -f "$dict_path" ]]; then
                    entity_dict="$dict_path"
                    break
                fi
            done
            
            # 如果找不到Entity Dictionary，创建基础版本
            if [[ -z "$entity_dict" ]]; then
                entity_dict="$PROJECT_ROOT/.claude/entity_dictionary.yaml"
                
                cat > "$entity_dict" << 'EOF'
# NOVELSYS-SWARM Entity Dictionary
# Auto-generated and maintained by entity sync Hook

characters:
  # Main characters will be detected and added here
  
locations:
  # Locations mentioned in chapters will be tracked here
  
objects:
  # Important objects and items will be catalogued here
  
concepts:
  # Abstract concepts and terminology will be indexed here

# Metadata
metadata:
  created_by: "auto-entity-sync Hook"
  last_updated: ""
  total_entities: 0
  chapters_scanned: []
EOF
                echo "📚 Created new Entity Dictionary at $(basename "$entity_dict")"
            fi
            
            # 实体检测模式
            detected_entities=()
            new_entities=()
            
            # 1. 检测人名 (常见中文人名模式)
            # 检测形如"张三"、"李小明"等人名
            while IFS= read -r name; do
                if [[ -n "$name" && ${#name} -ge 2 && ${#name} -le 4 ]]; then
                    detected_entities+=("character:$name")
                fi
            done < <(grep -oP '[\\u4e00-\\u9fff]{2,4}(?=说|道|想|看|走|来|去|的)' "$unix_path" 2>/dev/null | sort -u)
            
            # 2. 检测地点 (带有地点标识词的实体)
            while IFS= read -r location; do
                if [[ -n "$location" ]]; then
                    location_clean=$(echo "$location" | sed 's/[店房屋楼院馆场所]$//')
                    if [[ -n "$location_clean" && ${#location_clean} -ge 2 ]]; then
                        detected_entities+=("location:$location_clean")
                    fi
                fi
            done < <(grep -oP '[\\u4e00-\\u9fff]{2,8}[店房屋楼院馆场所]' "$unix_path" 2>/dev/null | sort -u)
            
            # 3. 检测物品 (引号内的物品名称)
            while IFS= read -r item; do
                if [[ -n "$item" && ${#item} -ge 2 && ${#item} -le 10 ]]; then
                    detected_entities+=("object:$item")
                fi
            done < <(grep -oP '「[\\u4e00-\\u9fff]{2,10}」' "$unix_path" 2>/dev/null | sed 's/[「」]//g' | sort -u)
            
            # 4. 检测特殊词汇 (大写英文或专有名词)
            while IFS= read -r term; do
                if [[ -n "$term" && ${#term} -ge 3 ]]; then
                    detected_entities+=("concept:$term")
                fi
            done < <(grep -oP '[A-Z][a-zA-Z]{2,}' "$unix_path" 2>/dev/null | sort -u)
            
            # 处理检测到的实体
            if [[ ${#detected_entities[@]} -gt 0 ]]; then
                
                # 读取现有Entity Dictionary
                existing_entities=()
                
                if [[ -f "$entity_dict" ]]; then
                    # 提取已存在的实体 (简化版解析)
                    while IFS= read -r line; do
                        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name:[[:space:]]*(.+)$ ]]; then
                            existing_entities+=("${BASH_REMATCH[1]}")
                        elif [[ "$line" =~ ^[[:space:]]*([\\u4e00-\\u9fff\\w]+):[[:space:]]*$ ]]; then
                            current_category="${BASH_REMATCH[1]}"
                        fi
                    done < "$entity_dict"
                fi
                
                # 识别新实体
                for entity in "${detected_entities[@]}"; do
                    entity_type="${entity%%:*}"
                    entity_name="${entity#*:}"
                    
                    # 检查是否已存在
                    entity_exists=false
                    for existing in "${existing_entities[@]}"; do
                        if [[ "$existing" == "$entity_name" ]]; then
                            entity_exists=true
                            break
                        fi
                    done
                    
                    if [[ "$entity_exists" == "false" ]]; then
                        new_entities+=("$entity")
                    fi
                done
                
                # 如果有新实体，更新Entity Dictionary
                if [[ ${#new_entities[@]} -gt 0 ]]; then
                    
                    # 创建临时文件进行更新
                    temp_dict="$entity_dict.tmp"
                    cp "$entity_dict" "$temp_dict"
                    
                    # 按类型添加新实体
                    current_time=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')
                    
                    for entity in "${new_entities[@]}"; do
                        entity_type="${entity%%:*}"
                        entity_name="${entity#*:}"
                        
                        case "$entity_type" in
                            "character")
                                # 添加到characters部分
                                if grep -q "^characters:" "$temp_dict"; then
                                    sed -i "/^characters:/a\\  - name: \"$entity_name\"\\n    first_appeared: \"ch$chapter_num\"\\n    auto_detected: true\\n    status: \"needs_review\"" "$temp_dict"
                                fi
                                ;;
                            "location") 
                                # 添加到locations部分
                                if grep -q "^locations:" "$temp_dict"; then
                                    sed -i "/^locations:/a\\  - name: \"$entity_name\"\\n    first_mentioned: \"ch$chapter_num\"\\n    auto_detected: true\\n    type: \"unknown\"" "$temp_dict"
                                fi
                                ;;
                            "object")
                                # 添加到objects部分
                                if grep -q "^objects:" "$temp_dict"; then
                                    sed -i "/^objects:/a\\  - name: \"$entity_name\"\\n    first_mentioned: \"ch$chapter_num\"\\n    auto_detected: true\\n    significance: \"unknown\"" "$temp_dict"
                                fi
                                ;;
                            "concept")
                                # 添加到concepts部分
                                if grep -q "^concepts:" "$temp_dict"; then
                                    sed -i "/^concepts:/a\\  - name: \"$entity_name\"\\n    first_used: \"ch$chapter_num\"\\n    auto_detected: true\\n    definition: \"needs_definition\"" "$temp_dict"
                                fi
                                ;;
                        esac
                    done
                    
                    # 更新metadata
                    if grep -q "last_updated:" "$temp_dict"; then
                        sed -i "s/last_updated:.*/last_updated: \"$current_time\"/" "$temp_dict"
                    fi
                    
                    # 添加当前章节到scanned列表
                    if grep -q "chapters_scanned:" "$temp_dict"; then
                        if ! grep -q "ch$chapter_num" "$temp_dict"; then
                            sed -i "/chapters_scanned:/a\\    - \"ch$chapter_num\"" "$temp_dict"
                        fi
                    fi
                    
                    # 应用更新
                    mv "$temp_dict" "$entity_dict"
                    
                    # 记录同步操作
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Entity sync for ch$chapter_num: added ${#new_entities[@]} new entities" >> "$PROJECT_ROOT/.claude/logs/entity-sync.log"
                    
                    for entity in "${new_entities[@]}"; do
                        echo "  + $entity" >> "$PROJECT_ROOT/.claude/logs/entity-sync.log"
                    done
                    
                    # 用户提示
                    echo "📚 Entity Dictionary updated: +${#new_entities[@]} entities from Chapter $chapter_num"
                    
                    # 显示新实体 (限制输出)
                    if [[ ${#new_entities[@]} -le 3 ]]; then
                        for entity in "${new_entities[@]}"; do
                            entity_type="${entity%%:*}"
                            entity_name="${entity#*:}"
                            echo "  ✓ $entity_type: $entity_name"
                        done
                    else
                        entity_type1="${new_entities[0]%%:*}"
                        entity_name1="${new_entities[0]#*:}"
                        echo "  ✓ $entity_type1: $entity_name1"
                        echo "  ✓ ... and $((${#new_entities[@]} - 1)) more (review needed)"
                    fi
                    
                else
                    # 没有新实体，只记录扫描
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Entity sync for ch$chapter_num: no new entities found" >> "$PROJECT_ROOT/.claude/logs/entity-sync.log"
                fi
                
            else
                # 没有检测到实体
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Entity detection for ch$chapter_num: no entities detected" >> "$PROJECT_ROOT/.claude/logs/entity-sync.log"
            fi
            
        fi
    fi
fi

# 成功退出
exit 0