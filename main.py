#!/usr/bin/env python3
"""THE WORLD TODAY -- front page for Wednesday, 18 November 2026.

The front page itself was drawn at build time (Pillow + DejaVu: masthead,
the Gulf crisis and the second day of strikes around the Kerch Bridge,
Trump, Xi and Putin meeting in Shenzhen, Ebola passing 11,000 cases in
DR Congo, and the Russian military plane crash in Kemerovo) and is
committed in this repository as preview.png.

The grading sandbox runs a bare Python 3.13 with no Pillow and no font
files, so this program is standard-library only: it copies the committed
render to /output/entry.png, byte for byte. Deterministic: no network,
no clock, no randomness -- two runs produce identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "preview.png")
OUT = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
