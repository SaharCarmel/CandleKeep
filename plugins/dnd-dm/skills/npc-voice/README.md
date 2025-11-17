# NPC Voice Skill

Text-to-Speech for bringing NPCs and narration to life using ElevenLabs AI voices.

## Quick Start

```bash
# Test it out
node .claude/skills/npc-voice/speak-npc.js \
  --text "Hello, adventurer!" \
  --voice merchant \
  --npc "Shopkeeper"
```

## Installation

1. **Get API Key**: Sign up at [ElevenLabs](https://elevenlabs.io) and get your API key from [settings](https://elevenlabs.io/app/settings/api-keys)

2. **Configure**: Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add: ELEVENLABS_API_KEY=your_key_here
   ```

3. **Install Dependencies**:
   ```bash
   cd .claude/skills/npc-voice && npm install
   ```

## Usage

### Basic Command

```bash
node .claude/skills/npc-voice/speak-npc.js \
  --text "Your dialogue here" \
  --voice <preset> \
  --npc "Character Name"
```

### Voice Presets

Run `--list` to see all available voices:

```bash
node .claude/skills/npc-voice/speak-npc.js --list
```

**Popular Presets:**
- `narrator` - Storytelling, scene descriptions
- `merchant` - Friendly shopkeeper
- `villain` - Menacing antagonist
- `wizard` - Wise spellcaster
- `warrior` - Gruff fighter
- `goblin` - Sneaky creature
- `dwarf` - Deep, gruff
- `elf` - Elegant

### Examples

**D&D Session:**
```bash
# DM narration
node .claude/skills/npc-voice/speak-npc.js \
  --text "You enter a dimly lit tavern. The smell of ale and pipe smoke fills the air." \
  --voice narrator

# NPC dialogue
node .claude/skills/npc-voice/speak-npc.js \
  --text "Welcome to my shop! Looking for potions?" \
  --voice merchant \
  --npc "Albus the Alchemist"

# Villain monologue
node .claude/skills/npc-voice/speak-npc.js \
  --text "You fools! You cannot stop me now!" \
  --voice villain \
  --npc "Dark Wizard Malakar"
```

## How It Works

1. **Text Input**: You provide dialogue/narration text
2. **Voice Selection**: Choose from preset character voices
3. **AI Generation**: ElevenLabs generates natural-sounding speech
4. **Auto-Play**: Audio plays automatically through your system
5. **Cleanup**: Temporary files are removed

## Technical Details

- **Model**: ElevenLabs eleven_flash_v2_5
- **Audio Format**: MP3, 44.1kHz, 128kbps
- **Audio Player**:
  - macOS: `afplay`
  - Linux: `mpg123`
- **Dependencies**:
  - `@elevenlabs/elevenlabs-js`
  - `dotenv`

## Use Cases

- **D&D/TTRPG**: Voice NPCs and narrate scenes
- **Storytelling**: Read passages from books with character voices
- **Content Creation**: Generate voiceovers for videos/podcasts
- **Accessibility**: Convert text to speech for easier consumption
- **Game Development**: Prototype character voices

## Files

- `speak-npc.js` - Main TTS script
- `skill.md` - Skill documentation for Claude
- `package.json` - Node.js dependencies
- `.env.example` - Environment variable template
- `.env` - Your API key (git-ignored)

## Troubleshooting

**"API key not configured"**
- Make sure `.env` file exists with valid `ELEVENLABS_API_KEY`

**"Audio player exited with code 1"**
- macOS: `afplay` should work by default
- Linux: Install `mpg123` with `sudo apt install mpg123`

**"401 Unauthorized"**
- Check your API key is correct and active
- Verify you have credits remaining in your ElevenLabs account

## Cost

ElevenLabs pricing (as of 2024):
- Free tier: 10,000 characters/month
- Paid tiers: Starting at $5/month for 30,000 characters

Short NPC dialogues typically use 50-200 characters each.

---

**Created by**: Sahar Carmel
**License**: MIT
**ElevenLabs**: https://elevenlabs.io
