# GenshiBASIC Interpreting Process


Process example using ```programs/test.bas```



## Get source code as string ```GenshiBASIC.py```
```
1  DEF FN FTEST(X) = X*3
2  PRINT FN FTEST(4)
4  LET A4 = 2
5  PRINT "REPLACE ME"
6  LET A$=14
7  LET B$=-4
8  PRINT (-4+5) - (6/3) *8
10 FOR NI = 1 TO 5 STEP .5
20   PRINT NI,
30   FOR NJ = 1 TO 3
32      FOR NK = 3 TO 1 STEP -1
35        PRINT NI,NJ,NK
37      ENDFOR
40   ENDFOR
50 ENDFOR
55 IF A4 > 1 THEN PRINT "HELLO"
5  PRINT "HELLO GENSHI BASIC"
```



## Break source code into dictionary of lexemes ```Lexer.py```
``` Python
OrderedDict([
  ('1', ['DEF', 'FN', 'FTEST', '(', 'X', ')', '=', 'X', '*', '3']), 
  ('2', ['PRINT', 'FN', 'FTEST', '(', '4', ')']), 
  ('4', ['LET', 'A4', '=', '2']), 
  ('5', ['PRINT', '"', 'HELLO', 'GENSHI', 'BASIC', '"']), 
  ('6', ['LET', 'A$', '=', '14']), 
  ('7', ['LET', 'B$', '=', '-', '4']), 
  ('8', ['PRINT', '(', '-', '4', '+', '5', ')', '-', '(', '6', '/', '3', ')', '*', '8']), 
  ('10', ['FOR', 'NI', '=', '1', 'TO', '5', 'STEP', '.', '5']), 
  ('20', ['PRINT', 'NI', ',']), 
  ('30', ['FOR', 'NJ', '=', '1', 'TO', '3']), 
  ('32', ['FOR', 'NK', '=', '3', 'TO', '1', 'STEP', '-', '1']), 
  ('35', ['PRINT', 'NI', ',', 'NJ', ',', 'NK']), 
  ('37', ['ENDFOR']), 
  ('40', ['ENDFOR']), 
  ('50', ['ENDFOR']), 
  ('55', ['IF', 'A4', '>', '1', 'THEN', 'PRINT', '"', 'HELLO', '"'])])
```



