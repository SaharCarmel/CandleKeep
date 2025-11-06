# [TASK001] - CLI Tool for Book Management with Metadata Storage

**Status:** Pending
**Added:** 2025-11-01
**Updated:** 2025-11-01

## Original Request

Create a CLI tool that:
1. Adds PDF or Markdown files to CandleKeep library
2. Converts PDFs to Markdown (stored locally)
3. Extracts and stores metadata in SQLite database
4. Generates table of contents from books
5. Provides commands to list, show, search, update, and remove books

**Focus:** Metadata-only storage in database, full content as local markdown files.
**Database:** SQLite with Alembic migrations for schema management.

## Context & Background

### Architecture Decision
- **Local-First**: Books stored as markdown files in `~/.candlekeep/library/`
- **Metadata-Only Database**: SQLite stores only book metadata, not content chunks
- **Database Migrations**: Alembic for schema version control and migrations
- **PDF Conversion**: One-time PDF → Markdown conversion using pymupdf4llm
- **File Organization**: Original PDFs optionally kept in `~/.candlekeep/originals/`

### Technology Stack
- **CLI Framework**: Typer (type-hint based, built on Click)
- **Database**: SQLAlchemy ORM + SQLite
- **Migrations**: Alembic for database schema management
- **PDF Parsing**: PyMuPDF (pymupdf4llm for markdown conversion)
- **Markdown Parsing**: python-frontmatter for YAML frontmatter
- **UI/Output**: Rich for beautiful terminal output

### Metadata Extraction Strategy

#### PDF Metadata (Priority Order)
1. **Embedded PDF Metadata** - PyMuPDF `doc.metadata` (title, author, subject, keywords, dates)
2. **Table of Contents** - PyMuPDF `doc.get_toc()` (chapter structure)
3. **First Page Analysis** - Fallback extraction from first page text
4. **Filename Parsing** - Extract from filename pattern
5. **User Input** - Manual override via CLI flags

#### Markdown Metadata (Priority Order)
1. **YAML Frontmatter** - python-frontmatter extraction
2. **First Heading** - Use `# Title` as fallback
3. **Filename** - Parse from filename
4. **User Input** - Manual override via CLI flags

### Database Schema

```sql
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- Core Metadata
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),

    -- File Information
    original_file_path VARCHAR(1000) NOT NULL,
    markdown_file_path VARCHAR(1000) NOT NULL,
    source_type ENUM('pdf', 'markdown') NOT NULL,
    file_hash VARCHAR(64) UNIQUE NOT NULL,

    -- Dates
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- PDF-specific metadata
    pdf_creation_date DATETIME,
    pdf_mod_date DATETIME,
    pdf_creator VARCHAR(255),
    pdf_producer VARCHAR(255),

    -- Content metrics
    page_count INT,
    word_count INT,
    chapter_count INT,

    -- Categorization
    subject VARCHAR(500),
    keywords TEXT,
    category VARCHAR(100),
    tags JSON,

    -- Additional info
    isbn VARCHAR(20),
    publisher VARCHAR(255),
    publication_year INT,
    language VARCHAR(10) DEFAULT 'en',

    -- Indexes
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_category (category),
    INDEX idx_source_type (source_type),
    FULLTEXT INDEX idx_keywords (keywords)
);

CREATE TABLE book_notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    note_type ENUM('summary', 'review', 'tag', 'other') DEFAULT 'other',
    content TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    INDEX idx_book_type (book_id, note_type)
);
```

### File Structure

```
~/.candlekeep/
├── candlekeep.db            # SQLite database
├── library/                 # All books as markdown
│   ├── clean-code.md
│   ├── refactoring.md
│   └── my-coding-guide.md
└── originals/               # Original PDFs (optional backup)
    ├── clean-code.pdf
    └── refactoring.pdf
```

### Project Structure

