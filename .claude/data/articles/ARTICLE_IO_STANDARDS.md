# Article I/O Standards and Quality Requirements
*Comprehensive input/output specifications for all art-* agents in the Article Production System*

**Version**: 2.0
**Created**: 2025-09-18
**Updated**: 2025-09-21
**Status**: Active with User Materials Integration
**Purpose**: Define minimum requirements and quality standards for each agent

---

## Overview

This document defines the input/output specifications and quality requirements for each agent in the article production system with user materials integration. Each agent can exceed requirements but must meet the minimum standards.

### Core Principles

1. **Quality First** - Every output must meet minimum quality standards
2. **Intelligent Detection** - Agents actively assess completion and quality
3. **User Confirmation** - Critical decisions require user approval
4. **Progressive Enhancement** - Can exceed requirements for excellence
5. **User Materials Integration** - Leverage user research when available

---

## Agent I/O Specifications

### Phase 1: Brainstorming & Strategy

**Note**: Phase 1 is handled directly by Main Claude through interactive brainstorming process.
No dedicated agent - the art-workflow-coordinator guides the interactive strategy development.

---

### Phase 2: Article Initiation

#### art-article-initiator

**Purpose**: Create article folder structure and initialize metadata with user materials support

**Input Requirements**:
```yaml
Required:
  - topic: string (article subject from user)
  - article_type: string (e.g., "ai_realist")
  - working_directory: path (base directory for article creation)

Optional:
  - specific_angle: string
  - initial_metadata: object
```

**Output Requirements**:
```yaml
Minimum Standards:
  Folder Structure:
    - 8 subdirectories created: user_materials/, processed/, agent_outputs/, drafts/, reports/, visuals/, published/, images/
    - All directories accessible with proper permissions

  metadata.json:
    - article_id: generated in YYYYMMDD_HHMMSS_topic_slug format
    - topic: original topic string
    - type: article type identifier
    - created: ISO timestamp
    - status: "initiated"
    - phase: "user_materials_check"
    - target_word_count: 2000
    - user_materials: initialization object with has_materials: false
    - progress: all phases initialized to "pending"
    - citation_requirements: inline_hyperlinks_only
    - strategy_files: paths to strategy and voice guide

Quality Metrics:
  - folder_creation: 100% success required (including new 3-folder structure)
  - metadata_validity: valid JSON required with user materials tracking
  - path_resolution: all paths accessible
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Folder structure created successfully. 8/8 directories verified including user materials integration."
  - "Metadata initialized with user materials tracking. Ready for materials check phase."
  - "Article ID generated: 20250921_143022_ai_risks. Unique and valid."
```

---

### Phase 3A: User Materials Processing (NEW)

#### art-materials-processor

**Purpose**: Analyze user-provided materials and extract insights for research integration

**Input Requirements**:
```yaml
Required:
  - working_directory: path (absolute path to article folder)
  - topic: string (from metadata.json)

Optional:
  - analysis_depth: string ("standard" | "deep")
  - focus_areas: array of specific areas to emphasize
```

**Output Requirements**:
```yaml
Minimum Standards:
  processed/materials_insights.md:
    executive_summary:
      - 3-5 key insights from user materials
      - Priority assessment based on PRIORITY_, CORE_, SUPP_ prefixes
      - Integration recommendations for research agents

    prioritized_insights:
      - High priority findings (from PRIORITY_ files): minimum 2 if present
      - Core themes (from CORE_ files): minimum 3 if present
      - Supporting context (from SUPP_ files): cataloged and summarized

    research_guidance:
      - Specific areas for agent investigation: minimum 3
      - Gaps where additional research needed: minimum 2
      - Unique angles to explore further: minimum 2

    data_extraction:
      - Statistics and data points from materials
      - Expert quotes and attributions
      - Sources for fact-checking and verification
      - User-specific insights not available in public research

Quality Metrics:
  - materials_coverage: 100% of provided materials analyzed
  - priority_system_application: correct categorization and weighting
  - insight_quality: actionable guidance for research agents
  - integration_readiness: clear instructions for research integration
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Found 7 user materials: 2 PRIORITY, 3 CORE, 2 SUPP. All analyzed."
  - "Extracted 12 unique insights not available in public research."
  - "Generated research guidance covering 5 specific investigation areas."
```

