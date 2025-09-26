#!/usr/bin/env python3
"""
art-materials-processor.py
Process PDF materials using MinerU Pipeline AUTO mode
With CONSERVATIVE orphan image handling - preserves document integrity
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image

def run_mineru(pdf_path, output_dir):
    """Run MinerU on PDF file"""
    mineru_exe = Path("D:/NOVELSYS-SWARM/.claude/mineru-env/Scripts/mineru.exe")

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
        print(f"MinerU failed: {result.stderr[:500]}")
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
            print(f"      Error analyzing {orphan_info['filename']}: {e}")
            continue

    return meaningful


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
        print(f"    Filtering {orphan_report['orphan_images']} orphan images...")
        meaningful_orphans = filter_meaningful_images(orphan_report["orphans"], images_dir)
        print(f"    {len(meaningful_orphans)} meaningful orphans found")

        if not meaningful_orphans:
            orphan_report["filtered_out"] = len(orphan_report["orphans"])
            orphan_report["handling_method"] = "All orphans filtered as artifacts"
            return orphan_report

        # Read current markdown
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # No longer creating backup since the process is stable
        # Original content is always preserved, only appending orphans

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

        print(f"    Conservative handling: {len(meaningful_orphans)} orphan images appended to document end")
        if orphan_report["filtered_artifacts"] > 0:
            print(f"    Filtered out: {orphan_report['filtered_artifacts']} likely artifacts")

        return orphan_report

    except Exception as e:
        orphan_report["error"] = str(e)
        print(f"    Error in conservative orphan handling: {e}")
        return orphan_report


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

    # Create simple orphan entries (no metadata needed)
    for filename in orphans:
        orphan_report["orphans"].append({
            "filename": filename
        })

    return orphan_report


def process_pdf_to_markdown(pdf_path, output_dir="output", enable_conservative_orphans=True):
    """Process PDF with MinerU and handle orphan images conservatively"""

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        return False

    pdf_name = pdf_path.stem
    print(f"Processing: {pdf_path}")

    # Create output directories
    mineru_output_dir = output_dir / "mineru_temp"
    final_output_dir = output_dir / pdf_name

    mineru_output_dir.mkdir(parents=True, exist_ok=True)
    final_output_dir.mkdir(parents=True, exist_ok=True)

    # Run MinerU
    print("  Running MinerU extraction...")
    if not run_mineru(pdf_path, mineru_output_dir):
        return False

    # Find MinerU output (MinerU creates PDF_name/auto/ subdirectory)
    auto_dirs = list(mineru_output_dir.glob("*/auto"))
    if not auto_dirs:
        print(f"  Error: MinerU output not found in {mineru_output_dir}")
        return False

    auto_dir = auto_dirs[0]
    pdf_name_from_output = auto_dir.parent.name

    # Copy essential files to final output (excluding content_list.json)
    essential_files = [
        f"{pdf_name_from_output}.md",
        f"{pdf_name_from_output}_origin.pdf"
    ]

    for filename in essential_files:
        src = auto_dir / filename
        if src.exists():
            dst = final_output_dir / filename.replace(pdf_name_from_output, pdf_name)
            shutil.copy2(src, dst)
        else:
            print(f"    Warning: Expected file not found: {src}")

    # Copy images directory
    src_images = auto_dir / "images"
    if src_images.exists():
        dst_images = final_output_dir / "images"
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)

    # Handle orphan images conservatively if enabled
    if enable_conservative_orphans:
        orphan_report = conservative_orphan_handling(
            final_output_dir / f"{pdf_name}.md",
            final_output_dir / "images"
        )
    else:
        # Just detect orphans without handling
        orphan_report = detect_orphan_images(
            final_output_dir / f"{pdf_name}.md",
            final_output_dir / "images"
        )

    # Handle reporting based on orphan status
    if orphan_report["orphan_images"] > 0:
        if orphan_report.get("orphans_appended"):
            # Orphans were found and handled
            print(f"    Orphan images: {orphan_report['orphans_appended']} appended to document")
            # No report file needed after handling - all images are now in markdown
        else:
            print(f"    Warning: {orphan_report['orphan_images']} orphan images detected but not handled")
    else:
        # No orphans - all images are referenced
        print(f"    All {orphan_report['total_images']} images are properly referenced")

    # Clean up temporary MinerU output (removes all the extra PDFs and JSONs)
    shutil.rmtree(mineru_output_dir)

    print(f"  Complete: {final_output_dir}")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process PDF with MinerU and conservative orphan handling")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--output-dir", default="output", help="Output directory (default: output)")
    parser.add_argument("--no-orphan-handling", action="store_true",
                       help="Disable conservative orphan image handling")

    args = parser.parse_args()

    success = process_pdf_to_markdown(
        args.pdf_path,
        args.output_dir,
        enable_conservative_orphans=not args.no_orphan_handling
    )

    sys.exit(0 if success else 1)