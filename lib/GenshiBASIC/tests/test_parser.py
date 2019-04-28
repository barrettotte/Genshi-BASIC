import unittest, GenshiBASIC

class Test_Parser(unittest.TestCase):

    def setUp(self):
        self.genshiBas = GenshiBASIC.New()
        print("Running test: " + str(self._testMethodName))
        

if __name__ == "__main__": unittest.main()