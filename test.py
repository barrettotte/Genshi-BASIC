import os
from GenshiBas import GenshiBas


def main():
    genshiBas = GenshiBas.New()
    
    with open('./test.bas', 'r') as f:
        genshiBas.interpret(f)
    

if __name__ == "__main__": main()