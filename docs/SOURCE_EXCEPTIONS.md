# Source rows requiring special handling

This audit is for **Monster Prom 2: Monster Camp**, not the first game.
The source catalog has 33,850 rows. A translated/loaded row and a row
actually addressable by the game's native `Localization.txt` are different
concepts; the build manifest distinguishes them.

## Preserved, non-linguistic source values (13 rows)

- Six duration values `english_camp_metatexts/GME_DRT_30`,
  `GME_DRT_45`, `GME_DRT_60`, `GME_DRT_70`, `GME_DRT_90`,
  `GME_DRT_120` contain only the integers `30`, `45`, `60`, `70`,
  `90`, `120`. They must remain unchanged rather than be misrepresented
  as Korean translations. `build_preview.load_translations()` currently
  rejects unchanged English/source values.
- Seven values in `english_camp_events_maingame/bp_miloyolo3` contain only
  `PLACEHOLDER`, `C1`, or `C2`. The actual storyline has separately
  extracted `bp_miloyolo3_intro`, `bp_miloyolo3_gossip`, and
  `bp_miloyolo3_outro_*` records, already translated. Do not invent
  dialogue to fill these internal placeholders.

These 13 rows should remain deliberately unchanged. A raw 100% catalog
coverage metric would be misleading without accounting for them.

## Text with no native localization ID (19 rows)

The original event assets contain **19 dialogue/source rows** with synthetic
`line-...` identifiers instead of native localization IDs:

- 14 drink-event rows;
- three `antterrarium2` rows;
- one `strandedinthelake` row;
- one `bandrehearsal` row.

The ID-based `CustomLocalizationParser` cannot target these rows. The
first 18 have Korean translations recorded, but the native text export
intentionally omits them and lists them under `requires_asset_patch`
in `build/MonsterCampKR/manifest.json`. The remaining
`bandrehearsal` row is part of unfinished source coverage.

If all translatable text is to display in the game, investigate a safe
mod-packaged asset override for these rows. Do **not** modify installed
original game bundles in place or fabricate a native ID.

## Validation boundary

Catalog JSON, variable/numeric equivalence checks, and in-memory Unity
TextAsset rendering establish translation integrity. They do **not** prove
the text appears, fits, or has appropriate fonts in actual gameplay. The
game's ModTool registration and an in-game branch/UI smoke test remain
separate release criteria.
