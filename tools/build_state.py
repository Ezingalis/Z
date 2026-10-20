#!/usr/bin/env python3
"""Builds state/progression.json and state/progression.md.

One source of truth for every number the four characters can say out loud,
level 1 to 9, under the 2024 rules. Chapter scripts must quote these values.
Run: python3 tools/build_state.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROF = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4}
SLOTS = {  # full-caster slot table (Sorcerer and Cleric)
    1: [2], 2: [3], 3: [4, 2], 4: [4, 3], 5: [4, 3, 2], 6: [4, 3, 3],
    7: [4, 3, 3, 1], 8: [4, 3, 3, 2], 9: [4, 3, 3, 3, 1],
}


def mod(score):
    return (score - 10) // 2


def sgn(n):
    return f"+{n}" if n >= 0 else str(n)


def hp(level, die_avg, con_mod, extra_per_level=0):
    # level 1: max die; later levels: fixed average (d6=4, d8=5, d10=6)
    first = {4: 6, 5: 8, 6: 10}[die_avg]
    return first + (level - 1) * die_avg + level * (con_mod + extra_per_level)


# Which levels each character's ability scores change at (2024 ASI feat: +2 to one score).
MILOSH = dict(base=dict(STR=8, DEX=14, CON=14, INT=10, WIS=12, CHA=16),
              asi={4: "CHA", 8: "CHA"})
TAMSIN = dict(base=dict(STR=8, DEX=16, CON=14, INT=12, WIS=14, CHA=10),
              asi={4: "DEX", 8: "DEX"})
OSKAR = dict(base=dict(STR=16, DEX=12, CON=16, INT=8, WIS=10, CHA=10),
             asi={4: "STR", 6: "STR", 8: "CON"})
IMELDA = dict(base=dict(STR=12, DEX=10, CON=14, INT=10, WIS=16, CHA=10),
              asi={4: "WIS", 8: "WIS"})


def scores(ch, level):
    s = dict(ch["base"])
    for lv, ab in ch["asi"].items():
        if level >= lv:
            s[ab] = min(20, s[ab] + 2)
    return s


MILOSH_FEATURES = {
    1: ["Spellcasting", "Innate Sorcery (2 uses per long rest)"],
    2: ["Font of Magic (2 sorcery points)", "Metamagic (2 options: Quickened Spell, Subtle Spell)"],
    3: ["Wild Magic Sorcery subclass: Wild Magic Surge, Tides of Chaos (see bible: non-SRD, paraphrased)"],
    4: ["Ability Score Improvement (Charisma +2)", "5th cantrip"],
    5: ["Sorcerous Restoration (regain sorcery points on a short rest)", "3rd-level spells"],
    6: ["Wild Magic: Bend Luck (reaction, spend 1 sorcery point, add or subtract 1d4 on another creature's d20 roll)"],
    7: ["Sorcery Incarnate", "4th-level spells"],
    8: ["Ability Score Improvement (Charisma +2)"],
    9: ["5th-level spells"],
}
MILOSH_SPELLS = {
    1: ("Fire Bolt, Minor Illusion, Prestidigitation, Mage Hand", "Magic Missile, Thunderwave"),
    2: ("same", "+ Shield, Disguise Self"),
    3: ("same", "+ Misty Step, Invisibility"),
    4: ("+ Friends", "+ Hold Person"),
    5: ("same", "+ Fireball, Counterspell"),
    6: ("same", "+ Enlarge/Reduce"),
    7: ("same", "+ Dimension Door"),
    8: ("same", "+ Greater Invisibility"),
    9: ("same", "+ Animate Objects, Cone of Cold"),
}
SORC_PREPARED = {1: 2, 2: 4, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14}
SORC_CANTRIPS = {1: 4, 2: 4, 3: 4, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}

TAMSIN_FEATURES = {
    1: ["Expertise (Stealth, Thieves' Tools)", "Sneak Attack 1d6", "Thieves' Cant", "Weapon Mastery"],
    2: ["Cunning Action (bonus action Dash, Disengage, Hide)"],
    3: ["Thief subclass: Fast Hands, Second-Story Work", "Steady Aim", "Sneak Attack 2d6"],
    4: ["Ability Score Improvement (Dexterity +2)"],
    5: ["Cunning Strike", "Uncanny Dodge", "Sneak Attack 3d6"],
    6: ["Expertise (two more skills: Perception, Investigation)"],
    7: ["Evasion", "Reliable Talent", "Sneak Attack 4d6"],
    8: ["Ability Score Improvement (Dexterity +2)"],
    9: ["Thief: Supreme Sneak", "Sneak Attack 5d6"],
}
SNEAK = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5}

OSKAR_FEATURES = {
    1: ["Fighting Style: Archery (+2 to ranged weapon attacks)", "Second Wind", "Weapon Mastery"],
    2: ["Action Surge (one use)", "Tactical Mind"],
    3: ["Champion subclass: Improved Critical (crit on 19-20)"],
    4: ["Ability Score Improvement (Strength +2)"],
    5: ["Extra Attack (two attacks per Attack action)", "Tactical Shift"],
    6: ["Ability Score Improvement (Strength +2)"],
    7: ["Champion: Remarkable Athlete"],
    8: ["Ability Score Improvement (Constitution +2)"],
    9: ["Indomitable (one use)", "Tactical Master"],
}
IMELDA_FEATURES = {
    1: ["Spellcasting", "Divine Order: Protector (martial weapons, heavy armor)", "Dwarven Toughness (+1 HP per level)"],
    2: ["Channel Divinity: Divine Spark, Turn Undead (2 uses)"],
    3: ["Life Domain subclass: Disciple of Life, Preserve Life"],
    4: ["Ability Score Improvement (Wisdom +2)"],
    5: ["Sear Undead", "3rd-level spells"],
    6: ["Life Domain: Blessed Healer"],
    7: ["Blessed Strikes", "4th-level spells"],
    8: ["Ability Score Improvement (Wisdom +2)"],
    9: ["5th-level spells"],
}
CLERIC_PREPARED = {1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14}
CLERIC_CANTRIPS = {1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4}

# Level at the START and END of each chapter. Level-ups happen at the marked moments.
CHAPTER_LEVELS = {
    1: (1, 1), 2: (1, 1), 3: (1, 2), 4: (2, 2), 5: (2, 2), 6: (2, 3), 7: (3, 3), 8: (3, 4),
    9: (4, 4), 10: (4, 4), 11: (4, 5), 12: (5, 5), 13: (5, 5), 14: (5, 6), 15: (6, 6),
    16: (6, 7), 17: (7, 7), 18: (7, 8), 19: (8, 8), 20: (8, 9), 21: (9, 9), 22: (9, 9),
}


def character_rows(level):
    p = PROF[level]
    out = {}

    s = scores(MILOSH, level)
    cm, dm, com = mod(s["CHA"]), mod(s["DEX"]), mod(s["CON"])
    out["MILOSH"] = dict(
        scores=s, mods={k: mod(v) for k, v in s.items()},
        hp=hp(level, 4, com), ac="12 (10 + Dex 2); 15 with Mage Armor; +5 with Shield spell",
        spell_attack=cm + p, spell_dc=8 + cm + p,
        slots=SLOTS[level], cantrips=SORC_CANTRIPS[level], prepared=SORC_PREPARED[level],
        sorcery_points=0 if level < 2 else level,
        cantrip_list=MILOSH_SPELLS[level][0], spell_changes=MILOSH_SPELLS[level][1],
        fire_bolt=f"{1 + (level >= 5) + (level >= 11)}d10",
        skills=dict(Deception=cm + p, SleightOfHand=dm + p, Persuasion=cm + p, Arcana=mod(s["INT"]) + p,
                    Stealth=dm + p, Performance=cm + p, Perception=mod(s["WIS"]) + p),
        save_dex=dm, save_con=com, save_cha=cm + p,
        features=[f for lv in range(1, level + 1) for f in MILOSH_FEATURES.get(lv, [])],
    )

    s = scores(TAMSIN, level)
    dxm, wsm, com = mod(s["DEX"]), mod(s["WIS"]), mod(s["CON"])
    out["TAMSIN"] = dict(
        scores=s, mods={k: mod(v) for k, v in s.items()},
        hp=hp(level, 5, com), ac=11 + dxm,
        dagger_attack=dxm + p, dagger_damage=f"1d4{sgn(dxm)}", sneak_attack=f"{SNEAK[level]}d6",
        skills=dict(Stealth=dxm + 2 * p, ThievesTools=dxm + 2 * p, Perception=wsm + (2 * p if level >= 6 else p),
                    Investigation=mod(s["INT"]) + (2 * p if level >= 6 else 0)),
        passive_perception=10 + wsm + (2 * p if level >= 6 else p),
        save_dex=dxm + p,
        features=[f for lv in range(1, level + 1) for f in TAMSIN_FEATURES.get(lv, [])],
    )

    s = scores(OSKAR, level)
    sm, dxm, com = mod(s["STR"]), mod(s["DEX"]), mod(s["CON"])
    out["OSKAR"] = dict(
        scores=s, mods={k: mod(v) for k, v in s.items()},
        hp=hp(level, 6, com), ac=16,
        longsword_attack=sm + p, longsword_damage=f"1d8{sgn(sm)}",
        longbow_attack=dxm + p + 2, longbow_damage=f"1d8{sgn(dxm)}",
        attacks_per_action=2 if level >= 5 else 1, crit_range="19-20" if level >= 3 else "20",
        second_wind_heal=f"1d10+{level}", save_str=sm + p, save_con=com + p,
        features=[f for lv in range(1, level + 1) for f in OSKAR_FEATURES.get(lv, [])],
    )

    s = scores(IMELDA, level)
    wm, com = mod(s["WIS"]), mod(s["CON"])
    out["IMELDA"] = dict(
        scores=s, mods={k: mod(v) for k, v in s.items()},
        hp=hp(level, 5, com, extra_per_level=1), ac="18 (chain mail 16 + shield 2)",
        spell_attack=wm + p, spell_dc=8 + wm + p,
        slots=SLOTS[level], cantrips=CLERIC_CANTRIPS[level], prepared=CLERIC_PREPARED[level],
        sacred_flame=f"{1 + (level >= 5) + (level >= 11)}d8",
        healing_word=f"{2 + 0}d4{sgn(wm)}", save_wis=wm + p, save_cha=mod(s["CHA"]) + p,
        features=[f for lv in range(1, level + 1) for f in IMELDA_FEATURES.get(lv, [])],
    )
    return out


def main():
    data = {"proficiency": PROF, "chapter_levels": CHAPTER_LEVELS, "levels": {}}
    for lv in range(1, 10):
        data["levels"][lv] = character_rows(lv)
    os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
    with open(os.path.join(ROOT, "state", "progression.json"), "w") as f:
        json.dump(data, f, indent=2)

    md = ["# Character progression, levels 1 to 9 (2024 rules)", "",
          "Generated by tools/build_state.py. These numbers are canon: quote them, never recompute.", "",
          "## Which level each chapter plays at", "", "| Chapter | Starts at | Ends at |", "| --- | --- | --- |"]
    for ch, (a, b) in CHAPTER_LEVELS.items():
        md.append(f"| {ch} | {a} | {b} |")
    for lv in range(1, 10):
        md += ["", f"## Level {lv} (proficiency bonus +{PROF[lv]})", ""]
        for name, d in data["levels"][lv].items():
            md.append(f"### {name.title()}")
            for k, v in d.items():
                if k == "features":
                    md.append("- features: " + "; ".join(v))
                else:
                    md.append(f"- {k}: {v}")
            md.append("")
    with open(os.path.join(ROOT, "state", "progression.md"), "w") as f:
        f.write("\n".join(md))
    print("wrote state/progression.json and state/progression.md")


if __name__ == "__main__":
    main()
