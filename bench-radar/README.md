# Mathlib4 benchmark suite

This directory contains the mathlib4 benchmark suite.
It is built around [radar](github.com/leanprover/radar)
and benchmark results can be viewed on the [Lean FRO radar instance](https://radar.lean-lang.org/repos/mathlib4).

To execute the entire suite, call the `run` script in this directory.
To execute an individual benchmark, call the `run` script in the benchmark's directory.

## Benchmarks

### The `build` benchmark

This benchmark executes a complete build of mathlib4 and collects global and per-module metrics.

The following metrics are collected by a wrapper around the entire build process:

- `build//instructions`
- `build//maxrss`
- `build//task-clock`
- `build//wall-clock`

The following metrics are collected from `leanc --profile` and summed across all modules:

- `build/profile/<name>//wall-clock`

The following metrics are collected individually for each module:

- `build/module/<name>//lines`
- `build/module/<name>//instructions`

## The `lint` benchmark

This benchmark runs `lake exe runLinter Mathlib`.
It measures the following metrics:

- `lint//instructions`
- `lint//maxrss`
- `lint//task-clock`
- `lint//wall-clock`

## The `open-mathlib` benchmark

This benchmark approximates `import Mathlib` in the editor by running `lake lean Mathlib.lean`.
It measures the following metrics:

- `open-mathlib//instructions`
- `open-mathlib//maxrss`
- `open-mathlib//task-clock`
- `open-mathlib//wall-clock`

## The `size` benchmark

This benchmark measures a few deterministic values.

- `size/.lean//lines`
- `size/.olean//bytes`
- `size/porting notes//lines`
