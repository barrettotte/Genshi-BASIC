# collection of parsed genshi BASIC statements with line numbers

class Program:

    def __init__(self):
        self.__pgm = {}  # { '10': 'PRINT "WASD"' }
    
    def __str__(self):
        return 'program' # TODO: