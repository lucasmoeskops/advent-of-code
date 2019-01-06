import unittest
from .program import altsplit, is_valid_triangle, solve


class AltSplitTestCase(unittest.TestCase):
    def test_example(self):
        self.assertEqual(((101, 102, 103), (301, 302, 303), (501, 502, 503),
                          (201, 202, 203), (401, 402, 403), (601, 602, 603)),
                         tuple(altsplit(
                             ((101, 301, 501), (102, 302, 502), 
                              (103, 303, 503), (201, 401, 601),
                              (202, 402, 602), (203, 403, 603)))))


class IsValidTriangleTestCase(unittest.TestCase):
    def test_5_10_25_any_order(self):
        self.assertEqual(False, is_valid_triangle(5, 10, 25))
        self.assertEqual(False, is_valid_triangle(25, 10, 5))
        self.assertEqual(False, is_valid_triangle(5, 25, 10))

    def test_5_10_12_any_order(self):
        self.assertEqual(True, is_valid_triangle(5, 10, 12))
        self.assertEqual(True, is_valid_triangle(5, 12, 10))
        self.assertEqual(True, is_valid_triangle(12, 5, 10))


class SolveTestCase(unittest.TestCase):
    def test_5_10_25(self):
        from io import StringIO
        self.assertEqual(0, solve(StringIO('  5  10  25'))[0])

    def test_5_10_25_5_10_12(self):
        from io import StringIO
        self.assertEqual(1, solve(StringIO('5 10 25\n5 10 12'))[0])


if __name__ == '__main__':
    unittest.main()

