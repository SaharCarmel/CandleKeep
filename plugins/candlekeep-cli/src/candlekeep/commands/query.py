"""Commands for querying books in the library."""

import re
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console

from ..db.models import Book, BookImage
from ..db.session import get_db_manager
from ..utils.config import get_config

console = Console()
app = typer.Typer()


def _format_book_for_llm(book: Book, full: bool = False, fields: Optional[List[str]] = None) -> str:
    """
    Format a book's metadata in LLM-optimized text format.

    Uses structured markdown with key-value pairs for easy parsing.
    """
    lines = []
    lines.append(f"## Book ID: {book.id}")
    lines.append(f"Title: {book.title}")

    # Essential fields (always shown)
    if book.author:
        lines.append(f"Author: {book.author}")
    lines.append(f"Type: {book.source_type.value}")

    if book.page_count:
        lines.append(f"Pages: {book.page_count}")

    if book.added_date:
        lines.append(f"Added: {book.added_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # Additional fields based on flags
    if full or (fields and 'category' in fields):
        if book.category:
            lines.append(f"Category: {book.category}")

    if full or (fields and 'tags' in fields):
        if book.tags:
            lines.append(f"Tags: {', '.join(book.tags)}")

    if full or (fields and 'word_count' in fields):
        if book.word_count:
            lines.append(f"Word Count: {book.word_count:,}")

    if full or (fields and 'chapter_count' in fields):
        if book.chapter_count:
            lines.append(f"Chapters: {book.chapter_count}")

    if full:
        # Show all metadata
        if book.subject:
            lines.append(f"Subject: {book.subject}")
        if book.keywords:
            lines.append(f"Keywords: {book.keywords}")
        if book.isbn:
            lines.append(f"ISBN: {book.isbn}")
        if book.publisher:
            lines.append(f"Publisher: {book.publisher}")
        if book.publication_year:
            lines.append(f"Publication Year: {book.publication_year}")
        if book.language:
            lines.append(f"Language: {book.language}")
        if book.pdf_creator:
            lines.append(f"PDF Creator: {book.pdf_creator}")
        if book.pdf_producer:
            lines.append(f"PDF Producer: {book.pdf_producer}")
        if book.pdf_creation_date:
            lines.append(f"PDF Created: {book.pdf_creation_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if book.pdf_mod_date:
            lines.append(f"PDF Modified: {book.pdf_mod_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Original Path: {book.original_file_path}")
        lines.append(f"Markdown Path: {book.markdown_file_path}")

    return "\n".join(lines)


def _format_toc_for_llm(book: Book) -> str:
    """
    Format a book's table of contents in LLM-optimized text format.

    Uses hierarchical indentation for nested structure.
    """
    lines = []
    lines.append(f"## Table of Contents - Book ID: {book.id}")
    lines.append(f"Title: {book.title}")
    lines.append("")

    if not book.table_of_contents:
        lines.append("No table of contents available for this book.")
        return "\n".join(lines)

    # Format TOC entries with hierarchical indentation
    for entry in book.table_of_contents:
        level = entry.get('level', 1)
        title = entry.get('title', 'Untitled')
        page = entry.get('page', 'N/A')

        # Indent based on level (2 spaces per level)
        indent = "  " * (level - 1)
        lines.append(f"{indent}{title} (Page {page})")

    return "\n".join(lines)


def _parse_page_ranges(page_str: str) -> List[int]:
    """
    Parse page range string into list of page numbers.

    Supports formats like:
    - "1,2,3" -> [1, 2, 3]
    - "1-5" -> [1, 2, 3, 4, 5]
    - "1-5,10-15" -> [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15]
    """
    pages = set()

    for part in page_str.split(','):
        part = part.strip()
        if '-' in part:
            # Range
            start, end = part.split('-', 1)
            try:
                start_num = int(start.strip())
                end_num = int(end.strip())
                pages.update(range(start_num, end_num + 1))
            except ValueError:
                raise ValueError(f"Invalid page range: {part}")
        else:
            # Single page
            try:
                pages.add(int(part))
            except ValueError:
                raise ValueError(f"Invalid page number: {part}")

    return sorted(pages)


def _resolve_printed_to_physical_pages(book_id: int, page_list: List[int], session) -> List[int]:
    """
    Attempt to resolve printed page numbers to physical PDF page numbers.

    Strategy:
    1. Query BookImage table for pages with matching printed_page_number
    2. If found, map to physical page_number
    3. If not found, assume page_list contains physical page numbers (fallback)

    Args:
        book_id: Book ID to query
        page_list: List of page numbers (potentially printed page numbers)
        session: Database session

    Returns:
        List of physical page numbers (PDF indices)
    """
    # Query for all BookImage records for this book with printed page numbers
    images_with_printed = session.query(BookImage).filter(
        BookImage.book_id == book_id,
        BookImage.printed_page_number.isnot(None)
    ).all()

    if not images_with_printed:
        # No printed page data available, treat as physical pages
        return page_list

    # Build mapping: printed_page_number -> physical page_number
    printed_to_physical = {}
    for img in images_with_printed:
        if img.printed_page_number not in printed_to_physical:
            printed_to_physical[img.printed_page_number] = img.page_number

    # Try to resolve each requested page
    resolved_pages = []
    for page_num in page_list:
        if page_num in printed_to_physical:
            # Found mapping: this is a printed page number
            resolved_pages.append(printed_to_physical[page_num])
        else:
            # No mapping: assume it's already a physical page number
            resolved_pages.append(page_num)

    return sorted(set(resolved_pages))  # Remove duplicates and sort


def _extract_pages_from_markdown(md_path: Path, pages: List[int]) -> str:
    """
    Extract specific pages from a markdown file.

    Uses page markers inserted during PDF/markdown processing.
    Returns markdown content for requested pages.

    Note: pymupdf4llm uses 0-based PDF indices in page markers (e.g., "end of page=103"),
    but our database uses 1-based page numbers (e.g., page_number=104).
    We must convert: marker_index = page_number - 1
    """
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all page markers
    # Pattern: --- end of page=N ---
    page_pattern = re.compile(r'--- end of page=(\d+) ---')
    matches = list(page_pattern.finditer(content))

    if not matches:
        # No page markers found - return entire content if page 1 is requested
        if 1 in pages:
            return content
        else:
            return ""

    # Build a map of page numbers to content positions
    # Note: pymupdf4llm markers use 0-based PDF indices
    # "end of page=103" means PDF index 103 (our DB page 104) content ends here
    page_map = {}
    for i, match in enumerate(matches):
        pdf_index = int(match.group(1))  # 0-based PDF index from marker
        db_page_num = pdf_index + 1  # Convert to 1-based page number for our DB

        # Start position is after previous marker (or start of file for page 0)
        if i == 0:
            start_pos = 0
        else:
            start_pos = matches[i - 1].end()

        # End position is at the current marker (before "--- end of page=N ---")
        end_pos = match.start()

        page_map[db_page_num] = (start_pos, end_pos)

    # Extract requested pages
    result_lines = []
    for page_num in pages:
        if page_num in page_map:
            start, end = page_map[page_num]
            page_content = content[start:end].strip()
            result_lines.append(f"### Page {page_num}")
            result_lines.append(page_content)
            result_lines.append("")  # Blank line separator

    return "\n".join(result_lines)


@app.command("list")
def list_books(
    full: bool = typer.Option(False, "--full", help="Show all metadata fields"),
    fields: Optional[str] = typer.Option(None, "--fields", help="Comma-separated list of specific fields to show"),
):
    """
    List all books in the library with metadata.

    Output is optimized for LLM consumption with structured markdown format.
    """
    try:
        config = get_config()

        # Check if CandleKeep is initialized
        if not config.is_initialized:
            console.print("Error: CandleKeep not initialized. Run 'candlekeep init' first.")
            raise typer.Exit(1)

        # Parse fields if provided
        field_list = None
        if fields:
            field_list = [f.strip() for f in fields.split(',')]

        # Get all books from database
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            books = session.query(Book).order_by(Book.id).all()

            if not books:
                console.print("No books found in library.")
                raise typer.Exit(0)

            # Format output
            output_lines = [f"# Library Books (Total: {len(books)})", ""]

            for book in books:
                book_text = _format_book_for_llm(book, full=full, fields=field_list)
                output_lines.append(book_text)
                output_lines.append("")  # Blank line between books

            # Print to stdout
            print("\n".join(output_lines))

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"Error: {e}")
        raise typer.Exit(1)


@app.command("toc")
def get_toc(
    book_id: int = typer.Argument(..., help="Book ID to get table of contents for"),
):
    """
    Get table of contents for a specific book.

    Output is optimized for LLM consumption with hierarchical text format.
    """
    try:
        config = get_config()

        # Check if CandleKeep is initialized
        if not config.is_initialized:
            console.print("Error: CandleKeep not initialized. Run 'candlekeep init' first.")
            raise typer.Exit(1)

        # Get book from database
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()

            if not book:
                console.print(f"Error: Book with ID {book_id} not found.")
                raise typer.Exit(1)

            # Format and print TOC
            toc_text = _format_toc_for_llm(book)
            print(toc_text)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"Error: {e}")
        raise typer.Exit(1)


