"""File handling utilities for CandleKeep."""

import re
from pathlib import Path
from typing import Optional, Tuple


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize a filename for safe filesystem storage.

    Args:
        filename: Original filename
        max_length: Maximum length for filename (default: 200)

    Returns:
        Sanitized filename safe for all filesystems
    """
    # Remove file extension
    name = Path(filename).stem

    # Replace problematic characters with hyphens
    name = re.sub(r'[<>:"/\\|?*]', '-', name)

    # Replace multiple spaces/hyphens with single hyphen
    name = re.sub(r'[-\s]+', '-', name)

    # Remove leading/trailing hyphens and spaces
    name = name.strip('- ')

    # Truncate if too long
    if len(name) > max_length:
        name = name[:max_length].rstrip('- ')

    # Ensure not empty
    if not name:
        name = "untitled"

    return name.lower()


def parse_filename_metadata(filename: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract title and author from filename patterns.

    Common patterns:
    - "Title - Author.pdf"
    - "Title by Author.pdf"
    - "Author - Title.pdf"
    - "Title (Author).pdf"

    Args:
        filename: Filename to parse

    Returns:
        Tuple of (title, author) - either may be None
    """
    # Remove extension
    name = Path(filename).stem

    title = None
    author = None

    # Pattern 1: "Title - Author" or "Author - Title"
    if ' - ' in name:
        parts = name.split(' - ', 1)
        # Heuristic: if first part has common author patterns, it's author first
        if any(indicator in parts[0].lower() for indicator in ['dr.', 'prof.', 'jr.', 'sr.']):
            author = parts[0].strip()
            title = parts[1].strip()
        else:
            title = parts[0].strip()
            author = parts[1].strip()

    # Pattern 2: "Title by Author"
    elif ' by ' in name.lower():
        parts = re.split(r'\s+by\s+', name, maxsplit=1, flags=re.IGNORECASE)
        title = parts[0].strip()
        author = parts[1].strip() if len(parts) > 1 else None

    # Pattern 3: "Title (Author)"
    elif match := re.match(r'^(.+?)\s*\(([^)]+)\)\s*$', name):
        title = match.group(1).strip()
        author = match.group(2).strip()

    # Pattern 4: Just use filename as title
    else:
        title = name.strip()

    return (title if title else None, author if author else None)


def ensure_directory(directory: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        directory: Path to directory
    """
    directory.mkdir(parents=True, exist_ok=True)


def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """
    Generate a unique filename by appending numbers if file exists.

    Args:
        directory: Target directory
        base_name: Base filename without extension
        extension: File extension (with or without dot)

    Returns:
        Path to unique filename
    """
    # Ensure extension starts with dot
    if not extension.startswith('.'):
        extension = f'.{extension}'

    filepath = directory / f"{base_name}{extension}"

    if not filepath.exists():
        return filepath

    # File exists, add counter
    counter = 1
    while True:
        filepath = directory / f"{base_name}-{counter}{extension}"
        if not filepath.exists():
            return filepath
        counter += 1
