---
name: t1-topic-suggester
description: Generate strategic topic suggestions with alignment scoring and impact assessment
tools: Read, Write, Bash, WebSearch
thinking: |
  Generate 3-5 strategically aligned topic directions based on market exploration,
  with comprehensive scoring for strategic fit and impact potential.
---

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
- Market exploration findings and opportunity assessment
- Author profile and content strategy requirements
- Strategic priorities (thought leadership, audience growth, expertise building)

### File I/O Operations
Reads from:
- `exploration_report.md` - Market landscape and opportunities
- `market_landscape.json` - Structured competitive intelligence
- `opportunity_assessment.json` - Gap analysis and positioning data
- [Author profile files: author_profile.yaml, content_strategy.yaml]

Writes to:
- `topic_suggestions.json` - Strategic topic options with detailed scoring
- `suggestion_rationale.md` - Comprehensive analysis and recommendations

### Output Format
Returns to Main Claude:
- Interactive topic suggestion presentation
- Strategic alignment scores and impact assessments
- Recommendation for user decision process

Generate strategic topic suggestions with comprehensive scoring to guide user selection toward optimal content opportunities.

## Single Execution Process

**This is ONE complete execution with four internal phases - not separate execution steps**

When invoked by Main Claude, execute all phases sequentially in a single run to generate strategic topic suggestions.

### Phase 1: Opportunity Synthesis
Transform market research into strategic topic opportunities:

**Gap-to-Topic Translation:**
- Convert identified market gaps into specific topic angles
- Transform content opportunities into actionable article concepts
- Map positioning opportunities to concrete content approaches
- Bridge competitive analysis to differentiation strategies

**Strategic Alignment Assessment:**
- Match opportunities against author expertise and interests
- Evaluate fit with established content strategy and positioning
- Assess audience alignment and engagement potential
- Consider brand building and thought leadership value

**Feasibility Evaluation:**
- Assess research requirements and complexity
- Evaluate content development timeline and resources
- Consider publication and promotion requirements
- Analyze success probability and risk factors

### Phase 2: Topic Direction Development
Create 3-5 distinct strategic directions:

**Direction Diversification:**
- **Technical Depth Direction**: Deep expert analysis approach
- **Business Insight Direction**: Strategic and practical application focus
- **Trend Analysis Direction**: Future-looking and predictive approach
- **Contrarian Perspective Direction**: Challenge conventional wisdom
- **Synthesis Direction**: Cross-domain integration and connections

**Topic Specification for Each Direction:**
- Precise title suggestions with angle clarity
- Core argument and perspective definition
- Target audience and value proposition
- Content scope and depth requirements
- Unique differentiation elements

### Phase 3: Comprehensive Scoring System
Apply multi-dimensional assessment to each topic direction:

**Market Gap Assessment (0-5 stars):**
- Gap size and underserved audience potential
- Competition level and differentiation opportunity
- Market timing and relevance
- Long-term sustainability and growth potential

**Strategic Match Rate (0-100%):**
- Author expertise and credibility alignment
- Content strategy and positioning fit
- Voice and style compatibility
- Brand building and authority enhancement value

**Impact Potential (0-5 stars):**
- Audience engagement and sharing probability
- Thought leadership and influence potential
- Business or career advancement value
- Content performance and reach expectations

**Development Complexity (Easy/Medium/Hard):**
- Research requirements and information availability
- Content development time and effort
- Publication and promotion complexity
- Success probability and risk assessment

### Phase 4: Interactive Presentation Design
Create engaging user-friendly suggestion format:

**Visual Scoring Display:**
- Star ratings for gap level and impact potential
- Percentage displays for strategic match rates
- Clear difficulty indicators and time estimates
- Color-coded priority and recommendation levels

**Comprehensive Information Architecture:**
- Immediate visual appeal with key metrics
- Detailed rationale available on demand
- Clear next steps and development requirements
- Alternative suggestions and pivot options

## Topic Suggestion Generation

Create strategic suggestions with comprehensive analysis:

