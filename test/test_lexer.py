from genshibasic.lexer import Lexer
import unittest

class LexerTestSuite(unittest.TestCase):

    def test_hello(self):
        tokens = self.__lex('hello')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].pos, (1,5))
        self.assertEqual(tokens[0].tok_type, 3)
        self.assertEqual(tokens[0].lexeme, 'HELLO')
    
    def test_general(self):
        actual = self.__lex('10 LET A=3+4 * 6%2')
        expected = [
            { 'pos': (1,2),   'tok_type': 1,  'lexeme': '10'  },
            { 'pos': (4,6),   'tok_type': 28, 'lexeme': 'LET' },
            { 'pos': (8,8),   'tok_type': 3,  'lexeme': 'A'   },
            { 'pos': (9,9),   'tok_type': 80, 'lexeme': '='   },
            { 'pos': (10,10), 'tok_type': 1,  'lexeme': '3'   },
            { 'pos': (11,11), 'tok_type': 70, 'lexeme': '+'   },
            { 'pos': (12,12), 'tok_type': 1,  'lexeme': '4'   },
            { 'pos': (14,14), 'tok_type': 72, 'lexeme': '*'   },
            { 'pos': (16,16), 'tok_type': 1,  'lexeme': '6'   },
            { 'pos': (17,17), 'tok_type': 74, 'lexeme': '%'   },
            { 'pos': (18,18), 'tok_type': 1,  'lexeme': '2'   },
        ]
        self.__match(actual, expected)
        
    
    def test_string(self):
        actual = self.__lex('5 PRINT "HELLO"; " WORLD"')
        expected = [
            { 'pos': (1,1),   'tok_type': 1,  'lexeme': '5'        },
            { 'pos': (3,7),   'tok_type': 38, 'lexeme': 'PRINT'    },
            { 'pos': (9,15),  'tok_type': 0,  'lexeme': '"HELLO"'  },
            { 'pos': (16,16), 'tok_type': 85, 'lexeme': ';'        },
            { 'pos': (18,25), 'tok_type': 0,  'lexeme': '" WORLD"' },
        ]
        self.__match(actual, expected)

    def test_float(self):
        actual = self.__lex('250 LET PI= 3.14')
        expected = [
            { 'pos': (1,3),   'tok_type': 1,  'lexeme': '250'  },
            { 'pos': (5,7),   'tok_type': 28, 'lexeme': 'LET'  },
            { 'pos': (9,10),  'tok_type': 3,  'lexeme': 'PI'   },
            { 'pos': (11,11), 'tok_type': 80, 'lexeme': '='    },
            { 'pos': (13,16), 'tok_type': 2,  'lexeme': '3.14' },
        ]
        self.__match(actual, expected)
    
    def test_sym2(self):
        actual = self.__lex('100 LET X = 4 <> 5')
        expected = [
            { 'pos': (1,3),   'tok_type': 1,  'lexeme': '100' },
            { 'pos': (5,7),   'tok_type': 28, 'lexeme': 'LET' },
            { 'pos': (9,9),   'tok_type': 3,  'lexeme': 'X'   },
            { 'pos': (11,11), 'tok_type': 80, 'lexeme': '='   },
            { 'pos': (13,13), 'tok_type': 1,  'lexeme': '4'   },
            { 'pos': (15,16), 'tok_type': 79, 'lexeme': '<>'  },
            { 'pos': (18,18), 'tok_type': 1,  'lexeme': '5'   },
        ]

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
            self.assertEqual(actual[i].tok_type, expected[i]['tok_type'])
            self.assertEqual(actual[i].lexeme, expected[i]['lexeme'])


if __name__ == '__main__': unittest.main()