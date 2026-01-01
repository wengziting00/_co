import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Usage: VMTranslator.py <inputfile.vm or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        # 多檔案模式
        vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        code_writer = CodeWriter(os.path.join(input_path, os.path.basename(input_path) + '.asm'))
        # Bootstrap code for Chapter 8
        code_writer.write_init()
        for vm_file in vm_files:
            parser = Parser(os.path.join(input_path, vm_file))
            code_writer.set_file_name(vm_file)
            while parser.has_more_commands():
                parser.advance()
                cmd_type = parser.command_type()
                if cmd_type == 'C_ARITHMETIC':
                    code_writer.write_arithmetic(parser.arg1())
                elif cmd_type in ('C_PUSH', 'C_POP'):
                    code_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
                elif cmd_type == 'C_LABEL':
                    code_writer.write_label(parser.arg1())
                elif cmd_type == 'C_GOTO':
                    code_writer.write_goto(parser.arg1())
                elif cmd_type == 'C_IF':
                    code_writer.write_if(parser.arg1())
                elif cmd_type == 'C_FUNCTION':
                    code_writer.write_function(parser.arg1(), parser.arg2())
                elif cmd_type == 'C_CALL':
                    code_writer.write_call(parser.arg1(), parser.arg2())
                elif cmd_type == 'C_RETURN':
                    code_writer.write_return()
        code_writer.close()
    else:
        # 單檔模式
        parser = Parser(input_path)
        out_file = input_path.replace('.vm', '.asm')
        code_writer = CodeWriter(out_file)
        code_writer.set_file_name(os.path.basename(input_path))
        # Bootstrap for Chapter 8 only if you want
        code_writer.write_init()
        while parser.has_more_commands():
            parser.advance()
            cmd_type = parser.command_type()
            if cmd_type == 'C_ARITHMETIC':
                code_writer.write_arithmetic(parser.arg1())
            elif cmd_type in ('C_PUSH', 'C_POP'):
                code_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
            elif cmd_type == 'C_LABEL':
                code_writer.write_label(parser.arg1())
            elif cmd_type == 'C_GOTO':
                code_writer.write_goto(parser.arg1())
            elif cmd_type == 'C_IF':
                code_writer.write_if(parser.arg1())
            elif cmd_type == 'C_FUNCTION':
                code_writer.write_function(parser.arg1(), parser.arg2())
            elif cmd_type == 'C_CALL':
                code_writer.write_call(parser.arg1(), parser.arg2())
            elif cmd_type == 'C_RETURN':
                code_writer.write_return()
        code_writer.close()

if __name__ == "__main__":
    main()
