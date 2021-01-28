from genshibasic.parser import Parser
from genshibasic.lexer import Lexer
import unittest


class ParserTestSuite(unittest.TestCase):

    def test_var_declaration(self):
        actual = self.__parse('10 LET A=3+4 * 6%2')

    def __parse(self, src, debug_print=False):
        tokens = Lexer().lex(src)
        # Parser().parse(tokens, 0)
        # TODO:

    def __match(self, actual, expected):
        self.assertEqual(len(expected), len(actual))

        for i in range(len(expected)):
            self.assertEqual(actual[i].pos, expected[i]['pos'])
            self.assertEqual(actual[i].tok_type, expected[i]['tok_type'])
            self.assertEqual(actual[i].lexeme, expected[i]['lexeme'])


if __name__ == '__main__':
    unittest.main()
