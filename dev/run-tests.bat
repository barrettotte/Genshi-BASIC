@ECHO OFF
SET CACHE=%CD%
CD ../lib/GenshiBASIC
ECHO Running test_lexer... & CALL python -m unittest tests.test_lexer
ECHO Running test_parser... & CALL python -m unittest tests.test_parser
CD %CACHE%
ECHO Done.
PAUSE
REM Run all tests:  
REM    python -m unittest discover (run all test*.py)