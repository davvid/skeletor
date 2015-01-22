import unittest

from skeletor.core import util


class UtilTestCase(unittest.TestCase):

    def test_deep_update_one_level_deep(self):
        """Ensure that deep dictionary values are preserved"""

        a = {'foo': {'bar': True, 'baz': True},
             'fez': True}
        b = {'foo': {'baz': False}}
        util.deep_update(a, b)

        self.assertTrue('foo' in a)
        self.assertTrue(a['fez'])
        self.assertTrue(a['foo']['bar'])
        self.assertFalse(a['foo']['baz'])

    def test_deep_update_two_levels_deep(self):
        """Ensure that deeply deep dictionary values are preserved"""

        a = {
            'foo': {
                'bar': True,
                'baz': {
                    'answer': 'unknown',
                },
            },
            'fez': True,
        }

        b = {
            'foo': {
                'baz': {
                    'answer': 42,
                },
            },
            'fez': False,
            'ringo': True,
        }

        util.deep_update(a, b)

        self.assertTrue('foo' in a)
        self.assertTrue('fez' in a)
        self.assertTrue('ringo' in a)

        self.assertFalse(a['fez'])
        self.assertTrue(a['ringo'])

        self.assertEqual(a['foo']['baz']['answer'], 42)


if __name__ == '__main__':
    unittest.main()
