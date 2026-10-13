# G3 — Animatic (default transitions)

Goal: validate the story order and pacing with the engine's default transitions only — no custom motion yet.
Output: `studio animatic <name>` (480p, looping player with chapters, scrubber, frame stepping).

## Steps
1. **Questions (≤4)**: target total length, which beats deserve more time, which transitions read wrong.
2. `studio animatic <name>` (or `--act <act>` while tuning). Default transition by id: same id morphs,
   new fades in, missing fades out; `morph_from` pairs ids.
3. Tune without motion code: `hold=` (reading time), `run_time=` (transition), ids and `morph_from` (what turns into
   what), beat order. A piece that should travel = same id in both beats at different positions.
4. **Self-check**: `studio frames <video> --every 1` around changes; total length vs brief; chapter times sensible.
5. **Show** the loop page. Stop.

## Exit
User validates order and pacing. STATUS.md: G3 ✓, duration, list of beats that still need a custom motion (with
the reason the default does not carry the concept). Commit "G3: animatic validated".

## Pitfalls seen before
- Changes in two places at once read as noise: one thing changes per beat.
- A morph between unrelated pieces confuses — give them different ids (fade) instead.
