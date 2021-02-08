# "header" file containing definitions for Genshi BASIC

class Genshi():

    # Parser states - used for program flow
    STATE_NORMAL = 0
    STATE_HALT = 1
    STATE_GOTO = 3
    STATE_LOOP_START = 4
    STATE_LOOP_NORMAL = 5
    STATE_LOOP_DONE = 6
    STATE_GOSUB = 7
    STATE_RETURN = 8

    # Token types
    TT_STRING = 0
    TT_UINT = 1
    TT_UFLOAT = 2
    TT_IDENTIFIER = 3

    # Keywords
    KW_ABS = 10     # absolute value
    KW_AND = 11     # logical AND
    KW_ASC = 12     # convert char to ASCII value
    KW_ATN = 13     # arc tangent
    KW_CHR = 14     # convert number (0-255) to ASCII char
    KW_COS = 15     # cosine
    KW_DATA = 16    # store constants in code, pair with READ
    KW_DIM = 17     # allocate memory for new array
    KW_ELSE = 18    # optional else for if statement
    KW_END = 19     # end of program
    KW_EXP = 20     # inverse natural log (e^x)
    KW_FOR = 21     # for loop start
    KW_GOSUB = 22   # enter subroutine
    KW_GOTO = 23    # go to line number
    KW_IF = 24      # if statement
    KW_INPUT = 25   # accept user input
    KW_INT = 26     # round numbers
    KW_LEFT = 27    # substring starting at left
    KW_LEN = 28     # length of string
    KW_LET = 29     # variable declaration
    KW_LOG = 30     # natural logarithm
    KW_MID = 31     # substring
    KW_NEXT = 32    # end for loop block
    KW_NOT = 33     # logical NOT
    KW_ON = 34      # go to line number in list given index
    KW_OR = 35      # logical OR
    KW_PRINT = 36   # print
    KW_READ = 37    # read constants from DATA
    KW_REM = 38     # comment (remark)
    KW_RETURN = 39  # return from subroutine, used with GOSUB
    KW_RIGHT = 40   # substring starting at right
    KW_RND = 41     # random float
    KW_SGN = 42     # negative=-1, zero=0, positive=1
    KW_SIN = 43     # sine
    KW_SPC = 44     # whitespaces
    KW_SQR = 45     # square root
    KW_STEP = 46    # increment of FOR loop
    KW_STR = 47     # convert number to string
    KW_TAN = 48     # tangent
    KW_THEN = 49    # IF..THEN
    KW_TO = 50      # FOR loop
    KW_XOR = 51     # logical XOR

    # Symbols (operators or additional syntax)
    SYM_ADD = 70
    SYM_SUB = 71
    SYM_MUL = 72
    SYM_DIV = 73
    SYM_MOD = 74
    SYM_LT = 75
    SYM_GT = 76
    SYM_LE = 77
    SYM_GE = 78
    SYM_NE = 79
    SYM_EQ = 80
    SYM_LPAREN = 81
    SYM_RPAREN = 82
    SYM_COMMA = 83
    SYM_COLON = 84
    SYM_SEMICOLON = 85
    SYM_NEWLINE = 86

    # Keyword lookup table
    KEYWORDS = {
        'ABS':  KW_ABS, 'AND': KW_AND, 'ASC': KW_ASC, 'ATN': KW_ATN,
        'CHR': KW_CHR, 'COS': KW_COS, 'DATA': KW_DATA, 'DIM': KW_DIM,
        'END':  KW_END, 'EXP': KW_EXP, 'FOR': KW_FOR, 'GOSUB': KW_GOSUB,
        'GOTO': KW_GOTO, 'IF':  KW_IF, 'INPUT': KW_INPUT, 'INT': KW_INT,
        'LEFT': KW_LEFT, 'LEN': KW_LEN, 'LET': KW_LET, 'LOG': KW_LOG,
        'MID': KW_MID, 'NEXT': KW_NEXT, 'NOT': KW_NOT, 'ON': KW_ON,
        'OR': KW_OR, 'PRINT': KW_PRINT, 'READ': KW_READ, 'REM': KW_REM,
        'RETURN': KW_RETURN, 'RIGHT': KW_RIGHT, 'RND': KW_RND, 'SGN': KW_SGN,
        'SIN': KW_SIN, 'SPC': KW_SPC, 'SQR': KW_SQR, 'STEP': KW_STEP,
        'STR': KW_STR, 'TAN': KW_TAN, 'THEN': KW_THEN, 'TO': KW_TO,
        'XOR': KW_XOR
    }

    # Symbol lookup table
    SYMBOLS = {
        '+': SYM_ADD, '-': SYM_SUB, '*': SYM_MUL, '/': SYM_DIV,
        '%': SYM_MOD, '<': SYM_LT, '>': SYM_GT, '<=': SYM_LE,
        '>=': SYM_GE, '<>': SYM_NE, '=': SYM_EQ, '(': SYM_LPAREN,
        ')': SYM_RPAREN, ',': SYM_COMMA, ':': SYM_COLON, ';': SYM_SEMICOLON,
        '\n': SYM_NEWLINE
    }
