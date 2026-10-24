"""Validate translations against installed game strings and render plain-text previews.

The output stays in work/preview. The original game files are never modified.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import UnityPy

from extract_catalog import BUNDLES, OUTPUT, UI_ENTRY


ROOT = Path(__file__).resolve().parent
TRANSLATION_FILES = tuple(sorted((ROOT / "translations").glob("*_ko.json")))
# Preserve both lower-case markup ([n], [sub], [sp]) and the game's
# bracketed uppercase UI parameters ([NPC], [ITEM], [PRICE]). The %...%
# expression stays first so composite variables containing [sp] are atomic.
TOKEN = re.compile(r"%[A-Z][^%\r\n]{0,96}%|\[/?[a-z0-9]+\]|\[[A-Z][A-Z0-9_]*\]|<[A-Z][A-Z_0-9/-]{0,80}>|</?[a-z]+(?:\s[^<>]*?)?>")


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict:
    """Prevent duplicate IDs in one translation JSON from silently disappearing."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON translation key: {key}")
        result[key] = value
    return result


def load_catalog() -> dict[str, dict]:
    with (OUTPUT.parent / "catalog.jsonl").open(encoding="utf-8") as file:
        entries = [json.loads(line) for line in file]
    return {entry["id"]: entry for entry in entries}


def load_translations(catalog: dict[str, dict]) -> dict[str, str]:
    translations = {}
    for path in TRANSLATION_FILES:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_json_keys)
        # Windows console codepages may turn an entire Korean translation
        # into literal '?' characters while preserving valid JSON. Reject
        # that silent corruption before including it in any mod build.
        if len(data) >= 5 and not any(
            '\uac00' <= char <= '\ud7a3' for value in data.values()
            if isinstance(value, str) for char in value
        ):
            raise ValueError(f"Suspected lost Korean characters in {path.name}: no Hangul syllables")
        # A partially recovered file may contain a mixture of Korean text
        # and large runs of '?' left by lossy stdin encoding. Korean dialogue
        # uses question marks, but never this densely across a whole batch.
        values = ''.join(value for value in data.values() if isinstance(value, str))
        if len(data) >= 5 and values and values.count('?') > max(20, len(values) * 0.15):
            raise ValueError(f"Suspected encoding loss in {path.name}: excessive '?' characters")
        for key, text in data.items():
            entry_id = key if "/" in key else f"english_camp_metatexts/{key}"
            if entry_id in translations:
                raise ValueError(f"Repeated translation ID: {entry_id}")
            if entry_id not in catalog:
                raise KeyError(f"Translation has no source entry: {entry_id}")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"Empty translation: {entry_id}")
            if len(text) >= 14 and text.count('?') >= max(6, len(text) * 0.25):
                raise ValueError(f"Suspected corrupted Korean text at {entry_id}: excessive '?' characters")
            if any(sep in text for sep in ("\r", "\n", "\t")):
                raise ValueError(f"Use game markup for line breaks, not literal control characters: {entry_id}")
            english = catalog[entry_id]["english"]
            old = collections.Counter(TOKEN.findall(english))
            new = collections.Counter(TOKEN.findall(text))
            if old != new:
                raise ValueError(f"Variable/formatting token mismatch {entry_id}: {old} != {new}")
            if text == english:
                raise ValueError(f"Untranslated text: {entry_id}")
            translations[entry_id] = text
    return translations


def render_events(script: str, asset: str, catalog: dict[str, dict],
                  translations: dict[str, str]) -> tuple[str, int]:
    rows = {entry["line"]: entry for entry in catalog.values()
            if entry["asset"] == asset and entry["id"] in translations}
    lines = script.split("\n")
    current_event = ""
    events_at_line = {}
    for i, raw_line in enumerate(lines, 1):
        if raw_line.startswith(">>>\t"):
            current_event = raw_line.split("\t")[1].strip()
        events_at_line[i] = current_event
    if len(rows) != len({entry["id"] for entry in rows.values()}):
        raise ValueError(f"Conflicting event line replacements: {asset}")
    for line_no, entry in rows.items():
        if line_no < 1 or line_no > len(lines):
            raise ValueError(f"Line number outside asset: {entry['id']}")
        if events_at_line[line_no] != entry["event"]:
            raise ValueError(f"Event identity changed: {entry['id']}")
        cells = lines[line_no - 1].split("\t")
        col = entry["column"]
        if len(cells) <= col:
            raise ValueError(f"Installed source changed: {entry['id']}")
        native_id = entry["key"].split("/")[1]
        if len(cells) > 5 and cells[5].strip() != native_id:
            raise ValueError(f"Row identity changed: {entry['id']}")
        # split('\n') keeps CR from CRLF. Preserve it if the text is the last
        # cell on a malformed four-column event line without the usual row ID.
        final_cr = "\r" if col == len(cells) - 1 and cells[col].endswith("\r") else ""
        english = cells[col][:-1] if final_cr else cells[col]
        if english != entry["english"]:
            raise ValueError(f"Installed source changed: {entry['id']}")
        cells[col] = translations[entry["id"]] + final_cr
        lines[line_no - 1] = "\t".join(cells)
    return "\n".join(lines), len(rows)


def render_ui(script: str, asset: str, catalog: dict[str, dict],
              translations: dict[str, str]) -> tuple[str, int]:
    lines = script.split("\n")
    applied = set()
    for i, line in enumerate(lines):
        match = UI_ENTRY.match(line)
        if match is None:
            continue
        key = json.loads('"' + match.group("key") + '"')
        entry_id = f"{asset}/{key}"
        if entry_id not in translations:
            continue
        english = json.loads('"' + match.group("value") + '"')
        if english != catalog[entry_id]["english"]:
            raise ValueError(f"Installed UI source changed: {entry_id}")
        new_value = json.dumps(translations[entry_id], ensure_ascii=False)[1:-1]
        lines[i] = line[:match.start("value")] + new_value + line[match.end("value"):]
        applied.add(entry_id)
    expected = {key for key in translations if key.startswith(asset + "/")}
    if applied != expected:
        raise ValueError(f"Unmatched UI replacements: {sorted(expected - applied)[:10]}")
    return "\n".join(lines), len(applied)


def main() -> None:
    catalog = load_catalog()
    translations = load_translations(catalog)
    env = UnityPy.load(str(BUNDLES / "texts_assets_all.bundle"))
    dest = OUTPUT.parent / "preview"
    dest.mkdir(parents=True, exist_ok=True)
    changed = collections.Counter()
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        asset = obj.peek_name()
        if not any(key.startswith(asset + "/") for key in translations):
            continue
        script = obj.read_typetree()["m_Script"]
        if asset == "english_camp_metatexts":
            rendered, count = render_ui(script, asset, catalog, translations)
        else:
            rendered, count = render_events(script, asset, catalog, translations)
        (dest / f"{asset}.txt").write_bytes(rendered.encode("utf-8"))
        changed[asset] = count
    if sum(changed.values()) != len(translations):
        raise ValueError(f"Applied {sum(changed.values())} != {len(translations)} translations")
    print(json.dumps({"total_catalog": len(catalog), "translated": len(translations),
                      "by_asset": changed, "preview_dir": str(dest)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
