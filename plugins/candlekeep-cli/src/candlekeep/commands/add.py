"""Commands for adding books to the library."""

import shutil
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from ..db.models import Book, BookImage, SourceType
from ..db.session import get_db_manager
from ..parsers.pdf import parse_pdf, PDFParser
from ..parsers.markdown import parse_markdown
from ..utils.config import get_config
from ..utils.file_utils import sanitize_filename, ensure_directory, get_unique_filename
from ..utils.hash_utils import compute_file_hash
from ..utils.image_utils import create_book_image_directory, generate_image_filename

console = Console()
app = typer.Typer()


def _process_and_save_images(
    book_id: int,
    pdf_path: Path,
    markdown_path: Path,
    progress_task_id=None,
    progress_obj=None
) -> tuple[int, str]:
    """
    Extract images from PDF, save them, create database records, and update markdown.

    Args:
        book_id: ID of the book
        pdf_path: Path to the original PDF
        markdown_path: Path to the saved markdown file
        progress_task_id: Optional progress task ID for status updates
        progress_obj: Optional progress object for status updates

    Returns:
        Tuple of (image_count, updated_markdown_content)
    """
    try:
        config = get_config()

        # Create image directory for this book
        image_dir = create_book_image_directory(book_id)

        # Extract images using PDFParser with image extraction enabled
        with PDFParser(pdf_path) as parser:
            # Convert to markdown with image extraction
            markdown_with_images = parser.convert_to_markdown(
                extract_images=True,
                image_path=image_dir,
                dpi=150,
                size_limit=0.05
            )

            # Extract image metadata
            images_metadata = parser.extract_image_metadata()

        # Convert relative image paths to absolute in markdown
        markdown_absolute = PDFParser.convert_image_paths_to_absolute(
            markdown_with_images,
            book_id,
            image_dir
        )

        # Create BookImage database records
        db_manager = get_db_manager()
        image_count = 0

        with db_manager.get_session() as session:
            for img_meta in images_metadata:
                # Generate filename for this image
                filename = generate_image_filename(
                    page=img_meta['page_number'],
                    index=image_count,  # Use sequential index
                    format=img_meta['format']
                )

                # Create BookImage record
                book_image = BookImage(
                    book_id=book_id,
                    page_number=img_meta['page_number'],
                    printed_page_number=img_meta.get('printed_page_number'),  # May be None
                    xref=img_meta['xref'],
                    file_path=str(image_dir / filename),
                    width=img_meta['width'],
                    height=img_meta['height'],
                    format=img_meta['format'],
                    colorspace=img_meta.get('colorspace'),
                    has_transparency=img_meta.get('has_transparency', False),
                    file_size=img_meta.get('file_size')
                )
                session.add(book_image)
                image_count += 1

            # Update book's image statistics
            book = session.query(Book).filter(Book.id == book_id).first()
            if book:
                book.image_count = image_count
                book.has_images = image_count > 0

        # Update the markdown file with absolute paths
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_absolute)

        return image_count, markdown_absolute

    except Exception as e:
        console.print(f"\n[yellow]Warning:[/yellow] Image extraction failed: {e}")
        console.print("[yellow]Book added successfully, but without images.[/yellow]")
        return 0, ""


