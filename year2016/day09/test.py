import unittest
from program import decompress, decompressedv2_length


class DecompressTestCase(unittest.TestCase):
    def test(self):
        f = decompress
        self.assertEqual('ADVENT', f('ADVENT'))
        self.assertEqual('ABBBBBC', f('A(1x5)BC'))
        self.assertEqual('XYZXYZXYZ', f('(3x3)XYZ'))
        self.assertEqual('ABCBCDEFEFG', f('A(2x2)BCD(2x2)EFG'))
        self.assertEqual('(1x3)A', f('(6x1)(1x3)A'))
        self.assertEqual('X(3x3)ABC(3x3)ABCY', f('X(8x2)(3x3)ABCY'))


class Decompressv2LenTestCase(unittest.TestCase):
    def test(self):
        f = decompressedv2_length
        self.assertEqual(9, f('(3x3)XYZ'))
        self.assertEqual(20, f('X(8x2)(3x3)ABCY'))
        self.assertEqual(241920, f('(27x12)(20x12)(13x14)(7x10)(1x12)A'))
        self.assertEqual(
                445,
                f('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
        )


if __name__ == '__main__':
    unittest.main()

