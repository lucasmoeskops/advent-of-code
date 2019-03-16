import unittest

from year2016.day23.main import parse_program
from .main import HQComputer


class HQComputerTestCase(unittest.TestCase):
    def test(self):
        data = 'cpy 2 a\n'\
               'tgl a\n'\
               'tgl a\n'\
               'tgl a\n'\
               'cpy 1 a\n'\
               'dec a\n'\
               'dec a\n'
        program = parse_program(data.strip().split('\n'))
        computer = HQComputer()
        computer.execute(program)
        self.assertEqual(3, computer.registers['a'])


if __name__ == '__main__':
    unittest.main()

