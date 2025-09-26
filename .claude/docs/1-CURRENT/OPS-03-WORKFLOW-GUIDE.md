# Universal Writing Workflow v2.0 - Based on 5-Layer Architecture

## Executive Summary

This document defines the standardized writing workflow for multiple content types (articles, short stories, novels, series) following the NOVELSYS-SWARM 5-layer architecture (v6.6 standards). It provides a clear, systematic approach to content creation from initial concept to final output.

## Core Philosophy

### First Principles
1. **Story First** - Technology serves storytelling, not vice versa
2. **Quality Over Quantity** - Better to write one great chapter than ten mediocre ones
3. **Iterative Refinement** - Every chapter can be improved
4. **Consistency Matters** - Characters, world, and style must remain consistent
5. **Reader Experience** - The final judge is reader engagement

### System Goals
- Create engaging, high-quality fiction
- Maintain consistency across long narratives
- Support multiple genres and styles
- Enable rapid iteration and improvement
- Scale from short stories to epic series

## 5-Layer Architecture for Novel System

```
User Layer (Author)
    |
Command Layer (Interface)
    |
Main Claude (Orchestrator)
    |
Coordination Layer (Planning)
    |
Agent Layer (Execution)
    |
=====================================
File System / Data Layer (Persistence)
=====================================
```

### Layer Responsibilities

#### 1. User Layer
- **Role**: Author/Creator providing creative direction
- **Inputs**: Story concepts, chapter requests, quality requirements
- **Decisions**: Creative choices, approval of content

#### 2. Command Layer
- **Components**: 3-5 simple commands
- **Pattern**: `/novel:[action] [parameters]`
- **Focus**: Clear, intuitive interface for common tasks
- **Examples**:
  - `/novel:start` - Begin new novel project
  - `/novel:write` - Create new chapter
  - `/novel:revise` - Improve existing content

#### 3. Main Claude Layer
- **Role**: Central orchestrator with Task tool
- **Responsibilities**:
  - Parse user commands
  - Decide execution strategy
  - Call coordinators for planning
  - Execute agent tasks
  - Manage workflow state

#### 4. Coordination Layer
- **Components**: 2-3 specialized coordinators
- **Tools**: Read, Write, Bash, Grep (NO Task!)
- **Output**: JSON execution plans
- **Examples**:
  - `novel-planning-coordinator` - Plans story structure
  - `chapter-generation-coordinator` - Orchestrates chapter creation
  - `quality-improvement-coordinator` - Plans enhancement workflow

#### 5. Agent Layer
- **Components**: 4-6 focused agents
- **Tools**: Task-specific (NO Task!)
- **Pattern**: Single responsibility per agent
- **Examples**:
  - `bible-creator` - Generates world and character bible
  - `outline-generator` - Creates chapter outlines
  - `content-writer` - Writes actual prose
  - `quality-scorer` - Evaluates content quality

#### 6. Data Layer
- **Structure**: Organized file system
- **Format**: YAML for structured data, Markdown for content
- **Pattern**: Atomic writes, version control
- **Organization**:
  ```
  projects/
    [novel_name]/
      bible.yaml        # Core truth document
      outline.yaml      # Story structure
      chapters/
        001/
          content.md    # Chapter text
          meta.json     # Chapter metadata
          quality.json  # Quality scores
      context/
        characters.yaml # Character development tracking
        world.yaml      # World-building evolution
        plot.yaml       # Plot progression
  ```

## Universal Writing Workflow

### Phase -1: Content Type Detection and Routing

#### Purpose
Intelligently identify the type of content the user wants to create and route to appropriate workflow.

#### Detection Process
```
User Input: "I want to write..."
        |
    Analysis Engine
        |
    Type Detection
        |
+-------+-------+-------+-------+
|       |       |       |       |
Article Story  Novel  Series  Blog
```

#### Type Characteristics Matrix
```yaml
Content_Types:
  article:
    length: 1000-10000 words
    structure: Linear argument
    bible_complexity: Minimal
    quality_focus: Information accuracy
    special_needs: Research, citations

  short_story:
    length: 1000-20000 words
    structure: Single arc
    bible_complexity: Basic
    quality_focus: Impact, payoff
    special_needs: Tight pacing

  novel:
    length: 50000-120000 words
    structure: Multiple arcs
    bible_complexity: Comprehensive
    quality_focus: Character development
    special_needs: Chapter management

  series:
    length: Multiple volumes
    structure: Layered arcs
    bible_complexity: Master + individual
    quality_focus: Continuity
    special_needs: Cross-book tracking

  blog:
    length: 500-3000 words
    structure: Hook-value-CTA
    bible_complexity: Minimal
    quality_focus: Engagement
    special_needs: SEO optimization
```

