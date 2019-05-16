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
        self.genshi_basic.interpret(prog)
    
    def test_bif(self):
        prog = "\n".join([
          '10 LET A=COS(1)',
          '11 LET B=SIN(1)',
          '12 LET C=TAN(1)',
          '13 LET D = TAN(COS(SIN(A)))',
          '14 LET E = PI(2)',
          '15 LET F = RND(3)',
          '16 LET G = SQR(16)',
          '17 LET H = SGN(-4)',
          '18 LET I = ABS(-16)',
          '19 LET J = BIN$(8)',
          '20 LET K = HEX$(15)',
          '21 LET L = EXP(2)',
          '22 LET M = INT(3.57)',
          '23 LET N = LOG(23)',
          '24 LET O = SPC$(10)',
          '25 LET P = CHR$(66)',
          '26 LET Q = STR$(1234)',
          '27 LET R = 1 EQ 1 XOR 1 EQ 1'
        ])
        self.genshi_basic.interpret(prog)
        
    def test_print_and_go(self):
        prog = "\n".join([
          '10 LET A = LEFT$("HELLO", 4)',
          '11 LET B = RIGHT$("HELLO", 4)',
          '12 CLR',
          '13 LET C = MID$("HELLO WORLD", 3, 8)',
          '15 LET D = LEN("HELLO WORLD")',
          '16 LET E = CAT$("HELLO ", 123)',
          '17 LET F = ASC("ASD")',
          '25 PRINTL "HELLO WORLD"',
          '26 PRINTL " WASD"',
          '27 PRINT SIN(5)',
          '100 LET G = "HELLO"',
          '112 PRINTL G',
          '113 PRINT 2 + SIN(5)',
          '115 PRINT G',
          '110 LET H = 10',
          '112 LET I = "WASD"',
          '120 GOTO 100*H',
          '150 I = "UH OH"',
          '130 END',
          '1000 PRINT "HELLO WORLD"'
        ])
        self.genshi_basic.interpret(prog)

    def test_udf_and_if(self):
        prog = "\n".join([
          '10 DEF FN FTEST(X) = X*10',
          '12 DEF FN WASD(X) = GOTO X',
          '13 REM WASD(1000)',
          '14 DEF FN PR(X) = PRINT X',
          '15 LET A = FTEST(10)',
          '20 LET B = FTEST(SIN(A))',
          '30 LET C = SIN(100) * 10',
          '40 DEF FN ADD(X,Y) = X + Y',
          '50 LET D = ADD(1,FTEST(2+LEN("WASD")))',
          '60 DEF FN MEME(X) = X + LEN("MEME")',
          '70 LET E = MEME(10)',
          '80 PR("AHHHHHH")',
          '90 PRINTL 1+4*10',
          '91 PRINTL (1+4)*10',
          '100 A=0+1',
          '101 LET M=((1*6)/3)+9-A',
          '103 LET N= 1 GT 0',
          '105 IF 1 GT 0 THEN PRINT "I WANT DEATH"',
          '107 IF A EQ 1 THEN GOTO 1000',
          '150 PRINT "?????"',
          '1000 END'
        ])
        self.genshi_basic.interpret(prog)

    
        

if __name__ == "__main__": unittest.main()