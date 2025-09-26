#!/usr/bin/env python3
"""
batch_process_pdfs.py
Batch process multiple PDFs using art-materials-processor
"""

import sys
import os
from pathlib import Path
import subprocess
import json
from datetime import datetime

def process_pdf_batch(input_dir, output_base_dir="batch_output"):
    """Process all PDFs in a directory"""

    input_path = Path(input_dir)
    output_base = Path(output_base_dir)

    if not input_path.exists():
        print(f"Error: Input directory not found: {input_path}")
        return False

    # Find all PDF files
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {input_path}")
        return False

    print(f"Found {len(pdf_files)} PDF files to process")
    print("-" * 50)

    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_base / f"batch_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Track processing results
    results = {
        "timestamp": timestamp,
        "input_directory": str(input_path),
        "output_directory": str(output_dir),
        "total_files": len(pdf_files),
        "processed": [],
        "failed": []
    }

    # Process each PDF
    processor_script = Path(__file__).parent / "art-materials-processor.py"
    python_exe = sys.executable

    for idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file.name}")
        print("-" * 30)

        try:
            # Run the processor
            cmd = [
                python_exe,
                str(processor_script),
                str(pdf_file),
                "--output-dir", str(output_dir)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per PDF
            )

            if result.returncode == 0:
                print(f"  SUCCESS: {pdf_file.name}")
                results["processed"].append({
                    "file": pdf_file.name,
                    "status": "success",
                    "output_dir": str(output_dir / pdf_file.stem)
                })
            else:
                print(f"  FAILED: {pdf_file.name}")
                print(f"  Error: {result.stderr[:200]}")
                results["failed"].append({
                    "file": pdf_file.name,
                    "status": "failed",
                    "error": result.stderr[:500]
                })

        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT: {pdf_file.name} (exceeded 5 minutes)")
            results["failed"].append({
                "file": pdf_file.name,
                "status": "timeout",
                "error": "Processing exceeded 5 minute timeout"
            })
        except Exception as e:
            print(f"  ERROR: {pdf_file.name}")
            print(f"  {str(e)}")
            results["failed"].append({
                "file": pdf_file.name,
                "status": "error",
                "error": str(e)
            })

    # Save batch report
    report_file = output_dir / "batch_processing_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 50)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 50)
    print(f"Total files: {len(pdf_files)}")
    print(f"Successfully processed: {len(results['processed'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Output directory: {output_dir}")
    print(f"Report saved: {report_file}")

    return len(results['failed']) == 0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch process PDFs with MinerU")
    parser.add_argument("input_dir", help="Directory containing PDF files")
    parser.add_argument("--output-dir", default="batch_output",
                       help="Base output directory (default: batch_output)")

    args = parser.parse_args()

    success = process_pdf_batch(args.input_dir, args.output_dir)
    sys.exit(0 if success else 1)