#### Intelligent Routing Logic
```python
def route_content_type(user_input):
    # Keywords and patterns for detection
    patterns = {
        'article': ['article', 'essay', 'analysis', 'explain'],
        'story': ['story', 'tale', 'narrative', 'short'],
        'novel': ['novel', 'book', 'chapters'],
        'series': ['series', 'trilogy', 'saga', 'books'],
        'blog': ['blog', 'post', 'website']
    }

    # If explicit type mentioned, use it
    detected_type = detect_explicit_type(user_input, patterns)

    # If not explicit, analyze intent
    if not detected_type:
        detected_type = analyze_intent(user_input)

    # Route to appropriate workflow
    return select_workflow(detected_type)
```

#### Workflow Selection
```yaml
Selected_Workflow:
  article: -> Phase 0A (Research) -> Phase 1A (Structure) -> Phase 2A (Write)
  story: -> Phase 0 (Brainstorm) -> Phase 1 (Setup) -> Phase 2 (Write)
  novel: -> Phase 0 (Brainstorm) -> Phase 1 (Bible) -> Phase 2 (Chapters)
  series: -> Phase 0S (Series Plan) -> Phase 1 (Bible) -> Phase 2 (Books)
  blog: -> Phase 0B (Topic) -> Phase 1B (Outline) -> Phase 2B (Draft)
```

### Phase 0A: Article Workflow (Non-Fiction Path)

#### Purpose
Research and structure informational content with fact-checking and citation management.

#### Workflow Steps:
1. **Topic Definition**: Clarify angle and scope
2. **Research Phase**: Gather sources and information
3. **Outline Creation**: Structure argument/narrative
4. **Draft Writing**: Create content with inline citations
5. **Fact Checking**: Verify all claims
6. **Quality Review**: Clarity, coherence, completeness

#### Article-Specific Bible
```yaml
article_bible:
  topic: "Main subject"
  angle: "Unique perspective"
  audience: "Target readers"
  thesis: "Core argument"
  key_points:
    - Point 1 with evidence
    - Point 2 with evidence
  sources:
    - Credible source 1
    - Credible source 2
  tone: "Formal/informal"
  length: 2000-5000 words
```

### Phase 0B: Short Story Workflow (Concentrated Fiction)

#### Purpose
Create impactful short fiction with tight structure and powerful payoff.

#### Workflow Steps:
1. **Concept Development**: Core idea/twist
2. **Character Sketching**: 1-3 main characters
3. **Single Arc Planning**: Beginning-middle-end
4. **Draft Creation**: Focus on impact
5. **Pacing Refinement**: Every word counts
6. **Payoff Enhancement**: Maximize ending impact

#### Short Story Bible
```yaml
story_bible:
  premise: "What if..."
  protagonist:
    name: "Character"
    want: "Desire"
    obstacle: "Conflict"
  setting: "Time and place"
  tone: "Mood/atmosphere"
  theme: "Underlying message"
  twist: "Revelation/payoff"
  length: 3000-7000 words
```

### Phase 0: Creative Incubation (Human-in-the-Loop Exploration)

#### Purpose
Transform vague creative ideas into structured, actionable story foundations through iterative human-AI collaboration.

#### Workflow Pattern: Diverge -> Explore -> Converge
```
Initial Idea (vague)
    |
Divergent Exploration (brainstorming)
    |
Iterative Refinement (human feedback loops)
    |
Convergent Definition (structured output)
    |
Bible-Ready Document
```

#### Workflow Steps:
1. **User Input**: `/novel:brainstorm "I want to write about..."`
2. **Initial Exploration**:
   - AI generates multiple interpretations
   - Explores different angles and possibilities
   - Presents options for human consideration

3. **Interactive Development Loop**:
   ```
   Present Ideas -> Human Feedback -> Refine -> Expand
        ^                                        |
        |----------------------------------------|
   ```

4. **Key Discussion Areas**:
   - **Genre Exploration**: "This could be mystery/thriller/literary..."
   - **Character Seeds**: "What if the protagonist is..."
   - **World Possibilities**: "Setting could be..."
   - **Theme Discovery**: "The core message might be..."
   - **Conflict Options**: "The main tension could come from..."

