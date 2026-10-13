# G2 — Stills (states only, no motion)

Goal: every beat as one frame — layout, words, what is lit — validated before any animation.
Output: beats in `films/<name>/film.py` (states only, no `motion=`), `studio still <name>` page.

## Steps
1. **Questions (≤4)** only on what the brief leaves open: layout of the key images, which actor stands for what,
   order of beats inside an act.
2. **Write states**, one act at a time. In `film.py`:
   - `Act(name, "01 · TITLE", "Toc name", [Beat(...), …])`, short English act names (`studio act <film> <name>`).
   - `Beat(name, state, note="…")`; `state(st)` returns `{id: mobject}` — pure, fresh mobjects every call.
   - Keep the **same id** for the same thing across beats (that is what will morph at G3); `morph_from` when a
     piece becomes another (block → word). Order of the dict = drawing order.
   - Positions from `studio.kit.layout` anchors (chat left · chip centre · panel right · band · data).
   - Dim what is not relevant yet (`set_opacity`, `DIMC` rails); light only what this beat is about.
   - Every on-screen string through `st.tr(...)` / `st.L(...)`; add its FR entry.
3. `studio still <name> --act <act>` (seconds). Self-check the sheet with `checklist.md`.
4. When all acts are drafted: `studio still <name>` and `studio still <name> --lang fr`.
5. **Show** stills.html (the user can comment beat by beat: numbers are stable). Stop.

## Exit
User validates every beat (layout + words). STATUS.md: G2 ✓, beat list, decisions. Commit "G2: stills validated".

## Pitfalls seen before
- Text too small at 480p (check the sheet tile: if unreadable there, it's too small).
- Too much on screen: condense what has been explained; drop the example once the concept is built.
- Stacked semi-transparent copies to "highlight" — recolour the piece itself (`motions.highlight`).
