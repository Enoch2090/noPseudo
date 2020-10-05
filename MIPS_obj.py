import re
import os
from pseudo_settings import PSEUDO_INSTR


def low_bits(constant_str):
    if not("0x" in constant_str):
        hex_str = str(hex(int(constant_str) & 0x0000FFFF))
        return hex_str.replace("0x", "0x"+"0"*(6-len(hex_str)))
    else:
        hex_str = str(hex(int(constant_str, 16) & 0x0000FFFF))
        return hex_str.replace("0x", "0x"+"0"*(6-len(hex_str)))


def high_bits(constant_str):
    if not("0x" in constant_str):
        hex_str = str(hex(int(constant_str) & 0xFFFF0000))
        return hex_str.replace("0x", "0x"+"0"*(6-len(hex_str)))[0:5]
    else:
        hex_str = str(hex(int(constant_str, 16) & 0xFFFF0000))
        return hex_str.replace("0x", "0x"+"0"*(6-len(hex_str)))[0:5]


class MIPS_obj(object):
    def __init__(self, filename, translate_level=2):
        self.op_lines = []
        self.code = ""
        self.line_cnt = 0
        self.translated_instr = 0
        self.translation_expand = 0
        self.translate_level = translate_level
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.op_lines = lines
        else:
            raise FileNotFoundError
        if len(self.op_lines) == 0:
            self.code = "No instructions."
            self.line_cnt = 0
        else:
            for line in self.op_lines:
                self.code += line
            self.line_cnt = len(self.op_lines)
        return

    def __str__(self):
        return self.code

    def update_code(self):
        self.code = ""
        self.line_cnt = len(self.op_lines)
        for line in self.op_lines:
            self.code += line
        return self.code

    def remove_pseudo(self, print_log=False):
        self.translated_instr = 0
        self.translation_expand = 0
        new_lines = []
        for line in self.op_lines:
            ops = line.split(",")
            ops_all = []
            op_temp = ""
            if len(ops[0].split("\t")) == 1:  # User used space.
                op_temp = ops[0].split(" ")
            else:  # User used tab. Awesome!
                op_temp = ops[0].split("\t")
            instruction = op_temp[0]
            if instruction in PSEUDO_INSTR[self.translate_level-1].keys():
                op_temp = list(filter(lambda x: x != "", op_temp))
                ops_all.append(op_temp[1])
                ops_all += ops[1::]
                ops = []
                for op in ops_all:
                    ops.append(
                        re.sub(r'[\s]*', "", re.sub(r'\#[\S\s]*', "", op)))
                comment = ""
                try:
                    comment = re.search(r'\#[\S\s]*', line).group(0)
                except AttributeError:
                    pass
                translation_set = PSEUDO_INSTR[self.translate_level-1][instruction]
                translated_line = ""
                self.translated_instr += 1
                for translated_instruction in translation_set:
                    if "!!" in translated_instruction[0]:
                        if (('0x' in ops[-1] and int(ops[-1], 16) <= 65535) or (not '0x' in ops[-1] and int(ops[-1]) <= 65535)):
                            continue
                    self.translation_expand += 1
                    for translated_op in translated_instruction:
                        translated_line += (eval(translated_op.replace("&", ""))) if (
                            "&" in translated_op) else (translated_op)
                        translated_line += " "
                    translated_line += comment + "\n"
                new_lines.append(translated_line)
            else:
                new_lines.append(line)
        self.op_lines = new_lines
        self.update_code()
        if print_log:
            print("Translation done.")
            print(self.get_info())
        return

    def to_file(self, filename, print_log=False):
        with open(filename, 'w') as f:
            f.write(self.code)
        if print_log:
            print("File saved to %s" % filename)
        return True

    def reset_level(self, new_translate_level):
        if new_translate_level == 1 or new_translate_level == 2:
            self.translate_level = new_translate_level
            return True
        else:
            print("Translate level must be 1 or 2.")
            return False

    def get_info(self):
        info = "Total %s lines. Expanded %s lines of pseudo-instructions into %s lines of instructions." % (
            self.line_cnt, self.translated_instr, self.translation_expand)
        return info
