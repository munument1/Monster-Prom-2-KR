"""Inventory installed Monster Camp images without changing source bundles.

    python inspect_images.py
    python inspect_images.py --preview-count 3 --preview-max-mib 6
    python inspect_images.py --bundle metashop_assets_all.bundle --preview-count 2

Only ignored work/image_inventory.json and optional work/images_preview/*.png
are written. Candidate names are heuristic; this script does not perform OCR.
"""

from __future__ import annotations

import argparse
import collections
import io
import json
import re
from pathlib import Path

import UnityPy
from UnityPy.enums.TextureFormat import TextureFormat

from extract_catalog import BUNDLES


ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
INVENTORY = WORK / "image_inventory.json"
PREVIEW_DIR = WORK / "images_preview"

# These are hints in filenames, not evidence that pixels contain English text.
TEXT_HINTS = (
    "text", "letter", "word", "font", "language", "english", "en_",
    "title", "logo", "banner", "poster", "sign", "label", "caption",
    "subtitle", "dialog", "speech", "credit", "tutorial", "instruction",
    "menu", "button", "icon_ui", "ui_", "interface", "loading", "splash",
    "badge", "map", "notice", "calendar", "board", "ticket", "note",
    "card", "book", "screen", "panel", "achievement", "shop",
)


def format_name(value: object) -> str:
    try:
        return TextureFormat(int(value)).name
    except (TypeError, ValueError):
        return f"Unknown({value})"


def alpha_capability(texture_format: str) -> str:
    """Can this pixel format carry alpha? Not a pixel-transparency test."""
    fmt = texture_format.upper()
    if "DXT1" in fmt or fmt == "BC1":
        return "possible"
    if any(part in fmt for part in (
        "RGBA", "ARGB", "BGRA", "ALPHA", "DXT3", "DXT5", "BC2",
        "BC3", "BC7", "ATC_RGBA", "ASTC", "ETC2_RGBA",
    )):
        return "yes"
    if fmt.startswith(("RGB", "R8", "R16", "RHALF", "RFLOAT", "RG", "BC4", "BC5", "BC6", "EAC", "ETC", "ATC_RGB", "PVRTC_RGB")):
        return "no"
    return "unknown"


def hints_for(name: str) -> list[str]:
    lowered = name.lower()
    parts = set(re.split(r"[^a-z0-9]+", lowered))
    matched = []
    for hint in TEXT_HINTS:
        # "green_*" is not the English locale "en_*"; "textured" is
        # not an illustration with text. Avoid these common false positives.
        if hint == "en_":
            yes = "en" in parts
        elif hint == "text":
            yes = "text" in parts or "texts" in parts
        elif hint in ("sign", "note", "map", "card", "book", "word"):
            yes = hint in parts or any(p.startswith(hint) for p in parts)
        else:
            yes = hint in lowered
        if yes:
            matched.append(hint)
    return matched


def rect_data(value: object) -> dict[str, float] | None:
    if not isinstance(value, dict):
        return None
    fields = ("x", "y", "width", "height")
    if not all(isinstance(value.get(k), (int, float)) for k in fields):
        return None
    return {k: round(float(value[k]), 3) for k in fields}


def reference(value: object) -> dict[str, int] | None:
    if not isinstance(value, dict):
        return None
    file_id = value.get("m_FileID")
    path_id = value.get("m_PathID")
    if not isinstance(file_id, int) or not isinstance(path_id, int) or path_id == 0:
        return None
    return {"file_id": file_id, "path_id": path_id}


def output_paths_are_safe(preview: bool) -> None:
    """Reject redirected output paths; no write must ever reach the game."""
    targets = [WORK, INVENTORY]
    if preview:
        targets.append(PREVIEW_DIR)
    if any(path.is_symlink() for path in targets):
        raise ValueError("Inventory/preview output may not be a symbolic link")
    root = ROOT.resolve()
    for path in targets:
        if root not in path.resolve().parents:
            raise ValueError(f"Output path escapes project: {path}")


def bundle_selection(names: list[str], maximum: int) -> list[Path]:
    if not BUNDLES.is_dir():
        raise FileNotFoundError(f"Installed Monster Camp bundles not found: {BUNDLES}")
    available = {p.name: p for p in sorted(BUNDLES.glob("*.bundle")) if p.is_file()}
    if names:
        missing = sorted(set(names) - available.keys())
        if missing:
            raise ValueError(f"Unknown bundle name(s): {', '.join(missing)}")
        chosen = [available[name] for name in sorted(set(names))]
    else:
        chosen = list(available.values())
    return chosen[:maximum] if maximum else chosen


