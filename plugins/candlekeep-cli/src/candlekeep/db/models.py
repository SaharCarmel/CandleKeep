"""SQLAlchemy models for CandleKeep database."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    JSON,
    Boolean,
)
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class SourceType(enum.Enum):
    """Source type for books."""
    PDF = "pdf"
    MARKDOWN = "markdown"


class NoteType(enum.Enum):
    """Note type for book annotations."""
    SUMMARY = "summary"
    REVIEW = "review"
    TAG = "tag"
    OTHER = "other"


class Book(Base):
    """Book model - stores metadata only, content in markdown files."""

    __tablename__ = "books"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core metadata
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(255), index=True)

    # File information
    original_file_path = Column(String(1000), nullable=False)
    markdown_file_path = Column(String(1000), nullable=False)
    source_type = Column(Enum(SourceType), nullable=False, index=True)
    file_hash = Column(String(64), unique=True, nullable=False)

    # Dates
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_date = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # PDF-specific metadata
    pdf_creation_date = Column(DateTime)
    pdf_mod_date = Column(DateTime)
    pdf_creator = Column(String(255))
    pdf_producer = Column(String(255))

    # Content metrics
    page_count = Column(Integer)
    word_count = Column(Integer)
    chapter_count = Column(Integer)
    table_of_contents = Column(JSON)  # List of TOC entries with level, title, page

    # Categorization
    subject = Column(String(500))
    keywords = Column(Text)  # Comma-separated
    category = Column(String(100), index=True)
    tags = Column(JSON)  # List of tags

    # Additional info
    isbn = Column(String(20))
    publisher = Column(String(255))
    publication_year = Column(Integer)
    language = Column(String(10), default="en")

    # Image metrics
    image_count = Column(Integer, default=0, nullable=False)
    has_images = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    notes = relationship("BookNote", back_populates="book", cascade="all, delete-orphan")
    images = relationship("BookImage", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"


class BookNote(Base):
    """Book notes and annotations."""

    __tablename__ = "book_notes"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    # Note data
    note_type = Column(Enum(NoteType), default=NoteType.OTHER, nullable=False)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    book = relationship("Book", back_populates="notes")

    # Indexes
    __table_args__ = (
        Index("idx_book_type", "book_id", "note_type"),
    )

    def __repr__(self):
        return f"<BookNote(id={self.id}, book_id={self.book_id}, type={self.note_type})>"


class BookImage(Base):
    """Book image metadata - stores information about images extracted from PDFs."""

    __tablename__ = "book_images"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)

    # Image location
    page_number = Column(Integer, nullable=False)  # PDF physical page index (0-based, canonical)
    printed_page_number = Column(Integer, nullable=True)  # Number printed on actual page (user-friendly)
    xref = Column(Integer, nullable=False)  # PDF object reference for potential deduplication
    file_path = Column(String(1000), nullable=False)  # Path to extracted image file

    # Image dimensions
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    # Image properties
    format = Column(String(10), nullable=False)  # png, jpg, etc.
    colorspace = Column(String(20))  # RGB, CMYK, Gray, etc.
    has_transparency = Column(Boolean, default=False)
    file_size = Column(Integer)  # Size in bytes

    # Metadata
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    book = relationship("Book", back_populates="images")

    # Indexes
    __table_args__ = (
        Index("idx_book_page", "book_id", "page_number"),
    )

    def __repr__(self):
        return f"<BookImage(id={self.id}, book_id={self.book_id}, page={self.page_number}, format={self.format})>"
