# Series bible: Milosh and the Rotting Well

A 22-chapter learn-to-play D&D (2024 rules) audio drama. A table of four players and a DM plays a full campaign; a brand-new listener learns how to play by hearing it done. Each chapter must render to at least 60 minutes of audio. Read this whole file before writing anything.

## Files you will use

| Path | What it is |
| --- | --- |
| `source/campaign.md` | Canon: cast, level-1 numbers, the 22-chapter plan, and Chapter 1 (lines 97 to 677). |
| `chapters/01/script.md` | Chapter 1, cleaned and unescaped. **The style reference.** Read it before drafting. |
| `source/dungeon_notes/*.md` | Faithful notes on the seven source dungeons (CC BY-SA 4.0). Story content comes from here. |
| `state/progression.md` | Every number each character can say, levels 1 to 9. Quote it; never recompute. |
| `tools/roll.py` | Seeded dice roller that logs to `chapters/NN/rolls.log`. |
| `tools/surge.py` | Milosh's original Wild Magic surge table. |
| `tools/lint.py` | Format and length checker. Run it on every script. |
| `SPINE.md` | Chapter-by-chapter outline and handoffs (written before drafting). |

## Output per chapter (folder `chapters/NN/`)

- `outline.md`: scenes, rules taught, monster stat blocks, rolls needed, handoff.
- `script.md`: the chapter script, nothing else (no summaries, tables, or notes in it).
- `rolls.log`: written by the tools while you draft.
- `handoff.json`: state at the end of the chapter (see below).

## Script format (identical to Chapter 1)

- Every non-blank line is one of: a heading (`## Chapter N: Title`, `### Scene N: Title`, `#### Round N`), a standalone cue, or a speaker line.
- Speaker lines start with an uppercase tag and a colon: `DM:`, `MILOSH:`, `TAMSIN:`, `OSKAR:`, `IMELDA:`. NPCs are spoken by the DM: `DM: [as BELVEDERE, silky] ...`.
- `[OOC]` at the start of or inside a line marks out-of-character table talk (rules questions, jokes). No tag means in character.
- Emotion and delivery cues go in square brackets inside the line: `[laughs]`, `[whispering]`, `[sighs]`, `[shouting]`, `[as FINDLAY, frantic]`.
- Standalone cue lines, each on its own line: `[SFX: wooden barrel tipping, water splashing]` and `[MUSIC: plucky, sneaky pizzicato strings]`.
- Every die roll gets `[SFX: dice roll]` on its own line immediately before the spoken result. Several dice at once: `[SFX: two dice roll]`. Rolls made behind the DM screen: `[SFX: dice roll behind screen]`.
- Plain square brackets only. Never backslash-escaped brackets.
- **No em dashes and no en dashes anywhere.** Use commas, periods, or colons. American spelling.
- Numbers in speech are written as words, like Chapter 1 ("Fourteen! Plus five, nineteen."). Game tokens keep their form: d20, d6, DC 15, AC 12.
- Open each chapter with a short `[MUSIC: main theme ...]` sting and a two-line "Previously" recap by the DM only from Chapter 2 on. Close with a recap of **at most three lines**, then the credits scene (below).

## Length: 8,500 to 9,500 spoken words (this is the hard part)

Chapter 1 as written is only about 3,950 spoken words, which is under half an hour. Real hour-long chapters need about 9,000 spoken words. `tools/lint.py` counts only the words after speaker tags (cue brackets excluded) and fails anything outside 8,500 to 9,500. Plan for it:

- Six to eight scenes of roughly 1,100 to 1,500 words each, plus a recap and credits.
- Fill with story, not padding: sensory narration from the DM, NPC scenes with real personalities, party banter and disagreement, in-character planning, a rule explained at the moment it matters, rolls said as math, consequences of failures, and jokes with setups and payoffs.
- A combat or hazard scene should run at least three rounds with every player acting each round.
- Never summarize an action that could be played. Play it.

## Teaching rules

- Chapters 1 to 6: say every roll as math out loud ("d20 shows 16, plus my +5, that's 21"). The DM explains each new rule the first time it appears, in one or two sentences, then never again unless a player asks.
- Chapters 7 to 14: spell out only new or unusual rolls. Chapters 15 to 22: play like an experienced table.
- Each chapter teaches the rules the plan lists for it (`source/campaign.md`, plan table, and `SPINE.md`). No rules lectures, no fluff, no long recaps.
- A rule taught earlier is never re-explained unless a player asks, in which case another player answers in one line.
- Failure moves the story forward and never stalls it.
- The DM may say "you can try" and the table may disagree about the rules; real tables do. When the table gets a rule wrong, a player corrects it within the same scene.

## Non-negotiable story rules

1. Milosh is a human Wild Magic sorcerer with the Charlatan background, played as a comedic "failed wizard" who claims he left the Academy to start a business. He starts at level 1.
2. Wild Magic does not exist before level 3 (Chapter 6). From then on, recurring bits: he casts the wrong spell at the worst moment, and his bragging triggers Wild Magic surges mid-story. Fire Bolt against fire-immune devils is a running joke.
3. Milosh's business cards **do not appear, are not mentioned, and are not used in any spell until Chapter 20**, when he reaches level 9 and learns Animate Objects. The finale (Chapter 22) has him animate every card he has ever printed. `tools/lint.py` fails any earlier mention of "business card". (Foreshadow differently: he keeps promising to "print something", or says he has "stationery plans", never cards.)
4. Belvedere is the through-line villain: he escapes with his second horn in Chapter 5 and is beaten in Chapter 22 at the Emporium, full circle. Every arc in between either delays him or hands the party a tool they need for Chapter 22.
5. Every number is correct for 2024 rules and the character's current level (`state/progression.md`). No drift.

