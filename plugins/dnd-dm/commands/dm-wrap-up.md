# DM Wrap-Up - End D&D Session and Update Campaign Files

You are the Dungeon Master wrapping up a D&D campaign session. Follow these steps to document the session and update all campaign files.

**IMPORTANT: All file updates in this command use APPEND operations only. Never overwrite existing content.**

## Step 1: Review the Current Session

Review the conversation history from this session to extract:

1. **Session events**:
   - Major encounters (combat, exploration, social)
   - Key decisions and player choices
   - NPC interactions
   - Discoveries and revelations

2. **Combat outcomes**:
   - Enemies defeated
   - Damage taken
   - Resources used (spell slots, abilities, items)
   - Treasure and XP earned

3. **Current party status**:
   - Current HP for each character
   - Resources remaining (spell slots, abilities)
   - Current location
   - Active effects or conditions

4. **Story progression**:
   - Quests advanced or completed
   - New plot hooks discovered
   - Unresolved mysteries
   - Where the session ended (cliffhanger)

## Step 2: Determine Session Number and Title

Read the existing campaign log to find the last session number:

```bash
cat .claude/skills/dnd-dm/sessions/<campaign-name>/campaign-log.md
```

- Note the last session number
- Next session number = last number + 1
- Generate a memorable session title based on the main event (e.g., "The Goblin Ambush", "Negotiating with Sildar", "Into the Cragmaw Hideout")

## Step 3: Append to Campaign Log

**File**: `.claude/skills/dnd-dm/sessions/<campaign-name>/campaign-log.md`

**Action**: APPEND the new session at the end of the file.

Use this structure:

```markdown

---

# Session X - [Memorable Title]

**Date**: [Current Date]
**Duration**: [Approximate session length]

## Table of Contents
1. Session Summary
2. [Major Event 1]
3. [Major Event 2]
4. [Additional events as needed]
5. Party Status
6. Key NPCs and Enemies
7. Treasure and Loot
8. Experience Gained
9. Cliffhanger

## Session Summary

[2-3 paragraph overview of the entire session - what happened from start to finish, focusing on the narrative arc and major accomplishments]

## [Major Event 1 Title]

### Context
[Setup and situation leading into this event]

### What Happened
[Detailed account including:
- Player actions and decisions
- Dice rolls (attack rolls, damage, saving throws, ability checks)
- NPC reactions and dialogue
- Outcomes of actions]

### Results
[Consequences of this event:
- Changes to game state
- Character conditions or effects
- Story implications
- Resources used/gained]

## [Major Event 2 Title]

[Repeat same structure for each major event]

## Party Status

**Current Location**: [Where the party is now]

**Character Status**:
- **[Character 1 Name]**: HP X/Y, Spell Slots [remaining], Special Abilities [used/available], Conditions [if any]
- **[Character 2 Name]**: HP X/Y, Resources [details]
- [Continue for all characters]

**Active Effects**: [Any ongoing effects, buffs, debuffs, or conditions]

## Key NPCs and Enemies

**Encountered This Session**:
- **[NPC/Enemy Name]**: [Status - alive/dead/fled], [Relationship/attitude toward party], [Important information]
- [Continue for all significant NPCs]

**Previously Known NPCs**:
- [Brief updates on their status if relevant]

## Treasure and Loot

**Found/Earned**:
- [Item 1]: [Description, who has it]
- [Currency]: [Amount and type]
- [Magic items or quest items]

**Current Party Inventory** (significant items):
- [List key items and who carries them]

## Experience Gained

**Combat XP**: [Total from enemies defeated]
- [Enemy 1]: X XP
- [Enemy 2]: X XP

**Milestone XP**: [Any story or quest XP awarded]

**Total XP This Session**: [Amount]

**Character XP Totals**:
- [Character 1]: [Total XP] (Level [X], [Y] XP to next level)
- [Character 2]: [Total XP] (Level [X], [Y] XP to next level)

## Cliffhanger

[Describe where the session ended - the immediate situation, tension, or question that will hook into the next session]

**Immediate Threats/Concerns**:
- [Active danger or time-sensitive situation]
- [Unresolved conflict]

**Open Questions**:
- [Mysteries to solve]
- [Decisions to make]
- [Goals to pursue]

**Next Session Preview**:
[Brief tease of what's likely to happen next based on where they are and what they're doing]

## DM Notes

**What Went Well**:
- [Successful moments, good player engagement, cool rulings]

**For Next Session**:
- [Prep needed: NPCs, encounters, maps]
- [Rules to review]
- [Plot threads to advance]

**Adventure Context**:
- **Book**: [Adventure name]
- **Pages Used**: [Page range from adventure book]
- **Next Section**: [What to prepare for continuation]

---
```

