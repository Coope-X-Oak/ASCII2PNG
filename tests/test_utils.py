import unittest
from ascii2png.utils import hex_to_rgb

class TestUtils(unittest.TestCase):
    def test_hex_to_rgb_standard(self):
        self.assertEqual(hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#FF0000"), (255, 0, 0))

    def test_hex_to_rgb_no_hash(self):
        self.assertEqual(hex_to_rgb("FFFFFF"), (255, 255, 255))
        
    def test_hex_to_rgb_invalid(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("ZZZZZZ")
        with self.assertRaises(ValueError):
            hex_to_rgb("123")
        self.assertEqual(hex_to_rgb(None), (0, 0, 0))
        self.assertEqual(hex_to_rgb(""), (0, 0, 0))

if __name__ == '__main__':
    unittest.main()
