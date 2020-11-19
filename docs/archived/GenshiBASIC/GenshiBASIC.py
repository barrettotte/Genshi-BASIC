import io, sys
import Constants as constants
import Utils as utils
import Warnings as warnings
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter

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

    def read_src(self, src):
        prepped = []
        lines = src.split("\n") if not type(src) is list else src
        for i in range(len(lines)):
            split = utils.split_and_filter(lines[i])
            if len(split) > 0 and not split[0].isdigit():
                warnings.raise_missing_linenum(lines[i])
                lines[i] = str(i+1) + " " + lines[i]
            if len(lines[i]) > 0:
                prepped.append(lines[i])
        return prepped

    def load_src(self, src, is_file_path=False):
        self.check_src_params(src, is_file_path)
        src = utils.read_file(src, throw_error=True) if is_file_path else src
        if type(src) is io.TextIOWrapper:
            ext_split = src.name.split(".")
            if ext_split[len(ext_split)-1] != "bas": 
                warnings.raise_file_extension(src.name)
            src = src.readlines()
        return self.read_src(src)

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

    def parse(self, src, is_file_path=False):
        return self.parser.parse(self.lexer.lex(self.load_src(src, is_file_path)))

    def interpret(self, src, is_file_path=False):
        out = self.interpreter.interpret(self.parser.parse(self.lexer.lex(self.load_src(src, is_file_path))))
        print("\n".join(out))

    def debug(self, src, is_file_path=False):
        info = {"src_original": src}
        info["src_cleaned"] = self.load_src(src, is_file_path)
        info["lexemes"] = self.lexer.make_lexemes(info["src_cleaned"])
        info["tokens"] = self.lexer.lex(info["src_cleaned"])
        info["parse_tree"] = self.parser.parse(info["tokens"])
        info["interpreted"] = self.interpreter.debug(info["parse_tree"])
        return info
    
    def print_tokens(self, tokens_dict):
        for line_num, tokens in tokens_dict.items():
            print(line_num)
            for token in tokens:
                print("  " + str(token))