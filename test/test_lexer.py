from genshibasic.genshi import Genshi
from genshibasic.lexer import Lexer
import unittest


class LexerTestSuite(unittest.TestCase):

    def test_hello(self):
        tokens = self.__lex('hello')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].pos, (1, 5))
        self.assertEqual(tokens[0].kind, 3)
        self.assertEqual(tokens[0].lexeme, 'HELLO')

    def test_general(self):
        actual = self.__lex('10 LET X=3+4 * 6/2')
        expected = [
            {'pos': (1, 2), 'kind': Genshi.TT_UINT, 'lexeme': '10'},
            {'pos': (4, 6), 'kind': Genshi.KW_LET, 'lexeme': 'LET'},
            {'pos': (8, 8), 'kind': Genshi.TT_IDENTIFIER, 'lexeme': 'X'},
            {'pos': (9, 9), 'kind': Genshi.SYM_EQ, 'lexeme': '='},
            {'pos': (10, 10), 'kind': Genshi.TT_UINT, 'lexeme': '3'},
            {'pos': (11, 11), 'kind': Genshi.SYM_ADD, 'lexeme': '+'},
            {'pos': (12, 12), 'kind': Genshi.TT_UINT, 'lexeme': '4'},
            {'pos': (14, 14), 'kind': Genshi.SYM_MUL, 'lexeme': '*'},
            {'pos': (16, 16), 'kind': Genshi.TT_UINT, 'lexeme': '6'},
            {'pos': (17, 17), 'kind': Genshi.SYM_DIV, 'lexeme': '/'},
            {'pos': (18, 18), 'kind': Genshi.TT_UINT, 'lexeme': '2'},
        ]
        self.__match(actual, expected)

    def test_string(self):
        actual = self.__lex('5 PRINT "HELLO"; " WORLD"')
        expected = [
            {'pos': (1, 1), 'kind': Genshi.TT_UINT, 'lexeme': '5'},
            {'pos': (3, 7), 'kind': Genshi.KW_PRINT, 'lexeme': 'PRINT'},
            {'pos': (9, 15), 'kind': Genshi.TT_STRING, 'lexeme': 'HELLO'},
            {'pos': (16, 16), 'kind': Genshi.SYM_SEMICOLON, 'lexeme': ';'},
            {'pos': (18, 25), 'kind': Genshi.TT_STRING, 'lexeme': ' WORLD'},
        ]
        self.__match(actual, expected)

    def test_float(self):
        actual = self.__lex('250 LET PI= 3.14')
        expected = [
            {'pos': (1, 3), 'kind': Genshi.TT_UINT, 'lexeme': '250'},
            {'pos': (5, 7), 'kind': Genshi.KW_LET, 'lexeme': 'LET'},
            {'pos': (9, 10), 'kind': Genshi.TT_IDENTIFIER, 'lexeme': 'PI'},
            {'pos': (11, 11), 'kind': Genshi.SYM_EQ, 'lexeme': '='},
            {'pos': (13,  16), 'kind': Genshi.TT_UFLOAT, 'lexeme': '3.14'},
        ]
        self.__match(actual, expected)

    def test_sym2(self):
        actual = self.__lex('100 LET X = 4 <> 5')
        expected = [
            {'pos': (1, 3), 'kind': Genshi.TT_UINT, 'lexeme': '100'},
            {'pos': (5, 7), 'kind': Genshi.KW_LET, 'lexeme': 'LET'},
            {'pos': (9, 9), 'kind': Genshi.TT_IDENTIFIER, 'lexeme': 'X'},
            {'pos': (11, 11), 'kind': Genshi.SYM_EQ, 'lexeme': '='},
            {'pos': (13, 13), 'kind': Genshi.TT_UINT, 'lexeme': '4'},
            {'pos': (15, 16), 'kind': Genshi.SYM_NE, 'lexeme': '<>'},
            {'pos': (18, 18), 'kind': Genshi.TT_UINT, 'lexeme': '5'},
        ]
        self.__match(actual, expected)

    def __lex(self, src, debug_print=False):
        tokens = Lexer().lex(src)
        if debug_print:
            for t in tokens:
                print(t)
        return tokens

    def __match(self, actual, expected):
        self.assertEqual(len(expected), len(actual))

        for i in range(len(expected)):
            self.assertEqual(actual[i].pos, expected[i]['pos'])
            self.assertEqual(actual[i].kind, expected[i]['kind'])
            self.assertEqual(actual[i].lexeme, expected[i]['lexeme'])


if __name__ == '__main__':
    unittest.main()
