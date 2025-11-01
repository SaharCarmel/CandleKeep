"""File hashing utilities for duplicate detection."""

import hashlib
from pathlib import Path
from typing import Union


def compute_file_hash(file_path: Union[str, Path]) -> str:
    """
    Compute SHA256 hash of a file for duplicate detection.

    Args:
        file_path: Path to the file

    Returns:
        SHA256 hash as hexadecimal string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    sha256_hash = hashlib.sha256()

    # Read file in chunks to handle large files efficiently
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def compute_string_hash(text: str) -> str:
    """
    Compute SHA256 hash of a string.

    Args:
        text: String to hash

    Returns:
        SHA256 hash as hexadecimal string
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
