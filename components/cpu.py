from functools import partial

from components.system_mappings import Instruction
from protocols import Bus, Timer


class CPU:
    """The CPU of the Gameboy"""
    is_stopped: bool
    is_halted: bool
    instructions: dict[int, Instruction]
    cb_instructions: dict[int, Instruction]
    is_cb: bool = False
    interrupts_enabled = False

    def decode(self, opcode: int, cb=False):
        """Check if this is a CB prefixed instruction,
        if so, return the CB instruction if not return the normal instruction,
        since these have already been mapped, is simply a lookup"""
        decoded = getattr(self, ('cb_' if cb else '') + 'instructions')[opcode]
        if self.is_cb:
            self.is_cb = False
        return decoded

    def execute(self, bus: 'Bus', instruction: 'Instruction') -> int:
        # likely needs to return more values, but stubbed for now
        """Uses pattern matching to execute the instruction"""
        op_code = instruction.op_code
        mnemonic = instruction.mnemonic
        operand1, operand2 = instruction.operand1, instruction.operand2
        flags = instruction.flags

        read_1 = partial(bus.read, operand1)
        read_2 = partial(bus.read, operand2)
        write_1 = partial(bus.write, operand1)

        match instruction.mnemonic:
            case 'NOP':
                """No operation"""
            case 'HALT':
                """Halt CPU & LCD display until button pressed"""
                # this has some funky logic as I understand it
                self.is_halted = True
            case 'STOP':
                """Stop CPU & LCD display until button pressed"""
                # this has some funky logic as I understand it
                self.is_stopped = True
            case 'PREFIX':
                """Prefix CB"""
                self.is_cb = True
            case 'SET':
                """Set bit n in register r"""
                write_1(read_1() | (1 << op_code & 0b111))
            case 'CALL' | 'RET' | 'RETI' | 'RETN' | 'RST':
                """Call address nn"""
                bus.write('SP', bus.read('SP') + 2)
            case 'JP':
                """Jump to address"""
                bus.write('PC', read_1())
            case 'JR':
                """Jump to address relative to current address if condition is met"""
                if read_2() or operand2 is None:
                    bus.write('PC', bus.read('PC') + read_1())
            case 'DI' | 'EI':
                """Disable/enable interrupts"""
                self.interrupts_enabled = op_code == 0xF3
            case 'SWAP':
                """Swap upper & lower nibbles of register"""
                write_1((read_1() << 4) | (read_1() >> 4))
            case 'BIT':
                """Test bit n in register r"""
                bus.write('F', (bus.read('F') & 0b11110000) | (1 << 4) | (
                        read_1() & (1 << op_code & 0b111)))
            case 'RES':
                """Reset bit n in register r"""
                write_1(read_1() & ~(1 << op_code & 0b111))
            case 'RLC' | 'RRC':
                """Rotate register left/right"""
                if mnemonic[1] == 'L':
                    write_1((read_1() << 1) | (read_1() >> 7))
                else:
                    write_1((read_1() >> 1) | (read_1() << 7))
            case 'RL' | 'RR':
                """Rotate register left/right through carry"""
                if mnemonic[1] == 'L':
                    write_1((read_1() << 1) | (bus.read('F') & 1))
                else:
                    write_1((read_1() >> 1) | (bus.read('F') & 1))
            case 'SLA' | 'SRA':
                """Shift register left/right arithmetically"""
                if mnemonic[1] == 'L':
                    write_1((read_1() << 1) | (read_1() >> 7))
                else:
                    write_1((read_1() >> 1) | (read_1() & 0b10000000))
            case 'SRL':
                """Shift register right"""
                write_1((read_1() >> 1) | (read_1() & 0b10000000))
            case 'RLCA' | 'RRCA' if operand1 is None and operand2 is None:
                """Rotate A left/right"""
                if mnemonic[2] == 'L':
                    bus.write('A', (bus.read('A') << 1) | (bus.read('A') >> 7))
                else:
                    bus.write('A', (bus.read('A') >> 1) | (bus.read('A') << 7))
            case 'RLA' | 'RRA':
                """Rotate A left/right through carry"""
                if mnemonic[2] == 'L':
                    bus.write('A', (bus.read('A') << 1) | (bus.read('F') & 1))
                else:
                    bus.write('A', (bus.read('A') >> 1) | (bus.read('F') & 1))
            case 'DAA':
                """Decimal adjust register A"""
                if bus.read('F') & 0b10000000:
                    if bus.read('F') & 0b10000:
                        bus.write('A', bus.read('A') - 0x60)
                    if bus.read('F') & 0b1000:
                        bus.write('A', bus.read('A') - 0x6)
                else:
                    if bus.read('F') & 0b10000 or bus.read('A') > 0x99:
                        bus.write('A', bus.read('A') + 0x60)
                        bus.write('F', bus.read('F') | 0b10000)
                    if bus.read('F') & 0b1000 or (bus.read('A') & 0x0F) > 0x09:
                        bus.write('A', bus.read('A') + 0x6)
            case 'CPL':
                """Complement register A"""
                bus.write('A', ~bus.read('A'))
            case 'CCF':
                """Complement carry flag"""
                bus.write('F', bus.read('F') ^ 0b10000)
            case 'SCF':
                """Set carry flag"""
                bus.write('F', bus.read('F') | 0b10000)
            case 'LD' | 'LDH' | 'LDI' | 'LDD':
                """Load register r2 into register r1"""
                write_1(read_2())
            case 'PUSH':
                bus.write('SP', bus.read('SP') - 2)
                bus.write('SP', read_1())
            case 'POP':
                write_1(bus.read('SP'))
                bus.write('SP', bus.read('SP') + 2)
            case 'ADD':
                write_1(read_1() + (read_2() if operand2 is not None else bus.read('A')))
            case 'SUB':
                """Sub register r2 to register r1"""
                write_1(read_1() - read_2() if operand2 is not None else bus.read('A'))
            case 'ADC':
                """Add register r2 to register r1 with carry"""
                write_1(read_1() + read_2() + (bus.read('F') & 1))
            case 'SBC':
                """Sub register r2 to register r1 with carry"""
                write_1(read_1() - read_2() - (bus.read('F') & 1))
            case 'AND':
                """AND register r2 with register r1"""
                write_1(read_1() & (read_2() if operand2 is not None else bus.read('A')))
            case 'OR':
                """OR register r2 with register r1"""
                write_1(read_1() | (read_2() if operand2 is not None else bus.read('A')))
            case 'XOR':
                """XOR register r2 with register r1"""
                write_1(read_1() ^ (read_2() if operand2 is not None else bus.read('A')))
            case 'INC':
                """Increment register r1"""
                write_1(read_1() + 1)
            case 'DEC':
                """Decrement register r1"""
                write_1(read_1() - 1)
            case 'CP':
                """Compare register r2 with register r1"""
                bus.write('F', (bus.read('F') & 0b11110000) | (
                        read_1() - (read_2() if operand2 is not None else bus.read('A'))))
            case _:
                print(
                    f'Unknown instruction: {hex(op_code)} | {mnemonic} | {repr(operand1)} {repr(operand2)} | {repr(flags)}')
        return instruction.cycles

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __init__(self, instructions, cb_instructions):
        self.instructions = instructions
        self.cb_instructions = cb_instructions

    def __str__(self):
        return f'CPU'

    def run(self, bus:Bus):
        bus = bus
        cycles = 0
        while True:
            op_code = yield cycles
            print(f'OP_CODE: {op_code:#02X}')
            current_instr = self.decode(op_code, self.is_cb)
            print(f'DECODED: {current_instr.mnemonic} {current_instr.operand1} {current_instr.operand2} {current_instr.flags}')
            cycles = self.execute(bus, current_instr)
            print(f'CYCLES: {cycles}')

