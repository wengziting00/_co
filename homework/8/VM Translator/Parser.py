class Parser:
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.current_command = None
        self.lines = [line.strip() for line in self.file if line.strip() and not line.startswith('//')]
        self.current_index = -1
        self.file.close()

    def has_more_commands(self):
        return self.current_index + 1 < len(self.lines)

    def advance(self):
        self.current_index += 1
        self.current_command = self.lines[self.current_index].split('//')[0].strip()

    def command_type(self):
        if self.current_command.startswith('push'):
            return 'C_PUSH'
        elif self.current_command.startswith('pop'):
            return 'C_POP'
        elif self.current_command in ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'):
            return 'C_ARITHMETIC'
        elif self.current_command.startswith('label'):
            return 'C_LABEL'
        elif self.current_command.startswith('goto'):
            return 'C_GOTO'
        elif self.current_command.startswith('if-goto'):
            return 'C_IF'
        elif self.current_command.startswith('function'):
            return 'C_FUNCTION'
        elif self.current_command.startswith('call'):
            return 'C_CALL'
        elif self.current_command.startswith('return'):
            return 'C_RETURN'
        else:
            return 'C_UNKNOWN'

    def arg1(self):
        if self.command_type() == 'C_ARITHMETIC':
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self):
        parts = self.current_command.split()
        if len(parts) >= 3:
            return int(parts[2])
        else:
            return None