```
candlekeep/
├── pyproject.toml
├── README.md
├── src/
│   └── candlekeep/
│       ├── __init__.py
│       ├── cli.py              # Typer CLI entry point
│       ├── db/
│       │   ├── __init__.py
│       │   ├── models.py       # SQLAlchemy models
│       │   └── session.py      # Database connection
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── pdf.py          # PDF parsing & metadata extraction
│       │   └── markdown.py     # Markdown parsing & frontmatter
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── init.py         # Setup command
│       │   ├── add.py          # Add PDF/MD commands
│       │   ├── list.py         # List books
│       │   ├── show.py         # Show details
│       │   ├── update.py       # Update metadata
│       │   ├── search.py       # Search books
│       │   ├── remove.py       # Remove books
│       │   └── stats.py        # Library statistics
│       └── utils/
│           ├── __init__.py
│           ├── config.py       # Configuration management
│           ├── file_utils.py   # File operations
│           └── hash_utils.py   # SHA256 hashing
└── tasks/
    └── TASK001-cli-tool-book-management-metadata.md
```

## Implementation Plan

### Phase 1: Foundation & Configuration
**Goal:** Set up project structure, dependencies, and initialization

- [ ] 1.1 Create project structure (src/candlekeep with all subdirectories)
- [ ] 1.2 Set up pyproject.toml with all dependencies
- [ ] 1.3 Create SQLAlchemy models (books, book_notes)
- [ ] 1.4 Create database session management
- [ ] 1.5 Implement configuration management (config.yaml reader/writer)
- [ ] 1.6 Implement `candlekeep init` command
  - Create `~/.candlekeep/` directory structure
  - Initialize SQLite database (~/.candlekeep/candlekeep.db)
  - Run Alembic migrations to create schema
  - Create library/ folder for books
- [ ] 1.7 Test: Run init command and verify setup

### Phase 2: PDF Processing
**Goal:** Extract metadata and convert PDFs to markdown

- [ ] 2.1 Implement SHA256 hashing utility
- [ ] 2.2 Implement PDF metadata extraction (PyMuPDF)
  - Extract embedded metadata (title, author, subject, keywords, dates)
  - Extract table of contents
  - Count pages
- [ ] 2.3 Implement PDF to markdown conversion (pymupdf4llm)
- [ ] 2.4 Implement word/chapter counting
- [ ] 2.5 Implement filename parsing fallback
- [ ] 2.6 Create PDF parser module that returns structured metadata
- [ ] 2.7 Test: Parse sample PDF and verify metadata extraction

### Phase 3: Markdown Processing
**Goal:** Extract metadata from markdown files

- [ ] 3.1 Implement YAML frontmatter parsing (python-frontmatter)
- [ ] 3.2 Implement first heading extraction fallback
- [ ] 3.3 Implement word/heading counting
- [ ] 3.4 Implement filename parsing fallback
- [ ] 3.5 Create markdown parser module that returns structured metadata
- [ ] 3.6 Test: Parse sample markdown and verify metadata extraction

### Phase 4: Add Commands
**Goal:** Implement commands to add books to library

- [ ] 4.1 Implement `candlekeep add-pdf` command
  - Accept file path and optional metadata flags
  - Check for duplicates via hash
  - Extract metadata
  - Convert to markdown
  - Save to ~/.candlekeep/library/
  - Optionally copy original to originals/
  - Insert into database
  - Display success message with Rich formatting
- [ ] 4.2 Implement `candlekeep add-md` command
  - Accept file path and optional metadata flags
  - Check for duplicates via hash
  - Extract metadata
  - Copy to ~/.candlekeep/library/
  - Insert into database
  - Display success message with Rich formatting
- [ ] 4.3 Test: Add PDF and markdown books, verify files and database

### Phase 5: Query Commands
**Goal:** Implement commands to view and search books

- [ ] 5.1 Implement `candlekeep list` command
  - Support filters (category, author, tag)
  - Support output formats (table, json, simple)
  - Support sorting (title, author, date, id)
  - Rich table formatting
- [ ] 5.2 Implement `candlekeep show <book-id>` command
  - Display all metadata
  - Show file paths
  - Rich formatted output
- [ ] 5.3 Implement `candlekeep search <query>` command
  - Search in title, author, keywords, or all
  - Limit results
  - Rich formatted output
- [ ] 5.4 Implement `candlekeep stats` command
  - Total books, pages, words
  - Category breakdown
  - Top authors
  - Rich formatted output
- [ ] 5.5 Test: List, show, search, and stats commands

