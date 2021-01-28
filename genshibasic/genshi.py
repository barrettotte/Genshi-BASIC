# "header" file containing definitions for Genshi BASIC

class Genshi:

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
    KW_END = 18     # end of program
    KW_EXP = 19     # inverse natural log (e^x)
    KW_FOR = 20     # for loop start
    KW_GOSUB = 21   # enter subroutine
    KW_GOTO = 22    # go to line number
    KW_IF = 23      # if statement
    KW_INPUT = 24   # accept user input
    KW_INT = 25     # round numbers
    KW_LEFT = 26    # substring starting at left
    KW_LEN = 27     # length of string
    KW_LET = 28     # variable declaration
    KW_LOG = 29     # natural logarithm
    KW_MID = 30     # substring
    KW_NEXT = 31    # end for loop block
    KW_NOT = 32     # logical NOT
    KW_ON = 33      # go to line number in list given index
    KW_OR = 34      # logical OR
    KW_PRINT = 35   # print
    KW_READ = 36    # read constants from DATA
    KW_REM = 37     # comment (remark)
    KW_RETURN = 38  # return from subroutine, used with GOSUB
    KW_RIGHT = 39   # substring starting at right
    KW_RND = 40     # random float
    KW_SGN = 41     # negative=-1, zero=0, positive=1
    KW_SIN = 42     # sine
    KW_SPC = 43     # whitespaces
    KW_SQR = 44     # square root
    KW_STEP = 45    # increment of FOR loop
    KW_STR = 46     # convert number to string
    KW_TAN = 47     # tangent
    KW_THEN = 48    # IF..THEN
    KW_TO = 49      # FOR loop
    KW_XOR = 50     # logical XOR

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
