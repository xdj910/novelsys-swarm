# T1 Profile Initialization Command

Initialize or update author profile for consistent voice and strategic positioning across all T1-TTD articles.

## Usage

```bash
/t1-profile-init              # Initialize new profile (interactive Q&A)
/t1-profile-init --update     # Update existing profile sections
/t1-profile-init --show       # Display current profile
```

## Command Overview

**Purpose**: Guide users through profile customization to establish:
- Author identity and expertise
- Voice characteristics and style
- Quality standards and preferences
- Content approach and positioning

**Time Investment**: 10-15 minutes one-time setup

**Value**: Saves 5-10 minutes per article through automatic voice consistency and strategic alignment.

## Profile System Benefits

### 1. Consistent Voice
- Every article inherits your voice automatically
- Recognizable author brand develops naturally
- Less per-article configuration needed

### 2. Personalized Topic Suggestions
- Topic-suggester considers your expertise
- Strategic alignment with your domains
- Relevant trend recommendations

### 3. Quality Standards Enforcement
- Your accuracy requirements applied
- Revision tolerance respected
- Collaboration preferences followed

### 4. Faster Article Creation
- 80% of voice defined upfront
- Only 20% per-article customization
- Confirmed_topic inherits profile + adds specifics

### 5. Contradiction Prevention (NEW v1.5.1)
- **7 validation rules** prevent profile inconsistencies
- **Three-layer validation** ensures internal coherence
- **Smart warnings** explain trade-offs during setup
- **Critical blocking** prevents impossible configurations
- **Future-proof quality**: No contradictions that degrade articles later

## Command Delegation

Main Claude orchestrates profile initialization through systematic agent coordination:

### Mode 1: Initialize New Profile

**User Intent**: First-time setup or complete re-initialization

**Workflow**:
```yaml
Step 1: Profile Status Check
  Action: Read .claude/profiles/author_profile.yaml
  Check: Is profile still default template?
  Detection: name = "Default Author" indicates default

Step 2: Explain Benefits
  Display: Profile system advantages
  Time investment: 10-15 minutes
  Value proposition: Consistent voice, faster creation

Step 3: Confirm Intent
  Ask: "Ready to customize your profile? (yes/no)"
  If no: Exit gracefully
  If yes: Proceed to initialization

Step 4: Launch Profile Initializer
  Task -> t1-profile-initializer
  Mode: "init"
  Profile path: .claude/profiles/author_profile.yaml
  Workspace: .claude/profiles/

  Agent executes interactive Q&A:
    - Author identity (name, expertise, background)
    - Voice characteristics (tone, style, avoid)
    - Content preferences (depth balance, evidence types)
    - Quality standards (accuracy, sources, originality)

Step 5: Profile Generation
  Agent generates customized author_profile.yaml
  Creates profile_initialization_report.md
  Returns completion status to Main Claude

Step 6: Success Confirmation
  Display: Initialization summary
  Show: Author name, expertise, voice summary
  Guide: Next steps - try /t1-ttd-article

Step 7: Usage Instructions
  Explain: How profile affects article creation
  Show: Expected improvements in workflow
  Suggest: Create first article to see benefits
```

**Expected Output**:
```
Profile initialization completed successfully.

Author: {your_name}
Expertise: {domains_summary}
Voice: {tone_summary}
Quality Standards: {standards_summary}

Your profile is ready. Articles will now:
- Inherit your voice automatically
- Align with your expertise
- Meet your quality standards

Profile saved: .claude/profiles/author_profile.yaml
Report: .claude/profiles/profile_initialization_report.md

Ready to create your first article? Try:
/t1-ttd-article "your topic idea"
```

### Mode 2: Update Existing Profile

**User Intent**: Modify specific sections without complete re-initialization

