from collections import OrderedDict
import GenshiBASIC.Constants as constants
import GenshiBASIC.Utils as utils
import GenshiBASIC.Warnings as warnings

class Lexer:
    def __init__(self):
        self.lexemes = OrderedDict()
        self.tokens = OrderedDict()

    def clean_line(self, s):
        line = s.lstrip().replace("\n", "").upper()
        if len(line) > constants.COL_LEN: warnings.raise_col_len(s)
        line = line[0:constants.COL_LEN]
        for ch in (constants.PUNCTUATION + constants.OPERATORS):
            if ch in line:
                line = line.replace(ch, " " + ch + " ")
        return utils.split_and_filter(line)

    def make_lexemes(self, src_code):
        self.lexemes = OrderedDict()
        for s in src_code:
            line = self.clean_line(s)
            line_num = line[0]
            if line_num.isdigit():
                self.lexemes[line_num] = line[1:]
                if int(line_num) == constants.MAX_LINES: 
                    warnings.raise_max_lines(len(src_code)) 
                    break
        return self.lexemes

    def classify_lexeme(self, lexeme):
        for op in constants.OPERATORS: 
            if lexeme == op: return "OPERATOR"
        for p in constants.PUNCTUATION: 
            if lexeme == p:  return "PUNCTUATION"
        for kw in constants.KEYWORDS: 
            if lexeme == kw["word"]: return kw["type"]
        return "LITERAL"

    def make_tokens(self, lexemes_dict):
        self.tokens = OrderedDict()
        for line_num, lexemes_list in lexemes_dict.items():
            self.tokens[line_num] = []
            for lexeme in lexemes_list:
                self.tokens[line_num].append({
                    "type": self.classify_lexeme(lexeme), 
                    "value": lexeme, 
                    "line_num": line_num
                })
        return self.tokens

    def lex(self, src_code):
        self.make_lexemes(src_code)
        self.make_tokens(self.lexemes)
        return self.tokens