5. **Progressive Refinement Stages**:
   - Stage 1: Broad exploration (5-10 different directions)
   - Stage 2: Narrow to 2-3 promising concepts
   - Stage 3: Deep dive into chosen concept
   - Stage 4: Structure into bible format

#### Human Decision Points:
```yaml
Each iteration presents:
  Options:
    1) I like option A - expand on this
    2) Combine B and C elements
    3) Try a different direction
    4) This is good - let's develop it
    5) Ready to formalize into bible
```

#### Output: Bible Seed Document
```yaml
# Generated through brainstorming session
bible_seed:
  core_concept: "Refined from initial idea"
  genre: "Decided through exploration"
  themes: "Discovered through discussion"

  protagonist:
    concept: "Developed through iteration"
    motivation: "Clarified through questions"
    arc: "Emerged from exploration"

  world:
    setting: "Chosen from options"
    rules: "Defined through discussion"
    atmosphere: "Refined through feedback"

  conflict:
    central: "Crystallized from possibilities"
    stakes: "Raised through iteration"
    resolution_path: "Suggested direction"

  tone_and_style:
    voice: "Discovered through examples"
    mood: "Selected from options"
    influences: "Identified through discussion"
```

#### Key Features of Creative Incubation:

1. **Non-Linear Process**: Can jump between topics as inspiration strikes
2. **Memory Across Sessions**: Saves exploration history
3. **Idea Parking**: "Interesting but not for this story" list
4. **Inspiration Integration**: Can incorporate references, examples
5. **Constraint Introduction**: Gradually add practical limits

#### Example Interaction Flow:
```
Human: "I want to write about someone who collects memories"

AI: "Fascinating concept! Let me explore some directions:
1. Literal memory collector - sci-fi with technology that extracts memories
2. Metaphorical - antique dealer where objects hold memories
3. Supernatural - someone who absorbs memories through touch
4. Psychological - therapist specializing in recovered memories
5. Mystery - detective who pieces together victim's last memories

Which resonates, or should we explore other angles?"
```

#### Architecture in Phase 0:
- **Command**: `/novel:brainstorm` - Simple interface for creative exploration
- **Main Claude**: Manages interactive conversation flow
- **Coordinator**: `brainstorming-coordinator` - Plans exploration strategies
- **Agents**: `idea-generator`, `concept-refiner` - Generate and refine ideas
- **Data**: Saves brainstorming sessions for continuity

### Phase 1: Initialization (Story Foundation)

#### Workflow Steps:
1. **User Input**: `/novel:start "My Amazing Novel"` or use bible_seed from Phase 0
2. **Command Processing**: Parse title and requirements
3. **Coordinator Planning**: `novel-planning-coordinator` creates initialization plan
4. **Agent Execution**:
   - `bible-creator` -> Generate comprehensive bible from seed
   - `outline-generator` -> Create story structure
   - `project-initializer` -> Set up file structure
5. **Data Output**: Complete project structure with bible and outline

#### Key Decisions:
- Genre selection (affects writing style)
- Target audience (affects complexity and themes)
- Series vs standalone (affects story arc)
- Chapter target length (affects pacing)

#### Quality Gates:
- Bible completeness check
- Outline coherence validation
- Character arc verification

### Phase 2: Chapter Creation (Content Generation)

#### Workflow Steps:
1. **User Input**: `/novel:write 1` (write chapter 1)
2. **Command Processing**: Validate chapter sequence
3. **Coordinator Planning**: `chapter-generation-coordinator` creates execution plan
4. **Agent Execution** (Sequential):
   - `outline-generator` -> Create detailed chapter outline
   - `content-writer` -> Generate chapter prose
   - `quality-scorer` -> Evaluate quality (target: 85+)
5. **Conditional Flow**:
   - If quality >= 85: Save and complete
   - If quality < 85: Auto-improve with `quality-enhancer`

#### Key Components:
- **Bible Adherence**: All content must follow bible rules
- **Style Consistency**: Match established narrative voice
- **Pacing Control**: Follow outline's pacing requirements
- **Character Voice**: Maintain distinct character personalities

#### Anti-AI Patterns:
- Avoid overused transitions ("however", "moreover")
- Vary sentence structure and length
- Limit internal monologue frequency
- Show don't tell enforcement
- Natural dialogue patterns

### Phase 3: Quality Enhancement (Iterative Improvement)

