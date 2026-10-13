# Prompt — start "Film Studio" in a clean context

> Copied from `visuels_mcp_harness/docs/` (@ 6fb3c32, 13 Oct 2026) into film_studio (Phase 6). Paths such as `_archives/…`, `../film.py` or `../ETAT_PROJET.md` refer to `../visuels_mcp_harness/` (read-only reference; `ETAT_PROJET.md` is also in `history/`).

Copy everything below the line into a new Claude Code session started in
`/Users/satcheenshakya/Documents/IndigoNeo/presentations/`.

---

I want to turn a one-off Manim film into a reusable, self-contained "film studio": a codebase + a Claude Code skill
that lets me go from a presentation or research doc to a short concept video, through validated gates, without
rebuilding scenes by hand.

## Context — read these first (do not skip)
The reference project is `visuels_mcp_harness/` (git repo, Manim CE 0.21 in `.venv`, PyAV for frames, no ffmpeg).
It produced the film "AI - Retrieving dynamic data" over ~130 requests and ~50 versions. Read, in this order:
1. `visuels_mcp_harness/docs/PLAN_FILM_STUDIO.md` — the full plan (phases 0–7). This prompt executes it.
2. `visuels_mcp_harness/docs/AUDIT.md` — what is fragile in the current code and why.
3. `visuels_mcp_harness/docs/PROCESS_LOG.md` — every request I made, verbatim (design taste + workflow rules).
4. `visuels_mcp_harness/docs/VERSIONS.md` and `docs/frames/INDEX.md` — how the film evolved (look at a few sheets).
5. `visuels_mcp_harness/ETAT_PROJET.md`, `film.py`, `film_kit.py`, `dev.sh`, `build_auto_html.py`, `planche.py`.
Also follow my saved memories (ask multiple-choice questions before building; never render a final without my
validation; archive/commit before each change).

## What I want
- A new sibling folder `film_studio/` (its own git repo). The skill lives **inside the repo**
  (`film_studio/.claude/skills/film/`) so cloning the repo elsewhere brings the workflow with it. Add a `CLAUDE.md`.
- Input of a new film: a Markdown **brief** generated from my presentation/research.
- Four validated gates: **G1 brief & acts → G2 stills (one frame per beat, no animation) → G3 animatic
  (480p, default identical transitions) → G4 polish (custom motion only where it carries the concept) + final**.
- Same film code renders in three modes: `still`, `animatic`, `full`.
- All current tooling preserved and generalised: per-act/range drafts, HTML loop player with chapters + scrubber +
  frame stepping, contact sheets, i18n (EN default, FR switch), final 1080p + HTML.
- The current film must keep rendering **pixel-identical** at all times (store a baseline; frame-diff regression).
- A kit that grows slowly: primitives → actors (chat + badge, chip, MCP band, data block, panels, code file,
  harness frame) → motions (paired morph, packet send, flash, dim/light, highlight in place, rise-to-title,
  condense, words-from-blocks). The storyboard format is open: start Python-first, iterate.

## How to work
- Before each phase: ask me ≤4 multiple-choice questions (recommended option first), then build.
- Work phase by phase and stop for my validation after each phase. Commit at the end of each phase
  (I will tell you when to push; there is no remote yet).
- Never modify `visuels_mcp_harness/` (read-only reference), except to read its files.
- Self-check renders by sampling frames before showing me anything.
- Keep design rules from PLAN §1.2 as defaults (minimal TRON, keywords not sentences, morph transitions,
  dim until relevant, no stacked transparent copies, answers in the chat, end on words, no precise figures).

## Start now with
Phase 0 (bootstrap `film_studio/`, CLAUDE.md, skill skeleton, venv/requirements, .gitignore) and Phase 1
(port the tooling into one CLI) and Phase 2 (migrate the current film + baseline + regression passing).
Ask your questions first. Stop after Phase 2 and show me: the tree, the CLI help, the regression result,
and one stills/loop page proving the legacy film renders identically.
