"""Prevent a future translation pass from corrupting source-only values."""

from __future__ import annotations

import unittest

from audit_translation_coverage import (
    PRESERVED, PRESERVED_META, PRESERVED_PLACEHOLDERS,
)
from build_preview import load_catalog
from build_mod import localization_key


class SourceExceptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()

    def test_six_numeric_ui_choices_must_remain_source_values(self) -> None:
        self.assertEqual(len(PRESERVED_META), 6)
        for key in PRESERVED_META:
            with self.subTest(key=key):
                self.assertIn(key, self.catalog)
                self.assertTrue(self.catalog[key]["english"].isdecimal())

    def test_seven_internal_branch_placeholders_not_game_dialogue(self) -> None:
        self.assertEqual(len(PRESERVED_PLACEHOLDERS), 7)
        for key in PRESERVED_PLACEHOLDERS:
            with self.subTest(key=key):
                self.assertIn(key, self.catalog)
                self.assertIn(self.catalog[key]["english"],
                              {"PLACEHOLDER", "C1", "C2"})
        self.assertEqual(len(PRESERVED), 13)

    def test_nineteen_non_native_source_lines_are_never_exported(self) -> None:
        missing_native_id = [
            item for item in self.catalog.values()
            if item["kind"] == "event" and
            item["key"].split("/")[-2].startswith("line-")
        ]
        self.assertEqual(len(missing_native_id), 19)
        for item in missing_native_id:
            with self.subTest(source=item["id"]):
                with self.assertRaisesRegex(ValueError, "No stable native"):
                    localization_key(item)


if __name__ == "__main__":
    unittest.main()
