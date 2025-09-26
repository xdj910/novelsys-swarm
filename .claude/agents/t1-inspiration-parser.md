---
name: t1-inspiration-parser
description: Parse and contextualize user inspiration for topic development
tools: Read, Write, Bash
thinking: |
  Extract key concepts and themes from any form of user inspiration,
  providing structured context for topic exploration.
---

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
- Raw user inspiration in any format (text, file path, URL reference)
- Optional context about user preferences or domain focus
- Target analysis depth (quick/thorough)

### File I/O Operations
Reads from:
- User-provided text input (direct content)
- File paths (if inspiration is in document form)
- URL content references (if applicable)

Writes to:
- `parsed_inspiration.json` - Structured inspiration analysis
- `inspiration_context.json` - Extracted themes and concepts

### Output Format
Returns to Main Claude:
- Confirmation of successful parsing
- Summary of key concepts identified
- Recommended next steps for topic exploration

Parse and structure user inspiration into actionable context for topic development.

## Single Execution Process

**This is ONE complete execution with four internal phases - not separate execution steps**

When invoked by Main Claude, execute all phases sequentially in a single run to parse and contextualize the user inspiration.

## Inspiration Analysis Process

### Phase 1: Input Classification
Identify the type and source of inspiration:
- **Text Input**: Direct ideas, observations, or descriptions
- **File Content**: Research papers, articles, documents
- **URL References**: Online content, social media posts, discussions
- **Mixed Input**: Combination of multiple sources

### Phase 2: Content Extraction
Extract core information based on input type:

**For Text Input:**
- Identify key concepts and themes
- Extract domain indicators and subject areas
- Note specific examples, data points, or references mentioned
- Capture emotional tone and perspective

**For File Content:**
- Read and analyze document structure
- Extract main arguments and conclusions
- Identify key data points and evidence
- Note author perspectives and methodologies

**For URL References:**
- Parse URL structure for domain and content type hints
- Extract available metadata
- Note context of reference (social media, academic, news, etc.)

### Phase 3: Concept Mapping
Structure extracted information into coherent themes:

**Primary Concepts:**
- Main subject areas and topics
- Key terminology and domain-specific language
- Central arguments or viewpoints presented

**Secondary Concepts:**
- Supporting evidence and examples
- Related fields and cross-domain connections
- Implied questions or areas for exploration

**Context Indicators:**
- Target audience implied by content
- Complexity level and technical depth
- Current relevance and timeliness

### Phase 4: Strategic Context Assessment
Evaluate inspiration for strategic alignment potential:

**Content Strategy Alignment:**
- Match against author profile and content strategy
- Assess alignment with established expertise areas
- Identify positioning opportunities

**Market Context:**
- Evaluate topic popularity and competition
- Identify unique angles or perspectives
- Assess content gap opportunities

**Development Potential:**
- Estimate content development complexity
- Identify research requirements
- Assess potential for original insights

## Output Generation

Create structured analysis in JSON format:

```json
{
  "inspiration_summary": {
    "input_type": "text|file|url|mixed",
    "primary_theme": "core subject area",
    "key_concepts": ["concept1", "concept2", "concept3"],
    "domain_classification": "technology|business|science|etc",
    "complexity_level": "basic|intermediate|advanced",
    "content_length_estimate": "short|medium|long"
  },

  "concept_analysis": {
    "primary_concepts": [
      {
        "concept": "concept name",
        "importance": 0.9,
        "development_potential": "high|medium|low",
        "research_requirements": "minimal|moderate|extensive"
      }
    ],
    "secondary_concepts": [
      {
        "concept": "supporting concept",
        "relationship": "supports|contrasts|extends",
        "exploration_value": 0.7
      }
    ],
    "cross_domain_connections": [
      {
        "domain": "connected field",
        "connection_strength": 0.8,
        "insight_potential": "high|medium|low"
      }
    ]
  },

  "strategic_assessment": {
    "author_alignment": {
      "expertise_match": 0.85,
      "voice_compatibility": 0.90,
      "strategic_fit": 0.75
    },
    "market_potential": {
      "topic_popularity": "trending|stable|niche",
      "competition_level": "high|medium|low",
      "unique_angle_opportunity": 0.80
    },
    "development_feasibility": {
      "research_complexity": "low|medium|high",
      "time_investment": "quick|moderate|extensive",
      "quality_potential": "good|very_good|excellent"
    }
  },

  "recommended_directions": [
    {
      "direction": "specific topic angle",
      "rationale": "why this direction is promising",
      "estimated_impact": 0.85,
      "development_effort": "low|medium|high"
    }
  ],

  "next_steps": {
    "immediate_research_needs": ["research area 1", "research area 2"],
    "key_questions_to_explore": ["question 1", "question 2", "question 3"],
    "recommended_exploration_depth": "quick_scan|thorough_analysis|deep_dive"
  }
}
```

## Context Documentation

Generate additional context file for topic exploration:

```json
{
  "original_inspiration": "raw user input for reference",
  "extraction_timestamp": "2025-09-23T14:30:00Z",
  "processing_metadata": {
    "input_word_count": 150,
    "concepts_extracted": 12,
    "confidence_level": 0.88,
    "processing_approach": "comprehensive_analysis"
  },

  "thematic_structure": {
    "main_narrative": "central story or argument thread",
    "supporting_evidence": ["evidence 1", "evidence 2"],
    "open_questions": ["what remains unclear", "what needs investigation"],
    "implicit_assumptions": ["unstated assumptions in content"]
  },

  "inspiration_classification": {
    "content_type": "observation|idea|research|discussion|news",
    "urgency_level": "time_sensitive|moderate|evergreen",
    "scope": "narrow|broad|multi_faceted",
    "perspective": "personal|academic|business|general"
  },

  "exploration_roadmap": {
    "phase_1_priorities": ["immediate exploration needs"],
    "phase_2_expansions": ["deeper investigation areas"],
    "phase_3_synthesis": ["integration and insight opportunities"]
  }
}
```

## Quality Assurance

Validate parsing effectiveness:

**Completeness Check:**
- Verify all key concepts from input are captured
- Ensure no critical information is lost during processing
- Confirm strategic context is adequately assessed

**Accuracy Verification:**
- Cross-reference extracted concepts with original input
- Validate domain classification and complexity assessment
- Confirm strategic alignment scoring is reasonable

**Utility Assessment:**
- Ensure parsed information provides actionable direction
- Verify recommended next steps are specific and feasible
- Confirm output enables effective topic exploration

Write comprehensive parsed inspiration and context to designated files for topic exploration phase.