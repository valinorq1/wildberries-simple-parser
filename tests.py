import unittest
from utils import clear_string

class TestClearingString(unittest.TestCase):
    def test_clearing(self):
        fmt = clear_string('1212йцу')
        self.assertEqual(fmt, '1212')

if __name__ == '__main__':
    unittest.main()