**Workflow**:
```yaml
Step 1: Profile Status Check
  Action: Read current author_profile.yaml
  Display: Current profile summary
  Confirm: Profile is customized

Step 2: Update Options
  Display: "Your profile: {author_name}"
  Ask: "What would you like to update?"
  Options:
    1) Author identity (name, expertise)
    2) Voice characteristics (tone, style)
    3) Content preferences (depth, evidence)
    4) Quality standards (accuracy, sources)
    5) Complete re-initialization
    6) Cancel

Step 3: Backup Current Profile
  Create: profile_backup_{timestamp}.yaml
  Purpose: Allow rollback if needed

Step 4: Launch Profile Initializer
  Task -> t1-profile-initializer
  Mode: "update"
  Skip sections: Based on user selection
  Profile path: .claude/profiles/author_profile.yaml

  Agent executes targeted Q&A:
    - Show current values for context
    - Prompt only for selected sections
    - Allow "press Enter to keep" for quick updates

Step 5: Profile Update
  Agent updates author_profile.yaml
  Preserves unchanged sections
  Creates update report

Step 6: Confirmation
  Display: Updated sections summary
  Backup: Previous version saved
  Guide: Changes take effect immediately
```

**Expected Output**:
```
Profile updated successfully.

Updated Sections:
- Voice characteristics: Tone changed to "analytical and precise"
- Quality standards: Accuracy raised to "High"

Unchanged: Author identity, Content preferences

Backup: .claude/profiles/profile_backup_20250928_153045.yaml
Profile: .claude/profiles/author_profile.yaml

Changes will apply to all new articles.
```

### Mode 3: Show Current Profile

**User Intent**: View current profile configuration

**Workflow**:
```yaml
Step 1: Read Profile
  Action: Read author_profile.yaml
  Parse: All sections

Step 2: Launch Profile Initializer
  Task -> t1-profile-initializer
  Mode: "show"
  Profile path: .claude/profiles/author_profile.yaml

  Agent generates formatted display:
    - Author identity summary
    - Voice characteristics
    - Content preferences
    - Quality standards
    - Profile status (customized/default)

Step 3: Display Profile
  Show: Complete formatted profile
  Offer: Actions (update, edit, exit)
```

**Expected Output**:
```
Your Current Author Profile
============================

Author Identity
---------------
Name: Jane Smith
Expertise: AI Safety, Machine Learning, Ethics
Background: AI Researcher, Policy Advisor
Unique Perspective: Cross-disciplinary analysis, practical ethics

Voice Characteristics
--------------------
Primary Tone: Analytical and balanced
Secondary Tone: Accessible and engaging
Style Elements: Research citations, real-world examples, ethical frameworks

Content Preferences
------------------
Depth Balance: Analysis 70%, Narrative 20%, Practical 10%
Evidence Types: Academic research, expert interviews, case studies

Quality Standards
----------------
Accuracy: High - all claims must be verifiable
Originality: Significant unique insights required
Revision Tolerance: High - willing to iterate

Actions:
1. Update profile: /t1-profile-init --update
2. Edit directly: .claude/profiles/author_profile.yaml
```

## Integration with Article Creation

Profile is automatically used by T1-TTD system:

**Phase 1: Topic Exploration**
- t1-inspiration-parser reads profile for context
- t1-topic-suggester aligns with expertise domains
- Strategic positioning matches your authority

**Phase 2: Content Creation**
- Voice characteristics guide tone and style
- Quality standards enforced automatically
- Content preferences shape structure

**Phase 3: Quality Validation**
- Voice consistency checked against profile
- Accuracy requirements determine thresholds
- Originality evaluated by your standards

## When to Initialize Profile

### Recommended: Before First Article
```bash
# First time using T1-TTD
/t1-profile-init              # 10-15 minutes setup
/t1-ttd-article "topic"       # Articles use your profile
```

**Benefits**:
- Immediate voice consistency
- Better topic suggestions from start
- Quality standards clear

### Alternative: After First Article
```bash
# Try system with defaults first
/t1-ttd-article "topic"       # Uses default profile
# Then customize based on experience
/t1-profile-init              # Refine based on learnings
```

**Benefits**:
- Understand system before customization
- Know what to optimize
- Informed profile decisions

## When to Update Profile

Update profile when:
- **Expertise evolves**: New domains or focus areas
- **Writing style changes**: Tone or voice refinement
- **Quality preferences shift**: Standards adjustment
- **Strategic repositioning**: New audience or platform

Command: `/t1-profile-init --update`

