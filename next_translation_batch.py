"""List untranslated Monster Camp events without changing any game files.

Usage:
    python next_translation_batch.py --limit 16
    python next_translation_batch.py --asset english_camp_events_endings --limit 12
    python next_translation_batch.py --include-partial --json

Files still being written may be invalid JSON. Complete translation files before
running this tool for a stable result.
"""

from __future__ import annotations

import argparse
import collections
import json

from build_preview import load_catalog, load_translations


def event_queue(catalog: dict, translations: dict, asset: str,
                include_partial: bool) -> list[dict]:
    grouped: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for entry_id, entry in catalog.items():
        if not entry["event"] or (asset and entry["asset"] != asset):
            continue
        grouped[(entry["asset"], entry["event"])].append(entry_id)

    pending = []
    for (source, event), ids in grouped.items():
        remaining = sum(entry_id not in translations for entry_id in ids)
        if remaining and (include_partial or remaining == len(ids)):
            pending.append({
                "asset": source,
                "event": event,
                "remaining": remaining,
                "total": len(ids),
                "suggested_file": (
                    "translations/maingame_" + event + "_ko.json"
                    if source == "english_camp_events_maingame"
                    else "translations/" + source.removeprefix("english_camp_events_")
                         + "_" + event + "_ko.json"
                ),
            })
    return pending


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset", default="english_camp_events_maingame")
    parser.add_argument("--limit", type=int, default=16)
    parser.add_argument("--include-partial", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")

    catalog = load_catalog()
    translations = load_translations(catalog)
    pending = event_queue(catalog, translations, args.asset, args.include_partial)
    chosen = pending[:args.limit]
    if args.json:
        print(json.dumps({
            "total_translated": len(translations),
            "remaining_events": len(pending),
            "next": chosen,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"{len(translations):,} translated; {len(pending):,} eligible untranslated events")
        for row in chosen:
            print(f"{row['event']:<30} {row['remaining']:>3}/{row['total']:<3} {row['suggested_file']}")


if __name__ == "__main__":
    main()
