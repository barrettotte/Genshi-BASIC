import unittest, GenshiBASIC, warnings

class Test_Interpreter(unittest.TestCase):

    def setUp(self):
        self.genshi_basic = GenshiBASIC.New()
        print("   Running test: " + str(self._testMethodName))
        warnings.filterwarnings("ignore") # suppress warning output

    def print_dict_of_lists(self, d): 
        for k, v in d.items():
            print(k)
            for e in v: print("   " + str(e))

    def test_var(self):
        prog = "\n".join([
          '10 LET A=4', '20 LET B=A+1', '30 LET C="HELLO WORLD"', '40 A=123', '50 B=B+A+2.5'
        ])
        self.genshi_basic.interpret(prog)
        # TODO: unit test against debug info

    def test_symbolic_ops(self):
        prog = "\n".join([
          '10 LET A=0', '11 LET B=0', '12 LET C=0', '13 LET D=0', '14 LET E=0', '15 LET F=0',
          '20 A=4+1',   '30 B=2*4',   '40 C=6/3',   '50 D=2*5',   '60 E=7%4',   '70 F=10^2'
        ])
        expected = {"A": 5, "B": 8, "C": 2, "D": 10, "E": 3, "F": 100}
        identifiers = self.genshi_basic.debug(prog)["interpreted"]["identifiers"]
        for ident, val in expected.items():
            self.assertTrue(expected[ident] == identifiers[ident])
    
    def test_bif(self):
        prog = "\n".join([
          '10 LET A=COS(1)', '11 LET B=SIN(1)', '12 LET C=TAN(1)', '13 LET D = TAN(COS(SIN(A)))',
          '14 LET E = PI(2)', '15 LET F = RND(3)', '16 LET G = SQR(16)', '17 LET H = SGN(-4)',
          '18 LET I = ABS(-16)', '19 LET J = BIN$(8)', '20 LET K = HEX$(15)', '21 LET L = EXP(2)',
          '22 LET M = INT(3.57)', '23 LET N = LOG(23)', '24 LET O = SPC$(10)', '25 LET P = CHR$(66)',
          '26 LET Q = STR$(1234)', '27 LET R = 1 EQ 1 XOR 1 EQ 1'
        ])
        expected_identifiers = {
          "A": 0.5403023058681398, "B": 0.8414709848078965, "C": 1.5574077246549023, "D": 1.186745810605441,
          "E": 6.283185307179586, "G": 4, "H": -1, "I": 16, "J": '0b1000', "K": '0xf', "L": 7.38905609893065, 
          "M": 3, "N": 3.1354942159291497, "O": '          ', "P": 'B', "Q": "1234", "R": 0
        }
        debug = self.genshi_basic.debug(prog)["interpreted"]
        identifiers = debug["identifiers"]
        out = debug["out_buffer"]
        self.assertTrue(len(out) == 0)
        for ident, val in expected_identifiers.items():
            self.assertTrue(expected_identifiers[ident] == identifiers[ident])
        
    def test_print_and_go(self):
        prog = "\n".join([
          '10 LET A = LEFT$("HELLO", 4)', '11 LET B = RIGHT$("HELLO", 4)', '12 CLR',
          '13 LET C = MID$("HELLO WORLD", 3, 8)', '15 LET D = LEN("HELLO WORLD")',
          '16 LET E = CAT$("HELLO ", 123)', '17 LET F = ASC("ASD")', '25 PRINTL "HELLO WORLD"', 
          '26 PRINTL " WASD"', '27 PRINT SIN(5)', '100 LET G = "HELLO"', '112 PRINTL G', 
          '113 PRINT 2 + SIN(5)', '115 PRINT G', '110 LET H = 10', '112 LET I = "WASD"', '120 GOTO 100*H',
          '150 I = "UH OH"', '130 END', '1000 PRINT "HELLO WORLD"'
        ])
        expected_identifiers = {
          "C": 'LO WO', "D": 11, "E": 'HELLO 123', "F": 65, "G": 'HELLO', "I": 'UH OH', "H": 10
        }
        expected_out = ['HELLO WORLD', ' WASD', '-0.95892427466313851.0410757253368614HELLOHELLO WORLD']
        debug = self.genshi_basic.debug(prog)["interpreted"]
        identifiers = debug["identifiers"]
        out = debug["out_buffer"]
        for ident, val in expected_identifiers.items():
            self.assertTrue(expected_identifiers[ident] == identifiers[ident])
        for i in range(len(expected_out)):
            self.assertTrue(expected_out[i] == out[i])

    def test_udf_and_if(self):
        prog = "\n".join([ 
          '10 DEF FN FTEST(X) = X*10','12 DEF FN WASD(X) = GOTO X', '13 REM WASD(1000)', 
          '14 DEF FN PR(X) = PRINT X', '15 LET A = FTEST(10)', '20 LET B = FTEST(SIN(A))', 
          '30 LET C = SIN(100) * 10', '40 DEF FN ADD(X,Y) = X + Y', '50 LET D = ADD(1,FTEST(2+LEN("WASD")))', 
          '60 DEF FN MEME(X) = X + LEN("MEME")', '70 LET E = MEME(10)', '80 PR("AHHHHHH")', '90 PRINTL 1+4*10', 
          '91 PRINTL (1+4)*10', '100 A=0+1', '101 LET M=((1*6)/3)+9-A', '103 LET N= 1 GT 0', 
          '105 IF 1 GT 0 THEN PRINT "I WANT DEATH"', '107 IF A EQ 1 THEN GOTO 1000', '150 PRINT "?????"', '1000 END'
        ])
        expected_identifiers = {
          "A": 1, "B": -5.063656411097588, "C": -5.063656411097588, "D": 61, "E": 14, "M": 10, "N": 1
        }
        expected_funcs = {
          "FTEST": (["X"], 1), "WASD": (["X"], 2), "PR": (["X"], 2),
          "ADD": (["X","Y"], 1), "MEME": (["X"], 1)
        }
        expected_out = ['AHHHHHH41', '50', 'I WANT DEATH']
        debug = self.genshi_basic.debug(prog)["interpreted"]
        identifiers = debug["identifiers"]
        out = debug["out_buffer"]

        for ident, val in expected_identifiers.items():
            self.assertTrue(expected_identifiers[ident] == identifiers[ident])
        for func, val in expected_funcs.items():
            self.assertTrue(identifiers[func]['params'] == val[0])
            self.assertTrue(len(identifiers[func]['def']) == val[1])
        for i in range(len(expected_out)):
            self.assertTrue(expected_out[i] == out[i])
    
    def test_array(self):
        prog = "\n".join([
          '10 DIM A(7)',
          '15 A(1) = 123',
          '20 DIM B(4,2,1)',
          '40 B(0,0,0) = 5',
          '41 B(1,0,0) = 1',
          '42 B(1,1,0) = 2',
          '43 B(0,1,0) = 3',
          '60 LET X = 5+B(0,0,0)',
          '65 LET Y = B(0,11-X,0)',
          '70 LET Z = B(0,0,0) + A(1)',
          '1000 END'
        ])
        self.genshi_basic.interpret(prog)

    def test_gosub(self):
      prog = "\n".join([
        '10 PRINT "HELLO"',
        '20 GOSUB 500',
        '100 END',
        '200 PRINT "!!!"',
        '500 PRINT "WORLD"',
        '510 RETURN'
      ])
      expected_out = ['HELLOWORLD']
      debug = self.genshi_basic.debug(prog)["interpreted"]
      identifiers = debug["identifiers"]
      self.assertTrue(identifiers == {})
      out = debug["out_buffer"]
      self.assertTrue(out == ['HELLOWORLD'])

    def test_for(self):
      prog = "\n".join([
        '10  REM THE CLASSIC FIZZBUZZ',
        '20  FOR I=1 TO 100 STEP 1',
        '30    IF (I % 15) EQ 0 THEN PRINTL CAT$(I, " - FIZZBUZZ")',
        '40    IF (I % 3)  EQ 0 THEN PRINTL CAT$(I, " - FIZZ")',
        '50    IF (I % 5)  EQ 0 THEN PRINTL CAT$(I, " - BUZZ")',
        '60  ENDFOR',
        '70  END'  
      ])
      debug = self.genshi_basic.debug(prog)["interpreted"]
      out = debug["out_buffer"]
      self.assertTrue(len(out) == 59) # You're crazy if you think I'm going to check every entry
      self.assertTrue(debug["identifiers"]["I"] == 100)
        

if __name__ == "__main__": unittest.main()