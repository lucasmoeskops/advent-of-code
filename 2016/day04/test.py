import unittest
from program import decipher, is_valid_room, parse_room, solve


class ParseRoomTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual(('aaaaa-bbb-z-y-x', 123, 'abxyz'),
                         parse_room('aaaaa-bbb-z-y-x-123[abxyz]'))


class IsValidRoomTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual(True, is_valid_room('aaaaa-bbb-z-y-x', 'abxyz'))
        self.assertEqual(True, is_valid_room('a-b-c-d-e-f-g-h', 'abcde'))
        self.assertEqual(True, is_valid_room('not-a-real-room', 'oarel'))
        self.assertEqual(False, is_valid_room('totally-real-room', 'decoy'))


class DecipherTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual('very encrypted name', 
                         decipher('qzmt-zixmtkozy-ivhz', 343))


class SolveTestCase(unittest.TestCase):
    def test(self):
        from io import StringIO
        self.assertEqual(5, solve(StringIO('zzzxxyyab-2[zxyab]\n'\
                                           'abcdefhhi-4[abcde]\n'\
                                           'abcdefghi-3[abcde]\n'))[0])



if __name__ == '__main__':
    unittest.main()

