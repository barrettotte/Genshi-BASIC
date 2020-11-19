from .context import genshibasic
import unittest

class ParserTestSuite(unittest.TestCase):
    
    def test_simple(self):
        assert 1==1

if __name__ == '__main__': unittest.main()