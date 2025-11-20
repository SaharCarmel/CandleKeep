---
name: npc-voice
description: Generate AI-powered voice acting for D&D NPCs using ElevenLabs TTS. Brings characters to life with distinct voices for important moments and memorable NPCs.
---

# NPC Voice Text-to-Speech Skill

Use ElevenLabs AI voices to bring NPCs and narration to life with realistic speech synthesis.

## When to Use

Use this skill **sparingly** for maximum dramatic impact:

- **Important NPC introductions**: First time meeting a major NPC
- **Dramatic moments**: Villain speeches, emotional reveals, climactic scenes
- **Recurring NPCs**: Builds consistency and player attachment
- **Boss taunts**: Makes combat more memorable
- **Scene narration**: Add atmosphere to key story moments

**Don't overuse it** - save it for special moments so it remains impactful!

## Setup Requirements

**First-time setup:**
1. Get an API key from [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) (free tier available)
2. Create `.env` file in this skill directory:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   cd .claude/skills/npc-voice && npm install
   ```

**If no API key is configured**, simply skip using this tool - the dnd-dm skill works perfectly without it!

## Usage

```bash
# Basic usage - speak as an NPC
node .claude/skills/npc-voice/speak-npc.js \
  --text "Welcome to my shop, traveler!" \
  --voice merchant \
  --npc "Elmar Barthen"

# Villain monologue
node .claude/skills/npc-voice/speak-npc.js \
  --text "You dare challenge me? Foolish mortals!" \
  --voice villain \
  --npc "Dark Lord Karzoth"

# Scene narration
node .claude/skills/npc-voice/speak-npc.js \
  --text "The ancient door creaks open, revealing a dark corridor..." \
  --voice narrator

# List all available voices
node .claude/skills/npc-voice/speak-npc.js --list
```

## Available Voice Presets

**Fantasy Character Types:**
- `goblin` - Sneaky, nasty creatures
- `dwarf` - Deep, gruff voices
- `elf` - Elegant, refined speech
- `wizard` - Wise, scholarly tone
- `warrior` - Gruff, commanding
- `rogue` - Sneaky, sly
- `cleric` - Gentle, compassionate

**NPC Archetypes:**
- `merchant` - Friendly, talkative
- `guard` - Authoritative
- `noble` - Refined, aristocratic
- `villain` - Menacing, threatening

**General:**
- `narrator` - Storytelling and scene descriptions
- `default` - Neutral male voice

**Age/Gender:**
- `oldman` - Elderly male
- `youngman` - Young male
- `woman` - Female
- `girl` - Young female

## Example in Gameplay

```
DM: As you enter the cave, a hulking bugbear emerges from the shadows.

[Use TTS for dramatic effect:]
node .claude/skills/npc-voice/speak-npc.js \
  --text "You dare enter Klarg's lair? Your bones will join the others!" \
  --voice villain \
  --npc "Klarg"

The gravelly voice echoes through the cavern, sending a chill down your spine.
What do you do?
```

## Technical Details

- Uses ElevenLabs TTS API (eleven_flash_v2_5 model for speed)
- Generates high-quality MP3 audio (44.1kHz, 128kbps)
- Auto-plays using system audio player:
  - macOS: `afplay` (built-in)
  - Linux: `mpg123` (install via package manager)
- Temporary files are cleaned up automatically

## Troubleshooting

If TTS doesn't work:
1. Check that `.env` file exists with valid API key
2. Verify audio player is available on your system
3. Check ElevenLabs API quota at https://elevenlabs.io
4. **Remember: TTS is optional!** The dnd-dm skill works fine without it

## Cost Information

**ElevenLabs Pricing** (as of 2024):
- Free tier: 10,000 characters/month
- Paid tiers: Starting at $5/month for 30,000 characters
- Short NPC dialogues typically use 50-200 characters each

---

**Ready to bring your NPCs to life with voice acting!**
