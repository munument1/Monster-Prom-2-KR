"""Build Monster Camp's native fan-translation Localization.txt from reviewed rows.

Output is staged under build/. It does not install or publish the mod.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_preview import ROOT, load_catalog, load_translations, main as verify_installed_sources


BUILD_DIR = ROOT / "build" / "MonsterCampKR"


def localization_key(entry: dict) -> str:
    if entry["kind"] == "ui":
        return entry["key"]
    # The last column of game event rows is its native translation ID, which
    # the game's CustomLocalizationParser reads before the TAB separator.
    fragments = entry["key"].split("/")
    if len(fragments) != 3 or not fragments[2].startswith("col-"):
        raise ValueError(f"No stable native localization ID: {entry['id']}")
    row_id = fragments[1]
    if row_id.startswith("line-"):
        raise ValueError(f"No stable native localization ID: {entry['id']}")
    return row_id


def main() -> None:
    # Refuse export when a game update has moved or replaced source rows.
    verify_installed_sources()
    catalog = load_catalog()
    translations = load_translations(catalog)
    native = {}
    origin = {}
    for entry_id, korean in translations.items():
        key = localization_key(catalog[entry_id])
        if key in native and native[key] != korean:
            raise ValueError(f"Conflicting native localization ID: {key}")
        native[key] = korean
        origin[key] = entry_id
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    content = "".join(f"{key}\t{value}\n" for key, value in native.items())
    if any(not line or line.count("\t") != 1 for line in content.splitlines()):
        raise ValueError("Malformed native Localization.txt")
    target = BUILD_DIR / "Localization.txt"
    target.write_bytes(content.encode("utf-8"))
    manifest = {"game": "Monster Prom 2: Monster Camp",
                "native_translation_entries": len(native),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "source_ids": origin,
                "note": "Staged native localization text; a complete mod may also require Descriptor.mcmtd"}
    (BUILD_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Staged {len(native)} localized IDs: {target}")


if __name__ == "__main__":
    main()
