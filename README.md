# GenshiBASIC-Interpreter

An interpreter for 原始 (Genshi) BASIC; A BASIC dialect based on Commodore 64 BASIC.

Even though writing an interpreter for a custom BASIC dialect is pretty useless, the same 
lexing, parsing, and interpreting fundamentals I learned can be applied to other languages.


## 原始 BASIC
Genshi BASIC has 50 keywords and 7 symbolic operators. The grammar rules were taken from Commodore 64 BASIC
and changed to fit the scope of this project with my limited knowledge of parsing/interpreting.

**Rewritten 11/15/20** to reflect the things I've learned since the original implimentation.


## Usage
```python
TODO:
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
| NEXT      | Close scope of loop                        | ```FOR X=1 TO 3: PRINT X: NEXT``` -> 1...3   |
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


## Notable differences vs Commodore 64 BASIC
* As previously mentioned, all memory manipulation and I/O (except ```PRINT```) is stripped out.


## Problems
TODO:


## References
* Compilers and Interpreters Chapter 4 http://flint.cs.yale.edu/cs421/lectureNotes/c04.pdf
* Commodore 64 BASIC 
  * https://www.c64-wiki.com/wiki/BASIC
  * https://www.c64-wiki.com/wiki/C64-Commands
* ENBF https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
