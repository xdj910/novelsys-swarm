# Chapter-Start Architecture Refactor Design

## Current Architecture Problems

1. **Logical Flaw**: 8 agents try to analyze non-existent chapter content
2. **Coordinator Confusion**: Novel-parallel-coordinator passes chapter number but agents have nothing to read
3. **No Actual Generation**: Agents are configured for analysis, not creation
4. **Pseudo-code Everywhere**: Commands contain non-executable code

## Root Cause Analysis

The system was designed with a fundamental misunderstanding:
- **Intent**: Generate a chapter using specialized agents
- **Implementation**: Agents configured to analyze existing chapters
- **Result**: Agents fail or hallucinate when no content exists

## New Architecture: Sequential Generation Pipeline

### Phase 1: Planning & Outline
```yaml
step_1_outline:
  agent: bible-architect
  input:
    - bible: Full project Bible
    - chapter_num: Target chapter number
    - previous_summary: Summary of previous chapter
    - entity_dictionary: For consistent naming
  output:
    - chapter_outline: Detailed scene-by-scene outline
    - key_beats: Major plot points to hit
    - character_arcs: Character development goals
```

### Phase 2: Initial Draft Generation
```yaml
step_2_draft:
  agent: scene-generator
  input:
    - chapter_outline: From Phase 1
    - bible: Project Bible
    - entity_dictionary: For naming consistency
    - genre: For appropriate conventions
  output:
    - initial_draft: Raw first draft of full chapter
    - scene_boundaries: Marked scene transitions
```

### Phase 3: Character & Dialogue Enhancement
```yaml
step_3_character:
  agents:
    - character-psychologist: Deepen character motivations
    - dialogue-master-specialist: Polish dialogue authenticity
  input:
    - initial_draft: From Phase 2
    - character_states: Current character development
    - relationship_map: Character relationships
  output:
    - enhanced_draft: Draft with improved character work
```

### Phase 4: World & Atmosphere Enhancement
```yaml
step_4_world:
  agent: world-builder
  input:
    - enhanced_draft: From Phase 3
    - world_context: Existing world details
    - location_maps: Setting information
  output:
    - atmospheric_draft: Draft with rich world details
```

### Phase 5: Continuity & Logic Check
```yaml
step_5_continuity:
  agent: continuity-guard-specialist
  input:
    - atmospheric_draft: From Phase 4
    - timeline: Story timeline
    - previous_chapters: For consistency check
    - entity_dictionary: For reference validation
  output:
    - validated_draft: Continuity-checked draft
    - issues_found: List of any continuity problems
```

### Phase 6: Literary Polish
```yaml
step_6_polish:
  agents:
    - prose-craft-specialist: Enhance prose quality
    - emotion-weaver-specialist: Deepen emotional resonance
  input:
    - validated_draft: From Phase 5
    - style_guide: Writing style requirements
  output:
    - polished_draft: Literary quality enhanced
```

### Phase 7: Final Validation
```yaml
step_7_validate:
  agents:
    - plot-hole-detector: Check logic
    - quality-scorer: Score final quality
  input:
    - polished_draft: From Phase 6
    - genre: For genre-aware validation
    - entity_dictionary: For consistency check
  output:
    - final_chapter: Ready for output
    - quality_report: Detailed quality scores
    - issues: Any remaining problems
```

## Implementation Strategy

### 1. Remove Parallel Coordinator
- Archive novel-parallel-coordinator.md
- It serves no purpose in generation

### 2. Rewrite chapter-start.md
- Sequential pipeline instead of parallel
- Each phase builds on previous
- Clear inputs/outputs at each stage

### 3. Update Agent Prompts
- Change from "analyze chapter X" to "generate content for chapter X"
- Provide actual inputs (outline, previous draft, etc.)
- Clear output expectations

### 4. Add Iteration Logic
- If quality < 95, identify weak areas
- Re-run specific phases to improve
- Maximum 3 iterations before accepting

## Benefits of New Architecture

1. **Logical Flow**: Each agent has actual content to work with
2. **Progressive Enhancement**: Chapter improves through pipeline
3. **Clear Responsibilities**: Each agent knows exactly what to do
4. **Measurable Progress**: Can track completion through phases
5. **Targeted Fixes**: Can re-run specific phases if needed

## Migration Path

1. Create new `chapter-generate.md` command with new architecture
2. Test with single chapter generation
3. Compare quality with old system
4. Archive old chapter-start.md once confirmed
5. Update all references to use new command

## Quality Gates

Each phase has exit criteria:
- Phase 1: Outline completeness > 90%
- Phase 2: Draft word count within target
- Phase 3: Character consistency > 95%
- Phase 4: World detail richness > 85%
- Phase 5: Zero critical continuity errors
- Phase 6: Prose quality > 90%
- Phase 7: Overall score > 95%

## Entity Dictionary Integration

- Phase 1: Use for planning character references
- Phase 2: Apply approved variations during generation
- Phase 3: Validate dialogue references
- Phase 5: Check all entity references
- Phase 7: Flag any unrecognized variations

## Estimated Performance

- Old system: Undefined (agents analyze nothing)
- New system: ~7-10 minutes per chapter
- Quality improvement: Measurable at each phase
- Iteration cost: ~2-3 minutes per phase re-run