## Cast and voices

| Tag | Character | Notes |
| --- | --- | --- |
| DM | The Dungeon Master | Warm, wry. Plays every NPC and monster with `[as NAME, delivery]`. Explains rules briefly, then gets out of the way. |
| MILOSH | Milosh | Human Sorcerer (Charlatan). Theatrical, a beat too loud, panics fast. The listener's stand-in: asks the beginner questions. |
| TAMSIN | Tamsin Reedwhistle | Halfling Rogue. Dry, quick, veteran who explains things to Milosh. Stealth, locks, Sneak Attack. |
| OSKAR | Oskar Dahl | Human Fighter. Big, cheerful, says "I hit it" a lot. The wall. Carries a longbow he is bad at. |
| IMELDA | Sister Imelda | Dwarf Cleric of the Lantern Order. Kind, firm, the conscience. Healing, saves, Help action. |

Recurring NPCs: **Findlay** (frantic, bow tie, missing a finger, exclamation points; a real wizard with his own shop), **Belvedere** (silky devil, whip, second horn), **Bif** (dumb, slow, deep), **Poo** (cheeky, giggly, high), **Fog** (wheezy, loyal to Belvedere), **Max** (imp revolutionary, introduced Chapter 3), **Pepe** (firedrake, Chapter 2), **Leo** (Chapter 2). New NPCs may appear when the source dungeon calls for them; give each a one-line voice direction in the outline.

## Dice protocol

- Roll every check, attack, and save with `tools/roll.py` while drafting, with `--ch N --label "..."`. Write the story around the results, including bad ones. Do not invent results.
- Monster and NPC rolls too (they happen "behind the screen").
- You may use `--reroll` at most **twice per chapter**, only for pacing, and each is logged as REROLL.
- Rolls the script says out loud must match the log (the reviewers will spot-check).
- Where a source dungeon prints no AC or HP, the DM supplies sensible numbers for the party's level, listed in `outline.md` and kept consistent in the script.

## Wild Magic (house version, paraphrased; this subclass is not in SRD 5.2)

SRD 5.2 contains the Draconic Sorcery subclass only, so Wild Magic cannot be quoted from the book. The series uses its own paraphrase and an original surge table (`tools/surge.py`). Do not quote Wizards of the Coast text for it. At the table, the DM says "it works like this" in plain words:

- **Wild Magic Surge (level 3).** Right after Milosh casts a spell with a spell slot, the DM may call for a d20; on a 20, roll on the surge table. Separately, as a **house rule** the DM invents at the table: when Milosh brags about his own power in character, the DM may call a "bragging check": a d20, and on a 1 to 5 a surge happens. The DM explains once that this one is the table's own rule.
- **Tides of Chaos (level 3).** Once per long rest, Milosh may give himself advantage on one d20 roll. After that, his next slot spell triggers a surge automatically, and then Tides of Chaos recharges.
- **Bend Luck (level 6).** Reaction, spend 1 sorcery point: add or subtract 1d4 from another creature's d20 roll.
- Surge results come only from `tools/surge.py --ch N`. Never improvise a result.

## Rules sources

- Rules content comes from SRD 5.2 (CC BY 4.0) and the 2024 rules as paraphrased facts. Never copy non-SRD text from Wizards of the Coast books. Spells, monsters, conditions and class features may be named and used by their mechanics.
- SRD 5.2 feats are limited to the Origin feats (Alert, Magic Initiate, Savage Attacker, Skilled) and the general feats Ability Score Improvement and Grappler. When a plan row says "feat", use those; the table's level-up feats are Ability Score Improvements as in `state/progression.md`.
- The Charlatan background and the Wild Magic subclass are Milosh's established identity; use them by name and mechanics only.

## Continuity (`handoff.json`)

Write `chapters/NN/handoff.json` at the end of every chapter with: `level_end`; for each character `hp_current` and `hp_max`; `spell_slots_remaining`; `sorcery_points_remaining`; `conditions`; `gold_party` and per-person gold if split; `inventory_added` and `inventory_removed`; `named_magic_items` (for example the cloudy green potion); `relationships` (NPC attitudes); `open_threads`; `callbacks_planted` (jokes and objects that must pay off later, with the chapter they pay off in); `rules_taught` (list); `rolls_rerolled`. Read the previous chapter's `handoff.json` and `SPINE.md` before drafting.

Between chapters the party gets a long rest unless the spine says otherwise, so slots and hit points refill at the start of each chapter. A chapter that must start mid-crisis says so in the spine.

## Credits and license (end of every chapter)

Final scene "Credits": the DM, out of character, speaks (short and warm) the author credit for every source dungeon used in that chapter, the CC BY-SA 4.0 license, the SRD 5.2 CC BY 4.0 notice, and "This audio drama is shared under CC BY-SA 4.0". Authors, exactly as printed:

| Dungeon | Author credit |
| --- | --- |
| Findlay's Lamp Emporium | Mister Rees |
| Baphomet's Baleful Bathhouse | Teun Veekens |
| Time Troubles | William D. Renninger |
| Locally Sourced | Horrorseed and James |
| Vicious Cycle | Justin Evans |
| Over the Moon | Moose Castle Media (James and Mateusz) |
| The Sphere of Avantarr | John Nash |

All from the 2024 One Page Dungeon Contest Winners' Circle.

## Style, in one paragraph

Short lines. Plain words. The DM narrates in present tense, three or four sentences at a time, then hands the table a choice. Players talk over each other like friends. Jokes come from character: Milosh over-promises, Tamsin under-reacts, Oskar hits things, Imelda sighs and heals. Teaching lives inside the fiction: the listener learns a rule because a character needs it right now.
