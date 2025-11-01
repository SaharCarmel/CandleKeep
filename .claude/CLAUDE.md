# CandleKeep - Project Configuration

## Package Management: UV

**Always use UV, not pip.**

```bash
uv sync                    # Install dependencies
uv add <package>          # Add dependency
uv run candlekeep <cmd>   # Run CLI command
```

## Testing: E2E Only

- ✅ End-to-end tests only (manual execution by Claude Code)
- ❌ No unit tests, integration tests, or test frameworks
- Tests documented in `tasks/` folder

## Development Workflow

1. `uv sync` - Install dependencies
2. Write code in `src/candlekeep/`
3. Test E2E following task file instructions
4. Update task file with results

## Project Structure

```
CandleKeep/
├── .claude/CLAUDE.md      # This file
├── tasks/                 # Task tracking with E2E test instructions
├── src/candlekeep/        # Main package
├── alembic/               # Database migrations
└── pyproject.toml         # Dependencies
```

## Quick Start

```bash
uv sync                    # Setup
uv run candlekeep init    # Initialize
```
