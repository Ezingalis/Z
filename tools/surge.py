#!/usr/bin/env python3
"""Original Wild Magic surge table for Milosh (our own text; not WotC's table).

Usage: tools/surge.py [--ch N] [--seed S] [--label TEXT]   -> rolls a d20 on the table
       tools/surge.py --list                                -> prints the whole table
Rolls are logged to chapters/NN/rolls.log like tools/roll.py.
"""
import argparse
import os
import random
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TABLE = {
    1: "Paper birds burst from Milosh's sleeves and flutter off. For 1 minute, every creature within 30 feet that can see him has disadvantage on Perception checks to notice anything else.",
    2: "Milosh's voice booms at double volume for 10 minutes. He cannot whisper, and Stealth checks he makes by sound alone fail.",
    3: "A shower of glitter coats everyone within 10 feet for 1 hour. Stealth checks against creatures who can see them have disadvantage.",
    4: "Every creature within 10 feet, friend or foe, gains 1d6 temporary hit points as a warm gust of cinnamon-scented air rolls out.",
    5: "Milosh floats 1 foot off the ground for 1 minute. He ignores difficult ground and cannot be knocked prone, but cannot push, pull, or climb anything.",
    6: "The spell he cast is cast again at a random target within range, as if from a second Milosh. No extra slot spent; the DM picks the target with a die.",
    7: "Milosh's hair turns neon blue and stands straight up for 1 day. Advantage on his next Performance check; disadvantage on his next Stealth check.",
    8: "A harmless bell tolls overhead. Each creature within 60 feet must succeed on a DC 13 Wisdom save or be unable to take reactions until the start of its next turn.",
    9: "Milosh turns invisible until the end of his next turn, clothes and gear included, and cannot be seen by himself either, so he walks into something.",
    10: "A small, offended goat appears beside him for 1 hour. It follows him, ignores everyone else, and has 4 hit points and AC 10. It bleats at the worst moments.",
    11: "Gravity wobbles. Each creature within 20 feet must succeed on a DC 13 Strength save or fall prone as the floor feels briefly sideways.",
    12: "Milosh swaps places with a random creature within 30 feet (the DM rolls). Both are startled; neither takes damage.",
    13: "All metal within 15 feet hums loudly for 1 minute. Nobody can speak quietly or use Stealth on a metal floor.",
    14: "Bubbles. Everything within 10 feet is covered in a sticky soap film until the end of Milosh's next turn: speed halved and Dexterity saves have disadvantage.",
    15: "A flash of light. Milosh and every creature within 10 feet must succeed on a DC 13 Constitution save or be blinded until the end of their next turn.",
    16: "Milosh grows to Large size, as if by Enlarge, for 1 minute. His clothes do not. This is not a joke the DM is willing to skip.",
    17: "A hungry cloud of small, fluffy fire spirits appears and attacks the nearest non-Milosh creature once (+5 to hit, 1d6 fire damage), then pops. Devils are immune; the DM points this out.",
    18: "Milosh swaps one of his prepared spells for a random spell of the same level from the sorcerer list until his next long rest. He finds out when he casts it.",
    19: "Every creature within 30 feet that can see him must succeed on a DC 13 Wisdom save or be charmed by Milosh until the end of his next turn. He is as surprised as they are.",
    20: "Ten feet in every direction, the air turns to harmless colored smoke and confetti, then a deep voice says: 'Milosh, you are being billed for this.' Roll again on this table, ignoring a repeat of 20.",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    p.add_argument("--ch", type=int)
    p.add_argument("--seed", type=int)
    p.add_argument("--label", default="")
    a = p.parse_args()
    if a.list:
        for k, v in TABLE.items():
            print(f"{k:>2}. {v}")
        return
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    n = random.Random(seed).randint(1, 20)
    line = f"surge d20 = {n}: {TABLE[n]}"
    print(line)
    if a.ch is not None:
        d = os.path.join(ROOT, "chapters", f"{a.ch:02d}")
        os.makedirs(d, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        with open(os.path.join(d, "rolls.log"), "a") as f:
            f.write(f"{ts} seed={seed} {a.label} | {line}\n")


if __name__ == "__main__":
    main()
