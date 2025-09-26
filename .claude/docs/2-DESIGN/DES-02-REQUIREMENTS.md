# Requirements Document - Universal Writing System

## 1. Functional Requirements

### 1.1 Content Type Detection & Adaptation
#### 1.1.1 Auto-Detection
- **FR-001**: System MUST detect content type from initial prompt keywords
  - "article" / "文章" -> Article mode (500-5000 words)
  - "short story" / "短篇" -> Short story mode (2000-7500 words)
  - "novel" / "长篇" -> Novel mode (50000-100000 words)
  - "series" / "系列" -> Series mode (multiple novels)
  - "blog" / "博客" -> Blog mode (300-2000 words)

#### 1.1.2 Manual Override
- **FR-002**: User MUST be able to explicitly specify content type
- **FR-003**: System MUST confirm content type before proceeding

#### 1.1.3 Type-Specific Parameters
- **FR-004**: Each content type MUST have specific configuration:
  - Article: headline, subheadings, key points, conclusion
  - Short story: plot arc, single conflict, resolution
  - Novel: chapters, multiple plot lines, character arcs
  - Series: overarching narrative, continuity tracking
  - Blog: SEO keywords, casual tone, call-to-action

### 1.2 Research-Driven Creation Process

#### 1.2.0 Natural Language Research Triggers
- **FR-004a**: System MUST recognize research needs from conversation:
  - "什么类型火？" → trend-analyzer
  - "竞争激烈吗？" → competitor-scanner
  - "读者喜欢什么？" → audience-profiler
  - "XX是什么？" → topic-explorer
  - "如何提高曝光？" → keyword-researcher
  - NO explicit commands needed

- **FR-004b**: Intelligent context understanding:
  - System infers research needs from discussion
  - Triggers appropriate agents automatically
  - Presents findings naturally in conversation
  - Builds knowledge base transparently

- **FR-004c**: Research agents available during ANY phase (with web capabilities):
  - `trend-analyzer` - WebSearch for market trends, save analysis
    - Tools: [Read, Write, WebSearch, WebFetch]
    - Output: trend_analysis_{genre}_{date}.json

  - `competitor-scanner` - Find and analyze similar works
    - Tools: [Read, Write, WebSearch, WebFetch, Grep]
    - Output: competitor_analysis_{genre}_{date}.md

  - `audience-profiler` - Build detailed reader personas
    - Tools: [Read, Write, WebSearch, WebFetch]
    - Output: audience_profile_{target}_{date}.yaml

  - `keyword-researcher` - SEO and discoverability optimization
    - Tools: [Read, Write, WebSearch]
    - Output: keywords_{topic}_{date}.csv

  - `topic-explorer` - Deep research on subject matter
    - Tools: [Read, Write, WebSearch, WebFetch]
    - Output: topic_research_{subject}_{date}.md

  - `data-collector` - Gather statistics and facts
    - Tools: [Read, Write, WebSearch, WebFetch]
    - Output: data_collection_{topic}_{date}.json

- **FR-004c**: Research outputs automatically organized:
  ```
  /knowledge_base/
    /20250115_trend_analysis_romance.md
    /20250115_competitor_detective_novels.json
    /20250115_audience_profile_mystery.yaml
    /20250115_keyword_research_thriller.csv
  ```

- **FR-004d**: Research insights MUST influence:
  - Genre selection
  - Plot elements
  - Character archetypes
  - Writing style
  - Chapter length
  - Publishing strategy

### 1.3 Research Convergence Process

#### 1.3.1 From Broad to Specific
- **FR-050**: Research follows convergence pattern:
  ```
  Stage 1: Broad Market Scan (多个方向探索)
  ↓ User selects direction
  Stage 2: Genre Deep Dive (特定类型深入)
  ↓ User refines focus
  Stage 3: Niche Analysis (细分市场分析)
  ↓ User confirms approach
  Stage 4: Project Bible Generation (项目圣经生成)
  ```

#### 1.3.2 Knowledge Crystallization
- **FR-051**: Research results progressively refined:
  - Raw data → Insights → Recommendations → Decisions → Bible/Outline
  - Each stage builds on previous findings
  - Final output: Actionable project blueprint

