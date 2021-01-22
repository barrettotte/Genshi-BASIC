# "header" file containing definitions for Genshi BASIC

class Genshi:

    # Token types
    TT_STRING     = 0
    TT_UINT       = 1
    TT_UFLOAT     = 2
    TT_IDENTIFIER = 3

    # Keywords
    KW_ABS    = 10   # absolute value
    KW_AND    = 11   # boolean AND
    KW_ASC    = 12   # convert char to ASCII value
    KW_ATN    = 13   # arc tangent
    KW_CHR    = 14   # convert number (0-255) to ASCII char
    KW_COS    = 15   # cosine
    KW_DATA   = 16   # store constants in code, pair with READ
    KW_DIM    = 17   # allocate memory for new array
    KW_END    = 18   # end of program
    KW_EXP    = 19   # inverse natural log (e^x)
    KW_FOR    = 20  # for loop start
    KW_GOSUB  = 21  # enter subroutine
    KW_GOTO   = 22  # go to line number
    KW_IF     = 23  # if statement
    KW_INPUT  = 24  # accept user input
    KW_INT    = 25  # round numbers
    KW_LEFT   = 26  # substring starting at left
    KW_LEN    = 27  # length of string
    KW_LET    = 28  # variable declaration
    KW_LIST   = 29  # display current program
    KW_LOAD   = 30  # load file
    KW_LOG    = 31  # natural logarithm
    KW_MID    = 32  # substring
    KW_NEW    = 33  # release all memory
    KW_NEXT   = 34  # end for loop block
    KW_NOT    = 35  # boolean NOT
    KW_ON     = 36  # go to line number in list given index
    KW_OR     = 37  # boolean OR 
    KW_PRINT  = 38  # print
    KW_READ   = 39  # read constants from DATA
    KW_REM    = 40  # comment (remark)
    KW_RETURN = 41  # return from subroutine, used with GOSUB
    KW_RIGHT  = 42  # substring starting at right
    KW_RND    = 43  # random float
    KW_RUN    = 44  # starts BASIC program
    KW_SAVE   = 45  # saves BASIC program to disk
    KW_SGN    = 46  # negative=-1, zero=0, positive=1
    KW_SIN    = 47  # sine
    KW_SPC    = 48  # whitespaces
    KW_SQR    = 49  # square root
    KW_STEP   = 50  # increment of FOR loop
    KW_STOP   = 51  # stops BASIC program
    KW_STR    = 52  # convert number to string
    KW_TAN    = 53  # tangent
    KW_THEN   = 54  # IF..THEN
    KW_TO     = 55  # FOR loop
    KW_XOR    = 56  # Boolean XOR

    # Symbols (operators or additional syntax)
    SYM_ADD       = 70
    SYM_SUB       = 71
    SYM_MUL       = 72
    SYM_DIV       = 73
    SYM_MOD       = 74
    SYM_LT        = 75
    SYM_GT        = 76
    SYM_LE        = 77
    SYM_GE        = 78
    SYM_NE        = 79
    SYM_EQ        = 80
    SYM_LPAREN    = 81
    SYM_RPAREN    = 82
    SYM_COMMA     = 83
    SYM_COLON     = 84
    SYM_SEMICOLON = 85
    SYM_NEWLINE   = 86

    # Keyword lookup table
    KEYWORDS = {
        'ABS':  KW_ABS, 'AND': KW_AND, 'ASC': KW_ASC, 'ATN': KW_ATN,   
        'CHR$': KW_CHR, 'COS': KW_COS, 'DATA': KW_DATA, 'DIM': KW_DIM,   
        'END':  KW_END, 'EXP': KW_EXP, 'FOR': KW_FOR, 'GOSUB': KW_GOSUB, 
        'GOTO': KW_GOTO, 'IF':  KW_IF, 'INPUT': KW_INPUT, 'INT': KW_INT,   
        'LEFT$': KW_LEFT, 'LEN': KW_LEN, 'LET': KW_LET, 'LIST': KW_LIST,  
        'LOAD': KW_LOAD, 'LOG': KW_LOG, 'MID$': KW_MID, 'NEW': KW_NEW, 
        'NEXT': KW_NEXT, 'NOT': KW_NOT, 'ON': KW_ON, 'OR': KW_OR, 
        'PRINT': KW_PRINT, 'READ': KW_READ, 'REM': KW_REM, 'RETURN': KW_RETURN, 
        'RIGHT$': KW_RIGHT, 'RND': KW_RND, 'RUN': KW_RUN, 'SAVE': KW_SAVE, 
        'SGN': KW_SGN, 'SIN': KW_SIN, 'SPC': KW_SPC, 'SQR': KW_SQR, 
        'STEP': KW_STEP, 'STOP': KW_STOP, 'STR$': KW_STR, 'TAN': KW_TAN, 
        'THEN': KW_THEN, 'TO': KW_TO, 'XOR': KW_XOR
    }

    # Symbol lookup table
    SYMBOLS = {
        '+': SYM_ADD, '-': SYM_SUB, '*': SYM_MUL, '/': SYM_DIV,
        '%': SYM_MOD, '<': SYM_LT, '>': SYM_GT, '<=': SYM_LE, 
        '>=': SYM_GE, '<>': SYM_NE, '=': SYM_EQ, '(': SYM_LPAREN,
        ')': SYM_RPAREN, ',': SYM_COMMA, ':': SYM_COLON, ';': SYM_SEMICOLON,
        '\n': SYM_NEWLINE
    }