def collect(bundles: list[Path]) -> dict:
    report = {
        "schema_version": 1,
        "bundle_directory": str(BUNDLES),
        "bundles_scanned": [p.name for p in bundles],
        "summary": {},
        "by_bundle": {},
        "textures": [],
        "sprites": [],
        "sprite_atlases": [],
        "atlas_analysis": {},
        "suspected_english_text": {},
        "previews": [],
        "errors": [],
    }
    formats = collections.Counter()
    suspicion = collections.Counter()
    types = collections.Counter()
    alpha = collections.Counter()
    groupings = collections.defaultdict(list)
    explicit_atlas = 0
    for source in bundles:
        bundle_name = source.name
        bundle_stats = collections.Counter()
        try:
            env = UnityPy.load(str(source))
            objects = [obj for obj in env.objects if obj.type.name in ("Texture2D", "Sprite", "SpriteAtlas")]
        except Exception as exc:
            report["errors"].append({"bundle": bundle_name, "error": f"load: {type(exc).__name__}: {exc}"})
            continue
        for obj in objects:
            kind = obj.type.name
            try:
                tree = obj.read_typetree()
                name = str(tree.get("m_Name", ""))
                common = {
                    "name": name,
                    "bundle": bundle_name,
                    "serialized_file": str(obj.assets_file.name),
                    "path_id": obj.path_id,
                }
                if kind == "Texture2D":
                    fmt = format_name(tree.get("m_TextureFormat"))
                    cap = alpha_capability(fmt)
                    stream = tree.get("m_StreamData") or {}
                    cues = hints_for(name)
                    item = {
                        **common,
                        "width": tree.get("m_Width"),
                        "height": tree.get("m_Height"),
                        "texture_format": fmt,
                        "alpha_capability": cap,
                        "alpha_nonopaque": None,  # known only for decoded previews
                        "image_bytes_reported": tree.get("m_CompleteImageSize", 0),
                        "streamed_bytes_reported": stream.get("size", 0),
                        "suspected_text_keywords": cues,
                    }
                    report["textures"].append(item)
                    formats[fmt] += 1
                    alpha[cap] += 1
                    suspicion.update(cues)
                    if cues:
                        bundle_stats["suspected_textures"] += 1
                elif kind == "Sprite":
                    rd = tree.get("m_RD") or {}
                    texture = reference(rd.get("texture"))
                    atlas = reference(tree.get("m_SpriteAtlas"))
                    cues = hints_for(name)
                    item = {
                        **common,
                        "width": (tree.get("m_Rect") or {}).get("width"),
                        "height": (tree.get("m_Rect") or {}).get("height"),
                        "sprite_rect": rect_data(tree.get("m_Rect")),
                        "texture_rect": rect_data(rd.get("textureRect")),
                        "texture_ref": texture,
                        "alpha_texture_ref": reference(rd.get("alphaTexture")),
                        "sprite_atlas_ref": atlas,
                        "atlas_tags": tree.get("m_AtlasTags", []),
                        "suspected_text_keywords": cues,
                    }
                    report["sprites"].append(item)
                    if texture:
                        groupings[(bundle_name, texture["file_id"], texture["path_id"])].append(item)
                    if atlas or item["atlas_tags"]:
                        explicit_atlas += 1
                    if cues:
                        bundle_stats["suspected_sprites"] += 1
                else:
                    packed = tree.get("m_PackedSprites") or []
                    report["sprite_atlases"].append({
                        **common,
                        "packed_sprites_count": len(packed),
                        "packed_sprite_refs": [ref for ref in (reference(v) for v in packed) if ref],
                        "render_data_entry_count": len(tree.get("m_RenderDataMap") or []),
                    })
                types[kind] += 1
                bundle_stats[kind] += 1
            except Exception as exc:
                report["errors"].append({
                    "bundle": bundle_name, "object_type": kind,
                    "path_id": obj.path_id, "error": f"{type(exc).__name__}: {exc}",
                })
        report["by_bundle"][bundle_name] = dict(bundle_stats)
        del objects, env

    # Resolve local references only; file_id != 0 points to an external serialized file.
    textures_by_id = {(t["bundle"], t["path_id"]): t for t in report["textures"]}
    resolved = 0
    shared = []
    for sprite in report["sprites"]:
        ref = sprite["texture_ref"]
        if ref and ref["file_id"] == 0:
            target = textures_by_id.get((sprite["bundle"], ref["path_id"]))
            if target:
                sprite["texture_name"] = target["name"]
                sprite["texture_width"] = target["width"]
                sprite["texture_height"] = target["height"]
                sprite["alpha_capability"] = target["alpha_capability"]
                sprite["alpha_nonopaque"] = target["alpha_nonopaque"]
                resolved += 1
    for (bundle, file_id, path_id), sprites in sorted(groupings.items()):
        if len(sprites) > 1:
            shared.append({"bundle": bundle, "file_id": file_id, "texture_path_id": path_id,
                           "sprite_count": len(sprites),
                           "sprite_names": [s["name"] for s in sprites]})
    report["summary"] = {
        "bundle_count": len(bundles),
        "textures": types["Texture2D"],
        "sprites": types["Sprite"],
        "sprite_atlas_objects": types["SpriteAtlas"],
        "texture_formats": dict(formats.most_common()),
        "alpha_format_capability": dict(alpha),
        "suspected_textures": sum(bool(t["suspected_text_keywords"]) for t in report["textures"]),
        "suspected_sprites": sum(bool(s["suspected_text_keywords"]) for s in report["sprites"]),
        "object_errors": len(report["errors"]),
    }
    report["suspected_english_text"] = {
        "method": "case-insensitive filename keywords only; images have not been OCR-scanned",
        "keyword_counts_textures": dict(suspicion.most_common()),
        "example_texture_names": [t["name"] for t in report["textures"] if t["suspected_text_keywords"]][:100],
    }
    report["atlas_analysis"] = {
        "sprite_atlas_objects": len(report["sprite_atlases"]),
        "sprites_with_atlas_reference_or_tags": explicit_atlas,
        "sprites_with_resolved_local_texture": resolved,
        "textures_referenced_by_multiple_sprites": len(shared),
        "shared_texture_groups": shared,
        "note": "Shared textures indicate potential sprite packing; no SpriteAtlas object is required.",
    }
    return report


