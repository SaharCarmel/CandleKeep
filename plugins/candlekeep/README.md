# CandleKeep Plugin

Personal knowledge base system for Claude Code that gives AI agents direct access to your books.

## What is this?

A Claude Code plugin that provides a skill for querying your personal book library. CandleKeep treats books as source material you can reference with precise page citations, enabling AI agents to provide responses grounded in your actual knowledge collection.

## Features

- **PDF & Markdown Support**: Add books in PDF or Markdown format
- **Table of Contents Navigation**: Query book structure to find relevant sections
- **Precise Page Extraction**: Extract specific page ranges with page markers
- **Local-First Storage**: All data stored in `~/.candlekeep/` (SQLite database)
- **Token-Efficient Workflow**: Progressive disclosure pattern (list → TOC → pages)
- **Privacy-Focused**: No external data transmission, all processing local

## Installation

### Prerequisites
- Python 3.10+
- UV package manager ([install here](https://github.com/astral-sh/uv))

### Install Steps

1. **Install plugin via marketplace**
   ```bash
   # Plugin will be installed to ~/.claude/skills/candlekeep
   ```

2. **Initialize CandleKeep**
   ```bash
   cd ~/.claude/skills/candlekeep
   uv sync
   uv run candlekeep init
   ```

3. **Add your first book**
   ```bash
   uv run candlekeep add-pdf ~/Books/my-book.pdf
   # or
   uv run candlekeep add-md ~/Books/my-book.md
   ```

## Commands

All commands run from `~/.claude/skills/candlekeep/`:

### Initialize (First Time Only)
```bash
uv run candlekeep init
```

### List Books
```bash
uv run candlekeep list
```

### Get Table of Contents
```bash
uv run candlekeep toc <book-id>
```

### Extract Pages
```bash
uv run candlekeep pages <book-id> <start-page> <end-page>
```

### Add Books
```bash
uv run candlekeep add-pdf /path/to/book.pdf
uv run candlekeep add-md /path/to/book.md
```

## Usage with Claude

When you ask Claude questions that could be answered from your book library, Claude will:

1. **List** available books
2. **Check TOC** to find relevant sections
3. **Extract pages** with precise content
4. **Cite sources** with book title and page numbers

**Example:**
```
You: "What does Clean Code say about naming variables?"

Claude:
1. Lists your books, finds "Clean Code"
2. Checks TOC, identifies Chapter 2 about names
3. Extracts pages 18-25
4. Answers: "According to Clean Code (pages 18-25), meaningful names should..."
```

## Progressive Disclosure Workflow

This token-efficient pattern minimizes context usage:

1. **List** → See what books are available
2. **TOC** → Navigate to relevant sections
3. **Pages** → Extract only what you need

Instead of loading an entire 300-page book, you extract just the 3-5 pages needed to answer the question.

## Data Storage

```
~/.candlekeep/
├── candlekeep.db       # SQLite database (metadata only)
├── library/            # Converted markdown files
│   └── book-slug/
│       └── content.md  # With page markers
└── originals/          # Original PDF/MD files (optional)
```

## Current Status

**Version**: 0.1.0 (Early Development)

### What Works
- ✅ PDF and Markdown book imports
- ✅ Page marker system for precise extraction
- ✅ Table of contents extraction and storage
- ✅ SQLite database with duplicate detection
- ✅ Metadata extraction from PDFs
- ✅ YAML frontmatter parsing for markdown books

### Planned Features
- ⏳ Full-text search across library
- ⏳ Note-taking and annotations
- ⏳ Session tracking
- ⏳ Connection mapping (knowledge patterns)

## Developer Setup

For local plugin development:

```bash
# Clone the marketplace repository
git clone https://github.com/SaharCarmel/CandleKeep.git
cd CandleKeep

# Symlink to Claude skills directory
ln -s $(pwd)/plugins/candlekeep/skills/candlekeep ~/.claude/skills/candlekeep

# Install dependencies
cd ~/.claude/skills/candlekeep
uv sync

# Initialize
uv run candlekeep init

# Add a test book
uv run candlekeep add-pdf ~/test.pdf
```

## Dependencies

This plugin is required by:
- **DND-DM plugin** - Uses CandleKeep to access D&D adventure books and rulebooks

## Troubleshooting

### "Candlekeep not initialized"
```bash
cd ~/.claude/skills/candlekeep && uv run candlekeep init
```

### "UV not found"
Install UV package manager: https://github.com/astral-sh/uv

### "Python version error"
Requires Python 3.10 or higher

### "Book ID not found"
Run `uv run candlekeep list` to see valid book IDs

## License

MIT

## Support

- GitHub Issues: https://github.com/SaharCarmel/CandleKeep/issues
- Documentation: See SKILL.md for detailed agent usage guide
