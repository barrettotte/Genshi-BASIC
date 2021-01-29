# Parse list of tokens one line at a time.
#
# Rather than build a parse tree and then traverse it, 
# just evaluate expressions as is, build the symbol table,
# and let the interpreter handle branching (GOTO,GOSUB,etc).

from .stack import Stack
from .genshi import Genshi

class Parser:

    def __init__(self):
        self.__idx = 0
        self.__tokens = []
        self.__line_no = 0
        self.__symbols = {}
        self.__op_stack = Stack()
        self.__pgm_data = []  # DATA,READ
    
    # peek symbol table, return a copy
    def peek_symbols(self):
        return self.__symbols.copy()

    # peek program data, return a copy
    def peek_data(self):
        return self.__pgm_data.copy()

    # parse token list and return syntax tree
    def parse(self, tokens, line_no_tok):
        self.__idx = 0
        self.__tokens = tokens
        self.__line_no = line_no_tok.lexeme
        self.__tok = self.__tokens[self.__idx]
        return self.__parse_stmt()

    # handler for base statements
    def __parse_stmt(self):
        k = self.__tok.kind
        if k == Genshi.KW_REM:
            return None  # ignore comments
        elif k in self.PARSE_DICT:
            return self.PARSE_DICT[k](self)
        self.__raise(f'Invalid statement found')

    # consume a token
    def __consume(self):
        self.__idx += 1
        if not self.__idx >= len(self.__tokens):
            self.__tok = self.__tokens[self.__idx]

    # utility so i can cut down on writing "on line x" in each exception
    def __raise(self, msg, err_type=SyntaxError):
        e = f"{msg} on line {self.__line_no}\n\tcurrent token: {self.__tok}"
        raise err_type(e)

    # assert syntax based on current token
    def __assert_syntax(self, expected):
        actual = self.__tok.kind
        if actual != expected:
            self.__raise(f"Expected '{expected}', but got '{actual}'")

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
        self.__consume()  # MYVAR

        if self.__tok.kind == Genshi.SYM_EQ:
            self.__consume()  # =
            self.__parse_expr_logic()
            self.__symbols[var] = self.__op_stack.pop()
        elif self.__tok.kind == Genshi.SYM_LPAREN:
            self.__parse_assign_arr(f'@{var}')
        else:
            self.__raise(f"Could not assign variable '{var}'")
    
    # parse array element assignment
    def __parse_assign_arr(self, var):
        self.__assert_syntax(Genshi.SYM_LPAREN)
        self.__consume()                                 # (
        indices = self.__parse_list([Genshi.SYM_COMMA])  #  I,J,K

        if var not in self.__symbols:
            self.__raise(f"Array '{var[1:]}' is undefined", KeyError)
        dims = self.__get_arr_dim(self.__symbols[var])

        if dims != len(indices):
            self.__raise(f"Invalid access to array '{var[1:]}'", IndexError)
        self.__assert_syntax(Genshi.SYM_RPAREN)
        self.__consume()                                 # )
        self.__assert_syntax(Genshi.SYM_EQ)
        self.__consume()                                 # =

        self.__parse_expr_logic()
        val = self.__op_stack.pop()

        try:
            if dims == 1:
                self.__symbols[var]
            elif dims == 2:
                self.__symbols[var]
            elif dims == 3:
                self.__symbols[var]
        except IndexError as e:
            self.__raise('Array index out of bounds', e)

    # parse internal program data (constants)
    def __parse_data(self):
        self.__consume()  # DATA
        self.__pgm_data.extend(self.__parse_list([Genshi.SYM_COMMA]))

    # parse array declaration
    def __parse_dim(self):
        self.__consume()                              # DIM
        var = f'@{self.__tok.lexeme}'
        self.__consume()                              # MYARR
        self.__assert_syntax(Genshi.SYM_LPAREN)
        self.__consume()                              # (
        dims = self.__parse_list([Genshi.SYM_COMMA])  #   I,J,K
        self.__assert_syntax(Genshi.SYM_RPAREN)
        self.__consume()                              # )
        dim_len = len(dims)

        if dim_len == 0:
            self.__raise(f'Array declared with no dimensions')
        elif dim_len < 0:
            self.__raise(f'Array declared with invalid dimensions')
        elif dim_len > 3:
            self.__raise(f'Array declared with too many dimensions')

        arr_init = [0]
        if dim_len >= 1:
            arr_init = [arr_init * dims[0]]  # 1D with I elements
        if dim_len >= 2:
            arr_init = [arr_init * dims[1]]  # 2D with IxJ elements
        if dim_len == 3:
            arr_init = [arr_init * dims[2]]  # 3D with IxJxK elements
        self.__symbols[var] = arr_init

    # parse a list of expressions with delimiters
    def __parse_list(self, delimiters):
        vals = []
        if not self.__idx >= len(self.__tokens):
            self.__parse_expr()
            vals.append(self.__op_stack.pop())

            while self.__tok.kind in delimiters:
                self.__consume()  # delimiter
                self.__parse_expr()
                vals.append(self.__op_stack.pop())
        return vals

    # parse expression (add or sub two terms)
    def __parse_expr(self):
        self.__parse_term()

        while self.__tok.kind in [Genshi.SYM_ADD, Genshi.SYM_SUB]:
            op = self.__tok.kind
            self.__consume()  #  +  -
            self.__parse_term()
            (r, l) = self.__pop_two()
            self.__op_stack.push((l + r) if op == Genshi.SYM_ADD else (l - r))

    # parse an expression term (mul,div,mod two factors)
    def __parse_term(self):
        self.__parse_factor()
        # TODO: preserve sign?

        while self.__tok.kind in [Genshi.SYM_MUL, Genshi.SYM_DIV, Genshi.SYM_MOD]:
            op = self.__tok.kind
            self.__consume()  #  *  /  %
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
            self.__consume()  # string literal

        elif self.__tok.kind == Genshi.TT_UINT:
            self.__op_stack.push(int(self.__tok.lexeme))
            self.__consume()  # integer literal

        elif self.__tok.kind == Genshi.TT_UFLOAT:
            self.__op_stack.push(float(self.__tok.lexeme))
            self.__consume()  # floating point literal

        elif self.__tok.kind == Genshi.TT_IDENTIFIER:
            var = self.__tok.lexeme

            if f'@{var}' in self.__symbols:
                self.__parse_factor_array()
            elif var in self.__symbols:
                self.__op_stack.push(self.__symbols[var])
            else:
                self.__raise(f"Variable '{var}' is undefined")
            self.__consume()  # identifier

        elif self.__tok.kind in self.BIF_DICT:
            self.__op_stack(self.BIF_DICT[self.__tok.kind](self))

        elif self.__tok.kind == Genshi.SYM_LPAREN:
            raise NotImplementedError('factor => GROUPS!!')  # TODO:

        else:
            self.__raise('Unexpected value for factor', RuntimeError)

    # parse factor as an array element
    def __parse_factor_array(self):
        var = f'@{self.__token.lexeme}'
        self.__consume()                                 # MYARR
        self.__assert_syntax(Genshi.SYM_LPAREN)
        self.__consume()                                 # (
        indices = self.__parse_list([Genshi.SYM_COMMA])  #   I,J,K
        self.__assert_syntax(Genshi.SYM_RPAREN)
        self.__consume()                                 # )
        elem = self.__get_arr_elem(self.__symbols[var], indices)
        self.__op_stack.push(elem)

    # get element from array based on 1-3 indices
    def __get_arr_elem(self, arr, indices):
        dims = len(indices)
        if dims != self.__get_arr_dim(arr):
            self.__raise(f'Array dimension mismatch', RuntimeError)
        try:
            if dims == 1:
                return arr[indices[0]]
            elif dims == 2:
                return arr[indices[0]][indices[1]]
            elif dims == 3:
                return arr[indices[0]][indices[1]][indices[2]]
        except IndexError as e:
            self.__raise(f'Array index out of bounds', e)

    # get dimension of array
    def __get_arr_dim(self, arr):
        if not type(arr) == list:
            return []
        return [len(arr)] + self.__get_arr_dim(arr[0])
        # TODO: check if jagged arrays are a thing ?

    # parse a logical expression (AND,OR,XOR,NOT)
    def __parse_expr_logic(self):
        if self.__tok.kind == Genshi.KW_NOT:
            self.__parse_not()
        else:
            self.__parse_expr_rel()

        while self.__tok.kind in [Genshi.KW_AND, Genshi.KW_OR, Genshi.KW_XOR]:
            op = self.__tok.kind
            self.__consume()  #  AND  OR  XOR

            if self.__tok.kind == Genshi.KW_NOT:
                self.__parse_not()
            else:
                self.__parse_expr_rel()
            (r, l) = self.__pop_two()

            if op == Genshi.KW_AND:
                val = l and r
            elif op == Genshi.KW_OR:
                val = l or r
            else:
                val = l ^ r
            self.__op_stack.push(val)
    
    # parse a relational expression
    def __parse_expr_rel(self):
        self.__parse_expr()

        if self.__is_rel_op(self.__tok.kind):
            op = self.__tok.kind
            self.__consume()  #  >  <  >=  <=  =  <>
            self.__parse_expr()
            (r, l) = self.__pop_two()

            if op == Genshi.SYM_LT:
                val = l < r
            elif op == Genshi.SYM_LE:
                val = l <= r
            elif op == Genshi.SYM_EQ:
                val = l == r
            elif op == Genshi.SYM_GE:
                val = l >= r
            elif op == Genshi.SYM_GT:
                val = l > r
            elif op == Genshi.SYM_NE:
                val = l != r
            self.__op_stack.push(val)

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
        self.__consume()  # LET
        self.__parse_assign()

    # parse logical NOT
    def __parse_not(self):
        self.__consume()  # NOT
        self.__parse_expr_rel()
        self.__op_stack.push(not self.__op_stack.pop())

    # parse print to screen
    def __parse_print(self):
        self.__consume()  # PRINT
        if not self.__idx >= len(self.__tokens):
            # TODO: refactor
            self.__parse_expr_logic()
            print(self.__op_stack.pop, end='')

            #  use additional zone(s) => PRINT A,B,5
            while self.__tok.kind in [Genshi.SYM_COMMA, Genshi.SYM_SEMICOLON]:
                self.__consume()  #  ,  ;
                self.__parse_expr_logic()
                print(self.__op_stack.pop, end='')
        print('')

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
