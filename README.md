# Genshi-BASIC
An interpreter for Genshi BASIC; A BASIC dialect based on BASIC version 2.

Even though writing an interpreter for a custom BASIC dialect is pretty useless, the same 
lexing, parsing, and interpreting fundamentals I learned can be applied to other languages.


## Genshi BASIC
Genshi BASIC has ?? keywords and ? symbolic operators. TODO:
As stated above, the grammar is based on BASIC version 2.

Genshi (原始) means simple in romaji. I chose this name because I stripped out a lot of
functionality to make a simpler BASIC. Arguably this makes it pretty useless, 
but this is a learning project rather than a useful one.


### Notable differences from BASIC version 2
Genshi BASIC is meant to be a simpler version of BASIC version 2.
I stripped out a bunch of stuff and didn't really add anything special.

I used [this page](https://www.c64-wiki.com/wiki/C64-Commands) on Commodore 64 commands
as reference for BASIC version 2.

Removed:

- function declarations - ```DEF```, ```FN```
- memory operations - ```FRE```, ```PEEK```, ```POKE```, ```WAIT```
- system operations - ```GET```, ```STATUS```, ```SYS```, ```USR```, ```TIME```
- file operations - ```OPEN```, ```CLOSE```, ```VERIFY```

Added:

- new keywords - ```XOR```


## Usage
```python
# usage.py

TODO:
```


## Genshi BASIC Examples
TODO: printing, comments, variables, arithmetic, arrays, loops, if, subroutines
```
```


## Language Overview
TODO: keywords, operators


## Problems
TODO:


## Development
- Install deps - ```pip3 install -r requirements.txt```
- Run tests - ```python3 -m unittest discover```


## References
- Commodore 64 BASIC
  - https://www.c64-wiki.com/wiki/BASIC
  - https://www.c64-wiki.com/wiki/C64-Commands
- EBNF https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
