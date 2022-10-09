import operator
from functools import partial

from constants import Instruction
from typing import Protocol, Callable

class Bus(Protocol):
    read_operator: Callable[[str], int | bool]
    write_operator: Callable[[str, int | bool], bool]

class CPU:
    is_stopped: bool
    is_halted: bool
    is_cb: bool
    instructions: dict[int, Instruction]
    cb_instructions: dict[int, Instruction]

    def fetch(self, bus: 'Bus') -> int:
        return bus.read_operator('PC')

    def fetch16(self, bus: 'Bus'):
        return self.fetch(bus) | (self.fetch(bus) << 8)

    def decode(self, opcode: int, cb=False):
        return getattr(self, 'cb_' if cb else '' + 'instructions')[opcode]

    # this type hint is stub, I don't know everything that is going to be returned, and int isn't descriptive enough
    def execute(self, bus: 'Bus', instruction: 'Instruction') -> 'cyles':
        op_code = instruction.op_code
        mnemonic = instruction.mnemonic
        operand1, operand2 = instruction.operand1, instruction.operand2
        flags = instruction.flags

        read_1 = partial(bus.read_operator, operand1)
        read_2 = partial(bus.read_operator, operand2)
        write_1 = partial(bus.write_operator, operand1)
        write_2 = partial(bus.write_operator, operand2)

        def __attempted(failed: bool = False, do_print= True):
            if do_print:
                print( f'{hex(op_code)} | {mnemonic} | {repr(operand1)} {repr(operand2)} | {repr(flags)} | {failed}')

        match instruction.mnemonic:
            case 'NOP':
                pass
            case 'HALT':
                self.is_halted = True
            case 'STOP':
                self.is_stopped = True
            case 'PREFIX':
                self.is_cb = True
            case 'SET':
                write_1(1 << read_2())
            case 'RET':
                __attempted()
            case _:
                pass
                __attempted(True, False)

        return instruction.cycles

    def run(self, bus: 'Bus'):
        while True:
            opcode = self.fetch(bus)
            instruction = self.decode(opcode)
            yield self.execute(bus, instruction)

    def __init__(self, instructions, cb_instructions):
        self.instructions = instructions
        self.cb_instructions = cb_instructions