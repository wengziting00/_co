import sys
import os

class HackAssembler:
    def __init__(self):
        # 1. 預定義符號表
        self.symbol_table = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576
        }
        for i in range(16):
            self.symbol_table[f"R{i}"] = i
        
        self.next_variable_address = 16

        # 2. C-指令對照表
        self.dest_map = {
            None: "000", "M": "001", "D": "010", "MD": "011",
            "A": "100", "AM": "101", "AD": "110", "AMD": "111"
        }
        self.jump_map = {
            None: "000", "JGT": "001", "JEQ": "010", "JGE": "011",
            "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
        }
        self.comp_map = {
            "0": "0101010", "1": "0111111", "-1": "0111010",
            "D": "0001100", "A": "0110000", "!D": "0001101",
            "!A": "0110001", "-D": "0001111", "-A": "0110011",
            "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
            "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
            "A-D": "0000111", "D&A": "0000000", "D|A": "0010010",
            "M": "1110000", "!M": "1110001", "-M": "1110011",
            "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
            "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
            "D|M": "1010010"
        }

    def clean_line(self, line):
        """移除註解與空白"""
        line = line.split("//")[0]
        return line.strip()

    def assemble(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # 第一階段：處理標籤 (L-Instructions)
        instructions = []
        rom_address = 0
        for line in lines:
            cleaned = self.clean_line(line)
            if not cleaned: continue
            
            if cleaned.startswith("(") and cleaned.endswith(")"):
                label = cleaned[1:-1]
                self.symbol_table[label] = rom_address
            else:
                instructions.append(cleaned)
                rom_address += 1

        # 第二階段：轉換為二進位
        binary_output = []
        for line in instructions:
            if line.startswith("@"):
                binary_output.append(self.handle_a_instruction(line))
            else:
                binary_output.append(self.handle_c_instruction(line))
        
        return binary_output

    def handle_a_instruction(self, line):
        value = line[1:]
        if value.isdigit():
            address = int(value)
        else:
            if value not in self.symbol_table:
                self.symbol_table[value] = self.next_variable_address
                self.next_variable_address += 1
            address = self.symbol_table[value]
        return format(address, '016b')

    def handle_c_instruction(self, line):
        # 解析 dest=comp;jump
        temp = line
        dest, jump = None, None
        
        if "=" in temp:
            dest, temp = temp.split("=")
        if ";" in temp:
            comp, jump = temp.split(";")
        else:
            comp = temp
            
        return f"111{self.comp_map[comp]}{self.dest_map[dest]}{self.jump_map[jump]}"

# --- 執行部分 ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式: python assembler.py YourFile.asm")
    else:
        asm_file = sys.argv[1]
        assembler = HackAssembler()
        results = assembler.assemble(asm_file)
        
        output_file = asm_file.replace(".asm", ".hack")
        with open(output_file, 'w') as f:
            f.write("\n".join(results) + "\n")
        print(f"轉換完成！已生成: {output_file}")
