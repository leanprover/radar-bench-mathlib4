#!/usr/bin/env bash
set -euo pipefail

BENCH="$PWD"
REPO="$1"
OUT="$2"

cd "$REPO"
lean --version # install and sanity check
touch build_upload_lakeprof_report

if [ -d "scripts/bench-radar" ]; then
  echo Using the bench-radar suite
  timeout -s KILL 4h scripts/bench-radar/run
elif [ -d "scripts/bench" ] && [ -f "scripts/bench/README.md" ]; then
  echo Using the bench suite
  timeout -s KILL 4h scripts/bench/run
else
  echo Bringing my own copy of the bench-radar suite
  cp -r "$BENCH/bench-radar" scripts/bench-radar
  timeout -s KILL 4h scripts/bench-radar/run
fi

mv radar.jsonl "$OUT"
