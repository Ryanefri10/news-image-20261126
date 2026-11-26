# The World in One Image — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Ryanefri10/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Ryanefri10/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for [news-image-20261126](https://make.fun/bounty/news-image-20261126):
sum up Thursday 26 November 2026's world news in one image.

## The image

`entry.png` — 1024x1024, 458,703 bytes,
sha256 `e8f31923ef4793c6d843365a4e33e35cbde08dd7ea2b35f87f97ad0b40d9c9e7`

A newspaper front page: masthead dated **THURSDAY · 26 NOVEMBER 2026**,
a hero panel on the Gulf oil attacks, a 2×2 grid of the day's other
big stories, and a footer strip of smaller items.

## Stories covered

1. **THE GULF — Fire in the Gulf (hero).** Houthis attack Saudi
   Arabia's Ras Tanura oil refinery, and two oil tankers hit naval
   mines in the Strait of Hormuz. (Reported 26 Nov.)
2. **UKRAINE — oil war.** Ukraine strikes Russian oil refineries;
   Putin vows retaliation; the US shelves proposals to use business
   deals with Russia to end the war. (26 Nov.)
3. **GAZA — ceasefire under strain.** Israel strikes a Hamas official
   in Gaza. (26 Nov.)
4. **SPACE — Pakistan's first astronaut.** Pakistan's Muhammad Zeeshan
   Ali joins China's Shenzhou-24 mission to the Tiangong space
   station — the first foreign astronaut on it. (26 Nov.)
5. **INDIA — Mumbai remembers 26/11.** 18th anniversary of the Mumbai
   terror attacks; India also marks Constitution Day (Samvidhan Divas).
   (26 Nov.)
6. **ALSO TODAY —** a fuel tanker crash ignites a fire in Cairo
   killing at least 30; Gukesh draws with Sindarov in game 2 of the
   World Chess Championship; 15-year-old Vaibhav Sooryavanshi smashes
   the fastest List A double century (204 off 53 balls); a
   5.6-magnitude earthquake hits Nepal's Koshi Province; close-up
   images reveal a new crater from Earth's asteroid defence test.

## How it runs

`main.py` is stdlib only (hashlib, os, struct, sys, zlib, pathlib). It
loads the vendored `entry.png`, validates the PNG signature, IHDR
(1024×1024, 8-bit, palette), every chunk's length and CRC through
IEND, the 1 MiB size cap and the sha256 digest, then copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Run twice, the outputs are
byte-identical.

## License

MIT — see `LICENSE`.
