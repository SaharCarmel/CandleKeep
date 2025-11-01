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

**Overall Status:** Not Started - 0% Complete

### Subtasks
| ID | Description | Status | Updated | Notes |
|----|-------------|--------|---------|-------|
| 1.1 | Create project structure | Not Started | 2025-11-01 | src/candlekeep with subdirectories |
| 1.2 | Set up pyproject.toml | Not Started | 2025-11-01 | All dependencies configured |
| 1.3 | Create SQLAlchemy models | Not Started | 2025-11-01 | books and book_notes tables |
| 1.4 | Create database session management | Not Started | 2025-11-01 | Connection pooling, session factory |
| 1.5 | Implement configuration management | Not Started | 2025-11-01 | Read/write config.yaml |
| 1.6 | Implement init command | Not Started | 2025-11-01 | Full setup workflow |
| 1.7 | Test init command | Not Started | 2025-11-01 | E2E test |
| 2.1 | Implement SHA256 hashing | Not Started | 2025-11-01 | File deduplication |
| 2.2 | Implement PDF metadata extraction | Not Started | 2025-11-01 | PyMuPDF extraction |
| 2.3 | Implement PDF to markdown conversion | Not Started | 2025-11-01 | pymupdf4llm |
| 2.4 | Implement word/chapter counting | Not Started | 2025-11-01 | Content metrics |
| 2.5 | Implement filename parsing | Not Started | 2025-11-01 | Fallback extraction |
| 2.6 | Create PDF parser module | Not Started | 2025-11-01 | Complete integration |
| 2.7 | Test PDF parsing | Not Started | 2025-11-01 | E2E test |
| 3.1 | Implement frontmatter parsing | Not Started | 2025-11-01 | python-frontmatter |
| 3.2 | Implement heading extraction | Not Started | 2025-11-01 | Fallback method |
| 3.3 | Implement word/heading counting | Not Started | 2025-11-01 | Content metrics |
| 3.4 | Implement filename parsing | Not Started | 2025-11-01 | Fallback extraction |
| 3.5 | Create markdown parser module | Not Started | 2025-11-01 | Complete integration |
| 3.6 | Test markdown parsing | Not Started | 2025-11-01 | E2E test |
| 4.1 | Implement add-pdf command | Not Started | 2025-11-01 | Full workflow |
| 4.2 | Implement add-md command | Not Started | 2025-11-01 | Full workflow |
| 4.3 | Test add commands | Not Started | 2025-11-01 | E2E test |
| 5.1 | Implement list command | Not Started | 2025-11-01 | With filters and formats |
| 5.2 | Implement show command | Not Started | 2025-11-01 | Rich formatting |
| 5.3 | Implement search command | Not Started | 2025-11-01 | Full-text search |
| 5.4 | Implement stats command | Not Started | 2025-11-01 | Library statistics |
| 5.5 | Test query commands | Not Started | 2025-11-01 | E2E test |
| 6.1 | Implement update command | Not Started | 2025-11-01 | Metadata updates |
| 6.2 | Implement remove command | Not Started | 2025-11-01 | With confirmation |
| 6.3 | Test management commands | Not Started | 2025-11-01 | E2E test |
| 7.1 | Add error handling | Not Started | 2025-11-01 | Comprehensive coverage |
| 7.2 | Add progress indicators | Not Started | 2025-11-01 | For long operations |
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

- [ ] Test 1: Initial Setup ✓
- [ ] Test 2: Add PDF Book ✓
- [ ] Test 3: Add Markdown Book ✓
- [ ] Test 4: Duplicate Detection ✓
- [ ] Test 5: List Books ✓
- [ ] Test 6: Show Book Details ✓
- [ ] Test 7: Search Books ✓
- [ ] Test 8: Library Statistics ✓
- [ ] Test 9: Update Metadata ✓
- [ ] Test 10: Remove Book ✓
- [ ] Test 11: Error Handling ✓
- [ ] Test 12: Edge Cases ✓

### Success Criteria

**The task is complete when:**
1. All 12 E2E tests pass without errors
2. CLI commands are intuitive and user-friendly
3. Error messages are clear and helpful
4. Rich formatting is consistent and beautiful
5. Performance is acceptable (<5s for most operations)
6. Documentation is complete and accurate

## Progress Log

### 2025-11-01
- Task created with comprehensive context and testing plan
- Research completed on CLI frameworks, PDF parsing, and MySQL libraries
- Architecture and implementation plan defined
- End-to-end testing strategy documented