## Profile vs Per-Article Customization

**Hybrid Approach** (Recommended):

**Profile (80% - One time)**:
- Core identity and expertise
- Default voice and tone
- General quality standards
- Typical content preferences

**Per-Article (20% - Each article)**:
- Topic-specific strategic angle
- Article-specific voice nuances
- Context-dependent depth balance
- Unique positioning for topic

**Result**: Consistency + Flexibility

## Profile Validation System (v1.5.1)

### Why Validation Matters

Previous versions allowed contradictory settings like:
- "70% analysis depth" with "800-word platform limit" (physically impossible)
- "Academic research evidence" with "Medium accuracy" (logically inconsistent)
- "Independent voice" with "Authoritative sources only" (philosophically unclear)

**Result**: Articles failed to meet profile expectations, quality degraded.

**Solution**: Three-layer validation with 7 embedded rules catches contradictions during setup.

### Three-Layer Validation Architecture

**Layer 1: Real-Time Field Validation**
- Validates each answer immediately after user input
- Checks: Non-empty, correct format, valid range
- Example: Depth balance must total 100%
- Applied: During Q&A, instant feedback

**Layer 2: Cross-Field Consistency Checks**
- Validates relationships between related fields
- Checks: Accuracy vs evidence, depth vs engagement
- Example: High evidence requires High accuracy
- Applied: After completing each major section

**Layer 3: Final Comprehensive Review**
- Validates entire profile before generation
- Runs all 7 rules, displays summary with status
- Requires user confirmation to proceed
- Applied: Before profile creation, final safeguard

### 7 Validation Rules

**Rule 1: Accuracy-Evidence Consistency** (BLOCK for Flexible, WARN for Medium - v1.5.1)
```
What it checks: Does accuracy standard match evidence complexity?

BLOCK violation:
  - Evidence: 4+ types including "Academic research"
  - Accuracy: "Flexible - clarity over verification"

Problem: Academic research incompatible with flexible verification standards

Resolution: Change accuracy to "Medium" or "High" OR remove academic research

WARN situation:
  - Evidence: 4+ types including "Academic research"
  - Accuracy: "Medium - key claims verified, personal insights allowed"

Explanation: Medium accuracy can work if academic sources provide background context
             rather than primary claim verification. Key claims still verified.

User choice: Accept warning (Medium works for context use) OR upgrade to High
```

**Rule 2: Depth-Platform Feasibility** (WARN if strained)
```
What it checks: Can analysis depth fit platform word limits?

Example warning:
  - Analysis: 70%
  - Platform: Substack 1000 words = 700 words for analysis

Explanation: T1-length-controller compresses intelligently
  - Priority 1 (preserved): Authentic insights, verified facts, core arguments
  - Priority 2 (compressed): Supporting examples, background context
  - Priority 3 (reduced): Redundancy, transitions

User confirms understanding before proceeding
```

**Rule 3: Voice-Source Alignment** (WARN if unclear)
```
What it checks: Does independent voice conflict with authoritative sources?

Example warning:
  - Unique perspective: "Independent voice vs corporate narrative"
  - Sources: "Authoritative industry sources preferred"

Solution: Add source integration philosophy:
  "Use authoritative sources for factual grounding.
   Apply independent analysis to interpret and critique.
   Independent voice means independent interpretation."

Clarifies relationship, prevents confusion
```

**Rule 4: Originality-Evidence Trade-off** (WARN if imbalanced)
```
What it checks: Balance between originality and evidence depth

Example warning:
  - Originality: "High - significant unique insights required"
  - Evidence: 2 types only

Recommendation: High originality needs strong evidence foundation (3+ types)

User decides final balance
```

**Rule 5: Revision-Accuracy Alignment** (BLOCK if violated)
```
What it checks: Does revision willingness match accuracy standards?

Example violation:
  - Accuracy: "High - all claims must be verifiable"
  - Revision: "Low - prefer rapid publication"

Problem: High accuracy requires 3-5 iteration rounds in T1-TTD

Resolution: Change revision to "Medium" (minimum) OR "High" (optimal)
```

