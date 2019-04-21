from collections import OrderedDict
import GenshiBASIC.Constants as constants
import GenshiBASIC.Utils as utils
import GenshiBASIC.Warnings as warnings
from GenshiBASIC.Token import Token

class Lexer:
    
    def __init__(self):
        self.lexemes = OrderedDict()
        self.tokens = OrderedDict()

    def clean_line(self, s):
        line = s.lstrip().replace("\n", "").upper()
        if len(line) > constants.COL_LEN: warnings.raise_col_len(s)
        line = line[0:constants.COL_LEN]
        for elem in constants.PUNCTUATION + constants.OPERATORS:
            if elem["char"] in line: line = line.replace(elem["char"], " " + elem["char"] + " ")
        return utils.split_and_filter(line)

    def make_lexemes(self, src):
        self.lexemes = OrderedDict()
        for s in src:
            line = self.clean_line(s)
            line_num = line[0]
            if line_num.isdigit():
                self.lexemes[line_num] = line[1:]
                if int(line_num) == constants.MAX_LINES: 
                    warnings.raise_max_lines(len(src)) 
                    break
        return self.lexemes

    def classify_lexeme(self, lexeme):
        for op in constants.OPERATORS: 
            if lexeme == op["char"]: return op["type"]
        for p in constants.PUNCTUATION: 
            if lexeme == p["char"]:  return p["type"]
        for kw in constants.KEYWORDS: 
            if lexeme == kw["word"]: return kw["type"]
        return "LITERAL"
    
    def set_token_literals(self, tokens):
        for i in range(len(tokens)):
            if tokens[i].literal == None:
                if tokens[i].token_type == "QUOTATION":
                    for j in range(i+1, len(tokens)):
                        if tokens[j].token_type == "QUOTATION":
                            for x in range(i+1, j):
                                tokens[x].literal = "STRING"
                            break
                elif tokens[i].token_type == "LITERAL":
                    if i < (len(tokens)-1) and tokens[i+1].token_type == "EQUALS":
                        tokens[i].literal = "IDENTIFIER"
                    elif i > 0 and tokens[i-1].lexeme == "NEXT":
                        tokens[i].literal = "IDENTIFIER"
                    else:
                        tokens[i].literal = "NUMERIC" if tokens[i].lexeme.isdigit() else "IDENTIFIER" 

    def make_tokens(self, lexemes_dict):
        self.tokens = OrderedDict()
        for line_num, lexemes_list in lexemes_dict.items():
            self.tokens[line_num] = []
            for lexeme in lexemes_list:
                self.tokens[line_num].append(Token(self.classify_lexeme(lexeme), lexeme, line_num))
                self.set_token_literals(self.tokens[line_num])
        return self.tokens

    def lex(self, src):
        return self.make_tokens(self.make_lexemes(src))

