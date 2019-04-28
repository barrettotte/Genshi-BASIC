import unittest, GenshiBASIC, warnings

class Test_Lexer(unittest.TestCase):

    def setUp(self):
        self.genshiBas = GenshiBASIC.New()
        self.example_program = self.get_example_program()
        print("   Running test: " + str(self._testMethodName))
        warnings.filterwarnings("ignore") # suppress warning output

    def print_dict_of_lists(self, d): 
        for k, v in d.items():
            print(k)
            for e in v: print("   " + str(e))

    def get_example_program(self):
        return "\n".join([
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
        ])


# ==== Lexemes

    def test_lexemes_HelloWorld(self):
        res = self.genshiBas.make_lexemes('10 PRINT "HELLO WORLD"')
        self.assertTrue(res['10'] == ['PRINT', '"', 'HELLO', 'WORLD', '"'])

    def test_lexemes_Blank(self):
        res = self.genshiBas.make_lexemes('')
        self.assertTrue(len(res) == 0)

    def test_lexemes_NoLineNumber(self):
        with self.assertWarns(SyntaxWarning):
            res = self.genshiBas.make_lexemes('PRINT "HELLO THERE"')
            self.assertTrue(res['1'] == ['PRINT', '"', 'HELLO', 'THERE', '"'])

    def test_lexemes_MaxLineNumber(self):
        with self.assertWarns(SyntaxWarning):
            res = self.genshiBas.make_lexemes('63999 LET X=3\n67000 LET Y=4')
            self.assertTrue(len(res) == 1) # All lines after max are skipped
    
    def test_lexemes_MaxColLength(self):
        with self.assertWarns(SyntaxWarning):
            res = self.genshiBas.make_lexemes('10 PRINT "' + ("A"*50) + '"')
            self.assertTrue(len(res['10']) == 3) # last quotation lexeme was ignored

    def test_lexemes_ExampleProgram(self):
        res = self.genshiBas.make_lexemes(self.example_program)
        expected_lens = [7, 9, 2, 1, 10, 10, 6, 4, 5]
        self.assertTrue(len(res) == len(expected_lens))
        i = 0
        for k,v in res.items():
            self.assertTrue(len(v) == expected_lens[i])
            i += 1

    def test_lexemes_ExampleProgram_Line50(self):
        res = self.genshiBas.make_lexemes(self.example_program)
        expected = ['DEF', 'FN', 'FTEST', '(', 'X', ')', '=', 'X', '*', '3']
        self.assertTrue(len(res['50']) == len(expected))
        for i in range(len(res['50'])):
            self.assertTrue(res['50'][i] == expected[i])
    

# ==== Tokens

    def test_tokens_HelloWorld(self):
        res = self.genshiBas.make_tokens('10 PRINT "HELLO WORLD"')
        tokens = res['10']
        expected = ["NO-PARAM", "QUOTATION", "LITERAL", "LITERAL", "QUOTATION"]
        self.assertTrue(len(tokens) == len(expected))
        for i in range(len(tokens)):
                self.assertTrue(tokens[i].token_type == expected[i])
        self.assertTrue(tokens[2].literal == "STRING")
        self.assertTrue(tokens[3].literal == "STRING")
        
    def test_tokens_Blank(self):
        res = self.genshiBas.make_tokens('')
        self.assertTrue(len(res) == 0)

    def test_tokens_NoLineNumber(self):
        with self.assertWarns(SyntaxWarning):
            res = self.genshiBas.make_tokens('PRINT "HELLO THERE"')
            tokens = res['1']
            expected = ["NO-PARAM", "QUOTATION", "LITERAL", "LITERAL", "QUOTATION"]
            self.assertTrue(len(tokens) == len(expected))
            for i in range(len(tokens)):
                self.assertTrue(tokens[i].token_type == expected[i])
            self.assertTrue(tokens[2].literal == "STRING")
            self.assertTrue(tokens[3].literal == "STRING")
    
    def test_tokens_MissingQuotation(self):
        with self.assertRaises(SyntaxError):
            res = self.genshiBas.make_tokens('10 PRINT "IM MISSING A QUOTE')
    
    def test_tokens_ExampleProgram(self):
        res = self.genshiBas.make_tokens(self.example_program)
        expected_lens = [7, 9, 2, 1, 10, 10, 6, 4, 5]
        self.assertTrue(len(res) == len(expected_lens))
        i = 0
        for k,v in res.items():
            self.assertTrue(len(v) == expected_lens[i])
            i += 1
    
    def test_tokens_ExampleProgram_Line50(self):
        res = self.genshiBas.make_tokens(self.example_program)
        expected = [
            'FUNC-DEF', 'FUNCTION', 'LITERAL', 'LEFT_PAREN', 'LITERAL', 
            'RIGHT_PAREN', 'EQUALS', 'LITERAL', 'BINARY', 'LITERAL'
        ]
        self.assertTrue(len(res['50']) == len(expected))
        for i in range(len(res['50'])):
            self.assertTrue(str(res['50'][i].token_type) == expected[i])


if __name__ == "__main__": unittest.main()