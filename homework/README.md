## not
AND(in, in) = in\
NAND(in, in) = NOT(in)

## And
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


## Or
|a|b  |	na|	nb|na AND nb|	NAND(na,nb)|	最終 out|
|--|--|---|---|---------|------------|---------|
|0 |	0|	1 |	1 |	1       |	0          |	0       |
|0 |	1|	1 |	0 |	0       |	1          |	1       |
|1 |	0|	0 |	1 |	0       |	1          |	1       |
|1 |	1|	0 |	0 |	0       |	1          |	1       | |

## Or8Way

它先用兩個 Or4Way 分別計算前四個 (in[0..3]) 和後四個 (in[4..7]) 的 OR，得到 or4a_out 和 or4b_out，再用一個 2-input Or 把這兩個結果合併成最終輸出 out


## Or16
每一行對應一位：out[i] = a[i] OR b[i]，從第 0 位到第 15 位

## Xor
|a|b|nab=¬(a∧b) (Nand 1)|anb=¬(a∧nab) (Nand 2)|bna=¬(b∧nab) (Nand 3)|輸出 out=¬(anb∧bna) (Nand 4)|Xor預期結果|
|--|--|---|---|---------|------------|--------|
|0|0|¬(0∧0)=1|¬(0∧1)=1|¬(0∧1)=1|¬(1∧1)=0|0|
|0|1|¬(0∧1)=1|¬(0∧1)=1|¬(1∧1)=0|¬(1∧0)=1|1|
|1|0|¬(1∧0)=1|¬(1∧1)=0|¬(0∧1)=1|¬(0∧1)=1|1|
|1|1|¬(1∧1)=0|¬(1∧0)=1|¬(1∧0)=1|¬(1∧1)=0|0| |



## Mxu
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

## Mux4Way16
第一層用 sel[0]，分別在 (a, b) 和 (c, d) 兩組中各選一個輸出，得到 ab_out 與 cd_out\
第二層再用 sel[1]，在 ab_out 和 cd_out 之間做選擇，決定最終的 out

## Mux8Way16
用 sel[0..1] 在前四組輸入 (a–d) 和後四組輸入 (e–h) 中各選出一個 16 位元資料，接著再用 sel[2] 決定要輸出前四組的結果還是後四組的結果，因此三位元選擇訊號剛好對應八種輸入情況，透過「先選哪一半、再選其中一個」的分層方式，用較小的多工器組合成 8 路 16-bit 多工器

## DMux
先把 sel 反相：Not\
用 in 和 NOT sel 做 AND，得到 a\
用 in 和 sel 做 AND，得到 b

##Not16
每一行都是單獨對應一位：out[i] = NOT in[i]，從 in[0] 到 in[15]\
就是把 16 位元的二進位數做按位元取反，等同於硬體中的 16-bit inverter


## Halfadder
一個半加器負責計算兩個單一位元 ($a$ 和 $b$) 的和，會產生兩個輸出：\
Sum (和)：結果的最低位（右邊的位元）\
Carry (進位)：結果的最高位（左邊的位元）
1. 和位元 (Sum) 的計算Sum的值是 a 和 b 相加後，不帶進位 的結果
   
|a|b|a+b (十進位)|Sum (結果的最低位)|

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

## FullAdder
1. 第一個 Half Adder（計算 $a + b$）

程式碼： HalfAdder(a=a, b=b, sum=s1, carry=c1)
功能：計算 $a$ 和 $b$ 的和

輸出中間和 s1（a ⊕ b）
輸出第一個進位 c1（a ⊕ b）

2. 第二個 Half Adder（計算 $s1 + c$）

程式碼： HalfAdder(a=s1, b=c, sum=sum, carry=c2)
功能：計算上一步的中間和 $\mathbf{s1}$ 和輸入進位 $\mathbf{c}$ 的和

$\mathbf{sum}$ 輸出：
這個結果就是最終的和位元：
三個位元 $a,b,c$ 的總和之右邊那一位\
sum=s1⊕c=(a⊕b)⊕c

$\mathbf{c2}$ 輸出：
這是 $s1$ 和 $c$ 相加產生的第二個進位。

3. Or 閘（計算最終進位 $\text{carry}$）

程式碼： Or(a=c1, b=c2, out=carry)
功能：決定最終的進位輸出 $\mathbf{carry}$。

$\mathbf{c1}$：代表 $a + b$ 產生的進位