**Fallback Behavior**:
```yaml
No User Materials:
  - Skip processing gracefully
  - Create minimal materials_insights.md indicating no materials
  - Allow workflow to proceed to Phase 3B without interruption
```

---

### Phase 3B: Research Collection (Updated with Materials Integration)

#### art-trend-researcher

**Purpose**: Analyze market trends and emerging patterns with user materials integration

**Input Requirements**:
```yaml
Required:
  - topic: string
  - target_audience: object (from strategy)
  - research_scope: string ("broad" | "focused" | "deep")
  - working_directory: path (absolute path to article folder)

Optional:
  - time_frame: string (default: "last_12_months")
  - geographic_focus: array
  - industry_sectors: array
  - user_materials_insights: processed/materials_insights.md (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  agent_outputs/trends.md:
    user_materials_integration:
      - section: if materials available, lead with user insights
      - user_trends: trends identified from user materials
      - validation: cross-reference user trends with public research

    current_trends:
      - count: minimum 5 (can include user-identified trends)
      - description: 50-100 words each
      - data_support: minimum 2 statistics per trend
      - source_quality: authoritative sources only
      - user_correlation: note alignment with user insights where applicable

    emerging_patterns:
      - count: minimum 3
      - evidence: minimum 3 indicators each
      - timeline: estimated emergence period
      - user_perspective: incorporate user forward-looking insights

    market_dynamics:
      - growth_areas: minimum 3
      - declining_areas: minimum 2
      - disruption_factors: minimum 3
      - user_intelligence: incorporate user market observations

    statistics:
      - relevant_data_points: minimum 10
      - sources: properly cited with inline hyperlinks
      - recency: < 12 months old (unless historical comparison)
      - user_data: include relevant user-provided statistics

Quality Metrics:
  - data_reliability: >= 95%
  - source_authority: >= 90%
  - relevance_score: >= 85%
  - completeness: >= 90%
  - user_integration: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Found 7 major trends (3 from user materials, 4 from research). Coverage sufficient?"
  - "User insights identified regulatory trend 6 months before public discussion. High value."
  - "Cross-validated user market data with 3 independent sources. Alignment: 94%."
```

#### art-audience-analyst

**Purpose**: Deep dive into target audience psychology and needs with user insights

**Input Requirements**:
```yaml
Required:
  - topic: string
  - target_audience: object (from strategy)
  - analysis_depth: string ("surface" | "standard" | "deep")
  - working_directory: path (absolute path to article folder)

Optional:
  - demographic_data: object
  - psychographic_hints: array
  - survey_data: object
  - user_materials_insights: processed/materials_insights.md (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  agent_outputs/audience.md:
    user_materials_integration:
      - user_audience_insights: audience data from user materials
      - validation: cross-reference with public research
      - unique_perspectives: user insights not available publicly

    audience_profile:
      - demographics: minimum 5 dimensions (enhanced with user data)
      - psychographics: minimum 5 traits
      - knowledge_level: clear assessment with evidence
      - content_preferences: minimum 5 identified
      - user_observations: incorporate user audience experience

    pain_points:
      - count: minimum 5
      - severity_ranking: 1-10 scale
      - evidence: quotes or data supporting each
      - emotional_impact: described for each
      - user_validation: confirmation from user materials where available

    information_needs:
      - must_know: minimum 5 items
      - want_to_know: minimum 5 items
      - surprised_by: minimum 3 items
      - user_priorities: audience priorities identified by user

    engagement_patterns:
      - preferred_formats: minimum 3
      - consumption_habits: minimum 5 behaviors
      - sharing_triggers: minimum 3
      - action_triggers: minimum 3
      - user_experience: incorporate user audience interaction data

Quality Metrics:
  - profile_depth: >= 85%
  - insight_quality: >= 80%
  - actionability: >= 90%
  - user_integration: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "User provided unique audience segment data: technical beginners in enterprise. Significant gap in public research."
  - "Cross-validated user pain points with industry surveys. 89% alignment."
  - "User engagement data reveals preference shift not yet in public studies."
```

