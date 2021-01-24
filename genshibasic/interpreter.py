# Interpret a file or run genshi BASIC interactively

import sys


class Interpreter:

    def __init__(self):
        pass  # TODO:

    # interpret a file from given filepath
    def interpret_from(self, fp):
        pass  # TODO:

    # interpret from given file
    def interpret_file(self, f):
        pass  # TODO:

    # interpret from given string
    def interpret_src(self, src):
        pass  # TODO:

    # run interpreter interactively
    def repl(self):
        try:
            pass  # TODO:
        except Exception as e:
            print(e, file=sys.stderr, flush=True)
