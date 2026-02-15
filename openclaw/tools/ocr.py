"""OCR and image processing utilities"""

import logging
from typing import Optional

import cv2
import numpy as np
import pytesseract
from PIL import Image


logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR and image processing for text extraction"""

    def __init__(self, tesseract_path: Optional[str] = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    async def extract_text_from_image(
        self, image_path: str, preprocess: bool = True
    ) -> Optional[str]:
        """
        Extract text from an image file.

        Args:
            image_path: Path to image file
            preprocess: Whether to preprocess image for better OCR

        Returns:
            Extracted text
        """
        try:
            if preprocess:
                # Load and preprocess image
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

                # Extract text
                text = pytesseract.image_to_string(gray)
            else:
                # Direct OCR
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image)

            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return None

    async def extract_structured_data(
        self, image_path: str, data_type: str = "receipt"
    ) -> Optional[dict]:
        """
        Extract structured data from an image.

        Args:
            image_path: Path to image file
            data_type: Type of data (receipt, invoice, business_card)

        Returns:
            Structured data dictionary
        """
        text = await self.extract_text_from_image(image_path)
        if not text:
            return None

        # This is a simple implementation
        # For production, you'd use Claude's vision API or specialized OCR models
        return {
            "raw_text": text,
            "type": data_type,
            "extracted": True,
        }

    async def detect_tables(self, image_path: str) -> list:
        """
        Detect and extract tables from an image.

        Args:
            image_path: Path to image file

        Returns:
            List of detected tables
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect horizontal and vertical lines
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

            horizontal_lines = cv2.morphologyEx(
                gray, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
            )
            vertical_lines = cv2.morphologyEx(
                gray, cv2.MORPH_OPEN, vertical_kernel, iterations=2
            )

            # Combine lines
            table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)

            # Find contours (table cells)
            contours, _ = cv2.findContours(
                table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            tables = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 50 and h > 50:  # Filter small contours
                    tables.append({"x": x, "y": y, "width": w, "height": h})

            return tables

        except Exception as e:
            logger.error(f"Error detecting tables: {e}")
            return []