#### art-competitor-scanner

**Purpose**: Analyze competitive content landscape with user competitive intelligence

**Input Requirements**:
```yaml
Required:
  - topic: string
  - target_keywords: array
  - analysis_scope: integer (number of competitors)
  - working_directory: path (absolute path to article folder)

Optional:
  - specific_competitors: array
  - platform_focus: array
  - time_range: string
  - user_materials_insights: processed/materials_insights.md (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  agent_outputs/competitors.md:
    user_materials_integration:
      - user_competitive_intelligence: competitor insights from user materials
      - insider_knowledge: user observations not publicly available
      - market_positioning: user perspective on competitive landscape

    analyzed_content:
      - count: minimum 5 pieces
      - platforms: source diversity required
      - recency: at least 3 within last 6 months
      - user_additions: competitors identified by user not in initial research

    content_gaps:
      - identified_gaps: minimum 3
      - opportunity_size: estimated for each
      - difficulty_level: assessed for each
      - user_insights: gaps identified through user experience

    successful_patterns:
      - patterns: minimum 5 identified
      - evidence: engagement metrics or shares
      - applicability: assessed for our context
      - user_observations: patterns noted by user from market experience

    differentiation_opportunities:
      - unique_angles: minimum 3
      - uncovered_topics: minimum 2
      - innovative_formats: minimum 2
      - user_advantages: leverage user unique knowledge/position

    benchmark_metrics:
      - average_length: calculated
      - engagement_rates: if available
      - quality_indicators: assessed
      - user_performance: user content performance vs competitors

Quality Metrics:
  - analysis_depth: >= 85%
  - opportunity_identification: >= 80%
  - strategic_value: >= 85%
  - user_integration: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "User identified competitor X focusing on Y angle. Not visible in public content analysis."
  - "User performance data shows 3x engagement on topic Z vs competitors. Opportunity confirmed."
  - "User insider knowledge reveals competitor strategic shift. Adjust positioning recommendations."
```

#### art-topic-explorer

**Purpose**: Deep exploration of the topic and subtopics with user expert knowledge

**Input Requirements**:
```yaml
Required:
  - main_topic: string
  - research_depth: string ("overview" | "standard" | "comprehensive")
  - target_audience: object
  - working_directory: path (absolute path to article folder)

Optional:
  - focus_areas: array
  - exclude_areas: array
  - technical_level: string
  - user_materials_insights: processed/materials_insights.md (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  agent_outputs/topic.md:
    user_materials_integration:
      - user_expert_knowledge: topic expertise from user materials
      - insider_perspectives: user insights not available publicly
      - unique_angles: user-identified approaches to topic

    topic_overview:
      - definition: clear and comprehensive (enhanced with user perspective)
      - scope: well-defined boundaries
      - importance: 3-5 reasons with evidence
      - user_context: user's unique relationship to topic

    subtopics:
      - count: minimum 10
      - depth: 2-3 paragraphs each
      - interconnections: mapped relationships
      - priority_ranking: by relevance (informed by user priorities)
      - user_emphasis: subtopics highlighted by user materials

    expert_opinions:
      - count: minimum 5
      - diversity: different viewpoints represented
      - authority: credentials verified
      - quotes: properly attributed
      - user_expertise: incorporate user expert perspective where applicable

    controversies:
      - count: minimum 2 (if exist)
      - sides: all perspectives presented
      - evidence: supporting data for each
      - implications: analyzed
      - user_experience: user observations on controversies

    knowledge_requirements:
      - prerequisites: clearly listed
      - complexity_levels: mapped
      - learning_path: suggested
      - user_guidance: user recommendations for understanding topic

Quality Metrics:
  - comprehensiveness: >= 90%
  - accuracy: >= 95%
  - depth: >= 85%
  - organization: >= 90%
  - user_integration: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "User expert knowledge fills 4 research gaps in public information."
  - "User controversy perspective provides inside view not available in public sources."
  - "User learning path recommendations based on practical experience. High value."
```

