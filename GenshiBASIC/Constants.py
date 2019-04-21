COL_LEN = 40
MAX_LINES = 63999

OPERATORS = [ 
    { "char": "+",  "type": "BINARY" },
    { "char": "-",  "type": "BINARY" },
    { "char": "/",  "type": "BINARY" },
    { "char": "*",  "type": "BINARY" },
    { "char": "^",  "type": "BINARY" },
    { "char": "=",  "type": "EQUALS" },
    { "char": "<",  "type": "BINARY" },
    { "char": ">",  "type": "BINARY" },
    { "char": "<>", "type": "BINARY" },
    { "char": "<=", "type": "BINARY" },
    { "char": "=<", "type": "BINARY" },
    { "char": ">=", "type": "BINARY" },
    { "char": "=>", "type": "BINARY" }
]

PUNCTUATION = [ 
    { "char": "(",  "type": "LEFT_PAREN"  },
    { "char": ")",  "type": "RIGHT_PAREN" },
    { "char": ";",  "type": "SEMICOLON"   },
    { "char": ":",  "type": "COLON"       },
    { "char": ",",  "type": "COMMA"       },
    { "char": ".",  "type": "PERIOD"      },
    { "char": "\"", "type": "QUOTATION"   }
]

KEYWORDS = [
    { "word": "ABS",    "type": "ONE-PARAM"   },
    { "word": "AND",    "type": "OPERATOR"    },
    { "word": "ASC",    "type": "ONE-PARAM"   },
    { "word": "ATN",    "type": "ONE-PARAM"   },
    { "word": "CHR$",   "type": "ONE-PARAM"   },
    { "word": "CLR",    "type": "NO-PARAM"    },
    { "word": "COS",    "type": "ONE-PARAM"   },
    { "word": "DEF",    "type": "FUNCTION"    },
    { "word": "DIM",    "type": "VAR-DEF"     },
    { "word": "END",    "type": "NO-PARAM"    },
    { "word": "EXP",    "type": "ONE-PARAM"   },
    { "word": "FN",     "type": "FUNCTION"    },
    { "word": "FOR",    "type": "FOR-START"   },
    { "word": "GOSUB",  "type": "FLOW-CTRL"   },
    { "word": "GOTO",   "type": "FLOW-CTRL"   },
    { "word": "IF",     "type": "IF-DEF"      },
    { "word": "INT",    "type": "ONE-PARAM"   },
    { "word": "LEFT$",  "type": "TWO-PARAM"   },
    { "word": "LEN",    "type": "ONE-PARAM"   },
    { "word": "LET",    "type": "VAR-DEF"     },
    { "word": "LOG",    "type": "ONE-PARAM"   },
    { "word": "MOD",    "type": "OPERATOR"    },
    { "word": "MID$",   "type": "THREE-PARAM" },
    { "word": "ENDFOR", "type": "FOR-END"     },
    { "word": "NOT",    "type": "BOOLEAN"     },
    { "word": "OR",     "type": "OPERATOR"    },
    { "word": "PRINT",  "type": "NO-PARAM"    },
    { "word": "REM",    "type": "COMMENT"     },
    { "word": "RETURN", "type": "NO-PARAM"    },
    { "word": "RIGHT$", "type": "TWO-PARAM"   },
    { "word": "RND",    "type": "ONE-PARAM"   },
    { "word": "SGN",    "type": "ONE-PARAM"   },
    { "word": "SIN",    "type": "ONE-PARAM"   },
    { "word": "SPC",    "type": "ONE-PARAM"   },
    { "word": "SQR",    "type": "ONE-PARAM"   },
    { "word": "STEP",   "type": "FOR-DEF"     },
    { "word": "STR$",   "type": "ONE-PARAM"   },
    { "word": "TAB",    "type": "ONE-PARAM"   },
    { "word": "TAN",    "type": "ONE-PARAM"   },
    { "word": "THEN",   "type": "IF-DEF"      },
    { "word": "TO",     "type": "FOR-DEF"     },
    { "word": "XOR",    "type": "BOOLEAN"     }
]