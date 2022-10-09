import constants
from constants import Instruction
from typing import Protocol, Callable

class Bus(Protocol):
    read_operator: Callable[[str], int | bool]
    write_operator: Callable[[str, int | bool], bool]

class CPU:
    is_stopped: bool
    is_halted: bool
    is_cb: bool
    instruction, cb_instructions = Instruction.load_instructions('op_codes.json').values()

    def fetch(self, bus: 'Bus') -> int:
        return bus.read_operator('PC')

    def fetch16(self, bus: 'Bus'):
        return self.fetch(bus) | (self.fetch(bus) << 8)

    def decode(self, opcode: int, cb=False):
        return getattr(self, 'cb_' if cb else '' + 'instructions')[opcode]

    # this type hint is stub, I don't know everything that is going to be returned, and int isn't descriptive enough
    def execute(self, bus: 'Bus', instruction: 'Instruction') -> 'cyles':
        match instruction.mnemonic:
            case 'NOP':
                pass
            case 'HALT':
                self.is_halted = True
            case 'STOP':
                self.is_stopped = True
            case 'PREFIX':
                self.is_cb = True
            case 'LD' | 'LDI' | 'LDD' | 'LDH':
                bus.write_operator(instruction.operand1, bus.read_operator(instruction.operand2))
            case _:
                print(f'Unknown instruction {instruction.mnemonic} with operands {instruction.operand1} and {instruction.operand2}')
        return instruction.cycles

    def run(self, bus: 'Bus'):
        while True:
            opcode = self.fetch(bus)
            instruction = self.decode(opcode)
            yield self.execute(bus, instruction)
