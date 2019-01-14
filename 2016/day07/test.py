import unittest
from program import get_abas, has_abba, is_aba, is_abba, reverse_aba, solve, \
        supports_ssl, supports_tls


class IsAbbaTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(is_abba('abba'))
        self.assertTrue(is_abba('baab'))
        self.assertFalse(is_abba('aabb'))
        self.assertFalse(is_abba('abca'))
        self.assertFalse(is_abba('abbc'))
        self.assertFalse(is_abba('aaaa'))


class IsAbaTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(is_aba('aba'))
        self.assertTrue(is_aba('bab'))
        self.assertFalse(is_aba('aab'))
        self.assertFalse(is_aba('abb'))
        self.assertFalse(is_aba('aaa'))


class HasAbbaTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(has_abba('lalaabba'))
        self.assertFalse(has_abba('lalalala'))


class GetAbasTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual(('aba',), tuple(get_abas('abas')))
        self.assertEqual(('aba', 'bab'), tuple(get_abas('abab')))


class ReverseAbaTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual('bab', reverse_aba('aba'))


class SupportsTLSTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(supports_tls('abba[mnop]qrst'))
        self.assertFalse(supports_tls('abcd[bddb]xyyx'))
        self.assertFalse(supports_tls('aaaa[qwer]tyui'))
        self.assertTrue(supports_tls('ioxxoj[asdfgh]zxcvbn'))


class SupportsSSLTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(supports_ssl('aba[bab]xyz'))
        self.assertFalse(supports_ssl('xyx[xyx]xyx'))
        self.assertTrue(supports_ssl('aaa[kek]eke'))
        self.assertTrue(supports_ssl('zazbz[bzb]cdb'))


if __name__ == '__main__':
    unittest.main()

