# The World in One Day — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/LecialiArthelais/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026, built
for the make.fun news-image-20261119 bounty: a newspaper front page with the
day named in a red date band and eleven verified stories from that day.

## The day, in six stories

- **Hero — Shenzhen:** Trump, Xi and Putin hold their first three-way summit
  at APEC; Ukraine and nuclear arms top the agenda.
- **The Hague:** the International Court of Justice rules on the Rohingya
  genocide case, Gambia v. Myanmar.
- **Ukraine:** Kyiv strikes the Crimean Bridge for the third time in a week;
  the EU proposes a €45bn loan.
- **Antalya:** COP31 ministers race to unblock the climate deal and agree a
  final text.
- **Markets:** Anthropic raises a record $79.4bn in its stock market debut.
- **Culture:** GTA VI launches — the year's biggest game release arrives.

The "Also today" strip adds five more: the IAEA on North Korea's uranium
enrichment, a Russian military plane crash in Siberia (19 killed), a Van Gogh
selling for $190.4M (an artist record), the EU–Indonesia trade pact, and
Estonia shutting its Russia border crossings from 1 December.

## How it is built

`main.ts` (Node 22, standard library only) copies the finished front page,
`entry.png` (1024×1024 PNG, 959,336 bytes), to `/output/entry.png`. No
network, no clock, no randomness — both grading runs produce identical bytes.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