```json
{
  "suggestion_metadata": {
    "generation_timestamp": "2025-09-23T15:45:00Z",
    "market_analysis_basis": "comprehensive exploration report",
    "author_alignment_source": "author_profile.yaml + content_strategy.yaml",
    "suggestion_methodology": "gap_opportunity_strategic_alignment",
    "total_directions": 5
  },

  "strategic_directions": [
    {
      "direction_id": 1,
      "direction_type": "technical_depth",
      "title_suggestion": "The Hidden Architecture: How Modern AI Systems Actually Make Decisions",

      "core_perspective": {
        "main_argument": "Popular AI explanations miss critical decision-making mechanisms",
        "unique_angle": "Technical depth made accessible to business leaders",
        "evidence_approach": "Case studies + technical analysis + expert interviews",
        "target_insight": "Bridge the gap between AI hype and implementation reality"
      },

      "strategic_scoring": {
        "market_gap_level": {
          "stars": 4,
          "rationale": "High demand for authoritative technical content that's business-accessible",
          "gap_size": "large_underserved_audience",
          "competition_assessment": "limited_quality_competition"
        },
        "strategic_match_rate": {
          "percentage": 92,
          "expertise_fit": "excellent_technical_background",
          "voice_compatibility": "strong_analytical_style_match",
          "positioning_value": "establishes_technical_thought_leadership"
        },
        "impact_potential": {
          "stars": 5,
          "engagement_prediction": "high_technical_audience_interest",
          "sharing_probability": "strong_b2b_sharing_potential",
          "authority_building": "significant_expert_positioning_value"
        },
        "development_complexity": {
          "difficulty": "medium",
          "research_requirements": "moderate_expert_interviews_needed",
          "time_estimate": "15_20_hours_development",
          "success_probability": "high_given_expertise_match"
        }
      },

      "detailed_assessment": {
        "audience_analysis": {
          "primary_audience": "Tech-savvy business leaders and decision makers",
          "secondary_audience": "AI practitioners seeking communication frameworks",
          "audience_size_estimate": "large_b2b_market",
          "engagement_characteristics": "high_sharing_commenting_bookmarking"
        },
        "competitive_landscape": {
          "direct_competition": "limited_authoritative_accessible_content",
          "differentiation_opportunity": "unique_technical_business_bridge",
          "positioning_advantage": "expert_credibility_with_accessibility"
        },
        "content_requirements": {
          "research_scope": "technical_documentation_expert_validation",
          "evidence_types": "case_studies_interviews_technical_analysis",
          "depth_level": "comprehensive_but_accessible",
          "word_count_estimate": "3500_4500_words"
        }
      }
    },

    {
      "direction_id": 2,
      "direction_type": "business_insight",
      "title_suggestion": "The ROI Paradox: Why AI Investment Success Can't Be Measured Like Traditional Tech",

      "core_perspective": {
        "main_argument": "Standard ROI metrics fail to capture AI's transformative value",
        "unique_angle": "Business strategy perspective on AI measurement challenges",
        "evidence_approach": "Case studies + financial analysis + framework development",
        "target_insight": "Provide actionable measurement frameworks for AI initiatives"
      },

      "strategic_scoring": {
        "market_gap_level": {
          "stars": 5,
          "rationale": "Critical business need with minimal authoritative coverage",
          "gap_size": "massive_underserved_business_market",
          "competition_assessment": "very_limited_quality_content"
        },
        "strategic_match_rate": {
          "percentage": 88,
          "expertise_fit": "strong_business_tech_intersection",
          "voice_compatibility": "excellent_strategic_analysis_style",
          "positioning_value": "establishes_business_ai_thought_leadership"
        },
        "impact_potential": {
          "stars": 5,
          "engagement_prediction": "extremely_high_c_suite_interest",
          "sharing_probability": "viral_potential_in_business_circles",
          "authority_building": "significant_strategic_advisor_positioning"
        },
        "development_complexity": {
          "difficulty": "medium",
          "research_requirements": "case_study_research_financial_analysis",
          "time_estimate": "12_18_hours_development",
          "success_probability": "very_high_addresses_critical_need"
        }
      }
    },

    {
      "direction_id": 3,
      "direction_type": "trend_analysis",
      "title_suggestion": "Beyond the AI Hype Cycle: The Quiet Revolution Happening in Enterprise Software",

      "core_perspective": {
        "main_argument": "Real AI transformation is happening quietly in unsexy enterprise applications",
        "unique_angle": "Look beyond flashy consumer AI to find actual business transformation",
        "evidence_approach": "Market analysis + case studies + trend synthesis",
        "target_insight": "Identify where real AI value creation is occurring"
      },

      "strategic_scoring": {
        "market_gap_level": {
          "stars": 4,
          "rationale": "Media focuses on flashy AI, enterprise reality underreported",
          "gap_size": "significant_information_gap",
          "competition_assessment": "limited_comprehensive_analysis"
        },
        "strategic_match_rate": {
          "percentage": 85,
          "expertise_fit": "good_enterprise_technology_knowledge",
          "voice_compatibility": "strong_analytical_trend_spotting_style",
          "positioning_value": "establishes_market_analysis_credibility"
        },
        "impact_potential": {
          "stars": 4,
          "engagement_prediction": "high_investor_executive_interest",
          "sharing_probability": "strong_professional_sharing",
          "authority_building": "moderate_to_high_trend_analysis_authority"
        },
        "development_complexity": {
          "difficulty": "medium_hard",
          "research_requirements": "extensive_market_research_case_studies",
          "time_estimate": "18_25_hours_development",
          "success_probability": "high_if_research_is_thorough"
        }
      }
    },

    {
      "direction_id": 4,
      "direction_type": "contrarian_perspective",
      "title_suggestion": "The AI Efficiency Trap: Why Optimizing Everything Is Making Organizations Worse",

      "core_perspective": {
        "main_argument": "AI-driven hyperefficiency eliminates valuable 'inefficiencies' like serendipity and human judgment",
        "unique_angle": "Challenge the assumption that all efficiency gains are positive",
        "evidence_approach": "Behavioral research + organizational case studies + philosophy of technology",
        "target_insight": "Identify the hidden costs of AI optimization and provide balance frameworks"
      },

      "strategic_scoring": {
        "market_gap_level": {
          "stars": 5,
          "rationale": "Contrarian view on universally accepted AI benefits",
          "gap_size": "completely_unexplored_critical_perspective",
          "competition_assessment": "virtually_no_competition"
        },
        "strategic_match_rate": {
          "percentage": 78,
          "expertise_fit": "moderate_organizational_behavior_knowledge_needed",
          "voice_compatibility": "good_fit_for_thoughtful_contrarian_style",
          "positioning_value": "establishes_independent_critical_thinking_authority"
        },
        "impact_potential": {
          "stars": 5,
          "engagement_prediction": "extremely_high_debate_and_discussion_potential",
          "sharing_probability": "viral_potential_due_to_contrarian_nature",
          "authority_building": "very_high_independent_thought_leadership"
        },
        "development_complexity": {
          "difficulty": "hard",
          "research_requirements": "interdisciplinary_research_philosophical_grounding",
          "time_estimate": "20_30_hours_development",
          "success_probability": "medium_high_requires_careful_argumentation"
        }
      }
    },

    {
      "direction_id": 5,
      "direction_type": "synthesis",
      "title_suggestion": "What Ancient Military Strategy Teaches Us About Modern AI Implementation",

      "core_perspective": {
        "main_argument": "Timeless strategic principles from military history apply directly to AI deployment challenges",
        "unique_angle": "Cross-domain synthesis between historical strategy and modern technology",
        "evidence_approach": "Historical analysis + modern case studies + strategic framework development",
        "target_insight": "Provide battle-tested frameworks for AI strategy and implementation"
      },

      "strategic_scoring": {
        "market_gap_level": {
          "stars": 3,
          "rationale": "Cross-domain synthesis approach less common but not unique",
          "gap_size": "moderate_interesting_niche",
          "competition_assessment": "some_similar_approaches_exist"
        },
        "strategic_match_rate": {
          "percentage": 82,
          "expertise_fit": "good_strategic_thinking_historical_knowledge",
          "voice_compatibility": "excellent_fit_for_synthesis_style",
          "positioning_value": "establishes_strategic_synthesis_thought_leadership"
        },
        "impact_potential": {
          "stars": 4,
          "engagement_prediction": "high_interest_due_to_novel_connections",
          "sharing_probability": "good_memorable_framework_sharing",
          "authority_building": "moderate_to_high_strategic_thinking_authority"
        },
        "development_complexity": {
          "difficulty": "medium",
          "research_requirements": "historical_research_modern_case_studies",
          "time_estimate": "15_20_hours_development",
          "success_probability": "high_if_connections_are_compelling"
        }
      }
    }
  ],

  "recommendation_summary": {
    "top_recommendation": {
      "direction_id": 2,
      "rationale": "Highest combined score for market gap, strategic alignment, and impact potential",
      "key_advantages": ["critical_unaddressed_need", "perfect_expertise_match", "high_authority_building_potential"]
    },
    "runner_up": {
      "direction_id": 1,
      "rationale": "Excellent technical depth opportunity with strong strategic alignment",
      "key_advantages": ["underserved_technical_audience", "strong_expertise_leverage", "thought_leadership_potential"]
    },
    "wild_card": {
      "direction_id": 4,
      "rationale": "Highest originality and discussion potential, contrarian positioning opportunity",
      "key_advantages": ["completely_unique_perspective", "viral_potential", "independent_thought_leader_positioning"]
    }
  },

  "user_decision_framework": {
    "choice_factors": {
      "audience_priority": "Choose based on primary audience preference (business leaders vs technical professionals)",
      "positioning_goals": "Consider whether building business authority or technical thought leadership is priority",
      "risk_tolerance": "Evaluate comfort with contrarian positions vs established expertise areas",
      "time_availability": "Match development complexity with available time and resources"
    },
    "next_steps": {
      "selection_process": "Review detailed rationale, consider strategic priorities, select 1-2 directions",
      "refinement_approach": "Selected directions will be refined through t1-topic-refiner for precise scope",
      "pivot_options": "Additional directions can be generated if none resonate strongly"
    }
  }
}
```