---

### Phase 4: Content Creation (Updated)

#### art-article-writer

**Purpose**: Transform research and user insights into high-quality article draft

**Input Requirements**:
```yaml
Required:
  - agent_outputs_folder: path to all research files
  - strategy_docs: strategy and voice guide paths
  - article_type: string (warning | analysis | solution)
  - word_count_target: integer
  - working_directory: path (absolute path to article folder)

Optional:
  - specific_angle: string
  - must_include_points: array
  - tone_adjustment: string
  - processed_insights: processed/materials_insights.md (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  drafts/v1_draft.md:
    structure:
      - title: compelling and clear
      - introduction: 150-200 words with hook (can use user insights)
      - main_sections: minimum 3
      - conclusion: 150-200 words with CTA
      - key_takeaways: 3-5 bullet points

    content_quality:
      - word_count: target ±10%
      - data_integration:
          statistics_used: minimum 10 (including user data where relevant)
          sources_cited: all claims supported with inline hyperlinks
          examples: minimum 3 detailed (can include user examples)
      - unique_insights: minimum 2 (enhanced by user materials when available)
      - actionable_advice: minimum 5 points
      - logical_flow: score >= 85%
      - user_integration: seamless incorporation of user insights (when available)

    writing_quality:
      - readability: Flesch-Kincaid 8-12
      - sentence_variety: good mix
      - paragraph_length: 3-5 sentences average
      - transition_quality: smooth throughout
      - voice_consistency: matches guide >= 90%
      - user_voice: respects user expertise while maintaining brand voice

Quality Metrics:
  - content_completeness: >= 95%
  - research_utilization: >= 80% (both agent research and user materials)
  - originality: >= 70% (enhanced by user unique perspectives)
  - engagement_potential: >= 75%
  - user_integration: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Progress Monitoring:
  - "Currently at 1,200/2,000 words. Integrated 4 user insights, 6 research data points."
  - "User case study provides unique angle not available in competitor content."
  - "Voice consistency check: 92% match. User expertise seamlessly integrated."

Completion Assessment:
  - "Draft complete. User materials integration adds unique value: 3 insights not available publicly."
  - "User data strengthens argument in section 2. Overall impact: significantly enhanced."
  - "Ready for quality review. Strength: unique user perspective (96% integration)."
```

---

### Phase 5: Quality Review (Updated)

#### art-fact-checker

**Purpose**: Verify all facts, data, and claims including user materials cross-reference

**Input Requirements**:
```yaml
Required:
  - article_draft: path to draft
  - agent_outputs_files: path to research folder
  - validation_level: string ("basic" | "standard" | "rigorous")
  - working_directory: path (absolute path to article folder)

Optional:
  - known_sources: array of trusted sources
  - fact_check_priority: array of critical claims
  - processed_insights: processed/materials_insights.md (for cross-reference)
```

