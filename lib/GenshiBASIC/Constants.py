COL_LEN = 64
MAX_LINES = 65536

OPERATORS = [ 
    { "char": "+",  "type": "BINARY" },
    { "char": "-",  "type": "UNARY" },
    { "char": "/",  "type": "BINARY" },
    { "char": "*",  "type": "BINARY" },
    { "char": "^",  "type": "BINARY" },
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
    { "word": "ABS",    "type": "ONE-PARAM"   },
    { "word": "AND",    "type": "BINARY"      },
    { "word": "ASC",    "type": "ONE-PARAM"   },
    { "word": "ATN",    "type": "ONE-PARAM"   },
    { "word": "CHR$",   "type": "ONE-PARAM"   },
    { "word": "CLR",    "type": "NO-PARAM"    },
    { "word": "COS",    "type": "ONE-PARAM"   },
    { "word": "DEF",    "type": "FUNC-DEC"    },
    { "word": "DIM",    "type": "ARR-DEC"     },
    { "word": "END",    "type": "NO-PARAM"    },
    { "word": "EQ",     "type": "BINARY"      },
    { "word": "EXP",    "type": "ONE-PARAM"   },
    { "word": "FN",     "type": "FUNCTION"    },
    { "word": "FOR",    "type": "FOR-DEF"     },
    { "word": "GE",     "type": "BINARY"      },
    { "word": "GLUE",   "type": "TWO-PARAM"   },
    { "word": "GOSUB",  "type": "GO-DEF"      },
    { "word": "GOTO",   "type": "GO-DEF"      },
    { "word": "GT",     "type": "BINARY"      },
    { "word": "IF",     "type": "IF-DEF"      },
    { "word": "INT",    "type": "ONE-PARAM"   },
    { "word": "LE",     "type": "BINARY"      },
    { "word": "LEFT$",  "type": "TWO-PARAM"   },
    { "word": "LEN",    "type": "ONE-PARAM"   },
    { "word": "LET",    "type": "VAR-DEC"     },
    { "word": "LT",     "type": "BINARY"      },
    { "word": "LOG",    "type": "ONE-PARAM"   },
    { "word": "MOD",    "type": "BINARY"      },
    { "word": "MID$",   "type": "THREE-PARAM" },
    { "word": "ENDFOR", "type": "FOR-END"     },
    { "word": "NE",     "type": "BINARY"      },
    { "word": "NOT",    "type": "UNARY"       },
    { "word": "OR",     "type": "BINARY"      },
    { "word": "PRINT",  "type": "PRINT"       },
    { "word": "PRINTL", "type": "PRINT"       },
    { "word": "REM",    "type": "COMMENT"     },
    { "word": "RETURN", "type": "NO-PARAM"    },
    { "word": "RIGHT$", "type": "TWO-PARAM"   },
    { "word": "RND",    "type": "ONE-PARAM"   },
    { "word": "SGN",    "type": "ONE-PARAM"   },
    { "word": "SIN",    "type": "ONE-PARAM"   },
    { "word": "SPC",    "type": "ONE-PARAM"   },
    { "word": "SQR",    "type": "ONE-PARAM"   },
    { "word": "STEP",   "type": "FOR-STEP"    },
    { "word": "STR$",   "type": "ONE-PARAM"   },
    { "word": "TAB",    "type": "ONE-PARAM"   },
    { "word": "TAN",    "type": "ONE-PARAM"   },
    { "word": "THEN",   "type": "THEN"        },
    { "word": "TO",     "type": "FOR-TO"      },
    { "word": "XOR",    "type": "BINARY"      }
]

GRAMMAR_RULES = { 
  "ARR-DEC":      ["IDENTIFIER", "ARGUMENTS"],
  "FOR-DEF":      ["IDENTIFIER", "EQUALS", "EXPRESSION", "FOR-TO", "EXPRESSION", "FOR-STEP", "EXPRESSION"],
  "FOR-END":      [],
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
