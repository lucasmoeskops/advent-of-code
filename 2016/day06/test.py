import unittest
from program import LEAST_COMMON, decode_message, solve


class DecodeMessageTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual('good',
                         decode_message(('geot', 'goad', 'nood')))
        self.assertEqual('neat',
                         decode_message(('geot', 'goad', 'nood'), LEAST_COMMON))


if __name__ == '__main__':
    unittest.main()

