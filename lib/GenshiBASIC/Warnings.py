import Constants as constants
import warnings


def raise_max_lines(line_len):
    s = "Genshi BASIC max lines reached. Lexer loaded " + str(line_len) + " line(s)."
    warnings.warn(s + "Additional lines will be ignored. Max=" + str(constants.MAX_LINES) + "\n", 
        SyntaxWarning, stacklevel=10
    )

def raise_col_len(line):
    s = "Genshi BASIC max column length reached for\n     " + line
    warnings.warn(s + "  Additional characters will be ignored. Max=" + str(constants.COL_LEN) + "\n", 
        SyntaxWarning, stacklevel=10
    )

def raise_missing_linenum(line):
    s = "Genshi BASIC detected missing line number for\n     " + line
    warnings.warn(s + "  Lexer will attempt to auto generate line number.\n", 
        SyntaxWarning, stacklevel=10
    )

def raise_file_extension(filepath):
    s = "Genshi BASIC detected mismatched file extension for " + filepath + "\n"
    warnings.warn(s + "Lexer will still try to run as normal. It is suggested to change file extension to '.bas'\n", 
        UserWarning, stacklevel=10
    )
