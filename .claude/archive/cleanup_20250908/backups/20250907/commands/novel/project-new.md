---
description: Create new novel project with Bible
argument-hint: <project_name>
---

# Create New Novel Project with Brainstorming

Creating project: **$ARGUMENTS**

## Book Number Convention
For all paths in this command:
- **BOOK_NUMBER** = 1 (new projects always start with book_1)
- When creating subsequent books, use /novel:next-book command
- Dynamic book support enables series expansion

## Execution Flow

### Phase 1: Series-Level Brainstorming
Gather series-level information first (this defines the overall project):

#### 1.1 Series Foundation
Ask: "What type of novel project is this?"
- **Project Format**:
  * Series: Multiple books sharing world/characters
  * Standalone: Single complete story
  * Trilogy: Three connected books
  * Collection: Short story anthology
  * Serial: Episodic web fiction

- **Language & Regional Variant**:
  * Primary Language: English/Other
  * English Variant: 
    - US English (largest market, Amazon default)
    - UK English (Commonwealth markets, certain settings)
    - International English (neutral, broad appeal)
    - Canadian English (US spelling, UK vocabulary)
    - Australian English (specific market)
  * Setting Influence:
    - If UK/European setting  ->  Consider UK English
    - If US/Canadian setting  ->  US English recommended  
    - If international/fantasy  ->  International English
  * Target Market Priority: US/UK/Global/Regional

- **Spelling & Vocabulary Preferences**:
  * Spelling System:
    - US spelling (-ize, -or, -er): maximize, color, center
    - UK spelling (-ise, -our, -re): maximise, colour, centre
    - Oxford spelling (-ize, -our, -re): maximize, colour, centre
  * Vocabulary Choice:
    - US terms (elevator, apartment, vacation, gas)
    - UK terms (lift, flat, holiday, petrol)
    - Neutral/both (avoid contentious terms)
  * Date Format: MM/DD/YYYY (US) or DD/MM/YYYY (UK/EU)
  * Measurement: Imperial/Metric/Both with conversion

- **Writing Style**:
  * Prose Approach: Contemporary/Literary/Commercial/Genre-specific
  * Complexity Level: Accessible/Moderate/Complex/Experimental
  * Cultural References: US pop culture/UK culture/International/Minimal

- **Language Selection Guide** (System Recommendations):
  ```
  IF setting = UK/Ireland/Europe AND target = UK/Europe:
     ->  UK English strongly recommended
  ELIF setting = US/Canada AND target = US:
     ->  US English strongly recommended
  ELIF genre = "Cozy Mystery" AND setting = UK village:
     ->  UK English (use "cosy" spelling)
  ELIF genre = "Cozy Mystery" AND setting = US small town:
     ->  US English (use "cozy" spelling)
  ELIF setting = Commonwealth (AU/NZ/SA):
     ->  UK English or local variant
  ELIF setting = International/Fantasy/Sci-Fi:
     ->  International English (US spelling, neutral vocabulary)
  ELSE (maximizing market reach):
     ->  US English (largest market) with neutral vocabulary
  
  Special Cases:
  - Canary Islands/Mediterranean  ->  UK English (British expat readers)
  - Historical fiction  ->  Match the period and location
  - YA Global  ->  US English with minimal slang
  ```

#### 1.2 Genre & Category
Ask: "What is the primary genre and subgenre?"
- **Main Genre**: 
  * Fantasy/Science Fiction/Mystery/Thriller/Romance/Horror/Literary Fiction
  * Young Adult/Middle Grade/New Adult/Adult
- **Subgenre**:
  * Fantasy: Epic/Urban/Dark/Paranormal/Historical/Portal
  * Sci-Fi: Space Opera/Cyberpunk/Dystopian/Time Travel/Hard SF
  * Mystery: Cozy/Police Procedural/Amateur Sleuth/Private Eye
  * Romance: Contemporary/Historical/Paranormal/Romantic Suspense
- **Tone**: Light-hearted/Dark/Gritty/Hopeful/Satirical/Serious
- **POV**: First Person/Third Limited/Third Omniscient/Multiple POV/Unreliable Narrator
- **Core Themes**: Coming of age/Redemption/Power & corruption/Love & sacrifice/Identity/Good vs Evil

#### 1.3 Target Market & Publishing Strategy
Ask: "What is your target market and publishing plan?"
- **Target Market**:
  * Primary Region: US/UK/Canada/Australia/Europe/Global
  * Age Group: Middle Grade (8-12)/Young Adult (13-17)/New Adult (18-25)/Adult (25+)
  * Target Readers: Genre fans/Literary readers/Book club readers/Series readers
  * Reader Expectations: Fast-paced action/Character-driven/World-building/Romance subplot