#### 1.3.3 Voice Options Presentation
- **FR-052a**: System MUST present 3 complete voice options:
  - Each with full specifications (3-3-3+1 model)
  - Market fit percentage from research data
  - Sample paragraph demonstrating the voice
  - Strengths and weaknesses analysis
  - Named memorably (e.g., "Warm Island Friend")

- **FR-052b**: Voice discussion and refinement:
  - User can select one option
  - User can request hybrid of multiple options
  - User can ask for different options
  - System creates final voice specification

#### 1.3.4 Bible/Outline Generation
- **FR-052c**: Automated creation based on research + voice:
  - For Novel: `bible.yaml` with genre, themes, audience, voice guide
  - For Article: `outline.md` with keywords, structure, voice specs
  - For Series: `series_bible.yaml` with world-building, voice consistency
  - All include: Research-backed decisions with rationale

### 1.4 Human-Machine Collaborative Creation (Phase 0)

#### 1.4.0 Type Determination & Project Setup
- **FR-005a**: FIRST interaction MUST determine content type with numbered options:
  ```
  What would you like to create today?
  1) Article (1000-5000 words)
  2) Blog post (500-2000 words)
  3) Short story (2000-7500 words)
  4) Novel (50000-100000 words)
  5) Series (multiple novels)
  Please enter 1-5:
  ```
- **FR-005b**: Upon type selection, IMMEDIATELY create project folder:
  - Path: `D:\NOVELSYS-SWARM\.claude\data\{timestamp}_{type}`
  - Example: `D:\NOVELSYS-SWARM\.claude\data\20250115143022_novel`
  - Example: `D:\NOVELSYS-SWARM\.claude\data\20250115150530_article`
  - NO name required at creation (can be added later in project.yaml)
- **FR-005c**: Folder structure created based on type (ALL include knowledge base):
  - Article/Blog: `/draft`, `/research`, `/knowledge_base`, `/exports`
  - Short Story: `/draft`, `/notes`, `/knowledge_base`, `/versions`, `/exports`
  - Novel: `/chapters`, `/characters`, `/timeline`, `/notes`, `/knowledge_base`, `/versions`, `/exports`
  - Series: `/books`, `/series_bible`, `/characters`, `/timeline`, `/knowledge_base`, `/exports`

  Knowledge base structure:
  ```
  /knowledge_base/
    /market_research/      # 市场趋势分析
    /competitor_analysis/  # 竞品分析
    /audience_insights/    # 读者画像
    /topic_research/       # 主题调研
    /trend_tracking/       # 趋势跟踪
    /references/          # 参考资料
    /statistics/          # 数据统计
  ```
- **FR-005d**: IMMEDIATELY create `project.yaml` in root folder with metadata:
  ```yaml
  project_id: "20250115143022_novel"
  type: "novel"
  title: ""  # Filled during brainstorming
  created: "2025-01-15T14:30:22"
  language: "zh"  # auto-detected from user input
  status: "brainstorming"  # brainstorming|outlining|drafting|revising|complete
  genre: ""  # Determined during brainstorming
  description: ""  # Filled during brainstorming
  tags: []
  word_count_target: 80000  # Type-specific defaults
  current_word_count: 0
  last_modified: "2025-01-15T14:30:22"
  ```

#### 1.2.1 Brainstorming Stage
- **FR-005**: System MUST support iterative idea exploration
- **FR-006**: MUST NOT proceed to outline until user explicitly approves
- **FR-007**: Each iteration MUST build upon previous discussion
- **FR-008**: System MUST track and summarize key decisions

#### 1.2.2 Convergence Mechanism
- **FR-009**: System MUST identify when ideas are stabilizing
- **FR-010**: MUST present consolidated concept for approval
- **FR-011**: User MUST have option to:
  - Approve and proceed
  - Request specific modifications
  - Restart brainstorming

#### 1.2.3 Brainstorming Output
- **FR-012**: Final output MUST be structured "Creation Bible":
  - Core concept (1-2 sentences)
  - Key themes (3-5 items)
  - Target audience
  - Tone and style
  - Unique selling points
  - Constraints and boundaries

