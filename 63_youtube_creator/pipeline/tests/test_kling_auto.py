import asyncio
import os
import tempfile
import unittest

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import kling_auto


class KlingAutoTests(unittest.TestCase):
    def test_generate_scene_image_returns_false_without_cookies(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.jpg")
            original_cookie_path = kling_auto.COOKIE_PATH
            kling_auto.COOKIE_PATH = os.path.join(tmpdir, "missing_cookies.json")
            try:
                result = asyncio.run(kling_auto.generate_scene_image("test prompt", output_path))
            finally:
                kling_auto.COOKIE_PATH = original_cookie_path
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
