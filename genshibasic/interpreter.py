# Feed the parser and traverse through program until halted.

from .genshi import Genshi
from .parser import Parser
from .stack import Stack


class Interpeter:

    def __init__(self):
        self.__pgm = {}
        self.__jump_stack = Stack()

    def peek_pgm(self):
        return self.__pgm.copy()
    
    def interpret(self, tokens):
        self.__parser = Parser()
        self.__load_pgm(tokens)

        lines = list(self.__pgm.keys()).sort()
        next_line = self.__lines[0]
        idx = 0

        while idx < len(lines):
            stmt = lines[idx]
            (jump_to, state) = self.__parser.parse(stmt[0], stmt[1:])

            if state == Genshi.STATE_GOTO:
                idx = lines.index(jump_to)
                next_line = jump_to

            elif state == Genshi.STATE_LOOP_START:
                self.__jump_stack.push(next_line)  # save loop start
                idx += 1
                next_line = lines[idx]

            elif state == Genshi.STATE_LOOP_NORMAL:
                idx = lines.index(self.__jump_stack.pop())
                next_line = lines[idx]
            
            elif state == Genshi.STATE_LOOP_DONE:
                idx += 1
                while idx < len(lines):
                    toks = self.__pgm[lines[idx]]
                    if len(toks) > 1 and toks[0].kind == Genshi.KW_NEXT \
                        and toks[1].lexeme == jump_to:

                        idx += 1
                        if idx < len(lines):
                            next_line = lines[idx]
                            break
                    idx += 1

            elif state == Genshi.STATE_GOSUB:
                if idx + 1 < len(lines):
                    self.__jump_stack.push(lines[idx + 1])
                idx = lines.index(jump_to)
                next_line = jump_to

            elif state == Genshi.STATE_RETURN:
                idx = lines.index(self.__jump_stack.pop())
                next_line = lines[idx]

            else:
                idx += 1
                next_line = lines[idx]
    
    # load program into interpreter
    def __load_pgm(self, tokens):
        for tok in tokens:
            self.__pgm[tok[0]] = tok[1:]
