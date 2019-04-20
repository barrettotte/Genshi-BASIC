import os
from GenshiBASIC import GenshiBASIC


def main():
    genshiBas = GenshiBASIC.New()
    
    with open('./programs/binary.bas', 'r') as f:
        genshiBas.interpret(f)


if __name__ == "__main__": main()