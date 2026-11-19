# Credits

"OTM Trio": three OTM videos joined into one Instagram Reel, in English (about 104 s) and Thai (about 109 s):

1. "The Last $1,000" (`otm-thousand`, `otm-thousand-th`): protect a small account, risk 1% or less, one setup.
2. "Stop Strategy Hopping" (`otm-hopping`, `otm-hopping-th`): stick with one strategy long enough to let it work.
3. "The Skill of Doing Nothing" (`otm-nothing`, `otm-nothing-th`): the market pays for being picky, not busy.

The first two are cut where their "Order the market..." outro line begins, so the outro (emblem, handles, educational
line) appears once, at the end of the third video; there is no end card. Each join is a short dip to black (0.4 s), and
the next part starts with its own opening line.

Everything (scripts, voices, visuals, sound effects, font) comes from the three projects; see their CREDITS.md files.
Music: none.

Rebuild: render the six projects (`npx hyperframes render -o renders/<project>.mp4`), then
`bash otm-trio/combine.sh en ROOT otm-trio_reels.mp4` and `bash otm-trio/combine.sh th ROOT otm-trio-th_reels.mp4`,
where ROOT is the folder holding the six project folders.
