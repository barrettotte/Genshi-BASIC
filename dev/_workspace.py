import GenshiBASIC, re


genshiBas = GenshiBASIC.New()
fpath='/home/barrett/Repos/GenshiBASIC-Interpreter/GenshiBASIC-Programs/fizzbuzz.bas'

with open(fpath, 'r') as f:
    genshiBas.interpret(f)
