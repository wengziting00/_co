## 1.not
AND(in, in) = in\
NAND(in, in) = NOT(in)\
老師上課講解


## 2.And
第一步:
Nand(a=a, b=b, out=n);把輸入a和b送進Nand閘，輸出為n 有1即為0
| a | b | n (Nand 輸出) |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |  |

第二步:
把上一步的輸出n送進一個Not閘(非閘/反相器)，輸出就是最終的 out
|n(Nand 輸出)|out(Not 輸出)|
|---|---|
|1  |  0|
|1  |  0|
|1  |  0|
|0  |  1| |

合起來就是And 閘的功能\
參考AI 有看懂

## 3.Or
|a|b  |	na|	nb|na AND nb|	NAND(na,nb)|	最終 out|
|--|--|---|---|---------|------------|---------|
|0 |	0|	1 |	1 |	1       |	0          |	0       |
|0 |	1|	1 |	0 |	0       |	1          |	1       |
|1 |	0|	0 |	1 |	0       |	1          |	1       |
|1 |	1|	0 |	0 |	0       |	1          |	1       | |

參考AI有看懂


## 4.Xor
|a|b|nab=¬(a∧b) (Nand 1)|anb=¬(a∧nab) (Nand 2)|bna=¬(b∧nab) (Nand 3)|輸出 out=¬(anb∧bna) (Nand 4)|Xor預期結果|
|--|--|---|---|---------|------------|--------|
|0|0|¬(0∧0)=1|¬(0∧1)=1|¬(0∧1)=1|¬(1∧1)=0|0|
|0|1|¬(0∧1)=1|¬(0∧1)=1|¬(1∧1)=0|¬(1∧0)=1|1|
|1|0|¬(1∧0)=1|¬(1∧1)=0|¬(0∧1)=1|¬(0∧1)=1|1|
|1|1|¬(1∧1)=0|¬(1∧0)=1|¬(1∧0)=1|¬(1∧1)=0|0| |

參考AI 看不懂

## 5.Mxu
1. 準備¬sel(Not)\
   程式碼：Not(in=sel, out=nsel)\
   目的： 計算sel的反向訊號nsel(¬sel)，作為a輸入的開關\
   當 sel=0 時，nsel=1(允許a通過)\
   當 sel=1 時，nsel=0(關閉a通道)
   
2. 處理輸入 a(And 1)
   程式碼： And(a=a, b=nsel, out=aPart)\
   公式對應： aPart = a ∧ nsel\
   作用： 這個 And 閘是一個「受控開關」\
   當 sel=0 (nsel=1)： aPart = a ∧  aPart= a (a 的值被傳遞)\
   當 sel=1nsel=0)：aPart= a ∧ 0 aPart= 0 (a 的值被阻斷為 0)
   
4. 處理輸入 b (And 2)
程式碼： And(a=b, b=sel, out=bPart)\
公式對應： bPart= b ∧sel\
作用： 這是另一個「受控開關」\
當sel=0：bPart = b ∧ bPart= 0 (b的值被阻斷為 0)\
當sel=1：bPart = b∧ bPart = b。 (b的值被傳遞)

5. 組合輸出 (Or)
程式碼： Or(a=aPart, b=bPart, out=out)\
公式對應：out =aPart ∨ bPart\
作用： 將這兩個中間結果 (aPar 和bPart) 進行 Or 運算，得到最終輸出。由於在任何時候，aPart和 bPart 只有一個可能等於in}的值，另一個必定是 0，所以 Or} 運算確保了輸出out 總是等於被選中的那個輸入

參考AI看不懂

## 6.DMux
先把 sel 反相：Not\
用 in 和 NOT sel 做 AND，得到 a\
用 in 和 sel 做 AND，得到 b
參考AI 有看懂

## 7.Halfadder
一個半加器負責計算兩個單一位元 ($a$ 和 $b$) 的和，會產生兩個輸出：\
Sum (和)：結果的最低位（右邊的位元）\
Carry (進位)：結果的最高位（左邊的位元）
1. 和位元 (Sum) 的計算Sum的值是 a 和 b 相加後，不帶進位 的結果
   
|a|b|a+b (十進位)|Sum (結果的最低位)|
|--|--|---------|------------|
|0|0|0|0|
|0|1|1|1|
|1|0|1|1|
|1|1|2 (或 102​)|0| |

觀察Sum 這一欄：只有當 a和 b 不同 時，輸出才是 1\
程式碼： XOR(a=a, b=b, out=sum)\
2. 進位位元 (Carry) 的計算 Carry 的值是a 和 b 相加後，是否產生進位 的旗標
|a|b|a+b (二進位)|Carry (是否進位)|
|--|--|---------|------------|
|0|0|002|0|
|0|1|012|0|
|1|0|012|0|
|1|1|102​|1| |

觀察 Carry 這一欄：只有當 a 和b 同時是 1 時，輸出才是 1\
程式碼： AND(a=a, b=b, out=carry)

## 8. FullAdder
1. 第一個 Half Adder（計算 $a + b$）

程式碼： HalfAdder(a=a, b=b, sum=s1, carry=c1)
功能：計算 $a$ 和 $b$ 的和

輸出中間和 $\mathbf{s1}$（$a \oplus b$）
輸出第一個進位 $\mathbf{c1}$（$a \land b$）

2. 第二個 Half Adder（計算 $s1 + c$）

程式碼： HalfAdder(a=s1, b=c, sum=sum, carry=c2)
功能：計算上一步的中間和 $\mathbf{s1}$ 和輸入進位 $\mathbf{c}$ 的和

$\mathbf{sum}$ 輸出：
這個結果就是最終的和位元：
三個位元 $a,b,c$ 的總和之右邊那一位。

sum
=
𝑠
1
⊕
𝑐
=
(
𝑎
⊕
𝑏
)
⊕
𝑐
sum=s1⊕c=(a⊕b)⊕c

$\mathbf{c2}$ 輸出：
這是 $s1$ 和 $c$ 相加產生的第二個進位。

3. Or 閘（計算最終進位 $\text{carry}$）

程式碼： Or(a=c1, b=c2, out=carry)
功能：決定最終的進位輸出 $\mathbf{carry}$。

$\mathbf{c1}$：代表 $a + b$ 產生的進位

$\mathbf{c2}$：代表 $(a+b\text{ 的和}) + c$ 產生的進位

只要 $c1$ 或 $c2$ 有任一個為 1，就會產生最後的進位：

carry
=
𝑐
1
∨
𝑐
2
carry=c1∨c2


 ## And16
把16個小AND閘列出，每一位對應一個AND\
參考AI 有看懂

