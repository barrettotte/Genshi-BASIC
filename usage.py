# Usage of genshi BASIC interpreter

from genshibasic import lexer

def main():
    l = lexer.Lexer()
    tokens = l.lex('hello')
    print('-'*25)
    for t in tokens:
        print(t)

if __name__ == '__main__': main()