- **Publishing Platforms**:
  * Self-Publishing: Amazon KDP/KDP Select (exclusive)/Wide distribution
  * Other Platforms: Apple Books/Kobo/Barnes & Noble/Google Play/Draft2Digital/IngramSpark
  * Traditional: Seeking agent/Direct submission/Hybrid publishing
  * Audiobook: ACX/Findaway Voices/Author narrated/Professional narrator
  * Adaptation Rights: Film/TV/Gaming/Graphic novel/Reserved

#### 1.4 Book Length & Series Planning
Ask: "What is your planned book length and release schedule?"
- **Book Specifications**:
  * Word Count Target: 50K/70K/90K/120K/150K+ words
  * Chapter Count: 20/30/40/50+ chapters
  * Chapter Length: 2000/3000/4000/5000 words average
  * Series Structure: Standalone/Duology/Trilogy/Ongoing series (4-7 books)/Long series (8+)

- **Release Strategy**:
  * For Series: Rapid release (monthly)/Standard (3-6 months)/Annual releases
  * Pre-launch Strategy: ARC readers/NetGalley/BookSprout/Direct reviewers
  * Launch Plan: Soft launch/Full marketing launch/Stealth launch
  * Price Strategy: $0.99 intro/$2.99-4.99 standard/$5.99+ premium/KU exclusive

#### 1.5 Story Hooks & Unique Selling Points
Ask: "What makes your story unique and compelling?"
- **Core Conflict**:
  * Conflict Type: Person vs Person/Nature/Society/Self/Technology/Fate
  * Stakes: Personal/Family/Community/World/Universe/Reality
  * Central Question: What core question drives the narrative?

- **Unique Elements**:
  * Magic System: Hard magic/Soft magic/Science-based/Unique twist
  * World Building: Alternate history/Secondary world/Portal fantasy/Hidden world
  * Story Hook: Opening with action/Mystery/Character moment/World reveal
  * Twist/USP: Genre blend/Unique perspective/Fresh take on tropes

#### 1.6 World & Character Foundation
Ask: "What are the key world and character elements?"
- **World Setting**:
  * Time Period: Contemporary/Historical (specify)/Near future/Far future/Timeless
  * Geographic Scope: Single city/Country/Continent/Planet/Multi-world/Multiverse
  * Technology Level: Pre-industrial/Industrial/Modern/Near-future/Far-future/Mixed
  * Magic/Power Level: None/Low/Medium/High/Reality-breaking

- **Protagonist Design**:
  * Protagonist Type: Single POV/Dual POV/Ensemble cast/Rotating POV
  * Character Archetype: Chosen one/Reluctant hero/Anti-hero/Everyman/Specialist
  * Growth Arc: Zero to hero/Fall and redemption/Coming of age/Corruption arc
  * Defining Traits: Proactive/Reactive/Clever/Strong/Empathetic/Flawed

#### 1.7 Comparative Titles & Market Position
Ask: "What published books is your novel similar to?"
- **Comp Titles** (Comparative/Comparable titles):
  * Book 1: [Title by Author] - Why similar?
  * Book 2: [Title by Author] - What element matches?
  * "It's like X meets Y": Classic elevator pitch format

- **Market Differentiation**:
  * What's familiar: Genre conventions you're keeping
  * What's fresh: Your unique twist or angle
  * Target Keywords: For Amazon/SEO optimization
  * Category fit: Specific Amazon/BISAC categories targeted

#### 1.8 Content Considerations & Tropes
Ask: "What content warnings and genre conventions apply?"
- **Content Warnings**:
  * Violence Level: None/Mild/Moderate/Graphic
  * Sexual Content: None/Fade-to-black/On-page/Explicit
  * Heat Level (Romance): Sweet/Mild/Moderate/Steamy/Explicit
  * Trigger Warnings: Death/Trauma/Abuse/Mental health/None
  * Language: Clean/Mild profanity/Strong language

- **Genre Tropes**:
  * Embraced Tropes: Which classic tropes are you using?
  * Subverted Tropes: Which tropes will you twist?
  * Avoided Tropes: Which clichés to deliberately avoid?
  * Reader Promises: HEA for romance/Justice for mystery/etc.

#### 1.9 Series & Writing Specifics
Ask: "What are your series continuity and writing style preferences?"
- **Series Continuity** (if series):
  * Arc Type: Episodic/Continuous story/Hybrid
  * Entry Points: Must start Book 1/Any book works
  * Recurring Elements: Signature settings/Items/Phrases
  * Overarching Mystery: Series-wide question/plot

