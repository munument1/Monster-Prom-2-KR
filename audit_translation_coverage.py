"""Read-only translation integrity and coverage audit.

Default: audit *committed* files, so incomplete work-in-progress JSON files
from parallel translators cannot break a verified release snapshot.
Use --working only once all writers have finished their files.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
from pathlib import Path

import build_preview


ROOT = Path(__file__).resolve().parent
NUMBERS = re.compile(r"[0-9]+")

# Intentionally unchanged engine/UI values; see docs/SOURCE_EXCEPTIONS.md.
PRESERVED_META = {f"english_camp_metatexts/GME_DRT_{n}" for n in
                  (30, 45, 60, 70, 90, 120)}
PRESERVED_PLACEHOLDERS = {
    "english_camp_events_maingame/bp_miloyolo3/"
    f"bp_miloyolo3_{suffix}/col-3"
    for suffix in ("PRE_1", "CHO_1", "CHO_2", "OUT_1_SUC_1",
                   "OUT_1_FAIL_1", "OUT_2_SUC_1", "OUT_2_FAIL_1")
}
PRESERVED = PRESERVED_META | PRESERVED_PLACEHOLDERS


def translation_files(include_working: bool) -> list[Path]:
    if include_working:
        return sorted((ROOT / "translations").glob("*_ko.json"))
    names = subprocess.check_output(
        ["git", "ls-files", "--", "translations/*_ko.json"],
        cwd=ROOT, text=True, encoding="utf-8",
    ).splitlines()
    return [ROOT / name for name in names]


def batch_manifest(path: Path) -> Path | None:
    stem = path.stem
    patterns = {
        "maingame_batch_": "main",
        "endings_batch_": "endings",
        "gossips_batch_": "gossips",
        "icebreakers_batch_": "icebreakers",
        "metatexts_batch_": "meta",
        "meta_batch_": "meta",
    }
    for prefix, folder in patterns.items():
        if stem.startswith(prefix):
            suffix = stem.removeprefix(prefix).removesuffix("_ko")
            if len(suffix) == 2 and suffix.isdecimal():
                return ROOT / "work" / "translation_batches" / folder / (
                    f"batch_{suffix}.json")
    return None


def audit(include_working: bool) -> int:
    catalog = build_preview.load_catalog()
    files = translation_files(include_working)
    errors: list[str] = []
    numeric_warnings: list[str] = []
    no_hangul: list[str] = []
    translated: dict[str, str] = {}
    asset_count = collections.Counter()

    for path in files:
        try:
            payload = path.read_bytes()
            if payload.startswith(b"\xef\xbb\xbf"):
                errors.append(f"{path.name}: UTF-8 BOM")
            data = json.loads(
                payload.decode("utf-8"),
                object_pairs_hook=build_preview._reject_duplicate_json_keys,
            )
        except (UnicodeDecodeError, ValueError, OSError) as exc:
            errors.append(f"{path.name}: unreadable JSON: {exc}")
            continue
        manifest = batch_manifest(path)
        if manifest and manifest.is_file():
            expected = [row["id"] for row in json.loads(
                manifest.read_text(encoding="utf-8"))]
            if list(data) != expected:
                errors.append(f"{path.name}: source ID/order mismatch "
                              f"({len(data)} vs {len(expected)})")
        for key, korean in data.items():
            source_id = key if "/" in key else f"english_camp_metatexts/{key}"
            if source_id not in catalog:
                errors.append(f"{path.name}: unknown ID {source_id}")
                continue
            if source_id in translated:
                errors.append(f"{path.name}: duplicate ID {source_id}")
                continue
            if not isinstance(korean, str) or not korean.strip():
                errors.append(f"{source_id}: empty/non-string translation")
                continue
            source = catalog[source_id]["english"]
            # Triple question marks are legitimate *source* punctuation in
            # this game's dialogue. Flag only newly introduced runs.
            damaged_punctuation = korean.count("???") > source.count("???")
            if (korean == source or any(c in korean for c in "\r\n\t\ufffd")
                    or damaged_punctuation):
                errors.append(f"{source_id}: unchanged/invalid control text")
            old = collections.Counter(build_preview.TOKEN.findall(source))
            new = collections.Counter(build_preview.TOKEN.findall(korean))
            if old != new:
                errors.append(f"{source_id}: formatting/variable mismatch")
            if not any("\uac00" <= c <= "\ud7a3" for c in korean):
                no_hangul.append(source_id)
            if collections.Counter(NUMBERS.findall(source)) != collections.Counter(
                    NUMBERS.findall(korean)):
                # Historical translations may spell numbers in Korean rather than
                # digits. New batch files are held to stricter source equality.
                if manifest is not None:
                    errors.append(f"{source_id}: batch digit mismatch")
                else:
                    numeric_warnings.append(source_id)
            translated[source_id] = korean
            asset_count[catalog[source_id]["asset"]] += 1

    missing = set(catalog) - set(translated)
    meaningful_missing = missing - PRESERVED
    accidentally_translated = PRESERVED & set(translated)
    if accidentally_translated:
        errors.append("Engine numeric/placeholder values must stay unchanged: "
                      f"{sorted(accidentally_translated)}")
    unsupported = [k for k in translated if
                   catalog[k]["kind"] == "event" and
                   catalog[k]["key"].split("/")[-2].startswith("line-")]
    preserved_unexpected = PRESERVED - set(catalog)
    if preserved_unexpected:
        errors.append(f"Preserved exception IDs missing from catalog: "
                      f"{sorted(preserved_unexpected)}")
    print(f"Translation files: {len(files)}")
    print(f"Translated: {len(translated):,} / {len(catalog):,}")
    print(f"Meaningful untranslated: {len(meaningful_missing):,}")
    print(f"Preserved engine values/placeholders: {len(missing & PRESERVED)}")
    print(f"Translated rows without native ID: {len(unsupported)}")
    print(f"Historical numeric-style warnings: {len(numeric_warnings)}")
    print(f"Existing translations with no Hangul: {len(no_hangul)}")
    for asset, count in sorted(asset_count.items()):
        print(f"  {asset}: {count:,}")
    if meaningful_missing:
        print("Top remaining assets:",
              collections.Counter(catalog[k]["asset"] for k in
                                  meaningful_missing).most_common())
    for message in errors[:30]:
        print("ERROR:", message)
    if len(errors) > 30:
        print(f"... and {len(errors)-30} more errors")
    print(f"Audit status: {'FAIL' if errors else 'PASS'}")
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--working", action="store_true",
        help="include uncommitted JSON (only when every writer has finished)",
    )
    options = parser.parse_args()
    raise SystemExit(audit(options.working))