**Output Requirements**:
```yaml
Minimum Standards:
  reports/fact_check.md:
    summary:
      - total_claims: count
      - verified_claims: count with percentage
      - problematic_claims: count with details
      - verification_confidence: percentage
      - user_materials_validation: cross-reference status

    critical_issues:
      - count: exact number
      - details: for each issue
          location: paragraph and line
          claim: exact text
          problem: specific issue
          correction: suggested fix
          priority: high/medium/low

    data_verification:
      - statistics_checked: all numerical claims
      - sources_validated: all citations verified
      - date_accuracy: temporal claims checked
      - calculation_verification: any math validated
      - user_data_verification: cross-reference user materials for validation

    user_materials_cross_reference:
      - claims_supported: user materials that support article claims
      - claims_contradicted: any conflicts between article and user materials
      - additional_validation: user materials provide additional support
      - credibility_assessment: user materials credibility evaluation

    logical_consistency:
      - contradictions: none allowed
      - assumption_validity: checked
      - conclusion_support: verified
      - user_integration_consistency: user insights logically integrated

Quality Metrics:
  - accuracy_rate: must be 100% for facts
  - source_reliability: >= 90%
  - completeness: 100% of claims checked
  - user_materials_validation: >= 95% when available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Fact check 98% complete. User materials provide additional validation for 7 claims."
  - "Found user statistic that updates public 2023 data. Article reflects latest user data."
  - "User case study details verified against public company information. Consistent."
```

#### art-quality-scorer

**Purpose**: Comprehensive quality assessment including user materials integration evaluation

**Input Requirements**:
```yaml
Required:
  - article_draft: path to draft
  - strategy_docs: strategy and voice guide
  - target_metrics: object with minimum scores
  - working_directory: path (absolute path to article folder)

Optional:
  - emphasis_areas: array of priority dimensions
  - audience_profile: detailed audience data
  - processed_insights: processed/materials_insights.md (for integration assessment)
```

**Output Requirements**:
```yaml
Minimum Standards:
  reports/quality_score.md:
    overall_score:
      - total: X/100
      - rating: (Excellent|Good|Acceptable|Needs Work)

    dimension_scores:
      readability:
        - score: X/20
        - flesch_kincaid: exact score
        - sentence_variety: assessment
        - paragraph_flow: rating

      structure:
        - score: X/20
        - logical_organization: rating
        - heading_effectiveness: assessment
        - section_balance: analysis

      voice_alignment:
        - score: X/20
        - consistency: percentage
        - strategy_match: assessment
        - tone_appropriateness: rating

      value_delivery:
        - score: X/20
        - insight_density: insights per 500 words
        - actionability: count of actionable points
        - uniqueness: originality assessment (enhanced by user materials)

      engagement:
        - score: X/20
        - hook_strength: rating
        - narrative_flow: assessment
        - emotional_resonance: score
        - conclusion_impact: rating

      user_materials_integration: (NEW - when available)
        - score: X/10 (bonus points)
        - integration_quality: seamless vs forced
        - value_addition: unique insights provided
        - credibility_enhancement: user expertise impact

    improvement_recommendations:
      - priority_1: must fix before publishing
      - priority_2: should improve
      - priority_3: nice to enhance
      - specific_suggestions: minimum 5 actionable items
      - user_materials_optimization: enhance user insights integration

Quality Metrics:
  - minimum_acceptable_score: 70/100
  - target_score: 85/100
  - excellence_score: 95/100
  - user_integration_bonus: up to 10 additional points when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Quality score 82/100 + 8 bonus for user integration = 90/100. User materials significantly enhance value."
  - "User expertise adds unique credibility not available in standard research. High differentiation."
  - "Integration seamless in sections 2-4. Section 1 could benefit from user perspective."
```

---

### Phase 7: Visual Production (Unchanged but Materials-Aware)

#### art-visual-designer

**Purpose**: Design visual elements and create generation prompts

**Input Requirements**:
```yaml
Required:
  - final_article: path to approved article
  - platform_list: array of target platforms
  - visual_style: string (from strategy)
  - working_directory: path (absolute path to article folder)

Optional:
  - brand_guidelines: object
  - example_images: array of reference URLs
  - specific_requirements: object
  - user_visual_references: from user materials (if available)
```

