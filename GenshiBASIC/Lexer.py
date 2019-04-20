from collections import OrderedDict
import GenshiBASIC.Constants as constants
import GenshiBASIC.Utils as utils

class Lexer:
    def __init__(self):
        print("Made Lexer")
        self.ops = constants.OPERATORS
        self.cmds = constants.COMMANDS
        self.puncs = constants.PUNCTUATION

    def clean_line(self, s):
        line = s.lstrip().replace("\n", "").upper()[0:39] # C64 max_col=40
        for ch in (self.puncs + self.ops):
            if ch in line:
                line = line.replace(ch, " " + ch + " ")
        return list(filter(None, line.strip().split(" ")))
                
    def make_code_dict(self, src_code):
        code_dict = OrderedDict()
        for s in src_code:
            line = self.clean_line(s) 
            line_num = line[0]
            if line_num.isdigit(): # Assume lines starting with non-numeric are invalid, ignore them
                code_dict[line_num] = line[1:]
        return code_dict

    def lex(self, src_code):
        print("Lexing...")
        code_dict = self.make_code_dict(src_code)
        
        # TODO: Remove these debug lines !
        for k,v in code_dict.items():
            print(k + "\n" + str(v))
        print("\n\n")
        line = "A(I)=N-INT(N/2)*2"
        print("1100  " + line)
        print("Tokens  " + str(self.clean_line(line)))
            
        