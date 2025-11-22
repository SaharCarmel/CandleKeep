"""Image storage and management utilities for CandleKeep."""

import os
import shutil
from pathlib import Path
from typing import Optional

from candlekeep.utils.config import get_config


def create_book_image_directory(book_id: int) -> Path:
    """Create image directory for a specific book.

    Args:
        book_id: ID of the book

    Returns:
        Path to the created directory

    Raises:
        OSError: If directory creation fails
    """
    config = get_config()
    book_image_dir = config.images_dir / str(book_id)
    book_image_dir.mkdir(parents=True, exist_ok=True)
    return book_image_dir


def generate_image_filename(page: int, index: int, format: str) -> str:
    """Generate filename for an extracted image using page-based naming.

    Args:
        page: Page number where image appears
        index: Image index on the page (0-based)
        format: Image format (png, jpg, etc.)

    Returns:
        Filename in format: page-{page}-img-{index}.{ext}

    Example:
        >>> generate_image_filename(41, 0, 'png')
        'page-41-img-0.png'
        >>> generate_image_filename(41, 1, 'jpg')
        'page-41-img-1.jpg'
    """
    # Normalize format (remove dot if present, lowercase)
    ext = format.lower().lstrip('.')
    return f"page-{page}-img-{index}.{ext}"


def get_book_image_directory(book_id: int) -> Path:
    """Get the image directory path for a specific book.

    Args:
        book_id: ID of the book

    Returns:
        Path to the book's image directory
    """
    config = get_config()
    return config.images_dir / str(book_id)


def cleanup_book_images(book_id: int) -> bool:
    """Remove all images for a specific book.

    Args:
        book_id: ID of the book

    Returns:
        True if cleanup successful, False if directory didn't exist

    Raises:
        OSError: If deletion fails for other reasons
    """
    book_image_dir = get_book_image_directory(book_id)

    if not book_image_dir.exists():
        return False

    shutil.rmtree(book_image_dir)
    return True


def get_absolute_image_path(book_id: int, filename: str) -> str:
    """Get absolute path to an image file.

    Args:
        book_id: ID of the book
        filename: Image filename (e.g., 'page-5-img-0.png')

    Returns:
        Absolute path to the image file as a string

    Example:
        >>> get_absolute_image_path(1, 'page-5-img-0.png')
        '/Users/user/.candlekeep/images/1/page-5-img-0.png'
    """
    book_image_dir = get_book_image_directory(book_id)
    image_path = book_image_dir / filename
    return str(image_path.absolute())


def get_image_path_for_markdown(book_id: int, filename: str) -> str:
    """Get absolute path suitable for markdown image references.

    This is an alias for get_absolute_image_path but makes the intent
    clear when used in markdown generation.

    Args:
        book_id: ID of the book
        filename: Image filename

    Returns:
        Absolute path as a string for use in markdown ![](path) syntax
    """
    return get_absolute_image_path(book_id, filename)


def book_has_images(book_id: int) -> bool:
    """Check if a book has any images stored.

    Args:
        book_id: ID of the book

    Returns:
        True if image directory exists and contains files
    """
    book_image_dir = get_book_image_directory(book_id)

    if not book_image_dir.exists():
        return False

    # Check if directory contains any files
    return any(book_image_dir.iterdir())


def count_book_images(book_id: int) -> int:
    """Count the number of images stored for a book.

    Args:
        book_id: ID of the book

    Returns:
        Number of image files in the book's image directory
    """
    book_image_dir = get_book_image_directory(book_id)

    if not book_image_dir.exists():
        return 0

    # Count only files (not directories)
    return sum(1 for item in book_image_dir.iterdir() if item.is_file())


def validate_image_exists(book_id: int, filename: str) -> bool:
    """Check if an image file exists for a book.

    Args:
        book_id: ID of the book
        filename: Image filename to check

    Returns:
        True if image file exists and is readable
    """
    image_path = Path(get_absolute_image_path(book_id, filename))
    return image_path.exists() and image_path.is_file()
