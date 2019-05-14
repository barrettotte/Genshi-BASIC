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
        #TODO: unit test against debug info

    

    
        

if __name__ == "__main__": unittest.main()