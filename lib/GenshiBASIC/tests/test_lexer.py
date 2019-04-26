import unittest, GenshiBASIC, warnings

class Test_Lexer(unittest.TestCase):

    def setUp(self):
        self.genshiBas = GenshiBASIC.New()
        self.test_program = self.get_test_program()
        print("   Running test: " + str(self._testMethodName))
        warnings.filterwarnings("ignore")

    def print_tokens(self, tokens):
        for line_num, token_list in tokens.items():
            print(line_num)
            for t in token_list: print("   " + str(t))

    def get_test_program(self):
        pgm = [
            '5  PRINT "REPLACE ME"',
            '10 FOR NI = 3 TO 1 STEP -1',
            '20   PRINT NI',
            '30 ENDFOR',
            '40 IF X > 1 THEN PRINT "HELLO WORLD"',
            '50 DEF FN FTEST(X) = X*3',
            '60 PRINT FN FTEST(4)',
            '70 LET A4 = 2',
            '80 REM I AM A COMMENT',
            '5  PRINT "TESTING..."',
        ]
        return "\n".join(pgm)

    def test_lexemes_HelloWorld(self):
        res = self.genshiBas.make_lexemes('10 PRINT "HELLO WORLD"')
        self.assertTrue(res['10'] == ['PRINT', '"', 'HELLO', 'WORLD', '"'])

    def test_lexemes_Blank(self):
        res = self.genshiBas.make_lexemes('')
        self.assertTrue(len(res) == 0)

    def test_lexemes_NoLineNumber(self):
        res = self.genshiBas.make_lexemes('PRINT "HELLO THERE"')
        self.assertTrue(res['1'] == ['PRINT', '"', 'HELLO', 'THERE', '"'])
    
    def test_tokens_HelloWorld(self):
        res = self.genshiBas.make_tokens('10 PRINT "HELLO WORLD"')
        tokens = res['10']
        self.assertTrue(len(tokens) == 5)
        self.assertTrue(tokens[0].token_type == "NO-PARAM")
        self.assertTrue(tokens[1].token_type == "QUOTATION")
        self.assertTrue(tokens[2].token_type == "LITERAL" and tokens[2].literal == "STRING")
        self.assertTrue(tokens[3].token_type == "LITERAL" and tokens[3].literal == "STRING")
        self.assertTrue(tokens[4].token_type == "QUOTATION")
        
    def test_tokens_Blank(self):
        res = self.genshiBas.make_tokens('')
        self.assertTrue(len(res) == 0)

    def test_tokens_NoLineNumber(self):
        res = self.genshiBas.make_tokens('PRINT "HELLO THERE"')
        tokens = res['1']
        self.assertTrue(len(tokens) == 5)
        self.assertTrue(tokens[0].token_type == "NO-PARAM")
        self.assertTrue(tokens[1].token_type == "QUOTATION")
        self.assertTrue(tokens[2].token_type == "LITERAL" and tokens[2].literal == "STRING")
        self.assertTrue(tokens[3].token_type == "LITERAL" and tokens[3].literal == "STRING")
        self.assertTrue(tokens[4].token_type == "QUOTATION")



if __name__ == "__main__": unittest.main()