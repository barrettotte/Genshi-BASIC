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
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)
    
    def test_grouping(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = ((x / 5))')
        expected = [
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex1(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = X * 4 + (3 / 5)')
        expected = [
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex2(self):
        res = self.genshiBas.parse('10 DEF FN FTEST (X) = ((X * (3 / 5)))')
        expected = [
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "IDENTIFIER", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary1(self):
        res = self.genshiBas.parse('10 DEF FN FTEST(X,Y,Z)=-(x+y)')
        expected = [
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", "IDENTIFIER",
            "COMMA", "IDENTIFIER", "COMMA", "IDENTIFIER", "RIGHT_PAREN",
            "EQUALS", "UNARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary2(self):
        res = self.genshiBas.parse('10 DEF FN FTEST(X) = -(x)--(-(-y--z))')
        expected = [
            "FUNC-DEF", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", "IDENTIFIER",
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

if __name__ == "__main__": unittest.main()