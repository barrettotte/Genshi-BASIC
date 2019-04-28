@ECHO OFF
SET CACHE=%CD%
CD ../lib/GenshiBASIC
ECHO Running all test cases... & python -m unittest discover
CD %CACHE%
ECHO Done.
PAUSE