# gameboy cpu
import operator
import sys
import time
from dataclasses import dataclass

import constants
from cartridge import Cartridge


# we need a timer class that can be ticked at a sonsitent rate
class Timer:
    div: int = 0
    tima: int = 0
    tma: int = 0
    tac: int = 0


    def tick(self, cycles: int):
        ...

    def read(self, address: int):
        if address == 0xFF04:
            return self.div
        elif address == 0xFF05:
            return self.tima
        elif address == 0xFF06:
            return self.tma
        elif address == 0xFF07:
            return self.tac
        else:
            raise Exception(f'Invalid address {hex(address)}')

    def write(self, address: int, value: int):
        if address == 0xFF04:
            self.div = 0
        elif address == 0xFF05:
            self.tima = value
        elif address == 0xFF06:
            self.tma = value
        elif address == 0xFF07:
            self.tac = value
        else:
            raise Exception(f'Invalid address {hex(address)}')


@dataclass
class Register:
    a: int = 0x01
    b: int = 0x00
    c: int = 0x13
    d: int = 0x00
    e: int = 0xD8
    h: int = 0x01
    l: int = 0x4D
    f: int = 0xB0
    sp: int = 0xFFFE
    pc: int = 0x0100

    @property
    def af(self):
        return (self.a << 8) | self.f

    @af.setter
    def af(self, value):
        self.a = (value >> 8) & 0xFF
        self.f = value & 0xFF

    @property
    def bc(self):
        return (self.b << 8) | self.c

    @bc.setter
    def bc(self, value):
        self.b = (value >> 8) & 0xFF
        self.c = value & 0xFF

    @property
    def de(self):
        return (self.d << 8) | self.e

    @de.setter
    def de(self, value):
        self.d = (value >> 8) & 0xFF
        self.e = value & 0xFF

    @property
    def hl(self):
        return (self.h << 8) | self.l

    @hl.setter
    def hl(self, value):
        self.h = (value >> 8) & 0xFF
        self.l = value & 0xFF

    def __str__(self):
        out = ''
        for key, value in {
            'A': self.a,
            'B': self.b,
            'C': self.c,
            'D': self.d,
            'E': self.e,
            'H': self.h,
            'L': self.l,
            'F': self.f,
            'SP': self.sp,
            'PC': self.pc,

        }.items():
            out += f'{key}: {value:04X} '
        return out


class MMU:
    ...


class PPU:
    ...


