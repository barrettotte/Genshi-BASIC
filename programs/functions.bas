10 DEF FN FTEST(X) = X*3
20 DEF FN FUNC_A     (X,   Y,  Z) = X+ Y  *Z

REM ---- Exceptions ----

REM Expected 'FN'
REM 30 DEF FUNC_BAD(X) = X*3

REM Expected identifier
REM 30 DEF FN (X) = X*3

30 DEF FN FUNC_BAD(X) = X*3