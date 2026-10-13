---
name: film
description: Make or edit a short concept video in film_studio (Manim, minimal TRON style) from a presentation or research doc, through four validated gates — G1 brief & acts, G2 stills, G3 animatic, G4 polish + final. Use when the user wants to start a new film, resume one, iterate on an act or beat, render drafts or a final, or check that the legacy film still renders identically.
---

# Film workflow

A film goes through four gates. Each gate ends with the user's explicit validation; never start the next one before.

```
source (pptx/pdf/md) ─extract─▶ G1 brief & acts ─▶ G2 stills ─▶ G3 animatic ─▶ G4 polish ─▶ final
                                  brief.md          states only    default        custom motion   1080p + HTML
                                                    PNG per beat   transitions    where it carries
```

## Start (every session)
1. Read `CLAUDE.md` (rules, commands) and `lessons.md` (design defaults).
2. Which film? `studio list`. New film → `studio new <name>`, then G1.
3. Read `films/<name>/STATUS.md`: current gate, decisions already taken, open questions, next step.
   Then read the gate file below for the current gate — and only that one.

| Gate | File | Output | Exit = user validates |
|---|---|---|---|
| G1 | `g1_brief.md` | `brief.md` (+ `source.md`) | the one idea, the acts, the key image per act |
| G2 | `g2_stills.md` | beat states in `film.py`, `studio still` page | every beat's layout and words |
| G3 | `g3_animatic.md` | `studio animatic` loop page | story order and pacing |
| G4 | `g4_polish.md` | custom motions, `studio dev/act`, then `studio final --validated` | each act's motion, then the final |

## The loop inside every gate
1. **Ask** ≤4 multiple-choice questions (recommended option first). Do not re-ask what STATUS.md already settled.
   Plain words; when an option involves a technical concept, show a concrete example of what it means first.
2. **Commit** the current state before changing anything (`git commit`; never push unless asked).
3. **Build** the smallest useful scope: one act (`--act`), stills before motion, 480p before 1080p.
4. **Self-check** with `checklist.md`: look at the sheet / sampled frames, fix obvious issues yourself first.
5. **Show** the page (stills.html or the loop player) and **stop**. Wait for validation or feedback.
6. **Record** in STATUS.md: what was validated (date), decisions, feedback. Design feedback that should apply to
   future films → one line in `lessons.md`. Commit.

Feedback loops back to step 1 inside the same gate. A change that invalidates an earlier gate (e.g. a new act at G3)
goes back to that gate: update brief.md / stills first, then re-validate.

## Always
- Keywords on screen, never sentences; no precise business figures unless the source gives them.
- Build from the kit (`gallery/README.md` shows every piece). New actor/motion only when a pattern repeats twice —
  add it to `studio/kit`, give it a gallery still (`studio gallery`).
- English source text; every on-screen string gets its FR entry; check `--lang fr` stills before G3 exit.
- Kit / engine / pipeline touched? `studio regress ai_retrieving_dynamic_data` (the reference film) must say IDENTICAL.
- Never render or announce a final without explicit validation of the 480p version.

## Files
- `g1_brief.md` · `g2_stills.md` · `g3_animatic.md` · `g4_polish.md` — one per gate.
- `lessons.md` — design defaults learnt so far. `checklist.md` — self-check before showing anything.
- `films/_template/` — brief.md, STATUS.md, film.py, film.toml (copied by `studio new`).