#### Workflow Steps:
1. **User Input**: `/novel:revise 1` or auto-triggered by low quality
2. **Command Processing**: Load existing chapter
3. **Coordinator Planning**: `quality-improvement-coordinator` analyzes issues
4. **Agent Execution** (Parallel where possible):
   - `quality-scorer` -> Identify weak areas
   - `quality-enhancer` -> Apply targeted improvements
   - `consistency-checker` -> Verify bible compliance
5. **Iteration**: Repeat until quality >= 90 or user satisfied

#### Enhancement Strategies:
- **Prose Enhancement**: Improve sentence variety, remove cliches
- **Character Deepening**: Add subtle behaviors, unique speech patterns
- **World Enrichment**: Add sensory details, cultural elements
- **Pacing Adjustment**: Balance action, dialogue, and description
- **Emotion Amplification**: Strengthen emotional resonance

#### Quality Metrics:
```yaml
Technical Quality (40%):
  - Grammar and spelling: 10%
  - Sentence variety: 10%
  - Word choice: 10%
  - Flow and transitions: 10%

Narrative Quality (40%):
  - Character consistency: 10%
  - Plot advancement: 10%
  - World-building: 10%
  - Dialogue authenticity: 10%

Engagement Quality (20%):
  - Hook strength: 5%
  - Emotional impact: 5%
  - Page-turner factor: 5%
  - Memorable moments: 5%
```

### Phase 4: Context Synchronization (Learning from Success)

#### Workflow Steps:
1. **Trigger**: Chapter achieves 90+ quality score
2. **Automatic Process**: System learns from high-quality content
3. **Agent Execution**:
   - `context-extractor` -> Extract successful patterns
   - `bible-updater` -> Refine character/world details
   - `style-learner` -> Capture effective techniques
4. **Result**: Improved future chapter generation

#### Learning Targets:
- Character speech patterns that work well
- Effective scene transitions
- Successful emotional beats
- World details that enhance immersion

## Unified Process Comparison

### Content Type Process Matrix

| Phase | Article | Short Story | Novel | Series |
|-------|---------|-------------|--------|--------|
| **-1: Routing** | Detect non-fiction | Detect short fiction | Detect long fiction | Detect multi-book |
| **0: Planning** | Research topic | Brainstorm concept | Brainstorm world | Plan series arc |
| **1: Foundation** | Create outline | Develop characters | Create bible | Master + book bibles |
| **2: Creation** | Write w/ citations | Write complete story | Write chapters | Manage books |
| **3: Quality** | Fact-check | Impact check | Consistency check | Continuity check |
| **4: Learning** | Update style guide | Capture techniques | Learn from 90+ chapters | Cross-book patterns |

### Process Flow Variations

#### Linear Process (Articles/Blogs)
```
Research -> Outline -> Write -> Fact-check -> Publish
        No iteration needed if facts are correct
```

#### Circular Process (Short Stories)
```
Concept -> Draft -> Refine -> Impact Test
    ^                              |
    +-- Revise if impact weak -----+
```

#### Iterative Process (Novels)
```
Bible -> Chapter 1 -> Review -> Chapter 2 -> Review...
         Learn from each high-quality chapter
```

#### Hierarchical Process (Series)
```
Series Bible
    |
Book 1 Bible -> Book 1 Chapters
    |
Book 2 Bible -> Book 2 Chapters (with continuity check)
```

### Decision Points by Content Type

#### Article Decision Tree
```
Is topic clear? -> No -> Research more
                -> Yes -> Is angle unique? -> No -> Find angle
                                           -> Yes -> Write
```

#### Story Decision Tree
```
Is concept strong? -> No -> Brainstorm more
                   -> Yes -> Is ending powerful? -> No -> Rework
                                                  -> Yes -> Polish
```

#### Novel Decision Tree
```
Is bible complete? -> No -> Develop more
                   -> Yes -> Chapter quality 85+? -> No -> Revise
                                                   -> Yes -> Continue
```

## Data Flow Patterns

### Linear Flow (Most Common)
```
Command -> Coordinator (plan) -> Agent A -> Agent B -> Agent C -> Output
```

### Parallel Flow (For Independent Tasks)
```
Command -> Coordinator (plan) -> [Agent A, Agent B, Agent C] -> Merge -> Output
```

### Conditional Flow (Quality-Driven)
```
Command -> Coordinator (plan) -> Agent A -> Quality Check
                                              |
                                    Pass -> Save
                                    Fail -> Agent B (enhance) -> Loop
```

### Learning Flow (Context Update)
```
High-Quality Chapter -> Context Extraction -> Bible/Style Update
                                                |
                                    Future Chapters Improve
```

