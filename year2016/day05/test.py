import unittest
from program import calculate_password, solve


class CalculateHashTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual('18f47a30', calculate_password('abc'))


class Solve(unittest.TestCase):
    def test(self):
        self.assertEqual('18f47a30', solve('abc')[0])


if __name__ == '__main__':
    unittest.main()

