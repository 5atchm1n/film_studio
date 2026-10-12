# Design lessons (defaults for every film)

Source: the making of "AI - Retrieving dynamic data" (≈130 requests, ~50 versions, 11–13 Oct 2026).
Add a line whenever the user gives design feedback that should apply beyond one shot.

## Look
- Minimal TRON: black background, thin neon strokes with a discreet halo. Academic, never glitchy (no glitch effects).
- Fonts: DIN Alternate for labels (spaced capitals), Futura for numbers/titles, Menlo for code.
- Colours carry meaning: cyan = meaning / MCP, orange = trust / harness, ice = AI & text, red = error, green = validated,
  dim teal = unlit rails.
- No childish metaphors (the "chef" metaphor was rejected).

## Text
- Keywords only, never full sentences on screen.
- Chapter label top-left; a question or finding can rise to become the chapter title.
- No precise business figures unless provided — orders of magnitude only.

## Story & motion
- One continuous story; transitions are morphs: elements pair up and transform (FadeTransform per element), not cuts.
- A recurring actor set: chat window (the user, with an identity badge), AI chip, circuit rails, data blocks.
- Answers appear in the chat; the side of the screen explains the mechanism (panels).
- Dim everything not relevant yet; light it only when used.
- Never stack semi-transparent copies (lit copies over base paths look brighter where they overlap) — recolour in place.
- Right-angle circuits only; packets travel along rails; one path lit per call.
- Explain in detail once, then condense into icons / big-picture blocks; drop the example once the concept is built.
- End on words that summarise the concepts (blocks morph into words), never on a black screen.