## Quality Control System

### Three-Tier Quality Model

#### Tier 1: Minimum Viable (70-79)
- Grammatically correct
- Plot makes sense
- Characters act consistently
- Readable but may lack polish

#### Tier 2: Publication Ready (80-89)
- Engaging prose
- Strong character voices
- Good pacing
- Minor improvements possible

#### Tier 3: Excellence (90-100)
- Compelling narrative
- Memorable characters
- Immersive world
- Emotional resonance
- Becomes learning source

### Quality Checkpoints

1. **Pre-Writing**: Bible and outline validation
2. **Post-Generation**: Immediate quality scoring
3. **Enhancement**: Iterative improvement cycles
4. **Final Review**: Human-in-loop approval option

## Smart Command Suggestion System

### Purpose
Guide users through the optimal workflow path based on project state and quality metrics.

### Implementation Strategy

#### 1. State Analysis Agent
A lightweight agent that quickly analyzes project state:
```yaml
name: project-state-analyzer
purpose: Analyze current project state and suggest next actions
checks:
  - Project existence
  - Bible completeness
  - Chapter sequence gaps
  - Quality scores
  - Last activity
```

#### 2. Suggestion Rules Engine
Context-aware suggestion logic:
```yaml
Rules:
  No_Project:
    primary: "/novel:brainstorm - Start with an idea"
    alternative: "/novel:start - Jump straight to creation"

  Just_Started:
    primary: "/novel:write 1 - Begin your story"
    alternatives:
      - "/novel:bible - Review your world-building"
      - "/novel:status - Check project setup"

  Writing_Flow:
    high_quality: "/novel:write [next] - Keep the momentum!"
    medium_quality: "/novel:revise [current] - Polish before continuing"
    low_quality: "/novel:revise [current] - Essential improvements needed"

  Stuck_Point:
    writer_block: "/novel:brainstorm - Explore new directions"
    plot_issue: "/novel:bible - Review story structure"
    quality_issue: "/novel:revise - Focus on improvement"
```

#### 3. User Preference Learning
Track user patterns to personalize suggestions:
```yaml
User_Patterns:
  perfectionist: Suggests more revisions
  flow_writer: Encourages continuing forward
  planner: Emphasizes outline and bible work
  explorer: Offers more brainstorming options
```

### Display Format

Suggestions appear at the end of each command execution:

```
Chapter 3 created successfully!
Quality Score: 82/100

---
📝 Suggested Next Steps:
1. /novel:revise 3    - Improve quality to 85+ (recommended)
2. /novel:write 4     - Continue with next chapter
3. /novel:status      - Review overall progress

💡 Tip: Chapters with 85+ quality contribute to style learning!
```

### Smart Features

#### 1. Priority-Based Suggestions
- **Critical**: Fix breaking issues (missing chapters, <70 quality)
- **Recommended**: Quality improvements (70-84 quality)
- **Optional**: Enhancements (85+ quality)

#### 2. Workflow Momentum Detection
- If user is in a "writing flow" (multiple chapters in session), prioritize continuation
- If user is in "editing mode" (multiple revisions), suggest quality checks
- If user is exploring (multiple brainstorms), offer creative options

#### 3. Milestone Awareness
```yaml
Milestones:
  first_chapter: "Congratulations on starting! The first chapter sets the tone."
  chapter_10: "Great progress! Consider reviewing story arc: /novel:bible"
  chapter_20: "Novel-length achieved! Check consistency: /novel:status"
  complete: "Story complete! Ready for final review: /novel:export"
```

## Implementation Priorities

### MVP Components (Phase 1)
1. Basic bible creation
2. Simple outline generation
3. Chapter writing with basic quality
4. File system structure

### Enhanced Features (Phase 2)
1. Multi-genre support
2. Advanced quality scoring
3. Style learning system
4. Character arc tracking

### Advanced Capabilities (Phase 3)
1. Series management
2. Multiple POV handling
3. Subplot weaving
4. Beta reader simulation

## Success Metrics

### System Performance
- Chapter generation time: < 2 minutes
- Quality score accuracy: 85% correlation with human judgment
- Consistency maintenance: 95% bible adherence
- Iteration efficiency: 50% quality improvement per cycle

### Content Quality
- Reader engagement: Page-turner score > 7/10
- Character memorability: Distinct voices for all major characters
- World immersion: Rich sensory details
- Emotional impact: Reader connection achieved

## Error Handling and Recovery

