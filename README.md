# GenshiBas-Interpreter


## Interpreter Example
```python

from GenshiBas import GenshiBas

genshiBas = GenshiBas.New()

# Interpret contents of file
with open('./test.bas', 'r') as f:
    genshiBas.interpret(f)

# Open file at filepath and interpret contents
genshiBas.interpret('./test.bas', is_file_path=True)

# Interpret Genshi BASIC string
genshiBas.interpret('10 PRINT "HELLO GENSHI BASIC"')

```


## 原始 BASIC
Genshi BASIC has x commands and is a simpler version of Commodore 64 BASICv2 (71 commands)


## Commands

| Command | Description | Syntax |
| ------- | ----------- | ------ |
| x       | x           | x      |



## Sources
* Making a Python Package https://uoftcoders.github.io/studyGroup/lessons/python/packages/lesson/
* Commodore 64 Commands https://www.c64-wiki.com/wiki/C64-Commands