$\mathbf{c2}$：代表 $(a+b\text{ 的和}) + c$ 產生的進位

只要 $c1$ 或 $c2$ 有任一個為 1，就會產生最後的進位：\
carry=c1∨c2

## And16
把16個小AND閘列出，每一位對應一個AND\


## Inc16
最右邊（LSB）只需 +1，用 HalfAdder(a, 1) \
其他各 bit 都是\
該 bit + 前一位 carry + 0 用 FullAdder \
最左邊的 carry（ignore）不輸出

## Add16
每一位都計算對應的 a[i] + b[i] + c_in，並把進位傳給下一位，最低位進位設為 0，最高位進位忽略，這樣就能正確實現 16-bit 二補數加法


## ALU
第一步：zx → x = 0 或 x 保持原樣
Mux16(a=x, b=false, sel=zx, out=x_zeroed)\
sel = 0 → 輸出 x\
sel = 1 → 輸出 b（全 false）→ 16 個 0\
➡ 符合： if (zx == 1) x = 0

第二步：nx → 把 x 取反或保持原樣
Not16(in=x_zeroed, out=x_not);\
Mux16(a=x_zeroed, b=x_not, sel=nx, out=x_in);

sel = 0 → 輸出原本的 x\
sel = 1 → 輸出 !x\
➡ 符合： if (nx == 1) x = !x

對 y 做一模一樣的流程：zy, ny\
Mux16(a=y, b=false, sel=zy, out=y_zeroed);\
Not16(in=y_zeroed, out=y_not);\
Mux16(a=y_zeroed, b=y_not, sel=ny, out=y_in);\
➡ 完整實現 zy 與 ny 的邏輯。

第三步：決定要算 AND 還是 ADD\
Add16(a=x_in, b=y_in, out=x_plus_y);\
And16(a=x_in, b=y_in, out=x_and_y);\
Mux16(a=x_and_y, b=x_plus_y, sel=f, out=out_f);

f=0 → AND\
f=1 → ADD\
➡ 符合：if (f) out = x+y else out = x & y

第四步：是否取反輸出（no）\
Not16(in=out_f, out=out_not);\
Mux16(a=out_f, b=out_not, sel=no, out=out[0..15], out=final_out); \
no=0 → out = out_f\
no=1 → out = !out_f\
最後 out 與 final_out 同步

第五步：判斷輸出是否為負（ng）\
And(a=final_out[15], b=true, out=ng); \
two's complement 數的 MSB 是負號位\
final_out[15] = 1 表示 out < 0\
➡ 符合：ng = (out < 0)

第六步：判斷是否為零（zr）\
Or8Way(in=final_out[0..7], out=or_a);\
Or8Way(in=final_out[8..15], out=or_b);\
Or(a=or_a, b=or_b, out=is_not_zero); \
Not(in=is_not_zero, out=zr);


流程解釋：\
把前 8 bit 做 OR → 看是否有任意 1\
把後 8 bit 做 OR → 看是否有任意 1\
再 OR 一次 → 看整個 16 bits 是否為 0\
取反 → 如果都沒有 1 → zr=1\
➡ 符合：zr = (out == 0 ? 1 : 0)

## Mux16
對於 $\text{Mux16}$ 來說，這個規則必須應用於 $16$ 個位元向量中的每一個對應位元：\
輸出 $out[0]$：只從 $a[0]$ 和 $b[0]$ 中選一\
輸出 $out[1]$：只從 $a[1]$ 和 $b[1]$ 中選一個\
...以此類推輸出\
$out[15]$：只從 $a[15]$ 和 $b[15]$ 中選一個\
由於所有 $16$ 個選擇都由同一個 $\text{sel}$ 訊號控制，所以我們需要 $16$ 個基礎的 $\text{Mux}$ 晶片並行運作，每個晶片負責一個位元

## Bit

步驟 1: 輸出回饋 (Feedback)\
DFF(in=dff_in, out=out, out=prev_out);\
out 埠（即晶片的當前值）同時輸出到一個內部訊號 prev_out
prev_out代表了暫存器在 目前 時鐘週期儲存的值\
步驟 2: 載入決策 (Mux)Mux(a=prev_out, b=in, sel=load, out=dff_in);\
這個 Mux 晶片決定了 DFF 的下一個輸入 dff_in 是什麼

|load|Mux 輸出 dff_in|DFF 在下週期儲存的值|邏輯動作|
|--|--|---------|------------|
|0|prev_out|DFF 儲存它 自己舊的值|保持 (Maintain)：out(t+1)=out(t)|
|1|in|DFF 儲存 新的輸入值|載入 (Load)：out(t+1)=in(t)||

