---
name: candlekeep
description: Access a personal knowledge base of books to answer questions with actual source material rather than relying solely on training memory
---

# Candlekeep: Your Personal Library for AI Agents

Candlekeep is a knowledge base system that gives you direct access to books stored locally. Named after the legendary library fortress in D&D lore, it allows you to query actual book content rather than relying only on training data.

## Core Philosophy

**Books as Context, Not Data** - Candlekeep treats books as source material you can reference, maintaining precise page citations and table of contents navigation. This enables you to provide responses grounded in specific texts from the user's personal library.

## When to Use Candlekeep

Use Candlekeep when:
- User asks questions that could be answered from their book collection
- Research tasks require referencing specific documentation or books
- User mentions wanting to "check the book" or "look something up"
- User explicitly asks to search or query their knowledge base
- A task would benefit from grounded, citable source material

## Available Commands

All commands use `uv run candlekeep` from the skill directory.

### 1. Initialize (First Time Only)
```bash
cd ~/.claude/skills/candlekeep
uv run candlekeep init
```
Creates `~/.candlekeep/` directory with database and configuration.

### 2. List Books
```bash
uv run candlekeep list
```
Returns all books with metadata: ID, title, author, page count, tags, format.

**Output Format:**
```
Books in library:
ID: 1
Title: The Pragmatic Programmer
Author: David Thomas, Andrew Hunt
Pages: 352
Format: pdf
Tags: programming, software-engineering
```

### 3. Get Table of Contents
```bash
uv run candlekeep toc <book-id>
```
Returns hierarchical TOC for navigation.

**Example:**
```bash
uv run candlekeep toc 1
```

### 4. Extract Pages
```bash
uv run candlekeep pages <book-id> <start-page> <end-page>
```
Extracts content from specific page range.

**Example:**
```bash
uv run candlekeep pages 1 45 47
```

Returns markdown with page markers:
```
--- end of page=45 ---
[Content from page 45]
--- end of page=46 ---
[Content from page 46]
```

### 5. Add PDF Book
```bash
uv run candlekeep add-pdf /path/to/book.pdf
```
Converts PDF to markdown with page markers and stores in library.

### 6. Add Markdown Book
```bash
uv run candlekeep add-md /path/to/book.md
```
Adds markdown book with YAML frontmatter for metadata.

## Usage Patterns

### Progressive Disclosure Workflow

Follow this token-efficient pattern:

1. **List** → Get all available books
2. **TOC** → Find relevant sections
3. **Pages** → Extract specific content

**Example Session:**
```bash
# Step 1: See what books are available
uv run candlekeep list

# Step 2: Get TOC to find relevant chapter
uv run candlekeep toc 1

# Step 3: Extract specific pages based on TOC
uv run candlekeep pages 1 45 52
```

### Token Efficiency Guidelines

- **Don't extract entire books** - Use TOC to identify relevant sections first
- **Request small page ranges** - Start with 3-5 pages, expand if needed
- **Cache TOC information** - Remember book structure within conversation
- **Use list sparingly** - Only re-list if user adds new books

### Citing Sources

When providing answers from Candlekeep:
- Always cite the book title and page numbers
- Example: "According to *The Pragmatic Programmer* (pages 45-47), ..."
- Maintain academic rigor by grounding responses in actual text

## Error Handling

### Common Issues

**"Candlekeep not initialized"**
```bash
cd ~/.claude/skills/candlekeep && uv run candlekeep init
```

**"Book ID not found"**
- Run `uv run candlekeep list` to see valid IDs

**"UV not found"**
- User needs to install UV package manager: https://github.com/astral-sh/uv

**"Python version error"**
- Requires Python 3.10+

## Installation & Setup

### First-Time Setup
```bash
# 1. Install Python dependencies
cd ~/.claude/skills/candlekeep
uv sync

# 2. Initialize Candlekeep
uv run candlekeep init

# 3. Add your first book
uv run candlekeep add-pdf ~/Books/my-book.pdf
```

### Dependencies
- Python 3.10+
- UV package manager
- PyMuPDF (installed via uv sync)
- SQLite (included with Python)

## Current Limitations

Candlekeep is in early development (Phase 2 complete):
- ✅ PDF and Markdown support with page markers
- ✅ Metadata extraction and TOC storage
- ✅ SQLite database with deduplication
- ⏳ Full-text search (not yet implemented)
- ⏳ Note-taking features (not yet implemented)
- ⏳ Session tracking (not yet implemented)

## Best Practices

1. **Check initialization first** - Before any operation, verify Candlekeep is initialized
2. **Progressive queries** - List → TOC → Pages
3. **Small page ranges** - Extract only what you need
4. **Cite sources** - Always reference book and pages
5. **Handle errors gracefully** - Provide actionable error messages to user
6. **Respect privacy** - All data is local-first, never transmitted

## Working Directory

All commands should be executed from:
```
~/.claude/skills/candlekeep/
```

The Candlekeep data directory is:
```
~/.candlekeep/
├── config.yaml          # Configuration
├── candlekeep.db       # SQLite database
├── library/            # Converted markdown files
└── originals/          # Original PDF/MD files (optional)
```

## Example Interaction

**User:** "Can you check if I have any books on software testing?"

**You:**
```bash
cd ~/.claude/skills/candlekeep && uv run candlekeep list
```

If books found, examine TOC:
```bash
uv run candlekeep toc 3
```

Extract relevant section:
```bash
uv run candlekeep pages 3 120 125
```

Provide answer with citation:
"Based on *Software Testing Fundamentals* (pages 120-125), here are the key principles..."
