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

