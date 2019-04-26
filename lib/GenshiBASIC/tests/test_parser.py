import unittest, GenshiBASIC

class Test_Parser(unittest.TestCase):

    def setUp(self):
        self.genshiBas = GenshiBASIC.New()
        print("Running test: " + str(self._testMethodName))

    def test_valid_func(self):
        pass
        # res = self.genshiBas.parse("10 DEF FN FTEST(X) = X * 3")
        # TODO: assert result
    
    def test_invalid_func(self):
        pass


if __name__ == "__main__": unittest.main()