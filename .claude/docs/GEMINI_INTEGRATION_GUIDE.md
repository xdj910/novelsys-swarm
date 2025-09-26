# Gemini CLI Integration Guide for NOVELSYS-SWARM

## Overview

This guide provides comprehensive instructions for integrating Gemini CLI with NOVELSYS-SWARM, focusing on language consistency enforcement and optimal @ syntax usage for local file auditing.

## Critical Issues Resolved

### 1. Language Consistency Problem

**Issue**: Main Claude sometimes sends Chinese prompts to Gemini despite system requirement for English-only content.

**Root Cause**: Legacy bilingual formatting patterns and configuration traces from previous system versions.

**Solution Implemented**:
- **Language validation function** in gemini-auditor agent
- **Pre-prompt validation** checks for non-English characters
- **Template enforcement** using standardized English-only patterns
- **Response monitoring** to detect and flag non-English outputs

### 2. @ Syntax Context Overload

**Issue**: Using `@./` on large projects causes 503 errors and context overload.

**Root Cause**: Attempting to load entire project (100+ files) into Gemini's context window.

**Solution Implemented**:
- **Progressive analysis strategy**: Structure -> Focus -> Integration
- **File batching**: Maximum 5-10 files per prompt
- **Targeted paths**: Use specific directories like `@./src/` instead of `@./`
- **`.geminiignore`**: Exclude irrelevant files automatically

## @ Syntax Best Practices

### 1. Safe File Reference Patterns

```bash
# SAFE: Single file analysis
gemini -p "Review security in @./src/auth.py"

# SAFE: Multiple specific files (limited)
gemini -p "Analyze @./config.py @./database.py @./auth.py"

# SAFE: Directory with limits
gemini -p "Audit @./src/security/ (max 10 files)"

# DANGEROUS: Entire project
gemini -p "Analyze @./"  # Causes 503 errors!
```

### 2. Progressive Analysis Strategy

For large codebases like NOVELSYS-SWARM:

```bash
# Phase 1: Structure Overview (NO file loading)
gemini -p "List directory structure without loading file contents"

# Phase 2: Critical Components (SPECIFIC paths)
gemini -p "Security audit @./src/auth/ @./src/security/ (max 8 files each)"

# Phase 3: Integration Check (MINIMAL scope)
gemini -p "Check security between @./auth.py @./database.py"
```

### 3. File Type Optimization

```bash
# Code Analysis
gemini -p "Review Python files: @./src/*.py (exclude tests, max 10)"

# Documentation Review
gemini -p "Audit documentation: @./docs/*.md @./README.md"

# Configuration Security
gemini -p "Check config security: @./config/*.yaml @./.env.example"
```

## Language Enforcement Protocol

### 1. Validation Function Usage

All gemini-auditor operations now use automatic validation:

```bash
# Automatically applied to all prompts
VALIDATED_PROMPT=$(validate_english_prompt "Original prompt text")
gemini -p "$VALIDATED_PROMPT"
```

### 2. Detection and Sanitization

The validation function:
- **Detects Chinese characters** using Unicode range `[\u4e00-\u9fff]`
- **Sanitizes content** by stripping non-ASCII characters
- **Enforces English structure** by ensuring prompts start with English instructions
- **Adds explicit requirements** like "Respond in English only"

### 3. Response Monitoring

```bash
# Check response for non-English content
if grep -P '[\u4e00-\u9fff]' /tmp/gemini_output > /dev/null; then
    echo "WARNING: Non-English content detected in response"
fi
```

## Performance Optimization

### 1. .geminiignore Configuration

Created comprehensive ignore patterns:
- **Archive directories**: `.claude/archive/`, `archive/`
- **Large data files**: `*.json.gz`, `*.log`, `*.sqlite`
- **System files**: `.git/`, `__pycache__/`, `.vscode/`
- **Temporary files**: `*.tmp`, `*.backup`, `*~`

### 2. Context Management

**File Batching Guidelines**:
- **Single analysis**: 1-3 files maximum
- **Directory analysis**: Specify file limits (max 10 files)
- **Progressive scanning**: Build understanding incrementally
- **Memory management**: Clear context between major operations

### 3. Error Recovery Strategy

**Smart Retry Logic**:
1. **Attempt 1**: Full validated prompt
2. **Attempt 2**: Simplified prompt (50% length)
3. **Attempt 3**: Minimal prompt with English enforcement
4. **Fallback**: Ultra-simple query with explicit English requirement

