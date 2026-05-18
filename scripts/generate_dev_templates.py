"""
Generate dev base .package files (minimal DBPF) for local pipeline testing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "worker"))

from packager.dbpf import ResourceKey, create_minimal_texture_package
from packager.png_util import solid_png

MANIFEST = ROOT / "templates" / "manifest.json"
BASES = ROOT / "templates" / "bases"


def parse_hex_int(value: str) -> int:
    return int(value, 16)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    BASES.mkdir(parents=True, exist_ok=True)

    for tpl in manifest["templates"]:
        pkg_path = BASES / Path(tpl["basePackage"]).name
        res = tpl["textureResource"]
        png = solid_png(tpl["textureWidth"], tpl["textureHeight"], (80, 40, 120, 255))
        create_minimal_texture_package(
            pkg_path, png, instance=parse_hex_int(res["instance"])
        )
        print(f"Created dev base package: {pkg_path}")

    print("\nDev templates ready. For real in-game CC, export base packages from Sims 4 Studio.")


if __name__ == "__main__":
    main()
