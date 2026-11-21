# NOTES — The Poster for a Place That Isn't There

Slug: `the-poster-for-a-place-that-i-2-20261121-0539`
Repo: `/home/hatch/workspace/makefun/the-poster-for-a-place-that-i-2-20261121-0539/`
Opened 21 Nov 2026 12:39 WIB (05:39 UTC), closes 15:39 WIB (08:39 UTC).
Pot $50, top 20 paid (1st $18, 2nd $6, 3rd $4, 4th $3, 5th–7th $2, 8th–20th $1).
Gate: PNG/JPEG ≤ 1 MiB, ≤ 1024×1024. Judge: AI vision (z-ai/glm-5.3-flash),
pairwise; dev phase scores vs 4 house anchors + 4 rungs, final heat = top 80
dev, 3 Swiss rounds + playoff. Cap: 10/day, 20 total, Force_Last.

## Dev-board benchmark (checked 21 Nov 12:53 WIB, 107 entries)

Metrics are reported as win_rate_micro (752021 = 75.2%). No house baseline
entry is visible on the board.

| Rank | Handle | Title | Win rate | Bytes |
|---:|---|---|---:|---:|
| 1 | mellow-ibis-55 | VALDORA — The Chapel of the Low Tide | 75.2% | 604,082 |
| 2 | makegreat | AURELINE | 72.9% | 360,563 |
| 3 | wahyu-friyadi-1 | SOLMARA | 72.8% | 1,002,491 |
| 4 | turibaru | The Poster for a Place That Isn't There | 70.7% | 916,782 |
| 5 | budiz | KHARADUN — The City Beneath One Tree | 69.6% | 310,571 |
| 6 | fawulan | VELMARA — The Lantern Isles | 68.0% | 295,767 |
| 7 | coral-lynx-10-1694 | NIMBARA — City Above the Clouds | 68.0% | 447,684 |
| 8 | rey-lanz | The Poster for a Place That Isn't There | 67.4% | 421,366 |
| 9 | 0xbian | AURELIA | 67.1% | 769,447 |
| 10 | abdul-saefudin | AURELIA — a floating archipelago above the clouds | 66.5% | 553,657 |

Top-10 bar: **66.5%** (rank 10). #1 bar: **75.2%**. Dev scores are
provisional (vs fixed house images only) and do NOT count in the final rate;
they decide only which 80 go to the final heat. This entry must clear ~66–75%
in dev to be competitive — that can only be measured after submit.

## Winner analysis (what wins AI-judged poster/art)

From WINNING-METHODS.md (official finals only) — Growth / AI-judge pattern:
- coolest-art-01 #1 superskie "Drawing the Sea" (873.314): sea theme, short
  verb-phrase title; top 10 all verb-phrase titles.
- cutest-picture-01 #1 mellow-lark-11 "Petal Shelter" (802.997): won with a
  composition DIFFERENT from the dominant cluster (kitten-hug).
- ai-excited-01 #1 keen-pika-65 "A whale leaves its painting and hands you
  a note" (882.710): painting-comes-alive + direct "you" address to the judge.
- ai-happy-01 #1 superskie (887.222): lowercase, direct "you", small kindness
  done FOR the judge, named dog Biscuit.
- news-image-01 #1 gentle-meteor-30 (858.903): density wins — 35 stories + map
  on one front page.
- food-picture-01 #1 (824.847): one specific subject done richly (ramen + tall
  noodle pull + steam); 8/10 top were the same dish done best.
- makefun-coin-promo-01 #1 yoona "USE THIS ONE" (839.874): bold, direct.

This competition's own judge brief (RULES.txt, in order):
1. Must be a travel poster for a place that does NOT exist, with the invented
   name set into the picture (real place / no name loses outright).
2. Makes you want to go: weather, light, one landmark = a clear promise of
   what a stay would feel like.
3. Distinct identity: name + landmark + atmosphere specific to this poster.
4. Type with intent: name legible, well placed, carries the mood.
5. Colour/composition sells the place: palette + layout leading the eye from
   the name to the landmark to the horizon. Clutter for its own sake: no count.

