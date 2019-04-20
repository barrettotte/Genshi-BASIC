# GenshiBASIC-Interpreter

An interpreter for 原始 (Genshi) BASIC; A primitive implementation of BASIC based off of Commodore 64 BASICv2

This package is primarily for the Genshi BASIC interpreter, but the lexer and parser can also be used separately


## Install
```TBD```


## GenshiBASIC Package Examples
```python
from GenshiBASIC import GenshiBASIC
genshiBas = GenshiBASIC.New()
# Source code can be passed as string, File, or filepath string (with is_file_path=True)

# --- Interpreter ---
with open('./test.bas', 'r') as f:
    genshiBas.interpret(f)

genshiBas.interpret('./test.bas', is_file_path=True)

genshiBas.interpret('10 PRINT "HELLO GENSHI BASIC"')


# --- Warnings / Exceptions ---
genshiBas.interpret('../somewhere/missing.bas', is_file_path=True) # Throws FileNotFound exception
genshiBas.interpret('./test.txt', is_file_path=True) # Throws UserWarning for file extension

# Missing line numbers (raises SyntaxWarning)
genshiBas.interpret('PRINT "HELLO WORLD"\nA=123') # Converted to '1 PRINT "HELLO WORLD"\n2 A=123


# --- Lexer ---
genshiBas.lex('10 PRINT "HELLO WORLD"') # returns tokens

with open('./test.bas', 'r') as f:
    genshiBas.make_tokens(f) # same functionality as lex()

genshiBas.make_lexemes('./test.bas', is_file_path=True) # returns lexemes

```


## 原始 BASIC
Genshi BASIC has 41 commands and is a simpler version of Commodore 64 BASICv2 (71 commands).

Essentially, I stripped out all of the memory manipulation and I/O. Otherwise, 
I would be better off making a Commodore 64 VM instead of an interpreter to add all the proper functionality.

These changes objectively make this version of BASIC pretty useless, but this is just meant for education.


## Symbolic Operators
* Arithmetic ```+, -, *, \, ^```
* Assignment ```=```
* Relational ```<, >, <>, <=, =<, >=, =>``` (LT, GT, NE, LE, LE, GE, GE)


## Commands

| Command | Description                                | Syntax                                       |
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
| EXP     | Inverse natural log of numeric; EXP(x)=e^X | ```EXP(-1)``` -> 0.367879441                 |
| FN      | Executes defined function                  | ```FN FTEST(3)``` -> 9                       |
| FOR     | Declare a for loop                         | ```FOR X=0 TO 5: PRINT X: NEXT``` -> 0...5   |
| GOSUB   | Jump to subroutine at line number          | ```GOSUB 1000```                             |
| GOTO    | Jump to line number                        | ```GOTO 500```                               |
| IF      | Start if statement                         | ```IF A$="" THEN PRINT "EMPTY"``` -> "EMPTY" |
| INT     | Round a numeric                            | ```INT(1.53)``` -> 1                         |
| LEFT$   | Substring from left to numeric (0-255)     | ```A$="ABCDEF":LEFT$(A$, 3)``` -> "ABC"      |
| LEN     | Length of string                           | ```A$="ABCD":PRINT LEN(A$)``` -> 4           |
| LET     | Assign values to variable                  | ```LET C$ = $A + B$```                       |
| LOG     | Natural logarithm of numeric               | ```LOG(10)``` -> 2.30258509                  |
| MID$    | Substring from numeric to numeric (0-255)  | ```MID$(A$, 1, 3)```                         |
| MOD     | Modulus of numeric                         | ```4 MOD 3``` -> 1                           |
| NEXT    | Next iteration of for loop                 | ```FOR X=1 TO 3: PRINT X: NEXT X``` -> 1...3 |
| NOT     | Boolean NOT                                | ```IF NOT A=1 AND B$<>"TEST" THEN ```        |
| OR      | Boolean OR                                 | ```4<2 OR 1>9``` -> 0 (false)                |
| PRINT   | Print to screen. ';' suppress newline      | ```PRINT "HELLO"``` -> "HELLO"               |
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


## Possible future goals
* Look into adding **DATA**, **READ**, **INPUT** commands ... might be doable?


## References
* Making a Python Package https://uoftcoders.github.io/studyGroup/lessons/python/packages/lesson/
* https://hackernoon.com/lexical-analysis-861b8bfe4cb0
* Commodore 64 BASIC 
  * https://www.c64-wiki.com/wiki/BASIC
  * https://www.c64-wiki.com/wiki/C64-Commands
* Web BASIC interpreter https://yohan.es/swbasic/
