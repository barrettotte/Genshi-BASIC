10      REM CONVERT DECIMAL TO BINARY
100     DIM A(7)
110     N=47
120     IF N>255 OR N<0 GOTO 110
130     GOSUB 1000
140     PRINT "BINARY=";
150     FOR I=0 TO 7 STEP 1
160         PRINT A(I);
170     NEXT I
180     END
999     REM ---------------------------
1000    REM CONVERT TO BINARY
1001    REM ---------------------------
1010    FOR I=7 TO 0 STEP -1
1020        A(I)=N-INT(N/2)*2
1030        N=INT(N/2)
1040    NEXT I
1050    RETURN