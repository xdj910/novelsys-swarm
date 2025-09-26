#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
art-materials-processor.py
Unified PDF processor with auto-detection for single file or batch processing
Automatically handles orphan images with conservative approach
Unicode-safe for Windows paths with Chinese characters

Configuration:
- Set MINERU_PATH environment variable to override default MinerU location
- Default: D:/NOVELSYS-SWARM/.claude/mineru-env/Scripts/mineru.exe
- Example: export MINERU_PATH=/path/to/mineru.exe
"""

import sys
import os

# Set UTF-8 encoding for stdout to handle Chinese characters
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from PIL import Image


# Unicode-safe printing functions for Windows
def safe_print(message):
    """Print message safely, handling Unicode encoding errors"""
    try:
        print(message)
    except UnicodeEncodeError:
        try:
            # Try to encode as ASCII with replacement
            safe_msg = str(message).encode('ascii', errors='replace').decode('ascii')
            print(f"[UNICODE_SAFE] {safe_msg}")
        except:
            print("[UNICODE_SAFE] Message contains non-displayable characters")


def safe_format_path(path):
    """Format path for safe display, handling Unicode"""
    try:
        return str(path)
    except UnicodeEncodeError:
        try:
            # Replace problematic characters with ?
            return str(path).encode('ascii', errors='replace').decode('ascii')
        except:
            return "[Path with Unicode characters]"


def run_mineru(pdf_path, output_dir):
    """Run MinerU on PDF file"""
    # Try environment variable first, fall back to default path
    mineru_path = os.environ.get('MINERU_PATH', 'D:/NOVELSYS-SWARM/.claude/mineru-env/Scripts/mineru.exe')
    mineru_exe = Path(mineru_path)

    # Check if MinerU exists
    if not mineru_exe.exists():
        safe_print(f"ERROR: MinerU not found at {mineru_exe}")
        safe_print("Set MINERU_PATH environment variable or install MinerU at default location")
        return False

    cmd = [
        str(mineru_exe),
        "-p", str(pdf_path),
        "-o", str(output_dir),
        "-m", "auto",
        "-b", "pipeline",
        "--formula", "True",
        "--table", "True"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        safe_print(f"MinerU failed: {result.stderr[:500]}")
        return False
    return True


def filter_meaningful_images(orphan_list, images_dir, min_size=(100, 100)):
    """Filter out likely artifacts from orphan images"""
    meaningful = []

    for orphan_info in orphan_list:
        try:
            img_path = images_dir / orphan_info["filename"]
            if not img_path.exists():
                continue

            with Image.open(img_path) as img:
                width, height = img.size

                # Filter criteria:
                # 1. Minimum size (avoid tiny icons/artifacts)
                # 2. Reasonable aspect ratio (avoid line artifacts)
                # 3. Sufficient file size (avoid nearly empty images)

                if width < min_size[0] or height < min_size[1]:
                    continue

                aspect_ratio = max(width, height) / min(width, height)
                if aspect_ratio > 10:  # Likely a line or artifact
                    continue

                file_size = img_path.stat().st_size
                if file_size < 5000:  # Less than 5KB likely artifact
                    continue

                meaningful.append(orphan_info)

        except Exception as e:
            safe_print(f"      Error analyzing {orphan_info['filename']}: {e}")
            continue

    return meaningful


def detect_orphan_images(markdown_path, images_dir):
    """Detect orphan images and generate report"""
    import re

    orphan_report = {
        "total_images": 0,
        "referenced_images": 0,
        "orphan_images": 0,
        "orphans": []
    }

    # Get all image files
    if images_dir.exists():
        all_images = set(f.name for f in images_dir.glob("*.jpg"))
        orphan_report["total_images"] = len(all_images)
    else:
        return orphan_report

    # Get referenced images from markdown
    referenced = set()
    if markdown_path.exists():
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
            refs = re.findall(r'images/([a-f0-9]+\.jpg)', content)
            referenced = set(refs)

    orphan_report["referenced_images"] = len(referenced)

    # Find orphans
    orphans = all_images - referenced
    orphan_report["orphan_images"] = len(orphans)

    # Create simple orphan entries
    for filename in orphans:
        orphan_report["orphans"].append({
            "filename": filename
        })

    return orphan_report


def conservative_orphan_handling(markdown_path, images_dir):
    """
    CONSERVATIVE approach: Append orphan images to end with clear labeling
    This preserves document integrity while making orphans available
    """

    orphan_report = detect_orphan_images(markdown_path, images_dir)

    if orphan_report["orphan_images"] == 0:
        return orphan_report

    try:
        # Filter out likely artifacts
        safe_print(f"    Filtering {orphan_report['orphan_images']} orphan images...")
        meaningful_orphans = filter_meaningful_images(orphan_report["orphans"], images_dir)
        safe_print(f"    {len(meaningful_orphans)} meaningful orphans found")

        if not meaningful_orphans:
            orphan_report["filtered_out"] = len(orphan_report["orphans"])
            orphan_report["handling_method"] = "All orphans filtered as artifacts"
            return orphan_report

        # Read current markdown
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Append orphan images section to end of document
        orphan_section = "\n\n---\n\n"
        orphan_section += "## Additional Images Found\n\n"
        orphan_section += "*The following images were extracted from the PDF but not referenced in the main document. "
        orphan_section += "They may be appendix figures, supplementary materials, or processing artifacts.*\n\n"

        for idx, orphan_info in enumerate(meaningful_orphans, 1):
            filename = orphan_info["filename"]
            orphan_section += f"### Additional Image {idx}\n"
            orphan_section += f"![Additional Image {idx}](images/{filename})\n\n"

        # Write updated content
        updated_content = content + orphan_section
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Update report
        orphan_report["handling_method"] = "Conservative appendix"
        orphan_report["orphans_appended"] = len(meaningful_orphans)
        orphan_report["appendix_added"] = True
        orphan_report["filtered_artifacts"] = len(orphan_report["orphans"]) - len(meaningful_orphans)

        safe_print(f"    Conservative handling: {len(meaningful_orphans)} orphan images appended to document end")
        if orphan_report["filtered_artifacts"] > 0:
            safe_print(f"    Filtered out: {orphan_report['filtered_artifacts']} likely artifacts")

        return orphan_report

    except Exception as e:
        orphan_report["error"] = str(e)
        safe_print(f"    Error in conservative orphan handling: {e}")
        return orphan_report


def process_single_pdf(pdf_path, output_dir):
    """Process a single PDF file"""

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        safe_print(f"Error: PDF not found: {safe_format_path(pdf_path)}")
        return False

    pdf_name = pdf_path.stem
    safe_print(f"Processing: {safe_format_path(pdf_path)}")

    # Create output directories
    mineru_output_dir = output_dir / "mineru_temp"
    final_output_dir = output_dir / pdf_name

    mineru_output_dir.mkdir(parents=True, exist_ok=True)
    final_output_dir.mkdir(parents=True, exist_ok=True)

    # Run MinerU
    safe_print("  Running MinerU extraction...")
    if not run_mineru(pdf_path, mineru_output_dir):
        return False

    # Find MinerU output (MinerU creates PDF_name/auto/ subdirectory)
    auto_dirs = list(mineru_output_dir.glob("*/auto"))
    if not auto_dirs:
        safe_print(f"  Error: MinerU output not found in {safe_format_path(mineru_output_dir)}")
        return False

    auto_dir = auto_dirs[0]
    pdf_name_from_output = auto_dir.parent.name

    # Copy essential files to final output
    essential_files = [
        f"{pdf_name_from_output}.md",
        f"{pdf_name_from_output}_origin.pdf"
    ]

    for filename in essential_files:
        src = auto_dir / filename
        if src.exists():
            dst = final_output_dir / filename.replace(pdf_name_from_output, pdf_name)
            shutil.copy2(src, dst)

    # Copy images directory
    src_images = auto_dir / "images"
    if src_images.exists():
        dst_images = final_output_dir / "images"
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)

    # Clean markdown with all 17 patterns - save to separate file
    md_original = final_output_dir / f"{pdf_name}_original.md"
    md_cleaned = final_output_dir / f"{pdf_name}.md"

    # Rename MinerU output to _original.md
    if md_cleaned.exists():
        shutil.copy2(md_cleaned, md_original)
        safe_print(f"  Saved original markdown as: {pdf_name}_original.md")

    # Clean the markdown (output to same file)
    if md_original.exists():
        safe_print("  Cleaning markdown (Pattern 1-17)...")
        cleaner_script = Path(__file__).parent / "markdown_safe_cleaner.py"

        try:
            result = subprocess.run(
                [sys.executable, str(cleaner_script), str(md_original), str(md_cleaned)],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                safe_print("  Markdown cleaning complete")
                safe_print(f"    Original: {pdf_name}_original.md")
                safe_print(f"    Cleaned:  {pdf_name}.md")
            else:
                safe_print(f"  Warning: Markdown cleaning had issues: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            safe_print("  Warning: Markdown cleaning timed out")
        except Exception as clean_err:
            safe_print(f"  Warning: Markdown cleaning error: {clean_err}")

    # Clean up - remove ALL unnecessary files
    # Keep: _origin.pdf, _original.md, .md, images/
    safe_print("  Cleaning up unnecessary files...")

    # Files to keep (two markdown files now)
    keep_files = {
        f"{pdf_name}_origin.pdf",
        f"{pdf_name}_original.md",
        f"{pdf_name}.md"
    }

    # Remove all files except the ones we want to keep
    for item in final_output_dir.iterdir():
        if item.is_file() and item.name not in keep_files:
            try:
                item.unlink()
                safe_print(f"    Removed: {item.name}")
            except Exception as e:
                safe_print(f"    Warning: Could not remove {item.name}: {e}")
        elif item.is_dir() and item.name != "images":
            try:
                shutil.rmtree(item)
                safe_print(f"    Removed directory: {item.name}")
            except Exception as e:
                safe_print(f"    Warning: Could not remove {item.name}: {e}")

    # Clean up temporary MinerU output
    shutil.rmtree(mineru_output_dir)

    safe_print(f"  Complete: {safe_format_path(final_output_dir)}")
    safe_print(f"    Files: {pdf_name}_origin.pdf, {pdf_name}_original.md, {pdf_name}.md, images/")
    safe_print(f"    NOTE: Agent should verify markdown integrity before deleting _original.md")

    # Delete source PDF after successful processing (single file mode)
    if pdf_path.exists() and pdf_path.is_file():
        try:
            pdf_path.unlink()
            safe_print(f"  Source file deleted: {pdf_path.name}")
        except Exception as del_e:
            safe_print(f"  Warning: Could not delete source file: {del_e}")

    return True


def process_batch_pdfs(input_dir, output_dir):
    """Process all PDFs in a directory"""

    input_path = Path(input_dir)
    output_base = Path(output_dir)

    # Find all PDF files
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        safe_print(f"No PDF files found in: {safe_format_path(input_path)}")
        return False

    safe_print(f"Found {len(pdf_files)} PDF files to process")
    safe_print("-" * 50)

    # Create output directory (no timestamp)
    output_base.mkdir(parents=True, exist_ok=True)

    # Track processing results (for internal use only)
    success_count = 0
    failed_count = 0
    processed_files = []

    # Process each PDF
    for idx, pdf_file in enumerate(pdf_files, 1):
        safe_print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file.name}")
        safe_print("-" * 30)

        try:
            success = process_single_pdf(pdf_file, output_base)

            if success:
                safe_print(f"  SUCCESS: {pdf_file.name}")
                success_count += 1
                processed_files.append(pdf_file)
                # Note: Source PDF already deleted in process_single_pdf()
            else:
                safe_print(f"  FAILED: {pdf_file.name}")
                failed_count += 1

        except Exception as e:
            safe_print(f"  ERROR: {pdf_file.name}")
            safe_print(f"  {str(e)}")
            failed_count += 1

    # Print summary (no report file)
    safe_print("\n" + "=" * 50)
    safe_print("BATCH PROCESSING COMPLETE")
    safe_print("=" * 50)
    safe_print(f"Total files: {len(pdf_files)}")
    safe_print(f"Successfully processed: {success_count}")
    safe_print(f"Failed: {failed_count}")
    safe_print(f"Output directory: {safe_format_path(output_base)}")

    return failed_count == 0


def process_pdf_materials(input_path, output_dir="output"):
    """
    Main function that auto-detects input type and processes accordingly

    Args:
        input_path: Path to a PDF file or directory containing PDFs
        output_dir: Output directory (default: output)
    """

    input_path = Path(input_path)

    if not input_path.exists():
        safe_print(f"Error: Path not found: {safe_format_path(input_path)}")
        return False

    # Auto-detect: is it a file or directory?
    if input_path.is_file():
        if input_path.suffix.lower() != '.pdf':
            safe_print(f"Error: Not a PDF file: {safe_format_path(input_path)}")
            return False

        safe_print("Detected: Single PDF file")
        return process_single_pdf(input_path, output_dir)

    elif input_path.is_dir():
        safe_print("Detected: Directory (batch processing mode)")
        return process_batch_pdfs(input_path, output_dir)

    else:
        safe_print(f"Error: Unknown input type: {safe_format_path(input_path)}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process PDF materials with MinerU - auto-detects single file or batch mode"
    )
    parser.add_argument(
        "input",
        help="Path to PDF file or directory containing PDFs"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory (default: output)"
    )

    args = parser.parse_args()

    success = process_pdf_materials(args.input, args.output_dir)
    sys.exit(0 if success else 1)