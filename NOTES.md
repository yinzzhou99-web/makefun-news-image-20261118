# news-image-20261118 — "The World Today" front page

Entry: a Python program (`main.py`, stdlib + Pillow) that draws a 1024×1024
newspaper front page and writes it to `/output/entry.png`. No network, fully
deterministic. A local `preview.png` copy of the rendered output is included
for inspection (not read by the program).

## Headlines used (all verified via news search, 18 Nov 2026 ~07:20 UTC)

1. **Lead — Gulf crisis:** US jets struck a Revolutionary Guard missile
   launch site on Qeshm Island after Iran fired drones at a US radar base
   in Bahrain (third attack there in under a week); Kuwait air defences
   also intercepted drones. Sources: One Turn / Japan Times / CBS / Al
   Jazeera; Nexus Europa; Daily Baku.
2. **Ukraine:** Ukraine struck the Kerch Bridge to Crimea for a second day;
   part of its road span fell. Sources: One Turn, JagranJosh.
3. **Diplomacy:** Trump, Xi and Putin to meet in Shenzhen on Thursday as
   the APEC summit opens. Sources: One Turn, Global Puls Today / Reuters.
4. **Health:** Ebola in DR Congo passes 11,000 cases / 5,400 deaths in
   three months, per the UN. Source: One Turn.
5. **Disaster:** Russian military transport plane crashed in Kemerovo
   region, 19 dead. Sources: Daily Baku, CareerIndia.

## Verification (all passed)

- Two runs of `python3 main.py`: sha256 identical —
  `0d071f5f6576fa1ca9a7ab1e8344d00be2ee03c89fc0f17fe01b70699bf84a21`
- Output: PNG 1024×1024, 130,687 bytes (limit 1,048,576).
- Visual inspection of preview.png: masthead, lead headline (56pt serif),
  4 secondary stories (34pt headlines), drawn Gulf illustration panel;
  no text overlap or overflow (layout asserts in code enforce it).
- One fix made during verification: Ebola body shortened (was 4 lines,
  overflowing the footer); lead headline re-wrapped to 3 lines at 56pt.

## Files

- `main.py` — the entry program (draws the image).
- `LICENSE` — MIT, with SPDX identifier line.
- `preview.png` — rendered output for inspection.
- `NOTES.md` — this file.
