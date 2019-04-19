from collections import OrderedDict

class Lexer:
    def __init__(self):
        print("Made Lexer")

    def make_code_dict(self, src_code):
        code_dict = OrderedDict()
        for s in src_code:
            code = s.lstrip().replace("\n", "").upper()[0:39].split(" ") # C64 max_col=40
            if code[0].isdigit(): # Assume lines starting with non-numeric are invalid, ignore them
                code_dict[code[0]] = code[1:]
        return code_dict

    def lex(self, src_code):
        print("Lexing...")
        code_dict = self.make_code_dict(src_code)
        
        for k,v in code_dict.items():
            print(k + " " + str(v))
            
        