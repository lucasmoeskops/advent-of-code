import unittest
from .program import Screen, execute_operations, solve


class ScreenTestCase(unittest.TestCase):
    def test(self):
        screen = Screen(7, 3)
        ON = Screen.ON
        OFF = Screen.OFF
        self.assertEqual((OFF,) * 21, screen.state)
        screen.rect(3, 2)
        self.assertEqual((ON,) * 3 + (OFF,) * 4 + (ON,) * 3 + (OFF,) * 11,
                         screen.state)
        screen.rotate_column_x(1, 1)
        self.assertEqual((ON, OFF, ON) + (OFF,) * 4 + (ON,) * 3 + (OFF,) * 5 + \
                         (ON,) + (OFF,) * 5, screen.state)
        screen.rotate_row_y(0, 4)
        self.assertEqual((OFF,) * 4 + (ON, OFF) + (ON,) * 4 + (OFF,) * 5 + \
                         (ON,) + (OFF,) * 5, screen.state)
        screen.rotate_column_x(1, 1)
        self.assertEqual((OFF, ON, OFF, OFF, ON, OFF, ON, ON, OFF, ON) + \
                         (OFF,) * 5 + (ON,) + (OFF,) * 5, screen.state)
        self.assertEqual(6, screen.lit_pixels)


class ExecuteOperationsTestCase(unittest.TestCase):
    def test(self):
        screen = Screen(7, 3)
        ON = Screen.ON
        OFF = Screen.OFF
        operations = (
            'rect 3x2',
            'rotate column x=1 by 1',
            'rotate row y=0 by 4',
            'rotate column x=1 by 1',
        )
        execute_operations(screen, operations)
        self.assertEqual((OFF, ON, OFF, OFF, ON, OFF, ON, ON, OFF, ON) + \
                         (OFF,) * 5 + (ON,) + (OFF,) * 5, screen.state)


class SolveTestCase(unittest.TestCase):
    def test_part1(self):
        from io import StringIO
        puzzle_input = StringIO('rect 3x2\nrotate column x=1 by 1\n'
                                'rotate row y=0 by 4\nrotate column x=1 by 1')
        self.assertEqual(6, solve(puzzle_input)[0])


if __name__ == '__main__':
    unittest.main()