def write_previews(report: dict, args: argparse.Namespace) -> None:
    """Reopen only selected bundles, decode capped images, save bounded PNGs."""
    if not args.preview_count:
        return
    budget = int(args.preview_max_mib * 1048576)
    max_input_bytes = int(args.preview_max_source_mib * 1048576)
    candidates = [t for t in report["textures"] if
                  isinstance(t["width"], int) and isinstance(t["height"], int)
                  and 0 < t["width"] * t["height"] <= args.preview_max_pixels
                  and max(t["width"], t["height"]) > 0
                  and max(t["image_bytes_reported"], t["streamed_bytes_reported"]) <= max_input_bytes]
    strong_hints = {"english", "en_", "text", "word", "subtitle", "dialog",
                    "caption", "credit", "logo", "title", "letter", "banner",
                    "poster", "sign", "tutorial", "instruction"}
    candidates.sort(key=lambda t: (
        -sum(5 if h in strong_hints else 1 for h in t["suspected_text_keywords"]),
        t["bundle"], t["name"], t["path_id"],
    ))
    targets = candidates[:args.preview_count]
    if not targets:
        return
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    per_bundle = collections.defaultdict(list)
    for item in targets:
        per_bundle[item["bundle"]].append(item)
    used = 0
    # Count existing ignored previews too, so repeated runs cannot silently
    # accumulate an unlimited amount of files. Never delete earlier previews.
    total_disk_usage = sum(p.stat().st_size for p in PREVIEW_DIR.glob("*.png") if p.is_file())
    for bundle, rows in per_bundle.items():
        try:
            env = UnityPy.load(str(BUNDLES / bundle))
            by_id = {o.path_id: o for o in env.objects if o.type.name == "Texture2D"}
        except Exception as exc:
            report["errors"].append({"bundle": bundle, "error": f"preview-load: {type(exc).__name__}: {exc}"})
            continue
        for t in rows:
            try:
                image = by_id[t["path_id"]].read().image
                # This tests actual pixels only on selected, decoded previews.
                if "A" in image.getbands():
                    alpha_min, alpha_max = image.getchannel("A").getextrema()
                    t["alpha_nonopaque"] = alpha_min < 255
                    t["preview_alpha_extrema"] = [alpha_min, alpha_max]
                image.thumbnail((args.preview_max_side, args.preview_max_side))
                binary = io.BytesIO()
                image.save(binary, format="PNG", optimize=True)
                png = binary.getvalue()
                safe_name = re.sub(r"[^a-z0-9_-]+", "_", t["name"].lower())[:48].strip("_") or "unnamed"
                filename = f"{Path(bundle).stem}_{t['path_id']}_{safe_name}.png"
                destination = PREVIEW_DIR / filename
                if destination.is_symlink():
                    raise ValueError("Preview destination may not be a symbolic link")
                old_size = destination.stat().st_size if destination.exists() else 0
                if total_disk_usage - old_size + len(png) > budget:
                    report["previews"].append({"bundle": bundle, "path_id": t["path_id"],
                                               "skipped": "preview directory PNG size budget exceeded"})
                    continue
                destination.write_bytes(png)
                used += len(png)
                total_disk_usage += len(png) - old_size
                report["previews"].append({"bundle": bundle, "name": t["name"],
                                           "path_id": t["path_id"],
                                           "file": str(destination.relative_to(ROOT)),
                                           "bytes": len(png), "pixel_size": list(image.size)})
            except Exception as exc:
                report["errors"].append({"bundle": bundle, "path_id": t["path_id"],
                                         "error": f"preview: {type(exc).__name__}: {exc}"})
        del by_id, env
    report["summary"]["preview_bytes_written"] = used
    report["summary"]["preview_directory_bytes"] = total_disk_usage
    refreshed = {(t["bundle"], t["path_id"]): t for t in report["textures"]}
    for sprite in report["sprites"]:
        ref = sprite["texture_ref"]
        if ref and ref["file_id"] == 0:
            target = refreshed.get((sprite["bundle"], ref["path_id"]))
            if target:
                sprite["alpha_nonopaque"] = target["alpha_nonopaque"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", action="append", default=[], metavar="FILENAME",
                        help="Scan only this exact .bundle filename (repeatable)")
    parser.add_argument("--max-bundles", type=int, default=0,
                        help="Maximum bundles to scan; 0 = all (default)")
    parser.add_argument("--preview-count", type=int, default=0,
                        help="Opt in to up to N small PNG previews (default 0, hard limit 12)")
    parser.add_argument("--preview-max-mib", type=float, default=8,
                        help="Total bytes of newly written previews (MiB, max 16)")
    parser.add_argument("--preview-max-source-mib", type=float, default=16,
                        help="Skip images with larger encoded source payload (MiB, max 32)")
    parser.add_argument("--preview-max-pixels", type=int, default=4_000_000,
                        help="Skip images exceeding this source pixel count (max 16 million)")
    parser.add_argument("--preview-max-side", type=int, default=768,
                        help="Maximum dimension of preview PNGs (max 1024)")
    args = parser.parse_args()
    if args.max_bundles < 0:
        parser.error("--max-bundles must be nonnegative")
    if not 0 <= args.preview_count <= 12:
        parser.error("--preview-count must be between 0 and 12")
    if not 0 < args.preview_max_mib <= 16:
        parser.error("--preview-max-mib must be > 0 and <= 16")
    if not 0 < args.preview_max_source_mib <= 32:
        parser.error("--preview-max-source-mib must be > 0 and <= 32")
    if not 0 < args.preview_max_pixels <= 16_000_000:
        parser.error("--preview-max-pixels must be > 0 and <= 16000000")
    if not 0 < args.preview_max_side <= 1024:
        parser.error("--preview-max-side must be > 0 and <= 1024")
    output_paths_are_safe(args.preview_count > 0)
    files = bundle_selection(args.bundle, args.max_bundles)
    report = collect(files)
    report["scan_options"] = {
        "selected_bundles": args.bundle, "max_bundles": args.max_bundles,
        "preview_count": args.preview_count, "preview_max_mib": args.preview_max_mib,
        "preview_max_source_mib": args.preview_max_source_mib,
        "preview_max_pixels": args.preview_max_pixels,
        "preview_max_side": args.preview_max_side,
    }
    write_previews(report, args)
    report["summary"]["object_errors"] = len(report["errors"])
    WORK.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inventory": str(INVENTORY), "summary": report["summary"],
                      "atlas_analysis": {k: v for k, v in report["atlas_analysis"].items() if k != "shared_texture_groups"},
                      "previews_created": sum("file" in x for x in report["previews"]),
                      "errors": report["errors"][:5]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
