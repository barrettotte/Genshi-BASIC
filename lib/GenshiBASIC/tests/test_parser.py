import unittest, GenshiBASIC, warnings

class Test_Parser(unittest.TestCase):

    def setUp(self):
        self.genshiBasic = GenshiBASIC.New()
        print("Running test: " + str(self._testMethodName))
        warnings.filterwarnings("ignore") # suppress warning output
    

# ==== Expressions  
    def test_binary(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST (X) = X * 4+3')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "PARAMETERS", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)
    
    def test_grouping(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST (X) = ((x / 5))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "PARAMETERS", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex1(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST (X) = X * 4 + (3 / 5)')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "PARAMETERS", "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_complex2(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST (X) = ((X * (3 / 5)))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN",
            "PARAMETERS", "RIGHT_PAREN", "EQUALS", "GROUPING_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary1(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST(X,Y,Z)=-(x+y)')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", 
            "PARAMETERS", "RIGHT_PAREN", "EQUALS", "UNARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)

    def test_unary2(self):
        res = self.genshiBasic.parse('10 DEF FN FTEST(X) = -(x)--(-(-y--z))')
        expected = [
            "FUNC-DEC", "FUNCTION", "IDENTIFIER", "LEFT_PAREN", "PARAMETERS",
            "RIGHT_PAREN", "EQUALS", "BINARY_EXP"
        ]
        line10 = res.children[0]
        for i in range(len(expected)):
            self.assertTrue(expected[i] == line10.children[i].node_type)
    
    def test_bulk_expressions(self):
        self.genshiBasic.parse('10 DEF FN FTEST (X) = X * 4 + 3')
        self.genshiBasic.parse('10 DEF FN FTEST (X) = ((X / 5))')
        self.genshiBasic.parse('10 DEF FN FTEST (X) = X * 4 + (3 / 5)')
        self.genshiBasic.parse('10 DEF FN FTEST (X) = (((X * 4 + 1)))')
        self.genshiBasic.parse('10 DEF FN FTEST (X) = ((X * (3 / 5)))')
        self.genshiBasic.parse('10 DEF FN FTEST(X,Y) = X-Y')
        self.genshiBasic.parse('10 DEF FN FTEST(X,Y) = -X - Y')
        self.genshiBasic.parse('10 DEF FN FTEST(X,Y,Z)=-(x+y)')
        self.genshiBasic.parse('10 DEF FN FTEST(X)= -(-(x+y))')
        self.genshiBasic.parse('10 DEF FN FTEST(X) = -(X + -Y / 5)')
        self.genshiBasic.parse('10 DEF FN FTEST(X) = -(x)--(-(-y--z))')


# ==== Declarations  

    # TODO: Make more robust tests based off these
    def test_bulk_declarations(self):
        self.genshiBasic.parse('10 DIM A(1,2)')
        self.genshiBasic.parse('10 DIM A(X+1,2+y)')
        self.genshiBasic.parse('10 DIM A((X+3)-1,X)')
        self.genshiBasic.parse('10 DIM A(1)')
        self.genshiBasic.parse('10 LET A = 45')
        self.genshiBasic.parse('10 LET X! = (3 * Y + (-4))')

    def test_dec_for(self):
        prog = "\n".join([
          "10 FOR I = 1.0 TO 10 STEP 1",
          "20 LET X=X+2",
          "30 ENDFOR"
        ])
        self.genshiBasic.parse(prog)

    def test_go(self):
        self.genshiBasic.parse("10 GOTO X+4")
        self.genshiBasic.parse("10 GOSUB X*4+(1+y)")

    def test_func(self):
        self.genshiBasic.parse("10 COS(4, 3*(x-1))")
        self.genshiBasic.parse("10 DEF FN F() = X*2")
        self.genshiBasic.parse("10 X=COS(3,3)")
        self.genshiBasic.parse("10 DEF FN A (X,Y) = COS(X) + SIN(Y)")
        self.genshiBasic.parse("10 X = MID(1,2,3+X)")
        self.genshiBasic.parse("20 A(1,4)")
        self.genshiBasic.parse("10 X = HELLO(1,-2,3+-(X-4))")
        self.genshiBasic.parse("10 X = -MYFUNC(X, X*4)")
        self.genshiBasic.parse("10 X = A(B(X), X)")
        self.genshiBasic.parse("10 X = XYZ(X) + 3")
        self.genshiBasic.parse("10 X = 1 + XYZ(A)")
        self.genshiBasic.parse("10 X = A(B(X), X, 1 + C(Y))")
        self.genshiBasic.parse("10 X = A(4) + SIN(Y)")

    def test_if(self):
        self.genshiBasic.parse('10 IF N GT 255 OR N LT 0 THEN X=4+y')
        self.genshiBasic.parse('10 IF N EQ 0 THEN GOTO X+1')
        self.genshiBasic.parse('10 IF N EQ 0 THEN GOTO (X+1)')
        self.genshiBasic.parse('10 IF N EQ 0 THEN GOTO -(X+1)+w')
        self.genshiBasic.parse('10 IF N EQ 0 THEN GOTO SIN(X)+3')
        self.genshiBasic.parse('10 IF N EQ 0 THEN END')
        self.genshiBasic.parse('10 IF N EQ 0 THEN XYZ(1,3+A)')
        self.genshiBasic.parse('10 IF N EQ 0 THEN X = SIN(X)')
        self.genshiBasic.parse('10 IF INT(I/15)/(I/15) EQ 1 THEN PRINT "FIZZBUZZ"')

    def test_string(self):
        self.genshiBasic.parse('10 X="ABC"')
        self.genshiBasic.parse('10 X= ABC("HELLO", "WORLD")')

    def test_print(self):
        self.genshiBasic.parse('10 PRINT "HELLO WORLD"')
        self.genshiBasic.parse('10 PRINT "HELLO+4"')
        self.genshiBasic.parse('10 PRINT X')
        self.genshiBasic.parse('10 PRINT LEFT$("HELLO",1)')
        self.genshiBasic.parse('10 PRINT X+1')
        self.genshiBasic.parse('10 PRINT SIN(X) + COS(Y)')
        self.genshiBasic.parse('10 IF N EQ 0 THEN PRINT "HELLO"')


if __name__ == "__main__": unittest.main()