class CPU:
    timer: Timer = Timer()
    cartridge: Cartridge = None
    mmu: MMU
    ppu: PPU
    wram = bytearray(0x2000)
    vram = bytearray(0x2000)
    eram = bytearray(0x2000)
    hram = bytearray(0x80)
    oam = bytearray(0xA0)
    io = bytearray(0x80)

    reg: Register = Register()
    instructions, cb_instructions = constants.Instruction.load_instructions().values()
    cycles: int = 0
    halted: bool = False
    stopped: bool = False
    ime: bool = False
    ime_delay: bool = False
    is_cb: bool = False
    screen = []

    def read_address(self, address: int):
        match address:
            case constants.MemoryMapRanges.ROM:
                return self.cartridge.read_rom(address)
            case constants.MemoryMapRanges.VRAM:
                return self.vram[address - constants.MemoryMapRanges.VRAM.start]
            case constants.MemoryMapRanges.ERAM:
                return self.eram[address - constants.MemoryMapRanges.ERAM.start]
            case constants.MemoryMapRanges.WRAM:
                return self.wram[address - constants.MemoryMapRanges.WRAM.start]
            case constants.MemoryMapRanges.OAM:
                return self.oam[address - constants.MemoryMapRanges.OAM.start]
            case constants.MemoryMapRanges.HRAM:
                return self.hram[address - constants.MemoryMapRanges.HRAM.start]
            case constants.MemoryMapRanges.IE:
                return self.ime
            case constants.MemoryMapRanges.IF:
                return self.ime_delay
            case constants.MemoryMapRanges.PPU:
                #return self.ppu[address - constants.MemoryMapRanges.PPU.start]
                pass
            case constants.MemoryMapRanges.IO:
                return self.io[address - constants.MemoryMapRanges.IO.start]
            case constants.MemoryMapRanges.ECHO:
                return self.read_address(address - 0x2000)
            case constants.MemoryMapRanges.UNUSED:
                return 0xFF
            case _:
                raise Exception(f"Invalid address: {hex(address)}")

    def write_address(self, address: int, value: int):
        match address:
            case constants.MemoryMapRanges.ROM:
                self.cartridge.write_rom(address, value)
            case constants.MemoryMapRanges.VRAM:
                self.vram[address - constants.MemoryMapRanges.VRAM.start] = value
            case constants.MemoryMapRanges.ERAM:
                self.eram[address - constants.MemoryMapRanges.ERAM.start] = value
            case constants.MemoryMapRanges.WRAM:
                self.wram[address - constants.MemoryMapRanges.WRAM.start] = value
            case constants.MemoryMapRanges.OAM:
                self.oam[address - constants.MemoryMapRanges.OAM.start] = value
            case constants.MemoryMapRanges.HRAM:
                self.hram[address - constants.MemoryMapRanges.HRAM.start] = value
            case constants.MemoryMapRanges.IE:
                self.ime = bool(value)
            case constants.MemoryMapRanges.IF:
                self.ime_delay = bool(value)
            case constants.MemoryMapRanges.PPU:
                # self.ppu[address - constants.MemoryMapRanges.PPU.start] = value
                print('attempted to access PPU')
                pass
            case constants.MemoryMapRanges.IO:
                self.io[address - constants.MemoryMapRanges.IO.start] = value
            case constants.MemoryMapRanges.ECHO:
                self.write_address(address - 0x2000, value)
            case constants.MemoryMapRanges.UNUSED:
                pass
            case _:
                raise Exception(f"Invalid address: {hex(address)}")

    def read_register(self, register: str):
        return getattr(self.reg, register, None)

    def write_register(self, register: str, value: int):
        setattr(self.reg, register, value)

    def read_flag(self, flag: str):
        return self.reg.f & constants.Flags[flag].value

    def read_flags(self, flags: str):
        return [self.read_flag(flag) for flag in flags]

    def write_flag(self, flag: str, value: bool):
        if value:
            self.reg.f |= constants.Flags[flag].value
        else:
            self.reg.f &= ~constants.Flags[flag].value

    def write_flags(self, *, Z=None, N=None, H=None, C=None):
        for attr in ['Z', 'N', 'H', 'C']:
            if (value := locals()[attr]) is not None:
                self.write_flag(attr, value)

    def read_operator(self, op: str):
        match op:
            case 'A' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L' | 'F' | 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
                return self.read_register(op.lower())
            case 'd16' | 'a16':
                return self.fetch16()
            case 'a8' | 'r8' | 'd8':
                return self.fetch()
            case '(BC)' | '(DE)' | '(HL)' | '(HL+)' | '(HL-)' | '(C)' | '(a16)' | '(a8)':
                return self.read_address(self.read_operator(op[1:-1]))
            case 'Z' | 'N' | 'H' | 'C':
                return self.read_flag(op)
            case 'HL+' | 'HL-':
                value = self.read_operator('HL')
                self.write_operator('HL', value + (1 if op[-1] == '+' else -1))
                return value
            case '38H':
                return 0x38
            case 'NZ' | 'NC':
                return not self.read_flag(op[1])
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                return int(op)
            case None:
                return None
            case _:
                raise ValueError(f'Invalid operator: {repr(op)}')

    def write_operator(self, op: str, value: int | bool):
        match op:
            case 'A' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L' | 'F' | 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
                self.write_register(op.lower(), value)
            case '(BC)' | '(DE)' | '(HL)' | '(HL+)' | '(HL-)' | '(C)' | '(a16)' | '(a8)':
                self.write_address(self.read_operator(op[1:-1]), value)
            case 'Z' | 'N' | 'H' | 'C':
                self.write_flag(op, value)
            case 'a8' | 'r8' | 'd8' | 'a16' | 'd16':
                self.write_address(self.read_operator(op), value)
            case 'NZ' | 'NC':
                self.write_flag(op[0], not value)
            case '38H':
                pass
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                self.write_operator({
                                        '0': 'B',
                                        '1': 'C',
                                        '2': 'D',
                                        '3': 'E',
                                        '4': 'H',
                                        '5': 'L',
                                        '6': '(HL)',
                                        '7': 'A',
                                        '8': 'B',
                                        '9': 'C',
                                        '10': 'D',
                                        '11': 'E',
                                        '12': 'H',
                                        '13': 'L',
                                        '14': '(HL)',
                                        '15': 'A',
                                    }[op], value)
            case 'HL+':
                self.write_operator('HL', value + 1)
            case 'HL-':
                self.write_operator('HL', value - 1)
            case None:
                pass
            case _:
                raise ValueError(f'Invalid operator: {op}')

    def fetch(self):
        pc = self.read_register('pc')
        self.write_register('pc', self.read_register('pc') + 1)
        return self.read_address(pc)

    def fetch16(self):
        return self.fetch() | (self.fetch() << 8)

    def decode(self, opcode: int):
        if self.is_cb:
            self.is_cb = False
            return self.cb_instructions[opcode]
        else:
            return self.instructions[opcode]

    def execute(self, instruction: constants.Instruction):
        operator_1, operator_2 = instruction.operand1, instruction.operand2
        match instruction.mnemonic:
            # system
            case 'NOP':
                pass
            case 'HALT':
                self.halted = True
            case 'STOP':
                self.stopped = True

            case 'EI' | 'DI':
                self.ime = instruction.mnemonic == 'EI'

            case 'ADD' | 'ADC' | 'SUB' | 'SBC':
                value_1 = self.read_operator(operator_1)
                value_2 = self.read_operator(operator_2 if operator_2 is not None else 'A')
                do_add = instruction.mnemonic[0] == 'A'
                op = operator.add if do_add else operator.sub
                result = op(op(value_1, value_2), self.read_flag('C') if instruction.mnemonic[-1] else 0)
                self.write_operator(operator_1, result)
                self.write_flags(
                    Z=result == 0,
                    N=do_add,
                    H=(operator.lt if do_add else operator.gt)(result & 0xF, value_1 & 0xf),
                    C=(operator.gt if do_add else operator.lt(result, 0xff if do_add else 0)
                       ))

            case 'AND' | 'OR' | 'XOR':
                value_1 = self.read_operator(operator_1)
                value_2 = self.read_operator(operator_2 if operator_2 is not None else 'A')
                op = {
                    'A': operator.and_,
                    'O': operator.or_,
                    'X': operator.xor,
                }[instruction.mnemonic[0]]
                res = op(value_1, value_2)
                self.write_operator(operator_1, res)
                self.write_flags(Z=res == 0, N=False, H=instruction.mnemonic[0] == 'A', C=False)

            case 'CP' if operator_2 is None:
                value = self.read_operator(operator_1)
                self.write_flags(Z=value == 0, N=True, H=(value & 0xF) > (self.read_operator(operator_1) & 0xF),
                                 C=value < 0)
            case 'CP':
                value = self.read_operator(operator_1) - self.read_operator(operator_2)
                self.write_flags(Z=value == 0, N=True, H=(value & 0xF) > (self.read_operator(operator_1) & 0xF),
                                 C=value < 0)
            case 'INC':
                value = self.read_operator(operator_1) + 1
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=(value & 0xF) == 0)
            case 'DEC':
                value = self.read_operator(operator_1) - 1
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=True, H=(value & 0xF) == 0xF)
            case 'DAA':
                value = self.read_operator(operator_1)
                if self.read_flag('N'):
                    if self.read_flag('H'):
                        value = (value - 0x06) & 0xFF
                    if self.read_flag('C'):
                        value -= 0x60
                else:
                    if self.read_flag('H') or (value & 0xF) > 9:
                        value += 0x06
                    if self.read_flag('C') or value > 0x9F:
                        value += 0x60
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, H=False, C=value > 0xFF)
            case 'CPL':
                value = self.read_operator(operator_1) ^ 0xFF
                self.write_operator(operator_1, value)
                self.write_flags(N=True, H=True)
            case 'CCF':
                self.write_flags(N=False, H=False, C=not self.read_flag('C'))
            case 'SCF':
                self.write_flags(N=False, H=False, C=True)

            case 'RC':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value >> 1)
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 1)
            case 'RLC':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, (value << 1) | (value >> 7))
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x80)
            case 'RRC':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, (value >> 1) | (value << 7))
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x01)
            case 'RL':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, (value << 1) | self.read_flag('C'))
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x80)
            case 'RR':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, (value >> 1) | (self.read_flag('C') << 7))
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x01)
            case 'SLA':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value << 1)
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x80)
            case 'SRA':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, (value >> 1) | (value & 0x80))
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x01)
            case 'SRL':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value >> 1)
                self.write_flags(Z=value == 0, N=False, H=False, C=value & 0x01)
            # jumps
            case 'JP' if operator_2 is None:
                self.write_operator('PC', self.read_operator(operator_1))

            case 'JR' if operator_2 is None:
                self.write_operator('PC', self.read_operator('PC') + self.read_operator(operator_1))

            case 'JR':
                self.write_operator(operator_1, self.read_operator(operator_1) + self.read_operator(operator_2))

            case 'CALL' if operator_2 is None:
                self.write_operator('SP', self.read_operator('SP') - 2)
                self.write_operator('PC', self.read_operator(operator_1))

            case 'BIT':
                value = self.read_operator(operator_1)
                self.write_flags(Z=(value & (1 << self.read_operator(operator_2))) == 0, N=False, H=True)

            case 'SET':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value | (1 << self.read_operator(operator_2)))

            case 'RES':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value & ~(1 << self.read_operator(operator_2)))

            case 'SWAP':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, ((value & 0xF) << 4) | ((value & 0xF0) >> 4))
                self.write_flags(Z=value == 0, N=False, H=False, C=False)

            case 'PREFIX':
                self.is_cb = True

            case 'LD' | 'LDH' | 'LDHL' | 'PUSH' | 'POP' | 'DI' | 'EI' | 'CALL' | 'RET' | 'RST' | 'RETI' | 'JP':
                self.write_operator(operator_1, self.read_operator(operator_2))

            case _:
                print('Unknown instruction: ' + instruction.mnemonic)
        return instruction

    def step(self):
        op = self.fetch()
        inst = self.decode(op)
        return self.execute(inst)

    def run(self, cart: Cartridge):
        self.cartridge = cart
        self.reset()
        while True:
            yield self.step()

    def reset(self):
        for register, value in [
            ('AF', 0x01B0),
            ('BC', 0x0013),
            ('DE', 0x00D8),
            ('HL', 0x014D),
            ('SP', 0xFFFE),
            ('PC', 0x0100),
        ]:
            self.write_register(register, value)

