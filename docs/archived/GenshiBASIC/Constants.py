COL_LEN = 64
MAX_LINES = 65536

OPERATORS = [ 
    { "char": "+",  "type": "BINARY" },
    { "char": "-",  "type": "UNARY" },
    { "char": "/",  "type": "BINARY" },
    { "char": "*",  "type": "BINARY" },
    { "char": "^",  "type": "BINARY" },
    { "char": "%",  "type": "BINARY" },
    { "char": "=",  "type": "EQUALS" },
]

PUNCTUATION = [ 
    { "char": "(",  "type": "LEFT_PAREN"  },
    { "char": ")",  "type": "RIGHT_PAREN" },
    { "char": "\"", "type": "QUOTATION"   },
    { "char": ",",  "type": "COMMA"       },
   #{ "char": ";",  "type": "SEMICOLON"   },
   #{ "char": ":",  "type": "COLON"       },
]

KEYWORDS = [
    { "word": "ABS",    "type": "ONE-PARAM"   }, # DONE
    { "word": "AND",    "type": "BINARY"      }, # DONE
    { "word": "ASC",    "type": "ONE-PARAM"   }, # DONE
    { "word": "BIN$",   "type": "ONE-PARAM"   }, # DONE
    { "word": "CAT$",   "type": "TWO-PARAM"   }, # DONE
    { "word": "CHR$",   "type": "ONE-PARAM"   }, # DONE
    { "word": "CLR",    "type": "NO-PARAM"    }, # DONE
    { "word": "COS",    "type": "ONE-PARAM"   }, # DONE
    { "word": "DEF",    "type": "FUNC-DEC"    }, # DONE
    { "word": "DIM",    "type": "ARR-DEC"     },
    { "word": "END",    "type": "NO-PARAM"    }, # DONE
    { "word": "EQ",     "type": "BINARY"      }, # DONE
    { "word": "EXP",    "type": "ONE-PARAM"   }, # DONE
    { "word": "FN",     "type": "FUNCTION"    }, # DONE
    { "word": "FOR",    "type": "FOR-DEF"     },
    { "word": "GE",     "type": "BINARY"      }, # DONE
    { "word": "GOSUB",  "type": "GO-DEF"      },
    { "word": "GOTO",   "type": "GO-DEF"      }, # DONE
    { "word": "GT",     "type": "BINARY"      }, # DONE
    { "word": "HEX$",   "type": "ONE-PARAM"   }, # DONE
    { "word": "IF",     "type": "IF-DEF"      }, # DONE
    { "word": "INT",    "type": "ONE-PARAM"   }, # DONE
    { "word": "LE",     "type": "BINARY"      }, # DONE
    { "word": "LEFT$",  "type": "TWO-PARAM"   }, # DONE
    { "word": "LEN",    "type": "ONE-PARAM"   }, # DONE
    { "word": "LET",    "type": "VAR-DEC"     }, # DONE
    { "word": "LT",     "type": "BINARY"      }, # DONE
    { "word": "LOG",    "type": "ONE-PARAM"   }, # DONE
    { "word": "MID$",   "type": "THREE-PARAM" }, # DONE
    { "word": "ENDFOR", "type": "FOR-END"     },
    { "word": "NE",     "type": "BINARY"      }, # DONE
    { "word": "NOT",    "type": "UNARY"       }, # DONE
    { "word": "OR",     "type": "BINARY"      }, # DONE
    { "word": "PI",     "type": "ONE-PARAM"   }, # DONE
    { "word": "PRINT",  "type": "PRINT"       }, # DONE
    { "word": "PRINTL", "type": "PRINT"       }, # DONE
    { "word": "REM",    "type": "COMMENT"     }, # DONE
    { "word": "RETURN", "type": "NO-PARAM"    },
    { "word": "RIGHT$", "type": "TWO-PARAM"   }, # DONE
    { "word": "RND",    "type": "ONE-PARAM"   }, # DONE
    { "word": "SGN",    "type": "ONE-PARAM"   }, # DONE
    { "word": "SIN",    "type": "ONE-PARAM"   }, # DONE
    { "word": "SPC$",   "type": "ONE-PARAM"   }, # DONE
    { "word": "SQR",    "type": "ONE-PARAM"   }, # DONE
    { "word": "STEP",   "type": "FOR-STEP"    },
    { "word": "STR$",   "type": "ONE-PARAM"   }, # DONE
    { "word": "TAN",    "type": "ONE-PARAM"   }, # DONE
    { "word": "THEN",   "type": "THEN"        }, # DONE
    { "word": "TO",     "type": "FOR-TO"      },
    { "word": "XOR",    "type": "BINARY"      }  # DONE
]

GRAMMAR_RULES = { 
  "ARR-DEC":      ["IDENTIFIER", "ARGUMENTS"],
  "FOR-DEF":      ["IDENTIFIER", "EQUALS", "EXPRESSION", "FOR-TO", "EXPRESSION", "FOR-STEP", "EXPRESSION"],
  "FOR-END":      [],
  "NO-PARAM":     [],
  "ONE-PARAM":    ["ARGUMENTS"],
  "TWO-PARAM":    ["ARGUMENTS"],
  "THREE-PARAM":  ["ARGUMENTS"],
  "FUNC-DEC":     ["FUNCTION", "IDENTIFIER", "LEFT_PAREN", "PARAMETERS", "RIGHT_PAREN", "EQUALS", "EXPRESSION"],
  "GO-DEF":       ["EXPRESSION"],
  "VAR-DEC":      ["IDENTIFIER", "EQUALS", "EXPRESSION"],
  "IDENTIFIER":   {
                    "EQUALS":     ["EXPRESSION"],
                    "LEFT_PAREN": ["ARGUMENTS"],
                  },
  "IF-DEF":       ["EXPRESSION", "THEN", "EXPRESSION"],
  "PRINT":        ["STRING"],
}

EXPRESSION_START = [
  "IDENTIFIER", "LITERAL", "LEFT_PAREN", "UNARY", "ONE-PARAM", "TWO-PARAM", "THREE-PARAM", 
  "NO-PARAM", "QUOTATION"
]

FUNCTION_RULES = {
  "ABS":    ["NUMERIC"],
  "ASC":    ["STRING"],
  "BIN$":   ["NUMERIC"],
  "CAT$":   ["ANY", "ANY"],
  "CHR$":   ["NUMERIC"],
  "CLR":    [],
  "COS":    ["NUMERIC"],
  "END":    [],
  "EXP":    ["NUMERIC"],
  "HEX$":   ["NUMERIC"],
  "INT":    ["NUMERIC"],
  "PI":     ["NUMERIC"],
  "LEFT$":  ["STRING", "NUMERIC"],
  "LEN":    ["STRING"],
  "LOG":    ["NUMERIC"],
  "MID$":   ["STRING", "NUMERIC", "NUMERIC"],
  "RIGHT$": ["STRING", "NUMERIC"],
  "RND":    ["NUMERIC"],
  "SIN":    ["NUMERIC"],
  "SGN":    ["NUMERIC"],
  "SPC$":   ["NUMERIC"],
  "SQR":    ["NUMERIC"],
  "STR$":   ["NUMERIC"],
  "TAN":    ["NUMERIC"],
}