- **Writing Balance**:
  * Dialogue Ratio: 20-30%/30-40%/40-50%/50%+
  * Action vs Reflection: Action-heavy/Balanced/Introspective
  * Description Style: Cinematic/Detailed/Sparse/Poetic
  * Chapter Endings: All cliffhangers/Mix/Resolution-focused
  * Pacing Overall: Breakneck/Steady/Slow burn/Variable

#### 1.10 Author Platform & Marketing
Ask: "What's your author platform and marketing approach?"
- **Author Platform**:
  * Author Brand: Pen name or real name?
  * Existing Platform: Website/Newsletter/Social media followers
  * Content Strategy: Blog/YouTube/TikTok/Instagram/Twitter

- **Marketing Plan**:
  * Pre-launch: Beta readers/ARC team/Street team
  * Launch Strategy: BookBub/Facebook ads/Amazon ads/Organic
  * Long-term: Series momentum/Newsletter/Reader magnets

#### 1.11 Save Series Brainstorming Results

**Save series-level brainstorming to file:**
- Use Write tool: `.claude/data/projects/{PROJECT_NAME}/series_brainstorming.yaml`
- Format:
```yaml
# Project Foundation
project_foundation:
  project_type: "{series/standalone/trilogy/collection}"
  language:
    primary: "English"
    variant: "{US/UK/International/Canadian/Australian}"
    setting_match: "{yes/no}"  # Does language match setting?
    market_priority: "{US/UK/Global/Regional}"
  spelling_system:
    style: "{US/UK/Oxford}"  # -ize/-ise, -or/-our, -er/-re
    vocabulary: "{US/UK/Neutral}"  # elevator/lift, apartment/flat
    date_format: "{MM-DD-YYYY/DD-MM-YYYY}"
    measurements: "{Imperial/Metric/Both}"
    cultural_refs: "{US/UK/International/Minimal}"
  prose_style: "{contemporary/literary/commercial/genre_specific}"

# Genre & Category
genre:
  main_genre: "{Fantasy/SciFi/Mystery/Thriller/Romance/Horror/Literary}"
  age_category: "{MG/YA/NA/Adult}"
  subgenre: "{Epic_Fantasy/Urban_Fantasy/Cozy_Mystery/etc}"
  tone: "{light_hearted/dark/gritty/hopeful/serious}"
  pov: "{first_person/third_limited/third_omni/multiple}"
  themes: ["{coming_of_age}", "{redemption}", "{power_corruption}"]

# Target Market
market:
  primary_region: "{US/UK/Canada/Australia/Europe/Global}"
  target_age: "{8-12/13-17/18-25/25+}"
  reader_type: "{genre_fans/literary_readers/series_readers}"
  reader_expectations: ["{fast_paced}", "{character_driven}", "{world_building}"]

# Publishing Strategy  
publishing:
  primary_platform: "{KDP/KDP_Select/Wide}"
  additional_platforms: ["{Apple_Books}", "{Kobo}", "{B&N}"]
  traditional_plans: "{seeking_agent/direct_submission/none}"
  audiobook_plans: "{ACX/Findaway/none}"
  pricing_strategy: "{0.99_intro/2.99-4.99_standard/5.99+_premium/KU}"

# Book Specifications
book_specs:
  word_count_target: {50000/70000/90000/120000}
  chapter_count: {20/30/40/50}
  chapter_length_avg: {2000/3000/4000/5000}
  series_length: "{standalone/trilogy/4-7_books/8+_books}"

# Release Strategy
release:
  series_release_schedule: "{rapid_monthly/standard_quarterly/annual}"
  prelaunch_strategy: "{ARC_readers/NetGalley/BookSprout}"
  launch_type: "{soft_launch/full_marketing/stealth}"

# Story Elements
story_core:
  central_conflict: "{person_vs_person/nature/society/self}"
  stakes_level: "{personal/family/community/world/universe}"
  central_question: "{What_question_drives_the_narrative}"
  unique_selling_point: "{genre_blend/unique_perspective/fresh_take}"

hooks:
  opening_type: "{action/mystery/character_moment/world_reveal}"
  story_hook: "{What_makes_it_unique}"

# World & Character
world:
  time_period: "{contemporary/historical_YEAR/near_future/far_future}"
  geographic_scope: "{city/country/continent/planet/multiverse}"
  technology_level: "{pre_industrial/modern/near_future/far_future}"
  magic_level: "{none/low/medium/high/reality_breaking}"

protagonist:
  pov_structure: "{single/dual/ensemble/rotating}"
  archetype: "{chosen_one/reluctant_hero/antihero/everyman}"
  growth_arc: "{zero_to_hero/fall_redemption/coming_of_age}"
  key_traits: ["{proactive}", "{clever}", "{flawed}"]

# Content & Tropes
content_warnings:
  violence_level: "{none/mild/moderate/graphic}"
  sexual_content: "{none/fade_to_black/on_page/explicit}"
  heat_level: "{sweet/mild/moderate/steamy/explicit}"  # For romance
  trigger_warnings: ["{death}", "{trauma}", "{abuse}", "{mental_health}"]
  language: "{clean/mild_profanity/strong_language}"

genre_tropes:
  embraced: ["{enemies_to_lovers}", "{chosen_one}", "{found_family}"]
  subverted: ["{damsel_in_distress}", "{love_triangle}"]
  avoided: ["{instalove}", "{mary_sue}"]
  
reader_promises:
  emotional_journey: "{what_readers_will_feel}"
  satisfaction_guarantee: "{HEA/justice/revelation/growth}"
  genre_expectations: ["{fair_play_mystery}", "{no_cliffhanger_ending}"]

# Series & Writing Style
series_continuity:  # If applicable
  arc_type: "{episodic/continuous/hybrid}"
  entry_points: "{book1_only/any_book}"
  recurring_elements: ["{signature_location}", "{catchphrase}", "{item}"]
  overarching_mystery: "{series_wide_question}"

writing_style:
  dialogue_percentage: "{20-30/30-40/40-50/50+}"
  action_vs_reflection: "{action_heavy/balanced/introspective}"
  description_style: "{cinematic/detailed/sparse/poetic}"
  chapter_endings: "{cliffhangers/mixed/resolution}"
  pacing_preference: "{breakneck/steady/slow_burn/variable}"
  opening_style: "{action_start/slow_burn/in_medias_res}"

# Market Positioning
comp_titles:
  - title: "{Book_Title}"
    author: "{Author_Name}"
    similarity: "{Why_comparable}"
  - title: "{Book_Title_2}"
    author: "{Author_Name_2}"
    similarity: "{Shared_elements}"
  elevator_pitch: "{Its_X_meets_Y}"

market_keywords: ["{keyword1}", "{keyword2}", "{keyword3}"]
target_categories: ["{Amazon_category1}", "{BISAC_category1}"]

# Author Platform
author_platform:
  author_name: "{pen_name_or_real}"
  existing_reach:
    website: "{yes/no}"
    newsletter_size: {0/100/1000/5000+}
    social_followers: {0/100/1000/10000+}
  content_strategy: ["{blog}", "{youtube}", "{tiktok}", "{instagram}"]

marketing_plan:
  prelaunch: ["{beta_readers}", "{arc_team}", "{street_team}"]
  launch: ["{bookbub}", "{fb_ads}", "{amazon_ads}", "{organic}"]
  longterm: ["{series_momentum}", "{newsletter}", "{reader_magnets}"]

# Metadata
metadata:
  created_at: "{TIMESTAMP}"
  version: "5.0_Western_Language_Enhanced"
  language_logic_applied: true
```

