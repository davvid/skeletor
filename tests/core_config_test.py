import os
import unittest

from skeletor.core import config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.srcdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.examples = os.path.join(self.srcdir, 'examples')

    def test_simple(self):
        path = os.path.join(self.examples, 'overrides.json')
        values = config.JSONConfig(path)
        self.assertEqual(values['question'], 'what is your quest?')

    def test_includes(self):
        path = os.path.join(self.examples, 'example.json')
        values = config.JSONConfig(path)
        self.assertEqual(values['example'], 42)
        self.assertEqual(values['key'], 'overridden by overrides.json')
        self.assertEqual(values['question'], 'what is your quest?')
        self.assertEqual(values['answer'], 'to find the grail')


if __name__ == '__main__':
    unittest.main()
