# CandleKeep Marketplace - Project Configuration

This repository is a Claude Code plugin marketplace hosting two plugins:
1. **CandleKeep** - Knowledge base system
2. **DND-DM** - D&D Dungeon Master assistant

---

## Repository Structure

```
CandleKeep/
├── .claude-plugin/
│   └── marketplace.json          # Plugin catalog
├── schema/
│   └── marketplace-schema.json   # Validation schema
├── scripts/
│   ├── add-plugin.sh            # Add new plugins
│   └── validate.sh              # Validate marketplace
├── plugins/
│   ├── candlekeep/              # Core knowledge base plugin
│   │   └── skills/candlekeep/   # Python CLI tool (UV managed)
│   └── dnd-dm/                  # D&D DM assistant plugin
│       └── skills/              # Node.js tools (npm managed)
├── README.md                     # Marketplace overview
├── CONTRIBUTING.md              # Contribution guidelines
└── LICENSE                       # MIT License
```

---

## Development Setup

### CandleKeep Plugin (Python)

```bash
cd plugins/candlekeep/skills/candlekeep

# Install dependencies
uv sync

# Run CLI commands
uv run candlekeep <command>

# Examples
uv run candlekeep init
uv run candlekeep list
uv run candlekeep add-pdf ~/book.pdf
```

**Package Management**: Always use UV, not pip.

### DND-DM Plugin (Node.js)

```bash
cd plugins/dnd-dm/skills/dnd-dm

# Install dependencies
npm install

# Test dice roller
./roll-dice.sh 1d20+5 --label "Test"

# Test NPC voice (requires ElevenLabs API key)
node speak-npc.js --text "Hello" --voice wizard
```

---

## Testing Plugins Locally

Symlink plugins to Claude skills directory for testing:

```bash
# From repository root
ln -s $(pwd)/plugins/candlekeep/skills/candlekeep ~/.claude/skills/candlekeep
ln -s $(pwd)/plugins/dnd-dm/skills/dnd-dm ~/.claude/skills/dnd-dm
ln -s $(pwd)/plugins/dnd-dm/skills/npc-voice ~/.claude/skills/npc-voice

# Then test in Claude Code
cd ~/.claude/skills/candlekeep && uv run candlekeep init
cd ~/.claude/skills/dnd-dm && ./roll-dice.sh 1d20
```

---

## Marketplace Management

### Validate Marketplace

```bash
./scripts/validate.sh
```

Checks:
- marketplace.json syntax
- Required fields present
- Plugin count reporting

### Add New Plugin

```bash
./scripts/add-plugin.sh
```

Interactive script that:
1. Prompts for plugin details
2. Updates marketplace.json
3. Validates structure

---

## Plugin Dependencies

**DND-DM depends on CandleKeep:**
- DND-DM calls `cd ~/.claude/skills/candlekeep && uv run candlekeep` to access adventure books
- Users must install CandleKeep before using DND-DM
- Both plugins documented as such in README

---

## Working with Python (CandleKeep)

### Adding Dependencies

```bash
cd plugins/candlekeep/skills/candlekeep
uv add <package-name>
```

### Database Migrations

```bash
cd plugins/candlekeep/skills/candlekeep

# Create migration
uv run alembic revision -m "Description"

# Apply migrations
uv run alembic upgrade head

# Check status
uv run alembic current
```

### CandleKeep Data Directory

User data stored in:
```
~/.candlekeep/
├── candlekeep.db       # SQLite database
├── library/            # Markdown books
└── originals/          # Original PDFs (optional)
```

---

## Working with Node.js (DND-DM)

### Adding Dependencies

```bash
cd plugins/dnd-dm/skills/dnd-dm
npm install <package-name>
```

### Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Add API keys
echo "ELEVENLABS_API_KEY=sk_..." >> .env
```

### DND Campaign Data

User campaign files stored in:
```
~/.claude/skills/dnd-dm/sessions/
└── campaign-name/
    ├── campaign-summary.md
    ├── campaign-log.md
    └── character-*.md
