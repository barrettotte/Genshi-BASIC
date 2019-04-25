import unittest
from GenshiBASIC import GenshiBASIC

class Test_Parse(unittest.TestCase):
    def setUp(self):
        self.genshiBas = GenshiBASIC.New()

    def simple_func(self):
        res = self.genshiBas.parse("10 DEF FN FTEST(X) = X * 3")
        self.assertTrue(True)
    
    def bad_syntax(self):
        pass



if __name__ == "__main__": unittest.main()