## Step 4: Append Session Note to Campaign Summary

**File**: `.claude/skills/dnd-dm/sessions/<campaign-name>/campaign-summary.md`

**Action**: APPEND a brief session entry to the session log section.

Find the "## Session Log" section and append:

```markdown
### Session X - [Title] ([Date])
- [2-3 sentence summary]
- Location: [Current location]
- XP Earned: [Amount]
- Key Events: [Brief list of major events]

```

## Step 5: Append to Character Sheets

For each character file (`.claude/skills/dnd-dm/sessions/<campaign-name>/character-*.md`):

**Action**: APPEND a session update entry.

```bash
cat >> .claude/skills/dnd-dm/sessions/<campaign-name>/character-[name].md << 'EOF'

## Session X Update ([Date])

**HP**: [Current]/[Max]
**XP Gained**: +[Amount] (Total: [New Total])
**Level**: [Current Level] ([XP to next level] to level [Next])

**Resources**:
- Spell Slots: [Current status]
- Class Abilities: [What was used, what's available]
- Items Used: [Consumables used]

**New Items**:
- [Item 1]: [Description]
- [Item 2]: [Description]

**Status**: [Any conditions, effects, or notes]

EOF
```

## Step 6: Update Main Campaign Summary Sections

**File**: `.claude/skills/dnd-dm/sessions/<campaign-name>/campaign-summary.md`

**Action**: APPEND updates to relevant sections or append new quest entries.

For new quests, append to the "## Active Quests" section:

```markdown
### [Quest Name]
- **Status**: [Active/Completed/Failed]
- **Objective**: [What needs to be done]
- **Progress**: [What's been accomplished]
- **Reward**: [If known]

```

For location changes, append to "## Location History":

```markdown
- **Session X**: [New location] - [Brief context]

```

## Step 7: Final Confirmation

After all files have been updated, provide a summary:

```
✅ SESSION X WRAP-UP COMPLETE

**Files Updated**:
- campaign-log.md: Session X appended ([estimated lines] added)
- campaign-summary.md: Session log and quest updates appended
- character-[name1].md: Session X update appended
- character-[name2].md: Session X update appended

**Session Stats**:
- Duration: [time]
- XP Awarded: [amount] per character
- Treasure: [summary]
- Enemies Defeated: [count/list]

**Party Status**:
- Location: [Where they are]
- HP: [Summary of party health]
- Resources: [General state]

**Next Session**:
The party [brief description of current situation and what's likely next].

**DM Prep Needed**:
- [Item 1]
- [Item 2]

---

Session successfully logged! Use `/dm-prepare` to resume the campaign next time.
```

## Important Notes

- **All operations append only** - existing content is never overwritten
- **Session log grows over time** - this is intentional for campaign history
- **Character files track progression** - each session adds a new update entry
- **Campaign summary accumulates notes** - builds a complete campaign reference
- **Backup reminder**: Suggest backing up session files periodically (git commit)

## Tips

- Be specific about dice rolls and outcomes in the detailed write-up
- Capture player creativity and memorable moments
- Note any house rules or special rulings for consistency
- Include enough detail to resume smoothly next session
- End the write-up on an exciting note to build anticipation

---

**After completing all steps, the session is fully documented and the campaign is ready to resume!**
