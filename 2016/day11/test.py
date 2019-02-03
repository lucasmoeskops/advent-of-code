import unittest
from io import StringIO
from .main import solve


class SolveTestCase(unittest.TestCase):
    def test(self):
        puzzle_input = \
            StringIO(
                'The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.\n'
                'The second floor contains a hydrogen generator.\n'
                'The third floor contains a lithium generator.\n'
                'The fourth floor contains nothing relevant.')
        self.assertEqual(11, solve(puzzle_input)[0])


if __name__ == '__main__':
    unittest.main()
