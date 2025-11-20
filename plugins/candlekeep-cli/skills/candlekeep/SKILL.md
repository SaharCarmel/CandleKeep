---
name: candlekeep
description: Personal knowledge base that provides AI agents direct access to books. Use when answering questions that could benefit from book knowledge, when users ask about topics covered in their library, when providing coding/technical guidance that books might inform, or when users explicitly request book references. Proactively check the library when book knowledge might improve response quality.
---

# CandleKeep - Personal Library for AI Agents

CandleKeep gives you direct access to a user's personal book library. Like having a research assistant who can instantly reference any book, chapter, or page the user owns.

## Core Philosophy

**Check books first when knowledge might help.** If the user asks about a topic that books commonly cover—coding patterns, investment strategies, system design, domain expertise—check their library before relying solely on training knowledge.

Books in the user's library represent their chosen knowledge sources. Prefer book content over training memory when available.

## Workflow Decision Tree

```
User request
    │
    ├─► "Add this PDF/book"
    │   └─► Use add-pdf or add-md command
    │
    ├─► Question that might be answered by books
    │   ├─► 1. Check if CandleKeep is initialized
    │   ├─► 2. List available books (candlekeep list)
    │   ├─► 3. If relevant book exists:
    │   │   ├─► Get table of contents (candlekeep toc)
    │   │   └─► Extract specific pages (candlekeep pages)
    │   └─► 4. Answer using book content + cite source
    │
    └─► General request
        └─► Proceed normally, mention books if relevant
```

## Initialization Check

Before using CandleKeep, verify it's initialized:

```bash
# Check if initialized (look for ~/.candlekeep directory)
ls -la ~/.candlekeep

# If not initialized, run:
cd <plugin-directory> && uv run candlekeep init
```

**Initialization creates:**
- `~/.candlekeep/` - Main directory
- `~/.candlekeep/candlekeep.db` - SQLite database (metadata only)
- `~/.candlekeep/library/` - Markdown files (book content)
- `~/.candlekeep/originals/` - Original PDF/markdown files

## Command Reference

All commands require CandleKeep CLI. The plugin should install this automatically. Commands are run with `uv run candlekeep` from the plugin directory.

### 1. List Books (`list`)

See what books are available in the library.

```bash
# Basic list (essential metadata)
cd <plugin-directory> && uv run candlekeep list

# Full metadata
cd <plugin-directory> && uv run candlekeep list --full

# Specific fields
cd <plugin-directory> && uv run candlekeep list --fields category,tags
```

**Output format** (optimized for LLM consumption):
```markdown
# Library Books (Total: 3)

## Book ID: 1
Title: Clean Code
Author: Robert C. Martin
Type: pdf
Pages: 464
Added: 2024-11-20 10:30:00

## Book ID: 2
Title: Designing Data-Intensive Applications
Author: Martin Kleppmann
Type: pdf
Pages: 616
Added: 2024-11-19 15:45:00
```

**Use when:**
- User asks "what books do I have?"
- Checking if a topic is covered before answering
- Starting a session with book-related work

### 2. Get Table of Contents (`toc`)

View book structure to find relevant sections.

```bash
cd <plugin-directory> && uv run candlekeep toc <book-id>
```

**Example:**
```bash
cd <plugin-directory> && uv run candlekeep toc 1
```

**Output format:**
```markdown
## Table of Contents - Book ID: 1
Title: Clean Code

Clean Code (Page 1)
  Chapter 1: Clean Code (Page 7)
  Chapter 2: Meaningful Names (Page 17)
    Rules for Naming (Page 18)
    Use Intention-Revealing Names (Page 18)
  Chapter 3: Functions (Page 31)
```

**Use when:**
- Need to find where a topic is covered
- User asks "what does [book] say about [topic]?"
- Planning which pages to extract

### 3. Get Pages (`pages`)

Extract specific pages or ranges from a book.

```bash
cd <plugin-directory> && uv run candlekeep pages <book-id> --pages "<range>"
```

