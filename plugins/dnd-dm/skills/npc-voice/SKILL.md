---
name: npc-voice
description: Use ElevenLabs AI voices to bring NPCs and narration to life with realistic speech synthesis for D&D sessions, storytelling, and character voices
---

# NPC Voice - Text-to-Speech for Characters

Use ElevenLabs AI voices to bring NPCs and narration to life with realistic speech synthesis.

## Usage

When you need to speak dialogue as an NPC or read narration aloud, use this skill's speak-npc.js tool.

### Examples

```bash
# Speak as an NPC with character voice
node .claude/skills/npc-voice/speak-npc.js \
  --text "Welcome to my shop, traveler!" \
  --voice merchant \
  --npc "Elmar Barthen"

# Narrate scene description
node .claude/skills/npc-voice/speak-npc.js \
  --text "The ancient door creaks open, revealing a dark corridor..." \
  --voice narrator

# Villain monologue
node .claude/skills/npc-voice/speak-npc.js \
  --text "You dare challenge me? Foolish mortals!" \
  --voice villain \
  --npc "Dark Lord Karzoth"
```

## Available Voice Presets

**Default:**
- `default` - Neutral male voice
- `narrator` - Calm, storytelling voice

**Fantasy Archetypes:**
- `goblin` - Sneaky, nasty
- `dwarf` - Deep, gruff male
- `elf` - Elegant female
- `wizard` - Wise male
- `warrior` - Gruff male
- `rogue` - Sneaky
- `cleric` - Gentle female

**NPCs:**
- `merchant` - Friendly
- `guard` - Authoritative
- `noble` - Refined
- `villain` - Menacing

**Age/Gender:**
- `oldman` - Elderly male
- `youngman` - Young male
- `woman` - Female
- `girl` - Young female

## Setup

1. Get ElevenLabs API key from: https://elevenlabs.io/app/settings/api-keys
2. Create `.env` file in this skill directory:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```
3. The first time you use it, run:
   ```bash
   cd .claude/skills/npc-voice && npm install
   ```

## Command Reference

```bash
# List all available voices
node .claude/skills/npc-voice/speak-npc.js --list

# Get help
node .claude/skills/npc-voice/speak-npc.js --help

# Speak with specific voice
node .claude/skills/npc-voice/speak-npc.js \
  --text "<dialogue>" \
  --voice <preset> \
  --npc "<NPC Name>"
```

## When to Use

- **D&D Sessions**: Speak NPC dialogue, read scene descriptions
- **Storytelling**: Narrate events, read passages from books
- **Character Voices**: Give each NPC a distinct voice
- **Immersion**: Bring your games and stories to life

## Technical Details

- Uses ElevenLabs TTS API (eleven_flash_v2_5 model)
- Generates high-quality MP3 audio (44.1kHz, 128kbps)
- Auto-plays using system audio player (afplay on macOS, mpg123 on Linux)
- Temporary files are cleaned up automatically