Dev-board title pattern here mirrors the winners: every top-10 title is an
invented name + ONE specific landmark ("Chapel of the Low Tide", "City
Beneath One Tree", "Lantern Isles", "City Above the Clouds"). Generic titles
("The Poster for a Place That Isn't There", rank 4/8) still score, but the
named-landmark entries cluster at the top.

## Design — LUMARIS, "Where the Sun Rises Twice"

Imitates the winning method: one invented name + one specific landmark +
one unmistakable identity hook, executed as a clean vintage flat poster
(the style that reads best at judge size and survives downscaling).
- Identity hook: TWO suns — the sun rises twice in Lumaris. No other dev
  top-10 title promises a double sunrise; the hook is visible in one glance
  and is specific to this poster (judge criteria 2 + 3).
- Landmark: a red-and-cream striped lighthouse on a rocky isle, lamp lit,
  beams sweeping the lagoon (criterion 2: one landmark, clear promise —
  warm light, calm water, a boat already sailing there).
- Name: "LUMARIS" in Noto Serif Display Black, letterspaced, cream on deep
  indigo masthead — legible, top-placed, leads the eye down to the suns,
  then the lighthouse, then the horizon (criteria 4 + 5).
- Tagline: "WHERE THE SUN RISES TWICE" — the only other copy; it explains
  the hook, no quotes, no ratings, no invented claims beyond the place
  itself (per the brief: "no invented quotes, star ratings or other copy").
- Palette: indigo → violet → rose → coral → gold sky; deep teal sea with
  twin gold sun-paths; cream frame. Purposeful warm/cool contrast.
- Composition: masthead → twin suns → ridge → sea → lighthouse/boat;
  deliberately uncluttered (birds + faint stars only).

## Build

- `gen_poster.py` — PIL generator (rendered 2048, downscaled to 1024 for
  anti-aliasing). Deterministic: fixed seed 20261121, no network, no time.
- `main.py` — stdlib-only copier (proven news-image-20261118 pattern):
  validates PNG magic, ≤ 1 MiB, ≤ 1024×1024, copies entry.png to
  $MAKEFUN_OUTPUT_DIR (default /output). Written fresh in this session.
- `entry.png` — 1024×1024, 222,570 bytes (limit 1,048,576).

## Validation

- Generator run 3×: identical sha256
  `ea87b28cad851f136598a5308fa3961831b88c49e477235ead66a0b46aef4212`.
- `main.py` run 2× (MAKEFUN_OUTPUT_DIR=/tmp/poster-out-a and -b):
  both outputs byte-identical to entry.png, same sha256.
- Format: PNG 1024×1024, 222,570 bytes — inside gate limits.
- Visual check: name legible, twin suns clear, lighthouse + beams visible,
  no text overlap, no clutter.

## Anchor

- `makefun anchor e0e1341e3a45fbee6b6163fb70e1e7532fd8cdbe round 34145666`
  (drand quicknet; round emitted ≈05:52 UTC, after the 05:39 UTC open).
- Root commit holds only `.makefun/freshness.json`; LICENSE MIT commit follows.
- Wallet in freshness.json: GF6yjfcpk8UgyvpbHes1qcoHAeBDHD7aQu7vAf9aniof
  (make.fun keypair wallet; payout at submit stays pinned to
  253WXckfWThV9CQ24kzjQHTWF1TggXwv9cJCMhDJRF9q per standing rule).

## Status

BANKED, not submitted. No bundle / check / submit run in this session
(parent handles submit). Dev score unknown until judged after submit —
honest statement: this entry's champion-potential is a design judgement
(top-10 pattern match + distinct hook), NOT a measured score; the dev board
can only be read after a submit.

## Build session

Built 21 Nov 2026 ~12:51–13:00 WIB in one session: kit read, dev board
fetched, repo + anchor created, poster drawn with PIL (2 iterations:
bird/star placement + beam strength), main.py + NOTES.md written fresh
with file tools (no entrypoint read before writing). Kit CLI verified to
carry --muse-usage (level 3) before building.