**Rule 6: Depth-Engagement Strategy** (WARN if mismatched)
```
What it checks: Do engagement strategies match content depth?

Example warning:
  - Analysis: 70% (deep analytical content)
  - Engagement: "Interactive elements, community prompts" only

Recommendation: Deep analysis needs:
  - Thought-provoking questions
  - Counterintuitive insights
  - Strategic implications

User can adjust or accept
```

**Rule 7: Platform-Specific Length Reality Check** (WARN - v1.5.1 Educational)
```
What it checks: Does user understand 2025 platform specifications?

Displays during setup:
  "2025 Platform Targets (after compression):
   - Medium: 1400-2100 words (optimal: 1800)
   - Substack: 800-1200 words (optimal: 1000)
   - ElevenReader: 2500-5000 words (optimal: 3500)

   Your draft generates at full depth.
   T1-length-controller compresses intelligently to targets.

   Analysis X% means X% preserved in final output after compression."

Educational approach (v1.5.1):
  - Explains compression strategy with priority levels
  - Confirms user understanding: "Confirm to proceed"
  - WARN if user sets 70%+ analysis (explains compression impact)
  - Never blocks (education through warning, not blocking)

Purpose: Ensure informed decisions about depth settings, not test comprehension
```

### Validation Modes: Block vs Warn vs Suggest (v1.5.1 Updated)

**BLOCK (Critical - Must Resolve)** - Only 2 rules:
- Rule 1: Flexible accuracy with academic research (incompatible combination)
- Rule 5: High accuracy without adequate revision (T1-TTD requires iteration)

**User cannot proceed** with BLOCK-level contradictions. Must adjust settings or go back.

**WARN (Important - Should Understand)** - 5 rules:
- Rule 1: Medium accuracy with 4+ evidence types including academic (workable if research for context)
- Rule 2: Analysis depth may strain platform limits (compression strategy explained)
- Rule 3: Independent voice needs source integration philosophy (clarification helpful)
- Rule 4: Originality-evidence imbalance (optimization available)
- Rule 6: Depth-engagement strategy mismatch (strategy alignment)
- Rule 7: Platform awareness education (never blocks, always warns)

**User can proceed** after reading explanation and confirming understanding.

**SUGGEST (Optimization Available)**:
- All rules can suggest improvements when valid but suboptimal

**User can ignore** suggestions if they prefer current settings.

**Key Change in v1.5.1**: Reduced from 3 blocking rules to 2. Rule 1 now warns for Medium+academic (not blocks), Rule 7 never blocks (educational only).

### Example Validation Flow

**Scenario**: User creating AI researcher profile

**Section 3: Content Preferences**
```
Q: Evidence types? (Select 2-4)
A: 1,2,3,4 (Statistics, Academic research, Expert interviews, Case studies)

[Layer 1 validation: PASS - 4 types selected, valid range]

Q: Depth balance?
A: 70,20,10 (Analysis 70%, Narrative 20%, Practical 10%)

[Layer 1 validation: PASS - Totals 100%]
[Rule 7 triggered: Display platform targets + compression explanation]

"2025 Platform Targets:
 - Substack: 1000 words optimal
 - Your 70% analysis = 700 words for analytical content
 - T1-length-controller uses priority-based compression

 Understand compression strategy? (yes/no)"

User: yes

[Layer 2 validation after Section 3: Rule 6 check]
[Rule 6: PASS - 70% analysis with no engagement strategies set yet, will check later]
```

**Section 4: Quality Standards**
```
Q: Accuracy requirements?
A: 2 (Medium - key claims verified, personal insights allowed)

Q: Revision tolerance?
A: 2 (Medium - 2-3 rounds acceptable)

[Layer 2 validation after Section 4: Rules 1, 4, 5 checks]

[Rule 1 triggered: BLOCK]

"ERROR: Profile Contradiction Detected

Your settings:
  - Evidence: 4 types including Academic research
  - Accuracy: Medium

Problem: Academic research requires High accuracy for verification.

Resolution:
  1) Change accuracy to High (recommended)
  2) Remove academic research from evidence
  3) Reconsider evidence depth

Choose (1/2/3):"

User: 1 (Change to High accuracy)

[Rule 1 re-check: PASS]
[Rule 5 check: High accuracy + Medium revision = WARN]

"WARNING: High accuracy with Medium revision

High accuracy achieves best results with High revision tolerance.
T1-TTD typically needs 3-5 rounds for >=85% accuracy.

Recommendation: Change revision to High

Continue with Medium revision? (yes/no)"

User: no, change to High

[Rule 5 re-check: PASS]
[All Section 4 rules: PASS]
```

