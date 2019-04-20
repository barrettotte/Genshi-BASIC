# GenshiBASIC Interpreting Process


## Get source code as string ```GenshiBASIC.py```
```
5       PRINT "HELLO WORLD"
10      REM COMPUTE FACTORIAL OF N
20      PRINT "N=";
30      N = 123
40      LET X=1
50      FOR I=1 TO N
60          LET X=X*I
70      NEXT I
80      PRINT "N=";N,"N!=";X
90      END
5       PRINT "FACTORIAL"
```


## Break source code into dictionary of lexemes ```Lexer.py```
``` Python
OrderedDict([
  ('5', ['PRINT', '"', 'FACTORIAL', '"']),
  ('10', ['REM', 'COMPUTE', 'FACTORIAL', 'OF', 'N']),
  ('20', ['PRINT', '"', 'N', '=', '"', ';']),
  ('30', ['N', '=', '123']),
  ('40', ['LET', 'X', '=', '1']),
  ('50', ['FOR', 'I', '=', '1', 'TO', 'N']),
  ('60', ['LET', 'X', '=', 'X', '*', 'I']),
  ('70', ['NEXT', 'I']),
  ('80', ['PRINT', '"', 'N', '=', '"', ';', 'N', ',', '"', 'N!', '=', '"', ';', 'X']),
  ('90', ['END'])
])
```


## Create dictionary of tokens based on lexemes ```Lexer.py```
```python
OrderedDict([
  ('5', [
    {'type': 'PRINT', 'value': 'PRINT', 'line_num': '5'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '5'},
    {'type': 'LITERAL', 'value': 'FACTORIAL', 'line_num': '5'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '5'}
  ]), 
  ('10', [
    {'type': 'COMMENT', 'value': 'REM', 'line_num': '10'},
    {'type': 'LITERAL', 'value': 'COMPUTE', 'line_num': '10'},
    {'type': 'LITERAL', 'value': 'FACTORIAL', 'line_num': '10'},
    {'type': 'LITERAL', 'value': 'OF', 'line_num': '10'},
    {'type': 'LITERAL', 'value': 'N', 'line_num': '10'}
  ]), 
  ('20', [
    {'type': 'PRINT', 'value': 'PRINT', 'line_num': '20'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '20'},
    {'type': 'LITERAL', 'value': 'N', 'line_num': '20'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '20'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '20'},
    {'type': 'PUNCTUATION', 'value': ';', 'line_num': '20'}
  ]), 
  ('30', [
    {'type': 'LITERAL', 'value': 'N', 'line_num': '30'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '30'},
    {'type': 'LITERAL', 'value': '123', 'line_num': '30'}
  ]), 
  ('40', [
    {'type': 'VAR-DEF', 'value': 'LET', 'line_num': '40'},
    {'type': 'LITERAL', 'value': 'X', 'line_num': '40'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '40'},
    {'type': 'LITERAL', 'value': '1', 'line_num': '40'}
  ]), 
  ('50', [
    {'type': 'FOR-DEF', 'value': 'FOR', 'line_num': '50'},
    {'type': 'LITERAL', 'value': 'I', 'line_num': '50'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '50'},
    {'type': 'LITERAL', 'value': '1', 'line_num': '50'},
    {'type': 'FOR-DEF', 'value': 'TO', 'line_num': '50'},
    {'type': 'LITERAL', 'value': 'N', 'line_num': '50'}
  ]), 
  ('60', [
    {'type': 'VAR-DEF', 'value': 'LET', 'line_num': '60'},
    {'type': 'LITERAL', 'value': 'X', 'line_num': '60'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '60'},
    {'type': 'LITERAL', 'value': 'X', 'line_num': '60'},
    {'type': 'OPERATOR', 'value': '*', 'line_num': '60'},
    {'type': 'LITERAL', 'value': 'I', 'line_num': '60'}
  ]), 
  ('70', [
    {'type': 'FOR-DEF', 'value': 'NEXT', 'line_num': '70'},
    {'type': 'LITERAL', 'value': 'I', 'line_num': '70'}
  ]), 
  ('80', [
    {'type': 'PRINT', 'value': 'PRINT', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '80'},
    {'type': 'LITERAL', 'value': 'N', 'line_num': '80'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': ';', 'line_num': '80'},
    {'type': 'LITERAL', 'value': 'N', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': ',', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '80'},
    {'type': 'LITERAL', 'value': 'N!', 'line_num': '80'},
    {'type': 'OPERATOR', 'value': '=', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': '"', 'line_num': '80'},
    {'type': 'PUNCTUATION', 'value': ';', 'line_num': '80'},
    {'type': 'LITERAL', 'value': 'X', 'line_num': '80'}
  ]), 
  ('90', [
    {'type': 'NO-PARAM', 'value': 'END', 'line_num': '90'}
  ])
])
```

