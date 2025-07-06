import unittest
from target import add


class TestBasic(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
