#!/usr/bin/env python3
"""Lint a chapter script: python3 tools/lint.py chapters/02/script.md [--ch 2]

Checks: no em or en dashes, valid speaker tags, cue syntax, no business cards
before Chapter 20, spoken word count in range, dice cues vs rolls.log.
"""
import argparse
import os
import re
import sys

SPEAKERS = {"DM", "MILOSH", "TAMSIN", "OSKAR", "IMELDA"}
TARGET = (8500, 9500)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--ch", type=int)
    p.add_argument("--no-count", action="store_true", help="skip word-count range check")
    a = p.parse_args()
    ch = a.ch
    if ch is None:
        m = re.search(r"chapters/(\d+)/", os.path.abspath(a.path))
        ch = int(m.group(1)) if m else None

    text = open(a.path, encoding="utf-8").read()
    errors, warns = [], []
    spoken = 0
    dice_cues = 0
    for i, line in enumerate(text.splitlines(), 1):
        if "—" in line or "–" in line:
            errors.append(f"line {i}: em/en dash")
        if "\\[" in line or "&#91;" in line or "\\]" in line:
            errors.append(f"line {i}: markdown-escaped bracket (use plain [ ])")
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if re.fullmatch(r"\[(SFX|MUSIC):[^\]]+\]", s):
            if s.startswith("[SFX:") and "dice" in s.lower():
                dice_cues += 1
            continue
        m = re.match(r"([A-Z]+): (.+)", s)
        if not m:
            errors.append(f"line {i}: not a speaker line or standalone cue: {s[:60]!r}")
            continue
        if m.group(1) not in SPEAKERS:
            errors.append(f"line {i}: unknown speaker {m.group(1)}")
        body = m.group(2)
        for cue in []:
            warns.append(f"line {i}: inline SFX/MUSIC cue should be on its own line")
        if "dice" in body.lower() and "[SFX: dice" in body:
            dice_cues += 1
        spoken += len(re.sub(r"\[[^\]]*\]", " ", body).split())

    if ch is not None and ch < 20 and re.search(r"business cards?", text, re.I):
        errors.append("mentions business cards before Chapter 20")
    if re.search(r"\bsilver or gold coins? (?:bag|pouch)\b", text, re.I):
        pass
    if not a.no_count and not (TARGET[0] <= spoken <= TARGET[1]):
        errors.append(f"spoken words {spoken} outside {TARGET[0]}-{TARGET[1]}")

    rolls = None
    if ch is not None:
        log = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(a.path)))),
                           "chapters", f"{ch:02d}", "rolls.log")
        if os.path.exists(log):
            rolls = sum(1 for _ in open(log))
    print(f"spoken words: {spoken}")
    print(f"dice cues: {dice_cues}; logged rolls: {rolls}")
    for w in warns[:20]:
        print("warn:", w)
    for e in errors[:60]:
        print("ERROR:", e)
    if len(errors) > 60:
        print(f"... and {len(errors) - 60} more errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
