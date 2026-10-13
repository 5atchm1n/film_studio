# Status — AI - Retrieving dynamic data (reference film)

## Current gate
Done (made before the studio existed: ≈130 requests, ~50 versions, 11–13 Oct 2026). Regression reference for the kit,
engine and pipeline. Now an **engine film**: 6 acts, 35 live beats (`film.py`), pixel-identical to its baseline.

## Validations
| Gate | Date | What was validated |
|---|---|---|
| Final (v9, EN) | 2026-10-12 | Full film, 6 acts, in visuels_mcp_harness |
| Migration | 2026-10-13 | Pixel-identical in film_studio (Phase 2); kit extraction pixel-identical (Phase 3) |
| Change | 2026-10-13 | Chat title CHAT · AI in English (EN re-baselined) |
| Port | 2026-10-13 | Ported to Film/Act/Beat (live beats, one per reading pause): EN + FR IDENTICAL, 1,899/1,899 frames |

## Decisions (do not re-ask)
- Highlights stay as lit copies here (pixel identity); new films recolour in place.
- Port = live beats (the legacy animation code, cut at the reading pauses) so the full film stays pixel-identical;
  stills fast-forward. Pure states (for a real animatic) are a possible next step, to discuss.

## Layout
`film.py` (storyboard + beats) · `film_data.py` (text, FR, data, positions) · `film_stage.py` (hand-offs) ·
`film_pieces.py` (map, wiring, panels, harness run).

## Next step
To discuss: pure states for some acts (animatic + exact stills without fast-forward).
