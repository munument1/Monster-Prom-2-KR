"""Regression checks for automatic non-overlapping event selection."""

from __future__ import annotations

import unittest

from next_translation_batch import event_queue


class QueueTests(unittest.TestCase):
    def test_skips_completed_and_partial_by_default(self) -> None:
        catalog = {
            "a": {"asset": "english_camp_events_maingame", "event": "a"},
            "b": {"asset": "english_camp_events_maingame", "event": "a"},
            "c": {"asset": "english_camp_events_maingame", "event": "b"},
            "d": {"asset": "english_camp_events_maingame", "event": "c"},
            "e": {"asset": "english_camp_events_maingame", "event": "c"},
        }
        translations = {"a": "하나", "d": "넷", "e": "다섯"}
        default = event_queue(catalog, translations, "english_camp_events_maingame", False)
        self.assertEqual([v["event"] for v in default], ["b"])
        partial = event_queue(catalog, translations, "english_camp_events_maingame", True)
        self.assertEqual([v["event"] for v in partial], ["a", "b"])
        self.assertEqual(partial[0]["remaining"], 1)

    def test_asset_filter(self) -> None:
        catalog = {
            "a": {"asset": "english_camp_events_maingame", "event": "one"},
            "b": {"asset": "english_camp_events_endings", "event": "one"},
            "c": {"asset": "english_camp_events_endings", "event": "two"},
        }
        rows = event_queue(catalog, {}, "english_camp_events_endings", False)
        self.assertEqual([r["event"] for r in rows], ["one", "two"])
        self.assertTrue(rows[0]["suggested_file"].endswith("/endings_one_ko.json"))


if __name__ == "__main__":
    unittest.main()