```

**Important**: This directory is gitignored (user data, not part of plugin)

---

## Git Workflow

### Marketplace Changes

```bash
# Make changes to marketplace.json or add plugins
./scripts/validate.sh

# Commit
git add .
git commit -m "Add new plugin: plugin-name"
git push
```

### Plugin Development

```bash
# Work on plugin code
cd plugins/candlekeep/skills/candlekeep
# or
cd plugins/dnd-dm/skills/dnd-dm

# Make changes...

# Test locally (via symlinks)
cd ~/.claude/skills/candlekeep && uv run candlekeep <test>

# Commit when ready
git add .
git commit -m "feat(candlekeep): Add new feature"
git push
```

### Release Process

```bash
# Update version in marketplace.json
# Update version in plugin.json files
# Update CHANGELOG if you have one

# Tag release
git tag -a v1.1.0 -m "Release v1.1.0: Description"
git push origin v1.1.0
```

---

## Common Tasks

### Test CandleKeep Plugin

```bash
cd ~/.claude/skills/candlekeep
uv sync
uv run candlekeep init
uv run candlekeep add-pdf ~/test.pdf
uv run candlekeep list
```

### Test DND-DM Plugin

```bash
cd ~/.claude/skills/dnd-dm

# Test dice roller
./roll-dice.sh 1d20+5 --label "Attack"
./roll-dice.sh 1d20 --advantage --label "With advantage"

# Test NPC voice (if API key configured)
node speak-npc.js --text "You dare enter my lair?" --voice villain --npc "Klarg"
```

### Check CandleKeep Can Access Books

```bash
cd ~/.claude/skills/candlekeep

# Initialize if needed
uv run candlekeep init

# Add a test book
uv run candlekeep add-pdf ~/DND/lost-mine-of-phandelver.pdf

# Verify
uv run candlekeep list
uv run candlekeep toc 1
uv run candlekeep pages 1 1 3
```

### Verify DND-DM Can Call CandleKeep

```bash
# This is what DND-DM does internally
cd ~/.claude/skills/candlekeep && uv run candlekeep list

# Should show books if CandleKeep is properly installed
```

---

## Troubleshooting

### "UV not found"
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Permission denied" on scripts
```bash
chmod +x scripts/*.sh
chmod +x plugins/dnd-dm/skills/dnd-dm/roll-dice.sh
```

### "Module not found" in CandleKeep
```bash
cd plugins/candlekeep/skills/candlekeep
uv sync
```

### "Node module not found" in DND-DM
```bash
cd plugins/dnd-dm/skills/dnd-dm
npm install
```

### Marketplace validation fails
```bash
# Check marketplace.json syntax
cat .claude-plugin/marketplace.json | jq .

# Run validation
./scripts/validate.sh
```

---

## Quick Reference

### CandleKeep Commands
- `uv run candlekeep init` - Initialize
- `uv run candlekeep list` - List books
- `uv run candlekeep toc <id>` - Table of contents
- `uv run candlekeep pages <id> <start> <end>` - Extract pages
- `uv run candlekeep add-pdf <file>` - Add PDF
- `uv run candlekeep add-md <file>` - Add markdown

### DND-DM Commands
- `./roll-dice.sh 1d20+5 --label "Roll"` - Roll dice
- `./roll-dice.sh 1d20 --advantage` - Roll with advantage
- `./roll-dice.sh 1d20 --hidden` - Hidden roll
- `node speak-npc.js --text "..." --voice goblin` - NPC voice

### Marketplace Commands
- `./scripts/validate.sh` - Validate marketplace
- `./scripts/add-plugin.sh` - Add new plugin

---

## Philosophy

This marketplace demonstrates:
1. **Local-First**: All user data stays on their machine
2. **Privacy-Focused**: No external data transmission (except optional ElevenLabs)
3. **Plugin Dependencies**: DND-DM depends on CandleKeep, showing inter-plugin relationships
4. **Multiple Tech Stacks**: Python (CandleKeep) + Node.js (DND-DM) coexist
5. **User Data Separation**: Plugin code vs user data clearly separated

---

For more information, see the main [README.md](../README.md).