### Phase 1.5: Check Series Brainstorming Completeness

**Validate series brainstorming has sufficient information:**
1. **Use Task tool with:**
   - subagent_type: "brainstorming-completeness-checker"
   - description: "Check series brainstorming completeness"
   - prompt: """
     Check completeness of series brainstorming
     - File: .claude/data/projects/{PROJECT_NAME}/series_brainstorming.yaml
     - Type: series
     - Minimum threshold: 80%
     - Save report to: .claude/data/projects/{PROJECT_NAME}/series_brainstorming_completeness.json
     """

2. **Read completeness report:**
   - Use Read tool: `.claude/data/projects/{PROJECT_NAME}/series_brainstorming_completeness.json`
   - If completeness < 80%:
     * Display missing critical elements
     * Ask follow-up questions for each missing element
     * Update series_brainstorming.yaml with answers
     * Return to completeness check

3. **Confirm readiness:**
   - Display: "[x] Series brainstorming {completeness}% complete - ready to proceed"

### Phase 2: Generate Series Bible (With Author Voice Signature)

**Create Series Bible that defines standards for all books:**

1. **Launch series-bible-architect:**
   - Use Task tool with:
     * subagent_type: "series-bible-architect"
     * description: "Generate Series Bible"
     * prompt: """
       Create initial Series Bible for project '{PROJECT_NAME}'
       
       INITIAL_CREATION: true
       
       Context File to Read:
       - Series brainstorming: .claude/data/projects/{PROJECT_NAME}/series_brainstorming.yaml
       
       Instructions:
       - Extract language variant and writing preferences for author_voice_signature
       - Create phase_1_planning based on series structure
       - Include series metadata and continuity framework
       - Define author_voice_signature that all books MUST inherit
       
       Save to: .claude/data/projects/{PROJECT_NAME}/series_bible.yaml
       """
   - Display: "[x] Series Bible created with author voice signature"