## Create dictionary of tokens based on lexemes ```Lexer.py```
```python
1
  {'type': 'FUNC-DEF', 'lexeme': 'DEF', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'FUNCTION', 'lexeme': 'FN', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'FTEST', 'literal': 'IDENTIFIER', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'LEFT_PAREN', 'lexeme': '(', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'X', 'literal': 'IDENTIFIER', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'RIGHT_PAREN', 'lexeme': ')', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'X', 'literal': 'IDENTIFIER', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '*', 'literal': 'None', 'line': '1', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '3', 'literal': 'NUMERIC', 'line': '1', 'pos': '(0, 0)'}
2
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '2', 'pos': '(0, 0)'}
  {'type': 'FUNCTION', 'lexeme': 'FN', 'literal': 'None', 'line': '2', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'FTEST', 'literal': 'IDENTIFIER', 'line': '2', 'pos': '(0, 0)'}
  {'type': 'LEFT_PAREN', 'lexeme': '(', 'literal': 'None', 'line': '2', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '4', 'literal': 'NUMERIC', 'line': '2', 'pos': '(0, 0)'}
  {'type': 'RIGHT_PAREN', 'lexeme': ')', 'literal': 'None', 'line': '2', 'pos': '(0, 0)'}
4
  {'type': 'VAR-DEF', 'lexeme': 'LET', 'literal': 'None', 'line': '4', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'A4', 'literal': 'IDENTIFIER', 'line': '4', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '4', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '2', 'literal': 'NUMERIC', 'line': '4', 'pos': '(0, 0)'}
5
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '5', 'pos': '(0, 0)'}
  {'type': 'QUOTATION', 'lexeme': '"', 'literal': 'None', 'line': '5', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'HELLO', 'literal': 'STRING', 'line': '5', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'GENSHI', 'literal': 'STRING', 'line': '5', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'BASIC', 'literal': 'STRING', 'line': '5', 'pos': '(0, 0)'}
  {'type': 'QUOTATION', 'lexeme': '"', 'literal': 'None', 'line': '5', 'pos': '(0, 0)'}
6
  {'type': 'VAR-DEF', 'lexeme': 'LET', 'literal': 'None', 'line': '6', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'A$', 'literal': 'IDENTIFIER', 'line': '6', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '6', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '14', 'literal': 'NUMERIC', 'line': '6', 'pos': '(0, 0)'}
7
  {'type': 'VAR-DEF', 'lexeme': 'LET', 'literal': 'None', 'line': '7', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'B$', 'literal': 'IDENTIFIER', 'line': '7', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '7', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '-', 'literal': 'None', 'line': '7', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '4', 'literal': 'NUMERIC', 'line': '7', 'pos': '(0, 0)'}
8
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LEFT_PAREN', 'lexeme': '(', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '-', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '4', 'literal': 'NUMERIC', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '+', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '5', 'literal': 'NUMERIC', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'RIGHT_PAREN', 'lexeme': ')', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '-', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LEFT_PAREN', 'lexeme': '(', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '6', 'literal': 'NUMERIC', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '/', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '3', 'literal': 'NUMERIC', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'RIGHT_PAREN', 'lexeme': ')', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '*', 'literal': 'None', 'line': '8', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '8', 'literal': 'NUMERIC', 'line': '8', 'pos': '(0, 0)'}
10
  {'type': 'FOR-START', 'lexeme': 'FOR', 'literal': 'None', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NI', 'literal': 'IDENTIFIER', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '1', 'literal': 'NUMERIC', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'FOR-DEF', 'lexeme': 'TO', 'literal': 'None', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '5', 'literal': 'NUMERIC', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'FOR-DEF', 'lexeme': 'STEP', 'literal': 'None', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'PERIOD', 'lexeme': '.', 'literal': 'None', 'line': '10', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '5', 'literal': 'NUMERIC', 'line': '10', 'pos': '(0, 0)'}
20
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '20', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NI', 'literal': 'IDENTIFIER', 'line': '20', 'pos': '(0, 0)'}
  {'type': 'COMMA', 'lexeme': ',', 'literal': 'None', 'line': '20', 'pos': '(0, 0)'}
30
  {'type': 'FOR-START', 'lexeme': 'FOR', 'literal': 'None', 'line': '30', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NJ', 'literal': 'IDENTIFIER', 'line': '30', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '30', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '1', 'literal': 'NUMERIC', 'line': '30', 'pos': '(0, 0)'}
  {'type': 'FOR-DEF', 'lexeme': 'TO', 'literal': 'None', 'line': '30', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '3', 'literal': 'NUMERIC', 'line': '30', 'pos': '(0, 0)'}
32
  {'type': 'FOR-START', 'lexeme': 'FOR', 'literal': 'None', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NK', 'literal': 'IDENTIFIER', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'EQUALS', 'lexeme': '=', 'literal': 'None', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '3', 'literal': 'NUMERIC', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'FOR-DEF', 'lexeme': 'TO', 'literal': 'None', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '1', 'literal': 'NUMERIC', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'FOR-DEF', 'lexeme': 'STEP', 'literal': 'None', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '-', 'literal': 'None', 'line': '32', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '1', 'literal': 'NUMERIC', 'line': '32', 'pos': '(0, 0)'}
35
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '35', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NI', 'literal': 'IDENTIFIER', 'line': '35', 'pos': '(0, 0)'}
  {'type': 'COMMA', 'lexeme': ',', 'literal': 'None', 'line': '35', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NJ', 'literal': 'IDENTIFIER', 'line': '35', 'pos': '(0, 0)'}
  {'type': 'COMMA', 'lexeme': ',', 'literal': 'None', 'line': '35', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'NK', 'literal': 'IDENTIFIER', 'line': '35', 'pos': '(0, 0)'}
37
  {'type': 'FOR-END', 'lexeme': 'ENDFOR', 'literal': 'None', 'line': '37', 'pos': '(0, 0)'}
40
  {'type': 'FOR-END', 'lexeme': 'ENDFOR', 'literal': 'None', 'line': '40', 'pos': '(0, 0)'}
50
  {'type': 'FOR-END', 'lexeme': 'ENDFOR', 'literal': 'None', 'line': '50', 'pos': '(0, 0)'}
55
  {'type': 'IF-DEF', 'lexeme': 'IF', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'A4', 'literal': 'IDENTIFIER', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'BINARY', 'lexeme': '>', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': '1', 'literal': 'NUMERIC', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'IF-DEF', 'lexeme': 'THEN', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'NO-PARAM', 'lexeme': 'PRINT', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'QUOTATION', 'lexeme': '"', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'LITERAL', 'lexeme': 'HELLO', 'literal': 'STRING', 'line': '55', 'pos': '(0, 0)'}
  {'type': 'QUOTATION', 'lexeme': '"', 'literal': 'None', 'line': '55', 'pos': '(0, 0)'}
```