### Phase 6: Management Commands
**Goal:** Implement commands to update and remove books

- [ ] 6.1 Implement `candlekeep update <book-id>` command
  - Update title, author, category, tags, isbn, publisher, year
  - Support adding tags without replacing
  - Update modified_date
- [ ] 6.2 Implement `candlekeep remove <book-id>` command
  - Show confirmation with book details
  - Remove from database
  - Optionally delete files
  - Handle errors gracefully
- [ ] 6.3 Test: Update and remove commands

### Phase 7: Polish & Error Handling
**Goal:** Production-ready CLI with excellent UX

- [ ] 7.1 Add comprehensive error handling
  - File not found
  - Database connection errors
  - Invalid file formats
  - Duplicate books
  - Missing dependencies
- [ ] 7.2 Add progress indicators for long operations
  - PDF parsing
  - Large file operations
- [ ] 7.3 Add confirmation prompts for destructive operations
- [ ] 7.4 Improve Rich formatting consistency
- [ ] 7.5 Add helpful error messages with suggestions
- [ ] 7.6 Test: Error scenarios and edge cases

## Progress Tracking

**Overall Status:** Phase 3 Complete - 60% Complete (Foundation + PDF + Markdown Processing)

### Subtasks
| ID | Description | Status | Updated | Notes |
|----|-------------|--------|---------|-------|
| 1.1 | Create project structure | Complete | 2025-11-01 | src/candlekeep with all subdirectories created |
| 1.2 | Set up pyproject.toml | Complete | 2025-11-01 | UV package manager configured with all dependencies |
| 1.3 | Create SQLAlchemy models | Complete | 2025-11-01 | Book and BookNote models with 24+ fields |
| 1.4 | Create database session management | Complete | 2025-11-01 | SQLite connection with context manager |
| 1.5 | Set up Alembic migrations | Complete | 2025-11-01 | Initial migration created and tested |
| 1.6 | Implement init command | Complete | 2025-11-01 | Zero-config initialization with Rich UI |
| 1.7 | Test init command | Complete | 2025-11-01 | E2E test passed - all features verified |
| 2.1 | Implement SHA256 hashing | Complete | 2025-11-01 | utils/hash_utils.py with SHA256 file hashing |
| 2.2 | Implement PDF metadata extraction | Complete | 2025-11-01 | PyMuPDF extraction with TOC support (192 chapters) |
| 2.3 | Implement PDF to markdown conversion | Complete | 2025-11-01 | pymupdf4llm with page markers innovation |
| 2.4 | Implement word/chapter counting | Complete | 2025-11-01 | Content metrics calculation (82K words, 192 chapters) |
| 2.5 | Implement filename parsing | Complete | 2025-11-01 | Fallback extraction in file_utils.py |
| 2.6 | Create PDF parser module | Complete | 2025-11-01 | parsers/pdf.py with complete integration |
| 2.7 | Test PDF parsing | Complete | 2025-11-01 | E2E tests 2 & 4 passed + page extraction validated |
| 3.1 | Implement frontmatter parsing | Complete | 2025-11-06 | python-frontmatter with YAML extraction |
| 3.2 | Implement heading extraction | Complete | 2025-11-06 | Fallback to first # heading |
| 3.3 | Implement word/heading counting | Complete | 2025-11-06 | Word counting from clean text |
| 3.4 | Implement filename parsing | Complete | 2025-11-06 | Reuses utils/file_utils.py |
| 3.5 | Create markdown parser module | Complete | 2025-11-06 | parsers/markdown.py with full integration |
| 3.6 | Test markdown parsing | Complete | 2025-11-06 | E2E Test 3 passed + edge cases |
| 4.1 | Implement add-pdf command | Complete | 2025-11-01 | commands/add.py with progress indicators & rich output |
| 4.2 | Implement add-md command | Complete | 2025-11-06 | Full workflow with frontmatter support |
| 4.3 | Test add commands | Complete | 2025-11-06 | Both add-pdf and add-md tested |
| 5.1 | Implement list command | Not Started | 2025-11-01 | With filters and formats |
| 5.2 | Implement show command | Not Started | 2025-11-01 | Rich formatting |
| 5.3 | Implement search command | Not Started | 2025-11-01 | Full-text search |
| 5.4 | Implement stats command | Not Started | 2025-11-01 | Library statistics |
| 5.5 | Test query commands | Not Started | 2025-11-01 | E2E test |
| 6.1 | Implement update command | Not Started | 2025-11-01 | Metadata updates |
| 6.2 | Implement remove command | Not Started | 2025-11-01 | With confirmation |
| 6.3 | Test management commands | Not Started | 2025-11-01 | E2E test |
| 7.1 | Add error handling | Not Started | 2025-11-01 | Comprehensive coverage |
| 7.2 | Add progress indicators | Complete | 2025-11-01 | Implemented for PDF parsing operations |
| 7.3 | Add confirmation prompts | Not Started | 2025-11-01 | Destructive operations |
| 7.4 | Improve Rich formatting | Not Started | 2025-11-01 | Consistency |
| 7.5 | Add helpful error messages | Not Started | 2025-11-01 | With suggestions |
| 7.6 | Test error scenarios | Not Started | 2025-11-01 | E2E test |

