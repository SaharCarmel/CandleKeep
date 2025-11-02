"""Markdown parsing and metadata extraction."""

import re
from pathlib import Path
from typing import Dict, Optional, Any, List

import frontmatter

from ..utils.file_utils import parse_filename_metadata


class MarkdownParser:
    """Parser for extracting metadata and content from markdown files."""

    def __init__(self, md_path: Path):
        """
        Initialize Markdown parser.

        Args:
            md_path: Path to markdown file

        Raises:
            FileNotFoundError: If markdown file doesn't exist
            ValueError: If file cannot be read
        """
        self.md_path = Path(md_path)

        if not self.md_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {self.md_path}")

        try:
            with open(self.md_path, 'r', encoding='utf-8') as f:
                self.post = frontmatter.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read markdown file: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass

    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extract all metadata from markdown file.

        Priority order for metadata:
        1. YAML frontmatter
        2. First heading (for title)
        3. Filename parsing
        4. Defaults

        Returns:
            Dictionary containing all extracted metadata
        """
        metadata = {}

        # Extract frontmatter metadata
        frontmatter_data = self._extract_frontmatter_metadata()
        metadata.update(frontmatter_data)

        # Get content (without frontmatter)
        content = self.post.content

        # If title missing, try first heading
        if not metadata.get('title'):
            first_heading = self._extract_first_heading(content)
            if first_heading:
                metadata['title'] = first_heading

        # If title or author still missing, try filename parsing
        if not metadata.get('title') or not metadata.get('author'):
            filename_title, filename_author = parse_filename_metadata(self.md_path.name)
            if not metadata.get('title') and filename_title:
                metadata['title'] = filename_title
            if not metadata.get('author') and filename_author:
                metadata['author'] = filename_author

        # If still no title, use filename
        if not metadata.get('title'):
            metadata['title'] = self.md_path.stem

        # Extract or generate table of contents
        toc = self._extract_or_generate_toc(content)
        metadata['table_of_contents'] = toc
        metadata['chapter_count'] = len(toc)

        # Count words and headings
        metadata['word_count'] = self.count_words(content)

        # Store full content
        metadata['content'] = content

        return metadata

    def _extract_frontmatter_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from YAML frontmatter.

        Returns:
            Dictionary of frontmatter metadata
        """
        metadata = {}

        # Title
        if title := self.post.get('title', '').strip() if isinstance(self.post.get('title'), str) else '':
            metadata['title'] = title

        # Author
        if author := self.post.get('author', '').strip() if isinstance(self.post.get('author'), str) else '':
            metadata['author'] = author

        # Subject
        if subject := self.post.get('subject', '').strip() if isinstance(self.post.get('subject'), str) else '':
            metadata['subject'] = subject

        # Keywords
        if keywords := self.post.get('keywords', '').strip() if isinstance(self.post.get('keywords'), str) else '':
            metadata['keywords'] = keywords

        # Category
        if category := self.post.get('category', '').strip() if isinstance(self.post.get('category'), str) else '':
            metadata['category'] = category

        # Tags (can be list or comma-separated string)
        tags = self.post.get('tags', [])
        if tags:
            if isinstance(tags, list):
                # Convert list to comma-separated string
                metadata['tags'] = tags
            elif isinstance(tags, str):
                # Parse comma-separated string
                metadata['tags'] = [tag.strip() for tag in tags.split(',')]

        # ISBN
        if isbn := self.post.get('isbn', '').strip() if isinstance(self.post.get('isbn'), str) else '':
            metadata['isbn'] = isbn

        # Publisher
        if publisher := self.post.get('publisher', '').strip() if isinstance(self.post.get('publisher'), str) else '':
            metadata['publisher'] = publisher

        # Publication year
        if year := self.post.get('publication_year'):
            try:
                metadata['publication_year'] = int(year)
            except (ValueError, TypeError):
                pass

        # Language
        if language := self.post.get('language', '').strip() if isinstance(self.post.get('language'), str) else '':
            metadata['language'] = language

        # Table of contents from frontmatter (if exists)
        if toc := self.post.get('toc') or self.post.get('table_of_contents'):
            if isinstance(toc, list):
                metadata['frontmatter_toc'] = toc

        return metadata

    def _extract_first_heading(self, content: str) -> Optional[str]:
        """
        Extract title from first # heading in content.

        Args:
            content: Markdown content

        Returns:
            First heading text or None
        """
        # Match first level-1 heading (# Title)
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def _extract_or_generate_toc(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract TOC from frontmatter or generate from headings.

        Strategy:
        1. Check frontmatter for 'toc' or 'table_of_contents' field
        2. If found and valid, use it
        3. Otherwise, generate from markdown headings

        Args:
            content: Markdown content

        Returns:
            List of TOC entries with level, title, and page (0 for markdown)
        """
        # Check if frontmatter has TOC
        frontmatter_toc = self.post.get('toc') or self.post.get('table_of_contents')

        if frontmatter_toc and isinstance(frontmatter_toc, list):
            # Validate and normalize frontmatter TOC
            return self._normalize_frontmatter_toc(frontmatter_toc)

        # Generate TOC from headings
        return self._generate_toc_from_headings(content)

    def _normalize_frontmatter_toc(self, toc_data: List) -> List[Dict[str, Any]]:
        """
        Normalize frontmatter TOC to standard format.

        Args:
            toc_data: TOC from frontmatter

        Returns:
            Normalized TOC entries
        """
        normalized = []

        for entry in toc_data:
            if isinstance(entry, dict):
                normalized.append({
                    'level': entry.get('level', 1),
                    'title': entry.get('title', '').strip(),
                    'page': entry.get('page', 0)  # Markdown doesn't have pages
                })
            elif isinstance(entry, str):
                # Simple string entry, assume level 1
                normalized.append({
                    'level': 1,
                    'title': entry.strip(),
                    'page': 0
                })

        return normalized

    def _generate_toc_from_headings(self, content: str) -> List[Dict[str, Any]]:
        """
        Generate TOC from markdown headings.

        Extracts all headings (##, ###, etc.) and creates TOC structure
        matching the PDF parser format (level, title, page).

        Args:
            content: Markdown content

        Returns:
            List of TOC entries
        """
        toc_entries = []

        # Pattern to match headings: ##, ###, ####, etc. (not # as that's the title)
        # Captures: heading level (number of #) and heading text
        heading_pattern = re.compile(r'^(#{2,6})\s+(.+)$', re.MULTILINE)

        for match in heading_pattern.finditer(content):
            hashes = match.group(1)
            title = match.group(2).strip()

            # Remove markdown links, bold, italic from title
            title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)  # [text](url) -> text
            title = re.sub(r'\*\*([^\*]+)\*\*', r'\1', title)  # **bold** -> bold
            title = re.sub(r'\*([^\*]+)\*', r'\1', title)  # *italic* -> italic
            title = re.sub(r'`([^`]+)`', r'\1', title)  # `code` -> code

            toc_entries.append({
                'level': len(hashes),  # ## = 2, ### = 3, etc.
                'title': title,
                'page': 0  # Markdown files don't have page numbers
            })

        return toc_entries

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
        # Remove links
        clean_text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', clean_text)
        clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
        # Remove horizontal rules
        clean_text = re.sub(r'^---+$', '', clean_text, flags=re.MULTILINE)
        # Split and count
        words = clean_text.split()
        return len(words)

    def count_headings(self, text: str) -> int:
        """
        Count level-2 headings (##) in markdown.

        Args:
            text: Markdown text

        Returns:
            Number of ## headings
        """
        headings = re.findall(r'^##\s+.+$', text, re.MULTILINE)
        return len(headings)


def parse_markdown(md_path: Path) -> Dict[str, Any]:
    """
    Parse markdown file and extract all metadata and content.

    Args:
        md_path: Path to markdown file

    Returns:
        Dictionary containing:
        - All metadata fields (title, author, etc.)
        - content: Full markdown content (without frontmatter)
        - word_count: Number of words
        - chapter_count: Number of TOC entries
        - table_of_contents: List of TOC entries

    Raises:
        FileNotFoundError: If markdown file doesn't exist
        ValueError: If file cannot be read or parsed

    Example:
        >>> metadata = parse_markdown(Path('my-book.md'))
        >>> print(metadata['title'])
        'My Coding Philosophy'
        >>> print(f"Chapters: {metadata['chapter_count']}")
        Chapters: 5
    """
    with MarkdownParser(md_path) as parser:
        return parser.extract_metadata()
