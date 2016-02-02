# appendixc
Basic VM implemented in Python

# What is it?
A simple, 15 register, 12 (13 including a "meta" printing instruction) instruction, with 256 8-bit memory cells. It is capable of a number of real programs.

# Why?
For fun! As a first year CS student, I wanted to implement a simple machine that was described in [Computer Science: An Overview (12th Edition)](http://www.amazon.com/Computer-Science-Overview-12th-Edition/dp/0133760065) (Appendix C). I thought it would be an interesting way to get a better understanding of the concepts described.

# How does one use it?
Very carefully! The machine described has instructions encoded as 16-bit binary data. The four most significant bits are used for the operator, and the last 12 for the operands. These can be encoded in hexadecimal machine instructions. But that's no fun to work with! So I also implemented a very crude assembler. This makes it much easier to write programs, which I find nice. I also have it emit the valid machine instructions which will be run, with the original assembly at the end of each line.

Example (`foo.iasm`):

    ;; Start A4
    LOADV R0 00
    LOADV R1 03
    LOADV R2 01
    JUMP R1 B0
    ADD R0 R2 R0
    JUMP R0 AA
    HALT

This will output a file such as the following (`foo.machine`):

    2000 ;; LOADV R0 00
    2103 ;; LOADV R1 03
    2201 ;; LOADV R2 01
    B1B0 ;; JUMP R1 B0
    5020 ;; ADD R0 R2 R0
    B0AA ;; JUMP R0 AA
    C000 ;; HALT

The above is the actual set of instructions to be run by the machine. The program will loop three times and then `HALT`.

To run the above program (as an `.iasm`):

    python3 implementation.py -s 0xA4 -a foo.iasm

The option `-s` is to start the starting location of the program in memory. The `-a` flag is to denote an assembly file. (If one is interested, the `-p` flag can be used to run a machine program.)

# License
Refer to file: `LICENSE`.
