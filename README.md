# The World in One Day — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026, built
for the make.fun news-image-20261119 bounty: a newspaper front page on
cream paper, 36 verified stories, 13 original illustrations drawn in code,
a dotted world map with numbered pins, and a DATE CHECK box that names the
big stories deliberately left out because they happened on another day.

This is the v3 rebuild. The v2 entry scored 98.01% (rank 933/11,653) but
hit the ceiling of a text-only template: it carried two 18 November stories
as 19 November news (the EU's €45bn loan to Kyiv, the Van Gogh $190.4m
sale), the wrong Anthropic figure ($79.4bn instead of $81.3bn), five
consensus stories missing entirely, and zero illustrations, zero map, zero
DATE CHECK. v3 fixes all of that by following the winner template shared by
all 15 top-5 images across the news-18/19/20 bounties.

## The day, in 36 stories

- **Heroes:** (1) Trump, Xi and Putin meet in Shenzhen — the first
  three-way summit; (2) GTA VI launches — 24.5m copies on day one;
  (3) Anthropic's record $81.3bn IPO — 980m shares at $83, the biggest
  listing ever, topping SpaceX's $75bn.
- **Feature cards (4–13):** the World Court finds Myanmar committed
  genocide, 9–6; the COP31 draft drops all fossil-fuel language and admits
  1.5°C will be missed; Cyclone Akvan bears down on India (200,000
  evacuated); Korea goes quiet for the Suneung (551,864 sitting); Florida
  drowns in 15 inches of rain; Colombia strikes over the tax bill; a
  missile threat over Riyadh ends in all-clear; Australia's jobless rate
  hits 4.9%, a five-year high; Putin invites Europe to Moscow, Merz says
  talks yes, Moscow no; the IEA calls the Mideast crisis the worst energy
  threat in history.
- **Also on Thursday (14–36):** the Senate backs Trump on Iran war powers
  51–48; the White House cyber chief is fired after the outages; California
  subpoenas Nvidia; Indonesia's asset forfeiture law; the Greenland pact
  ratified 109–0; APEC's Shenzhen Outlook; Ukraine left off the Shenzhen
  agenda; the Greens rally behind Mélenchon; Jepchirchir banned 3 years
  for EPO; 589m children now live in war zones; and more.
- **DATE CHECK:** the EU loan, the Van Gogh sale, the Libya seizure,
  Voyager 1, the CMA Awards and the Pew study are all 18 November news and
  are excluded on purpose; Akvan's landfall and the COP31 final deal had
  not happened yet.

Every story carries its event date and source in `stories.json`. The iron
rule of this rebuild: a story's date is when the event happened, never the
date of the article reporting it.

## How it is built

`build_frontpage.py` (Python 3, Pillow) draws the whole page from
`stories.json` — cream paper, a navy band, one accent red, and 13 flat
vector illustrations drawn in code (summit table, Vice City sunset, IPO
candlesticks, courthouse and scales, globe and thermometer, cyclone
spiral, exam desk, flooded house, strike banner, Riyadh towers, jobless
bars, crossed-out Kremlin, oil drop) plus a dotted world map. No
photographs, no AI images. See `DESIGN.md` for the design philosophy.

`main.ts` (Node 22, standard library only) copies the finished front page,
`entry.png` (1024×1024 PNG, 217,091 bytes), to `/output/entry.png`. No
network, no clock, no randomness — both grading runs produce identical
bytes (sha256 57f6b82374ef4fe6147bec1666c7874a557582179be82952d21b51783ff350a2).

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Rebuild the image from its sources:

```sh
python3 build_frontpage.py
```
