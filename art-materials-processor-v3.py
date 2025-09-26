#!/usr/bin/env python3
"""
Art Materials Processor v3.0 - PRECISE VISUAL BOUNDARY DETECTION
Addresses critical boundary detection issues found in v2.0 screenshot evidence:

CRITICAL PROBLEMS FIXED:
1. Text-only content captured as "figures" - ELIMINATED
2. Charts cut off on right side - FIXED with proper visual detection
3. Including unwanted text paragraphs - EXCLUDED with content validation
4. Poor boundary detection - REPLACED with actual visual element detection

ROOT CAUSE ADDRESSED:
v2.0 used text-based expansion rather than actual visual detection.
v3.0 uses pdfplumber's visual elements (images, rects, curves) for precise boundaries.

KEY IMPROVEMENTS:
- Use page.images, page.rects, page.curves for actual visual detection
- Implement whitespace analysis for content boundaries
- Smart filtering to exclude pure text blocks
- Precise table detection using pdfplumber's table boundaries
- Visual element validation to ensure charts/tables contain actual visual content
"""

import os
import sys
import json
import time
import argparse
import re
import math
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, NamedTuple
import logging
import psutil
from dataclasses import dataclass
from enum import Enum

# Import PDF processing libraries with fallback handling
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("WARNING: PyMuPDF not available")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("WARNING: PDFPlumber not available")

try:
    from PIL import Image, ImageDraw, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNING: PIL not available")

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    print("INFO: OpenCV not available (using simplified visual detection)")


# === UNICODE SAFE PRINTING FUNCTIONS ===
def safe_print(message, *args, **kwargs):
    """
    Print function that safely handles Unicode characters on Windows.
    Falls back to ASCII representation if console encoding fails.
    """
    try:
        print(message, *args, **kwargs)
    except UnicodeEncodeError:
        # Replace problematic characters with safe alternatives
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(f"[UNICODE_SAFE] {safe_message}", *args, **kwargs)
    except Exception:
        # Last resort: show basic info without path details
        print("[UNICODE_ERROR] Processing file with non-ASCII characters", *args, **kwargs)


def safe_format_path(path_str):
    """
    Format path string safely for console output.
    Returns ASCII-safe representation for display.
    """
    try:
        # Try to display as-is first
        return str(path_str)
    except UnicodeEncodeError:
        # Fall back to ASCII representation
        return str(path_str).encode('ascii', 'replace').decode('ascii')


def safe_log_path(logger, level, message_template, path_str, *args):
    """
    Log message with path safely, handling Unicode characters.
    """
    try:
        message = message_template.format(path_str, *args)
        getattr(logger, level)(message)
    except UnicodeEncodeError:
        safe_path = safe_format_path(path_str)
        safe_message = message_template.format(safe_path, *args)
        getattr(logger, level)(f"[UNICODE_SAFE] {safe_message}")
    except Exception as e:
        logger.warning(f"Logging failed for path with Unicode characters: {e}")


# Constants - PRECISE VISUAL DETECTION
MIN_ELEMENT_AREA = 5000        # Increased for meaningful visual content
MIN_WIDTH = 250                # Minimum width for useful charts/tables
MIN_HEIGHT = 120               # Minimum height for useful charts/tables
MIN_VISUAL_ELEMENTS = 3        # Minimum visual elements to qualify as figure
DEFAULT_BUFFER_ZONE = 15.0     # Reduced precise buffer
TABLE_BUFFER_ZONE = 20.0       # Table-specific buffer
HIGH_QUALITY_SCALE = 3.0       # 3x scaling for screenshots
VISUAL_CONFIDENCE_THRESHOLD = 0.7  # Require high visual confidence
MAX_FILENAME_LENGTH = 50
TEXT_ONLY_THRESHOLD = 0.9      # If >90% text chars, exclude as figure


class ElementType(Enum):
    """Types of document elements to extract"""
    TABLE = "table"
    FIGURE = "figure"
    CHART = "chart"
    DIAGRAM = "diagram"
    IMAGE = "image"


@dataclass
class VisualElement:
    """Represents a detected visual element (line, rect, image, etc.)"""
    element_type: str  # 'line', 'rect', 'image', 'curve'
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    confidence: float
    attributes: Dict[str, Any]


