"""Video helpers on PyAV (no ffmpeg binary needed)."""

from pathlib import Path

import av
import numpy as np


def info(path: Path) -> dict:
    with av.open(str(path)) as c:
        s = c.streams.video[0]
        duration = float(s.duration * s.time_base) if s.duration else float(c.duration / av.time_base)
        return {"fps": float(s.average_rate), "size": [s.width, s.height], "frames": s.frames, "duration": duration}


def frames(path: Path):
    """Yield (t, RGB uint8 array) for every frame, in order."""
    with av.open(str(path)) as c:
        for fr in c.decode(video=0):
            yield float(fr.pts * fr.time_base), fr.to_ndarray(format="rgb24")


def frames_at(path: Path, times: list[float]) -> list[tuple[float, np.ndarray]]:
    """First frame at or after each requested time (times need not be sorted)."""
    order = sorted(range(len(times)), key=lambda k: times[k])
    found: dict[int, tuple[float, np.ndarray]] = {}
    last = None
    it = iter(order)
    k = next(it, None)
    for t, img in frames(path):
        last = (t, img)
        while k is not None and t + 1e-6 >= times[k]:
            found[k] = (t, img)
            k = next(it, None)
        if k is None:
            break
    while k is not None:  # past the end: last frame
        found[k] = last
        k = next(it, None)
    return [found[k] for k in range(len(times))]
