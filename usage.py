# Usage of genshi BASIC interpreter

from genshibasic.lexer import Lexer


def main():
    lexer = Lexer()
    tokens = lexer.lex('hello')
    print('-'*25)
    for t in tokens:
        print(t)


if __name__ == '__main__':
    main()
