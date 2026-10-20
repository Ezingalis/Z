#!/usr/bin/env python3
"""Seeded dice roller. Every roll is logged so it can be audited.

Examples:
  tools/roll.py "d20+5" --ch 2 --label "Milosh Deception vs DC 12"
  tools/roll.py "d20+2" --adv --ch 2 --label "Tamsin Stealth"
  tools/roll.py "2d4+3" --ch 2 --label "Healing Word"
  tools/roll.py "d20+5" --seed 12345 --ch 2 --label "replayed roll"
  tools/roll.py "d20+5" --ch 2 --reroll --label "pacing reroll (max two per chapter)"

Output is one line: the dice, the modifier, and the total. The same line is
appended to chapters/NN/rolls.log together with the seed.
"""
import argparse
import os
import random
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse(expr):
    m = re.fullmatch(r"\s*(\d*)d(\d+)\s*([+-]\s*\d+)?\s*", expr)
    if not m:
        sys.exit(f"bad dice expression: {expr!r}")
    n = int(m.group(1) or 1)
    sides = int(m.group(2))
    mod = int(m.group(3).replace(" ", "")) if m.group(3) else 0
    return n, sides, mod


def roll(expr, adv=False, dis=False, seed=None):
    n, sides, mod = parse(expr)
    if seed is None:
        seed = int.from_bytes(os.urandom(6), "big")
    rng = random.Random(seed)
    if (adv or dis) and not (n == 1 and sides == 20):
        sys.exit("advantage/disadvantage only applies to a single d20")
    if adv and dis:
        adv = dis = False
    if adv or dis:
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        kept = max(a, b) if adv else min(a, b)
        total = kept + mod
        detail = f"d20 {'ADV' if adv else 'DIS'} [{a}, {b}] keep {kept}"
    else:
        dice = [rng.randint(1, sides) for _ in range(n)]
        total = sum(dice) + mod
        detail = f"{n}d{sides} {dice}"
        if n == 1 and sides == 20:
            if dice[0] == 20:
                detail += " NATURAL 20"
            elif dice[0] == 1:
                detail += " NATURAL 1"
    if mod:
        detail += f" {'+' if mod > 0 else '-'} {abs(mod)}"
    return total, detail, seed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("expr")
    p.add_argument("--adv", action="store_true")
    p.add_argument("--dis", action="store_true")
    p.add_argument("--seed", type=int)
    p.add_argument("--ch", type=int, help="chapter number, for the log")
    p.add_argument("--label", default="")
    p.add_argument("--reroll", action="store_true", help="mark as a pacing reroll")
    a = p.parse_args()
    total, detail, seed = roll(a.expr, a.adv, a.dis, a.seed)
    line = f"{detail} = {total}"
    print(line)
    if a.ch is not None:
        d = os.path.join(ROOT, "chapters", f"{a.ch:02d}")
        os.makedirs(d, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        tag = " REROLL" if a.reroll else ""
        with open(os.path.join(d, "rolls.log"), "a") as f:
            f.write(f"{ts} seed={seed} {a.label} | {line}{tag}\n")


if __name__ == "__main__":
    main()
