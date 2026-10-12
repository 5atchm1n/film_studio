"""Motions: reusable ways of moving actors. Functions taking the scene (to play) or returning animations.

Design rules they encode: morph rather than cut, dim until relevant, one path lit per call,
recolour in place instead of stacking lit copies, end on words.
"""

from manim import *

from .primitives import rail


def morph(scene, old, new, *extra, run_time=0.8):
    """What leaves turns into what arrives (3Blue1Brown-style morph), element by element:
    each old element is paired with a new one; extra elements fade out in place."""
    olds = [m for g in old for m in (g if isinstance(g, VGroup) and not hasattr(g, "text") and len(g) > 2
                                       and all(isinstance(x, VGroup) for x in g) else [g])]
    news = [m for g in new for m in (g if isinstance(g, VGroup) and not hasattr(g, "text") and len(g) > 2
                                       and all(isinstance(x, VGroup) for x in g) else [g])]
    anims, n = [], min(len(olds), len(news))
    for o, w in zip(olds[:n], news[:n]):
        anims.append(FadeTransform(o, w, path_arc=-PI / 12))
    anims += [FadeOut(o, scale=0.9) for o in olds[n:]] + [FadeIn(w, scale=0.9) for w in news[n:]]
    scene.play(*anims, *extra, run_time=run_time, rate_func=rate_functions.ease_in_out_cubic)


def send(scene, packet, points, color, run_time=1.0):
    """A packet travels along a right-angle route, leaving a short fading trail."""
    path = rail(points)
    packet.move_to(points[0])
    trail = TracedPath(packet.get_center, stroke_color=color, stroke_width=3, dissipating_time=0.35)
    trail.set_z_index(7)
    scene.add(trail, packet)
    with scene.exact():
        scene.play(MoveAlongPath(packet, path), run_time=run_time, rate_func=rate_functions.ease_in_out_sine)
    scene.remove(trail)


def dim(mobs, factor):
    """Dim (or restore, factor=1) a group while respecting each layer's own opacity (neon halos stay halos).
    The first call on a mobject records its base opacity; later factors are relative to it."""
    fam = [m for mob in mobs for m in mob.family_members_with_points()]
    for m in fam:
        if not hasattr(m, "_base_op"):
            m._base_op = (m.get_stroke_opacity(), m.get_fill_opacity())
    start = [(m.get_stroke_opacity(), m.get_fill_opacity()) for m in fam]
    end = [(b[0] * factor, b[1] * factor) for b in (m._base_op for m in fam)]

    def update(_, a):
        for m, (s0, f0), (s1, f1) in zip(fam, start, end):
            m.set_stroke(opacity=s0 + (s1 - s0) * a, family=False)
            m.set_fill(opacity=f0 + (f1 - f0) * a, family=False)

    return UpdateFromAlphaFunc(Mobject(), update)


def light(mobs):
    """Restore dimmed mobjects to their base opacity."""
    return dim(mobs, 1.0)


def highlight(path, color, width=None):
    """Recolour a rail (or any stroke) in place — never a lit copy on top.
    Returns (light_animation, restore_animation)."""
    members = path.family_members_with_points()
    saved = [(m.get_stroke_color(), m.get_stroke_width(), m.get_stroke_opacity()) for m in members]

    def target(m):
        return m.animate.set_stroke(color, width if width is not None else m.get_stroke_width(), 1)

    on = AnimationGroup(*[target(m) for m in members])
    off = AnimationGroup(*[m.animate.set_stroke(c, w, o) for m, (c, w, o) in zip(members, saved)])
    return on, off


def rise_to_title(scene, src, text, toc=None, extra=()):
    """A finding or question rises and becomes the chapter title."""
    scene.chapter(text, toc, src=src, extra=extra)


def condense(scene, pairs, fade=(), run_time=1.6):
    """Once explained, details condense into big-picture blocks: each (detail, block) pair transforms,
    everything in `fade` disappears."""
    scene.play(*[FadeTransform(d, b) for d, b in pairs], *[FadeOut(m) for m in fade], run_time=run_time)


def words_from_blocks(scene, pairs, fade=(), center=None, scale=0.8, run_time=1.2):
    """Ending: the blocks re-centre, then each turns into the word that sums it up; `fade` blocks vanish."""
    blocks = VGroup(*[b for b, _ in pairs], *fade)
    if center is not None:
        scene.play(blocks.animate.scale(scale).move_to(center), run_time=0.9)
    scene.play(*[FadeTransform(b, w) for b, w in pairs], *[FadeOut(m, scale=0.8) for m in fade], run_time=run_time)
