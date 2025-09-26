#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
markdown_safe_cleaner.py
Safe markdown standardization with conservative cleaning and issue detection

Performs only 100% safe operations:
- Control character removal
- Whitespace normalization
- Obvious LaTeX artifact fixes
- Code block preservation
- Issue detection and reporting

Does NOT:
- Remove potentially valid LaTeX expressions
- Make semantic decisions
- Modify uncertain content

Dependencies: None (uses only Python standard library)
"""

import sys
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Set UTF-8 encoding for stdout to handle Unicode
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class MarkdownSafeCleaner:
    """Safe markdown cleaner with conservative approach"""

    def __init__(self, input_file: str):
        self.input_file = Path(input_file)

        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        self.content = self.input_file.read_text(encoding='utf-8')
        self.original_content = self.content  # Backup

        # Statistics and issue tracking
        self.stats = {
            'control_chars_removed': 0,
            'tabs_converted': 0,
            'nbsp_converted': 0,
            'zwsp_removed': 0,
            'orphaned_symbols_removed': 0,
            'junk_lines_removed': 0,
            'obvious_latex_fixed': 0,
            'blank_lines_normalized': 0
        }

        self.issues = {
            'uncertain_latex': [],
            'complex_latex': [],
            'potential_problems': []
        }

    # ========== Safe Operations ==========

    def remove_control_characters(self):
        """Remove control characters (100% safe)"""
        # Count before removal
        control_chars = re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', self.content)
        self.stats['control_chars_removed'] = len(control_chars)

        # Remove control characters (preserve \n and \r for now)
        self.content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', self.content)

    def normalize_whitespace(self):
        """Normalize all whitespace characters (100% safe)"""
        # Count tabs
        self.stats['tabs_converted'] = self.content.count('\t')
        # Convert tabs to 4 spaces
        self.content = self.content.replace('\t', '    ')

        # Count non-breaking spaces
        self.stats['nbsp_converted'] = self.content.count('\xA0')
        # Convert non-breaking spaces to regular spaces
        self.content = self.content.replace('\xA0', ' ')

        # Count zero-width spaces
        self.stats['zwsp_removed'] = len(re.findall(r'[\u200b-\u200d\ufeff]', self.content))
        # Remove zero-width characters
        self.content = re.sub(r'[\u200b-\u200d\ufeff]', '', self.content)

        # Normalize line endings to Unix style
        self.content = self.content.replace('\r\n', '\n').replace('\r', '\n')

    def remove_orphaned_symbols(self):
        """Remove orphaned symbol lines (100% safe, preserves HR rules)"""
        # Count before removal
        orphaned = re.findall(r'^[ \t]*[-_*](?![-_*]{2,})[ \t]*$', self.content, re.MULTILINE)
        self.stats['orphaned_symbols_removed'] = len(orphaned)

        # Remove headers with only symbols (e.g., "# -", "## _")
        self.content = re.sub(r'^#{1,6}[ \t]+[-_*#.:]+[ \t]*$', '', self.content, flags=re.MULTILINE)

        # Remove single orphaned symbols (but preserve HR: ---, ***, ___)
        self.content = re.sub(r'^[ \t]*[-_*](?![-_*]{2,})[ \t]*$', '', self.content, flags=re.MULTILINE)

        # Remove isolated single-character symbol lines (%, $, #, &, *, @, !, etc.)
        # These are OCR artifacts with no semantic meaning
        isolated_symbols = re.findall(r'^[ \t]*[%$#&*@!+=/\\|<>~`][ \t]*$', self.content, re.MULTILINE)
        self.stats['orphaned_symbols_removed'] += len(isolated_symbols)
        self.content = re.sub(r'^[ \t]*[%$#&*@!+=/\\|<>~`][ \t]*$', '', self.content, flags=re.MULTILINE)

    def is_junk_line(self, line: str) -> bool:
        """Intelligently detect junk lines from OCR artifacts

        Junk lines are typically:
        - Short (<80 chars)
        - Mostly symbols (>85% special chars)
        - No meaningful words (no 3+ letter sequences)
        - Not valid Markdown syntax

        Preserves:
        - Markdown horizontal rules (---, ***, ___)
        - Markdown headers (# ## ### with actual text)
        - Real quoted text
        - Actual content
        """
        stripped = line.strip()

        # Empty lines are fine
        if not stripped:
            return False

        # Preserve valid Markdown horizontal rules
        if re.match(r'^[-*_]{3,}$', stripped):
            return False

        # Preserve VALID Markdown headers (must have space + alphanumeric after #)
        if re.match(r'^#{1,6}\s+[a-zA-Z0-9]', stripped):
            return False

        # Check for meaningful words (3+ consecutive letters)
        has_words = bool(re.search(r'[a-zA-Z]{3,}', stripped))
        if has_words:
            return False

        # Check if line is symbol-heavy
        if len(stripped) < 80:
            # Count symbol characters (including $ for LaTeX junk)
            symbol_chars = sum(1 for c in stripped if c in '"\'"#&-_*.:;!?()[]{}|\\/@<>~`+=$')
            whitespace_chars = sum(1 for c in stripped if c.isspace())
            total_chars = len(stripped)

            # If 85%+ symbols/whitespace and no words, likely junk
            junk_ratio = (symbol_chars + whitespace_chars) / total_chars
            if junk_ratio > 0.85:
                return True

        return False

    def remove_junk_lines(self):
        """Remove OCR artifact junk lines (intelligent detection)"""
        lines = self.content.split('\n')
        junk_count = 0
        cleaned_lines = []

        for i, line in enumerate(lines):
            if self.is_junk_line(line):
                junk_count += 1
                # Keep track for reporting
                continue
            cleaned_lines.append(line)

        self.content = '\n'.join(cleaned_lines)
        self.stats['junk_lines_removed'] = junk_count

    def fix_obvious_latex_errors(self):
        """Fix only obvious LaTeX conversion errors (very conservative)"""
        fixed_count = 0

        # Pattern 1: Decimal percentage with spaces: "$9 . 3 \%$" or "$1 2 . 4 \%$" -> "9.3%" or "12.4%"
        def fix_decimal_percent(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract just the numbers and dots
            numbers = re.sub(r'[^\d.]', '', match.group(0))
            return numbers + '%'

        # Match: $ + digits/spaces + . + digits/spaces + \% + $
        self.content = re.sub(r'\$\s*[\d\s]+\.\s*[\d\s]+\s*\\%\s*\$', fix_decimal_percent, self.content)

        # Pattern 2: Integer percentage with spaces: "$4 0 \%$" -> "40%"
        def fix_percent(match):
            nonlocal fixed_count
            fixed_count += 1
            numbers = re.sub(r'[\s\\%$]+', '', match.group(0))
            numbers = re.sub(r'([0-9.]+)', r'\1', numbers)
            return numbers + '%'

        self.content = re.sub(r'\$\s*[0-9\s]+\s*\\?%\s*\$', fix_percent, self.content)

        # Pattern 3: Numbers with spaces in decimal (no %): "$4 . 5$" or "$1 2 . 3$" -> "4.5" or "12.3"
        def fix_decimal(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract just numbers and dots
            return re.sub(r'[^\d.]', '', match.group(0))

        self.content = re.sub(r'\$\s*[\d\s]+\.\s*[\d\s]+\s*\$', fix_decimal, self.content)

        # Pattern 4: Empty LaTeX commands: "\\textbf{}" -> ""
        empty_cmds = re.findall(r'\\[a-z]+\{\s*\}', self.content)
        fixed_count += len(empty_cmds)
        self.content = re.sub(r'\\[a-z]+\{\s*\}', '', self.content)

        # Pattern 5: Parenthesized percentages: "$( 2 1 . 6 \% )$" -> "(21.6%)"
        def fix_paren_percent(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract numbers and dots
            numbers = re.sub(r'[^\d.]', '', match.group(0))
            return '(' + numbers + '%)'

        self.content = re.sub(r'\$\(\s*[\d\s]+\.?\s*[\d\s]*\s*\\%\s*\)\$', fix_paren_percent, self.content)

        # Pattern 6: Percentage ranges in parentheses: "$( 5 0 - 7 5 \% )$" -> "(50-75%)"
        def fix_range_percent(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract all numbers
            nums = re.findall(r'\d+', match.group(0))
            if len(nums) >= 2:
                return f'({nums[0]}-{nums[1]}%)'
            return match.group(0)

        self.content = re.sub(r'\$\(\s*[\d\s]+-\s*[\d\s]+\s*\\%\s*\)\$', fix_range_percent, self.content)

        # Pattern 7: Multipliers with x: "$4 . 6 \mathrm { x }$" -> "4.6x"
        def fix_multiplier(match):
            nonlocal fixed_count
            fixed_count += 1
            numbers = re.sub(r'[^\d.]', '', match.group(0))
            return numbers + 'x'

        # Match various math formatting commands: \mathrm, \mathbf, \mathsf, etc.
        self.content = re.sub(r'\$\s*[\d\s]+\.?\s*[\d\s]*\s*\\math(?:rm|bf|sf|tt|it)\s*\{\s*[xX]\s*\}\s*\$', fix_multiplier, self.content)

        # Pattern 8: Simple numbers with spaces: "$1 5 0$" -> "150"
        def fix_spaced_number(match):
            nonlocal fixed_count
            fixed_count += 1
            return re.sub(r'[^\d+]', '', match.group(0))

        self.content = re.sub(r'\$\s*[\d\s]+\+?\s*\$', fix_spaced_number, self.content)

        # Pattern 9: Simple abbreviations: "$\mathrm { V 1 }$" -> "V1"
        def fix_abbrev(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract only alphanumeric and spaces
            text = re.sub(r'[^\w\s]', '', match.group(0))
            return text.replace(' ', '')

        self.content = re.sub(r'\$\\mathrm\s*\{\s*[A-Z\s\d]+\s*\}\s*\$', fix_abbrev, self.content)

        # Pattern 10: Empty math delimiters: "$ $" or "$  $" -> ""
        empty_math = re.findall(r'\$\s*\$', self.content)
        fixed_count += len(empty_math)
        self.content = re.sub(r'\$\s*\$', '', self.content)

        # Pattern 11: Arrow ranges (percentage transitions): "$( 0 . 0 3 \%  0 . 4 9 \%$" -> "(0.03% -> 0.49%)"
        def fix_arrow_range(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract all numbers with decimals
            nums = re.findall(r'\d+\.?\d*', match.group(0))
            if len(nums) >= 2:
                return f'({nums[0]}% -> {nums[1]}%)'
            return match.group(0)

        self.content = re.sub(r'\$\(?\s*[\d\s]+\.?\s*[\d\s]*\s*\\%\s+[\d\s]+\.?\s*[\d\s]*\s*\\%\s*\)?\$', fix_arrow_range, self.content)

        # Pattern 12: Percentage points: "$0 . 4 \mathrm { p p }$" -> "0.4pp"
        def fix_pp(match):
            nonlocal fixed_count
            fixed_count += 1
            numbers = re.sub(r'[^\d.]', '', match.group(0))
            return numbers + 'pp'

        self.content = re.sub(r'\$\s*[\d\s]+\.?\s*[\d\s]*\s*\\mathrm\s*\{\s*p\s*p\s*\}\s*\$', fix_pp, self.content)

        # Pattern 13: Parenthesized pp with sign: "$( + 4 . 5 { \mathrm { p p } } )$" -> "(+4.5pp)"
        def fix_paren_pp(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract sign, numbers and dots
            sign = '+' if '+' in match.group(0) else ('-' if '-' in match.group(0) else '')
            numbers = re.sub(r'[^\d.]', '', match.group(0))
            return f'({sign}{numbers}pp)'

        self.content = re.sub(r'\$\(\s*[+\-]?\s*[\d\s]+\.?\s*[\d\s]*\s*\{\s*\\mathrm\s*\{\s*p\s*p\s*\}\s*\}\s*\)\$', fix_paren_pp, self.content)

        # Pattern 14: Incomplete percentage range: "$( 2 5 \% - 7 5 \%$" -> "(25%-75%)"
        def fix_incomplete_range(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract all numbers
            nums = re.findall(r'\d+', match.group(0))
            if len(nums) >= 2:
                return f'({nums[0]}-{nums[1]}%)'
            return match.group(0)

        # Match: $( + numbers + \% + - + numbers + \% + $ (missing closing paren)
        self.content = re.sub(r'\$\(\s*[\d\s]+\s*\\%\s*-\s*[\d\s]+\s*\\%\s*\$', fix_incomplete_range, self.content)

        # Pattern 15: Complex abbreviations with superscripts (general purpose, content-based)
        # Matches: "${ \cal O } ^ { * } { \bf N } { \bf E } { \bf T }$" -> "O*NET"
        # Strategy: Match $ { ... } ^ { ... } ... $ structure, extract letters + stars
        def fix_complex_abbrev(match):
            nonlocal fixed_count
            fixed_count += 1
            text = match.group(0)
            # Step 1: Normalize star representations BEFORE removing commands
            text = text.replace(r'\ast', '*').replace(r'\star', '*')
            # Step 2: Remove all LaTeX commands
            text = re.sub(r'\\[a-z]+', '', text)
            # Step 3: Remove all special characters except letters and asterisk
            text = re.sub(r'[^A-Za-z*]', '', text)
            # Step 4: Handle 'ast' and 'star' remnants (from \ast, \star after \ removal)
            text = text.replace('ast', '*').replace('star', '*')
            # Step 5: Always uppercase (typical for abbreviations like O*NET)
            return text.upper()

        # Match: $ { ... } ^ { ... } ... $ - simple pattern, don't validate nesting
        # This catches various O*NET formatting styles with superscripts
        self.content = re.sub(r'\$\{[^$]*\}\s*\^\s*\{[^$]*\}[^$]*\$', fix_complex_abbrev, self.content)

        # Pattern 16: Simple name formatting: "$\mathsf { X } \mathsf { u }$" -> "Xu"
        def fix_name_format(match):
            nonlocal fixed_count
            fixed_count += 1
            # Extract only letters
            text = re.sub(r'[^\w]', '', match.group(0))
            return text

        # Match repeated \mathsf or similar commands with single letters
        self.content = re.sub(r'\$(?:\\math[a-z]{2}\s*\{\s*[A-Za-z]\s*\}\s*){2,}\$', fix_name_format, self.content)

        # Pattern 17: Author names with affiliation superscripts: "$\mathbf { B i } ^ { 2 }$" -> "Bi^2"
        def fix_author_name(match):
            nonlocal fixed_count
            fixed_count += 1
            text = match.group(0)
            # Step 1: Remove all LaTeX commands
            text = re.sub(r'\\[a-z]+', '', text)
            # Step 2: Extract letters and numbers separately
            letters = ''.join(c for c in text if c.isalpha())
            # Step 3: Find affiliation number (after ^)
            affiliation_match = re.search(r'\^\s*\{\s*(\d+)\s*\}', text)
            affiliation = '^' + affiliation_match.group(1) if affiliation_match else ''
            # Step 4: Capitalize first letter
            if letters:
                letters = letters[0].upper() + letters[1:].lower()
            return letters + affiliation

        # Match: $ + \cmd + { stuff with letters } + ^ + { number } + $
        # This pattern is for author names with affiliation numbers in academic papers
        self.content = re.sub(r'\$\\[a-z]+\s*\{[^$]*\}\s*(?:\^\s*\{[^}]*\})?\$', fix_author_name, self.content)

        self.stats['obvious_latex_fixed'] = fixed_count

    def normalize_blank_lines(self):
        """Reduce excessive blank lines to maximum 1 blank line (2 newlines)"""
        # Count before normalization
        before_lines = self.content.count('\n\n\n')

        # Reduce 3+ consecutive newlines to 2 (= 1 blank line)
        self.content = re.sub(r'\n{3,}', '\n\n', self.content)

        self.stats['blank_lines_normalized'] = before_lines

    def trim_trailing_whitespace(self):
        """Remove trailing whitespace from lines (100% safe)"""
        lines = self.content.split('\n')
        self.content = '\n'.join(line.rstrip() for line in lines)

    # ========== Issue Detection (No Modification) ==========

    def detect_uncertain_latex(self):
        """Detect LaTeX expressions that need manual review"""
        # Find all LaTeX expressions
        latex_pattern = re.compile(r'\$([^$]+)\$')

        for match in latex_pattern.finditer(self.content):
            expr = match.group(1)
            start = match.start()
            line_num = self.content[:start].count('\n') + 1

            # Get context (50 chars before and after)
            context_start = max(0, start - 50)
            context_end = min(len(self.content), match.end() + 50)
            context = self.content[context_start:context_end]

            # Categorize
            category = self._categorize_latex(expr, context)

            if category == 'uncertain':
                self.issues['uncertain_latex'].append({
                    'expression': expr,
                    'line': line_num,
                    'context': context,
                    'reason': self._explain_uncertainty(expr, context)
                })
            elif category == 'complex':
                self.issues['complex_latex'].append({
                    'expression': expr,
                    'line': line_num,
                    'context': context,
                    'suggestion': self._suggest_fix(expr, context)
                })

    def _categorize_latex(self, expr: str, context: str) -> str:
        """Categorize LaTeX expression: simple/complex/uncertain"""
        # Already handled "simple" in fix_obvious_latex_errors()

        # Check if it looks like valid math
        if self._is_valid_math_expression(expr):
            return 'uncertain'  # Might be intentional

        # Check if it has formatting commands
        if re.search(r'\\math(sf|rm|bf|it|tt)', expr):
            return 'complex'  # Likely conversion error but needs context

        # Short expressions in narrative text
        if len(expr) < 20 and self._is_in_narrative(context):
            return 'complex'

        return 'uncertain'

    def _is_valid_math_expression(self, expr: str) -> bool:
        """Check if expression looks like valid math"""
        # Has mathematical operators or structure
        math_indicators = [
            r'[+\-*/=<>]',      # Operators
            r'\^',               # Superscript
            r'_',                # Subscript
            r'\\frac',           # Fraction
            r'\\sum',            # Sum
            r'\\int',            # Integral
        ]

        # No formatting commands
        has_format_cmd = bool(re.search(r'\\math(sf|rm|bf)', expr))

        # Has math structure
        has_math = any(re.search(pattern, expr) for pattern in math_indicators)

        return has_math and not has_format_cmd

    def _is_in_narrative(self, context: str) -> bool:
        """Check if context is narrative text (vs formula section)"""
        narrative_words = [
            'is', 'are', 'was', 'were', 'the', 'a', 'an', 'of',
            'in', 'to', 'for', 'with', 'at', 'by', 'from'
        ]
        return sum(1 for word in narrative_words if word in context.lower()) >= 3

    def _suggest_fix(self, expr: str, context: str) -> str:
        """Suggest fix for complex LaTeX"""
        # Remove mathsf/mathrm/mathbf commands
        fixed = re.sub(r'\\math(sf|rm|bf|it|tt)\{([^}]+)\}', r'\2', expr)
        # Remove extra spaces
        fixed = re.sub(r'\s+', ' ', fixed).strip()
        return fixed

    def _explain_uncertainty(self, expr: str, context: str) -> str:
        """Explain why expression is uncertain"""
        reasons = []

        if self._is_valid_math_expression(expr):
            reasons.append("Contains mathematical notation")

        if len(expr) < 10:
            reasons.append("Short expression")

        if not self._is_in_narrative(context):
            reasons.append("Not in narrative context")

        return "; ".join(reasons) if reasons else "Needs manual review"

    def detect_potential_problems(self):
        """Detect other potential issues"""
        # Check for unbalanced code blocks
        fenced_blocks = re.findall(r'```', self.content)
        if len(fenced_blocks) % 2 != 0:
            self.issues['potential_problems'].append({
                'type': 'unbalanced_code_blocks',
                'description': f'Found {len(fenced_blocks)} code fence markers (should be even)'
            })

        # Check for suspiciously long lines
        lines = self.content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 500 and not line.strip().startswith('|'):  # Ignore table rows
                self.issues['potential_problems'].append({
                    'type': 'long_line',
                    'line': i,
                    'length': len(line),
                    'preview': line[:100] + '...'
                })

    # ========== Code Block Preservation ==========

    def preserve_code_blocks(self, operation_func):
        """Execute operation while preserving code blocks"""
        # Extract fenced code blocks
        code_blocks = []

        def replace_code_block(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        # Temporarily replace code blocks
        self.content = re.sub(r'```.*?```', replace_code_block, self.content, flags=re.DOTALL)

        # Execute operation
        operation_func()

        # Restore code blocks
        for i, block in enumerate(code_blocks):
            self.content = self.content.replace(f"__CODE_BLOCK_{i}__", block)

    # ========== Main Processing Pipeline ==========

    def clean(self):
        """Execute safe cleaning pipeline"""
        print("=" * 60)
        print("Markdown Safe Cleaner - Processing")
        print("=" * 60)

        print(f"\nInput: {self.input_file}")
        print(f"Size: {len(self.content):,} characters")

        # Round 1: Control characters and whitespace
        print("\n[Round 1] Control character cleanup...")
        self.remove_control_characters()
        self.normalize_whitespace()
        # IMPORTANT: Normalize blank lines immediately after removing control chars
        # Control char removal can create excessive blank lines
        self.normalize_blank_lines()
        print(f"  Control chars removed: {self.stats['control_chars_removed']}")
        print(f"  Tabs converted: {self.stats['tabs_converted']}")
        print(f"  Non-breaking spaces: {self.stats['nbsp_converted']}")
        print(f"  Zero-width spaces: {self.stats['zwsp_removed']}")
        print(f"  Blank lines normalized: {self.stats['blank_lines_normalized']}")

        # Round 2: Structural cleanup
        print("\n[Round 2] Structural cleanup...")
        self.remove_orphaned_symbols()
        self.remove_junk_lines()
        self.fix_obvious_latex_errors()
        print(f"  Orphaned symbols removed: {self.stats['orphaned_symbols_removed']}")
        print(f"  Junk lines removed: {self.stats['junk_lines_removed']}")
        print(f"  Obvious LaTeX fixed: {self.stats['obvious_latex_fixed']}")

        # Round 3: Final normalization
        print("\n[Round 3] Final normalization...")
        # Re-normalize blank lines in case Round 2 created new ones
        blank_before_final = self.content.count('\n\n\n')
        self.content = re.sub(r'\n{3,}', '\n\n', self.content)
        blank_after_final = blank_before_final - self.content.count('\n\n\n')
        if blank_after_final > 0:
            print(f"  Additional blank lines normalized: {blank_after_final}")

        # Trim trailing whitespace
        self.trim_trailing_whitespace()
        print(f"  Trailing whitespace trimmed")

        # CRITICAL: Trim can create new blank lines (spaces-only lines become empty)
        # Final pass to ensure no excessive blank lines remain
        final_blank_count = self.content.count('\n\n\n')
        if final_blank_count > 0:
            self.content = re.sub(r'\n{3,}', '\n\n', self.content)
            print(f"  Final blank line cleanup: {final_blank_count} locations fixed")

        # Issue detection
        print("\n[Detection] Analyzing remaining issues...")
        self.detect_uncertain_latex()
        self.detect_potential_problems()
        print(f"  Uncertain LaTeX: {len(self.issues['uncertain_latex'])}")
        print(f"  Complex LaTeX: {len(self.issues['complex_latex'])}")
        print(f"  Potential problems: {len(self.issues['potential_problems'])}")

    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        return {
            'input_file': str(self.input_file),
            'statistics': self.stats,
            'issues_for_review': {
                'uncertain_latex': self.issues['uncertain_latex'][:20],  # Limit to 20
                'complex_latex': self.issues['complex_latex'][:20],
                'potential_problems': self.issues['potential_problems']
            },
            'summary': {
                'total_safe_fixes': sum(self.stats.values()),
                'needs_manual_review': len(self.issues['uncertain_latex']) + len(self.issues['complex_latex']),
                'content_preserved': True
            }
        }

    def save(self, output_file: str, report_file: Optional[str] = None):
        """Save cleaned content and optional report"""
        # Save cleaned markdown with Unix line endings
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Force Unix line endings to prevent Windows \r\n conversion
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self.content)

        print(f"\n{'=' * 60}")
        print(f"Output saved: {output_path}")
        print(f"Size: {len(self.content):,} characters")

        # Save report if requested
        if report_file:
            report_path = Path(report_file)
            report = self.generate_report()
            report_path.write_text(
                json.dumps(report, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"Report saved: {report_path}")

        print("=" * 60)


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python markdown_safe_cleaner.py <input.md> <output.md> [report.json]")
        print("\nExample:")
        print("  python markdown_safe_cleaner.py input.md cleaned.md report.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    report_file = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        cleaner = MarkdownSafeCleaner(input_file)
        cleaner.clean()
        cleaner.save(output_file, report_file)

        # Print summary
        report = cleaner.generate_report()
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Safe fixes applied: {report['summary']['total_safe_fixes']}")
        print(f"Issues need review: {report['summary']['needs_manual_review']}")
        print(f"Content preserved: {report['summary']['content_preserved']}")

        if report['summary']['needs_manual_review'] > 0:
            print(f"\nReview report for details: {report_file}")

        print("\nProcessing complete!")

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()