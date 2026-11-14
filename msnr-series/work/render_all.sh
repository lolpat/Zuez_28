#!/bin/bash
cd "$(dirname "$0")/.."
r() { (cd eps/ep$1 && npx hyperframes render -o ../../renders/MSNR_ep$1.mp4 --quality delivery --skill hyperframes > ../../renders/ep$1.log 2>&1; echo "ep$1 exit $?"); }
for g in "0 1 2" "3 4 5" "6 7 8"; do for e in $g; do r $e & done; wait; done
