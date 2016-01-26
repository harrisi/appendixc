import sys
import collections
from machine import internals
from machine import util
from machine import registers
import argparse
import pprint

def fetch():
    instruction = ("0x" +
                   format(internals.memory[internals.PC]) +
                   format(internals.memory[internals.PC + 1]))
    internals.IR = int(instruction, 0)
    internals.PC += 2

def decode():
    bits = util.intToBits(internals.IR, 16)
    internals.controlunit = (bits[:4], bits[4:])

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
        if res in 'cC':
            break
        elif res in 'mM':
            pprint.pprint(collections.OrderedDict(
                [('0x{:02X}'.format(h),
                  '0x{:02X}'.format(int('0x' + str(v), 16)))
                 for (h, v) in internals.memory.items()
                 if not(v is 0)]))
            continue
        elif res in 'rR':
            pprint.pprint(collections.OrderedDict(
                [('0x{:02X}'.format(h),
                  '0x{:02X}'.format(v))
                 for (h, v) in internals.registers.items()
                 if not(v is 0)]))
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
    parser.add_argument("-a", "--assembly",
                        help="read assembly rather than machine code")
    args = parser.parse_args()
    if args.start:
        internals.PC = args.start
    if args.program:
        internals.storeProgramInMemory(args.program)
    elif args.assembly:
        foo = util.readAsm(args.assembly)
        fooMachine = args.assembly.split('.')[0] + '.machine'
        util.spitMachine(foo, fooMachine)
        internals.storeProgramInMemory(fooMachine)
    else:
        internals.storeProgramInMemory("out.machine")
    
    DEBUG = args.debug
    while True:
        breakpoint('pre fetch')
        fetch()
        breakpoint('pre decode')
        decode()
        breakpoint('pre execute')
        execute()