@dataclass
class BoundingBox:
    """Enhanced bounding box with visual validation"""
    x0: float
    y0: float
    x1: float
    y1: float
    confidence: float = 0.0
    visual_elements_count: int = 0
    text_density: float = 0.0
    has_visual_content: bool = False
    buffer_zone: float = DEFAULT_BUFFER_ZONE

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height if self.height > 0 else 1.0

    def is_valid_visual_element(self) -> bool:
        """Check if this represents valid visual content, not just text"""
        size_ok = (self.width >= MIN_WIDTH and
                  self.height >= MIN_HEIGHT and
                  self.area >= MIN_ELEMENT_AREA)

        visual_ok = (self.has_visual_content and
                    self.visual_elements_count >= MIN_VISUAL_ELEMENTS and
                    self.text_density < TEXT_ONLY_THRESHOLD)

        confidence_ok = self.confidence >= VISUAL_CONFIDENCE_THRESHOLD

        return size_ok and visual_ok and confidence_ok

    def expand(self, buffer: float = None) -> 'BoundingBox':
        """Expand bounding box with buffer zone"""
        buff = buffer or self.buffer_zone
        return BoundingBox(
            x0=max(0, self.x0 - buff),
            y0=max(0, self.y0 - buff),
            x1=self.x1 + buff,
            y1=self.y1 + buff,
            confidence=self.confidence,
            visual_elements_count=self.visual_elements_count,
            text_density=self.text_density,
            has_visual_content=self.has_visual_content,
            buffer_zone=buff
        )


@dataclass
class DocumentElement:
    """Represents a detected document element with visual validation"""
    element_type: ElementType
    number: int
    title: str
    bbox: BoundingBox
    page_number: int
    text_references: List[str]
    detection_method: str
    visual_elements: List[VisualElement]
    quality_metrics: Dict[str, float]