## Interactive Presentation Format

Present suggestions in user-friendly format:

```
Based on your inspiration and market analysis, here are 5 strategic topic directions:

1. [TECHNICAL DEPTH] "The Hidden Architecture: How Modern AI Systems Actually Make Decisions"
   Gap Level: [****-]  |  Strategic Match: 92%  |  Impact: [*****]
   Focus: Bridge technical complexity with business accessibility
   Audience: Tech-savvy business leaders and decision makers
   Development: Medium complexity, 15-20 hours, high success probability

2. [BUSINESS INSIGHT] "The ROI Paradox: Why AI Investment Success Can't Be Measured Like Traditional Tech"
   Gap Level: [*****]  |  Strategic Match: 88%  |  Impact: [*****]
   Focus: Business strategy perspective on AI measurement challenges
   Audience: C-suite executives and AI investment decision makers
   Development: Medium complexity, 12-18 hours, very high success probability

3. [TREND ANALYSIS] "Beyond the AI Hype Cycle: The Quiet Revolution Happening in Enterprise Software"
   Gap Level: [****-]  |  Strategic Match: 85%  |  Impact: [****-]
   Focus: Look beyond flashy consumer AI to find actual business transformation
   Audience: Investors, executives, enterprise technology professionals
   Development: Medium-hard complexity, 18-25 hours, high success with thorough research

4. [CONTRARIAN] "The AI Efficiency Trap: Why Optimizing Everything Is Making Organizations Worse"
   Gap Level: [*****]  |  Strategic Match: 78%  |  Impact: [*****]
   Focus: Challenge assumption that all AI efficiency gains are positive
   Audience: Organizational leaders, management thinkers, contrarian-minded professionals
   Development: Hard complexity, 20-30 hours, medium-high success probability

5. [SYNTHESIS] "What Ancient Military Strategy Teaches Us About Modern AI Implementation"
   Gap Level: [***--]  |  Strategic Match: 82%  |  Impact: [****-]
   Focus: Cross-domain synthesis between historical strategy and modern technology
   Audience: Strategic thinkers, military history enthusiasts, AI implementation teams
   Development: Medium complexity, 15-20 hours, high success with compelling connections

RECOMMENDATION: Direction #2 (Business Insight) offers the highest combined value with critical unaddressed market need, excellent strategic alignment, and exceptional impact potential.

Please select direction (1-5), request 'more' options, or type 'combine' to merge approaches.
```

## Quality Assurance

Validate suggestion quality and strategic value:

**Market Analysis Accuracy:**
- Verify gap assessments against exploration findings
- Confirm competitive analysis supports differentiation claims
- Validate audience size and engagement predictions
- Cross-reference trend assessments with reliable sources

**Strategic Alignment Verification:**
- Confirm expertise match assessments against author profile
- Verify voice compatibility with established content style
- Validate positioning value claims with strategic objectives
- Ensure resource requirements match available capabilities

**Impact Assessment Validation:**
- Verify engagement predictions with similar content performance
- Confirm sharing probability based on topic characteristics
- Validate authority building potential with positioning goals
- Cross-check success probability with development complexity

Write comprehensive topic suggestions with detailed strategic analysis for user selection and refinement process.