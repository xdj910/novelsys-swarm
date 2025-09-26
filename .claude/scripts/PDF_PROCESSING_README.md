# PDF Processing Scripts

## Current Active Script

### process_pdf_materials.py
**Status: ACTIVE**
**Purpose: Unified PDF processor with auto-detection**

Single command for all PDF processing needs:
- Automatically detects if input is a file or directory
- Processes single PDF or batch PDFs accordingly
- Always handles orphan images with conservative approach
- Produces clean output without redundant files

#### Usage:
```bash
# Single PDF file
python process_pdf_materials.py "path/to/file.pdf"

# Directory with multiple PDFs
python process_pdf_materials.py "path/to/pdf/folder"

# Custom output directory
python process_pdf_materials.py "input" --output-dir "custom_output"
```

#### Output Structure:
```
# Single PDF:
output/
  PDF_name/
    PDF_name.md          # Markdown with all images
    PDF_name_origin.pdf  # Original PDF copy
    images/              # All extracted images

# Batch processing:
output/
  batch_YYYYMMDD_HHMMSS/
    PDF1_name/
    PDF2_name/
    batch_processing_report.json
```

## Archived Scripts

Located in: `.claude/scripts/archived_scripts/`

### art-materials-processor.py
**Status: ARCHIVED**
**Reason: Replaced by unified script**
Original single PDF processor with orphan handling

### batch_process_pdfs.py
**Status: ARCHIVED**
**Reason: Replaced by unified script**
Original batch PDF processor

## Features

- **MinerU Pipeline AUTO mode**: Optimized PDF extraction
- **Conservative orphan handling**: Appends unreferenced images to document end
- **Smart filtering**: Removes artifacts (images <100x100px or <5KB)
- **Clean output**: No unnecessary files (no content_list.json, no backups, no reports after processing)

## For Agents

Use the unified script for all PDF processing:
```python
import subprocess

result = subprocess.run([
    "python",
    ".claude/scripts/process_pdf_materials.py",
    input_path,  # Can be file or directory
    "--output-dir", output_dir
], capture_output=True, text=True)
```

---
Last updated: 2025-09-23