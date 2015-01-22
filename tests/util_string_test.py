import unittest

from skeletor.util import string


class StringTestCase(unittest.TestCase):

    def test_expandvars_basic(self):
        expect = 'foobarbaz'
        actual = string.expandvars('$foo$bar$baz',
                                   environ=dict(foo='foo',
                                                bar='bar',
                                                baz='baz'))
        self.assertEqual(expect, actual)

    def test_expandvars_curly_braces(self):
        expect = 'foobarbaz'
        actual = string.expandvars('${foo}$bar${baz}',
                                   environ=dict(foo='foo',
                                                bar='bar',
                                                baz='baz'))
        self.assertEqual(expect, actual)

    def test_expandvars_empty_env(self):
        expect = '$foo'
        actual = string.expandvars('$foo', environ={})
        self.assertEqual(expect, actual)

    def test_expandvars_empty_value(self):
        expect = ''
        actual = string.expandvars('$foo', environ={'foo': ''})
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
