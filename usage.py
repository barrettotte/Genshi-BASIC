# Usage of genshi BASIC interpreter

from genshibasic.lexer import Lexer
from genshibasic.parser import Parser

def main():
    tokens = Lexer().lex('10 LET A=3+4 * 6/2') # 15
    tree = Parser().parse(tokens[1:], tokens[0])


if __name__ == '__main__':
    main()