## End-to-End Testing Instructions

**Testing Philosophy:** This project uses ONLY end-to-end testing. No unit tests or integration tests. All tests are executed manually by Claude Code following these procedures.

### Test Environment Setup

1. **Prerequisites:**
   - MySQL server running locally
   - Python 3.10+ installed
   - Clean home directory for testing (`~/.candlekeep` removed)

2. **Installation:**
   ```bash
   cd /Users/saharcarmel/Focus/CandleKeep
   pip install -e .
   ```

### Test Suite

#### Test 1: Initial Setup (Phase 1)
**Objective:** Verify initialization and configuration

```bash
# Clean slate
rm -rf ~/.candlekeep

# Run init command
candlekeep init

# Verify:
# - Prompts for MySQL connection details
# - Creates ~/.candlekeep/ directory
# - Creates config.yaml with correct settings
# - Creates library/ and originals/ subdirectories
# - Creates database tables (books, book_notes)
# - Shows success message

# Validation:
ls -la ~/.candlekeep/
cat ~/.candlekeep/config.yaml
mysql -u <user> -p -e "USE candlekeep; SHOW TABLES;"
mysql -u <user> -p -e "USE candlekeep; DESCRIBE books;"
```

**Expected Results:**
- Config file exists with correct MySQL settings
- Directory structure created
- Database schema created correctly
- No errors during setup

---

#### Test 2: Add PDF Book (Phase 2-4)
**Objective:** Add a PDF book and verify metadata extraction and storage

```bash
# Prepare test PDF (use a real PDF with metadata)
# Example: "Clean Code" by Robert C. Martin

candlekeep add-pdf ~/Downloads/clean-code.pdf --category "Software Engineering" --tags "programming,clean-code"

# Verify:
# - Shows progress indicator
# - Extracts metadata from PDF
# - Converts to markdown
# - Saves to ~/.candlekeep/library/clean-code.md
# - Stores metadata in database
# - Shows success message with book ID

# Validation:
ls -la ~/.candlekeep/library/
head -n 50 ~/.candlekeep/library/clean-code.md
mysql -u <user> -p -e "USE candlekeep; SELECT * FROM books;"
```

**Expected Results:**
- Markdown file created with correct content
- Metadata correctly extracted (title, author, pages)
- Database record created with all fields populated
- Table of contents extracted (chapter_count > 0)
- Word count calculated
- File hash stored correctly

**Test with various PDFs:**
- Well-formatted PDF with metadata
- PDF without metadata (test fallbacks)
- PDF with special characters in filename
- Large PDF (test progress indicator)

---

#### Test 3: Add Markdown Book (Phase 3-4)
**Objective:** Add a markdown book with YAML frontmatter

```bash
# Create test markdown file
cat > ~/test-book.md << 'EOF'
---
title: My Coding Philosophy
author: Sahar Carmel
category: Technical Writing
tags: [coding, philosophy, practices]
---

# My Coding Philosophy

## Chapter 1: Introduction
Content here...

## Chapter 2: Best Practices
More content...
EOF

candlekeep add-md ~/test-book.md

# Verify:
# - Extracts frontmatter metadata
# - Copies to ~/.candlekeep/library/
# - Stores metadata in database
# - Counts words and headings

# Validation:
cat ~/.candlekeep/library/my-coding-philosophy.md
mysql -u <user> -p -e "USE candlekeep; SELECT * FROM books WHERE source_type='markdown';"
```

