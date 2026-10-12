"""Film manifests: `films/<name>/film.toml`."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILMS = ROOT / "films"
OUT = ROOT / "out"


@dataclass
class Film:
    name: str
    dir: Path
    title: str
    kind: str
    scene_file: str
    scene_class: str
    acts: list[str]
    langs: list[str]

    @property
    def out(self) -> Path:
        return OUT / self.name

    @property
    def baseline(self) -> Path:
        return self.dir / "baseline"

    def check_act(self, act: str) -> str:
        if act not in self.acts:
            raise SystemExit(f"Unknown act '{act}' for {self.name} (acts: {', '.join(self.acts)})")
        return act


def load(name: str) -> Film:
    path = FILMS / name / "film.toml"
    if not path.exists():
        raise SystemExit(f"No film '{name}' (expected {path.relative_to(ROOT)}). Films: {', '.join(names()) or '-'}")
    m = tomllib.loads(path.read_text(encoding="utf-8"))
    return Film(name=name, dir=path.parent, title=m["title"], kind=m.get("kind", "legacy"),
                scene_file=m["scene_file"], scene_class=m.get("scene_class", "Film"), acts=list(m["acts"]),
                langs=list(m.get("langs", ["en"])))


def names() -> list[str]:
    return sorted(p.parent.name for p in FILMS.glob("*/film.toml") if not p.parent.name.startswith("_"))
