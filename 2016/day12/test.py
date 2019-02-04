import unittest
from io import StringIO
from .main import solve


class SolveTestCase(unittest.TestCase):
    def test(self):
        puzzle_input = (
            StringIO(
                'cpy 41 a\n'
                'inc a\n'
                'inc a\n'
                'dec a\n'
                'jnz a 2\n'
                'dec a\n'))
        self.assertEqual(42, solve(puzzle_input)[0])


if __name__ == '__main__':
    unittest.main()
