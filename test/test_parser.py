from genshibasic.parser import Parser
from genshibasic.lexer import Lexer
import unittest


class ParserTestSuite(unittest.TestCase):

    def test_ABS(self):
        pass
        # (symbols, data, out) = self.__parse('1 LET X = ABS(4)')
        # self.assertEqual(len(symbols.keys()), 0)
        # self.assertEqual(len(data), 0)
        # self.assertEqual(len(out), 0)

    def test_AND(self):
        pass

    def test_ASC(self):
        pass

    def test_ATN(self):
        pass

    def test_CHR(self):
        pass

    def test_COS(self):
        pass

    def test_DATA(self):
        pass

    def test_DIM(self):
        pass

    def test_END(self):
        pass

    def test_EXP(self):
        pass

    def test_FOR(self):
        pass

    def test_GOSUB(self):
        pass

    def test_GOTO(self):
        pass

    def test_IF(self):
        pass

    def test_INPUT(self):
        pass

    def test_INT(self):
        pass

    def test_LEFT(self):
        pass

    def test_LEN(self):
        pass

    def test_LET(self):
        (symbols, data, out) = self.__parse('10 LET X=3+4 * 6/2')
        self.assertTrue('X' in symbols)
        self.assertEqual(symbols['X'], 15.0)
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)

    def test_LOG(self):
        pass

    def test_MID(self):
        pass

    def test_NEXT(self):
        pass

    def test_NOT(self):
        pass

    def test_ON(self):
        pass

    def test_OR(self):
        pass

    def test_PRINT(self):
        (symbols, data, out) = self.__parse('5 PRINT "HELLO"; " WORLD"')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0], 'HELLO WORLD')

    def test_READ(self):
        pass

    def test_REM(self):
        (symbols, data, out) = self.__parse('1 REM I AM A COMMENT')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)

    def test_RETURN(self):
        pass

    def test_RIGHT(self):
        pass

    def test_RND(self):
        pass

    def test_SGN(self):
        pass

    def test_SIN(self):
        pass

    def test_SPC(self):
        pass

    def test_SQR(self):
        pass

    def test_STEP(self):
        pass

    def test_STR(self):
        pass

    def test_TAN(self):
        pass

    def test_THEN(self):
        pass

    def test_TO(self):
        pass

    def test_XOR(self):
        pass

    def __parse(self, src, debug_print=False):
        p = Parser()
        tokens = Lexer().lex(src)
        p.parse(tokens[1:], tokens[0])
        return (p.peek_symbols(), p.peek_data(), p.peek_output())


if __name__ == '__main__':
    unittest.main()
