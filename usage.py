# Usage of genshi BASIC interpreter

from genshibasic import lexer

def main():
    l = lexer.Lexer()
    l.lex('hello')

if __name__ == '__main__': main()