**Page range formats:**
- Single pages: `"1,5,10"`
- Ranges: `"1-5"` (pages 1 through 5)
- Mixed: `"1-5,10,15-20"` (pages 1-5, 10, and 15-20)

**Examples:**
```bash
# Get pages 17-31 (Chapter 2 of Clean Code)
cd <plugin-directory> && uv run candlekeep pages 1 --pages "17-31"

# Get specific pages
cd <plugin-directory> && uv run candlekeep pages 2 --pages "1,10,50-55"
```

**Output format:**
```markdown
## Book ID: 1 - Clean Code
Pages: 17-31

### Page 17
# Chapter 2: Meaningful Names
Names are everywhere in software...

### Page 18
## Use Intention-Revealing Names
The name of a variable, function, or class should answer...
```

**Use when:**
- Answering specific questions that a chapter covers
- Providing detailed guidance from book content
- User requests specific information from a known book

**Performance tip:** Extract only needed pages. A book might be 600 pages, but the relevant section is often 5-20 pages.

### 4. Add PDF Book (`add-pdf`)

Add a PDF book to the library.

```bash
cd <plugin-directory> && uv run candlekeep add-pdf <file-path> \
  [--category "category"] \
  [--tags "tag1,tag2"] \
  [--title "Custom Title"] \
  [--author "Custom Author"]
```

**Examples:**
```bash
# Basic add
cd <plugin-directory> && uv run candlekeep add-pdf ~/Downloads/clean-code.pdf

# With metadata
cd <plugin-directory> && uv run candlekeep add-pdf ~/Downloads/book.pdf \
  --category "Software Engineering" \
  --tags "coding,best-practices"
```

**Process:**
1. Computes file hash (duplicate detection)
2. Parses PDF with docling + LLM
3. Extracts metadata (title, author, TOC, page count)
4. Converts to markdown with page markers
5. Stores markdown in `~/.candlekeep/library/`
6. Stores metadata in database

**Use when:** User provides a PDF file to add to their library

### 5. Add Markdown Book (`add-md`)

Add a markdown book to the library.

```bash
cd <plugin-directory> && uv run candlekeep add-md <file-path> \
  [--category "category"] \
  [--tags "tag1,tag2"] \
  [--title "Custom Title"] \
  [--author "Custom Author"]
```

**Markdown frontmatter support:**
```markdown
---
title: My Guide to Python
author: Jane Developer
category: Programming
tags: [python, tutorial]
---

# Chapter 1
Content here...
```

**Use when:** User provides a markdown file to add (documentation, notes, agent-optimized books)

## Best Practices

### When to Query Books

**Always check books for:**
- Technical questions (coding, system design, algorithms)
- Domain expertise (finance, medicine, law, etc.)
- Methodologies and best practices
- Historical or research questions
- Specific author/book references

**Example triggers:**
- "How should I structure this React component?" → Check for React/design books
- "What's the best way to value a startup?" → Check for investing/valuation books
- "Explain CQRS pattern" → Check for architecture/design books

### Page Extraction Strategy

**Start narrow, expand if needed:**

1. **Check TOC first** to identify relevant pages
2. **Extract specific section** (e.g., pages 45-62 for one chapter)
3. **If insufficient, expand** to related chapters
4. **Avoid extracting entire book** unless specifically requested

**Example workflow:**
```bash
# 1. List books to find relevant one
cd <plugin-directory> && uv run candlekeep list

# 2. Get TOC to locate section
cd <plugin-directory> && uv run candlekeep toc 3

# 3. Extract specific pages based on TOC
cd <plugin-directory> && uv run candlekeep pages 3 --pages "120-145"
```

### Presenting Book Content

When answering with book content:

1. **Cite the source:** "According to *Clean Code* by Robert C. Martin (pages 17-19):"
2. **Synthesize, don't just quote:** Combine book knowledge with training knowledge
3. **Provide context:** Explain how the book's advice applies to their situation
4. **Reference specific pages:** This helps users verify and explore further