@app.command("add-pdf")
def add_pdf(
    file_path: Path = typer.Argument(..., help="Path to PDF file", exists=True, dir_okay=False),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Book category"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
    keep_original: bool = typer.Option(True, "--keep-original/--no-keep-original", help="Keep original PDF file"),
    title: Optional[str] = typer.Option(None, "--title", help="Override extracted title"),
    author: Optional[str] = typer.Option(None, "--author", help="Override extracted author"),
):
    """
    Add a PDF book to the CandleKeep library.

    The PDF will be converted to markdown and metadata will be extracted and stored.
    """
    try:
        config = get_config()

        # Check if CandleKeep is initialized
        if not config.is_initialized:
            console.print("[red]Error:[/red] CandleKeep not initialized. Run 'candlekeep init' first.")
            raise typer.Exit(1)

        # Validate file is a PDF
        if file_path.suffix.lower() != '.pdf':
            console.print(f"[red]Error:[/red] File must be a PDF, got: {file_path.suffix}")
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Compute file hash
            task = progress.add_task("[cyan]Computing file hash...", total=None)
            file_hash = compute_file_hash(file_path)
            progress.update(task, completed=True)

            # Step 2: Check for duplicates
            task = progress.add_task("[cyan]Checking for duplicates...", total=None)
            db_manager = get_db_manager()

            with db_manager.get_session() as session:
                existing = session.query(Book).filter(Book.file_hash == file_hash).first()
                if existing:
                    progress.stop()
                    console.print(f"\n[yellow]Book already exists:[/yellow] {existing.title} (ID: {existing.id})")
                    raise typer.Exit(0)

            progress.update(task, completed=True)

            # Step 3: Parse PDF and extract metadata
            task = progress.add_task("[cyan]Parsing PDF and extracting metadata...", total=None)
            try:
                metadata = parse_pdf(file_path, convert_to_md=True)
            except Exception as e:
                progress.stop()
                console.print(f"\n[red]Error parsing PDF:[/red] {e}")
                raise typer.Exit(1)
            progress.update(task, completed=True)

            # Override metadata if provided
            if title:
                metadata['title'] = title
            if author:
                metadata['author'] = author
            if category:
                metadata['category'] = category

            # Parse tags
            tag_list = None
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

            # Step 4: Save markdown to library
            task = progress.add_task("[cyan]Saving markdown to library...", total=None)

            # Generate filename from title
            safe_filename = sanitize_filename(metadata['title'])
            md_filepath = get_unique_filename(config.library_dir, safe_filename, '.md')

            # Write markdown content
            ensure_directory(config.library_dir)
            with open(md_filepath, 'w', encoding='utf-8') as f:
                f.write(metadata['markdown_content'])

            progress.update(task, completed=True)

            # Step 5: Optionally copy original PDF
            original_path = file_path
            if keep_original:
                task = progress.add_task("[cyan]Copying original PDF...", total=None)
                ensure_directory(config.originals_dir)
                original_copy_path = get_unique_filename(config.originals_dir, safe_filename, '.pdf')
                shutil.copy2(file_path, original_copy_path)
                original_path = original_copy_path
                progress.update(task, completed=True)

            # Step 6: Insert into database
            task = progress.add_task("[cyan]Storing metadata in database...", total=None)

            book = Book(
                title=metadata.get('title', 'Untitled'),
                author=metadata.get('author'),
                original_file_path=str(original_path),
                markdown_file_path=str(md_filepath),
                source_type=SourceType.PDF,
                file_hash=file_hash,
                pdf_creation_date=metadata.get('pdf_creation_date'),
                pdf_mod_date=metadata.get('pdf_mod_date'),
                pdf_creator=metadata.get('pdf_creator'),
                pdf_producer=metadata.get('pdf_producer'),
                page_count=metadata.get('page_count'),
                word_count=metadata.get('word_count'),
                chapter_count=metadata.get('chapter_count', 0),
                table_of_contents=metadata.get('table_of_contents'),
                subject=metadata.get('subject'),
                keywords=metadata.get('keywords'),
                category=category,
                tags=tag_list,
                language='en',
            )

            try:
                with db_manager.get_session() as session:
                    session.add(book)
                    session.flush()  # Get the ID
                    book_id = book.id

                progress.update(task, completed=True)

                # Step 7: Extract and save images
                task = progress.add_task("[cyan]Extracting images from PDF...", total=None)
                image_count, _ = _process_and_save_images(
                    book_id=book_id,
                    pdf_path=file_path,
                    markdown_path=md_filepath,
                    progress_task_id=task,
                    progress_obj=progress
                )
                progress.update(task, completed=True)

                # Update metadata with image count for display
                metadata['image_count'] = image_count
                metadata['has_images'] = image_count > 0

            except IntegrityError as e:
                progress.stop()
                console.print(f"\n[red]Database error:[/red] {e}")
                # Clean up created files
                if md_filepath.exists():
                    md_filepath.unlink()
                if keep_original and original_copy_path.exists():
                    original_copy_path.unlink()
                raise typer.Exit(1)

        # Success message
        _display_success(book_id, metadata, md_filepath, category, tag_list)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


def _display_success(
    book_id: int,
    metadata: dict,
    md_filepath: Path,
    category: Optional[str],
    tags: Optional[List[str]]
):
    """Display success message with book details."""

    # Create details table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("ID", str(book_id))
    table.add_row("Title", metadata.get('title', 'Untitled'))
    if metadata.get('author'):
        table.add_row("Author", metadata['author'])
    if category:
        table.add_row("Category", category)
    if tags:
        table.add_row("Tags", ", ".join(tags))
    table.add_row("Pages", str(metadata.get('page_count', 'N/A')))
    table.add_row("Words", f"{metadata.get('word_count', 0):,}")
    table.add_row("Chapters", str(metadata.get('chapter_count', 0)))
    if metadata.get('image_count', 0) > 0:
        table.add_row("Images", str(metadata.get('image_count', 0)))
    table.add_row("Markdown", str(md_filepath))

    panel = Panel(
        table,
        title="[green bold]✓ Book Added Successfully",
        border_style="green",
    )

    console.print()
    console.print(panel)


