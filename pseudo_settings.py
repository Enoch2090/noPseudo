PSEUDO_INSTR_LEVEL1 = {
    "move":     [["or", "&ops[0]", "&ops[1]", "$zero"]],
    "li":       [["!!lui", "&ops[0]", "&high_bits(ops[1])"],
                 ["ori", "&ops[0]", "&ops[0]", "&low_bits(ops[1])"]],
    "not": [["nor", "&ops[0]", "&ops[1]", "$zero"]],
    "nop": [["sll", "$zero", "$zero", "0"]]
}
PSEUDO_INSTR_LEVEL2 = {
    "bgt":      [["slt", "$at", "&ops[1]", "&ops[0]"],
                 ["bne", "$at", "$zero", "&ops[2]"]],
    "blt":      [["slt", "$at", "&ops[0]", "&ops[1]"],
                 ["bne", "$at", "$zero", "&ops[2]"]],
    "bge":      [["slt", "$at", "&ops[0]", "&ops[1]"],
                 ["beq", "$at", "$zero", "&ops[2]"]],
    "ble":      [["slt", "$at", "&ops[1]", "&ops[0]"],
                 ["beq", "$at", "$zero", "&ops[2]"]]
}

# RULEs:
# 1. Use !! to denote instructions that could be omitted(like lui when the original instruction is li an 16-bit number)
# 2. Use & to denote code to eval. The original instruction is parsed into three parts: string instruction denotes the instuction; array ops denotes the original operators; string comment denotes the comments. For registers, directly use them by name or number.

PSEUDO_INSTR = [PSEUDO_INSTR_LEVEL1, {
    **PSEUDO_INSTR_LEVEL1, **PSEUDO_INSTR_LEVEL2}]
