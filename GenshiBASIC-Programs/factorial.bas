5  PRINT "HELLO WORLD"
10 REM COMPUTE FACTORIAL OF N
20 PRINT "N=";
30 N = 123
40 LET X=1
50 FOR I=1 TO N
60   LET X=X*I
70 ENDFOR
80 PRINT GLUE("N! = ", X)
90 END
5  PRINT "FACTORIAL"