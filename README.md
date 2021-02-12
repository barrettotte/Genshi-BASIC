# Genshi-BASIC
Interpreter for Genshi BASIC; A simple dialect of BASIC created to 
learn the basics of making a programming language.

Even though writing an interpreter for a custom BASIC dialect is pretty useless, the same 
lexing, parsing, and interpreting fundamentals I learned can be applied to other languages.

I originally wrote this in 2019, but decided that this year (2021) I would rewrite it
to practice concepts I had learned since the original implementation.

I did get kind of lazy and skipped out on implementing a REPL, so for right now it
justs interprets an array of strings or a source file.


## Genshi BASIC
Genshi BASIC has 41 keywords. As stated above, the grammar is based on BASIC version 2.

Genshi (原始) means "simple" in romaji. I chose this name because I stripped out a lot of
functionality to make a simpler BASIC. Arguably this makes it pretty useless, 
but this is a learning project rather than a useful one.

Its worth noting that **this is not fully tested**. 
I more or less got a couple programs working correctly and called it a day.
As I said before, this is a rewrite and I'm honestly very bored of it now.


### Notable differences from BASIC version 2
Genshi BASIC is meant to be a simpler version of BASIC version 2.
I stripped out a bunch of stuff and didn't really add anything special.

I used [this page](https://www.c64-wiki.com/wiki/C64-Commands) on Commodore 64 commands
as reference for BASIC version 2.

Removed:

- function declarations - ```DEF```, ```FN```
- memory operations - ```FRE```, ```PEEK```, ```POKE```, ```WAIT```, ```NEW```
- system operations - ```GET```, ```STATUS```, ```SYS```, ```USR```, ```TIME```
- file operations - ```OPEN```, ```LOAD```, ```CLOSE```, ```VERIFY```, ```SAVE```
- "interactive" operations - ```RUN```, ```STOP```, ```LIST```

Changed:

- string variables are no longer required to end with '$'
- removed '$' characters from ```CHR$,LEFT$,MID$,RIGHT$``` operations

Added:

- new keywords - ```XOR```
- I lost motivation to add anything else cool


## Examples
```python
# Usage of genshi BASIC interpreter

from genshibasic.interpreter import Interpeter

pgm = [
  '10 REM Example 1',
  '20 LET A=3+4 * 6/2',
  '30 PRINT "A="; A',
  '40 A=8',
  '50 PRINT "NOW A="; A',
  '100 END'
]

genshi_int = Interpeter()
genshi_int.interpret(pgm)
    
# A=15.0
# NOW A=8
```


## Development
- Install deps - ```pip3 install -r requirements.txt```
- Run tests - ```python3 -m unittest discover```


## References
- Commodore 64 BASIC
  - https://www.c64-wiki.com/wiki/BASIC
  - https://www.c64-wiki.com/wiki/C64-Commands
- EBNF https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
