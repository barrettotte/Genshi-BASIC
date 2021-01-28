# Parse list of tokens

from .stack import Stack
from .genshi import Genshi

class Parser:

    def __init__(self):
        self.__tok_idx = 0
        self.__tokens = []
        self.__line_no = 0
        self.__symbols = {}
        self.__op_stack = Stack()
        self.__pgm_data = []

    # parse token list and return syntax tree
    def parse(self, tokens, line_no):
        self.__tok_idx = 0
        self.__tokens = tokens
        self.__line_no = line_no
        self.__tok = self.__tokens[self.__tok_idx]
        self.__parse_stmt()

    # handler for base statements
    def __parse_stmt(self):
        k = self.__tok.kind

        if k == Genshi.KW_REM:
            return None  # ignore comments
        elif k in self.PARSE_DICT:
            return self.PARSE_DICT[k](self)
        raise SyntaxError(
            f'Invalid statement found on line {self.__line_no} => {str(self.__tok)}')

    # consume a token
    def __consume(self):
        self.__tok_idx += 1
        if not self.__tok_idx >= len(self.__tokens):
            self.__tok = self.__tokens[self.__tok_idx]

    # check if token is a relational operator
    def __is_rel_op(self, t):
        return t in [Genshi.SYM_LT, Genshi.SYM_LE, Genshi.SYM_EQ, 
            Genshi.SYM_GE, Genshi.SYM_GT, Genshi.SYM_NE]

    # pop two operands from operand stack
    def __pop_two(self):
        return (self.__op_stack.pop(), self.__op_stack.pop())

    # parse variable or array element assignment
    def __parse_assign(self):
        var = self.__tok.lexeme
        self.__consume()

        if self.__tok.kind == Genshi.SYM_EQ:
            self.__consume()
            self.__parse_expr_logic()
            self.__symbols[var] = self.__op_stack.pop()
        elif self.__tok.kind == Genshi.SYM_LPAREN:
            return self.parse_arrassign(var)  # MYARR(1)="WASD"
        raise SyntaxError(f'Could not assign variable {var} on line {self.__line_no}')
    
    # parse array element assignment
    def __parse_assign_arr(self, var):
        raise NotImplementedError('assign_arr')

    def __parse_data(self):
        raise NotImplementedError('DATA')

    def __parse_dim(self):
        raise NotImplementedError('DIM')

    # parse expression (add or sub two terms)
    def __parse_expr(self):
        self.__parse_term()

        while self.__tok.kind in [Genshi.SYM_ADD, Genshi.SYM_SUB]:
            op = self.__tok.kind
            self.__consume()
            self.__parse_term()
            (r, l) = self.__pop_two()
            self.__op_stack.push((l + r) if op == Genshi.SYM_ADD else (l - r))

    # parse an expression term (mul,div,mod two factors)
    def __parse_term(self):
        self.__parse_factor()

        # TODO: preserve sign?

        while self.__tok.kind in [Genshi.SYM_MUL, Genshi.SYM_DIV, Genshi.SYM_MOD]:
            op = self.__tok.kind
            self.__consume()
            self.__parse_factor()
            (r, l) = self.__pop_two()

            if op == Genshi.SYM_MUL:
                self.__op_stack.push(l * r)
            elif op == Genshi.SYM_DIV:
                self.__op_stack.push(l / r)
            else:
                self.__op_stack.push(l % r)

    # parse an expression factor (atomic unit of numerical expression)
    def __parse_factor(self):

        if self.__tok.kind == Genshi.TT_STRING:
            self.__op_stack.push(self.__tok.lexeme)
            self.__consume()

        elif self.__tok.kind == Genshi.TT_UINT:
            self.__op_stack.push(int(self.__tok.lexeme))
            self.__consume()

        elif self.__tok.kind == Genshi.TT_UFLOAT:
            self.__op_stack.push(float(self.__tok.lexeme))
            self.__consume()

        elif self.__tok.kind == Genshi.TT_IDENTIFIER:
            var = self.__tok.lexeme

            if f'@{var}' in self.__symbols:
                self.__parse_factor_array()
            elif var in self.__symbols:
                self.__op_stack.push(self.__symbols[var])
            else:
                raise SyntaxError(f'Variable {var} is undefined on line {self.__line_no}')
            self.__consume()

        elif self.tok_kind in self.BIF_DICT:
            self.__op_stack(self.BIF_DICT[self.__tok.kind](self))

        elif self.tok_kind == Genshi.SYM_LPAREN:
            raise NotImplementedError('factor => GROUPS!!')  # TODO:
        
        else:
            raise RuntimeError(f'Unexpected value for factor on line {self.__line_no}')

    # parse factor as an array element
    def __parse_factor_array(self):
        var = f'@{self.__token.lexeme}'
        self.__consume()

        if self.__tok.kind != Genshi.SYM_LPAREN:
            raise SyntaxError(f"Expected '(' on line {self.__line_no}")
        
        indices = []  #  A(I,J,K)
        if not self.__tok_idx >= len(self.__tokens):
            self.__parse_expr()
            indices.append(self.__op_stack.pop())

            while self.__tok.kind == Genshi.SYM_COMMA:
                self.__consume()
                self.__parse_expr()
                indices.append(self.__op_stack.pop())

        elem = self.__get_arr_elem(self.__symbols[var], indices)
        self.__op_stack.push(elem)

    # get element from array based on 1-3 indices
    def __get_arr_elem(self, arr, indices):
        dims = len(indices)
        if dims != self.__get_arr_dim(arr):
            raise RuntimeError(f'Array dimension mismatch on line {self.__line_no}')
        try:
            if dims == 1:
                return arr[indices[0]]
            elif dims == 2:
                return arr[indices[0]][indices[1]]
            elif dims == 3:
                return arr[indices[0]][indices[1]][indices[2]]
        except IndexError:
            raise SyntaxError(f'Array index out of bounds on line {self.__line_no}')
    
    # get dimension of array
    def __get_arr_dim(self, arr):
        if not type(arr) == list:
            return []
        return [len(arr)] + self.__get_arr_dim(arr[0])
        # TODO: check if works correctly with jagged arrays?

    # parse a logical expression (AND,OR,XOR,NOT)
    def __parse_expr_logic(self):
        if self.__tok.kind == Genshi.KW_NOT:
            self.__parse_not()
        else:
            self.__parse_expr_rel()

        while self.__tok.kind in [Genshi.KW_AND, Genshi.KW_OR, Genshi.KW_XOR]:
            op = self.__tok.kind
            self.__consume()

            if self.__tok.kind == Genshi.KW_NOT:
                self.__parse_not()
            else:
                self.__parse_expr_rel()

            (r, l) = self.__pop_two()

            if op == Genshi.KW_AND:
                self.__op_stack.push(l and r)
            elif op == Genshi.KW_OR:
                self.__op_stack.push(l or r)
            else:
                self.__op_stack.push(l ^ r)
    
    # parse a relational expression
    def __parse_expr_rel(self):
        self.__parse_expr()

        if self.__is_rel_op(self.__tok.kind):
            op = self.__tok.kind
            self.__consume()
            self.__parse_expr()
            (r, l) = self.__pop_two()

            if op == Genshi.SYM_LT:
                self.__op_stack.push(l < r)
            elif op == Genshi.SYM_LE:
                self.__op_stack.push(l <= r)
            elif op == Genshi.SYM_EQ:
                self.__op_stack.push(l == r)
            elif op == Genshi.SYM_GE:
                self.__op_stack.push(l >= r)
            elif op == Genshi.SYM_GT:
                self.__op_stack.push(l > r)
            elif op == Genshi.SYM_NE:
                self.__op_stack.push(l != r)

    def __parse_for(self):
        raise NotImplementedError('FOR')

    def __parse_gosub(self):
        raise NotImplementedError('GOSUB')
    
    def __parse_goto(self):
        raise NotImplementedError('GOTO')
    
    def __parse_if(self):
        raise NotImplementedError('IF')

    def __parse_input(self):
        raise NotImplementedError('INPUT')

    # parse variable declaration
    def __parse_let(self):
        self.__consume()
        self.__parse_assign()

    # parse logical NOT
    def __parse_not(self):
        self.__consume()
        self.__parse_expr_rel()
        self.__op_stack.push(not self.__op_stack.pop())

    def __parse_print(self):
        raise NotImplementedError('PRINT')

    def __parse_read(self):
        raise NotImplementedError('READ')

    ### Built-in Functions ###

    def __bif_abs(self):
        raise NotImplementedError('ABS')

    def __bif_asc(self):
        raise NotImplementedError('ASC')

    def __bif_atn(self):
        raise NotImplementedError('ATN')

    def __bif_chr(self):
        raise NotImplementedError('CHR')

    def __bif_cos(self):
        raise NotImplementedError('COS')

    def __bif_exp(self):
        raise NotImplementedError('EXP')

    def __bif_int(self):
        raise NotImplementedError('INT')

    def __bif_left(self):
        raise NotImplementedError('LEFT')

    def __bif_len(self):
        raise NotImplementedError('LEN')

    def __bif_log(self):
        raise NotImplementedError('LOG')

    def __bif_mid(self):
        raise NotImplementedError('MID')

    def __bif_right(self):
        raise NotImplementedError('RIGHT')

    def __bif_rnd(self):
        raise NotImplementedError('RND')

    def __bif_sgn(self):
        raise NotImplementedError('SGN')

    def __bif_sin(self):
        raise NotImplementedError('SIN')

    def __bif_spc(self):
        raise NotImplementedError('SPC')

    def __bif_sqr(self):
        raise NotImplementedError('SQR')

    def __bif_str(self):
        raise NotImplementedError('STR')

    def __bif_tan(self):
        raise NotImplementedError('TAN')

    # dictionary of function pointers for "base statements"
    PARSE_DICT = {
        Genshi.KW_DATA: __parse_data, Genshi.KW_DIM: __parse_dim,
        Genshi.KW_FOR: __parse_for, Genshi.KW_GOSUB: __parse_gosub,
        Genshi.KW_GOTO: __parse_goto, Genshi.KW_IF: __parse_if,
        Genshi.KW_INPUT: __parse_input, Genshi.KW_LET: __parse_let,
        Genshi.KW_PRINT: __parse_print, Genshi.KW_READ: __parse_read,
    }

    # dictionary of function pointers for all built-in functions
    BIF_DICT = {
        Genshi.KW_ABS: __bif_abs, Genshi.KW_ASC: __bif_asc, Genshi.KW_ATN: __bif_atn,
        Genshi.KW_CHR: __bif_chr, Genshi.KW_COS: __bif_cos, Genshi.KW_EXP: __bif_exp,
        Genshi.KW_INT: __bif_int, Genshi.KW_LEFT: __bif_left, Genshi.KW_LEN: __bif_len,
        Genshi.KW_LOG: __bif_log, Genshi.KW_MID: __bif_mid, Genshi.KW_RIGHT: __bif_right,
        Genshi.KW_RND: __bif_rnd, Genshi.KW_SGN: __bif_sgn, Genshi.KW_SIN: __bif_sin,
        Genshi.KW_SPC: __bif_spc, Genshi.KW_SQR: __bif_sqr, Genshi.KW_STR: __bif_str,
        Genshi.KW_TAN: __bif_tan,
    }
