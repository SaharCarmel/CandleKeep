"""PDF parsing and metadata extraction."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

import fitz  # PyMuPDF
import pymupdf4llm

from ..utils.file_utils import parse_filename_metadata


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

    def convert_to_markdown(self) -> str:
        """
        Convert PDF to markdown using pymupdf4llm with page separators.

        Returns:
            Markdown content as string with page markers (--- end of page=N ---)
        """
        try:
            # Use pymupdf4llm for conversion with page separators
            md_text = pymupdf4llm.to_markdown(
                str(self.pdf_path),
                page_separators=True  # Add page markers for content extraction
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