## Register

既然 16 個位元在儲存上是獨立的，我們可以將 $16$ 個最基本的 1 位元儲存單元 ($\text{Bit}$ 晶片) 並排放置\
16 個 Bit 晶片：\
Bit0 負責 [0] 到 out[0]\
Bit1 負責 [1] 到 [1]\
...\
Bit15 負責 15 到 out[15]\
共享 load 訊號：\
load 訊號就像一個總開關，同時連接到所有 $16$ 個 $\text{Bit}$ 晶片的 $\text{load}$ 輸入\
當 $\text{load}=1$ 時，所有 $16$ 個 $\text{Bit}$ 晶片同時載入它們各自的輸入位元\
當 $\text{load}=0$ 時，所有 $16$ 個 $\text{Bit}$ 晶片同時保持它們各自的舊值

## RAM8
1. 寫入機制（載入控制）核心目標： 確保只有地址 ($\text{address}$) 所指向的暫存器，才能在主控訊號 $\text{load}=1$ 時改變內容。其他 $7$ 個暫存器必須保持不變

|元素|連接/功能|備註|
|--|--|------------|
|控制器|DMux8Way|寫入選擇器|
|輸入 (in)|連接到 RAM 的 load 訊號|主控載入訊號|
|選擇 (sel)|連接到 address （3 位元）|決定 8 個暫存器中哪一個被寫入|
|輸出 (w0 到 w7)|分別連接到 8 個 Register 的 load 輸入|只有一條輸出線會變成 1|
|結果|  |只有一個 Register 的 load=1，使其載入新的 in 數據。其他 7 個 Register 的 load=0，保持舊值||

2. 讀取機制（數據輸出）核心目標： 將 $8$ 個暫存器中，地址 ($\text{address}$) 所指向的那個暫存器的內容，傳遞到 $\text{RAM8}$ 的最終輸出 $\text{out}$

|元素|連接/功能|備註|
|--|--|------------|
|控制器|Mux8Way16|讀取選擇器|
|輸入 (i0 到 i7)|分別連接到 8 個 Register 的 16 位元輸出|8 個可能的數據來源|
|選擇 (sel)|連接到 address （3 位元）|決定選擇哪一個暫存器的輸出|
|輸出 (out)|作為 RAM8 的 最終輸出 out|輸出被選中的暫存器內容|
|結果| |Mux8Way16 根據 address 的值，選擇一個 16 位元的暫存器內容作為 RAM8 的輸出||

## RAM64
6 位元的 address 被拆成兩部分：高 3 位（address[3..5]） 用來「選擇哪一個 RAM8」，低 3 位（address[0..2]）用來「選擇該 RAM8 裡的哪一個暫存器」

DMux8Way 依據高 3 位 address，把 load 訊號只送到其中一個 RAM8，確保一次只寫入一個區塊；其他 RAM8 不會被改動。所有 RAM8 都同時接收 in 與低 3 位 address，但只有被選中的那個會真的載入資料

最後用 Mux8Way16，同樣根據高 3 位 address，從 8 個 RAM8 的輸出中選出正確的一個當作 out
這種寫法符合 nand2tetris「由小到大組裝硬體」的設計哲學，結構清楚、可擴充、也容易驗證正確性

## Dmux8Way
首先，最外層的 DMux 用 sel[2]（最高位） 把輸入 in 分成兩大組：

out04：對應輸出 a–d（sel[2] = 0）

out48：對應輸出 e–h（sel[2] = 1）

也就是先決定「要送到前四個還是後四個輸出」

接著，兩個 DMux4Way 再各自用 sel[0..1]（低兩位），在那一組四個輸出中選出真正要輸出的那一個，其餘都為 0
第一個 DMux4Way 產生 a、b、c、d；第二個產生 e、f、g、h

## RAM512
512 個暫存器需要 9 位 address，其中 高 3 位（address[6..8]） 用來選擇 8 個 RAM64 之中的哪一個，低 6 位（address[0..5]） 則用來選擇該 RAM64 裡的某一個暫存器

當 load = 1 時，DMux8Way 依照高 3 位 address，把 load 訊號只送到其中一個 RAM64（l0–l7），確保一次只寫入一個區塊；其他 RAM64 的內容保持不變。所有 RAM64 都同時接收 in 和低 6 位 address，但只有被選中的那一個會真正寫入資料

