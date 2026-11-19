# The World in One Day — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026, built
for the make.fun news-image-20261119 bounty: a newspaper front page with the
day named in a red date band and 39 verified stories from that day.

This is the v2 rebuild of the entry first submitted 19 Nov 16:42 WIB (judge
97.21%, rank 2,791/6,850). The rebuild answers the two gaps the leaderboard
showed: the old file was 959,336 bytes — above the top-50 maximum — and it
carried only 11 stories against a top-50 median of 40. This version has 39
verified stories and a 172,258-byte file.

## The day, in 39 stories

- **Hero — Shenzhen:** Trump, Xi and Putin hold their first three-way summit
  at APEC; Ukraine and nuclear arms top the agenda.
- **Top stories:** the International Court of Justice rules on the Rohingya
  genocide case; Ukraine's allies meet in Berlin; Kyiv hits the Crimean
  Bridge for the third time in a week; COP31 ministers race to unblock the
  climate deal; Anthropic raises a record $79.4bn in its stock market debut;
  Trump unveils $17bn of South-East Asia deals; GTA VI launches; a
  cyberattack hits the European Commission.
- **Around the world:** Indonesia passes its asset forfeiture law; Cyclone
  Akvan threatens India's east coast; Malaysia ends visa-free entry for
  Indians; India and Japan speed up their defence pact; the ancestral home
  of Muhammad Yunus is torched in Bangladesh; Denmark ratifies the Greenland
  pact 109-0; UK inflation hits a 12-month high; Italy passes its
  antisemitism law; UniCredit seals the €41bn Commerzbank pact; French women
  "work free" from 10:51; Walmart beats forecasts; the Dow drops 561;
  Fed minutes point to more rate rises; Google launches Gemini 4 Neon;
  Nvidia halts H200 shipments to China; Israel ends its Gaza tank raid;
  Egypt seals a $2.3bn IMF deal; Ruto proposes tax-free low pay; Senegal's
  ruling party expels its own president; Nigeria gets US intelligence help.
- **Also today:** the IAEA on North Korea's uranium enrichment; a Russian
  military plane crash in Siberia (19 killed); a Van Gogh selling for
  $190.4M (an artist record); the EU–Indonesia trade pact; Estonia shutting
  its Russia border crossings from 1 December; Takaichi and Xi shaking hands
  at APEC; Modi urging industry to put "India First"; South Korea urging
  talks with the North; a GAO report on chatbots drawing up attack plans;
  the Webb telescope eyeing a star that swallowed its companion.

Every story was verified against reports of the day (two sources where
possible); the full list with sources is in `stories.json`.

## How it is built

`build_frontpage.py` (Python 3, Pillow) draws the whole page from
`stories.json` — flat colours, one accent red, a hand-drawn Shenzhen
skyline in place of a photograph, so the PNG stays small. The design
follows the 21st.dev language: a neutral base with one accent, tight
display headings, small-caps eyebrow labels, soft 1px rules. See
`DESIGN.md` for the design philosophy.

`main.ts` (Node 22, standard library only) copies the finished front page,
`entry.png` (1024×1024 PNG, 172,258 bytes), to `/output/entry.png`. No
network, no clock, no randomness — both grading runs produce identical bytes.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Rebuild the image from its sources:

```sh
python3 build_frontpage.py
```