### 1.4 Trend Tracking & Prediction

#### 1.4.1 Market Intelligence System
- **FR-040**: System MUST track market signals:
  - Hot keywords trending up/down
  - Genre popularity shifts
  - Reader sentiment analysis
  - Seasonal patterns
  - Platform-specific trends (Amazon, Wattpad, etc.)

#### 1.4.2 Predictive Analytics
- **FR-041**: System SHOULD predict:
  - Next hot topics (3-6 months ahead)
  - Saturated genres to avoid
  - Emerging sub-genres
  - Optimal publication timing
  - Target audience growth areas

#### 1.4.3 On-Demand Research
- **FR-042**: Research triggered ONLY when user requests:
  - No automatic periodic updates
  - User explicitly asks for trend refresh
  - User decides when to research competitors
  - Research stays project-specific (no cross-sharing)

#### 1.4.4 Research-Based Decision Points
- **FR-043**: Key decisions backed by data:
  ```
  "Based on research:
   - Romance + Mystery growing 45% YoY
   - Competitor gap: No cozy mystery in tropical setting
   - Target audience: Women 25-45, prefer 60k words
   Recommendation: Cozy mystery romance, 60k words, tropical setting"
  ```

### 1.5 Quality Assurance Mechanisms

#### 1.3.1 Consistency Checking
- **FR-013**: Character consistency across chapters
- **FR-014**: Timeline continuity validation
- **FR-015**: Setting/location consistency
- **FR-016**: Plot logic verification

#### 1.3.2 Style Validation
- **FR-017**: Maintain consistent narrative voice
- **FR-018**: Vocabulary level consistency
- **FR-019**: Sentence structure variation metrics
- **FR-020**: Pacing consistency checks

#### 1.3.3 Content Completeness
- **FR-021**: Verify all plot threads resolved
- **FR-022**: Check character arc completion
- **FR-023**: Ensure thematic elements addressed
- **FR-024**: Validate chapter/section targets met

### 1.4 Workflow Flexibility

#### 1.4.1 Entry Points
- **FR-025**: Start from scratch (Phase 0)
- **FR-026**: Start with existing outline (Phase 1)
- **FR-027**: Start with partial draft (Phase 2)
- **FR-028**: Resume interrupted work

#### 1.4.2 Non-linear Operations
- **FR-029**: Edit any chapter/section independently
- **FR-030**: Reorder chapters/sections
- **FR-031**: Branch storylines for experimentation
- **FR-032**: Merge parallel versions

#### 1.4.3 Revision Cycles
- **FR-033**: Track version history
- **FR-034**: Compare versions side-by-side
- **FR-035**: Selective rollback capability
- **FR-036**: Change tracking with reasons

## 2. Non-Functional Requirements

### 2.1 Performance
- **NFR-001**: Generate 1000 words in < 30 seconds
- **NFR-002**: Quality check 10000 words in < 60 seconds
- **NFR-003**: Support documents up to 500000 words

### 2.2 Usability
- **NFR-004**: Maximum 3 prompts to start creating
- **NFR-005**: Clear progress indicators at each stage
- **NFR-006**: Intuitive command naming (verb-noun pattern)
- **NFR-007**: Helpful error messages with solutions

### 2.3 Reliability
- **NFR-008**: Auto-save every operation
- **NFR-009**: Crash recovery within last 5 minutes
- **NFR-010**: No data loss on unexpected termination
- **NFR-011**: Atomic operations (complete or rollback)

### 2.4 Scalability
- **NFR-012**: Handle 100+ chapter novel
- **NFR-013**: Manage 20+ book series
- **NFR-014**: Support 50+ character tracking
- **NFR-015**: Maintain performance with large datasets

### 2.5 Maintainability
- **NFR-016**: Modular architecture for easy updates
- **NFR-017**: Clear separation of concerns
- **NFR-018**: Comprehensive logging for debugging
- **NFR-019**: Version-controlled configuration

## 3. Data Requirements

