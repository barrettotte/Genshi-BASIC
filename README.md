# GenshiBASIC-Interpreter

An interpreter for 原始 (Genshi) BASIC; A primitive implementation of BASIC based off of Commodore 64 BASICv2.

This is my first attempt at writing an interpreter and a python package.

Even though writing an interpreter for a custom BASIC dialect is pretty useless, the same 
lexing, parsing, and interpreting fundamentals I learned can be applied to other languages.


## Install
```TBD```


## GenshiBASIC Package Examples
```python
from GenshiBASIC import GenshiBASIC
genshiBas = GenshiBASIC.New()
# Source code can be passed as string, File, or filepath string (with is_file_path=True)

# --- Interpreter ---
with open('./programs/test.bas', 'r') as f:
    genshiBas.interpret(f)

genshiBas.interpret('./programs/test.bas', is_file_path=True)

genshiBas.interpret('10 PRINT "HELLO GENSHI BASIC"')


# --- Warnings / Exceptions ---
genshiBas.interpret('../somewhere/missing.bas', is_file_path=True) # Throws FileNotFound exception
genshiBas.interpret('./programs/test.txt', is_file_path=True) # Raises UserWarning for file extension

# Missing line numbers (raises SyntaxWarning)
genshiBas.interpret('PRINT "HELLO WORLD"\nA=123') # Converted to '1 PRINT "HELLO WORLD"\n2 A=123


# --- Lexer ---
genshiBas.lex('10 PRINT "HELLO WORLD"') # returns tokens

with open('./programs/test.bas', 'r') as f:
    genshiBas.make_tokens(f) # same functionality as lex()

genshiBas.make_lexemes('./programs/test.bas', is_file_path=True) # returns lexemes


# --- Parser ---
genshiBas.parse('10 PRINT "HELLO WORLD"') # returns parse tree


# --- Interpreter ---

# TBD

```


## 原始 BASIC
Genshi BASIC has 48 keywords and is inspired by Commodore 64 BASICv2.

Essentially, I stripped out all of the memory manipulation and I/O (except PRINT). Otherwise, 
I would be better off making a Commodore 64 VM instead of an interpreter to add all the proper functionality.

I took the liberty of changing bits of the language to make the task of building a parser easier.
These changes objectively make this version of BASIC pretty useless, but this is just meant for education.


## C64 BASIC Rules
* Lines can only contain 40 characters
* Max number of lines is 63999


## Symbolic Operators
* Arithmetic ```+, -, *, \, ^```
* Assignment ```=```