### Phase 3: Book 1 Specific Brainstorming

**Now gather Book 1 specific information:**

#### 3.1 Book 1 Role in Series
Ask: "What will Book 1 accomplish in your series?"
- **Foundation Elements**:
  * Which characters are introduced?
  * What world elements are established?
  * Which mysteries/conflicts begin?
  
#### 3.2 Book 1 Specific Plot
Ask: "What is the specific story for Book 1?"
- **Main Conflict**: The central problem of this book
- **Opening Scene**: How does Book 1 begin?
- **Key Events**: Major plot points
- **Ending Type**: Resolution/Cliffhanger/Mixed

#### 3.3 Book 1 Characters
Ask: "Which characters appear in Book 1?"
- **Introduced in Book 1**: New characters
- **Character Focus**: Who gets the most development?
- **Relationships**: Which relationships are established?

#### 3.4 Save Book 1 Brainstorming

**Save Book 1 specific brainstorming:**
- Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_1`
- Use Write tool: `.claude/data/projects/{PROJECT_NAME}/book_1/book_brainstorming.yaml`
- Format:
```yaml
book_role:
  purpose_in_series: "Introduction/Foundation/Setup"
  establishes: ["world", "main characters", "central mystery"]
  
book_plot:
  main_conflict: "{specific to Book 1}"
  opening: "{how Book 1 starts}"
  climax: "{major turning point}"
  ending: "{resolution or cliffhanger}"
  
characters_in_book:
  introduced: ["character1", "character2"]
  focus: "primary character development"
  relationships_established: ["friendship1", "rivalry1"]
  
threads:
  opened: ["mystery1", "subplot1"]
  resolved: ["intro_conflict"]
  continuing: ["series_mystery"]
