from genshibasic.parser import Parser
from genshibasic.lexer import Lexer
import unittest


class ParserTestSuite(unittest.TestCase):

    def test_ABS(self):
        (symbols, data, out) = self.__parse('1 LET X = ABS(4)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(4, symbols['X'])

    def test_AND(self):
        (symbols, data, out) = self.__parse('1 LET X = 1=1 AND 1<>2')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertTrue(symbols['X'])

    def test_ASC(self):
        (symbols, data, out) = self.__parse('1 LET X = ASC("X")')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(88, symbols['X'])

    def test_ATN(self):
        (symbols, data, out) = self.__parse('1 LET X = ATN(3.14)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(1.262, round(symbols['X'], 3))

    def test_CHR(self):
        (symbols, data, out) = self.__parse('1 LET X = CHR(88)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual('X', symbols['X'])

    def test_COS(self):
        (symbols, data, out) = self.__parse('1 LET X = COS(3.14)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(-1.0, round(symbols['X'], 3))

    def test_DATA(self):
        (symbols, data, out) = self.__parse('1 DATA 1, 2, 3, 4, 5')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 5)
        self.assertEqual(len(out), 0)
        self.assertEqual([1, 2, 3, 4, 5], data)

    def test_DIM(self):
        (symbols, data, out) = self.__parse('1 DIM A(3)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('@A', symbols.keys())
        self.assertEqual([0, 0, 0], symbols['@A'])

    def test_END(self):
        (symbols, data, out) = self.__parse('1 END')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)

    def test_EXP(self):
        (symbols, data, out) = self.__parse('1 LET X = EXP(8)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(2980.958, round(symbols['X'], 3))

    def test_INT(self):
        (symbols, data, out) = self.__parse('1 LET X = INT(4.2)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(4, symbols['X'])

    def test_LEN(self):
        (symbols, data, out) = self.__parse('1 LET X = LEN("WASD")')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(4, symbols['X'])

    def test_LET(self):
        (symbols, data, out) = self.__parse('10 LET X=3+4 * 6/2')
        self.assertIn('X', symbols)
        self.assertEqual(symbols['X'], 15.0)
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)

    def test_LOG(self):
        (symbols, data, out) = self.__parse('1 LET X = LOG(4.2)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(1.435, round(symbols['X'], 3))

    def test_NOT(self):
        (symbols, data, out) = self.__parse('1 LET X = NOT 0')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertTrue(symbols['X'])

    def test_OR(self):
        (symbols, data, out) = self.__parse('1 LET X = 1 OR 0')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertTrue(symbols['X'])

    def test_PRINT(self):
        (symbols, data, out) = self.__parse('5 PRINT "HELLO"; " WORLD"')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0], 'HELLO WORLD')

    def test_REM(self):
        (symbols, data, out) = self.__parse('1 REM I AM A COMMENT')
        self.assertEqual(len(symbols.keys()), 0)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)

    def test_RND(self):
        (symbols, data, out) = self.__parse('1 LET X = RND(5)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertLessEqual(symbols['X'], 5)

    def test_SGN(self):
        (symbols, data, out) = self.__parse('1 LET X = SGN(3)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(1, symbols['X'])

    def test_SIN(self):
        (symbols, data, out) = self.__parse('1 LET X = SIN(3.14)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(0.00159, round(symbols['X'], 5))

    def test_SPC(self):
        (symbols, data, out) = self.__parse('1 LET X = SPC(3)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual('   ', symbols['X'])

    def test_SQR(self):
        (symbols, data, out) = self.__parse('1 LET X = SQR(100)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(10, symbols['X'])

    def test_STR(self):
        (symbols, data, out) = self.__parse('1 LET X = STR(50)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual('50', symbols['X'])

    def test_TAN(self):
        (symbols, data, out) = self.__parse('1 LET X = TAN(3.14)')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertEqual(-0.00159, round(symbols['X'], 5))

    def test_XOR(self):
        (symbols, data, out) = self.__parse('1 LET X = 1 XOR 1')
        self.assertEqual(len(symbols.keys()), 1)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(out), 0)
        self.assertIn('X', symbols.keys())
        self.assertFalse(symbols['X'])

    def __parse(self, src, debug_print=False):
        p = Parser()
        tokens = Lexer().lex(src)
        p.parse(tokens[1:], tokens[0])
        return (p.peek_symbols(), p.peek_data(), p.peek_output())


if __name__ == '__main__':
    unittest.main()
