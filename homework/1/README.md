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
   當 sel=1 時，nsel=0(關閉a通道)\
   
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
作用： 將這兩個中間結果 (aPar 和bPart) 進行 Or 運算，得到最終輸出。由於在任何時候，aPart和 bPart 只有一個可能等於in}的值，另一個必定是 0，所以 Or} 運算確保了輸出out 總是等於被選中的那個輸入\

參考AI看不懂

 ## And16
把16個小AND閘列出，每一位對應一個AND\
參考AI 有看懂

## Dmux
Not：製造一個 開關訊號 給A出口。\
And for a：只有 A 的地址 (當 sel=0 時) 吻合，in才能進入a。\
And for b：只有 B 的地址 (當 sel=1 時) 吻合，in才能進入b。\
使用AI 看不懂