**Expected Results:**
- Frontmatter metadata correctly extracted
- Markdown file copied correctly
- Database record with accurate metadata
- Chapter count matches heading count

**Test with various markdown files:**
- With complete frontmatter
- Without frontmatter (test fallback to first heading)
- With minimal frontmatter
- With special characters

---

#### Test 4: Duplicate Detection
**Objective:** Verify SHA256 hash prevents duplicates

```bash
# Try adding the same PDF again
candlekeep add-pdf ~/Downloads/clean-code.pdf

# Expected: Error message saying book already exists
# Should show: "Book already exists: Clean Code (ID: 1)"
```

**Expected Results:**
- Duplicate detected via hash
- Clear error message
- No database insertion
- No file duplication

---

#### Test 5: List Books (Phase 5)
**Objective:** Test listing with various filters and formats

```bash
# List all books (table format)
candlekeep list

# List with filters
candlekeep list --category "Software Engineering"
candlekeep list --author "Martin"
candlekeep list --tag "programming"

# Different formats
candlekeep list --format json
candlekeep list --format simple

# Different sorting
candlekeep list --sort title
candlekeep list --sort author
candlekeep list --sort date
```

**Expected Results:**
- Table format shows ID, Title, Author, Type, Pages, Added
- Filters work correctly (case-insensitive)
- JSON output is valid JSON
- Simple format is clean and readable
- Sorting works correctly
- Shows count at bottom

---

#### Test 6: Show Book Details (Phase 5)
**Objective:** Display complete book information

```bash
candlekeep show 1

# Verify:
# - Shows all metadata fields
# - Shows file paths
# - Shows dates
# - Shows metrics (pages, words, chapters)
# - Rich formatted output
```

**Expected Results:**
- All metadata displayed correctly
- File paths are accurate
- Dates formatted properly
- Keywords/tags displayed
- Rich formatting looks good

---

#### Test 7: Search Books (Phase 5)
**Objective:** Full-text search functionality

```bash
# Search in all fields
candlekeep search "clean code"

# Search in specific fields
candlekeep search "Martin" --in author
candlekeep search "software" --in keywords

# Limit results
candlekeep search "code" --limit 5
```

**Expected Results:**
- Returns relevant results
- Search is case-insensitive
- Field-specific search works
- Limit parameter works
- Shows match context/snippet

---

#### Test 8: Library Statistics (Phase 5)
**Objective:** Display aggregate library stats

```bash
candlekeep stats

# Verify:
# - Total book count
# - Breakdown by type (PDF/Markdown)
# - Total pages and words
# - Category breakdown
# - Top authors
```

**Expected Results:**
- Accurate counts
- Correct aggregation
- Rich formatted output
- No errors with empty categories

---

#### Test 9: Update Metadata (Phase 6)
**Objective:** Modify book metadata

```bash
# Update various fields
candlekeep update 1 --title "Clean Code: Updated"
candlekeep update 1 --author "Robert C. Martin (Uncle Bob)"
candlekeep update 1 --category "Programming"
candlekeep update 1 --tags "clean-code,refactoring,best-practices"
candlekeep update 1 --add-tags "software-craftsmanship"
candlekeep update 1 --isbn "978-0132350884"

# Verify changes
candlekeep show 1
mysql -u <user> -p -e "USE candlekeep; SELECT title, author, tags FROM books WHERE id=1;"
```

**Expected Results:**
- All fields update correctly
- Tags replacement works
- Add-tags appends correctly
- Modified_date updates
- No data loss

---

#### Test 10: Remove Book (Phase 6)
**Objective:** Delete book from library

```bash
# Remove with file deletion
candlekeep remove 1

# Should show:
# - Book details
# - Confirmation prompt
# - Success message after confirmation

# Verify deletion
candlekeep list
ls ~/.candlekeep/library/
mysql -u <user> -p -e "USE candlekeep; SELECT COUNT(*) FROM books;"

# Test with --keep-files flag
candlekeep add-pdf ~/Downloads/test.pdf
candlekeep remove <new-id> --keep-files
# Verify file still exists but DB record removed
```