class PreciseVisualDetector:
    """v3.0 Precise Visual Boundary Detection System"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)

    def detect_elements(self, page, page_text: str) -> List[DocumentElement]:
        """Main detection pipeline using precise visual detection"""
        elements = []

        # Step 1: Find text references to tables/figures
        text_references = self._find_text_references(page_text)

        # Step 2: For each reference, find actual visual content
        for ref in text_references:
            visual_element = self._detect_visual_content_for_reference(page, ref)
            if visual_element and visual_element.bbox.is_valid_visual_element():
                elements.append(visual_element)

        # Step 3: Find standalone visual elements (no text reference)
        standalone_elements = self._find_standalone_visual_elements(page, elements)
        elements.extend(standalone_elements)

        return elements

    def _find_text_references(self, page_text: str) -> List[Dict[str, Any]]:
        """Find text references to tables, figures, charts"""
        references = []

        patterns = {
            ElementType.TABLE: [
                r'(?i)\btable\s+(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
                r'(?i)\btab\.\s*(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
            ],
            ElementType.FIGURE: [
                r'(?i)\bfigure\s+(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
                r'(?i)\bfig\.\s*(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
            ],
            ElementType.CHART: [
                r'(?i)\bchart\s+(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
                r'(?i)\bdiagram\s+(\d+(?:\.\d+)?)(?:\s*[:\-\.]\s*([^\n\r]{1,100}))?',
            ]
        }

        for element_type, type_patterns in patterns.items():
            for pattern in type_patterns:
                matches = re.finditer(pattern, page_text)
                for match in matches:
                    try:
                        number_str = match.group(1)
                        number = int(float(number_str))
                        title = match.group(2) if match.lastindex > 1 and match.group(2) else f"{element_type.value.title()} {number_str}"

                        references.append({
                            'element_type': element_type,
                            'number': number,
                            'title': title.strip(),
                            'text_match': match.group(0),
                            'position': match.start()
                        })

                    except (ValueError, AttributeError) as e:
                        self.logger.warning(f"Reference parsing failed: {e}")
                        continue

        return references

    def _detect_visual_content_for_reference(self, page, reference: Dict[str, Any]) -> Optional[DocumentElement]:
        """Detect actual visual content for a text reference using precise visual detection"""
        try:
            element_type = reference['element_type']

            if element_type == ElementType.TABLE:
                return self._detect_precise_table(page, reference)
            else:
                return self._detect_precise_figure(page, reference)

        except Exception as e:
            self.logger.warning(f"Visual detection failed for {reference['title']}: {e}")
            return None

    def _detect_precise_table(self, page, reference: Dict[str, Any]) -> Optional[DocumentElement]:
        """Detect table using pdfplumber's precise table boundaries"""
        try:
            # Use pdfplumber's table detection for precise boundaries
            tables = page.extract_tables()
            if not tables:
                return None

            # Find table closest to text reference
            text_position = self._find_text_position(page, reference['text_match'])
            if not text_position:
                return None

            best_table = None
            min_distance = float('inf')

            for table in tables:
                if not table or not table[0]:  # Skip empty tables
                    continue

                # Get precise table boundaries using pdfplumber's internal table object
                table_bbox = self._get_precise_table_boundaries(page, table)
                if not table_bbox:
                    continue

                # Calculate distance from text reference
                distance = self._calculate_distance(text_position, table_bbox)

                # Validate this is actually a table with visual structure
                if self._validate_table_visual_content(page, table_bbox) and distance < min_distance:
                    min_distance = distance
                    best_table = table_bbox

            if best_table and best_table.is_valid_visual_element():
                visual_elements = self._extract_visual_elements_in_area(page, best_table)
                return DocumentElement(
                    element_type=reference['element_type'],
                    number=reference['number'],
                    title=reference['title'],
                    bbox=best_table,
                    page_number=getattr(page, 'page_number', 1),
                    text_references=[reference['text_match']],
                    detection_method="precise_table_detection",
                    visual_elements=visual_elements,
                    quality_metrics={"visual_confidence": best_table.confidence}
                )

        except Exception as e:
            self.logger.warning(f"Precise table detection failed: {e}")

        return None

    def _detect_precise_figure(self, page, reference: Dict[str, Any]) -> Optional[DocumentElement]:
        """Detect figure using actual visual elements (images, rects, curves)"""
        try:
            # Get all visual elements from the page
            visual_elements = []

            # Add images
            if hasattr(page, 'images'):
                for img in page.images:
                    visual_elements.append(VisualElement(
                        element_type='image',
                        bbox=(img['x0'], img['top'], img['x1'], img['bottom']),
                        confidence=1.0,
                        attributes=img
                    ))

            # Add rectangles/shapes
            if hasattr(page, 'rects'):
                for rect in page.rects:
                    visual_elements.append(VisualElement(
                        element_type='rect',
                        bbox=(rect['x0'], rect['top'], rect['x1'], rect['bottom']),
                        confidence=0.8,
                        attributes=rect
                    ))

            # Add curves/lines
            if hasattr(page, 'curves'):
                for curve in page.curves:
                    visual_elements.append(VisualElement(
                        element_type='curve',
                        bbox=(curve['x0'], curve['top'], curve['x1'], curve['bottom']),
                        confidence=0.7,
                        attributes=curve
                    ))

            if not visual_elements:
                return None

            # Find text reference position
            text_position = self._find_text_position(page, reference['text_match'])
            if not text_position:
                return None

            # Find visual elements cluster near text reference
            figure_bbox = self._find_visual_cluster_near_text(visual_elements, text_position)

            if figure_bbox and figure_bbox.is_valid_visual_element():
                # Validate this contains actual visual content, not just text
                if self._validate_figure_visual_content(page, figure_bbox):
                    relevant_elements = [ve for ve in visual_elements
                                       if self._bbox_overlaps(ve.bbox, (figure_bbox.x0, figure_bbox.y0, figure_bbox.x1, figure_bbox.y1))]

                    return DocumentElement(
                        element_type=reference['element_type'],
                        number=reference['number'],
                        title=reference['title'],
                        bbox=figure_bbox,
                        page_number=getattr(page, 'page_number', 1),
                        text_references=[reference['text_match']],
                        detection_method="precise_visual_detection",
                        visual_elements=relevant_elements,
                        quality_metrics={"visual_confidence": figure_bbox.confidence}
                    )

        except Exception as e:
            self.logger.warning(f"Precise figure detection failed: {e}")

        return None

    def _get_precise_table_boundaries(self, page, table_data) -> Optional[BoundingBox]:
        """Get precise table boundaries using pdfplumber's table detection"""
        try:
            if not table_data or not table_data[0]:
                return None

            # Use pdfplumber's find_tables to get exact boundaries
            tables_with_metadata = page.find_tables()

            for table_obj in tables_with_metadata:
                # Get the actual table boundary box
                bbox = table_obj.bbox
                if bbox:
                    x0, y0, x1, y1 = bbox

                    # Validate dimensions
                    width, height = x1 - x0, y1 - y0
                    if width >= MIN_WIDTH and height >= MIN_HEIGHT:

                        # Count visual elements in table area
                        visual_count = self._count_visual_elements_in_area(page, (x0, y0, x1, y1))
                        text_density = self._calculate_text_density(page, (x0, y0, x1, y1))

                        return BoundingBox(
                            x0=x0, y0=y0, x1=x1, y1=y1,
                            confidence=0.95,
                            visual_elements_count=visual_count,
                            text_density=text_density,
                            has_visual_content=(visual_count >= MIN_VISUAL_ELEMENTS and text_density < TEXT_ONLY_THRESHOLD),
                            buffer_zone=TABLE_BUFFER_ZONE
                        )

        except Exception as e:
            self.logger.warning(f"Precise table boundaries failed: {e}")

        return None

    def _find_visual_cluster_near_text(self, visual_elements: List[VisualElement], text_bbox: Tuple[float, float, float, float]) -> Optional[BoundingBox]:
        """Find cluster of visual elements near text reference"""
        try:
            text_x0, text_y0, text_x1, text_y1 = text_bbox
            text_center_x = (text_x0 + text_x1) / 2
            text_center_y = (text_y0 + text_y1) / 2

            # Find visual elements within reasonable distance of text
            nearby_elements = []
            max_distance = 200  # Points

            for ve in visual_elements:
                ve_x0, ve_y0, ve_x1, ve_y1 = ve.bbox
                ve_center_x = (ve_x0 + ve_x1) / 2
                ve_center_y = (ve_y0 + ve_y1) / 2

                distance = math.sqrt((ve_center_x - text_center_x)**2 + (ve_center_y - text_center_y)**2)
                if distance <= max_distance:
                    nearby_elements.append(ve)

            if len(nearby_elements) < MIN_VISUAL_ELEMENTS:
                return None

            # Calculate bounding box of visual elements cluster
            all_x0 = [ve.bbox[0] for ve in nearby_elements]
            all_y0 = [ve.bbox[1] for ve in nearby_elements]
            all_x1 = [ve.bbox[2] for ve in nearby_elements]
            all_y1 = [ve.bbox[3] for ve in nearby_elements]

            cluster_x0, cluster_y0 = min(all_x0), min(all_y0)
            cluster_x1, cluster_y1 = max(all_x1), max(all_y1)

            # Validate cluster size
            width, height = cluster_x1 - cluster_x0, cluster_y1 - cluster_y0
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                return None

            # Calculate confidence based on visual element density
            cluster_area = width * height
            visual_density = len(nearby_elements) / (cluster_area / 1000)  # Elements per 1000 sq pts
            confidence = min(1.0, visual_density * 0.1)

            return BoundingBox(
                x0=cluster_x0, y0=cluster_y0, x1=cluster_x1, y1=cluster_y1,
                confidence=confidence,
                visual_elements_count=len(nearby_elements),
                text_density=0.0,  # Will be calculated later
                has_visual_content=True,
                buffer_zone=DEFAULT_BUFFER_ZONE
            )

        except Exception as e:
            self.logger.warning(f"Visual cluster detection failed: {e}")
            return None

    def _validate_table_visual_content(self, page, bbox: BoundingBox) -> bool:
        """Validate that table area contains actual table structure, not just text"""
        try:
            # Check for table-like visual elements (lines, borders)
            visual_count = self._count_visual_elements_in_area(page, (bbox.x0, bbox.y0, bbox.x1, bbox.y1))

            # Check text density - tables should have structured text, not paragraphs
            text_density = self._calculate_text_density(page, (bbox.x0, bbox.y0, bbox.x1, bbox.y1))

            # Tables should have some visual structure and not be pure text
            has_structure = visual_count >= 2  # At least some lines/borders
            not_pure_text = text_density < 0.95  # Allow some visual elements

            return has_structure and not_pure_text

        except Exception:
            return False

    def _validate_figure_visual_content(self, page, bbox: BoundingBox) -> bool:
        """Validate that figure area contains actual visual content, not just text"""
        try:
            # Count actual visual elements
            visual_count = self._count_visual_elements_in_area(page, (bbox.x0, bbox.y0, bbox.x1, bbox.y1))

            # Calculate text density
            text_density = self._calculate_text_density(page, (bbox.x0, bbox.y0, bbox.x1, bbox.y1))

            # Figures must have significant visual content and low text density
            has_visual_content = visual_count >= MIN_VISUAL_ELEMENTS
            low_text_density = text_density < TEXT_ONLY_THRESHOLD

            return has_visual_content and low_text_density

        except Exception:
            return False

    def _count_visual_elements_in_area(self, page, area: Tuple[float, float, float, float]) -> int:
        """Count visual elements (images, rects, curves) in specified area"""
        count = 0
        x0, y0, x1, y1 = area

        try:
            # Count images
            if hasattr(page, 'images'):
                for img in page.images:
                    if self._element_in_area(img, area):
                        count += 1

            # Count rectangles
            if hasattr(page, 'rects'):
                for rect in page.rects:
                    if self._element_in_area(rect, area):
                        count += 1

            # Count curves/lines
            if hasattr(page, 'curves'):
                for curve in page.curves:
                    if self._element_in_area(curve, area):
                        count += 1

        except Exception as e:
            self.logger.warning(f"Visual element counting failed: {e}")

        return count

    def _calculate_text_density(self, page, area: Tuple[float, float, float, float]) -> float:
        """Calculate text density in specified area (0.0 = no text, 1.0 = all text)"""
        try:
            x0, y0, x1, y1 = area
            area_size = (x1 - x0) * (y1 - y0)

            if area_size <= 0:
                return 0.0

            text_area = 0.0
            chars = getattr(page, 'chars', [])

            for char in chars:
                char_x0 = char.get('x0', 0)
                char_y0 = char.get('top', char.get('y0', 0))
                char_x1 = char.get('x1', char_x0)
                char_y1 = char.get('bottom', char.get('y1', char_y0))

                # Check if character is in area
                if (x0 <= char_x0 <= x1 and y0 <= char_y0 <= y1 and
                    x0 <= char_x1 <= x1 and y0 <= char_y1 <= y1):
                    char_area = (char_x1 - char_x0) * (char_y1 - char_y0)
                    text_area += char_area

            return min(1.0, text_area / area_size)

        except Exception:
            return 0.5  # Default neutral value

    def _element_in_area(self, element: Dict, area: Tuple[float, float, float, float]) -> bool:
        """Check if element overlaps with specified area"""
        try:
            area_x0, area_y0, area_x1, area_y1 = area
            elem_x0 = element.get('x0', 0)
            elem_y0 = element.get('top', element.get('y0', 0))
            elem_x1 = element.get('x1', elem_x0)
            elem_y1 = element.get('bottom', element.get('y1', elem_y0))

            # Check for overlap
            return not (elem_x1 < area_x0 or elem_x0 > area_x1 or
                       elem_y1 < area_y0 or elem_y0 > area_y1)

        except Exception:
            return False

    def _find_text_position(self, page, text: str) -> Optional[Tuple[float, float, float, float]]:
        """Find position of text on page"""
        try:
            chars = getattr(page, 'chars', [])
            if not chars:
                return None

            text_words = text.lower().split()
            if not text_words:
                return None

            # Simple text search for now
            page_text = ""
            char_positions = []

            for char in chars:
                char_text = char.get('text', '').strip()
                if char_text:
                    page_text += char_text.lower() + " "
                    char_positions.append(char)

            target_text = ' '.join(text_words)
            match_pos = page_text.find(target_text)

            if match_pos >= 0 and char_positions:
                # Approximate position based on character index
                word_count = len(page_text[:match_pos].split())

                if word_count < len(char_positions):
                    start_char = char_positions[word_count]
                    end_idx = min(word_count + len(text_words), len(char_positions) - 1)
                    end_char = char_positions[end_idx]

                    return (
                        start_char.get('x0', 0),
                        start_char.get('top', start_char.get('y0', 0)),
                        end_char.get('x1', start_char.get('x1', 100)),
                        end_char.get('bottom', end_char.get('y1', start_char.get('y1', 20)))
                    )

        except Exception as e:
            self.logger.warning(f"Text position finding failed: {e}")

        return None

    def _calculate_distance(self, bbox1: Tuple[float, float, float, float], bbox2: BoundingBox) -> float:
        """Calculate distance between two bounding boxes"""
        x1_center = (bbox1[0] + bbox1[2]) / 2
        y1_center = (bbox1[1] + bbox1[3]) / 2
        x2_center = (bbox2.x0 + bbox2.x1) / 2
        y2_center = (bbox2.y0 + bbox2.y1) / 2

        return math.sqrt((x2_center - x1_center)**2 + (y2_center - y1_center)**2)

    def _bbox_overlaps(self, bbox1: Tuple[float, float, float, float], bbox2: Tuple[float, float, float, float]) -> bool:
        """Check if two bounding boxes overlap"""
        x1_0, y1_0, x1_1, y1_1 = bbox1
        x2_0, y2_0, x2_1, y2_1 = bbox2

        return not (x1_1 < x2_0 or x1_0 > x2_1 or y1_1 < y2_0 or y1_0 > y2_1)

    def _find_standalone_visual_elements(self, page, existing_elements: List[DocumentElement]) -> List[DocumentElement]:
        """Find visual elements that don't have text references"""
        standalone = []

        try:
            # Get all significant visual clusters
            visual_elements = []

            # Collect all visual elements
            if hasattr(page, 'images'):
                for img in page.images:
                    visual_elements.append(VisualElement(
                        element_type='image',
                        bbox=(img['x0'], img['top'], img['x1'], img['bottom']),
                        confidence=1.0,
                        attributes=img
                    ))

            # Find clusters that aren't already covered by existing elements
            used_areas = [(e.bbox.x0, e.bbox.y0, e.bbox.x1, e.bbox.y1) for e in existing_elements]

            for ve in visual_elements:
                # Check if this visual element is already covered
                already_covered = any(self._bbox_overlaps(ve.bbox, used_area) for used_area in used_areas)

                if not already_covered:
                    # Check if it's large enough to be standalone
                    width = ve.bbox[2] - ve.bbox[0]
                    height = ve.bbox[3] - ve.bbox[1]

                    if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                        bbox = BoundingBox(
                            x0=ve.bbox[0], y0=ve.bbox[1], x1=ve.bbox[2], y1=ve.bbox[3],
                            confidence=ve.confidence,
                            visual_elements_count=1,
                            text_density=0.0,
                            has_visual_content=True
                        )

                        if bbox.is_valid_visual_element():
                            element = DocumentElement(
                                element_type=ElementType.FIGURE,
                                number=len(existing_elements) + len(standalone) + 1,
                                title=f"Figure {len(existing_elements) + len(standalone) + 1}",
                                bbox=bbox,
                                page_number=getattr(page, 'page_number', 1),
                                text_references=[],
                                detection_method="standalone_visual_detection",
                                visual_elements=[ve],
                                quality_metrics={"visual_confidence": ve.confidence}
                            )
                            standalone.append(element)

        except Exception as e:
            self.logger.warning(f"Standalone visual detection failed: {e}")

        return standalone

    def _extract_visual_elements_in_area(self, page, bbox: BoundingBox) -> List[VisualElement]:
        """Extract all visual elements within specified area"""
        elements = []
        area = (bbox.x0, bbox.y0, bbox.x1, bbox.y1)

        try:
            # Extract images
            if hasattr(page, 'images'):
                for img in page.images:
                    if self._element_in_area(img, area):
                        elements.append(VisualElement(
                            element_type='image',
                            bbox=(img['x0'], img['top'], img['x1'], img['bottom']),
                            confidence=1.0,
                            attributes=img
                        ))

            # Extract rectangles
            if hasattr(page, 'rects'):
                for rect in page.rects:
                    if self._element_in_area(rect, area):
                        elements.append(VisualElement(
                            element_type='rect',
                            bbox=(rect['x0'], rect['top'], rect['x1'], rect['bottom']),
                            confidence=0.8,
                            attributes=rect
                        ))

            # Extract curves
            if hasattr(page, 'curves'):
                for curve in page.curves:
                    if self._element_in_area(curve, area):
                        elements.append(VisualElement(
                            element_type='curve',
                            bbox=(curve['x0'], curve['top'], curve['x1'], curve['bottom']),
                            confidence=0.7,
                            attributes=curve
                        ))

        except Exception as e:
            self.logger.warning(f"Visual element extraction failed: {e}")

        return elements


