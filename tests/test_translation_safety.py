"""Regression tests for the most damaging translation file failures."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_preview


class TranslationSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "batch_ko.json"
        self.catalog = {
            f"english_camp_metatexts/TEST_{i}": {"english": "Welcome, %CURRENTPLAYERNAME%!"}
            for i in range(6)
        }

    def load(self, values: list[str]) -> dict[str, str]:
        data = {f"TEST_{i}": value for i, value in enumerate(values)}
        self.target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with patch.object(build_preview, "TRANSLATION_FILES", (self.target,)):
            return build_preview.load_translations(self.catalog)

    def test_valid_korean_keeps_tag(self) -> None:
        rows = self.load(["어서 와요, %CURRENTPLAYERNAME%!"] * 6)
        self.assertEqual(len(rows), 6)

    def test_fully_corrupted_question_marks_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "lost Korean"):
            self.load(["?? ????, %CURRENTPLAYERNAME%!"] * 6)

    def test_partly_corrupted_question_marks_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "encoding loss|corrupted Korean"):
            self.load(["환영합니다, %CURRENTPLAYERNAME%! ??? ????? ??? ?????"] * 6)

    def test_changed_variable_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "token mismatch"):
            self.load(["어서 와요, %OTHERNAME%!"] * 6)

    def test_nested_sp_token_is_indivisible(self) -> None:
        expected = "%GOSSIPQUALITY_RUN_DRY[sp]HUMP%"
        changed = "%GOSSIPQUALITY_BOGUS[sp]BOGUS%"
        self.assertEqual(build_preview.TOKEN.findall(expected), [expected])
        self.assertNotEqual(build_preview.TOKEN.findall(expected),
                            build_preview.TOKEN.findall(changed))


if __name__ == "__main__":
    unittest.main()