**Expected Results:**
- Confirmation prompt shows correct book
- Database record removed
- Files deleted (or kept with flag)
- No orphaned records
- Clean error if book doesn't exist

---

#### Test 11: Error Handling (Phase 7)
**Objective:** Graceful error handling for all scenarios

```bash
# File not found
candlekeep add-pdf /nonexistent/file.pdf

# Invalid file format
candlekeep add-pdf ~/Downloads/image.png

# Database connection error (stop MySQL)
sudo systemctl stop mysql
candlekeep list

# Invalid book ID
candlekeep show 9999
candlekeep update 9999 --title "Test"
candlekeep remove 9999

# Missing required arguments
candlekeep add-pdf
candlekeep update 1

# Invalid format option
candlekeep list --format invalid
```

**Expected Results:**
- Clear error messages for each scenario
- Suggestions for fixing errors
- No stack traces (unless debug mode)
- Graceful degradation
- Exit codes appropriate for errors

---

#### Test 12: Edge Cases
**Objective:** Handle unusual but valid scenarios

```bash
# PDF with no metadata
candlekeep add-pdf ~/minimal-metadata.pdf

# Very long title/author
candlekeep add-pdf ~/long-title.pdf --title "<500 char string>"

# Special characters in metadata
candlekeep add-pdf ~/test.pdf --title "Clean Code: A & B → C" --author "Martin, Robert C."

# Empty markdown file
echo "" > ~/empty.md
candlekeep add-md ~/empty.md

# Large PDF (>100MB)
candlekeep add-pdf ~/large-book.pdf

# Filename with spaces and special chars
candlekeep add-pdf "~/My Books/Clean Code - Robert C. Martin (2008).pdf"
```

**Expected Results:**
- Handles missing metadata gracefully
- Truncates or handles long strings
- Escapes special characters correctly
- Provides warnings for empty files
- Shows progress for large files
- Handles filename edge cases

---

### Test Execution Checklist

Before marking task as complete, ALL tests must pass:

- [x] Test 1: Initial Setup ✓ **PASSED** (Phase 1)
- [x] Test 2: Add PDF Book ✓ **PASSED** (Phase 2)
- [x] Test 3: Add Markdown Book ✓ **PASSED** (Phase 3)
- [x] Test 4: Duplicate Detection ✓ **PASSED** (Phase 2)
- [ ] Test 5: List Books ✓ (Phase 5)
- [ ] Test 6: Show Book Details ✓ (Phase 5)
- [ ] Test 7: Search Books ✓ (Phase 5)
- [ ] Test 8: Library Statistics ✓ (Phase 5)
- [ ] Test 9: Update Metadata ✓ (Phase 6)
- [ ] Test 10: Remove Book ✓ (Phase 6)
- [ ] Test 11: Error Handling ✓ (Phase 7)
- [ ] Test 12: Edge Cases ✓ (Phase 7)

### Success Criteria

**The task is complete when:**
1. All 12 E2E tests pass without errors
2. CLI commands are intuitive and user-friendly
3. Error messages are clear and helpful
4. Rich formatting is consistent and beautiful
5. Performance is acceptable (<5s for most operations)
6. Documentation is complete and accurate

## Progress Log

### 2025-11-01 - Phase 1 Complete ✅

**Implementation:**
- ✅ Created complete project structure with src/candlekeep/
- ✅ Configured UV package management with pyproject.toml
- ✅ Implemented SQLAlchemy models (Book with 24 fields, BookNote)
- ✅ Created DatabaseManager with SQLite support
- ✅ Set up Alembic migrations system
- ✅ Implemented init command with Rich UI
- ✅ Created initial migration: e5ffbf97468e_initial_schema.py

**Architecture Change:**
- Switched from MySQL to SQLite for local-first approach
- Added Alembic for database schema version control
- Zero-configuration initialization (no database prompts)

**End-to-End Testing Completed:**

