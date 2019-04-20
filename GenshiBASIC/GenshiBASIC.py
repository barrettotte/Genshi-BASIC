import io
import GenshiBASIC.Utils as utils
from GenshiBASIC.Lexer import Lexer
from GenshiBASIC.Parser import Parser
from GenshiBASIC.Interpreter import Interpreter

class New:

    def __init__(self):
        print("Made GenshiBas Object")
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()

    def get_src_code(self, s, is_file_path):
        if isinstance(s, io.IOBase):
            return s.readlines()
        return utils.read_file(s, throw_error=True) if is_file_path else s

    def interpret(self, s, is_file_path=False):
        src_code = self.get_src_code(s, is_file_path)
        self.lexer.lex(src_code)
        