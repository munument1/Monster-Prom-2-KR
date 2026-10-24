"""Summarize verified Korean translations by source asset and event.

Run after extract_catalog.py. The report is stored under ignored work/.
"""

from __future__ import annotations

import collections
import json
from datetime import datetime, timezone

from build_preview import OUTPUT, load_catalog, load_translations


def main() -> None:
    catalog = load_catalog()
    translated = load_translations(catalog)
    total_by_asset = collections.Counter()
    done_by_asset = collections.Counter()
    total_by_event = collections.Counter()
    done_by_event = collections.Counter()

    for entry_id, entry in catalog.items():
        asset = entry["asset"]
        total_by_asset[asset] += 1
        if entry["event"]:
            total_by_event[f"{asset}/{entry['event']}"] += 1
        if entry_id in translated:
            done_by_asset[asset] += 1
            if entry["event"]:
                done_by_event[f"{asset}/{entry['event']}"] += 1

    files = [
        {
            "asset": asset,
            "translated": done_by_asset[asset],
            "total": total,
            "percent": round(100 * done_by_asset[asset] / total, 2),
        }
        for asset, total in total_by_asset.items()
    ]
    events = [
        {
            "event": event,
            "translated": done_by_event[event],
            "total": total,
            "complete": done_by_event[event] == total,
        }
        for event, total in total_by_event.items()
    ]
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "translated": len(translated),
        "total": len(catalog),
        "percent": round(100 * len(translated) / len(catalog), 2),
        "complete_events": sum(e["complete"] for e in events),
        "total_events": len(events),
        "assets": files,
        "events": events,
    }
    output = OUTPUT.parent / "progress.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Translated {report['translated']:,} / {report['total']:,} ({report['percent']}%)")
    print(f"Complete events: {report['complete_events']} / {report['total_events']}")
    for entry in files:
        print(f"  {entry['asset']}: {entry['translated']:,} / {entry['total']:,} ({entry['percent']}%)")


if __name__ == "__main__":
    main()
