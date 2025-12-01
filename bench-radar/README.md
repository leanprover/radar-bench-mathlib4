# Mathlib4 benchmark suite

This directory contains the mathlib4 benchmark suite.
It is built around [radar](github.com/leanprover/radar)
and benchmark results can be viewed on the [Lean FRO radar instance](https://radar.lean-lang.org/repos/mathlib4).

To execute the entire suite, call the `run` script in this directory.
To execute an individual benchmark, call the `run` script in the benchmark's directory.
Some scripts output their measurements on stdout or stderr with the prefix `radar::measurement=`
while other scripts output their measurements in the file `radar.jsonl`.

The `*.py` symlinks exist only so the python files are a bit nicer to edit
in text editors that rely on the file ending.
