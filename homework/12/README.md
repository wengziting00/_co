# 都是使用

# 第六章
用高階語言（如 Python、Java 或 C++）將 Hack 組合語言（.asm）轉換成 Hack 電腦可執行的 16 位元機器碼（.hack）。在前五章中，學生已經完成 Hack 電腦的硬體設計，但電腦只能理解 0 與 1，因此第六章的目的就是在軟體層面建立「人類可讀程式」與「硬體可執行指令」之間的橋樑。此專案需要支援三種語法：A 指令（如 @21、@i）、C 指令（dest=comp;jump）以及標籤（(LABEL)），並採用兩遍掃描（two-pass assembler）：第一遍掃描用來記錄所有標籤對應的 ROM 位址，第二遍掃描則負責將每一行指令實際翻譯成二進位碼，同時處理符號查表與變數配置（從 RAM 位址 16 開始）。完成第六章後，學生能理解 CPU 指令的編碼方式、符號表的用途，以及組譯器在整個電腦系統中的角色，這也是後續 VM 與高階語言編譯章節的重要基礎。


# 第七章
1. 虛擬機（VM）的角色：中介層
在 Nand2Tetris 的架構中，直接將高階語言（如 Jack）編譯成機器碼非常困難。因此，作者引入了一個虛擬機層（VM Layer）。

高階語言（Jack）先編譯成 VM 程式碼（.vm 檔）。

VM 程式碼 再經由你的 VM Translator 轉換為 Hack 組合語言（.asm 檔）。

最後由第 6 章的組譯器轉為 機器碼。

這種類似 Java (Bytecode) 或 .NET (MSIL) 的設計，讓編譯器變得模組化且易於實作。

2. 堆疊架構（Stack-based Computing）
第 7 章定義了一種「堆疊式」的運算模型。所有的運算都發生在堆疊上：

算術運算：例如執行 add 時，VM 會從堆疊頂端彈出（pop）兩個數字，相加後再壓回（push）堆疊。

邏輯比較：如 eq、gt、lt，比較結果為真時壓入 -1 (True)，否則壓入 0 (False)。

這章要求你實作 9 個算術與邏輯指令： add, sub, neg, eq, gt, lt, and, or, not

3. 記憶體區段（Memory Segments）
這是第 7 章最具挑戰性的部分。VM 抽象出了多個「記憶體區段」，讓程式碼能處理變數：

local, argument, this, that：對應到 RAM 的不同區塊。

pointer, temp：固定位置的暫存區。

static：靜態變數（如你之前提供的 StaticTest.vm）。

constant：偽區段，純粹用來產生數值。

你必須撰寫程式碼，將 push argument 0 這種邏輯指令，轉換成 Hack Assembly 中複雜的 A, D, M 暫存器操作。

# 第八章
1. 流程控制 (Program Flow)
這是相對簡單的部分，你必須實作三個指令：

label symbol：定義一個位置。

goto symbol：無條件跳轉。

if-goto symbol：若堆疊頂端的值不為 0（True），則跳轉。

實作細節： 這些指令會被轉換成 Hack Assembly 的 @symbol 與 JMP 或 JNE 指令。

2. 函式呼叫與堆疊幀 (The Function Stack Frame)
這是全書最精彩也最燒腦的地方。當程式執行 call FunctionName nArgs 時，你必須在堆疊中建立一個 「框架 (Frame)」。

為了讓函式執行完後能順利「回到過去」，你必須在堆疊裡存下：

Return Address：回來的路徑。

LCL, ARG, THIS, THAT：呼叫者的記憶體狀態。

這意味著當一個函式被呼叫時，堆疊會長這樣：

[傳入的參數]

[返回地址]

[舊的 LCL]

[舊的 ARG]

[舊的 THIS]

[舊的 THAT]

新函式的 LCL 指標從這裡開始

3. 函式返回 (Return Logic)
return 是第 8 章最難寫的 Assembly 模板。你必須：

把函式的傳回值放到 ARG[0] 的位置（這會變成呼叫者看到的堆疊頂端）。

恢復呼叫者的 SP, LCL, ARG, THIS, THAT。

跳轉回之前存下的 Return Address。

4. 引導程式 (Bootstrap Code)
在第 7 章，我們是手動設定 SP=256。但在第 8 章，你的 Translator 必須自動產生一段 啟動碼：

將 SP 初始化為 256。

呼叫 Sys.init（這是所有 Jack 程式的進入點，相當於 C 或 Java 的 main）。

