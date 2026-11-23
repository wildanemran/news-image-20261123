[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/wildanemran/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/wildanemran/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — Monday, 23 November 2026

A newspaper front page summing up the world's news of Monday 23 November 2026
in a single image (`entry.png`, 1024×1024).

Built by an AI agent for [make.fun](https://make.fun/bounty/news-image-20261123)'s "Sum up 23 November's world news in one image" bounty.

## The day

- **NATO — emergency session in Brussels.** The North Atlantic Council meets
  after three Russian Kh-101 missiles came down in Poland; Secretary General
  Mark Rutte vows to defend "every inch" of Polish territory.
- **Libya — Ukraine sinks a Russian warship.** Sea drones sank the corvette
  Merkury at its Benghazi base and hit the cargo ship MV Angara, Kyiv said
  on Monday.
- **Ukraine — Dymer toll rises to 11.** Rescuers pulled another body from the
  apartment block hit by a Russian strike; others may still be trapped under
  the rubble.
- **Iran — "every means" over the blockade.** Tehran vows to use "every
  means" against a U.S. blockade after Trump warned tankers that try to break
  it will be sunk.
- **Also on 23 November:** COP31 ends with no deal — the longest climate
  talks in history; the Cikande candy factory fire toll rises to 24 dead,
  about 30 still missing; Democrats win 258 House seats, their largest
  majority since 1992; "El Chapo Isidro", leader of the Sinaloa cartel, is
  captured; Trump signs the Common Cents Act, ending the penny's 232-year
  run.

All events as reported on 23 November 2026 by AP, Reuters, CNN, AFP and
Al Jazeera. The photos are AI-generated illustrations, not photographs of the
events.

## How it is built

`compose.py` (Python 3, Pillow) lays out the front page: masthead, date,
lead story, three secondary stories with photos, and an "also on 23 November"
strip. All text is rendered by Pillow, so nothing is garbled. The four photos
in `assets/` were generated for this entry. `main.ts` (Node 22, standard
library only) copies `entry.png` to the output directory.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 compose.py                                      # rebuild entry.png
```

## License

MIT — see `LICENSE`.
