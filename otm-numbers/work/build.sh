#!/bin/bash
# assemble gen.py: doc.txt + the scene system head of otm-missed + _scenes.py (LANG + the shared "Know Your Numbers" scenes)
# + the shared tail (no end card), with FONTS (Kanit @font-face for Thai, empty for English) prepended to the CSS
set -e
cd "$(dirname "$0")"
G=${1:-../../otm-missed/work/gen.py}
L=$(grep -n "^def ix(i):" $G | cut -d: -f1); M=$(grep -n "end card, dust, ground, emblem" $G | cut -d: -f1)
{ cat doc.txt; sed -n "7,$((L-1))p" $G; cat _scenes.py; echo; echo; sed -n "$M,\$p" $G | sed 's/otm-missed/otm-numbers/g; s/mix_missed/mix_numbers/g; s/^CSS = """/CSS = FONTS + """/; s/<html lang="en"/<html lang="en"/'; } > gen.py
