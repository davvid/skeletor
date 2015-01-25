import os
import unittest

from skeletor.util import config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(os.path.abspath(__file__))

    def test_simple(self):
        path = os.path.join(self.testdir, 'overrides.json')
        values = config.JSONConfig(path)
        self.assertEqual(values['question'], 'what is your quest?')

    def test_includes(self):
        path = os.path.join(self.testdir, 'example.json')
        values = config.JSONConfig(path)
        self.assertEqual(values['example'], 42)
        self.assertEqual(values['key'], 'overridden by overrides.json')
        self.assertEqual(values['question'], 'what is your quest?')
        self.assertEqual(values['answer'], 'to find the grail')


if __name__ == '__main__':
    unittest.main()