```

#### 3.5 Check Book 1 Brainstorming Completeness

**Validate Book 1 brainstorming:**
1. **Use Task tool with:**
   - subagent_type: "brainstorming-completeness-checker"
   - description: "Check book brainstorming completeness"
   - prompt: """
     Check completeness of book brainstorming
     - File: .claude/data/projects/{PROJECT_NAME}/book_1/book_brainstorming.yaml
     - Type: book
     - Minimum threshold: 80%
     - Save report to: .claude/data/projects/{PROJECT_NAME}/book_1/book_brainstorming_completeness.json
     """

2. **Handle incompleteness:**
   - If < 80%: Ask follow-up questions and update

### Phase 4: Project Structure Creation

**Ensure base system directories exist:**
- Use Bash tool: `mkdir -p .claude/data/context .claude/data/projects .claude/data/templates`

**Create unified series project structure (all projects are series):**

1. **Create base project directories:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_{BOOK_NUMBER}/{chapters,context}`
   - Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/series_planning`
   - This creates the unified book_{BOOK_NUMBER} structure for all projects
   - Note: BOOK_NUMBER = 1 for new projects

2. **Create project-level directories:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/shared`
   - Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/global_context`
   - These manage series-wide resources and context

### Phase 5: Book 1 Bible Generation (Iterative with Quality Gate)

**IMPORTANT: Book 1 Bible MUST inherit author_voice_signature from Series Bible**

#### 5.1 Generate Book 1 Bible V1

**Create directories for Bible versions:**
- Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_{BOOK_NUMBER}/bible_versions`
- Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_{BOOK_NUMBER}/bible_reviews`

**Launch bible-architect agent for Book 1 Bible:**

1. **Use Task tool with:**
   - subagent_type: "bible-architect"
   - description: "Generate Book 1 Bible V1"
   - prompt: "Create comprehensive Book 1 Bible for project '{PROJECT_NAME}'
     * MUST READ Series Bible first: .claude/data/projects/{PROJECT_NAME}/series_bible.yaml
     * Book brainstorming: .claude/data/projects/{PROJECT_NAME}/book_1/book_brainstorming.yaml
     * CRITICAL: Inherit author_voice_signature from Series Bible
     * Genre: {detected_genre} - already in series_bible
     * Include all 8 required sections
     * Character arcs must have chapter-by-chapter progression for Book 1
     * Voice profile MUST match Series Bible author_voice_signature
     * If mystery genre, include complete mystery_structure
     * Save to: .claude/data/projects/{PROJECT_NAME}/book_1/bible_versions/bible_v1.yaml"

2. **Confirm Bible V1 created:**
   - Use Read tool: `.claude/data/projects/{PROJECT_NAME}/book_1/bible_versions/bible_v1.yaml`
   - If missing, report error and stop

#### 3.2 Bible Quality Review Loop

**Iteratively improve Bible until quality >= 95:**

**Iterative Bible quality improvement process (up to 5 iterations):**

Starting with version 1, repeat the following steps until quality score reaches 95 or maximum iterations (5) is reached:

**For each iteration:**

1. **Review current Bible version using Task tool:**
   - **subagent_type**: "bible-reviewer"
   - **description**: "Review Bible V[current_version]"
   - **prompt**: Provide the following instructions:
     ```
     Review Bible quality for project '**$PROJECT_NAME**'
     - Bible path: .claude/data/projects/**$PROJECT_NAME**/book_1/bible_versions/bible_v[current_version].yaml
     - Brainstorming path: .claude/data/projects/**$PROJECT_NAME**/brainstorming_results.yaml
     - Save review to: .claude/data/projects/**$PROJECT_NAME**/book_1/bible_reviews/review_v[current_version].json
     - Be thorough but constructive
     - Provide specific improvements
     ```

2. **Read review results:**
   - Use Read tool: `.claude/data/projects/**$PROJECT_NAME**/book_1/bible_reviews/review_v[current_version].json`
   - Extract the overall_score from the review

3. **Check quality threshold:**
   - Display: "Bible V[current_version] Score: [score]/100"
   - If score >= 95: 
     - Display: "[x] Bible V[current_version] meets quality standard: [score]/100"
     - Stop iteration and proceed to finalization
   - If score < 95 and not at max iterations:
     - Continue to improvement step

4. **Generate improved version (if needed):**
   - **Use Task tool:**
     - **subagent_type**: "bible-architect"
     - **description**: "Improve Bible to V[next_version]"
     - **prompt**: Provide the following instructions:
       ```
       Improve Bible based on review feedback
       - Previous Bible: .claude/data/projects/**$PROJECT_NAME**/book_1/bible_versions/bible_v[current_version].yaml
       - Review feedback: .claude/data/projects/**$PROJECT_NAME**/book_1/bible_reviews/review_v[current_version].json
       - Focus on critical issues first
       - Preserve strengths while fixing weaknesses
       - Save improved version to: .claude/data/projects/**$PROJECT_NAME**/book_1/bible_versions/bible_v[next_version].yaml
       ```
   - Increment version number and repeat from step 1

5. **Handle max iterations:**
   - If 5 iterations completed without reaching 95:
     - Display: "WARNING:️ Warning: Max iterations reached. Final score: [score]/100"
     - Display: "Consider manual intervention or adjusting requirements."

#### 5.3 Finalize Book 1 Bible

**Copy best version as the official Bible:**
- Use Bash tool: `cp .claude/data/projects/{PROJECT_NAME}/book_1/bible_versions/bible_v{current_version}.yaml .claude/data/projects/{PROJECT_NAME}/book_1/bible.yaml`
- Display: "[x] Book 1 Bible finalized with quality score: {quality_score}/100"
- Display: "[x] Voice profile successfully inherited from Series Bible"

### Phase 6: Generate Book Outline (Iterative with Quality Gate)

#### 4.1 Create directories for outline versions

**Setup outline versioning structure:**
- Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_1/outline_versions`
- Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/book_1/outline_reviews`

#### 4.2 Generate Outline V1

**Create initial book outline from Bible:**

1. **Display progress:**
   - Display: "📚 Generating Book Outline from Bible..."

2. **Launch book-outline-architect agent:**
   - Use Task tool with:
     * subagent_type: "book-outline-architect"
     * description: "Generate outline V1"
     * prompt: """
       Create comprehensive book outline for project '{PROJECT_NAME}'
       - Bible path: .claude/data/projects/{PROJECT_NAME}/book_1/bible.yaml
       - Brainstorming path: .claude/data/projects/{PROJECT_NAME}/brainstorming_results.yaml
       - Generate outline for all {TOTAL_CHAPTERS} chapters
       - Include chapter dependencies and progression maps
       - Map tension curves and clue progression
       - Save to: .claude/data/projects/{PROJECT_NAME}/book_1/outline_versions/outline_v1.yaml
       """

3. **Verify outline V1 created:**
   - Use Read tool: `.claude/data/projects/{PROJECT_NAME}/book_1/outline_versions/outline_v1.yaml`
   - If missing, report error and stop
   - Display: "[x] Outline V1 generated"

#### 4.3 Outline Quality Review Loop

**Iteratively improve outline until quality >= 95:**

**Iterative Outline quality improvement process (up to 4 iterations):**

Starting with version 1, repeat the following steps until quality score reaches 95 or maximum iterations (4) is reached:

**For each iteration:**

1. **Review current Outline version using Task tool:**
   - **subagent_type**: "book-outline-reviewer"
   - **description**: "Review Outline V[current_version]"
   - **prompt**: Provide the following instructions:
     ```
     Review book outline quality for project '**$PROJECT_NAME**'
     - Outline path: .claude/data/projects/**$PROJECT_NAME**/book_1/outline_versions/outline_v[current_version].yaml
     - Bible path: .claude/data/projects/**$PROJECT_NAME**/book_1/bible.yaml
     - Save review to: .claude/data/projects/**$PROJECT_NAME**/book_1/outline_reviews/review_v[current_version].json
     - Be thorough but constructive
     - Focus on story structure, pacing, and completeness
     ```

2. **Read review results:**
   - Use Read tool: `.claude/data/projects/**$PROJECT_NAME**/book_1/outline_reviews/review_v[current_version].json`
   - Extract the overall_score from the review

3. **Check quality threshold:**
   - Display: "Outline V[current_version] Score: [score]/100"
   - If score >= 95:
     - Display: "[x] Outline V[current_version] meets quality standard: [score]/100"
     - Stop iteration and proceed to finalization
   - If score < 95 and not at max iterations:
     - Continue to improvement step

4. **Generate improved version (if needed):**
   - **Use Task tool:**
     - **subagent_type**: "book-outline-architect"
     - **description**: "Improve Outline to V[next_version]"
     - **prompt**: Provide the following instructions:
       ```
       Improve book outline based on review feedback
       - Previous Outline: .claude/data/projects/**$PROJECT_NAME**/book_1/outline_versions/outline_v[current_version].yaml
       - Review feedback: .claude/data/projects/**$PROJECT_NAME**/book_1/outline_reviews/review_v[current_version].json
       - Bible: .claude/data/projects/**$PROJECT_NAME**/book_1/bible.yaml
       - Focus on critical issues first, then high priority items
       - Preserve strengths while fixing weaknesses
       - Save improved version to: .claude/data/projects/**$PROJECT_NAME**/book_1/outline_versions/outline_v[next_version].yaml
       ```
   - Increment version number and repeat from step 1

5. **Handle max iterations:**
   - If 4 iterations completed without reaching 95:
     - Display: "WARNING:️ Warning: Max iterations reached. Final score: [score]/100"
     - Display: "Consider manual intervention or adjusting requirements."

#### 4.4 Finalize Outline

**Copy best version as the official outline:**
- Use Bash tool: `cp .claude/data/projects/{PROJECT_NAME}/book_1/outline_versions/outline_v{current_version}.yaml .claude/data/projects/{PROJECT_NAME}/book_1/outline.yaml`
- Display: "[x] Book Outline finalized with quality score: {quality_score}/100"
- Display key metrics: "{total_chapters} chapters, {act_count} acts, {tension_peaks} tension peaks"

### Phase 7: Initialize Project Metadata

**Create and save project metadata:**

1. **Build project metadata object with:**
   - name: PROJECT_NAME
   - type: PROJECT_TYPE (from brainstorming)
   - genre: GENRE (from brainstorming)
   - status: "planning"
   - bible_created: true
   - series_bible_created: true   # Created during project initialization
   - books_planned: 1             # Start with single book (can extend later)
   - created: current_timestamp
   - brainstorm_results: (all brainstorming answers)
   - progress:
     * total_chapters: PLANNED_CHAPTERS
     * completed_chapters: 0
     * current_chapter: 0
     * total_words: 0

2. **Save metadata:**
   - Use Write tool: `.claude/data/projects/{PROJECT_NAME}/project.json`
   - Write metadata object as JSON

### Phase 7: Initialize Context

#### 5.1 [ENHANCED] Initialize Entity Dictionary

**Create entity dictionary from Bible:**

1. **Create shared directory:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{PROJECT_NAME}/shared`

