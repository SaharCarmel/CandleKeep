# D&D Dungeon Master Plugin

A comprehensive D&D 5e Dungeon Master assistant for Claude Code that provides immersive gameplay features including campaign management, dice rolling, and AI-powered NPC voices.

## Features

### Core DM Tools
- **Adventure Book Integration**: Query D&D adventure modules stored in CandleKeep
- **Dice Rolling**: CLI-based dice roller for all game mechanics
- **Campaign Management**: Track sessions, character progression, and story arcs
- **Two Game Modes**: Adventure Mode (immersive) or Debug Mode (transparent)

### NPC Voice Acting
- **AI Text-to-Speech**: Bring NPCs to life with ElevenLabs AI voices
- **Multiple Voice Presets**: Goblins, wizards, villains, merchants, and more
- **Fast Generation**: Uses ElevenLabs `eleven_flash_v2_5` for real-time gameplay
- **Narrator Mode**: Voice scene descriptions and storytelling

## Quick Start

### Basic Setup

1. Install the plugin through the Claude Code marketplace
2. Load your D&D adventure books in CandleKeep
3. Use the `/dm-prepare` command to start or resume a campaign
4. Begin your adventure!

### Optional: NPC Voice Setup

To enable text-to-speech for NPC voices:

1. **Get an API Key**:
   - Sign up at [ElevenLabs](https://elevenlabs.io)
   - Navigate to Settings → API Keys
   - Copy your API key

2. **Configure the Plugin**:
   ```bash
   cd plugins/dnd-dm/skills/npc-voice
   cp .env.example .env
   ```

3. **Add Your API Key**:
   Edit `.env` and replace `your_api_key_here` with your actual API key:
   ```
   ELEVENLABS_API_KEY=sk_your_actual_key_here
   ```

4. **Install Dependencies**:
   ```bash
   npm install
   ```

5. **Test It**:
   ```bash
   node speak-npc.js --text "Welcome, brave adventurer!" --voice wizard --npc "Gandalf"
   ```

## Skills Included

### 1. DND-DM Skill
The main Dungeon Master skill that integrates with CandleKeep for adventure books and manages campaigns.

**Location**: `skills/dnd-dm/`

**Features**:
- Campaign tracking and session logs
- Character management
- Adventure book queries
- DM guidance and rules assistance

### 2. NPC-Voice Skill
Text-to-speech system for bringing NPCs and narration to life.

**Location**: `skills/npc-voice/`

**Features**:
- Multiple character voice presets
- Fast AI voice generation
- Automatic audio playback
- DM narration mode

## Using NPC Voices During Gameplay

The DM skill uses TTS **sparingly** for dramatic moments:

- First introductions of major NPCs
- Villain speeches and taunts
- Emotional reveals
- Climactic moments

### Available Voice Presets

```bash
# List all available voices
cd plugins/dnd-dm/skills/npc-voice
node speak-npc.js --list
```

**Character Types**:
- `goblin` - Sneaky, nasty creatures
- `dwarf` - Deep, gruff voices
- `elf` - Elegant, refined speech
- `wizard` - Wise, scholarly tone
- `warrior` - Gruff, commanding
- `villain` - Menacing, threatening
- `merchant` - Friendly, talkative
- `guard` - Authoritative
- `narrator` - Storytelling and scene descriptions

### Example Usage

```bash
cd plugins/dnd-dm/skills/npc-voice

# Goblin ambush
node speak-npc.js --text "You die now, pinkskin!" --voice goblin --npc "Cragmaw Scout"

# Wise wizard
node speak-npc.js --text "The path ahead is fraught with danger." --voice wizard --npc "Elminster"

# Villain monologue
node speak-npc.js --text "You fools! You've played right into my hands!" --voice villain --npc "The Black Spider"

# DM narration
node speak-npc.js --text "You enter a dimly lit tavern. The smell of ale and pipe smoke fills the air." --voice narrator
```

## Dice Roller

The built-in dice roller handles all game mechanics:

```bash
cd plugins/dnd-dm/skills/dnd-dm

# Basic rolls
./roll-dice.sh 1d20+5 --label "Attack roll"
./roll-dice.sh 2d6+3 --label "Damage"

# Advantage/Disadvantage
./roll-dice.sh 1d20+3 --advantage --label "Attack with advantage"
./roll-dice.sh 1d20 --disadvantage --label "Stealth in heavy armor"

# Hidden rolls (for DM)
./roll-dice.sh 1d20+6 --hidden --label "Enemy stealth"
```

## Game Modes

### Adventure Mode (Default)
- Immersive gameplay with hidden DM information
- Secret rolls for enemies
- Builds suspense and mystery

### Debug Mode
- All information visible (rolls, DCs, stats)
- Helpful for learning or troubleshooting
- Request with: "Let's play in debug mode"

## Campaign Management

The skill automatically tracks:
- Session logs with detailed accounts
- Character progression and XP
- Party resources (HP, spell slots, items)
- NPC relationships and quest status
- Complete campaign history

Campaign files are stored in your local skill directory.

## Commands

- `/dm-prepare` - Resume a campaign session (reads logs and prepares next content)
- `/dm-wrap-up` - End a session and save progress

## Templates

Session tracking template available in `templates/session-notes.md` for organizing your campaign notes.

## Requirements

- **Node.js**: >= 18.0.0
- **npm**: >= 9.0.0
- **Optional**: ElevenLabs API key for NPC voices
- **Recommended**: CandleKeep plugin for adventure book integration

## Troubleshooting

### TTS Not Working?

1. **Check API Key**: Verify `.env` file exists in `skills/npc-voice/` with valid key
2. **Audio Player**:
   - macOS: Uses `afplay` (built-in)
   - Linux: Install `mpg123` via package manager (`sudo apt install mpg123`)
3. **API Quota**: Check usage at [ElevenLabs Dashboard](https://elevenlabs.io)
4. **Skip It**: TTS is optional! The plugin works perfectly without it

### Dependencies Not Installed?

```bash
# For DND-DM skill
cd plugins/dnd-dm/skills/dnd-dm
npm install

# For NPC-Voice skill
cd plugins/dnd-dm/skills/npc-voice
npm install
```

### Permission Issues?

Make scripts executable:
```bash
cd plugins/dnd-dm/skills/dnd-dm
chmod +x roll-dice.sh
chmod +x speak-npc.js
```

## Plugin Structure

```
plugins/dnd-dm/
├── .claude-plugin/
│   └── plugin.json        # Plugin metadata
├── README.md              # This file
├── skills/
│   ├── dnd-dm/            # Main DM skill
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── dm-guide.md
│   │   ├── roll-dice.sh
│   │   ├── speak-npc.js
│   │   ├── package.json
│   │   └── .env.example
│   └── npc-voice/         # NPC voice skill
│       ├── SKILL.md
│       ├── README.md
│       ├── speak-npc.js
│       ├── package.json
│       └── .env.example
├── commands/
│   ├── dm-prepare.md      # Resume campaign command
│   └── dm-wrap-up.md      # End session command
└── templates/
    └── session-notes.md   # Session tracking template
```

## Tips for Great Games

1. **Read Ahead**: Know the next 2-3 encounters
2. **Take Notes**: Track NPC interactions and player decisions
3. **Use Voice Sparingly**: Save TTS for impactful moments
4. **Be Flexible**: Players will surprise you - embrace it!
5. **Have Fun**: Your enthusiasm is contagious!

## Cost Information

**ElevenLabs Pricing** (as of 2024):
- Free tier: 10,000 characters/month
- Paid tiers: Starting at $5/month for 30,000 characters
- Short NPC dialogues typically use 50-200 characters each

## Support

For issues or questions:
- Check the [Claude Code Documentation](https://docs.claude.com)
- Review individual skill README files in `skills/` directories
- Consult `dm-guide.md` for detailed DMing tips

## License

MIT

## Author

Sahar Carmel

---

**Ready to start your adventure? Just say "Let's play D&D" and begin!**
