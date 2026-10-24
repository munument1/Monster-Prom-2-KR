"""Regression tests for player-visible Korean stat terminology."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "translations"
PLACEHOLDER = re.compile(r"%[^%\r\n]+%|<[^>]*>")
UNTRANSLATED_STAT = re.compile(
    r"(?<![A-Za-z_])(?:BOLDNESS|CREATIVITY|CHARM|FUN|SMARTS|MONEY)"
    r"(?![A-Za-z_])"
)


class TranslationStyleTests(unittest.TestCase):
    def test_stat_names_are_localized_outside_placeholders(self) -> None:
        untranslated: list[str] = []
        for path in sorted(TRANSLATIONS.glob("*_ko.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            for key, value in data.items():
                visible_text = PLACEHOLDER.sub("", value)
                if UNTRANSLATED_STAT.search(visible_text):
                    untranslated.append(f"{path.name}: {key}: {value}")
        self.assertEqual(untranslated, [])

    def test_player_name_placeholder_uses_consonant_final_particles(self) -> None:
        invalid_suffixes = ("가", "는", "를", "와", "랑", "로", "잖아")
        invalid: list[str] = []
        for path in sorted(TRANSLATIONS.glob("*_ko.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            for key, value in data.items():
                for placeholder in ("%CURRENTPLAYERNAME%", "%CURRENTPLAYERNAMECAPS%"):
                    for suffix in invalid_suffixes:
                        if placeholder + suffix in value:
                            invalid.append(f"{path.name}: {key}: {placeholder}{suffix}")
        self.assertEqual(invalid, [])


if __name__ == "__main__":
    unittest.main()