## Integration Workflows

### 1. Code Security Audit

```bash
# Complete security audit workflow
analyze_security() {
    # Phase 1: Structure analysis
    STRUCTURE=$(validate_english_prompt "Identify security-critical files without loading content")
    gemini -p "$STRUCTURE"

    # Phase 2: Critical file analysis
    SECURITY=$(validate_english_prompt "Security audit @./src/auth/ @./src/security/ (max 8 files each)")
    gemini -p "$SECURITY"

    # Phase 3: Integration security
    INTEGRATION=$(validate_english_prompt "Check security integration between critical components")
    gemini -p "$INTEGRATION"
}
```

### 2. Novel Manuscript Review

```bash
# English-only manuscript analysis
review_manuscript() {
    MANUSCRIPT=$(validate_english_prompt "Analyze @./chapters/ for English consistency:
    - Plot coherence and pacing
    - Character development
    - Language variant consistency (US/UK)
    - Ensure all content is English only
    Respond in English only.")

    gemini -p "$MANUSCRIPT"
}
```

### 3. Documentation Audit

```bash
# Documentation quality and consistency
audit_documentation() {
    DOCS=$(validate_english_prompt "Review documentation @./docs/*.md for:
    - Clarity and accuracy
    - English language consistency
    - Technical completeness
    - User experience quality
    Provide recommendations in English only.")

    gemini -p "$DOCS"
}
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| **503 Error** | "Model overloaded" | Use specific paths, not `@./` |
| **Chinese Output** | Mixed language responses | Apply `validate_english_prompt()` |
| **Context Overflow** | Timeout/memory errors | Batch files (max 10 per prompt) |
| **File Not Found** | `@./file` fails | Check `.geminiignore` patterns |
| **Slow Performance** | Long response times | Use progressive analysis strategy |

### Debug Commands

```bash
# Test validation function
validate_english_prompt "测试中文内容"  # Should sanitize

# Check file accessibility
ls -la .geminiignore  # Verify ignore file exists

# Test progressive analysis
gemini -p "$(validate_english_prompt "List main directories only")"
```

## Best Practices Summary

### DO:
1. **Use specific paths**: `@./src/auth/` instead of `@./`
2. **Validate all prompts**: Apply English-only validation
3. **Batch files**: Maximum 5-10 files per analysis
4. **Progressive approach**: Structure -> Focus -> Integration
5. **Monitor responses**: Check for language consistency
6. **Use .geminiignore**: Exclude irrelevant files
7. **Handle errors gracefully**: Implement retry logic

### DON'T:
1. **Load entire projects**: Never use `@./` on large codebases
2. **Send raw prompts**: Always validate for English content
3. **Ignore file limits**: Respect context window constraints
4. **Skip error handling**: Always implement fallback strategies
5. **Mix languages**: Maintain English-only consistency
6. **Overload context**: Use targeted file selection

## Integration Testing

### Validation Script

```bash
# Test gemini-auditor integration
test_gemini_integration() {
    echo "Testing English validation..."
    result=$(validate_english_prompt "Analyze code quality")
    echo "Validation result: $result"

    echo "Testing file reference..."
    gemini -p "$(validate_english_prompt "List files in @./src/ without loading content")"

    echo "Testing error handling..."
    smart_gemini_english "Simple test prompt"
}
```

### Success Metrics

- **Language Consistency**: 100% English-only outputs
- **Performance**: No 503 errors on file references
- **Context Efficiency**: Successful analysis of large codebases
- **Error Recovery**: Graceful handling of overload situations

## Maintenance

### Regular Tasks

1. **Update .geminiignore**: Add new ignore patterns as project grows
2. **Monitor language outputs**: Check for non-English responses
3. **Performance review**: Optimize file selection strategies
4. **Error log analysis**: Identify patterns in failures

### Future Improvements

1. **Automated validation**: Pre-commit hooks for language consistency
2. **Smart file selection**: AI-driven critical file identification
3. **Performance metrics**: Tracking context efficiency
4. **Enhanced error recovery**: More sophisticated fallback strategies

---

**Document Version**: 1.0
**Last Updated**: 2025-09-17
**Status**: Production Ready
**Maintained By**: NOVELSYS-SWARM Development Team