---
name: film
description: Make or edit a short concept video in film_studio (Manim, minimal TRON style) from a brief, through four validated gates — G1 brief & acts, G2 stills, G3 animatic, G4 polish + final. Use when the user wants to start a new film from a presentation/research doc, iterate on an act, render drafts or a final, or check the legacy film still renders identically.
---

# Film workflow

Skeleton (Phase 0). Gates G2–G3 need the Film/Act/Beat engine (Phase 4); until then only legacy films exist.
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

## G2 — Stills *(Phase 4)*
Write each beat as a screen *state* (actors, positions, text, what is lit). `studio still <film>` → one frame
per beat on a sheet. Iterate on layout and wording here, not in animation.

## G3 — Animatic *(Phase 4)*
`studio animatic <film>` → 480p with default transitions (paired morph, fade). Validate pacing and story.

## G4 — Polish & final
Add custom motions only where they carry the concept. Per-act loops (`studio act`, `studio range`).
`studio final <film> --validated` only after the user explicitly validates.

## Legacy film
`ai_retrieving_dynamic_data` is the reference film. After touching the kit, pipeline or its scene:
`studio regress ai_retrieving_dynamic_data` must report IDENTICAL for EN and FR.

## Files
- `lessons.md` — design rules learnt so far (update when the user gives new design feedback).
- `checklist.md` — self-check list before showing a render.
