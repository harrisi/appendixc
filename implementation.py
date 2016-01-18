import sys
import collections
from machine import internals
from machine import util
import argparse

def fetch():
    instruction = ("0x" +
                   format(internals.memory[internals.PC]) +
                   format(internals.memory[internals.PC + 1]))
    internals.IR = int(instruction, 0)
    internals.PC += 2

def decode():
    bits = [] # bad
    for bit in format(internals.IR, '016b'): # bad (?)
        bits.append(bit)
    bits = [int(bit) for bit in bits] # bad
    internals.controlunit = (bits[:4], bits[4:])
    # internals.controlunit.operator = bits[:4]
    # internals.controlunit.operand = bits[4:]
    # operator = bits[:4] # first four bits
    # operand = bits[4:] # last 12 bits

def execute():
    f = internals.opDict[
        util.operatorToFunction(internals.controlunit[0])]
    o = internals.controlunit[1]
    f(o)

DEBUG = False

def breakpoint(label):
    if not(DEBUG):
        return
    print(label.upper())
    print('PC: 0x%X' % internals.PC)
    print('IR: 0x%X' % internals.IR)
    print('CU: ' + str(internals.controlunit))
    while True:
        res = input('(C)ontinue, (M)emory, (R)egisters, (H)alt:\n(C)> ')
        # if res is '':
        #     continue
        if res in 'cC':
            break
        elif res in 'mM':
            print(internals.memory)
            continue
        elif res in 'rR':
            print(internals.registers)
            continue
        elif res in 'hH':
            sys.exit('(breakpoint) HALT')
        else:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start",
                        help="starting location for program in memory",
                        type=(lambda i: int(i, 0)))
    parser.add_argument("-p", "--program",
                        help="location of program on host machine")
    parser.add_argument("-d", "--debug",
                        help="add debug points between each step of machine cycle",
                        action="store_true")
    args = parser.parse_args()
    if args.start:
        # print('0x%X' % args.start) # bad
        internals.PC = args.start
    if args.program:
        internals.storeProgramInMemory(args.program)
    else:
        internals.storeProgramInMemory("out.machine")
    DEBUG = args.debug
    while True:
        breakpoint('pre fetch')
        fetch()
        # breakpoint('post fetch')
        breakpoint('pre decode')
        decode()
        # breakpoint('post decode')
        breakpoint('pre execute')
        execute()
        # breakpoint('post execute')