**Final Pre-Generation Review (Layer 3)**
```
"Profile Consistency Check

Rule 1: Accuracy-evidence -> PASS
Rule 2: Depth-platform -> PASS (700 words sufficient with compression)
Rule 3: Voice-source -> PASS (no conflict)
Rule 4: Originality-evidence -> PASS (4 evidence types support High originality)
Rule 5: Revision-accuracy -> PASS (High revision supports High accuracy)
Rule 6: Depth-engagement -> PASS (engagement strategies appropriate)
Rule 7: Platform awareness -> PASS (user understands compression)

Profile Validation: 7 rules passed, 0 warnings

Your profile is internally consistent and production-ready.

Continue to profile generation? (yes/no)"

User: yes

[Proceed to profile generation]
```

### Benefits of Validation System

**Prevents Future Problems**:
- No contradictions that degrade article quality later
- No impossible configurations that cause workflow failures
- No confusion about how settings interact

**Educational Value**:
- Explains platform constraints during setup
- Shows how settings affect article creation
- Guides optimal configuration choices

**Time Savings**:
- Catches issues during 15-minute setup vs discovering over weeks
- Prevents profile redesign after multiple articles
- Reduces support questions about unexpected behavior

**Quality Assurance**:
- Ensures profile can achieve stated quality targets
- Validates accuracy-evidence consistency
- Confirms revision tolerance matches standards

### Troubleshooting Validation Issues

**Issue: "I want Low revision but High accuracy"**
```
Why blocked: T1-TTD achieves >=85% accuracy through iteration cycles

Solution:
  - Change revision to Medium (minimum for High accuracy)
  - OR change accuracy to Medium (if rapid publication priority)
  - OR understand: High accuracy requires multiple rounds

System protects you from setting impossible expectations
```

**Issue: "I want 4 evidence types but Medium accuracy"**
```
Why blocked: Academic research requires rigorous verification

Solution:
  - Change accuracy to High (aligns with evidence depth)
  - OR remove academic research (keep Medium accuracy with 2-3 types)
  - OR understand: More evidence types = higher accuracy requirements

System ensures evidence matches verification standards
```

**Issue: "Warning about 70% analysis in 800 words"**
```
Why warned: Platform limits may constrain analytical depth

Explanation:
  - Substack optimal: 1000 words
  - 70% analysis = 700 words analytical content
  - T1-length-controller compresses intelligently
  - Priority 1 content (authentic insights) always preserved

Action: Confirm you understand compression strategy

This is educational, not blocking
```

**Issue: "Validation keeps rejecting my choices"**
```
What's happening: Profile has logical contradictions

Solution:
  1) Read error messages carefully - they explain the problem
  2) Choose one of the offered resolutions
  3) If unsure, select "recommended" option
  4) Validation guides you to consistent configuration

System wants internally coherent profile, not arbitrary restrictions
```

## Error Handling

### Profile Not Found
```
Creating new profile from template...
Ready to customize your author profile.
```
- Creates default template automatically
- Proceeds with initialization

### Invalid YAML Syntax
```
ERROR: Profile has invalid YAML syntax
Line 23: Unexpected character

Options:
1) Fix manually and retry
2) Start fresh with new profile
3) Restore from backup (if available)
```
- Shows specific error location
- Offers recovery options
- Preserves data when possible

### User Cancels
```
Profile initialization cancelled.
No changes made.

Current profile unchanged: {author_name}
Try again anytime: /t1-profile-init
```
- Graceful exit
- No modifications
- Clear next steps

## File Locations

**Profile**:
- `.claude/profiles/author_profile.yaml` - Active profile
- `.claude/profiles/profile_backup_{timestamp}.yaml` - Backups (on update)

