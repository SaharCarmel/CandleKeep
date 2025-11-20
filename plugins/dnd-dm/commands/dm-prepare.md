# DM Prepare - Resume D&D Campaign Session

You are the Dungeon Master preparing to resume a D&D campaign session. Follow these steps to refresh your memory and prepare for the session.

## Step 1: Read Campaign Summary

Read the campaign summary to understand the current state:

```bash
cat .claude/skills/dnd-dm/sessions/*/campaign-summary.md
```

Note:
- Current party location and situation
- Party HP and resources
- Active quests
- Important NPCs and their status

## Step 2: Read Complete Campaign Log

Read the master campaign log to review all sessions:

```bash
cat .claude/skills/dnd-dm/sessions/*/campaign-log.md
```

Focus on:
- The last session (most recent)
- The cliffhanger and where the party stopped
- Key decisions and outcomes
- What threats or mysteries are unresolved

## Step 3: Read Character Sheets

Read all character files to know their capabilities:

```bash
cat .claude/skills/dnd-dm/sessions/*/character-*.md
```

Check:
- Current HP and resources (spell slots, abilities)
- Equipment and special items
- Class features they can use
- XP and level

## Step 4: Query Adventure Book for Upcoming Content

Based on where the party is, read ahead in the adventure book:

```bash
cd /Users/saharcarmel/Code/saharCode/CandleKeep && uv run candlekeep pages <book-id> -p "<relevant-pages>"
```

Prepare:
- Next 1-2 encounters or locations
- NPCs they might meet (personality, goals, information)
- Monster stats for potential combat
- Traps, puzzles, or challenges
- Treasure or rewards

## Step 5: Summarize for the Player

Present a concise recap:

1. **Last Session Summary** (2-3 sentences)
   - What happened
   - Key accomplishments or discoveries

2. **Current Situation**
   - Where they are right now
   - Immediate circumstances
   - Party status (HP, resources)

3. **What You've Prepared**
   - Brief overview of what's ahead (without spoilers!)
   - Options available to them
   - Time-sensitive considerations

4. **Ask**: "What do you want to do?"

## Example Output Format:

```
📖 CAMPAIGN RESUMED: [Campaign Name]

### Last Session Recap:
[2-3 sentence summary of what happened]

### Current Situation:
**Location**: [Where they are]

**Party Status:**
- Character 1: HP X/Y, resources
- Character 2: HP X/Y, resources
- XP: [amount] each

**Active Quests:**
- [Quest 1]
- [Quest 2]

---

### What I've Prepared:

[Brief description of what's ahead if they continue in likely direction]

**Key Information:**
- [Important detail 1]
- [Important detail 2]

---

### Your Options:

1. **[Option 1]**
   - [What this involves]
   - [Considerations]

2. **[Option 2]**
   - [What this involves]
   - [Considerations]

3. **[Option 3]**
   - [What this involves]
   - [Considerations]

---

**What do you want to do?**
```

## Important Notes:

- **Don't spoil surprises**: Mention what's prepared but don't reveal all secrets
- **Present options**: Give players agency, don't railroad
- **Consider party state**: Account for their current resources and capabilities
- **Be ready to improvise**: Players might do something unexpected

---

**After completing preparation, you are ready to DM the session!**
