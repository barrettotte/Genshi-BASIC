# collection of parsed genshi BASIC statements

class Program:

    def __init__(self):
        self.__pgm = {}  # { '10': 'PRINT "WASD"' }
    
    def __str__(self):
        return 'program' # TODO: