# Code audit — `visuels_mcp_harness/` (13 Oct 2026)

> Copied from `visuels_mcp_harness/docs/` (@ 6fb3c32, 13 Oct 2026) into film_studio (Phase 6). Paths such as `_archives/…`, `../film.py` or `../ETAT_PROJET.md` refer to `../visuels_mcp_harness/` (read-only reference; `ETAT_PROJET.md` is also in `history/`).

Scope: `film.py` (1,913 lines), `tron.py` (532), `story.py` (445), `presentation.py` (508), `dev.sh` (77),
`build_auto_html.py` (246), `planche.py` (30). Status (13 Oct): recommendations 1–3 done (`c5778ca`, `13a47aa`, `ed516b5`); `tron.py`, `story.py`, `presentation.py` now live in `_archives/gen2_code/`. File names below describe the state at audit time.
Method: static scan (unused symbols, translation keys, imports) + reading of each act.

## Summary
The film works, but `film.py` is the sediment of ~130 iterations: features were removed visually by
replacing them with no-ops or empty `VGroup()`s rather than deleted, so ~15–20 % of the file is dead or vestigial.
Acts depend on each other through ~40 `self.<attr>` hand-offs, which is what makes per-act drafts fragile.
`tron.py` drags in two older generations (`story.py`, `presentation.py`, `manim_slides`) for ~10 helpers.

## 1. Dead code (safe to delete)
| What | Where | Note |
|---|---|---|
| Unused functions/methods | `icon_db`, `cam`, `old_doc_to_question`, `mini_tree`, `badge_follow`, inner `stream` | `old_doc_to_question` alone ≈ 30 lines; `cam` also shadows `Tron.cam` |
| Unused constants | `CALL_BAD`, `FORBIDDEN`, `DROPPED`, `CODE_LINES`, `CALL_POS`, `CODE_CENTER`, `CONCEPT_XS`, `GHOST_X`, `EUROPE`, `EU_CITIES` | leftovers from plates refusal, harness.py screen, 4-domain layout, EU zoom |
| Unused translations | 37 of 146 keys in `EN` | model swap (MODÈLE A–D, REMPLAÇABLE, DURABLE), plates refusal, old chapter names, old titles |
| Empty acts | `a_modele`, `a_outro` (`pass`) | still listed in `construct()` |
| Dead branch | `run(fail=True)` (barrier, red bits, `self.barrier`) | no caller since the plates refusal was removed |
| Dead state | `self.popup`/`clear_popup`, `self.answer`/`display()` kept at opacity 0, `self.ph_marks`, `self.box_ph`, `self.conf_lbl/conf_sub`, `self.crosses`, `self.mini`, `self.call`, `self.answer_refused`, `self.ghost`, `self.doubt_links`, `self.runs` | set to `VGroup()` / invisible only so later acts don't crash |
| Legacy helpers | `tool_card` (used once as a title icon), `user_icon` + `USER_POS` (only in act 1 intro), `q_label` | review: keep only if act 1 still needs them |
| Background grid | `grid = Tron.grid` in `Film` | grid no longer drawn |

Estimated removal: ~300–350 lines from `film.py` without any visual change.

## 2. Fragility (what breaks iteration)
1. **Implicit act hand-offs.** Acts communicate through attributes created anywhere (`self.p3_rail`, `self.p4_grid`, `self.lit_ok`,
   `self.chat_extra`, `self.strip`, `self.code_lines`, `self.badge`…). Removing a feature in act 4 crashes act 5
   (seen several times: `scope_pill`, `call`, `mini`). Guards like `hasattr(self, "code_lines")` and
   `getattr(self, "condensed", False)` are symptoms.
2. **Mutating shared geometry mid-film.** `self.box_shape`, `self.band_shape`, `self.chip.size *= CHIP_IN_HARNESS`,
   `self.tables` re-bound to a single DATA group, `self.gates.submobjects[3] = log_m`. Later code silently uses the new meaning.
3. **Opacity / z-index bookkeeping.** 52 `set_z_index` calls with ad-hoc values; `dim()` relies on a cached `_base_op`
   per sub-object; `set_opacity` vs `dim` mixed (caused the grey DATA box and the filled badge icon bugs).
4. **Overlapping semi-transparent copies.** Lit paths are copies drawn over base paths (`lit`, `lit2`, `out_lit`, `lit_ok`) —
   fixed once, but the pattern is still the default way to highlight.
5. **Global monkey-patching.** `tron.neon = neon` overrides the library at import time.
6. **`play()` override with `slow`, `MIN_RT`, `_raw`.** Durations depend on a hidden flag toggled around blocks;
   forgetting to reset `_raw` changes timings of everything after.
7. **French source strings as keys.** All text is French and translated through `tr()`; a typo in a key silently falls back to French.

## 3. Structure
- One 1,900-line class mixing: layout constants, geometry data (Paris/France/world), icon factories, scene helpers
  (chat, panels, badge, code file), and six acts.
- Helpers that belong together are scattered (chat: `make_chat`, `chat_bubble_pos`, `doc_to_question`, `chat_bubble`,
  `chat_reply`, `user_badge`, `badge_*`; panels: `panel_frame`, `table_panel`, `tool_panel`, `tools_strip`, `domain_grid`).
- Magic numbers for positions everywhere (`[-2.55, OUT_Y]`, `+ 0.65`, `- 0.28`…), several derived from previous layouts.
- Comments are French; code identifiers are mixed FR/EN (`a_devine`, `a_refus` that no longer refuses anything).

## 4. Dependencies & pipeline
- `tron.py` imports `story.py` → `presentation.py` → `manim_slides`; the film uses only ~10 symbols from `tron.py`
  (colours, `L`, `neon`, `rail`, `flash_along`, 6 icons, `globe`, `Chip`). The rest (`TronAuto`, `s01`–`s13`, `boot`) is generation-2 code.
- `manim-slides` pins Manim to 0.21 — no longer needed by the film.
- `dev.sh` has one hard-coded branch per preview (`dev`, `dev13`, `dev35`, `dev4`, `dev5`, `final`) duplicated in
  `build_auto_html.py` (`film-dev*` variants). A generic `./dev.sh range <from> <to>` would replace them.
- Output names still `Oui_on_peut_controler_l_IA.*` (old title).
- `film_chapters.json` / `film_meta.json` written into the source folder on every render.

## 5. Recommendations (in order, each step renders identically before/after)
| # | Step | Effort | Gain |
|---|---|---|---|
| 1 | Delete dead code, constants, `EN` keys, empty acts, `fail` branch | S | −300 lines, less confusion |
| 2 | Rename acts/methods to what they show now (`a_refus` → `a_scope_demo`, `a_devine` → `a_guesses`…) and output files to the new title | S | readability |
| 3 | Extract a small `film_kit.py` from `tron.py` (colours, `L`, `neon`, `rail`, `flash_along`, icons, `Chip`) and drop the `story/presentation/manim_slides` chain | M | standalone, unpins Manim |
| 4 | Group helpers into modules: `layout.py` (constants), `geo.py` (maps), `widgets.py` (chat, badge, panels, code file) | M | `film.py` = acts only (~900 lines) |
| 5 | Make act hand-offs explicit: one `State` dataclass passed between acts, created once; no attribute created inside an act | M | per-act drafts stop breaking |
| 6 | Replace "lit copy" highlights with a `highlight(path, color)` helper that recolours in place and returns a restore animation | S | fixes the stacking bug class |
| 7 | Generic `dev.sh range <from> <to>` + single HTML builder entry | S | fewer duplicated branches |
| 8 | Write chapter/meta JSON to `media/` instead of the source folder | S | clean folder |

Out of scope for now (per decision): a reusable video toolkit / template. Steps 3–5 are the foundation for it later.

## 6. Docs to update after clean-up
`ETAT_PROJET.md` (still describes the old acts), `docs/VERSIONS.md` (add the post-cleanup baseline), `requirements.txt` (if manim-slides dropped).