**Output Requirements**:
```yaml
Minimum Standards:
  visuals/visual_production_guide.md:
    user_materials_considerations:
      - user_visual_preferences: if user provided visual guidance
      - user_brand_elements: user-specific visual requirements
      - user_examples: visual references from user materials

    hero_image:
      - concept: detailed description (100+ words, may incorporate user preferences)
      - style: specific style direction
      - mood: emotional tone defined
      - color_palette: specific colors or ranges
      - composition: layout and focal points
      - platform_specs:
          medium: exact dimensions
          beehiiv: exact dimensions
          substack: exact dimensions
      - generation_prompt: complete, ready to use

    supporting_images:
      - count: minimum 2
      - purpose: clearly defined for each
      - placement: suggested location in article
      - style_consistency: ensured across all
      - prompts: complete for each
      - user_content_alignment: visuals support user-provided insights

Quality Metrics:
  - prompt_clarity: >= 90%
  - style_consistency: >= 95%
  - platform_compliance: 100%
  - creative_quality: >= 80%
  - user_alignment: >= 80% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Identified 3 key visual opportunities. User materials suggest technical diagram approach."
  - "User provided reference visuals align with brand guidelines. Incorporated successfully."
  - "Article heavy on user data. Recommend 2 additional infographics for user statistics."
```

---

### Phase 8: Platform Optimization (Unchanged but Materials-Aware)

#### art-platform-optimizer

**Purpose**: Optimize content for each publishing platform while preserving user insights

**Input Requirements**:
```yaml
Required:
  - final_article: path to approved article
  - platform_strategy: from PLATFORM_OPTIMIZATION_STRATEGY.md
  - target_platforms: array
  - working_directory: path (absolute path to article folder)

Optional:
  - platform_accounts: object with account details
  - previous_performance: historical data
  - specific_goals: per platform
  - user_platform_insights: user platform experience from materials
```

**Output Requirements**:
```yaml
Minimum Standards:
  Per Platform (medium.md, substack.md, beehiiv.md, elevenreader.md):
    title_optimization:
      - platform_formula: applied correctly
      - character_limit: within bounds
      - keyword_placement: optimized
      - hook_strength: A-grade
      - user_insight_emphasis: highlight unique user perspectives in titles

    structure_adaptation:
      - opening: platform-specific hook (may feature user insights)
      - formatting: platform requirements met
      - length: optimized for platform
      - cta_placement: strategic positioning
      - user_content_preservation: maintain user insights across platforms

    seo_elements:
      - meta_description: if applicable
      - tags: optimal number and relevance
      - keywords: proper density
      - internal_links: where appropriate

    engagement_elements:
      - platform_specific_features: utilized
      - interaction_prompts: included
      - share_triggers: embedded (may emphasize user unique insights)
      - community_elements: if applicable

Quality Metrics:
  - platform_compliance: 100%
  - optimization_score: >= 85%
  - expected_performance: above average
  - user_value_preservation: >= 95% when materials available
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Medium optimization complete. User expert angle emphasized in title. Click potential: 94%."
  - "Substack version highlights user case study in opening. Community engagement expected."
  - "User insights preserved across all 3 platforms while optimizing for each format."
```

---

### System Management (Updated)

#### art-registry-updater

**Purpose**: Update registry.json after each phase completion with user materials tracking

**Input Requirements**:
```yaml
Required:
  - article_path: path to article directory
  - update_context: string (e.g., "article_initiated", "user_materials_processed", "research_completed")

Optional:
  - statistics: object (word count, image count for publishing)
  - error_state: object (if phase failed)
  - user_materials_status: object (materials usage tracking)
```

**Output Requirements**:
```yaml
Registry Updates:
  For Phase Transitions:
    - current_work.status: updated to new status
    - current_work.phase: updated to next phase
    - last_updated: current timestamp
    - user_materials_status: tracking user materials usage

  For Article Completion:
    - current_work: cleared (set to null)
    - statistics: updated with final counts
    - global_stats: incremented appropriately
    - user_materials_tracking: record of materials usage for analytics

Quality Metrics:
  - update_accuracy: 100% required
  - atomic_operation: must use .tmp pattern
  - state_consistency: registry must match reality
  - user_materials_tracking: accurate tracking of materials integration
```

