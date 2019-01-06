import unittest
from program import find_position, is_actual_layout_position, \
        position_to_button, position_to_actual_button, solve


class FindPositionTestCase(unittest.TestCase):
    def test_U_1_1(self):
        self.assertEqual(1, find_position('U', 1 + 1j))

    def test_UU_1_1(self):
        self.assertEqual(1, find_position('UU', 1 + 1j))

    def test_DD_1_1(self):
        self.assertEqual(1 + 2j, find_position('DD', 1 + 1j))

    def test_LL_1_1(self):
        self.assertEqual(1j, find_position('LL', 1 + 1j))

    def test_RR_1_1(self):
        self.assertEqual(2 + 1j, find_position('RR', 1 + 1j))

    def test_LD_1_1(self):
        self.assertEqual(2j, find_position('LD', 1 + 1j))


class IsActualLayoutPositionTestCase(unittest.TestCase):
    def test_0_2(self):
        self.assertEqual(True, is_actual_layout_position(2j))

    def test_1_2(self):
        self.assertEqual(False, is_actual_layout_position(1 + 2j))


class PositionToActualButtonTestCase(unittest.TestCase):
    def test_m2(self):
        self.assertEqual('5', position_to_actual_button(-2))

    def test_0(self):
        self.assertEqual('7', position_to_actual_button(0))


class PositionToButtonTestCase(unittest.TestCase):
    def test_1_1(self):
        self.assertEqual('5', position_to_button(1 + 1j))


class TestSolve(unittest.TestCase):
    def test_1985(self):
        from io import StringIO
        self.assertEqual('1985', solve(StringIO('ULL\nRRDDD\nLURDL\nUUUUD'))[0])

    def test_5db3(self):
        from io import StringIO
        self.assertEqual('5DB3', solve(StringIO('ULL\nRRDDD\nLURDL\nUUUUD'))[1])


if __name__ == '__main__':
    unittest.main()