**Example:**
```
I checked your library and found relevant guidance in *Clean Code*
(pages 31-40). The book emphasizes that functions should:

1. Be small (ideally < 20 lines)
2. Do one thing well
3. Have descriptive names

For your React component, this means splitting `handleSubmit` into
smaller functions: `validateForm()`, `prepareData()`, and `sendRequest()`.

[Citation: Clean Code, Chapter 3: Functions, pages 31-40]
```

### Privacy and Discretion

- Books in the library represent user's personal knowledge collection
- Don't make assumptions about why they have certain books
- If a book contains personal notes/annotations (future feature), treat as private

## Technical Details

### Storage Architecture

- **Database:** SQLite at `~/.candlekeep/candlekeep.db` (metadata only)
- **Content:** Markdown files in `~/.candlekeep/library/` (actual book text)
- **Originals:** PDFs in `~/.candlekeep/originals/` (optional backup)

### Page Markers

PDFs are converted to markdown with page separators:
```markdown
Content from page 1...

--- end of page=1 ---

Content from page 2...

--- end of page=2 ---
```

This enables precise page extraction without loading entire books.

### Performance

- **Listing books:** <10ms (database query)
- **Getting TOC:** <10ms (database query, TOC stored as JSON)
- **Extracting pages:** <50ms (regex on markdown file)

**Token efficiency:** Extracting 10 pages (3,000 words) vs loading entire book (80,000 words) saves 77,000 tokens.

## Common Patterns

### Research Assistant Pattern

User working on a project with multiple relevant books:

```bash
# 1. Show available books
cd <plugin-directory> && uv run candlekeep list

# 2. For each relevant book, get TOC
cd <plugin-directory> && uv run candlekeep toc 1
cd <plugin-directory> && uv run candlekeep toc 2

# 3. Extract relevant sections from each
cd <plugin-directory> && uv run candlekeep pages 1 --pages "50-75"
cd <plugin-directory> && uv run candlekeep pages 2 --pages "120-135"

# 4. Synthesize answer using content from both books
```

### Quick Fact Check Pattern

User asks a specific question:

```bash
# 1. Check if library has relevant books
cd <plugin-directory> && uv run candlekeep list

# 2. Get TOC to verify coverage
cd <plugin-directory> && uv run candlekeep toc 3

# 3. Extract just the relevant pages (5-10 pages typically)
cd <plugin-directory> && uv run candlekeep pages 3 --pages "89-95"
```

### Library Building Pattern

User wants to add multiple books:

```bash
# Add books one at a time
cd <plugin-directory> && uv run candlekeep add-pdf ~/Downloads/book1.pdf --category "Engineering"
cd <plugin-directory> && uv run candlekeep add-pdf ~/Downloads/book2.pdf --category "Engineering"

# Verify they were added
cd <plugin-directory> && uv run candlekeep list
```

## Troubleshooting

### CandleKeep not initialized
```bash
# Initialize CandleKeep
cd <plugin-directory> && uv run candlekeep init
```

### Command not found
```bash
# Ensure you're in the plugin directory and using uv
cd <plugin-directory>
uv run candlekeep --help
```

### Book not parsing correctly
- PDF parsing uses docling + LLM - complex PDFs may take time
- If parsing fails, check PDF isn't encrypted/locked
- Markdown files should use UTF-8 encoding

### Pages not extracting
- Verify page numbers are within book's page count
- Check page range format: `"1-5"` not `1-5`
- Some books may not have page markers if added before that feature

## Summary

CandleKeep transforms how AI agents access knowledge:

- **Proactive:** Check books when they might help
- **Precise:** Extract specific pages, not entire books
- **Cited:** Always attribute information to source books
- **Efficient:** Fast queries, token-conscious extraction

Think of it as giving every AI agent access to a personal research library—making responses more informed, specific, and tailored to the user's knowledge collection.