**Intelligent Detection**:
```yaml
Self-Assessment:
  - "Registry updated: status changed from 'initiated' to 'user_materials_processing'"
  - "User materials detected and processed. Tracking: 5 files processed, 12 insights extracted."
  - "Article completed with user materials integration. Statistics updated: +1 article, +2047 words, user materials: enhanced."
```

---

## Implementation Guidelines

### 1. Progressive Enhancement Philosophy
- Start with minimum requirements
- Automatically suggest enhancements
- Allow user to decide depth
- Track and learn from choices
- Leverage user materials when available for superior outcomes

### 2. Quality Assurance Points
- Automatic checks at phase transitions
- Real-time monitoring during execution
- Predictive quality scoring
- Proactive issue identification
- User materials integration validation

### 3. User Confirmation Protocol
```yaml
Always Confirm:
  - Phase transitions
  - Quality below threshold
  - Significant additions
  - Strategy deviations
  - User materials processing results

Auto-Proceed When:
  - All minimums exceeded
  - Quality score > 90
  - User pre-approved
  - Minor enhancements only
  - User materials successfully integrated
```

### 4. Continuous Improvement
- Track actual vs. predicted quality
- Learn from user decisions
- Adjust thresholds based on outcomes
- Update requirements based on results
- Optimize user materials integration based on success patterns

---

## Success Metrics

### Article Production Success
- First Draft Quality: >= 75/100 (enhanced by user materials)
- Revision Rounds: <= 2
- Final Quality: >= 85/100 (with user materials bonus potential)
- User Satisfaction: >= 90%
- User Materials Integration: >= 80% when available

### System Performance
- Requirement Completion: 100% minimum, 80% enhanced
- Detection Accuracy: >= 95%
- User Confirmation Rate: <= 3 per article
- Production Time: <= 4-7 hours total (including materials processing)
- User Materials Processing: <= 30 minutes additional when materials provided

---

## Appendix: Quick Reference

### Minimum Agent Requirements Summary (Updated)

| Agent | Min. Outputs | Quality Score | Detection Points | Materials Integration |
|-------|--------------|---------------|------------------|----------------------|
| art-article-initiator | 8 folders + metadata | 100% | Structure validation | 3-folder system setup |
| art-materials-processor | materials_insights.md | >= 90% | Materials analysis | Priority system application |
| art-trend-researcher | 5 trends, 10 stats | >= 90% | Coverage assessment | User trend integration |
| art-audience-analyst | 5 pain points, profiles | >= 85% | Depth evaluation | User audience insights |
| art-competitor-scanner | 5 analyses, 3 gaps | >= 85% | Opportunity identification | User competitive intelligence |
| art-topic-explorer | 10 subtopics, 5 experts | >= 90% | Comprehensiveness | User expert knowledge |
| art-article-writer | 2000 words ±10% | >= 75% | Progress monitoring | Seamless user insights integration |
| art-fact-checker | 100% accuracy | 100% | Issue identification | User materials cross-reference |
| art-quality-scorer | Multi-dimension score | >= 70/100 | Improvement suggestions | User integration assessment |
| art-visual-designer | Hero + 2 supporting | >= 90% | Style consistency | User visual preferences |
| art-platform-optimizer | All platforms adapted | >= 85% | Platform compliance | User value preservation |
| art-registry-updater | Registry updates | 100% | State consistency | Materials usage tracking |

---

## Related Documentation

- **System Architecture** → [ARTICLE_SYSTEM_ARCHITECTURE.md](ARTICLE_SYSTEM_ARCHITECTURE.md)
- **Business Workflow** → [ARTICLE_WORKFLOW_DETAIL.md](ARTICLE_WORKFLOW_DETAIL.md)
- **Platform Strategy** → [PLATFORM_OPTIMIZATION_STRATEGY.md](PLATFORM_OPTIMIZATION_STRATEGY.md)
- **System Overview** → [README.md](README.md)

---

*This document defines the minimum viable outputs for quality article production with user materials integration. Agents are encouraged to exceed these requirements when possible.*