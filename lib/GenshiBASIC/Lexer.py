from collections import OrderedDict
import Constants as constants
import Utils as utils
import Warnings as warnings
from Token import Token

class Lexer:
    
    def __init__(self):
        self.lexemes = OrderedDict()
        self.tokens = OrderedDict()

    def clean_line(self, s):
        line = s.lstrip().replace("\n", "").replace("\r", "").upper()
        if len(line) > constants.COL_LEN: 
            warnings.raise_col_len(s)
        line = line[0:constants.COL_LEN]
        for elem in constants.PUNCTUATION + constants.OPERATORS:
            if elem["char"] in line:
                line = line.replace(elem["char"], " " + elem["char"] + " ")
        return utils.split_and_filter(line)

    def make_lexemes(self, src):
        self.lexemes = OrderedDict()
        for s in src:
            line = self.clean_line(s)
            line_num = line[0] if len(line) > 0 else ""
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
    
    def prepare_tokens(self, tokens):
        for i in range(len(tokens)):
            token = tokens[i]
            in_quote = False
            if token.literal != None: 
                continue
            elif token.token_type == "COMMENT":
                for j in range(i+1, len(tokens)): 
                    tokens[j].token_type = "COMMENT"
            elif token.token_type == "QUOTATION":
                in_quote = True
                for j in range(i+1, len(tokens)):
                    if tokens[j].token_type == "QUOTATION":
                        in_quote = False
                        for x in range(i+1, j): 
                            tokens[x].literal = "STRING"
                        break
                        if j+1 >= len(tokens): 
                            break
            elif token.token_type == "LITERAL":
                if i < (len(tokens)-1) and tokens[i+1].token_type == "EQUALS":
                    token.literal = "IDENTIFIER"
                elif i > 0 and tokens[i-1].lexeme == "NEXT":
                    token.literal = "IDENTIFIER"
                else:
                    token.literal = "NUMERIC" if token.lexeme.isdigit() else "IDENTIFIER"
            elif i > 0 and token.lexeme == "-" and tokens[i-1].token_type in ["RIGHT_PAREN", "LITERAL"]:
                tokens[i].token_type = "BINARY"
        if in_quote: 
            raise SyntaxError("Non-terminated string; line: " + self.tokens_to_line(tokens))
        return tokens

    def tokens_to_line(self, tokens):
        line = str(tokens[0].line)
        for t in tokens:
            line += " " + t.lexeme
        return line

    def make_tokens(self, lexemes_dict):
        self.tokens = OrderedDict()
        for line_num, lexemes_list in lexemes_dict.items():
            self.tokens[line_num] = []
            for lexeme in lexemes_list:
                self.tokens[line_num].append(Token(self.classify_lexeme(lexeme), lexeme, line_num))
            self.tokens[line_num] = self.prepare_tokens(self.tokens[line_num])
        return self.tokens

    def lex(self, src):
        return self.make_tokens(self.make_lexemes(src))