## Build node tree ```Parser.py```
```
type: ROOT           content:            level: -1    line: -1 children: Node[63]
  type: FUNC-DEF       content: DEF        level: 0    line: 1 children: Node[0]
  type: FUNCTION       content: FN         level: 0    line: 1 children: Node[0]
  type: LITERAL        content: FTEST      level: 0    line: 1 children: Node[0]
  type: LEFT_PAREN     content: (          level: 0    line: 1 children: Node[0]
  type: LITERAL        content: X          level: 0    line: 1 children: Node[0]
  type: RIGHT_PAREN    content: )          level: 0    line: 1 children: Node[0]
  type: EQUALS         content: =          level: 0    line: 1 children: Node[0]
  type: LITERAL        content: X          level: 0    line: 1 children: Node[0]
  type: BINARY         content: *          level: 0    line: 1 children: Node[0]
  type: LITERAL        content: 3          level: 0    line: 1 children: Node[0]
  type: NO-PARAM       content: PRINT      level: 0    line: 2 children: Node[0]
  type: FUNCTION       content: FN         level: 0    line: 2 children: Node[0]
  type: LITERAL        content: FTEST      level: 0    line: 2 children: Node[0]
  type: LEFT_PAREN     content: (          level: 0    line: 2 children: Node[0]
  type: LITERAL        content: 4          level: 0    line: 2 children: Node[0]
  type: RIGHT_PAREN    content: )          level: 0    line: 2 children: Node[0]
  type: VAR-DEF        content: LET        level: 0    line: 4 children: Node[0]
  type: LITERAL        content: A4         level: 0    line: 4 children: Node[0]
  type: EQUALS         content: =          level: 0    line: 4 children: Node[0]
  type: LITERAL        content: 2          level: 0    line: 4 children: Node[0]
  type: NO-PARAM       content: PRINT      level: 0    line: 5 children: Node[0]
  type: QUOTATION      content: "          level: 0    line: 5 children: Node[0]
  type: LITERAL        content: HELLO      level: 0    line: 5 children: Node[0]
  type: LITERAL        content: GENSHI     level: 0    line: 5 children: Node[0]
  type: LITERAL        content: BASIC      level: 0    line: 5 children: Node[0]
  type: QUOTATION      content: "          level: 0    line: 5 children: Node[0]
  type: VAR-DEF        content: LET        level: 0    line: 6 children: Node[0]
  type: LITERAL        content: A$         level: 0    line: 6 children: Node[0]
  type: EQUALS         content: =          level: 0    line: 6 children: Node[0]
  type: LITERAL        content: 14         level: 0    line: 6 children: Node[0]
  type: VAR-DEF        content: LET        level: 0    line: 7 children: Node[0]
  type: LITERAL        content: B$         level: 0    line: 7 children: Node[0]
  type: EQUALS         content: =          level: 0    line: 7 children: Node[0]
  type: BINARY         content: -          level: 0    line: 7 children: Node[0]
  type: LITERAL        content: 4          level: 0    line: 7 children: Node[0]
  type: NO-PARAM       content: PRINT      level: 0    line: 8 children: Node[0]
  type: LEFT_PAREN     content: (          level: 0    line: 8 children: Node[0]
  type: BINARY         content: -          level: 0    line: 8 children: Node[0]
  type: LITERAL        content: 4          level: 0    line: 8 children: Node[0]
  type: BINARY         content: +          level: 0    line: 8 children: Node[0]
  type: LITERAL        content: 5          level: 0    line: 8 children: Node[0]
  type: RIGHT_PAREN    content: )          level: 0    line: 8 children: Node[0]
  type: BINARY         content: -          level: 0    line: 8 children: Node[0]
  type: LEFT_PAREN     content: (          level: 0    line: 8 children: Node[0]
  type: LITERAL        content: 6          level: 0    line: 8 children: Node[0]
  type: BINARY         content: /          level: 0    line: 8 children: Node[0]
  type: LITERAL        content: 3          level: 0    line: 8 children: Node[0]
  type: RIGHT_PAREN    content: )          level: 0    line: 8 children: Node[0]
  type: BINARY         content: *          level: 0    line: 8 children: Node[0]
  type: LITERAL        content: 8          level: 0    line: 8 children: Node[0]
  type: FOR-START      content: FOR        level: 0    line: 10 children: Node[12]
    type: LITERAL        content: NI         level: 1    line: 10 children: Node[0]
    type: EQUALS         content: =          level: 1    line: 10 children: Node[0]
    type: LITERAL        content: 1          level: 1    line: 10 children: Node[0]
    type: FOR-DEF        content: TO         level: 1    line: 10 children: Node[0]
    type: LITERAL        content: 5          level: 1    line: 10 children: Node[0]
    type: FOR-DEF        content: STEP       level: 1    line: 10 children: Node[0]
    type: PERIOD         content: .          level: 1    line: 10 children: Node[0]
    type: LITERAL        content: 5          level: 1    line: 10 children: Node[0]
    type: NO-PARAM       content: PRINT      level: 1    line: 20 children: Node[0]
    type: LITERAL        content: NI         level: 1    line: 20 children: Node[0]
    type: COMMA          content: ,          level: 1    line: 20 children: Node[0]
    type: FOR-START      content: FOR        level: 1    line: 30 children: Node[6]
      type: LITERAL        content: NJ         level: 2    line: 30 children: Node[0]
      type: EQUALS         content: =          level: 2    line: 30 children: Node[0]
      type: LITERAL        content: 1          level: 2    line: 30 children: Node[0]
      type: FOR-DEF        content: TO         level: 2    line: 30 children: Node[0]
      type: LITERAL        content: 3          level: 2    line: 30 children: Node[0]
      type: FOR-START      content: FOR        level: 2    line: 32 children: Node[14]
        type: LITERAL        content: NK         level: 3    line: 32 children: Node[0]
        type: EQUALS         content: =          level: 3    line: 32 children: Node[0]
        type: LITERAL        content: 3          level: 3    line: 32 children: Node[0]
        type: FOR-DEF        content: TO         level: 3    line: 32 children: Node[0]
        type: LITERAL        content: 1          level: 3    line: 32 children: Node[0]
        type: FOR-DEF        content: STEP       level: 3    line: 32 children: Node[0]
        type: BINARY         content: -          level: 3    line: 32 children: Node[0]
        type: LITERAL        content: 1          level: 3    line: 32 children: Node[0]
        type: NO-PARAM       content: PRINT      level: 3    line: 35 children: Node[0]
        type: LITERAL        content: NI         level: 3    line: 35 children: Node[0]
        type: COMMA          content: ,          level: 3    line: 35 children: Node[0]
        type: LITERAL        content: NJ         level: 3    line: 35 children: Node[0]
        type: COMMA          content: ,          level: 3    line: 35 children: Node[0]
        type: LITERAL        content: NK         level: 3    line: 35 children: Node[0]
      type: FOR-END        content: ENDFOR      level: 2    line: 37 children: Node[0]
    type: FOR-END        content: ENDFOR      level: 1    line: 40 children: Node[0]
  type: FOR-END        content: ENDFOR      level: 0    line: 50 children: Node[0]
  type: IF-DEF         content: IF         level: 0    line: 55 children: Node[0]
  type: LITERAL        content: A4         level: 0    line: 55 children: Node[0]
  type: BINARY         content: >          level: 0    line: 55 children: Node[0]
  type: LITERAL        content: 1          level: 0    line: 55 children: Node[0]
  type: IF-DEF         content: THEN       level: 0    line: 55 children: Node[0]
  type: NO-PARAM       content: PRINT      level: 0    line: 55 children: Node[0]
  type: QUOTATION      content: "          level: 0    line: 55 children: Node[0]
  type: LITERAL        content: HELLO      level: 0    line: 55 children: Node[0]
  type: QUOTATION      content: "          level: 0    line: 55 children: Node[0]
```