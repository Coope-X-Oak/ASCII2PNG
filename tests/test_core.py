import unittest
import os
import shutil
from ascii2png.core import CoreService
from ascii2png import parser

class TestCoreService(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests_output"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_parser_basic(self):
        text = """
        +---+   +---+
        | A |-->| B |
        +---+   +---+
        """
        root = parser.parse(text)
        self.assertIsNotNone(root)
        # Verify structure roughly (implementation detail dependent)
        self.assertTrue(len(root.children) > 0)

    def test_convert_generation(self):
        text = "test"
        path = CoreService.convert(
            text=text,
            output_dir=self.test_dir,
            filename_hint="test_case"
        )
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".png"))
        self.assertIn("test_case", path)

    def test_custom_colors(self):
        text = "color test"
        custom_colors = {
            "bg": (255, 0, 0),
            "text": (0, 255, 0),
            "line": (0, 0, 255)
        }
        path = CoreService.convert(
            text=text,
            output_dir=self.test_dir,
            custom_colors=custom_colors
        )
        self.assertTrue(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
