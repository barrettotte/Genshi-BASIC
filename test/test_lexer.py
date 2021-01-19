from genshibasic.lexer import Lexer
import unittest

class LexerTestSuite(unittest.TestCase):

    def test_hello(self):
        tokens = self.__lex('hello')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].pos, (1,5))
        self.assertEqual(tokens[0].tok_type, 3)
        self.assertEqual(tokens[0].lexeme, 'HELLO')
    
    def test_vardeclare(self):
        tokens = self.__lex('10 LET A=3+4*6%2', True)
        

    def __lex(self, src, debug_print=False):
        tokens = Lexer().lex(src)
        if debug_print:
            for t in tokens: 
                print(t)
        return tokens


if __name__ == '__main__': unittest.main()