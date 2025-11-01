"""Content extraction utilities for markdown files with page markers."""

import re
from typing import Optional, Tuple


def extract_pages_from_markdown(
    markdown_text: str,
    start_page: int,
    end_page: Optional[int] = None
) -> str:
    """
    Extract content between specified pages from markdown with page markers.

    The markdown must contain page markers in the format:
    --- end of page=N ---

    Args:
        markdown_text: Markdown content with page markers
        start_page: Starting page number (1-indexed)
        end_page: Ending page number (1-indexed, inclusive). If None, extracts to end.

    Returns:
        Extracted markdown content for the specified page range

    Examples:
        # Extract just page 41
        content = extract_pages_from_markdown(md, 41, 41)

        # Extract pages 41-45
        content = extract_pages_from_markdown(md, 41, 45)

        # Extract from page 41 to end
        content = extract_pages_from_markdown(md, 41)
    """
    # Pattern to match page markers: --- end of page=N ---
    pattern = r'--- end of page=(\d+) ---'

    # Find all page markers and their positions
    markers = []
    for match in re.finditer(pattern, markdown_text):
        page_num = int(match.group(1))
        markers.append({
            'page': page_num,
            'start': match.start(),
            'end': match.end()
        })

    # If no markers found, return empty or full text
    if not markers:
        return markdown_text if start_page == 1 else ""

    # Find start position (content after start_page-1's marker)
    start_pos = 0
    for marker in markers:
        if marker['page'] == start_page - 1:
            start_pos = marker['end']
            break

    # Find end position (before end_page's marker or end of text)
    end_pos = len(markdown_text)
    if end_page is not None:
        for marker in markers:
            if marker['page'] == end_page:
                end_pos = marker['start']
                break

    # Extract and clean up the content
    content = markdown_text[start_pos:end_pos].strip()

    return content


def get_page_range_for_toc_entry(
    toc: list,
    entry_index: int
) -> Tuple[int, int]:
    """
    Get the page range for a TOC entry.

    Args:
        toc: List of TOC entries (each with 'level', 'title', 'page')
        entry_index: Index of the TOC entry to get range for

    Returns:
        Tuple of (start_page, end_page) for the TOC entry

    Examples:
        # Get page range for "Goblins" section
        toc = [
            {'level': 2, 'title': 'Goblinoids', 'page': 41},
            {'level': 3, 'title': 'Goblins', 'page': 41},
            {'level': 3, 'title': 'Hobgoblins', 'page': 46},
        ]
        start, end = get_page_range_for_toc_entry(toc, 1)
        # Returns: (41, 45) - from Goblins to just before Hobgoblins
    """
    if entry_index < 0 or entry_index >= len(toc):
        raise ValueError(f"Invalid TOC entry index: {entry_index}")

    entry = toc[entry_index]
    start_page = entry['page']
    entry_level = entry['level']

    # Find the end page by looking for the next entry at same or higher level
    end_page = None
    for i in range(entry_index + 1, len(toc)):
        next_entry = toc[i]
        # If we find an entry at same or higher level (lower number), that's our end
        if next_entry['level'] <= entry_level:
            end_page = next_entry['page'] - 1
            break

    # If no next section found, use None (extract to end)
    return (start_page, end_page)


def extract_toc_section(
    markdown_text: str,
    toc: list,
    entry_index: int
) -> str:
    """
    Extract content for a specific TOC entry.

    Convenience function that combines get_page_range_for_toc_entry
    and extract_pages_from_markdown.

    Args:
        markdown_text: Markdown content with page markers
        toc: List of TOC entries
        entry_index: Index of the TOC entry to extract

    Returns:
        Markdown content for the TOC section

    Examples:
        # Extract "Goblins" section
        content = extract_toc_section(md_text, toc, 1)
    """
    start_page, end_page = get_page_range_for_toc_entry(toc, entry_index)
    return extract_pages_from_markdown(markdown_text, start_page, end_page)


def find_toc_entry_by_title(
    toc: list,
    search_term: str,
    case_sensitive: bool = False
) -> Optional[int]:
    """
    Find a TOC entry index by searching for a title.

    Args:
        toc: List of TOC entries
        search_term: Text to search for in TOC titles
        case_sensitive: Whether search should be case sensitive

    Returns:
        Index of first matching TOC entry, or None if not found

    Examples:
        # Find "Goblins" section
        index = find_toc_entry_by_title(toc, "Goblins")
        if index is not None:
            content = extract_toc_section(md_text, toc, index)
    """
    if not case_sensitive:
        search_term = search_term.lower()

    for i, entry in enumerate(toc):
        title = entry['title']
        if not case_sensitive:
            title = title.lower()

        if search_term in title:
            return i

    return None
