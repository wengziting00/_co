// eq (第 n 次出現)
@SP
AM=M-1
D=M       // D = y
A=A-1
D=M-D     // D = x - y
@TRUE_n   // 如果 x == y，則 x - y = 0
D;JEQ

(FALSE_n)
@SP
A=M-1
M=0       // False = 0
@CONTINUE_n
0;JMP

(TRUE_n)
@SP
A=M-1
M=-1      // True = -1 (二進位全為 1)

(CONTINUE_n)
