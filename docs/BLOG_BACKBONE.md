# Blog backbone — "AI - Retrieving dynamic data"

> Copied from `visuels_mcp_harness/docs/` (@ 6fb3c32, 13 Oct 2026) into film_studio (Phase 6). Paths such as `_archives/…`, `../film.py` or `../ETAT_PROJET.md` refer to `../visuels_mcp_harness/` (read-only reference; `ETAT_PROJET.md` is also in `history/`).

*Draft structure only. Each section lists what happened, the evidence (files, frames, requests) and placeholders (TODO)
to fill when writing the article, after the code clean-up.*

Related docs in this folder:
- `PROCESS_LOG.md` — every request made, verbatim, in order (the raw source of truth).
- `VERSIONS.md` — the version map: archives, snapshots, what changed, which frames.
- `frames/INDEX.md` — contact sheets of each version (generated).
- `../ETAT_PROJET.md` — running project state (French).

---

## 0. Hook
- TODO: one-paragraph hook (an engineer wants to explain MCP + Harness to non-technical colleagues, with no speaker).
- Final frame: `frames/` (last entry) — TRUST / UNDERSTANDING / RETRIEVING DYNAMIC DATA.

## 1. Starting point — the idea and the constraint
- Request: PROCESS_LOG #2 ("MCP is the semantic layer, the Harness guarantees…"), #3 (write the whole speech first).
- Artifacts: `../../Discours_Histoire_MCP_Harness.md` (first speech), first outline.
- TODO: why a video and not slides; audience (townhall, French speakers).

## 2. Generation 1 — slides with Manim (one scene per slide)
- Requests: #4 (Manim), #6 (3Blue1Brown style, one continuous scene), #8 (auto-scrolling HTML), #9 (single floating board).
- Evidence: `_archives/png/S01…S10`, `_archives/mp4/`, `_archives/scenes.py`, `_archives/board.py`,
  `_archives/MCP_Harness*.html`, `_archives/Tableau_*.html`.
