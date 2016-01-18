import sys
import re

# Gets integer value from list of bits
def getValFromBits(bits):
    vals = [2 ** a for a in range(0, len(bits))]
    vals.reverse() # bad
    return sum([a * b for (a, b) in zip(bits, vals)])

def operatorToFunction(op): # [list of four elements in {0, 1}]
    opVal = sum([a * b for (a, b) in zip(op, [8, 4, 2, 1])])
    if not(0x1 <= opVal <= 0xD):
        sys.exit('operator doesn\'t exist')
    return opVal

def readFromFile(loc):
    res = []
    with open(loc, 'r') as f:
        for line in f:
            line = re.sub(';;.*', '', line)
            line = re.sub('[\s+]', '', line)
            if line:
                res.append(line[:2])
                res.append(line[2:])
    return res