### Common Failure Modes
1. **Bible Inconsistency**: Automatic validation before writing
2. **Quality Threshold Miss**: Automatic enhancement cycle
3. **Style Drift**: Context synchronization to maintain voice
4. **Plot Holes**: Outline validation before writing

### Recovery Strategies
- Checkpoint saves after each successful phase
- Rollback capability for failed improvements
- Alternative generation for stuck scenarios
- Human-in-loop override options

## Appendices

### A. Genre-Specific Configurations
```yaml
mystery:
  focus: [plot, clues, revelation]
  quality_weights: {plot: 0.4, character: 0.3, prose: 0.3}

romance:
  focus: [emotion, relationship, chemistry]
  quality_weights: {emotion: 0.4, character: 0.4, prose: 0.2}

scifi:
  focus: [world, technology, ideas]
  quality_weights: {world: 0.4, plot: 0.3, prose: 0.3}
```

### B. Command Reference with Smart Suggestions

#### Core Commands
```bash
/novel:brainstorm [idea]      # Start creative exploration
/novel:start [title]          # Initialize new novel project
/novel:write [chapter]        # Write new chapter
/novel:revise [chapter]       # Improve existing chapter
/novel:status                 # Show project status
/novel:bible                  # View/edit bible
```

#### Intelligent Command Flow Suggestions

The system provides context-aware suggestions after each command:

```yaml
After /novel:brainstorm:
  Success:
    - "Ready to create your novel? Try: /novel:start '[Your Title]'"
    - "Want to explore another angle? Try: /novel:brainstorm '[New Direction]'"
    - "Save this idea for later? Try: /novel:park-idea"

After /novel:start:
  Success:
    - "Project created! Write your first chapter: /novel:write 1"
    - "Review your bible: /novel:bible"
    - "Check project structure: /novel:status"

After /novel:write [N]:
  Quality >= 85:
    - "Great chapter! Continue with: /novel:write [N+1]"
    - "Review all chapters: /novel:status"
    - "Polish this chapter further: /novel:revise [N]"

  Quality 75-84:
    - "Good start! Improve quality: /novel:revise [N]"
    - "Or continue and revise later: /novel:write [N+1]"

  Quality < 75:
    - "Let's enhance this chapter: /novel:revise [N] (recommended)"
    - "Review writing guidelines: /novel:bible"

After /novel:revise [N]:
  Quality >= 90:
    - "Excellent! Continue story: /novel:write [N+1]"
    - "This chapter is now a learning source!"

  Quality improved:
    - "Better! Try another pass: /novel:revise [N]"
    - "Or move forward: /novel:write [N+1]"

After /novel:status:
  Has gaps:
    - "Missing chapter [X]: /novel:write [X]"
    - "Low quality chapter [Y]: /novel:revise [Y]"

  Complete:
    - "Ready to publish! Try: /novel:export"
    - "Start next book: /novel:start '[Book 2 Title]'"
```

#### Smart Context Detection

The system analyzes project state to suggest the most relevant next action:

```python
def suggest_next_command(current_state):
    if not project_exists:
        return "Start with: /novel:brainstorm or /novel:start"

    if no_chapters:
        return "Begin writing: /novel:write 1"

    if has_low_quality_chapters:
        return f"Improve chapter {lowest_quality}: /novel:revise {lowest_quality}"

    if missing_chapter_in_sequence:
        return f"Fill gap: /novel:write {first_missing}"

    if all_chapters_complete:
        return "Congratulations! Review: /novel:status or /novel:export"

    return f"Continue story: /novel:write {last_chapter + 1}"
```

### C. File Naming Conventions
```
bible.yaml                    # Core configuration
outline.yaml                  # Story structure
chapters/001/content.md       # Chapter text
chapters/001/meta.json        # Metadata
chapters/001/quality.json     # Quality scores
context/characters.yaml       # Character tracking
context/world.yaml           # World evolution
context/plot.yaml            # Plot progression
```

## Conclusion

This workflow provides a systematic, quality-focused approach to novel creation that:
1. Leverages the 5-layer architecture for clear separation of concerns
2. Maintains consistency through centralized bible management
3. Ensures quality through multiple checkpoints and iterations
4. Learns from successes to improve over time
5. Scales from simple stories to complex series

The system is designed to be simple enough for MVP implementation while allowing for sophisticated enhancements as needed.

---

**Document Version**: 1.0
**Last Updated**: 2024-12-15
**Status**: Draft for Review
**Next Steps**: Validate with test implementation