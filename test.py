import os
from GenshiBas import GenshiBas


def main():
    genshiBas = GenshiBas.New()
    f = os.path.join(os.getcwd(), "test0.bas")
    genshiBas.interpret(f, is_file_path=True)

if __name__ == "__main__": main()