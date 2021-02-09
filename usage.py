# Usage of genshi BASIC interpreter

from genshibasic.interpreter import Interpeter

def main():
    # example_1()
    example_2()

# example of assignment, operators, and printing
def example_1():
    pgm = [
        '10 REM Example 1',
        '20 LET A=3+4 * 6/2',
        '30 PRINT "A="; A',
        '40 A=8',
        '50 PRINT "NOW A="; A',
        '100 END'
    ]
    genshi_int = Interpeter()
    genshi_int.interpret(pgm)
    # A=15.0
    # NOW A=8

# example of arrays
def example_2():
    pgm = [
        '10  REM Example 2',
        '20  DIM X(2,3)',
        '30  X(1,1)=10',
        '40  PRINT X(1,1)',
        '50  X(2,1)=90',
        '60  X(2,2)= X(2,1) + X(1,1)',
        '70  PRINT X(2,2)',
        '100 END'
    ]
    genshi_int = Interpeter()
    genshi_int.interpret(pgm)
    genshi_int.dump()



if __name__ == '__main__':
    main()
