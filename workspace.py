import os
from GenshiBASIC import GenshiBASIC
import GenshiBASIC.Utils as utils


def main():
    genshiBas = GenshiBASIC.New()
    
    with open('./programs/functions.bas', 'r') as f:
        t = genshiBas.interpret(f)
        #print("------------\n")
        #print(str(t))
        
    #utils.print_dict(t)

if __name__ == "__main__": main()