import unittest
from program import change_face, determine_distance, first_revisited_location, \
        positions, solve


class ChangeFaceTestCase(unittest.TestCase):
    def test_north_right(self):
        self.assertEqual(1, change_face(-1j, 1))
    
    def test_east_right(self):
        self.assertEqual(1j, change_face(1, 1))
    
    def test_south_right(self):
        self.assertEqual(-1, change_face(1j, 1))
    
    def test_west_right(self):
        self.assertEqual(-1j, change_face(-1, 1))
    
    def test_north_left(self):
        self.assertEqual(-1, change_face(-1j, -1))
    
    def test_west_left(self):
        self.assertEqual(1j, change_face(-1, -1))
    
    def test_south_left(self):
        self.assertEqual(1, change_face(1j, -1))
    
    def test_east_left(self):
        self.assertEqual(-1j, change_face(1, -1))


class PositionsTestCase(unittest.TestCase):
    def test_r2_l3(self):
        self.assertEqual((1, 2, 2 - 1j, 2 - 2j, 2 - 3j), 
                         positions(('R2', 'L3')))

    def test_r2_r2_r2(self):
        self.assertEqual((1, 2, 2 + 1j, 2 + 2j, 1 + 2j, 2j), 
                         positions(('R2', 'R2', 'R2')))


class DetermineDistanceTestCase(unittest.TestCase):
    def test_r2_l3(self):
        self.assertEqual(5, determine_distance(positions(('R2', 'L3'))[-1]))

    def test_r2_r2_r2(self):
        self.assertEqual(2,
                         determine_distance(positions(('R2', 'R2', 'R2'))[-1]))

    def test_r5_l5_r5_r3(self):
        self.assertEqual(12, 
                         determine_distance(
                             positions(('R5', 'L5', 'R5', 'R3'))[-1]))


class FirstRevisitedLocationTestCase(unittest.TestCase):
    def test_r2_r2_r2_r2_r2(self):
        self.assertEqual(1, first_revisited_location(('R2',) * 5))

    def test_r8_r4_r4_r8(self):
        self.assertEqual(4, first_revisited_location(('R8', 'R4', 'R4', 'R8')))


class SolveTestCase(unittest.TestCase):
    def test_r2_l3(self):
        from io import StringIO
        self.assertEqual(5, solve(StringIO('R2, L3'))[0])

    def test_r2_r2_r2_r2_r2(self):
        from io import StringIO
        self.assertEqual((2, 1), solve(StringIO('R2, R2, R2, R2, R2')))


if __name__ == '__main__':
    unittest.main()