## Keywords
| Keyword | Description                                | Syntax                                       |
| ------- | ------------------------------------------ | -------------------------------------------- |
| ABS     | Absolute value of numeric                  | ```ABS(-10)``` -> 10                         |
| AND     | Boolean AND                                | ```3>2 AND 5<6``` -> -1 (true)               |
| ASC     | ASCII Value of first character             | ```ASC("ABC")``` -> 65                       |
| ATN     | Arc Tangent of numeric angle (radians)     | ```ATN(1)*4``` -> 3.1415266                  |
| CHR$    | Convert numeric (0-255) to ASCII character | ```CHR$(65)``` -> "A"                        |
| CLR     | Deletes variables, arrays, defs, etc.      | ```CLR```                                    |
| COS     | Cosine of numeric angle (radians)          | ```COS(0)``` -> 1                            |
| DEF     | Defines a function                         | ```DEF FN FTEST(X) = X*3```                  |
| DIM     | Allocate memory for an array               | ```DIM A$(2,3)```                            |
| END     | End program execution                      | ```END```                                    |
| ENDFOR  | Close scope of for loop                    | ```FOR X=1 TO 3: PRINT X: ENDFOR``` -> 1...3 |
| EQ      | Equal to relational operator               | ```IF I EQ I```                              |
| EXP     | Inverse natural log of numeric; EXP(x)=e^X | ```EXP(-1)``` -> 0.367879441                 |
| FN      | Executes defined function                  | ```FN FTEST(3)``` -> 9                       |
| FOR     | Declare a for loop                         | ```FOR X=0 TO 5: PRINT X: ENDFOR``` -> 0...5 |
| GE      | >= relational operator                     | ```IF I GE 0```                              |
| GOSUB   | Jump to subroutine at line number          | ```GOSUB 1000```                             |
| GOTO    | Jump to line number                        | ```GOTO 500```                               |
| GT      | > relational operator                      | ```IF I GT 0```                              |
| IF      | Start if statement                         | ```IF A$="" THEN PRINT "EMPTY"``` -> "EMPTY" |
| INT     | Round a numeric                            | ```INT(1.53)``` -> 1                         |
| LE      | <= relational operator                     | ```IF I LE 0```                              |
| LEFT$   | Substring from left to numeric (0-255)     | ```A$="ABCDEF":LEFT$(A$, 3)``` -> "ABC"      |
| LEN     | Length of string                           | ```A$="ABCD":PRINT LEN(A$)``` -> 4           |
| LET     | Assign values to variable                  | ```LET C$ = $A + B$```                       |
| LT      | < relational operator                      | ```IF I LT 0```                              |
| LOG     | Natural logarithm of numeric               | ```LOG(10)``` -> 2.30258509                  |
| MID$    | Substring from numeric to numeric (0-255)  | ```MID$(A$, 1, 3)```                         |
| MOD     | Modulus of numeric                         | ```4 MOD 3``` -> 1                           |
| NE      | != relational operator                     | ```IF I NE 4```                              |
| NOT     | Boolean NOT                                | ```IF NOT A=1 AND B$<>"TEST" THEN ```        |
| OR      | Boolean OR                                 | ```4<2 OR 1>9``` -> 0 (false)                |
| PRINT   | Print to screen                            | ```PRINT "HELLO"``` -> "HELLO"               |
| REM     | Comments                                   | ```REM THIS IS A COMMENT```                  |
| RETURN  | Finish subroutine                          | ```RETURN```                                 |
| RIGHT$  | Substring from right to numeric (0-255)    | ```RIGHT$($A, 3)```                          |
| RND     | Random float from 0.0 to 1.0               | ```INT(RND(1)*100)``` -> 65                  |
| SGN     | Return sign of numeric -1,0,1              | ```SGN(-11)``` -> -1                         |
| SIN     | Sine of numeric angle (radians)            | ```SIN(1)``` -> 0.8141470985                 |
| SPC     | Add spaces in print statement              | ```PRINT "HELLO" SPC(10) "WORLD"```          |
| SQR     | Square root of numeric                     | ```SQR(4)``` -> 2                            |
| STEP    | Used as iteration amount in for loop       | ```FOR X=1 TO 3 STEP 0.5```                  |
| STR$    | Convert numeric to string                  | ```STR$(1E11)``` -> "1E+11"                  |
| TAB     | Print a tab                                | ```PRINT "I:" TAB(10);I```                   |
| TAN     | Tangent of numeric angle (radians)         | ```TAN(1)``` -> 1.55740772                   |
| THEN    | Second half of if statement                | ```IF $A="" THEN PRINT "EMPTY"```            |
| TO      | Range keyword in for loop                  | ```FOR X=1 TO 3: PRINT "HELLO"```            |
| XOR     | Boolean Exclusive OR                       | ```IF $A="" XOR $B="" THEN ...```            |


## Notable differences vs Commodore 64 BASICv2
* As previously mentioned, all memory manipulation and I/O (except ```PRINT```) is stripped out.
* Replaced ```NEXT``` with ```ENDFOR``` to make parsing easier.
* Keyword ```STEP``` is necessary in ```FOR``` statements.
* Added ```XOR``` keyword for exclusive OR operator.
* Added ```MOD``` keyword for modulus operator.
* Replaced ```=, >, <, <>, <=, =<, >=, =>``` with ```EQ, GT, LT, NE, LE, GE```
  * I decided to mix the way CLP, SQL, and CFML handle relational operators; this made parsing tremendously easier.
* Identifiers can contain characters they normally shouldn't (!,@,#,[0-9],etc) (lazy lexing)
  * If an operator is specified in an identifier such as ```LET A+=4``` it is evaluated as ```LET A + = 4 (EXCEPTION)```
* Lines are stripped of whitespace > 1; To retain whitespace in printing use ```SPC(N)```
* A string variable by convention should end with '$', but I won't throw an exception.


## Possible future goals
* Look into adding **DATA**, **READ**, **INPUT** commands ... might be doable?
* Token column number tracking (begin, end) for better error messages
* Better error specification (column number + expression)
* Print format specifiers ```',', ';', ':'```


## References
* Compilers and Interpreters Chapter 4 http://flint.cs.yale.edu/cs421/lectureNotes/c04.pdf
* Commodore 64 BASIC 
  * https://www.c64-wiki.com/wiki/BASIC
  * https://www.c64-wiki.com/wiki/C64-Commands
* Crafting Interpreters https://craftinginterpreters.com/
* ENBF https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
* Introduction to Lexical Analysis https://hackernoon.com/lexical-analysis-861b8bfe4cb0
* Making a Python Package https://uoftcoders.github.io/studyGroup/lessons/python/packages/lesson/
* Web BASIC interpreter https://yohan.es/swbasic/
