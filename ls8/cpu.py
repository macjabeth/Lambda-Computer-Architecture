"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, program):
        """Construct a new CPU."""
        self.program = program
        self.branchtable = {}
        self.setup_branchtable()
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def setup_branchtable(self):
        self.branchtable[0b10000010] = self.ldi
        self.branchtable[0b10100010] = self.alu
        self.branchtable[0b01000111] = self.prn
        self.branchtable[0b00000001] = self.hlt

    def load(self):
        """Load a program into memory."""

        address = 0

        for instruction in self.program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

        self.pc += 3

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt(self):
        sys.exit()

    def ldi(self, register, value):
        self.reg[register] = value
        self.pc += 3

    def prn(self, register):
        print(self.reg[register])
        self.pc += 2

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if self.branchtable.get(IR):
                args = []

                if IR == 0b10000010:
                    args = [operand_a, operand_b]
                elif IR == 0b01000111:
                    args = [operand_a]
                elif IR == 0b10100010:
                    args = ['MUL', operand_a, operand_b]

                self.branchtable[IR](*args)
            else:
                print('Unknown instruction:', IR)
