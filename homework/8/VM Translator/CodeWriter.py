class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.file_name = ''
        self.label_counter = 0
        self.current_function = ''

    def set_file_name(self, filename):
        self.file_name = filename.split('.')[0]

    def write_init(self):
        # Chapter 8 bootstrap code
        self.file.write("// Bootstrap code\n")
        self.file.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, command):
        # 這邊示範 add，其他自己寫
        if command == 'add':
            self.file.write("// add\n")
            self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n")
        # 其他算術指令要補

    def write_push_pop(self, cmd, segment, index):
        # 簡單示範常用段的 push pop
        if cmd == 'C_PUSH':
            if segment == 'constant':
                self.file.write(f"// push constant {index}\n")
                self.file.write(f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'local':
                self.file.write(f"// push local {index}\n")
                self.file.write(f"@LCL\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            # 其他段落請自行補
        elif cmd == 'C_POP':
            if segment == 'local':
                self.file.write(f"// pop local {index}\n")
                self.file.write(f"@LCL\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n")
                self.file.write(f"@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            # 其他段落請自行補

    # 這邊要補 Chapter 8 新增指令
    def write_label(self, label):
        label_name = f"{self.current_function}${label}"
        self.file.write(f"({label_name})\n")

    def write_goto(self, label):
        label_name = f"{self.current_function}${label}"
        self.file.write(f"@{label_name}\n0;JMP\n")

    def write_if(self, label):
        label_name = f"{self.current_function}${label}"
        self.file.write("// if-goto\n")
        self.file.write("@SP\nAM=M-1\nD=M\n")
        self.file.write(f"@{label_name}\nD;JNE\n")

    def write_function(self, function_name, num_locals):
        self.current_function = function_name
        self.file.write(f"({function_name})\n")
        for _ in range(num_locals):
            self.file.write("@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def write_call(self, function_name, num_args):
        return_label = f"{function_name}$ret.{self.label_counter}"
        self.label_counter += 1
        self.file.write(f"// call {function_name} {num_args}\n")
        self.file.write(f"@{return_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        for seg in ("LCL", "ARG", "THIS", "THAT"):
            self.file.write(f"@{seg}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.file.write(f"@SP\nD=M\n@{num_args + 5}\nD=D-A\n@ARG\nM=D\n")
        self.file.write(f"@SP\nD=M\n@LCL\nM=D\n")
        self.file.write(f"@{function_name}\n0;JMP\n")
        self.file.write(f"({return_label})\n")

    def write_return(self):
        self.file.write("// return\n")
        # FRAME = LCL (R13)
        self.file.write("@LCL\nD=M\n@R13\nM=D\n")
        # RET = *(FRAME - 5) (R14)
        self.file.write("@5\nA=D-A\nD=M\n@R14\nM=D\n")
        # *ARG = pop()
        self.file.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        # SP = ARG + 1
        self.file.write("@ARG\nD=M+1\n@SP\nM=D\n")
        # Restore THAT
        self.file.write("@R13\nAM=M-1\nD=M\n@THAT\nM=D\n")
        # Restore THIS
        self.file.write("@R13\nAM=M-1\nD=M\n@THIS\nM=D\n")
        # Restore ARG
        self.file.write("@R13\nAM=M-1\nD=M\n@ARG\nM=D\n")
        # Restore LCL
        self.file.write("@R13\nAM=M-1\nD=M\n@LCL\nM=D\n")
        # goto RET
        self.file.write("@R14\nA=M\n0;JMP\n")

    def close(self):
        self.file.close()
