---
name: film
description: Make or edit a short concept video in film_studio (Manim, minimal TRON style) from a brief, through four validated gates — G1 brief & acts, G2 stills, G3 animatic, G4 polish + final. Use when the user wants to start a new film from a presentation/research doc, iterate on an act, render drafts or a final, or check the legacy film still renders identically.
---

# Film workflow

Skeleton (gates detailed in Phase 5). New films are engine films: `studio new <name>`.
Read `CLAUDE.md` (rules + commands) and `lessons.md` (design rules) before any change.

## Every gate
1. Ask ≤4 multiple-choice questions (recommended option first). Wait for answers.
2. Commit the current state before changing anything.
3. Build, render the smallest useful scope (one act / range, 480p).
4. Self-check: `studio sheet` / `studio frames` on the render, look at the frames, fix obvious issues first.
5. Show the user the loop page or sheet. Stop and wait for validation. Never skip ahead.

## G1 — Brief & acts
Input: a presentation or research doc. Output: `films/<name>/brief.md` from `films/_template/brief.md`
(audience, the one idea, 3–6 acts, one key image per act, vocabulary, actors). Settle open points with MCQs.

## G2 — Stills
Write each beat as a pure screen *state* `{id: mobject}` (actors, positions, text, what is lit), no motion.
`studio still <film>` → one PNG per beat, sheet, stills.html (seconds). Iterate on layout and wording here.

## G3 — Animatic
`studio animatic <film>` → 480p with default transitions (same id morphs, new fades in, missing fades out;
`morph_from` pairs ids). Tune `hold` / `run_time`. Validate pacing and story.

## G4 — Polish & final
Add `motion=` to a beat only where it carries the concept (`studio dev` / `act` render full mode). Per-act loops (`studio act`, `studio range`).
`studio final <film> --validated` only after the user explicitly validates.

## Legacy film
`ai_retrieving_dynamic_data` is the reference film. After touching the kit, pipeline or its scene:
`studio regress ai_retrieving_dynamic_data` must report IDENTICAL for EN and FR.

## Kit
Build scenes from `studio/kit` (see `gallery/README.md` for every piece). Prefer an existing actor/motion;
add a new one only when a pattern repeats twice, with a gallery still.

## Files
- `lessons.md` — design rules learnt so far (update when the user gives new design feedback).
- `checklist.md` — self-check list before showing a render.