### 3.1 Project Folder Naming Convention
- **DR-001a**: Folder name format: `{timestamp}_{type}`
  - timestamp: YYYYMMDDHHmmss (e.g., 20250115143022)
  - type: article|blog|shortstory|novel|series
  - NO name at creation (title determined during brainstorming)
- **DR-001b**: Examples:
  - `20250115143022_novel`
  - `20250115150530_article`
  - `20250115091015_series`
  - `20250115113045_shortstory`
  - `20250115082030_blog`
- **DR-001c**: Default word count targets by type:
  - article: 1500 words
  - blog: 800 words
  - shortstory: 5000 words
  - novel: 80000 words
  - series: 80000 per book

### 3.2 Input Data
- **DR-001**: User prompts (natural language)
- **DR-002**: Configuration files (YAML/JSON)
- **DR-003**: Existing drafts (Markdown)
- **DR-004**: Reference materials (context)

### 3.2 Persistent Data
- **DR-005**: Project configuration
- **DR-006**: Creation bible
- **DR-007**: Chapter/section drafts
- **DR-008**: Character profiles
- **DR-009**: Timeline/plot tracking
- **DR-010**: Version history

### 3.3 Output Data
- **DR-011**: Markdown formatted text
- **DR-012**: HTML export option
- **DR-013**: PDF export option
- **DR-014**: EPUB export option
- **DR-015**: Plain text option

## 4. Interface Requirements

### 4.1 Command Interface
- **IR-001**: CLI commands following pattern: `action-target`
- **IR-002**: Help available for each command
- **IR-003**: Tab completion for commands
- **IR-004**: Progress feedback during operations

### 4.2 File Interface
- **IR-005**: Standard directory structure
- **IR-006**: Human-readable file names
- **IR-007**: Consistent file extensions
- **IR-008**: Metadata in frontmatter

## 5. Constraints

### 5.1 Technical Constraints
- **TC-001**: Must work within NOVELSYS-SWARM architecture
- **TC-002**: No recursion (no Task tool in subagents)
- **TC-003**: File-based communication only
- **TC-004**: Windows path compatibility

### 5.2 Business Constraints
- **BC-001**: MVP in 8 weeks
- **BC-002**: Single user focus (no collaboration)
- **BC-003**: English and Chinese support only initially
- **BC-004**: Local file system only (no cloud)

## 6. Acceptance Criteria

### 6.1 MVP Success Metrics
- **AC-001**: Create complete article in single session
- **AC-002**: Generate coherent short story with plot
- **AC-003**: Produce novel chapter meeting quality standards
- **AC-004**: Successfully track series continuity
- **AC-005**: Human approval rate > 80% on first draft

### 6.2 Quality Metrics
- **AC-006**: Consistency score > 90%
- **AC-007**: Grammar/spelling accuracy > 95%
- **AC-008**: User modification rate < 20%
- **AC-009**: Completion rate > 90%
- **AC-010**: User satisfaction > 4/5

---

## Research Workflow Examples

### Example 1: Novel Project Research Flow
```
User: "我想写小说" → System creates project
↓
System: "Starting market research..."
↓
[Auto-trigger trend-analyzer]
→ Searches: "2025 novel trends", "bestselling genres", "reader preferences"
→ Saves: knowledge_base/trend_analysis_general_20250115.json
↓
System: "Top trending: Mystery +45%, Romance +23%, SciFi -12%
         Would you like to explore Mystery or Romance?"
↓
User: "Mystery"
↓
[Auto-trigger competitor-scanner]
→ Searches: "bestselling mystery novels 2024", "new mystery releases"
→ Analyzes: Top 10 titles, themes, lengths, styles
→ Saves: knowledge_base/competitor_analysis_mystery_20250115.md
↓
[Auto-trigger audience-profiler]
→ Searches: "mystery reader demographics", "mystery book reviews"
→ Builds: Reader personas, preferences, pain points
→ Saves: knowledge_base/audience_profile_mystery_20250115.yaml
↓
System: "Research complete. Key insights:
         - Gap: No cozy mystery in tropical settings
         - Audience: Women 25-45, prefer 60-80k words
         - Trend: Detective + Romance subplot rising

         Shall we brainstorm your mystery novel with these insights?"
```

