import unittest, GenshiBASIC, warnings

class Test_Parser(unittest.TestCase):

    def setUp(self):
        self.genshiBas = GenshiBASIC.New()
        print("Running test: " + str(self._testMethodName))
        warnings.filterwarnings("ignore") # suppress warning output
    

# ==== Expressions  
    def test_binary(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = X * 4+3')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)
    
    def test_grouping(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = ((x / 5))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex1(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = X * 4 + (3 / 5)')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex2(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = ((X * (3 / 5)))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary1(self):
        res = self.genshiBas.parse('10 DEF FN FTEST(X,Y,Z)=-(x+y)')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", "IDENTIFIER",
            "COMMA", "IDENTIFIER", "COMMA", "IDENTIFIER", "RIGHT_PAREN",
            "EQUALS", "UNARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary2(self):
        res = self.genshiBas.parse('10 DEF FN FTEST(X) = -(x)--(-(-y--z))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", "IDENTIFIER",
            "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)
    
    def test_bulk_expressions(self):
        self.genshiBas.parse('10 DEF FN FTEST (X) = X * 4 + 3')
        self.genshiBas.parse('10 DEF FN FTEST (X) = ((X / 5))')
        self.genshiBas.parse('10 DEF FN FTEST (X) = X * 4 + (3 / 5)')
        self.genshiBas.parse('10 DEF FN FTEST (X) = (((X * 4 + 1)))')
        self.genshiBas.parse('10 DEF FN FTEST (X) = ((X * (3 / 5)))')
        self.genshiBas.parse('10 DEF FN FTEST(X,Y) = X-Y')
        self.genshiBas.parse('10 DEF FN FTEST(X,Y) = -X - Y')
        self.genshiBas.parse('10 DEF FN FTEST(X,Y,Z)=-(x+y)')
        self.genshiBas.parse('10 DEF FN FTEST(X)= -(-(x+y))')
        self.genshiBas.parse('10 DEF FN FTEST(X) = -(X + -Y / 5)')
        self.genshiBas.parse('10 DEF FN FTEST(X) = -(x)--(-(-y--z))')


# ==== Declarations  

    # TODO: Make more robust tests based off these
    def test_bulk_declarations(self):
        self.genshiBas.parse('10 DIM A(1,2)')
        self.genshiBas.parse('10 DIM A(X+1,2+y)')
        self.genshiBas.parse('10 DIM A((X+3)-1,X)')
        self.genshiBas.parse('10 DIM A(1)')
        self.genshiBas.parse('10 LET A = 45')
        self.genshiBas.parse('10 LET X! = (3 * Y + (-4))')

    def test_dec_for(self):
        prog = "\n".join([
          "10 FOR I = 1.0 TO 10 STEP 1",
          "20 LET X=X+2",
          "30 ENDFOR"
        ])
        self.genshiBas.parse(prog)


if __name__ == "__main__": unittest.main()