讀取時，8 個 RAM64 都會輸出各自目前位址的資料，再由 Mux8Way16 根據同樣的高 3 位 address，選出正確的一組 16-bit 資料作為 out

## RAM4K
寫入時，DMux8Way 依照高 3 位 address，把 load 訊號只送到其中一個 RAM512（l0–l7），確保一次只會寫入 4096 個暫存器中的某一個；其他 RAM512 不會被改動

讀取時，8 個 RAM512 都會輸出各自對應位址的資料，再由 Mux8Way16 根據同樣的高 3 位 address，選出正確的一組 16-bit 資料作為 out

## RAM16K
這一層只需要 4 個 RAM4K\
寫入時，DMux4Way 依照高 2 位 address，把 load 訊號只送到其中一個 RAM4K（l0–l3），確保一次只會寫入 16K 中的某一個位置，其餘區塊內容保持不變

讀取時，4 個 RAM4K 都會輸出各自對應位址的資料，再由 Mux4Way16 根據相同的高 2 位 address，選出正確的 16-bit 資料作為 out

## PC

Register 它在每個 clock 都會把 mux_out 存進去，並把目前的值輸出成 out / current_out\
Inc16 先根據目前的值 current_out 算出 current_out + 1，得到 inc_out

接下來三個 Mux16 依序實現控制邏輯：
第一個 Mux 用 inc 決定是「保持原值」還是「加一」\
第二個 Mux 用 load 決定是否改成外部輸入 in\
第三個 Mux 用 reset 決定是否強制輸出 0

因為 Mux 是一層一層接的，後面的 Mux 會覆蓋前面的結果，所以自然形成了題目要求的優先順序：
reset ＞ load ＞ inc ＞ 保持不變。

## Computer
ROM32K
用 pc 當位址，輸出 instruction 給 CPU
→ 負責「取指令」

CPU
讀取 instruction 和 memOut
決定：

要不要寫記憶體（writeM）

寫什麼（outM）

寫哪（addressM）

下一個 pc

Memory
依 CPU 指示讀 / 寫資料，輸出 memOut 回 CPU

所有邏輯都在 CPU 裡，Computer 只負責接線

## CPU
1. 拆解指令（Instruction Decoding）

Hack 指令是 16 位元。

instruction[15]（Opcode）

0 → A 指令（@value），把值送進 A 暫存器

1 → C 指令，其餘位元才有意義

instruction[12]（a-bit）
決定 ALU 第二個輸入：0 用 A，1 用 M

instruction[11:6]
ALU 控制位元（決定運算）

instruction[5:3]（Dest）
決定結果存到 A、D、或 Memory

instruction[2:0]（Jump）
決定是否跳躍

2. A 暫存器管理（A-Register Logic）

A 暫存器有 兩個來源：

A 指令：直接使用指令中的值

C 指令：使用 ALU 的輸出（當 Dest 包含 A）

做法：

用 Mux16：

instruction[15]=0 → 選指令

instruction[15]=1 → 選 ALU 輸出

載入條件（load A）：

是 A 指令

或是 C 指令且 instruction[5]=1

3. ALU 與 D 暫存器

D 暫存器

只接 ALU 輸出

載入條件：C 指令且 instruction[4]=1

ALU 輸入

輸入 X：固定為 D

輸入 Y：用 Mux16 選

instruction[12]=0 → A

instruction[12]=1 → M

ALU 控制：由 instruction[11:6] 決定

4. 跳躍與 PC 控制（Jump Logic）

PC 要決定：

正常遞增（inc）

或跳躍（load A）

ALU 提供：

zr：結果為 0

ng：結果為負

推導：pos = !zr AND !ng

跳躍條件判斷（且必須是 C 指令）：

j1 且 ng → 跳

j2 且 zr → 跳

j3 且 pos → 跳

只要任一成立：
→ PC load = 1，跳到 A 暫存器的位址

## Memory
address[13..14] 決定存取對象

00 / 01 → RAM

10 → Screen

11 → Keyboard

寫入（DMux4Way）
load 只會送到對應的裝置\
RAM 的兩段再用 Or 合成一個 loadRAM

讀取（Mux4Way16）\
依 address[13..14] 選出 RAM / Screen / Keyboard 的輸出

除了老師上課講解的題目外其他都有使用[AI](https://gemini.google.com/app/69dadf1716fcedc7?hl=zh-TW)
