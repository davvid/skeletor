import unittest

from skeletor.cli.menu import Menu, confirm


class MenuInteraction(object):

    def __init__(self, inputs):
        self.inputs = inputs
        self.idx = -1
        self.calls = []

    def get(self, prompt):
        self.idx += 1
        return self.inputs[self.idx]

    def func_a(self):
        self.calls.append('func_a')

    def func_b(self):
        self.calls.append('func_b')


class NullLogger(object):

    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def error(self, msg):
        pass

    def warning(self, msg):
        pass


class MenuTestCase(unittest.TestCase):

    def test_menu_interaction(self):

        mi = MenuInteraction(['a', 'b', 'b', 'a', 'q'])
        menu = Menu('test',
                    logger=NullLogger(),
                    get_input=mi.get)
        menu.present((('a', ('a desscription', mi.func_a)),
                      ('b', ('b desscription', mi.func_b)),
                      ('q', ('quit', Menu.QUIT))))
        self.assertEqual(mi.calls, ['func_a', 'func_b', 'func_b', 'func_a'])

    def test_menu_interaction_case_sensitive(self):

        mi = MenuInteraction(['A', 'B', 'b', 'a', 'q'])
        menu = Menu('test',
                    get_input=mi.get,
                    logger=NullLogger(),
                    case_sensitive=True)
        menu.present((('a', ('a desscription', mi.func_a)),
                      ('b', ('b desscription', mi.func_b)),
                      ('q', ('quit', Menu.QUIT))))
        self.assertEqual(mi.calls, ['func_b', 'func_a'])

    def test_confirm_empty(self):
        mi = MenuInteraction([''])
        result = confirm('', get_input=mi.get)
        self.assertTrue(result is True)

    def test_confirm_empty_false(self):
        mi = MenuInteraction([''])
        expect = 'ok'
        actual = confirm('', default='ok', get_input=mi.get)
        self.assertEqual(expect, actual)

    def test_confirm_bad_empty(self):
        mi = MenuInteraction(['x', ''])
        expect = 'ok'
        actual = confirm('', default='ok', get_input=mi.get)
        self.assertEqual(expect, actual)

    def test_confirm_no(self):
        mi = MenuInteraction(['x', '', 'xxx', 'n'])
        actual = confirm('', empty_chooses=False, get_input=mi.get)
        self.assertTrue(actual is False)

    def test_confirm_yes(self):
        mi = MenuInteraction(['x', '', 'xxx', 'yes'])
        actual = confirm('', empty_chooses=False, get_input=mi.get)
        self.assertTrue(actual is True)


if __name__ == '__main__':
    unittest.main()
