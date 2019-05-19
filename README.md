# GenshiBASIC-Interpreter


[![pipeline status](https://gitlab.com/barrettotte/GenshiBASIC-Interpreter/badges/master/pipeline.svg)](https://gitlab.com/barrettotte/GenshiBASIC-Interpreter/commits/master)
![GitHub](https://img.shields.io/github/license/barrettotte/GenshiBASIC-Interpreter.svg)


An interpreter for 原始 (Genshi) BASIC; A BASIC dialect based on Commodore 64 BASICv2.

Even though writing an interpreter for a custom BASIC dialect is pretty useless, the same 
lexing, parsing, and interpreting fundamentals I learned can be applied to other languages.


## 原始 BASIC
Genshi BASIC has 50 keywords and 7 symbolic operators. The grammar rules were taken from Commodore 64 BASICv2
and changed to fit the scope of this project with my limited knowledge of parsing/interpreting.

Essentially, I stripped out all of the memory manipulation and I/O (except PRINT). Otherwise, 
I would have been better off making a Commodore 64 VM instead of an interpreter to add all the proper system functionality.


## Sample
```python
from GenshiBASIC import GenshiBASIC
genshi_basic = GenshiBASIC.New()

# Program can be loaded as file too
prog = "\n".join([
  '1     REM THE CLASSIC FIZZBUZZ PROGRAM IN GENSHI BASIC',
  '10    DEF FN FIZZPR(IDX, S$) = PRINTL CAT$(IDX, S$)',
  '20    FOR I=1 TO 100 STEP 1',
  '30      IF (I % 15) EQ 0 THEN FIZZPR(I, " FIZZBUZZ")',
  '40      IF (I % 3)  EQ 0 THEN FIZZPR(I, " FIZZ")',
  '50      IF (I % 5)  EQ 0 THEN FIZZPR(I, " BUZZ")',
  '60    ENDFOR',
  '1000  END',
])
genshi_basic.interpret(prog)

# ----- Console Output ----- #
3 FIZZ
5 BUZZ
.
.
.
90 FIZZBUZZ
93 FIZZ
95 BUZZ
96 FIZZ
99 FIZZ
100 BUZZ
# -------------------------- #
```



## Yeah...I Didn't Finish it
This was for educational purposes, so I have not extensively gone through every single scenario for testing.
I work on a lot of side projects, so I try not to stay in one place for too long. I plan out the project requirements, 
get them to a functional state with some test coverage, and move on to the next "shiny" side project idea that pops into my head.

It saddens me to say that this is not completely finished. I ran into a lot of problems towards the end and I just
want to look at something else now. I'm honestly surprised I even made it as far as I did.
In the future, I will definitely be using a library like Antlr to make a more stable
language. I learned a lot from this project, but I think its time to let this one sit on the shelf.



## Other Examples
```python
from GenshiBASIC import GenshiBASIC
genshi_basic = GenshiBASIC.New()
# Source code can be passed as string, File, or filepath string (with is_file_path=True)

# --- Interpreter ---

# The intrepreter constructs a print buffer and prints interpreted program to console

with open('./programs/test.bas', 'r') as f:
    genshi_basic.interpret(f)

genshi_basic.interpret('./programs/test.bas', is_file_path=True)
genshi_basic.interpret('10 PRINT "HELLO GENSHI BASIC"')
genshi_basic.interpret('10 PRINT "HELLO GENSHI BASIC"', debug=True) # Returns dictionary of debug info


# --- Warnings / Exceptions ---
genshi_basic.interpret('../somewhere/missing.bas', is_file_path=True) # Throws FileNotFound exception
genshi_basic.interpret('./programs/test.txt', is_file_path=True) # Raises UserWarning for file extension

# Missing line numbers (raises SyntaxWarning)
genshi_basic.interpret('PRINT "HELLO WORLD"\nA=123') # Converted to '1 PRINT "HELLO WORLD"\n2 A=123

# Each part of the interpreter can be called separately:
  
  # --- Lexer ---
  genshi_basic.lex('10 PRINT "HELLO WORLD"') # returns tokens
  
  with open('./programs/test.bas', 'r') as f:
      genshi_basic.make_tokens(f) # same functionality as lex()
  
  genshi_basic.make_lexemes('./programs/test.bas', is_file_path=True) # returns lexemes
  
  # --- Parser ---
  genshi_basic.parse('10 PRINT "HELLO WORLD"') # returns parse tree

```


## Keywords
| Keyword   | Description                                | Syntax                                       |
| --------- | ------------------------------------------ | -------------------------------------------- |
| ABS       | Absolute value of numeric                  | ```ABS(-10)``` -> 10                         |
| AND       | Boolean AND                                | ```3 GT 2 AND 5 LT 6``` -> -1 (true)         |
| ASC       | ASCII value of first character             | ```ASC("ABC")``` -> 65                       |
| BIN$      | Return binary string of numeric            | ```BIN$(1)```                                |
| CAT$      | Concatenate two expressions as a string    | ```PRINT CAT$("HELLO", X+1)```-> "HELLOX+1"  |
| CHR$      | Convert numeric (0-255) to ASCII character | ```CHR$(65)``` -> "A"                        |
| CLR       | Deletes variables, arrays, defs, etc.      | ```CLR```                                    |
| COS       | Cosine of numeric angle (radians)          | ```COS(0)``` -> 1                            |
| DEF       | Defines a function                         | ```DEF FN FTEST(X) = X*3```                  |
| DIM       | Declare an array up to three dimensions    | ```DIM A(2,3,2)```                           |
| END       | End program execution                      | ```END```                                    |
| ENDFOR    | Close scope of for loop                    | ```FOR X=1 TO 3: PRINT X: ENDFOR``` -> 1...3 |
| EQ        | Equal to relational operator               | ```IF I EQ I```                              |
| EXP       | Inverse natural log of numeric; EXP(x)=e^X | ```EXP(-1)``` -> 0.367879441                 |
| FN        | Executes defined function                  | ```FN FTEST(3)``` -> 9                       |
| FOR       | Declare a for loop                         | ```FOR X=0 TO 5: PRINT X: ENDFOR``` -> 0...5 |
| GE        | >= relational operator                     | ```IF I GE 0```                              |
| GOSUB     | Jump to subroutine at line number          | ```GOSUB 1000```                             |
| GOTO      | Jump to line number                        | ```GOTO 500```                               |
| GT        | > relational operator                      | ```IF I GT 0```                              |
| HEX$      | Return hex string of numeric               | ```HEX$(15)```                               |
| IF        | Start if statement                         | ```IF A$ EQ "" THEN PRINT "EMPTY"``` -> "EMPTY" |
| INT       | Round a numeric                            | ```INT(1.53)``` -> 1                         |
| LE        | <= relational operator                     | ```IF I LE 0```                              |
| LEFT$     | Substring from left to numeric (0-255)     | ```A$="ABCDEF":LEFT$(A$, 3)``` -> "ABC"      |
| LEN       | Length of string                           | ```A$="ABCD":PRINT LEN(A$)``` -> 4           |
| LET       | Assign values to variable                  | ```LET C$ = $A + B$```                       |
| LT        | < relational operator                      | ```IF I LT 0```                              |
| LOG       | Natural logarithm of numeric               | ```LOG(10)``` -> 2.30258509                  |
| MID$      | Substring from numeric to numeric (0-255)  | ```MID$(A$, 1, 3)```                         |
| NE        | != relational operator                     | ```IF I NE 4```                              |
| NOT       | Boolean NOT                                | ```IF NOT A EQ 1 AND B$ NE "TEST" THEN ```   |
| OR        | Boolean OR                                 | ```4 LT 2 OR 1 GT 9``` -> 0 (false)          |
| PI        | Return numeric PI * X                      | ```X=PI(2)```                                |
| PRINT     | Print to screen                            | ```PRINT "HELLO"``` -> "HELLO"               |
| PRINTL    | Print line to screen                       | ```PRINTL "HELLO"``` -> "HELLO\n"            |
| REM       | Comments                                   | ```REM THIS IS A COMMENT```                  |
| RETURN    | Finish subroutine                          | ```RETURN```                                 |
| RIGHT$    | Substring from right to numeric (0-255)    | ```RIGHT$($A, 3)```                          |
| RND       | Random float from 0.0 to 1.0               | ```INT(RND(1)*100)``` -> 65                  |
| SGN       | Return sign of numeric -1,0,1              | ```SGN(-11)``` -> -1                         |
| SIN       | Sine of numeric angle (radians)            | ```SIN(1)``` -> 0.8141470985                 |
| SPC$      | Return x spaces as string literal          | ```PRINT CAT$("HELLO", SPC$(10))```          |
| SQR       | Square root of numeric                     | ```SQR(4)``` -> 2                            |
| STEP      | Used as iteration amount in for loop       | ```FOR X=1 TO 3 STEP 0.5```                  |
| STR$      | Convert numeric to string                  | ```STR$(1E11)``` -> "1E+11"                  |
| TAN       | Tangent of numeric angle (radians)         | ```TAN(1)``` -> 1.55740772                   |
| THEN      | Second half of if statement                | ```IF $A EQ "" THEN PRINT "EMPTY"```         |
| TO        | Range keyword in for loop                  | ```FOR X=1 TO 3: PRINT "HELLO"```            |
| XOR       | Boolean Exclusive OR                       | ```IF $A EQ "" XOR $B EQ "" THEN ...```      |
| Operators | arithmetic: ```+, -, *, \, ^, %```, assignment: ```=``` |                                 | 


## Notable differences vs Commodore 64 BASICv2
* As previously mentioned, all memory manipulation and I/O (except ```PRINT```) is stripped out.
* Replaced ```NEXT``` with ```ENDFOR``` to make parsing easier.
* Keyword ```STEP``` is necessary in ```FOR``` statements.
* Replaced ```=, >, <, <>, <=, =<, >=, =>``` with ```EQ, GT, LT, NE, LE, GE```
  * I decided to mix the way CLP, SQL, and CFML handle relational operators; this made parsing tremendously easier.
* Identifiers can contain characters they normally shouldn't (!,@,#,[0-9],etc) (lazy lexing)
  * If an operator is specified in an identifier such as ```LET A+=4``` it is evaluated as ```LET A + = 4 (EXCEPTION)```
* Lines are stripped of whitespace > 1; To retain whitespace in printing use ```SPC(N)```
* A string variable by convention should end with '$', but I won't throw an exception.
* String concatentation must be done with variables
  * ```10 "HELLO" + "WORLD"``` would not work; you would have to do ```10 A$="HELLO" 11 B$="WORLD" 12 A$ + B$```
* Since I made relational operators longer, I bumped the max column count of each line to 64 characters
* Max program length is 64KB (65,536 bytes) lines
* To handle string literal concatentation easily, I added ```CAT$```. String variables can still be concatenated normally ```X$=Y$+Z$```. This was added to finish the parser faster.
* Currently there are no print format specifiers, I added ```PRINTL``` to provide a simple print line function
* If statements are 'truthy', if the expression evaluates to 1 -> true, 0 -> false
  * EX: ```IF 10-9 THEN PRINT "HELLO"```


## Possible future goals (unlikely)
* Look into adding **DATA**, **READ**, **INPUT** commands ... might be doable?
* Token column number tracking (begin, end) for better error messages
* Better error specification (column number + expression)
* Print format specifiers ```',', ';', ':'```
* Fix expression tree building
* Error logging


## Running in Docker
* ```docker build --tag=genshibasic .```


## Problems

### Expressions
So, due to lack of knowledge. My expression trees are not being built correctly. 
This has to do with the way I was using a stack to build my tree. Expressions are parsed right to left.
So, on line 10 below, ```5 EQ 0``` is evaluated first, then ```10 % 0```; throwing an exception

This was a really disappointing find and I think it would mean spending longer on this side project
to rewrite my parser. That is what I should do, but I'm not going to yet. It can be worked around by 
reordering the expression or using parenthesis.
```python
'5  IF 0 EQ 10 % 5 THEN PRINTL "A"',   # Prints "A"
'10 IF 10 % 5 EQ 0 THEN PRINTL "B"',   # Divide by zero error 
'15 IF (10 % 5) EQ 0 THEN PRINTL "C"', # Prints "B"
```


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