**Reports**:
- `.claude/profiles/profile_initialization_report.md` - Setup summary
- `.claude/profiles/insight_authenticity_profile.yaml` - Reference for authenticity standards

**Templates**:
- Default template embedded in t1-profile-initializer agent

## Tips for Effective Profiles

### 1. Be Specific
```yaml
Generic: "Professional and informative"
Specific: "Analytical with accessible explanations, evidence-based but conversational"
```

### 2. Match Your Actual Voice
```yaml
Don't aspire: "Academic and scholarly" (if you're not)
Be authentic: "Practitioner insights with business focus" (if you are)
```

### 3. Consider Your Audience
```yaml
Business leaders: "Strategic implications, ROI focus"
Researchers: "Rigorous analysis, peer-reviewed sources"
General readers: "Accessible explanations, real-world examples"
```

### 4. Set Realistic Standards
```yaml
If you're prolific: "Medium accuracy, good enough is publishable"
If you're perfectionist: "High accuracy, willing to iterate extensively"
```

## Examples

### Example 1: AI Researcher Profile
```yaml
Name: Dr. Sarah Chen
Expertise: AI Safety, Machine Learning, Ethics in AI
Tone: Analytical and balanced, accessible
Style: Research citations, ethical frameworks, balanced perspectives
Evidence: Academic research, expert interviews, case studies
Accuracy: High - all claims verifiable
Originality: Significant unique insights required
```

### Example 2: Product Manager Profile
```yaml
Name: Mike Johnson
Expertise: Product Management, User Experience, Startup Growth
Tone: Conversational and practical, avoid academic jargon
Style: Real-world case studies, actionable frameworks, lessons learned
Evidence: Industry data, personal experience, user research
Accuracy: Medium - key claims verified, insights prioritized
Originality: Fresh angle on known topics acceptable
```

### Example 3: Financial Analyst Profile
```yaml
Name: Alex Rivera
Expertise: Financial Markets, Investment Strategy, Risk Management
Tone: Professional yet approachable, data-driven
Style: Statistical analysis, market examples, strategic frameworks
Evidence: Financial data, historical patterns, quantitative models
Accuracy: High - all statistics must be sourced
Originality: High - proprietary analysis and unique perspectives
```

## FAQ

**Q: Do I have to use the profile system?**
A: No, default profile works fine. But customization improves consistency and saves time long-term.

**Q: How long does initialization take?**
A: 10-15 minutes for initial setup. Updates are faster (2-5 minutes).

**Q: Can I edit the profile file directly?**
A: Yes, edit `.claude/profiles/author_profile.yaml` directly. Follow YAML syntax carefully.

**Q: Does profile limit what topics I can write about?**
A: No, profile provides defaults. Each article can still explore any topic.

**Q: What if my style varies by topic?**
A: Set general profile for your core voice. Customize confirmed_topic for specific articles.

**Q: Can I have multiple profiles?**
A: Currently one profile per system. Consider profile as your default/primary voice.

**Q: How do I rollback a bad update?**
A: Use backup files in `.claude/profiles/profile_backup_*.yaml`. Restore and run `/t1-profile-init --update`.

## Success Metrics

Good profile initialization shows:
- Profile reflects YOUR actual voice (not generic)
- Expertise domains align with writing goals
- Quality standards are realistic and actionable
- You feel confident system will match your style
- First article demonstrates voice consistency

## Next Steps

After initializing profile:

1. **Create First Article**: `/t1-ttd-article "your topic"`
2. **Observe Integration**: Notice how profile affects suggestions and voice
3. **Refine If Needed**: `/t1-profile-init --update` to adjust
4. **Build Consistency**: Multiple articles develop recognizable brand

## See Also

- **Profile Usage Guide**: `.claude/profiles/PROFILE_USAGE_GUIDE.md`
- **T1-TTD System**: `/t1-ttd-article` command documentation
- **Author Profile Reference**: `.claude/profiles/author_profile.yaml`

---

**Command Version**: 1.0
**Created**: 2025-09-28 (P2 Fix #3)
**Purpose**: Improve user experience and leverage profile system
**Integration**: Works with existing T1-TTD v1.4.1 system