@app.command("pages")
def get_pages(
    book_id: int = typer.Argument(..., help="Book ID to get pages from"),
    pages: str = typer.Option(..., "--pages", "-p", help="Page ranges (e.g., '1-5,10-15' or '1,2,3')"),
):
    """
    Get specific pages from a book's markdown content.

    Supports page ranges and multiple pages. Output is raw markdown content.
    """
    try:
        config = get_config()

        # Check if CandleKeep is initialized
        if not config.is_initialized:
            console.print("Error: CandleKeep not initialized. Run 'candlekeep init' first.")
            raise typer.Exit(1)

        # Parse page ranges
        try:
            page_list = _parse_page_ranges(pages)
        except ValueError as e:
            console.print(f"Error: {e}")
            raise typer.Exit(1)

        # Get book from database
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()

            if not book:
                console.print(f"Error: Book with ID {book_id} not found.")
                raise typer.Exit(1)

            # Resolve printed page numbers to physical page numbers
            # This allows users to query by the page number printed in the book
            resolved_page_list = _resolve_printed_to_physical_pages(book_id, page_list, session)

            # Extract pages from markdown file
            md_path = Path(book.markdown_file_path)
            try:
                content = _extract_pages_from_markdown(md_path, resolved_page_list)

                if not content:
                    console.print(f"Warning: No content found for requested pages.")
                    raise typer.Exit(0)

                # Print header and content
                print(f"## Book ID: {book.id} - {book.title}")
                print(f"Pages: {pages}")
                print("")
                print(content)

            except FileNotFoundError as e:
                console.print(f"Error: {e}")
                raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"Error: {e}")
        raise typer.Exit(1)