✅ **Test 1.1: Fresh Initialization**
```bash
rm -rf ~/.candlekeep && candlekeep init
# Result: SUCCESS
# - Created ~/.candlekeep/ directory
# - Created library/ and originals/ subdirectories
# - Created candlekeep.db (45KB SQLite database)
# - Ran Alembic migration successfully
# - Beautiful Rich UI output displayed
```

✅ **Test 1.2: Database Schema Verification**
```bash
sqlite3 ~/.candlekeep/candlekeep.db ".tables"
# Result: SUCCESS
# Tables created: alembic_version, book_notes, books

sqlite3 ~/.candlekeep/candlekeep.db ".schema books"
# Result: SUCCESS
# - All 24 fields present (title, author, file_hash, etc.)
# - Indexes created: ix_books_title, ix_books_author, ix_books_category, ix_books_source_type
# - Unique constraint on file_hash
# - Proper data types (VARCHAR, TEXT, INTEGER, DATETIME, JSON)
```

✅ **Test 1.3: Alembic Migrations**
```bash
alembic current
# Result: e5ffbf97468e (head)

alembic downgrade -1
# Result: SUCCESS - Tables dropped

alembic upgrade head
# Result: SUCCESS - Tables recreated
```

✅ **Test 1.4: Reinitialize Handling**
```bash
echo "n" | candlekeep init
# Result: SUCCESS - Cancelled gracefully

echo "y" | candlekeep init
# Result: SUCCESS - Reinitialized without errors
```

✅ **Test 1.5: Schema Correctness**
- Book model: 24 fields verified
- BookNote model: 5 fields with foreign key
- Indexes: All 4 indexes created correctly
- Constraints: file_hash unique, foreign key with CASCADE
- Enums: SourceType (pdf/markdown), NoteType (summary/review/tag/other)

**Files Created:** 31 files, 2,281 insertions
**Branch:** feature/phase-1-foundation-sqlite
**Commit:** b3c9727
**Pull Request:** #1 - https://github.com/SaharCarmel/CandleKeep/pull/1

**Phase 1 Completion Criteria Met:**
- [x] Project structure created and organized
- [x] Dependencies installed and configured
- [x] Database models implemented
- [x] Session management working
- [x] Migrations set up and tested
- [x] Init command functional
- [x] E2E tests passed
- [x] Code committed and PR created

**Next: Phase 2 - PDF Processing**

---

### 2025-11-01 - Phase 2 Complete ✅

**Implementation:**
- ✅ Implemented SHA256 hashing utility (utils/hash_utils.py)
- ✅ Implemented PDF metadata extraction with PyMuPDF (parsers/pdf.py)
- ✅ Implemented PDF to markdown conversion with **page markers** (pymupdf4llm)
- ✅ Implemented word/chapter counting utilities
- ✅ Implemented filename parsing fallback (utils/file_utils.py)
- ✅ Created content extraction utilities (utils/content_utils.py)
- ✅ Implemented `candlekeep add-pdf` command (commands/add.py)
- ✅ Added table_of_contents JSON field to Book model
- ✅ Created migration: 350115ea15b8_add_table_of_contents_field.py

**Innovation - Page Markers:**
- PDFs now converted with page separators: `--- end of page=N ---`
- Enables surgical content extraction by page range
- AI agents can query TOC and extract precise sections
- Example: Extract pages 41-44 (1,290 words) instead of searching 82,835 words

**End-to-End Testing Completed:**

✅ **Test 2: Add PDF Book**
```bash
uv run candlekeep add-pdf ~/Downloads/volos-guide-to-monsters.pdf
# Result: SUCCESS
# - Title: "Volo's Guide to Monsters"
# - Pages: 226
# - Words: 82,835
# - Chapters: 192 TOC entries with hierarchy
# - Markdown file: ~/.candlekeep/library/volos-guide-to-monsters.md
# - Database record created with all metadata
# - TOC stored as JSON in database
# - Page markers inserted correctly (226 pages)
```

✅ **Test 4: Duplicate Detection**
```bash
uv run candlekeep add-pdf ~/Downloads/volos-guide-to-monsters.pdf
# Result: SUCCESS
# Error message: "Book already exists: Volo's Guide to Monsters (ID: 1)"
# - SHA256 hash correctly identifies duplicate
# - No database changes
# - No file creation
```