2. **Initialize entity dictionary using subagent:**
   - Display: "📚 Creating Entity Dictionary from Bible..."
   - Use Task tool with subagent_type: "entity-dictionary-creator"
   - Description: "Create entity dictionary"
   - Prompt: "Create entity dictionary for project '{PROJECT_NAME}' from bible at '.claude/data/projects/{PROJECT_NAME}/book_1/bible.yaml'. Extract all characters, locations, and objects. Save to .claude/data/projects/{PROJECT_NAME}/shared/entity_dictionary.yaml"

3. **Verify creation:**
   - Use Read tool: `.claude/data/projects/{PROJECT_NAME}/shared/entity_dictionary.yaml`
   - Display: "[x] Entity Dictionary created successfully"

#### 5.2 Character Context

**Initialize character tracking:**

1. **Build character context object:**
   - protagonists: (extract from Bible)
   - antagonists: (extract from Bible)
   - supporting: (extract from Bible)
   - development_tracking: empty dictionary

2. **Save character context:**
   - Use Write tool: `.claude/data/projects/{PROJECT_NAME}/book_1/context/characters.json`
   - Write character context as JSON

#### 5.3 Plot Context

**Initialize plot tracking:**

1. **Build plot context object:**
   - main_arc: (extract from Bible)
   - subplots: (extract from Bible)
   - completed_events: empty array
   - upcoming_events: empty array

