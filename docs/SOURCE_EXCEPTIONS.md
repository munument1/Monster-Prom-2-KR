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

The ID-based `CustomLocalizationParser` cannot target these rows. All
19 have Korean translations recorded, but the native text export
intentionally omits them and lists them under `requires_asset_patch`
in `build/MonsterCampKR/manifest.json`.

If all translatable text is to display in the game, investigate a safe
mod-packaged asset override for these rows. Do **not** modify installed
original game bundles in place or fabricate a native ID.

### Read-only runtime-path review

Inspection of the installed game's `Assembly-CSharp.dll` and Addressables
catalog confirms that `CustomLocalizationParser.ValidateId` accepts
only IDs present in the original game's localization key collection.
`ModTool.CreateMod` creates a descriptor inside Unity's persistent-data
`Mods` directory; `CustomLocalizationManager.PrepareMod` reads
`Localization.txt`. The text events themselves are loaded via the
Addressables-backed event parser. Consequently, the stock Fan Translation
ModTool cannot reach these 19 lines merely by adding new invented IDs.

A reversible runtime `TextAsset`/Addressables override might be technically
possible, but **no supported asset-override registration/loader was verified
in the installed game**. A bundle copied into `Mods` is not a demonstrated
replacement method. Do not distribute a guessed loader or rewrite the
installed original bundles. Treat these 19 lines as *translated source data
awaiting a separately verified in-game application mechanism*.

Proof of full in-game localization would require controlled installation and
reversibility tests, a valid mod registration path, actual branch rendering
for these 19 rows, and font/layout verification.

## Historical numeral-style warnings (151 rows)

The coverage audit reports 151 non-fatal numeral-format differences in older
translation files. On 2026-10-24, all 151 warnings were compared against the
source English and Korean wording: **no confirmed numerical meaning errors**
were found. They were classified as legitimate Korean numeral wording or
contextual adaptations, not as 151 untranslated/missing lines. Examples include
`4 out of 5` -> `다섯 명 중 네 명`, `#3` -> `세 번째`, and the deliberately
localized `2 kool 4 skool` pun. Conversely, spelling an English number as
an Arabic digit can also trigger the warning without changing its meaning.

Do not auto-rewrite all 151 warnings to pass a digit-only comparison. Future
edits should preserve numerical meaning, game counters and variables, and be
reviewed one row at a time. New translation batches remain subject to the
stricter digit-counter check.

## Validation boundary

Catalog JSON, variable/numeric equivalence checks, and in-memory Unity
TextAsset rendering establish translation integrity. They do **not** prove
the text appears, fits, or has appropriate fonts in actual gameplay. The
game's ModTool registration and an in-game branch/UI smoke test remain
separate release criteria.