### Example 2: Article Research Flow
```
User: "写篇技术文章"
↓
[Auto-trigger keyword-researcher]
→ Searches: trending tech topics, high-search keywords
→ Saves: knowledge_base/keywords_tech_20250115.csv
↓
System: "Hot topics: AI tools (+89%), Cloud security (+45%)
         Choose topic or request more research?"
```

## Research Principles (Confirmed)

1. **Research Automation**: **Manual Trigger Only**
   - User explicitly requests each research action
   - No automatic background research
   - System waits for user command

2. **Data Isolation**: **Project-Specific**
   - Each project has independent knowledge_base
   - No sharing between projects
   - Clean slate for each new project

3. **Update Strategy**: **On-Demand Only**
   - No scheduled updates
   - User decides when data is stale
   - Research only when user requests

## Research Through Natural Conversation

### Key Principle: Context-Driven Research Agents
**NOT command-based**: No `/research` or `/analyze` commands
**Natural dialogue**: System intelligently triggers agents based on conversation context

### Conversation-Triggered Research Flow
```
User: "我想写小说"
System: Creates project: /20250115143022_novel/
        "What kind of story interests you?"

User: "不太确定，什么类型现在比较火？"
System: [Recognizes market inquiry → Triggers trend-analyzer]
        [trend-analyzer → knowledge_base/trends_broad.json]
        "Based on current market analysis:
         Mystery novels up 45% this year
         Romance remains strong at +23%
         Sci-fi declining -12%
         Would you like to explore any of these?"

User: "我对Mystery感兴趣"

=== Stage 2: Genre Deep Dive ===
User: "Mystery有意思，但竞争会不会很激烈？"
System: [Recognizes competition concern → Triggers competitor-scanner]
        [competitor-scanner → knowledge_base/mystery_competitors.md]
        "I analyzed the mystery landscape. While competitive,
         I found an underserved niche: cozy mysteries in exotic
         locations. Only 3% of current titles, but high reader
         demand. Should I research this niche further?"

User: "Cozy mystery是什么？听起来有趣"
System: [Recognizes knowledge gap → Triggers topic-explorer]
        [topic-explorer → knowledge_base/cozy_mystery_guide.md]
        "Cozy mysteries are lighter mysteries with:
         - Amateur sleuth (not police)
         - Small community setting
         - Minimal violence/gore
         - Often includes crafts/hobbies/food
         - Think 'Murder She Wrote' not 'Silence of the Lambs'
         Readers love them for comfort reading."

=== Stage 3: Natural Niche Exploration ===
User: "我喜欢这个方向，如果设在热带岛屿怎么样？"
System: [Recognizes setting research need → Multiple agents]
        [audience-profiler → knowledge_base/tropical_cozy_audience.yaml]
        [keyword-researcher → knowledge_base/tropical_mystery_keywords.csv]
        "Excellent instinct! Tropical cozy mysteries show:
         - 89% reader satisfaction rate
         - Keywords 'island mystery' up 156% YoY
         - Readers want: paradise contrast, local culture, beach vibes
         - Gap: Most are Hawaii-based, other islands underrepresented"

User: "就tropical island cozy mystery了"

=== Stage 4: Author Voice Calibration ===
User: "分析目标读者喜欢的写作风格"
System: [voice-analyzer → knowledge_base/voice_analysis.yaml]

        "Based on analysis of top 20 tropical cozy mysteries, here are 3 voice options:

        OPTION 1: 'Warm Island Friend' (65% reader preference)
        ```yaml
        Core: First person, warm tone, medium pace
        Style: Varied sentences (10-20 words), Grade 7-9, balanced dialogue
        Engagement: Light humor, medium emotion, moderate detail
        Cultural: American English, Caribbean setting, US market
        Sample: 'I never expected to find a body at the beach barbecue.
                The steel drums stopped mid-song, and even the parrots
                went quiet. Sometimes paradise has terrible timing.'
        Strengths: High engagement, proven market fit
        Weaknesses: Common approach, less distinctive
        ```

        OPTION 2: 'British Expat Observer' (23% reader preference)
        ```yaml
        Core: First person, warm-cool mix, measured pace
        Style: Longer sentences (15-25 words), Grade 8-10, dialogue-heavy
        Engagement: Dry humor, subtle emotion, rich detail
        Cultural: British English, Caribbean setting, UK/US market
        Sample: 'Finding a body at what should have been a perfectly lovely
                beach barbecue was, I must say, rather poor form. The
                steel drums fell silent, as did the tropical birds, as if
                the island itself was holding its breath.'
        Strengths: Distinctive voice, appeals to literary readers
        Weaknesses: Smaller audience, requires consistent British voice
        ```

        OPTION 3: 'Island Noir Light' (12% reader preference)
        ```yaml
        Core: First person, cool-warm tone, quick pace
        Style: Short sentences (8-15 words), Grade 6-8, minimal dialogue
        Engagement: Dark humor, controlled emotion, sparse detail
        Cultural: International English, Caribbean setting, global market
        Sample: 'Body at the beach barbecue. The music died. Even the
                parrots knew something was wrong. In paradise, death
                hits different. Harder. The contrast is killer.'
        Strengths: Unique in cozy space, page-turner pace
        Weaknesses: May alienate traditional cozy readers
        ```

        Which voice resonates with your vision? We can also blend elements."

User: "我喜欢Option 1的亲切感，但想要Option 2的独特性"

System: "Let me create a hybrid voice combining warmth with distinction..."

=== Stage 5: Bible Generation ===
User: "基于调研和声纹生成bible"
System: [bible-generator reads all knowledge_base files + voice decision]
        Creates: /bible.yaml
        ```yaml
        genre: "Cozy Mystery"
        subgenre: "Tropical Island Mystery"
        target_audience: "Women 25-45"
        word_count: 65000

        # CRITICAL: Voice defines everything
        author_voice:
          # Core Elements (必需)
          perspective: "First person"               # 第一/第三人称
          tone: "Warm and conversational"          # 整体情感温度
          pacing: "Quick, 2000-3000 word chapters" # 节奏控制

          # Style Markers (风格标记)
          sentence_rhythm: "Varied, 10-20 words"   # 句子节奏
          vocabulary_level: "Grade 7-9"            # 词汇难度
          dialogue_style: "Natural, character-driven" # 对话风格

          # Reader Engagement (读者连接)
          humor_type: "Situational, character quirks" # 幽默类型
          emotion_intensity: "Medium, peaks in key scenes" # 情感强度
          detail_density: "Light, focus on atmosphere" # 细节密度

        tone: "Light, humorous, warm"
        themes: ["Community", "Paradise vs Reality"]

        research_rationale:
          - "45% YoY growth in cozy mystery"
          - "Gap in tropical settings"
          - "Audience prefers 60-70k words"
          - "Voice pattern matches 65% reader preference"
        ```

User: "好，开始写作"
System: All subsequent writing based on this bible
```

## Agent Requirements for Research System

### Essential Research Agents (Phase 1)
1. `trend-analyzer` - Market trends
2. `competitor-scanner` - Competition analysis
3. `audience-profiler` - Reader demographics
4. `keyword-researcher` - SEO/discoverability
5. `topic-explorer` - Subject deep dive
6. `voice-analyzer` - Author voice pattern analysis
   - Analyzes linguistic patterns (sentence structure, vocabulary)
   - Identifies cultural markers (US vs UK English)
   - Maps setting-appropriate descriptions
   - Tools: [Read, Write, WebSearch, WebFetch]
   - Output: voice_analysis_{market}_{genre}_{date}.yaml
7. `bible-generator` - Synthesize research + voice into bible

### Future Research Agents (Phase 2+)
7. `sentiment-analyzer` - Review sentiment analysis
8. `price-optimizer` - Pricing strategy research
9. `cover-trend-analyzer` - Visual trend analysis
10. `platform-analyzer` - Platform-specific insights

---

*Document Version: 1.0*
*Status: DRAFT - Under Discussion*
*Last Updated: 2025-01-15*