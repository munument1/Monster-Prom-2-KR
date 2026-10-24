"""Extract translatable Monster Camp source strings as a stable working catalog.

This reads the user's installed copy. All full-text extraction output is kept
under the ignored work/ directory; no Unity assets are edited.
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path

import UnityPy

from inspect_sources import BUNDLES, OUTPUT


UI_ENTRY = re.compile(
    r'^\s*"(?P<key>(?:\\.|[^"\\])*)"\s*:\s*"(?P<value>(?:\\.|[^"\\])*)"'
)
META_COLUMN_3 = {
    ">choice_option1", ">choice_option2", ">gossip_stat",
    ">gossip_custom_answer", ">lovelogcompliment_stat",
    ">gossip_stat_question", ">gossip_quality_question",
    ">gossip_quality_verynegative", ">gossip_quality_negative",
    ">gossip_quality_positive", ">gossip_quality_verypositive",
    ">gossip_custom_question", ">gossip_player_question",
}
META_COLUMN_2 = {">icebreaker_answer"}


def string_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def make_entry(asset: str, event: str, line_no: int, column: int,
               key: str, english: str, kind: str) -> dict:
    return {
        "id": f"{asset}/{key}",
        "asset": asset,
        "event": event,
        "line": line_no,
        "column": column,
        "kind": kind,
        "key": key,
        "source_hash": string_hash(english),
        "english": english,
    }


def event_entries(asset: str, script: str) -> list[dict]:
    result = []
    event = ""
    per_id = collections.Counter()
    for line_no, line in enumerate(script.splitlines(), 1):
        if line.startswith(">>>\t"):
            event = line.split("\t")[1].strip()
            continue
        cells = line.split("\t")
        col = None
        if line.startswith(">"):
            field = cells[0]
            if field in META_COLUMN_2:
                col = 2
            elif field in META_COLUMN_3:
                col = 3
        elif line.startswith("\t"):
            col = 3
        if col is None or len(cells) <= col or not cells[col].strip():
            continue
        uid = cells[5].strip() if len(cells) > 5 else ""
        if not uid:
            # Rare malformed or metadata-only lines lack canonical row ids.
            uid = f"{event}/line-{line_no}"
        base = f"{event}/{uid}/col-{col}"
        per_id[base] += 1
        key = base if per_id[base] == 1 else f"{base}/occ-{per_id[base]}"
        result.append(make_entry(asset, event, line_no, col, key, cells[col], "event"))
    return result


def ui_entries(asset: str, script: str) -> list[dict]:
    result = []
    seen = set()
    for line_no, line in enumerate(script.splitlines(), 1):
        match = UI_ENTRY.match(line)
        if not match:
            continue
        key = json.loads('"' + match.group("key") + '"')
        english = json.loads('"' + match.group("value") + '"')
        if key in seen:
            raise ValueError(f"Duplicate UI key: {key}")
        seen.add(key)
        result.append(make_entry(asset, "", line_no, -1, key, english, "ui"))
    return result


def main() -> None:
    if not BUNDLES.is_dir():
        raise FileNotFoundError(BUNDLES)
    env = UnityPy.load(str(BUNDLES / "texts_assets_all.bundle"))
    rows = []
    files = []
    game_version = "unknown"
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        tree = obj.read_typetree()
        asset = tree["m_Name"]
        script = tree["m_Script"]
        if asset == "app_info":
            for info_line in script.splitlines():
                cols = info_line.split("\t")
                if len(cols) >= 3 and cols[0] == "pc":
                    game_version = cols[2]
        if asset.startswith("english_camp_events_") or asset == "english_camp_challenges":
            entries = event_entries(asset, script)
        elif asset == "english_camp_metatexts":
            entries = ui_entries(asset, script)
        else:
            continue
        rows.extend(entries)
        files.append({"asset": asset, "path_id": obj.path_id,
                      "source_sha256": hashlib.sha256(script.encode("utf-8")).hexdigest(),
                      "translatable_rows": len(entries)})
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        repeated = [key for key, value in collections.Counter(ids).items() if value > 1]
        raise ValueError(f"Duplicate catalog IDs: {repeated[:20]}")
    out = OUTPUT.parent
    out.mkdir(parents=True, exist_ok=True)
    catalog_file = out / "catalog.jsonl"
    with catalog_file.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    report = {"game_version": game_version, "files": files,
              "total": len(rows), "unique_english": len({x["english"] for x in rows}),
              "type_counts": dict(collections.Counter(x["kind"] for x in rows))}
    (out / "catalog_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