- Lesson TODO: a deck in Manim is still a deck; the "chef" metaphor was rejected as childish (#11).

## 3. Generation 2 — one story, one style (TRON)
- Requests: #11 (one story, one flow), #12 (no full sentences, AI as a chip, minimalist TRON), #14 (better data examples, fewer pauses).
- Evidence: `_archives/Histoire_*.html`, `_archives/Tron_*.html`, `_archives/Film_MCP_Harness.mp4`; code `_archives/gen2_code/story.py`, `_archives/gen2_code/tron.py`.
- Lesson TODO: the visual vocabulary (chip, neon rails, packets) becomes the language.

## 4. Generation 3 — a standalone film with acts
- Requests: #15–#17 (more visual code/harness, Paris → France → world zoom, harness surrounds the chip), title "Yes, you can control AI".
- Evidence: `_archives/v6_dissolve_2026-10-11/` (first full film + MP4).
- Workflow shift: #20 → per-act drafts, `dev.sh`, contact sheets (`planche.py`), loop pages (`DEV13`, `DEV35`, `DEV4`, `DEV5`).
- Lesson TODO: rendering the full 1080p each time was the bottleneck; dev 480p + HTML loop pages fixed the feedback loop.

## 5. Iterating act by act (acts 1–3)
- Wired decision tree (v7 `_archives/v7_arbre_cable_2026-10-11/`), morph transitions (v8 `_archives/v8_actes13_morph_2026-10-11/`),
  chat window replaces the user, dissolve → circuit weaving, public/private split screen.
- Snapshots: `v8…/film_before_*.py` (tissage, semantic, mcpflow, chatuser, v9, v10).
- TODO: pick 3 before/after pairs from `frames/`.

## 6. Reworking the story (12 Oct) — from "control" to "retrieving dynamic data"
Ordered snapshots in `_archives/v9_final_en_2026-10-12/` (`film_before_<change>.py`), see `VERSIONS.md`:
- Problem (act 3): random table picking panel, answers in the chat, AMBIGUOUS under the title.
- Semantic layer (act 4): simplified → no tool-call animations → right-angle circuits → tool-call panel → 5 domains →
  same question asked twice gives a different answer (≠).
- Harness (act 5): panel morphs into the harness, TOOLS step on the chip, FORMAT before the chip, audit log inside,
  harness.py running "matrix" tests, user scope (director · west zone), condensed view.
- Together (act 6): icons, outputs (tables/charts/reports) sent back to the chat, words TRUST / UNDERSTANDING / RETRIEVING DYNAMIC DATA.
- TODO: the key insight — MCP gives meaning but the AI still chooses; the harness makes the process deterministic.

## 7. What made it work (method)
- Ask multiple-choice questions before every change (memory `feedback-ask-clarifying-questions`).
- Never render the final until validated; archive before each change (`_archives/…/film_before_*.py`).
- Frame sampling to self-check every render (PyAV contact sheets) before showing.
- TODO: numbers — ~130 requests, ~40 snapshots, film from 2:40 → ~2:00.

## 8. Stepping back: documenting, auditing, cleaning (13 Oct)
- Requests: "document the iterations… for a blog post", "audit", "commit", cleanup steps 1–3, "think big".
- Docs created: `PROCESS_LOG.md` (130 requests extracted from the session transcripts), `VERSIONS.md`, this backbone.
- Visual history: a background sub-agent re-rendered 39 code snapshots in isolated copies (0 failures, ~15 min)
  → `frames/INDEX.md`, 49 versions with contact sheets + per-chapter frames. Work continued in parallel.
- Audit: `AUDIT.md` — ~20 % dead code, ~40 implicit hand-offs between acts, legacy dependency chain.
- Git introduced (`097701d`); outputs ignored. Cleanup with a pixel-diff regression after each step
  (1,899/1,899 frames identical each time):
  - step 1 `c5778ca` dead code (1,913 → 1,741 lines),
  - step 2 `13a47aa` acts and outputs renamed,
  - step 3 `ed516b5` standalone `film_kit.py`, gen-2 modules archived, manim-slides dropped.
- Lesson TODO: a cheap regression check (frame diff) is what makes aggressive refactoring safe.

## 9. Thinking big: from one film to a film studio
- Request: "turn this into a skill / workflow… start from a presentation or research… stills first… keep all tooling".
- Plan: `PLAN_FILM_STUDIO.md` (brief → G1 acts → G2 stills → G3 animatic → G4 polish/final; Film/Act/Beat in
  still|animatic|full modes; kit = primitives → actors → motions; skill shipped inside the repo).
- Kick-off prompt for a clean context: `PROMPT_FILM_STUDIO.md` (`d9328c3`), run in a new session; the studio
  was built in that session, phase by phase, each phase opened by ≤4 multiple-choice questions and closed by a
  validation ("validated, go ahead with phase N").
- TODO after Phase 7: before/after — time to first stills for a new film vs. this one (here: ~2 days of iterations
  before a stable layout; with the engine, stills of 13 beats render in 3 s).

## 10. Building the studio (13 Oct) — phase by phase
Evidence: `film_studio` git log, `VERSIONS.md` § Generation 5, `frames/50–55`, `../CLAUDE.md`, `../.claude/skills/film/`.
- **Phase 0–1 — one repo, one CLI.** `studio dev | act | range | final | sheet | frames | player | regress` replaces
  six hard-coded `dev.sh` branches and their `build_auto_html.py` twins. Outputs leave the source folder (`out/`).
- **Phase 2 — the old film as first citizen.** Baseline rendered from an untouched temp copy of the reference;
  migrated copy → 1,899/1,899 identical frames, EN and FR (`50_studio_migrated`). Act/range drafts proven to be exact
  slices of the full film (frames 535–1636 of the baseline).
- **Phase 3 — extracting the kit without changing a pixel.** 7 steps (primitives, i18n flip to English source,
  scene base + motions, actors, layout anchors, an explicit `Stage` for 79 hand-offs, gallery), regression after
  each. The one failure was instructive: an actor storing `self.color` silently recoloured the whole harness.py panel
  orange in act 5 — caught by the frame diff (83–108 s), fixed in one line. Kit: 5 primitives, 7 actors, 7 motions
  (`52_studio_kit_gallery`).
- **A deliberate change.** "CHAT · IA" had been on screen in the English film the whole time (never in the
  translation dict). Fixed with the user's validation, EN re-baselined, FR untouched — the regression tells
  "intended" from "accidental" (`51_studio_chat_ai`).
- **Phase 4 — the engine.** A beat is a *state* of the screen (`{id: mobject}`), not an animation. Same film code,
  three modes: still (PNG per beat, 3 s), animatic (default transitions: same id morphs, new fades in, missing fades
  out — 5 s), full (custom motion only where it carries the concept — 6 s). Acts 01 + 06 of the old film re-expressed
  as 13 beats (`53–55`). The user did not understand the first question about "state models" — explained with a
  concrete example, then chose the snapshot model.
- **Phase 5 — the workflow as a skill in the repo.** G1 brief → G2 stills → G3 animatic → G4 polish/final, one file
  per gate, `STATUS.md` per film so any session (or a clone) resumes where the last one stopped; `studio extract`
  reads .pptx / .pdf sources.
- **Phase 6 — these docs moved in** (copied; the reference stays read-only).
- **Phase 7 — the pilot.** A 30 s COMEX opener (assist ≠ automate) from a 9-slide deck, through the four gates in one session: one MCQ round + one validation per gate, no gate re-opened. Self-checks caught 4 layout bugs at G2 before the user saw them. Stills render in ~3 s, the 1080p final in ~11 s. Kit gap found: a static `dimmed()` (added).
  TODO: compare with the first film (~130 requests, ~50 versions).
- TODO prose: the lesson — *regression first, refactor second*; and *stills before motion* (most feedback on the
  first film was about layout and words, which never needed animation to judge).

## 11. What I'd do differently / next
- Start from the brief and stills (G1/G2) instead of rendering animations from day one.
- Make every hand-off explicit from the start (the `Stage`), and recolour in place instead of stacking lit copies.
- TODO after Phase 7: requests and time needed for the pilot film vs. ~130 requests for this one.

## Appendix — file map
Paths below are relative to `visuels_mcp_harness/docs/` (the first film). film_studio equivalents:
`films/ai_retrieving_dynamic_data/legacy_scene.py` (film), `studio/kit/` (primitives → actors → motions),
`studio/cli.py` + `studio/pipeline/` (pipeline), `films/<name>/STATUS.md` (project state), `docs/` (this folder).

| Thing | File |
|---|---|
| Current film | `../film.py` |
| Visual primitives | `../film_kit.py` (gen-2 origin: `../_archives/gen2_code/tron.py`) |
| Dev / final pipeline | `../dev.sh`, `../build_auto_html.py`, `../planche.py` |
| Project state | `../ETAT_PROJET.md` |
| Raw requests | `PROCESS_LOG.md` |
| Version map | `VERSIONS.md` |
| Frames | `frames/` |
| Self-check frames taken during iterations | `../_archives/session_material/review_frames/` |
| Session transcripts (local only, not in git) | `../_archives/session_material/transcripts/` |
| Old rendered outputs | `../_archives/outputs_root_2026-10-13/`, `../_archives/v6…`, `../_archives/v9…` |
