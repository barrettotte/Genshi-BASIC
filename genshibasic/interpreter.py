# Feed the parser and traverse through program until halted.

from .genshi import Genshi
from .lexer import Lexer
from .parser import Parser
from .stack import Stack


class Interpeter:

    def __init__(self):
        self.__pgm = {}
        self.__jump_stack = Stack()
        self.__lines = []

    def peek_pgm(self):
        return self.__pgm.copy()

    def dump(self):
        print('pgm:')
        for line, stmt in self.__pgm.items():
            for tok in stmt:
                print(tok)
        print(f'lines: {self.__lines}')
        print(f'jump_stack: {self.__jump_stack}')

        self.__parser.dump()

    def interpret(self, src):
        idx = self.__load_pgm(src)
        next_line = self.__lines[0]

        while idx < len(self.__lines):
            stmt = self.__pgm[self.__lines[idx]]
            (jump_to, state) = self.__parser.parse(stmt[1:], stmt[0])

            if state == Genshi.STATE_GOTO:
                idx = self.__lines.index(jump_to)
                next_line = jump_to

            elif state == Genshi.STATE_LOOP_START:
                self.__jump_stack.push(next_line)  # save loop start
                idx += 1
                next_line = self.__lines[idx]

            elif state == Genshi.STATE_LOOP_NORMAL:
                idx = self.__lines.index(self.__jump_stack.pop())
                next_line = self.__lines[idx]

            elif state == Genshi.STATE_LOOP_DONE:
                idx += 1
                while idx < len(self.__lines):
                    toks = self.__pgm[self.__lines[idx]]
                    if len(toks) > 1 and toks[0].kind == Genshi.KW_NEXT \
                       and toks[1].lexeme == jump_to:

                        idx += 1
                        if idx < len(self.__lines):
                            next_line = self.__lines[idx]
                            break
                    idx += 1

            elif state == Genshi.STATE_GOSUB:
                if idx + 1 < len(self.__lines):
                    self.__jump_stack.push(self.__lines[idx + 1])
                idx = self.__lines.index(jump_to)
                next_line = jump_to

            elif state == Genshi.STATE_RETURN:
                idx = self.__lines.index(self.__jump_stack.pop())
                next_line = self.__lines[idx]

            elif idx + 1 < len(self.__lines):
                idx += 1
                next_line = self.__lines[idx]

            else:
                break

    # load program and line numbers into interpreter
    def __load_pgm(self, src):
        self.__lexer = Lexer()
        self.__parser = Parser()
        first_line = None

        for line in src:
            tokens = self.__lexer.lex(line)

            if not first_line:
                first_line = int(tokens[0].lexeme)
            self.__pgm[int(tokens[0].lexeme)] = tokens

        self.__lines = list(self.__pgm.keys())
        self.__lines.sort()
        return self.__lines.index(first_line)