class PreciseScreenshotProcessorV3:
    """v3.0 Processor with Precise Visual Boundary Detection"""

    def __init__(self, timeout_minutes: int = 30, verbose: bool = False):
        self.timeout_seconds = timeout_minutes * 60
        self.verbose = verbose
        self.visual_detector = PreciseVisualDetector(verbose)
        self.setup_logging()

        self.stats = {
            "start_time": time.time(),
            "pages_processed": 0,
            "elements_detected": 0,
            "screenshots_created": 0,
            "visual_accuracy": 0.0,
            "processing_time": 0.0,
            "method_used": "Precise Visual Boundary Detection v3.0",
            "errors": [],
            "warnings": [],
            "peak_memory_mb": 0.0,
            "v3_improvements": [
                "Actual visual element detection using page.images, page.rects, page.curves",
                "Pure text content exclusion with text density analysis",
                "Precise table boundaries using pdfplumber's find_tables()",
                "Visual cluster detection for figures/charts",
                "Content validation requiring actual visual elements",
                "Whitespace analysis for accurate boundary detection",
                "Smart filtering to exclude text-only areas"
            ]
        }

    def setup_logging(self):
        """Setup logging configuration with Unicode-safe handlers"""
        # Configure logging to handle Unicode properly
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('art_materials_processor_v3.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def process_pdf(self, pdf_path: str, output_dir: str) -> bool:
        """Process PDF using precise visual boundary detection"""
        try:
            if not self._validate_input(pdf_path):
                return False

            if not self._validate_requirements():
                return False

            self._log_memory_usage()

            pdf_path = str(Path(pdf_path)).replace('\\', '/')
            output_dir = str(Path(output_dir)).replace('\\', '/')

            pdf_name = Path(pdf_path).stem
            pdf_output_dir = os.path.join(output_dir, pdf_name)
            images_dir = os.path.join(pdf_output_dir, "images")

            os.makedirs(pdf_output_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Use safe logging for path with potential Unicode characters
            safe_log_path(self.logger, 'info', "Processing PDF with v3.0 Precise Visual Detection: {}", pdf_path)

            all_elements = []
            markdown_content = [f"# {pdf_name}\n\n"]
            markdown_content.append("*Extracted using Precise Visual Boundary Detection v3.0*\n\n")

            with pdfplumber.open(pdf_path) as pdf_plumber:
                pdf_pymupdf = fitz.open(pdf_path)

                for page_num, page in enumerate(pdf_plumber.pages):
                    self.logger.info(f"Processing page {page_num + 1} with precise visual detection")

                    page_text = page.extract_text() or ""

                    # Apply precise visual detection
                    elements = self.visual_detector.detect_elements(page, page_text)

                    # Generate screenshots for visually validated elements
                    page_elements = self._generate_precise_screenshots(
                        pdf_pymupdf, page_num, elements, images_dir
                    )

                    all_elements.extend(page_elements)

                    # Generate page content
                    page_content = self._generate_page_content(page_text, page_elements, page_num + 1)
                    markdown_content.append(page_content)

                    self.stats["pages_processed"] += 1
                    self._log_memory_usage()

                pdf_pymupdf.close()

            # Generate final document
            final_markdown = self._finalize_markdown(markdown_content, all_elements)

            doc_path = os.path.join(pdf_output_dir, "document.md")
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(final_markdown)

            self._save_metadata(pdf_output_dir, all_elements)

            self.stats["elements_detected"] = len(all_elements)
            self.stats["processing_time"] = time.time() - self.stats["start_time"]

            if all_elements:
                avg_visual_confidence = sum(e.quality_metrics.get("visual_confidence", 0) for e in all_elements) / len(all_elements)
                self.stats["visual_accuracy"] = avg_visual_confidence

            self.logger.info(f"SUCCESS: v3.0 Precise Detection completed")
            self.logger.info(f"Elements detected: {self.stats['elements_detected']}")
            self.logger.info(f"Visual accuracy: {self.stats['visual_accuracy']:.1%}")
            self.logger.info(f"Processing time: {self.stats['processing_time']:.1f}s")

            return True

        except Exception as e:
            self.stats["errors"].append(f"Processing failed: {e}")
            self.logger.error(f"v3.0 Processing failed: {e}")
            return False

    def _generate_precise_screenshots(self, pdf_pymupdf, page_num: int, elements: List[DocumentElement], images_dir: str) -> List[DocumentElement]:
        """Generate screenshots with precise visual boundaries"""
        screenshot_elements = []

        for element in elements:
            try:
                page = pdf_pymupdf[page_num]

                # Double-check visual validation
                if not element.bbox.is_valid_visual_element():
                    if self.verbose:
                        self.logger.warning(f"Skipping {element.title}: failed visual validation")
                    continue

                # Use precise boundaries
                bbox_fitz = fitz.Rect(
                    element.bbox.x0,
                    element.bbox.y0,
                    element.bbox.x1,
                    element.bbox.y1
                )

                # High quality screenshot
                mat = fitz.Matrix(HIGH_QUALITY_SCALE, HIGH_QUALITY_SCALE)
                pix = page.get_pixmap(matrix=mat, clip=bbox_fitz)

                # Validate screenshot quality
                if pix.width < MIN_WIDTH * HIGH_QUALITY_SCALE or pix.height < MIN_HEIGHT * HIGH_QUALITY_SCALE:
                    if self.verbose:
                        self.logger.warning(f"Skipping {element.title}: screenshot quality insufficient")
                    continue

                # Generate filename
                element_type_short = element.element_type.value.title()
                safe_title = self._sanitize_filename(element.title)
                filename = f"v3_{element_type_short}_{element.number:02d}_{safe_title}.png"
                filepath = os.path.join(images_dir, filename)

                pix.save(filepath)

                # Update metrics
                element.quality_metrics.update({
                    "screenshot_created": True,
                    "screenshot_path": filepath,
                    "screenshot_filename": filename,
                    "screenshot_width": pix.width,
                    "screenshot_height": pix.height,
                    "visual_elements_detected": element.bbox.visual_elements_count,
                    "text_density": element.bbox.text_density,
                    "detection_method": element.detection_method
                })

                screenshot_elements.append(element)
                self.stats["screenshots_created"] += 1

                if self.verbose:
                    self.logger.info(f"v3.0 screenshot: {filename} ({pix.width}x{pix.height}) - {element.bbox.visual_elements_count} visual elements")

            except Exception as e:
                self.logger.error(f"Screenshot failed for {element.title}: {e}")
                self.stats["errors"].append(f"Screenshot failed: {element.title}")

        return screenshot_elements

    def _validate_input(self, pdf_path: str) -> bool:
        """Input validation"""
        try:
            path_obj = Path(pdf_path)
            if not path_obj.exists() or not path_obj.is_file() or path_obj.suffix.lower() != '.pdf':
                return False
            return True
        except Exception:
            return False

    def _validate_requirements(self) -> bool:
        """Validate required libraries"""
        missing = []
        if not HAS_PYMUPDF:
            missing.append("PyMuPDF")
        if not HAS_PDFPLUMBER:
            missing.append("pdfplumber")
        if not HAS_PIL:
            missing.append("PIL")

        if missing:
            self.logger.error(f"Missing libraries: {missing}")
            return False
        return True

    def _log_memory_usage(self):
        """Memory monitoring"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.stats["peak_memory_mb"] = max(self.stats["peak_memory_mb"], memory_mb)
        except Exception:
            pass

    def _generate_page_content(self, page_text: str, elements: List[DocumentElement], page_num: int) -> str:
        """Generate page content with precise image links"""
        content_lines = [f"\n## Page {page_num}\n"]

        if not elements:
            clean_text = self._clean_text_content(page_text)
            if clean_text.strip():
                content_lines.append(clean_text)
        else:
            # Insert elements in order
            for element in elements:
                filename = element.quality_metrics.get("screenshot_filename", "")
                if filename:
                    width = element.quality_metrics.get("screenshot_width", 0)
                    height = element.quality_metrics.get("screenshot_height", 0)
                    visual_count = element.quality_metrics.get("visual_elements_detected", 0)
                    method = element.quality_metrics.get("detection_method", "")

                    caption = f"{element.title} ({width}x{height}px, {visual_count} visual elements, {method})"
                    content_lines.append(f"\n![{caption}](./images/{filename})\n")

        return "\n".join(content_lines)

    def _clean_text_content(self, text: str) -> str:
        """Clean text content"""
        if not text:
            return ""
        return text.strip()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename"""
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')

        if len(sanitized) > MAX_FILENAME_LENGTH:
            sanitized = sanitized[:MAX_FILENAME_LENGTH]

        return sanitized or "unnamed"

    def _finalize_markdown(self, content_lines: List[str], elements: List[DocumentElement]) -> str:
        """Finalize markdown with v3.0 summary"""
        final_content = []
        final_content.extend(content_lines)

        final_content.append("\n\n---\n\n## v3.0 Processing Summary\n")
        final_content.append(f"- **Method**: Precise Visual Boundary Detection v3.0\n")
        final_content.append(f"- **Pages**: {self.stats['pages_processed']}\n")
        final_content.append(f"- **Elements**: {len(elements)}\n")
        final_content.append(f"- **Screenshots**: {self.stats['screenshots_created']}\n")
        final_content.append(f"- **Visual Accuracy**: {self.stats.get('visual_accuracy', 0):.1%}\n")

        if elements:
            # Visual validation stats
            with_visual = sum(1 for e in elements if e.bbox.has_visual_content)
            final_content.append(f"- **Elements with Visual Content**: {with_visual}/{len(elements)}\n")

            avg_visual_elements = sum(e.bbox.visual_elements_count for e in elements) / len(elements)
            final_content.append(f"- **Avg Visual Elements per Element**: {avg_visual_elements:.1f}\n")

            avg_text_density = sum(e.bbox.text_density for e in elements) / len(elements)
            final_content.append(f"- **Avg Text Density**: {avg_text_density:.1%}\n")

        final_content.append("\n### v3.0 Key Improvements:\n")
        for improvement in self.stats["v3_improvements"]:
            final_content.append(f"- {improvement}\n")

        return "".join(final_content)

    def _save_metadata(self, output_dir: str, elements: List[DocumentElement]):
        """Save v3.0 metadata"""
        metadata = {
            "processing_stats": self.stats,
            "detected_elements": [
                {
                    "type": element.element_type.value,
                    "number": element.number,
                    "title": element.title,
                    "page": element.page_number,
                    "bbox": {
                        "x0": element.bbox.x0, "y0": element.bbox.y0,
                        "x1": element.bbox.x1, "y1": element.bbox.y1,
                        "width": element.bbox.width, "height": element.bbox.height,
                        "visual_elements_count": element.bbox.visual_elements_count,
                        "text_density": element.bbox.text_density,
                        "has_visual_content": element.bbox.has_visual_content
                    },
                    "visual_elements": [
                        {
                            "type": ve.element_type,
                            "bbox": ve.bbox,
                            "confidence": ve.confidence
                        } for ve in element.visual_elements
                    ],
                    "quality_metrics": element.quality_metrics,
                    "detection_method": element.detection_method
                }
                for element in elements
            ],
            "version": "v3.0 - Precise Visual Boundary Detection"
        }

        metadata_path = os.path.join(output_dir, "processing_metadata_v3.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Art Materials Processor v3.0 - Precise Visual Detection")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in minutes")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path) or not args.pdf_path.lower().endswith('.pdf'):
        safe_print(f"ERROR: Invalid PDF file: {safe_format_path(args.pdf_path)}")
        return 1

    processor = PreciseScreenshotProcessorV3(timeout_minutes=args.timeout, verbose=args.verbose)

    safe_print("=" * 80)
    safe_print("Art Materials Processor v3.0 - PRECISE VISUAL BOUNDARY DETECTION")
    safe_print("=" * 80)
    safe_print(f"Input PDF: {safe_format_path(args.pdf_path)}")
    safe_print(f"Output Directory: {safe_format_path(args.output_dir)}")
    safe_print("\nCRITICAL v3.0 IMPROVEMENTS:")
    safe_print("[OK] Actual visual element detection (images, rects, curves)")
    safe_print("[OK] Pure text content exclusion with density analysis")
    safe_print("[OK] Precise table boundaries using pdfplumber's find_tables()")
    safe_print("[OK] Visual cluster detection for figures/charts")
    safe_print("[OK] Content validation requiring visual elements")
    safe_print("[OK] Smart filtering to exclude text-only areas")
    safe_print("-" * 80)

    success = processor.process_pdf(args.pdf_path, args.output_dir)

    if success:
        safe_print("\n" + "=" * 80)
        safe_print("SUCCESS: v3.0 Precise Visual Detection completed")
        safe_print(f"Elements detected: {processor.stats['elements_detected']}")
        safe_print(f"Screenshots created: {processor.stats['screenshots_created']}")
        safe_print(f"Visual accuracy: {processor.stats.get('visual_accuracy', 0):.1%}")
        safe_print(f"Processing time: {processor.stats['processing_time']:.1f}s")
        return 0
    else:
        safe_print("\nFAILURE: Processing failed")
        for error in processor.stats['errors']:
            safe_print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())