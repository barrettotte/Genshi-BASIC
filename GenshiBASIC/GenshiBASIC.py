import io
import GenshiBASIC.Constants as constants
import GenshiBASIC.Utils as utils
import GenshiBASIC.Warnings as warnings
from GenshiBASIC.Lexer import Lexer
from GenshiBASIC.Parser import Parser
from GenshiBASIC.Interpreter import Interpreter

class New:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()

    def check_src_params(self, src_code, is_file_path):
        src_type = type(src_code)
        if not (src_type is str or src_type is io.TextIOWrapper):
            raise TypeError("Source code must be of type str or io.TextIOWrapper")
        elif src_type is io.TextIOWrapper and is_file_path:
            raise TypeError("Source code cannot be type io.TextIOWrapper and have is_file_path=True")
        elif is_file_path and not src_type is str:
            raise TypeError("Expected string for file path")

    def load_src(self, src_code, is_file_path=False):
        prepped = []
        self.check_src_params(src_code, is_file_path)
        src_code = utils.read_file(src_code, throw_error=True) if is_file_path else src_code
        if type(src_code) is io.TextIOWrapper:
            ext_split = src_code.name.split(".")
            if ext_split[len(ext_split)-1] != "bas": 
                warnings.raise_file_extension(src_code.name)
            src_code = src_code.readlines()
        lines = src_code.split("\n") if not type(src_code) is list else src_code
        for i in range(len(lines)):
            split = utils.split_and_filter(lines[i])
            if not split[0].isdigit():
                warnings.raise_missing_linenum(lines[i])
                lines[i] = str(i+1) + " " + lines[i]
            prepped.append(lines[i])
        return prepped

    def get_keywords(self):
        return constants.KEYWORDS

    def get_operators(self):
        return constants.OPERATORS

    def lex(self, src, is_file_path=False):
        return self.make_tokens(src, is_file_path)

    def make_tokens(self, src, is_file_path=False):
        return self.lexer.lex(self.load_src(src, is_file_path))
    
    def make_lexemes(self, src, is_file_path=False):
        return self.lexer.make_lexemes(self.load_src(src, is_file_path))

    def interpret(self, src, is_file_path=False):
        src = self.load_src(src, is_file_path)
        tokens = self.lexer.lex(src)
        # PARSE ...
        # INTERPRET ...
        results = tokens # TODO: TMP
        return results