2. **Save plot context:**
   - Use Write tool: `.claude/data/projects/{PROJECT_NAME}/book_1/context/plot.json`
   - Write plot context as JSON

#### 5.4 World Context

**Initialize world tracking:**

1. **Build world context object:**
   - setting: (extract from Bible)
   - locations: (extract from Bible)
   - rules: (extract from Bible)
   - discovered_elements: empty array

2. **Save world context:**
   - Use Write tool: `.claude/data/projects/{PROJECT_NAME}/book_1/context/world.json`
   - Write world context as JSON

### Phase 8: Set as Current Project

**Mark this project as the active project:**

1. **Build current project object:**
   - project: PROJECT_NAME
   - type: PROJECT_TYPE
   - switched_at: current_timestamp

2. **Save as current project:**
   - Use Write tool: `.claude/data/projects/{PROJECT_NAME}/current_project.json`
   - Write current project object as JSON
   
3. **Also update global current project (if needed):**
   - Check if `.claude/data/context/` directory exists
   - If yes, use Write tool: `.claude/data/context/current_project.json`
   - Write current project reference as JSON

### Phase 9: Generate Planning Documents

Create initial planning documents based on project type:

#### For Series
- Series roadmap
- Book breakdown
- Character evolution arcs

#### For Standalone
- Chapter outline
- Pacing plan
- Climax structure

## Success Output

```
[x] 项目 "$PROJECT_NAME" 创建成功！

📚 项目类型: $PROJECT_TYPE
🎭 小说类型: $GENRE
📖 目标规模: $TOTAL_CHAPTERS 章

📋 Bible生成过程:
   Version 1: Score 75/100 - 基础结构完成
   Version 2: Score 88/100 - 增强角色弧光
   Version 3: Score 96/100 [x] - 达到质量标准

📁 项目结构:
.claude/data/projects/$PROJECT_NAME/
+-- series_brainstorming.yaml   [x] 系列头脑风暴
+-- series_bible.yaml           [x] 系列圣经 (含author_voice_signature)
+-- project.json                [x] 项目配置
+-- book_1/                     📚 第一本书
|   +-- book_brainstorming.yaml [x] Book1头脑风暴
|   +-- bible.yaml              [x] 书籍圣经已生成 (96分，继承Series声纹)
|   +-- outline.yaml            [x] 书籍大纲已生成 (94分)
|   +-- bible_versions/         📚 Bible迭代历史
|   |   +-- bible_v1.yaml       
|   |   +-- bible_v2.yaml       
|   |   +-- bible_v3.yaml       
|   +-- bible_reviews/          📊 质量评审记录
|   |   +-- review_v1.json      
|   |   +-- review_v2.json      
|   |   +-- review_v3.json      
|   +-- outline_versions/       📋 大纲迭代历史
|   +-- outline_reviews/        📊 大纲评审记录
|   +-- chapters/               📝 章节目录 (准备就绪)
|   +-- context/                🧠 书籍级上下文
|       +-- characters.json     [x] 角色追踪
|       +-- plot.json          [x] 剧情追踪
|       +-- world.json         [x] 世界设定
+-- shared/                     🔗 系列共享资源
|   +-- entity_dictionary.yaml [x] 实体字典
+-- global_context/             🌍 系列级上下文

📝 下一步: 
   1. /novel:chapter-start 1 - 开始写第一章
   2. /novel:status - 查看项目详情
   3. 查看Bible: cat .claude/data/projects/$PROJECT_NAME/book_1/bible.yaml
   4. 查看系列规划: cat .claude/data/projects/$PROJECT_NAME/series_bible.yaml
```

## Error Handling

- If project name already exists: Prompt for different name or confirm overwrite
- If brainstorming interrupted: Save partial results and allow resume
- If Bible generation fails: Retry with manual input option


## Notes

- This command now includes the full brainstorming and Bible creation process
- The separate `/novel:bible-create` command becomes optional (for re-creating or updating Bible)
- All project decisions are made upfront during creation
- Project type determines the file structure and workflow
