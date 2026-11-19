[![Competition](https://make.fun/api/badges/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun](https://make.fun/api/badges/makefun.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![Entry](https://make.fun/api/badges/entry.svg)](https://make.fun/bounty/gta6-meme-x-01)

# Post a GTA 6 meme on X — our entry for gta6-meme-x-01

This repository is an entry for the make.fun bounty **"Post a GTA 6 meme on
X"**. The entry is a single post on X: a homemade GTA 6 meme whose picture
carries the make.fun ghost, posted from a public account with a caption
that tags @makefunai, links the bounty page and carries our play code. The
house reads the post back from X and an AI judge compares entries two at a
time — make.fun visible in the picture first, then the joke, the GTA 6
flavour, the pitch, the caption and the polish. The top 50 split $500.

make.fun is where people and their AI agents enter paid bounties and earn
real money when they place — which is exactly the joke all three memes
tell: while everyone else just waits for GTA VI, our agent is already
getting paid.

## The three meme options

Only one gets posted; the other two stay here as spares. All three are
1200×1200 PNGs in `meme/`, built with `tools/compose.py`: an AI-generated
Vice City / Leonida scene, the official make.fun ghost mark from the press
kit composited large, and the caption text rendered on top.

1. **Waiting** — `meme/meme-1-waiting.png`. Split panel: a skeleton at a
   cobwebbed desk, "WAITING FOR GTA VI SINCE 2013", over a neon Leonida
   sunset where the ghost is already surrounded by coins: "MY AI AGENT:
   ALREADY EARNING ON make.fun".
2. **Wasted** — `meme/meme-2-wasted.png`. A GTA death-screen homage over a
   red-washed Leonida beach: "WASTED — 12 YEARS WAITING FOR GTA VI", the
   ghost respawning next to a game-UI box that reads "BOUNTY COMPLETE
   +USDC - RESPAWNED ON make.fun".
3. **Six stars** — `meme/meme-3-sixstars.png`. A rainy neon street, police
   lights behind, and a wanted HUD showing **six** stars — one more than
   GTA ever allows: "THE 6TH STAR: HE EARNS FROM BOUNTIES NOW". The ghost
   carries a money bag.

Matching ready-to-post captions (each ≤ 280 characters, with the tag, the
link and the play code) live in `CAPTIONS.md`.

## How the entry flows

1. Pick one meme and post it on X from a public account, first picture =
   the meme, text = its caption from `CAPTIONS.md`.
2. Put the post's URL in `POST.json` at the repository root, e.g.
   `{"url": "https://x.com/<handle>/status/<id>"}` (it currently holds a
   placeholder).
3. Submit this repository with that commit; `main.ts` hands the grader a
   copy of `POST.json`, and the transcripts of the sessions that made the
   meme go up with the submission.

## Running main.ts locally

Needs Node 22, standard library only:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

That creates `out/POST.json`. Without the environment variables the
program uses the grader's defaults: it reads `/bot/POST.json` and writes
`/output/POST.json`, exiting 1 with an error naming POST.json if the copy
fails.

## Rebuilding the memes

```sh
python3 tools/compose.py
```

The script composites the generated scene backgrounds with the official
ghost mark (`mark-1024.png` from the make.fun press kit) and renders the
text with PIL in DejaVu Sans Bold.
