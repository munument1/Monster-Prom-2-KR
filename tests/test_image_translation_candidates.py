"""Validate image lettering references without patching or distributing game art."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from extract_catalog import BUNDLES


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "image_translations" / "candidates.json"


class ImageTranslationCandidatesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = json.loads(CANDIDATES.read_text(encoding="utf-8"))["items"]

    def test_all_candidates_have_translated_lettering(self) -> None:
        self.assertTrue(self.entries)
        identities = set()
        for item in self.entries:
            key = (item["bundle"], item["texture_path_id"])
            self.assertNotIn(key, identities)
            identities.add(key)
            self.assertTrue(item["texture"])
            self.assertEqual(len(item["dimensions"]), 2)
            self.assertTrue(item["text"])
            for segment in item["text"]:
                self.assertTrue(segment["english"].strip())
                self.assertTrue(any("\uac00" <= char <= "\ud7a3"
                                    for char in segment["korean"]))

    def test_installed_texture_identity_if_available(self) -> None:
        import UnityPy

        if not all((BUNDLES / item["bundle"]).is_file() for item in self.entries):
            self.skipTest("Installed Monster Camp artwork bundles not available")
        for item in self.entries:
            with self.subTest(texture=item["texture"]):
                env = UnityPy.load(str(BUNDLES / item["bundle"]))
                matched = [obj for obj in env.objects
                           if obj.type.name == "Texture2D"
                           and obj.path_id == item["texture_path_id"]]
                self.assertEqual(len(matched), 1)
                texture = matched[0].read()
                self.assertEqual(texture.m_Name, item["texture"])
                self.assertEqual([texture.m_Width, texture.m_Height],
                                 item["dimensions"])


if __name__ == "__main__":
    unittest.main()