# 第九章
第九章其實就是在用你前面章節做好的整套電腦，第一次寫「真正能跑的高階程式」：你用 Jack 語言寫一個完整小程式（像 Square），透過 OS 的 Screen、Keyboard 等 class 來畫畫面、讀鍵盤，而不用管底層 CPU、VM 怎麼實作；重點不是功能多強，而是證明你懂 Jack 的語法、物件、方法、迴圈與條件判斷，為後面第十、十一章自己寫編譯器做準備。

# 第十章
第十章是在寫「Jack 編譯器的前半段」：你要把第九章學會寫的 Jack 程式，讀進來並分析它的語法結構，把程式拆成 token（關鍵字、符號、變數、常數），再依照語法規則組成對應的結構（parse tree / XML），確認「這個程式語法是合法的」，但還不負責產生 VM code；簡單說，第十章是在教你怎麼讓電腦「看得懂 Jack 在寫什麼」，為第十一章真正翻譯成可執行指令做準備。

# 第十一章
第十一章則是把這個編譯器升級成 完整 Jack-to-VM 編譯器，也就是說，它要做的事情是：

讀入 Jack 程式（class、method、function、變數、表達式…）

分析語法結構（沿用第十章的編譯器方法）

生成對應的 VM 指令：

將變數、運算、控制流程（if、while）、方法呼叫、返回等，翻譯成 一系列虛擬機碼

這些 VM 指令是中間語言，可以用第七章做的 VM Translator 再轉成 Hack Assembly

保留程序邏輯：最終的 VM 程式能在 Hack CPU 模擬器上運行，實際控制螢幕或讀鍵盤，像第九章寫的 Square 程式一樣可以動

核心概念是 「語法分析 + 指令生成」：

每個 Jack 的語法單元（class、method、statement、expression）都對應到一組 VM 指令

你要寫的編譯器不是只做「文字轉換」，而是 保證程式邏輯正確、變數正確對應段（local, argument, static, this）

包括方法呼叫、返回值、算術運算、條件跳轉，全部都要生成 VM 代碼

# 第十二章
第 12 章「The Operating System」 的任務是為你親手建造的 Hack 電腦撰寫一個作業系統 (OS)。

在之前的章節，你已經有了硬體、組譯器、虛擬機和編譯器。但如果你想在螢幕上印一個數字，或者做乘法運算，你得寫幾百行代碼。第 12 章的目標就是把這些常用的功能封裝成 Jack 標準函式庫，讓開發者可以直接呼叫 Math.multiply() 或 Screen.drawCircle()。

這章你會用 Jack 語言 實作 8 個核心類別：

1. 數學運算 (Math.jack)
Hack 硬體只會做加法和減法。

挑戰：實作乘法與除法演算法（使用二進位效率優化，而非連加法）。

重點：實作 Math.sqrt（平方根），通常使用二分搜尋法來達成。

2. 記憶體管理 (Memory.jack)
這是在軟體層級實作 peek 和 poke，並管理堆積區 (Heap)。

挑戰：實作 alloc 和 dealloc。你必須維護一個 空閒清單 (Free List)。

重點：當呼叫 Memory.alloc(size) 時，OS 要找到足夠大的記憶體塊並分配出去；當呼叫 dealloc 時，要將其回收。

3. 圖形顯示 (Screen.jack)
這是最「有感」的一部分。你必須操作螢幕的記憶體映射區（Memory Map）。

挑戰：

畫線：實作 Bresenham's Algorithm（或是類似的直線演算法），僅使用加減法來畫出斜線。

畫圓：利用勾股定理計算出每一橫排需要塗黑的像素。

優化：直接操作 16 位元的暫存器（而非一個個像素點），能大幅提升繪圖速度。

4. 文字輸出 (Output.jack)
如何把字元（如 'A'）顯示在螢幕上？

核心：OS 內建了一張 點陣字體表 (Font Map)。當你想印出 'A'，OS 會查表找到對應的像素圖案，然後把這 8x11 的像素塊塗黑。

功能：管理游標位置（行列）、自動換行以及滾動螢幕。

5. 字串與陣列 (String.jack, Array.jack)
String：實作字串的動態擴展、整數轉字串（itoa）以及字串轉整數（atoi）。

Array：這是最簡單的，基本上就是呼叫 Memory.alloc。

6. 鍵盤輸入 (Keyboard.jack)
功能：讀取鍵盤暫存器的內容，並提供好用的函式如 readInt（讀取整數輸入）或 readLine（讀取整行文字）。

7. 系統控制 (Sys.jack)
功能：

Sys.init()：整個系統的啟動點。它會依序呼叫各個 OS 類別的 init 方法，最後呼叫 Main.main()。

Sys.wait(duration)：實作一個計時迴圈。

Sys.halt()：進入無限迴圈，代表程式結束。
