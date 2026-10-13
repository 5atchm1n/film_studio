# G1 — Brief & acts

Goal: agree on **what the film says** before any pixel. Output: `films/<name>/brief.md` (template already copied by
`studio new`), validated by the user.

## Steps
1. **Source.** `studio extract <name> <file>` for each presentation / research doc (.pptx .pdf .md; appends to
   `source.md`). Read `source.md` fully. If the user only described the idea, write it into `source.md` yourself.
2. **Questions (≤4, MCQ, recommended first).** Typical:
   - Audience and setting (COMEX, product team, all-hands; with or without a speaker).
   - The one idea — propose 2–3 candidate sentences drawn from the source.
   - Length (≤60 s / ~90 s / ~2 min) → number of acts (3–6) and beats (≈ 1 beat per 3–5 s).
   - Business example to carry the concept (from the source; never invented figures).
3. **Draft brief.md**: audience · one idea · acts table (what the viewer understands + one key image per act) ·
   vocabulary EN/FR (keywords only) · actors (reuse the kit's: chat + badge, chip, rails, panel, band, data,
   harness, code file) · constraints (figures, names) · ending words.
4. **Self-check**: each act moves the one idea forward; each key image is drawable with the kit (or names the one
   new actor it needs); no sentences in the vocabulary; ends on words; no precise figures without a source.
5. **Show** brief.md (short summary in chat + the file). Stop.

## Exit
User validates the one idea, the act list and the key images. Record in STATUS.md (gate G1 ✓, date, decisions),
commit "G1: brief validated".

## Pitfalls seen before
- Metaphors that feel childish (the "chef" was rejected) — prefer the system itself, drawn minimally.
- Too many acts: one story, one flow. Merge acts that don't change what the viewer understands.