@app.command("add-md")
def add_md(
    file_path: Path = typer.Argument(..., help="Path to markdown file", exists=True, dir_okay=False),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Book category"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
    title: Optional[str] = typer.Option(None, "--title", help="Override extracted title"),
    author: Optional[str] = typer.Option(None, "--author", help="Override extracted author"),
):
    """
    Add a markdown book to the CandleKeep library.

    The markdown file will be copied to the library and metadata will be extracted and stored.
    Metadata can be provided via YAML frontmatter or will be extracted from the document structure.
    """
    try:
        config = get_config()

        # Check if CandleKeep is initialized
        if not config.is_initialized:
            console.print("[red]Error:[/red] CandleKeep not initialized. Run 'candlekeep init' first.")
            raise typer.Exit(1)

        # Validate file is markdown
        if file_path.suffix.lower() not in ['.md', '.markdown']:
            console.print(f"[red]Error:[/red] File must be a markdown file (.md or .markdown), got: {file_path.suffix}")
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Compute file hash
            task = progress.add_task("[cyan]Computing file hash...", total=None)
            file_hash = compute_file_hash(file_path)
            progress.update(task, completed=True)

            # Step 2: Check for duplicates
            task = progress.add_task("[cyan]Checking for duplicates...", total=None)
            db_manager = get_db_manager()

            with db_manager.get_session() as session:
                existing = session.query(Book).filter(Book.file_hash == file_hash).first()
                if existing:
                    progress.stop()
                    console.print(f"\n[yellow]Book already exists:[/yellow] {existing.title} (ID: {existing.id})")
                    raise typer.Exit(0)

            progress.update(task, completed=True)

            # Step 3: Parse markdown and extract metadata
            task = progress.add_task("[cyan]Parsing markdown and extracting metadata...", total=None)
            try:
                metadata = parse_markdown(file_path)
            except Exception as e:
                progress.stop()
                console.print(f"\n[red]Error parsing markdown:[/red] {e}")
                raise typer.Exit(1)
            progress.update(task, completed=True)

            # Override metadata if provided
            if title:
                metadata['title'] = title
            if author:
                metadata['author'] = author
            if category:
                metadata['category'] = category

            # Parse tags
            tag_list = metadata.get('tags', [])
            if tags:
                # CLI tags override frontmatter tags
                tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            elif isinstance(tag_list, list):
                # Use frontmatter tags as-is
                pass
            else:
                tag_list = None

            # Step 4: Copy markdown to library
            task = progress.add_task("[cyan]Copying markdown to library...", total=None)

            # Generate filename from title
            safe_filename = sanitize_filename(metadata['title'])
            md_filepath = get_unique_filename(config.library_dir, safe_filename, '.md')

            # Copy file to library
            ensure_directory(config.library_dir)
            shutil.copy2(file_path, md_filepath)

            progress.update(task, completed=True)

            # Step 5: Insert into database
            task = progress.add_task("[cyan]Storing metadata in database...", total=None)

            book = Book(
                title=metadata.get('title', 'Untitled'),
                author=metadata.get('author'),
                original_file_path=str(file_path),
                markdown_file_path=str(md_filepath),
                source_type=SourceType.MARKDOWN,
                file_hash=file_hash,
                page_count=None,  # Markdown doesn't have pages
                word_count=metadata.get('word_count'),
                chapter_count=metadata.get('chapter_count', 0),
                table_of_contents=metadata.get('table_of_contents'),
                subject=metadata.get('subject'),
                keywords=metadata.get('keywords'),
                category=category or metadata.get('category'),
                tags=tag_list,
                isbn=metadata.get('isbn'),
                publisher=metadata.get('publisher'),
                publication_year=metadata.get('publication_year'),
                language=metadata.get('language', 'en'),
            )

            try:
                with db_manager.get_session() as session:
                    session.add(book)
                    session.flush()  # Get the ID
                    book_id = book.id

                progress.update(task, completed=True)

            except IntegrityError as e:
                progress.stop()
                console.print(f"\n[red]Database error:[/red] {e}")
                # Clean up created file
                if md_filepath.exists():
                    md_filepath.unlink()
                raise typer.Exit(1)

        # Success message
        _display_success_md(book_id, metadata, md_filepath, category or metadata.get('category'), tag_list)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


def _display_success_md(
    book_id: int,
    metadata: dict,
    md_filepath: Path,
    category: Optional[str],
    tags: Optional[List[str]]
):
    """Display success message for markdown book with details."""

    # Create details table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("ID", str(book_id))
    table.add_row("Title", metadata.get('title', 'Untitled'))
    if metadata.get('author'):
        table.add_row("Author", metadata['author'])
    if category:
        table.add_row("Category", category)
    if tags:
        table.add_row("Tags", ", ".join(tags))
    table.add_row("Words", f"{metadata.get('word_count', 0):,}")
    table.add_row("Chapters", str(metadata.get('chapter_count', 0)))
    if metadata.get('isbn'):
        table.add_row("ISBN", metadata['isbn'])
    if metadata.get('publisher'):
        table.add_row("Publisher", metadata['publisher'])
    if metadata.get('publication_year'):
        table.add_row("Year", str(metadata['publication_year']))
    table.add_row("File", str(md_filepath))

    panel = Panel(
        table,
        title="[green bold]✓ Markdown Book Added Successfully",
        border_style="green",
    )

    console.print()
    console.print(panel)
