"""PDF parsing and metadata extraction."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

import fitz  # PyMuPDF
import pymupdf4llm

from ..utils.file_utils import parse_filename_metadata
from ..utils.image_utils import get_absolute_image_path


class PDFParser:
    """Parser for extracting metadata and content from PDF files."""

    def __init__(self, pdf_path: Path):
        """
        Initialize PDF parser.

        Args:
            pdf_path: Path to PDF file

        Raises:
            FileNotFoundError: If PDF doesn't exist
            ValueError: If file is not a valid PDF
        """
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        try:
            self.doc = fitz.open(str(self.pdf_path))
        except Exception as e:
            raise ValueError(f"Invalid PDF file: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close document."""
        self.doc.close()

    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extract all metadata from PDF.

        Returns:
            Dictionary containing all extracted metadata
        """
        metadata = {}

        # Extract embedded PDF metadata
        embedded = self._extract_embedded_metadata()
        metadata.update(embedded)

        # Extract table of contents
        toc = self._extract_table_of_contents()
        metadata['chapter_count'] = len(toc)
        metadata['table_of_contents'] = toc

        # Page count
        metadata['page_count'] = len(self.doc)

        # If title or author missing, try filename parsing
        if not metadata.get('title') or not metadata.get('author'):
            filename_title, filename_author = parse_filename_metadata(self.pdf_path.name)
            if not metadata.get('title') and filename_title:
                metadata['title'] = filename_title
            if not metadata.get('author') and filename_author:
                metadata['author'] = filename_author

        # If still no title, use filename
        if not metadata.get('title'):
            metadata['title'] = self.pdf_path.stem

        return metadata

    def _extract_embedded_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata embedded in PDF.

        Returns:
            Dictionary of embedded metadata
        """
        pdf_metadata = self.doc.metadata
        metadata = {}

        # Title
        if title := pdf_metadata.get('title', '').strip():
            metadata['title'] = title

        # Author
        if author := pdf_metadata.get('author', '').strip():
            metadata['author'] = author

        # Subject
        if subject := pdf_metadata.get('subject', '').strip():
            metadata['subject'] = subject

        # Keywords
        if keywords := pdf_metadata.get('keywords', '').strip():
            metadata['keywords'] = keywords

        # Creator (software that created the PDF)
        if creator := pdf_metadata.get('creator', '').strip():
            metadata['pdf_creator'] = creator

        # Producer (software that produced the PDF)
        if producer := pdf_metadata.get('producer', '').strip():
            metadata['pdf_producer'] = producer

        # Creation date
        if creationDate := pdf_metadata.get('creationDate', '').strip():
            metadata['pdf_creation_date'] = self._parse_pdf_date(creationDate)

        # Modification date
        if modDate := pdf_metadata.get('modDate', '').strip():
            metadata['pdf_mod_date'] = self._parse_pdf_date(modDate)

        return metadata

    def _parse_pdf_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse PDF date format to datetime.

        PDF dates are in format: D:YYYYMMDDHHmmSSOHH'mm
        Example: D:20230101120000+00'00

        Args:
            date_str: PDF date string

        Returns:
            datetime object or None if parsing fails
        """
        if not date_str:
            return None

        try:
            # Remove D: prefix if present
            if date_str.startswith('D:'):
                date_str = date_str[2:]

            # Extract just the date/time part (ignore timezone for simplicity)
            date_part = date_str[:14]  # YYYYMMDDHHmmSS

            # Parse to datetime
            return datetime.strptime(date_part, '%Y%m%d%H%M%S')
        except (ValueError, IndexError):
            return None

    def _extract_table_of_contents(self) -> List[Dict[str, Any]]:
        """
        Extract table of contents from PDF.

        Returns:
            List of TOC entries with level, title, and page
        """
        toc = self.doc.get_toc()
        toc_entries = []

        for entry in toc:
            level, title, page = entry
            toc_entries.append({
                'level': level,
                'title': title.strip(),
                'page': page
            })

        return toc_entries

    def convert_to_markdown(
        self,
        extract_images: bool = False,
        image_path: Optional[Path] = None,
        dpi: int = 150,
        size_limit: float = 0.05
    ) -> str:
        """
        Convert PDF to markdown using pymupdf4llm with page separators.

        Args:
            extract_images: Whether to extract and save images (default: False)
            image_path: Directory to save extracted images (required if extract_images=True)
            dpi: Image resolution in DPI (default: 150)
            size_limit: Minimum image size as fraction of page area (default: 0.05 = 5%)

        Returns:
            Markdown content as string with page markers (--- end of page=N ---)

        Raises:
            ValueError: If extract_images=True but image_path is None
        """
        if extract_images and image_path is None:
            raise ValueError("image_path required when extract_images=True")

        try:
            # Prepare arguments for pymupdf4llm
            conversion_args = {
                "page_separators": True,  # Add page markers for content extraction
            }

            # Add image extraction parameters if requested
            if extract_images:
                conversion_args.update({
                    "write_images": True,
                    "image_path": str(image_path),
                    "dpi": dpi,
                    "image_size_limit": size_limit,
                })

            # Use pymupdf4llm for conversion
            md_text = pymupdf4llm.to_markdown(
                str(self.pdf_path),
                **conversion_args
            )
            return md_text
        except Exception as e:
            raise ValueError(f"Failed to convert PDF to markdown: {e}")

    def count_words(self, text: str) -> int:
        """
        Count words in text.

        Args:
            text: Text to count words in

        Returns:
            Word count
        """
        # Remove markdown syntax for more accurate count
        clean_text = re.sub(r'[#*`\[\]()]', ' ', text)
        words = clean_text.split()
        return len(words)

    def extract_first_page_text(self) -> str:
        """
        Extract text from first page (for fallback metadata extraction).

        Returns:
            First page text
        """
        if len(self.doc) == 0:
            return ""

        first_page = self.doc[0]
        return first_page.get_text()

    @staticmethod
    def convert_image_paths_to_absolute(
        markdown_content: str,
        book_id: int,
        image_dir: Path
    ) -> str:
        """
        Convert relative image paths in markdown to absolute paths.

        Args:
            markdown_content: Markdown text with relative image paths
            book_id: Book ID for generating absolute paths
            image_dir: Directory where images are stored

        Returns:
            Markdown with absolute image paths

        Example:
            Input:  ![](page-1-img-0.png)
            Output: ![](/Users/user/.candlekeep/images/1/page-1-img-0.png)
        """
        # Pattern to match markdown images: ![...](...) or ![](...)
        # Captures the filename in group 1
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        def replace_path(match):
            alt_text = match.group(1)
            relative_path = match.group(2)

            # Extract just the filename (in case there's a path)
            filename = Path(relative_path).name

            # Generate absolute path
            abs_path = get_absolute_image_path(book_id, filename)

            # Return markdown with absolute path
            return f'![{alt_text}]({abs_path})'

        return re.sub(pattern, replace_path, markdown_content)

    @staticmethod
    def detect_printed_page_number(page) -> Optional[int]:
        """
        Attempt to extract the printed page number from a PDF page.

        This method looks for standalone numbers in the header or footer
        of the page, which typically indicate the printed page number.

        Args:
            page: PyMuPDF page object

        Returns:
            Printed page number as integer, or None if not detectable

        Strategy:
            1. Check last 5 lines (footer) - most common location
            2. Check first 5 lines (header)
            3. Ignore obviously wrong numbers (> 9999, < 1)
        """
        text = page.get_text()
        lines = [line.strip() for line in text.split('\n')]

        # Strategy 1: Check footer (last 5 lines)
        for line in lines[-5:]:
            if line.isdigit() and 1 <= len(line) <= 4:
                num = int(line)
                if 1 <= num <= 9999:  # Sanity check
                    return num

        # Strategy 2: Check header (first 5 lines)
        for line in lines[:5]:
            if line.isdigit() and 1 <= len(line) <= 4:
                num = int(line)
                if 1 <= num <= 9999:
                    return num

        return None  # Could not detect

    def extract_image_metadata(self) -> List[Dict[str, Any]]:
        """
        Extract detailed metadata for all images in the PDF.

        Returns:
            List of dictionaries containing image metadata:
            - page_number: Page where image appears
            - xref: PDF object reference
            - width: Image width in pixels
            - height: Image height in pixels
            - format: Image format (png, jpg, etc.)
            - colorspace: Color space (RGB, CMYK, Gray, etc.)
            - has_transparency: Whether image has transparency/alpha channel
            - file_size: Estimated file size in bytes
        """
        images_metadata = []

        # Iterate through all pages
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            image_list = page.get_images()

            # Detect printed page number for this page (once per page)
            printed_page_num = self.detect_printed_page_number(page)

            # Process each image on the page
            for img_index, img_info in enumerate(image_list):
                try:
                    # img_info is a tuple: (xref, smask, width, height, bpc, colorspace, ...)
                    xref = img_info[0]
                    smask = img_info[1]  # Soft mask (transparency)
                    width = img_info[2]
                    height = img_info[3]
                    colorspace_int = img_info[5]

                    # Extract the image to get more details
                    base_image = self.doc.extract_image(xref)

                    if base_image:
                        # Map colorspace integer to string
                        colorspace_map = {
                            1: "Gray",
                            2: "Gray",  # GrayA (with alpha)
                            3: "RGB",
                            4: "RGBA",
                            5: "CMYK",
                            6: "CMYKA",
                        }
                        colorspace = colorspace_map.get(colorspace_int, f"Unknown({colorspace_int})")

                        # Get image format
                        image_format = base_image.get("ext", "png")

                        # Check for transparency
                        has_transparency = smask > 0 or colorspace in ["RGBA", "CMYKA", "GrayA"]

                        # Estimate file size (actual size of extracted image data)
                        file_size = len(base_image.get("image", b""))

                        images_metadata.append({
                            "page_number": page_num + 1,  # Convert to 1-based page numbering
                            "printed_page_number": printed_page_num,  # Detected printed number (may be None)
                            "xref": xref,
                            "width": width,
                            "height": height,
                            "format": image_format,
                            "colorspace": colorspace,
                            "has_transparency": has_transparency,
                            "file_size": file_size,
                        })

                except Exception as e:
                    # Log error but continue processing other images
                    print(f"Warning: Failed to extract metadata for image {img_index} on page {page_num + 1}: {e}")
                    continue

        return images_metadata


def parse_pdf(
    pdf_path: Path,
    convert_to_md: bool = True
) -> Dict[str, Any]:
    """
    Parse PDF and extract all metadata and content.

    Args:
        pdf_path: Path to PDF file
        convert_to_md: Whether to convert to markdown (default: True)

    Returns:
        Dictionary containing:
        - All metadata fields
        - markdown_content (if convert_to_md=True)
        - word_count (if convert_to_md=True)

    Raises:
        FileNotFoundError: If PDF doesn't exist
        ValueError: If PDF is invalid or conversion fails
    """
    with PDFParser(pdf_path) as parser:
        # Extract metadata
        metadata = parser.extract_metadata()

        # Convert to markdown if requested
        if convert_to_md:
            markdown_content = parser.convert_to_markdown()
            metadata['markdown_content'] = markdown_content
            metadata['word_count'] = parser.count_words(markdown_content)

        return metadata