✅ **Page Extraction Test (Content Utils)**
```python
# Query: "Tell me about goblins"
# Search TOC for "Goblins" → Found at index 17, page 41
# Next TOC entry at page 45 → Extract pages 41-44
# Result: 7,742 characters (~1,290 words) of precise content
# Extraction time: <50ms using regex
```

**Architecture Enhancement:**
- Table of Contents now stored in database as JSON
- Enables AI agents to query TOC without reading markdown files
- Page markers enable O(1) content extraction via regex
- Duplicate detection prevents re-adding books via SHA256 hash

**Files Created:** 7 new files, 797 lines of code
**Branch:** feature/phase-2-pdf-processing-with-page-markers
**Commit:** 4ef00b9
**Pull Request:** #2 - https://github.com/SaharCarmel/CandleKeep/pull/2

**Phase 2 Completion Criteria Met:**
- [x] SHA256 hashing implemented and tested
- [x] PDF metadata extraction working (title, author, TOC, etc.)
- [x] PDF to markdown conversion with page markers
- [x] Word and chapter counting accurate
- [x] Filename parsing fallback functional
- [x] Complete PDF parser module integrated
- [x] E2E tests 2 & 4 passed
- [x] add-pdf command implemented with rich UI
- [x] Progress indicators for long operations
- [x] Duplicate detection working
- [x] Code committed and PR created

**Next: Phase 3 - Markdown Processing**

---

### 2025-11-06 - Phase 3 Complete ✅

**Implementation:**
- ✅ Implemented YAML frontmatter parsing (python-frontmatter library)
- ✅ Implemented first heading extraction fallback
- ✅ Implemented word counting for markdown
- ✅ Reused filename parsing from utils/file_utils.py
- ✅ Created complete markdown parser module (parsers/markdown.py)
- ✅ Implemented `candlekeep add-md` command (commands/add.py)
- ✅ Progress indicators matching add-pdf command

**Metadata Extraction Strategy:**
1. **YAML Frontmatter** (priority 1): title, author, subject, keywords, category, tags, isbn, publisher, publication_year, language
2. **First Heading** (fallback for title): Extract from first `#` heading
3. **Filename Parsing** (fallback): Uses existing parse_filename_metadata()
4. **TOC Generation**: From frontmatter OR generated from markdown headings (##, ###, etc.)

**End-to-End Testing Completed:**

✅ **Test 3: Add Markdown Book**
```bash
uv run candlekeep add-md ~/test-book.md
# Result: SUCCESS
# - Title: "My Coding Philosophy" (from frontmatter)
# - Author: "Sahar Carmel" (from frontmatter)
# - Category: "Technical Writing" (from frontmatter)
# - Tags: ["coding", "philosophy", "practices"] (from frontmatter)
# - Words: 99
# - Chapters: 2 (from ## headings)
# - Markdown file: ~/.candlekeep/library/my-coding-philosophy.md
# - Database record created with all metadata
```

✅ **Edge Case Testing:**
- **Without Frontmatter**: Title extracted from first `#` heading ✓
- **With Special Characters**: Works with proper YAML quoting (colons require quotes) ✓
- **Minimal Metadata**: Fallback strategies working correctly ✓

**Architecture Consistency:**
- Markdown parser follows same pattern as PDF parser (context manager)
- Same metadata dictionary structure for consistency
- TOC format matches PDF parser (level, title, page)
- Same Rich UI formatting for success messages
- Tags stored as JSON list in database (both formats)

**Files Verified:** parsers/markdown.py (331 lines), commands/add.py includes add-md
**Branch:** feature/phase-3-markdown-processing-with-toc
**Commit:** 39e31ba

**Phase 3 Completion Criteria Met:**
- [x] Frontmatter parsing implemented and tested
- [x] Heading extraction fallback working
- [x] Word counting accurate
- [x] Filename parsing reused from utils
- [x] Complete markdown parser module
- [x] E2E Test 3 passed
- [x] add-md command functional with rich UI
- [x] Edge cases tested (no frontmatter, special chars)
- [x] Progress tracking updated

**Next: Phase 5 - Query Commands** (Phase 4 is complete with add-pdf and add-md)
