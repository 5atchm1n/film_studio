# G4 — Polish & final

Goal: custom motion **only where it carries the concept**, act by act; then the final render after explicit
validation. Output: `motion=` on chosen beats, `studio act` loop pages, `studio final <name> --validated`.

## Steps
1. **Questions (≤4)**: from the G3 list, which beats get a motion and what it should show (packet along the
   rails, a call lighting one path, a piece rising to the title, details condensing…).
2. Write `motion(sc, prev, cur)` for one beat at a time:
   - Prefer kit motions: `send` + `packet`, `flash_along`, `highlight`, `dim`/`light`, `morph_anims`,
     `condense_anims`, `words_anims`; `transition_anims(prev, cur, skip=…)` for everything the motion does not handle.
   - Whatever it plays, the engine then shows exactly `cur`: the motion ends where the still is.
   - `with sc.exact():` for packets / typing (no minimum duration stretch).
3. `studio act <name> <act>` (full mode, 480p, looping). Self-check frames around the motion.
4. **Show** the act's loop page. Stop. Next act only after validation.
5. All acts validated → `studio dev <name>` (whole film, EN) + `--lang fr`; show. Stop.
6. **Final only on explicit validation**: `studio final <name> --validated` (and `--lang fr` if wanted) →
   `out/<name>/final-<lang>/<Title>.mp4 + .html`. Self-check the final with `studio sheet`. Show.

## Exit
User validates the final. STATUS.md: G4 ✓, final files, date. Commit "Final: <title>". Push only if asked.
New reusable motion? Move it into `studio/kit/motions.py` + gallery still.

## Pitfalls seen before
- Motion for its own sake (glitches, gratuitous camera moves) — academic, minimal.
- Lit copies stacked over base paths (brighter where they overlap) — recolour in place.
- Forgetting that the final must match the validated 480p: no last-minute changes in the final step.
