"""Inspect Monster Camp's installed English TextAssets without modifying the game.

Run from any directory: python monster_camp/inspect_sources.py
"""

from __future__ import annotations

import collections
import json
import os
from pathlib import Path

import UnityPy


GAME_DIR = Path(os.environ.get(
    "MCKR_GAME_DIR", r"C:\Games\Steam\steamapps\common\Monster Prom 2 - Monster Camp"
))
BUNDLES = GAME_DIR / "MonsterCamp_Data" / "StreamingAssets" / "aa" / "StandaloneWindows"
OUTPUT = Path(__file__).resolve().parent / "work" / "inventory.json"


def main() -> None:
    if not BUNDLES.is_dir():
        raise FileNotFoundError(f"Monster Camp bundles not found: {BUNDLES}")

    env = UnityPy.load(str(BUNDLES / "texts_assets_all.bundle"))
    report = {"game_dir": str(GAME_DIR), "assets": [], "metadata_fields": {}}
    field_counts = collections.Counter()
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        tree = obj.read_typetree()
        name = tree["m_Name"]
        script = tree["m_Script"]
        if not isinstance(script, str):
            raise TypeError(f"Unexpected TextAsset script type: {name}")
        lines = script.splitlines()
        stats = collections.Counter()
        samples = {}
        for line in lines:
            if line.startswith(">>>\t"):
                stats["event_headers"] += 1
            elif line.startswith(">"):
                parts = line.split("\t")
                field = parts[0]
                field_counts[field] += 1
                if field not in samples:
                    samples[field] = parts[:7]
            elif line.startswith("\t"):
                parts = line.split("\t")
                stats[f"tab_line_{len(parts)}_columns"] += 1
                if len(parts) > 3 and parts[3].strip():
                    stats["tab_text_col_3"] += 1
            elif line.strip():
                stats["other_nonempty_lines"] += 1
        report["assets"].append({
            "name": name,
            "path_id": obj.path_id,
            "characters": len(script),
            "lines": len(lines),
            "stats": dict(stats),
            "field_examples": samples if name.startswith("english_camp_events_") else {},
        })
    report["metadata_fields"] = dict(field_counts.most_common())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for asset in report["assets"]:
        print(f"{asset['name']}: {asset['characters']:,} chars; {asset['lines']:,} lines; {asset['stats']}")
    print(f"Metadata field patterns: {len(field_counts)}")
    print(f"Detailed inventory: {OUTPUT}")


if __name__ == "__main__":
    main()
