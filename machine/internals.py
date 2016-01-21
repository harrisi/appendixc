import sys
from machine import util
# from machine import data
import collections

# registers 0-F
registers = collections.OrderedDict([(x, 0) for x in range(0xF + 1)])
# memory cells 0-255
memory = collections.OrderedDict([(x, 0) for x in range(2 ** 8)])
ControlUnit = collections.namedtuple('ControlUnit',
                                     ['operator', 'operand'])
controlunit = (None, None)

# Program counter
# Is set to the location in memory the program is currently at
PC = 0x0
# Instruction register
# is set to the full 16-bit instruction to be executed by the CPU
IR = 0x0

# 0x1
def LOAD(operands): # 12 bits as list
    global registers, memory
    R = operands[:4]
    XY = operands[4:]
    registers[util.getValFromBits(R)] = memory[util.getValFromBits(XY)]

# 0x2
def LOADV(operands):
    global registers
    R = operands[:4]
    XY = operands[4:]
    registers[util.getValFromBits(R)] = util.getValFromBits(XY)

# 0x3
def STORE(operands):
    global memory, registers
    R = operands[:4]
    XY = operands[4:]
    memory[util.getValFromBits(XY)] = registers[util.getValFromBits(R)]

# 0x4
def MOVE(operands): # first four bits ignored
    global registers
    R = operands[4:8]
    S = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)]

# 0x5
# XXX
def ADD(operands): # two's complement
    global registers
    R = operands[:4]
    S = operands[4:8]
    T = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)] + registers[util.getValFromBits(T)]

# 0x6
# XXX
def ADDF(operands): # floating-point
    global registers
    R = operands[:4]
    S = operands[4:8]
    T = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)] + registers[util.getValFromBits(T)]

# 0x7
def OR(operands):
    global registers
    R = operands[:4]
    S = operands[4:8]
    T = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)] | registers[util.getValFromBits(T)]

# 0x8
def AND(operands):
    global registers
    R = operands[:4]
    S = operands[4:8]
    T = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)] & registers[util.getValFromBits(T)]

# 0x9
def XOR(operands):
    global registers
    R = operands[:4]
    S = operands[4:8]
    T = operands[8:]
    registers[util.getValFromBits(R)] = registers[util.getValFromBits(S)] ^ registers[util.getValFromBits(T)]

# 0xA
def ROTATE(operands): # bits 8-12 ignored
    global registers
    R = operands[:4]
    X = operands[8:]
    def rotateHelper(l, n):
        if n == 0:
            return l
        else:
            return rotateHelper([l[-1]] + l[:-1], n - 1)
    registers[util.getValFromBits(R)] = util.getValFromBits(
        rotateHelper(
            util.intToBits(registers[util.getValFromBits(R)], 8),
            util.getValFromBits(X)))
    # print('ROTATE R' + str(util.getValFromBits(R)) + ' ' + str(util.getValFromBits(X)))

# 0xB
def JUMP(operands):
    global registers, PC
    R = operands[:4]
    XY = operands[4:]
    if registers[util.getValFromBits(R)] == registers[0]:
        PC = util.getValFromBits(XY)

# 0xC
def HALT(operands): # operands unused
    sys.exit('HALT')

# 0xD
# meta function (not part of Appendix C's machine)
def PRINT(operands):
    global memory, registers
    R = operands[:4] # register to probe
    XY = operands[4:] # memory cell to probe
    print('R' + str(util.getValFromBits(R)) +
          ': {:#010b}'.format(registers[util.getValFromBits(R)]) +
          '\nCell 0x{:02X}'.format(util.getValFromBits(XY)) +
          ': 0x{:02X}'.format(memory[util.getValFromBits(XY)]))

# operator v-table
opDict = {0x1: LOAD,   # LOAD R XY (contents)
          0x2: LOADV,  # LOADV R #XY (value)
          0x3: STORE,  # STORE R XY
          0x4: MOVE,   # MOVE R R
          0x5: ADD,    # ADD R ST (two's complement)
          0x6: ADDF,   # ADDF R ST (floating-point)
          0x7: OR,     # OR R R R
          0x8: AND,    # AND R R R
          0x9: XOR,    # XOR R R R
          0xA: ROTATE, # ROTATE R #
          0xB: JUMP,   # JUMP R XY
          0xC: HALT,   # HALT
          0xD: PRINT,  # PRINT R XY
          0xE: None,
          0xF: None}
    
def storeProgramInMemory(loc):
    instructions = util.readFromFile(loc)
    i = 0
    for instruction in instructions:
        memory[PC + i] = instruction
        i += 1
