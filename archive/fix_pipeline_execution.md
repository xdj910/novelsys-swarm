# Pipeline Execution Fix

## 🔴 问题诊断

### 症状：
- 应该执行10个步骤，实际只执行了3个（Step 1, 2, 10）
- 缺失步骤3-9的所有版本文件
- 最终质量96分，但缺少了70%的增强处理

### 根本原因：
1. **Coordinator执行中断或跳跃**
2. **缺少强制验证机制**
3. **Step 10可能有未记录的容错行为**

## 🛠️ 修复方案

### Fix 1: 增强Coordinator文档的执行强制性

在chapter-start-coordinator.md的第197行后添加：

```markdown
### ⚠️ MANDATORY EXECUTION REQUIREMENTS

**YOU MUST EXECUTE ALL 10 STEPS IN SEQUENCE. DO NOT SKIP ANY STEPS.**

1. Execute Step 1 → Verify v01 exists → Continue
2. Execute Step 2 → Verify v02 exists → Continue
3. Execute Step 3 → Verify v03 exists → Continue
4. Execute Step 4 → Verify v04 exists → Continue
5. Execute Step 5 → Verify v05 exists → Continue
6. Execute Step 6 → Verify v06 exists → Continue
7. Execute Step 7 → Verify v07 exists → Continue
8. Check genre → Execute Step 8 if applicable → Verify v08 if executed
9. Execute Step 9 → Verify v09 exists → Continue
10. Execute Step 10 → Verify v10 exists → Complete

**CRITICAL**: If ANY step fails to produce its output file:
- STOP immediately
- Report the failure
- DO NOT continue to next steps
- DO NOT skip to Step 10
```

### Fix 2: 添加执行检查点

在每个Step后添加强制验证：

```markdown
#### Mandatory Checkpoint After Step 3:
```bash
# MUST EXECUTE - DO NOT SKIP
if [ ! -f ".claude/data/projects/{project}/book_{book}/chapters/ch{NNN}/versions/v03_world_clues.md" ]; then
    echo "❌ CRITICAL: Step 3 failed - v03_world_clues.md not created"
    echo "❌ PIPELINE HALTED - Cannot continue without v03"
    exit 1
fi
echo "✅ Step 3 verified - v03_world_clues.md exists"
```
```

### Fix 3: 修复author-voice-signature-specialist

确保它只接受v09作为输入：

```markdown
### STEP 1: VERIFICATION

1. **Read Previous Version** (CRITICAL - NO FALLBACK)
   - **MUST READ**: `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/versions/v09_humanized.md`
   - **CRITICAL**: If v09_humanized.md does NOT exist:
     * ERROR: "❌ Cannot proceed: v09_humanized.md is missing"
     * EXIT immediately
     * DO NOT use any other version file
   - This is your ONLY valid input file
   - NO FALLBACK to earlier versions permitted
```

### Fix 4: 添加Pipeline状态跟踪

创建状态文件记录执行：

```markdown
#### Pipeline Status Tracking:
Create `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/pipeline_status.json`:

```json
{
  "chapter": 1,
  "pipeline_started": "2025-09-11T12:31:00Z",
  "steps": {
    "step_1": {"status": "completed", "file": "v01_initial_draft.md", "time": "12:32:00"},
    "step_2": {"status": "completed", "file": "v02_dialogue_character.md", "time": "12:33:00"},
    "step_3": {"status": "pending", "file": "v03_world_clues.md", "time": null},
    // ... etc
  },
  "current_step": 3,
  "errors": []
}
```
```

### Fix 5: 创建验证脚本

```bash
#!/bin/bash
# verify_pipeline.sh

PROJECT="$1"
BOOK="$2"
CHAPTER="$3"

VERSIONS_DIR=".claude/data/projects/${PROJECT}/book_${BOOK}/chapters/ch$(printf "%03d" $CHAPTER)/versions"

echo "🔍 Verifying pipeline execution for Chapter ${CHAPTER}..."

EXPECTED_FILES=(
    "v01_initial_draft.md"
    "v02_dialogue_character.md"
    "v03_world_clues.md"
    "v04_continuity_checked.md"
    "v05_emotions_woven.md"
    "v06_prose_polished.md"
    "v07_foreshadowing_added.md"
    "v08_genre_enhanced.md"  # May be optional
    "v09_humanized.md"
    "v10_voice_signature.md"
)

MISSING=0
for FILE in "${EXPECTED_FILES[@]}"; do
    if [ ! -f "${VERSIONS_DIR}/${FILE}" ]; then
        echo "❌ Missing: ${FILE}"
        MISSING=$((MISSING + 1))
    else
        echo "✅ Found: ${FILE}"
    fi
done

if [ $MISSING -gt 0 ]; then
    echo "❌ Pipeline incomplete: ${MISSING} files missing"
    exit 1
else
    echo "✅ Pipeline complete: All files present"
fi
```

## 🚀 实施步骤

1. **立即修复coordinator文档** - 添加强制执行要求
2. **修复author-voice-signature** - 禁止fallback
3. **添加验证检查点** - 每步后验证
4. **创建状态跟踪** - 记录执行进度
5. **测试修复** - 重新运行chapter 2生成

## 📊 成功标准

- 所有10个版本文件都生成
- 没有步骤被跳过
- 清晰的错误报告（如果失败）
- 可追踪的执行日志

## 🔧 长期改进

1. **创建integration test** - 测试完整pipeline
2. **添加telemetry** - 记录每步执行时间
3. **创建recovery机制** - 从中断点恢复
4. **优化并行执行** - 某些步骤可以并行