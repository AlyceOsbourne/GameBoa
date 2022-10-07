# gameboy cpu
import sys
import time
from dataclasses import dataclass

import constants
from cartridge import Cartridge


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
        return f'AF: {self.af:04X} BC: {self.bc:04X} DE: {self.de:04X} HL: {self.hl:04X} SP: {self.sp:04X} PC: {self.pc:04X}'


class CPU:
    cartridge: Cartridge = None
    ppu = bytearray(0x2000)
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
                constants.logger.debug(f'ROM: {address:04X}')
                return self.cartridge.read_rom(address)
            case constants.MemoryMapRanges.VRAM:
                constants.logger.debug(f'VRAM: {address:04X}')
                return self.vram[address - constants.MemoryMapRanges.VRAM.start]
            case constants.MemoryMapRanges.ERAM:
                constants.logger.debug(f'ERAM: {address:04X}')
                return self.eram[address - constants.MemoryMapRanges.ERAM.start]
            case constants.MemoryMapRanges.WRAM:
                constants.logger.debug(f'WRAM: {address:04X}')
                return self.wram[address - constants.MemoryMapRanges.WRAM.start]
            case constants.MemoryMapRanges.OAM:
                constants.logger.debug(f'OAM: {address:04X}')
                return self.oam[address - constants.MemoryMapRanges.OAM.start]
            case constants.MemoryMapRanges.HRAM:
                constants.logger.debug(f'HRAM: {address:04X}')
                return self.hram[address - constants.MemoryMapRanges.HRAM.start]
            case constants.MemoryMapRanges.IE:
                constants.logger.debug(f'IE: {address:04X}')
                return self.ime
            case constants.MemoryMapRanges.IF:
                constants.logger.debug(f'IF: {address:04X}')
                return self.ime_delay
            case constants.MemoryMapRanges.PPU:
                constants.logger.debug(f'PPU: {address:04X}')
                return self.ppu[address - constants.MemoryMapRanges.PPU.start]
            case constants.MemoryMapRanges.IO:
                constants.logger.debug(f'IO: {address:04X}')
                return self.io[address - constants.MemoryMapRanges.IO.start]
            case constants.MemoryMapRanges.ECHO:
                constants.logger.debug(f'ECHO: {address:04X}')
                return self.read_address(address - 0x2000)
            case constants.MemoryMapRanges.UNUSED:
                constants.logger.debug(f'UNUSED: {address:04X}')
                return 0xFF
            case _:
                raise Exception(f"Invalid address: {hex(address)}")

    def write_address(self, address: int, value: int):
        match address:
            case constants.MemoryMapRanges.ROM:
                constants.logger.debug(f'ROM: {address:04X}')
                self.cartridge.write_rom(address, value)
            case constants.MemoryMapRanges.VRAM:
                constants.logger.debug(f'VRAM: {address:04X}')
                self.vram[address - constants.MemoryMapRanges.VRAM.start] = value
            case constants.MemoryMapRanges.ERAM:
                constants.logger.debug(f'ERAM: {address:04X}')
                self.eram[address - constants.MemoryMapRanges.ERAM.start] = value
            case constants.MemoryMapRanges.WRAM:
                constants.logger.debug(f'WRAM: {address:04X}')
                self.wram[address - constants.MemoryMapRanges.WRAM.start] = value
            case constants.MemoryMapRanges.OAM:
                constants.logger.debug(f'OAM: {address:04X}')
                self.oam[address - constants.MemoryMapRanges.OAM.start] = value
            case constants.MemoryMapRanges.HRAM:
                constants.logger.debug(f'HRAM: {address:04X}')
                self.hram[address - constants.MemoryMapRanges.HRAM.start] = value
            case constants.MemoryMapRanges.IE:
                constants.logger.debug(f'IE: {address:04X}')
                self.ime = bool(value)
            case constants.MemoryMapRanges.IF:
                constants.logger.debug(f'IF: {address:04X}')
                self.ime_delay = bool(value)
            case constants.MemoryMapRanges.PPU:
                constants.logger.debug(f'PPU: {address:04X}')
                self.ppu[address - constants.MemoryMapRanges.PPU.start] = value
            case constants.MemoryMapRanges.IO:
                constants.logger.debug(f'IO: {address:04X}')
                self.io[address - constants.MemoryMapRanges.IO.start] = value
            case constants.MemoryMapRanges.ECHO:
                constants.logger.debug(f'ECHO: {address:04X}')
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

    def read_operator(self, operator: str):
        match operator:
            case 'A' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L' | 'F' | 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
                return self.read_register(operator.lower())
            case 'd16' | 'a16':
                return self.fetch16()
            case 'a8' | 'r8' | 'd8':
                return self.fetch()
            case '(BC)' | '(DE)' | '(HL)' | '(HL+)' | '(HL-)' | '(C)':
                return self.read_address(self.read_operator(operator[1:-1]))
            case '(a8)':
                return self.read_address(self.read_operator('a8'))
            case '(a16)':
                return self.read_address(self.read_operator('a16'))
            case 'Z' | 'N' | 'H' | 'C':
                return self.read_flag(operator)
            case '38H':
                return 0x38
            case 'HL+':
                value = self.read_operator('HL')
                self.write_operator('HL', value + 1)
                return value
            case 'HL-':
                value = self.read_operator('HL')
                self.write_operator('HL', value - 1)
                return value
            case 'NZ':
                return not self.read_flag('Z')
            case None:
                return None
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                return int(operator)
            case _:
                raise ValueError(f'Invalid operator: {repr(operator)}')

    def write_operator(self, operator: str, value: int | bool):
        match operator:
            case 'A' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L' | 'F':
                self.write_register(operator.lower(), value)
            case 'AF' | 'BC' | 'DE' | 'HL':
                self.write_register(operator.lower(), value)
            case 'SP':
                self.reg.sp = value
            case 'PC':
                self.reg.pc = value
            case '(BC)' | '(DE)' | '(HL)' | '(HL+)' | '(HL-)' | '(C)':
                self.write_address(self.read_operator(operator[1:-1]), value)
            case '(a8)':
                self.write_address(self.read_operator('a8'), value)
            case '(a16)':
                self.write_address(self.read_operator('a16'), value)
            case 'Z' | 'N' | 'H' | 'C':
                self.write_flag(operator, value)
            case 'a8':
                self.write_address(self.read_operator('a8'), value)
            case 'a16':
                self.write_address(self.read_operator('a16'), value)
            case 'NZ':
                self.write_flag('Z', not value)
            case '38H':
                pass
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                mapping = {
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
                }[operator]
                self.write_operator(mapping, value)

            case 'd8':
                self.write_operator('a8', value)

            case 'HL+':
                self.write_operator('HL', value + 1)
            case 'HL-':
                self.write_operator('HL', value - 1)

            case None:
                pass
            case _:
                raise ValueError(f'Invalid operator: {operator}')

    def fetch(self):
        pc = self.read_register('pc')
        self.write_register('pc', self.read_register('pc') + 1)
        return self.read_address(pc)

    def fetch16(self):
        return self.fetch() | (self.fetch() << 8)

    def decode(self, opcode):
        constants.logger.debug(f'PC: {self.reg.pc:04X} | Opcode: {opcode} | CB: {self.is_cb}')
        if self.check_cb(opcode):
            self.is_cb = True
            opcode = self.fetch()
            return self.cb_instructions[opcode]
        else:
            self.is_cb = False
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
            ## interrupts
            case 'EI':
                self.ime_delay = True
            case 'DI':
                self.ime = False
            # math
            case 'ADD':
                value = self.read_operator(operator_1) + self.read_operator(operator_2)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=(value & 0xF) < (self.read_operator(operator_1) & 0xF),
                                 C=value > 0xFF)
            case 'ADC':
                value = self.read_operator(operator_1) + self.read_operator(operator_2) + self.read_flag('C')
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=(value & 0xF) < (self.read_operator(operator_1) & 0xF),
                                 C=value > 0xFF)
            case 'SUB':
                value = self.read_operator(operator_1) - self.read_operator(operator_2)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=True, H=(value & 0xF) > (self.read_operator(operator_1) & 0xF),
                                 C=value < 0)
            case 'SBC':
                value = self.read_operator(operator_1) - self.read_operator(operator_2) - self.read_flag('C')
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=True, H=(value & 0xF) > (self.read_operator(operator_1) & 0xF),
                                 C=value < 0)

            case 'AND' if operator_2 is None:
                value = self.read_operator(operator_1) & self.read_operator('A')
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=True, C=False)

            case 'AND':
                value = self.read_operator(operator_1) & self.read_operator(operator_2)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=True, C=False)
            case 'OR' if operator_2 is None:
                value = self.read_operator(operator_1) | self.read_operator('A')
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=False, C=False)
            case 'OR':
                value = self.read_operator(operator_1) | self.read_operator(operator_2)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=False, C=False)

            case 'XOR' if operator_2 is None:
                value = self.read_operator(operator_1) ^ self.read_operator(operator_1)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=False, C=False)
            case 'XOR':
                value = self.read_operator(operator_1) ^ self.read_operator(operator_2)
                self.write_operator(operator_1, value)
                self.write_flags(Z=value == 0, N=False, H=False, C=False)
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
            # shifts
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
            case 'JP':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'JR' if operator_2 is None:
                self.write_operator('PC', self.read_operator('PC') + self.read_operator(operator_1))
            case 'JR':
                self.write_operator(operator_1, self.read_operator(operator_1) + self.read_operator(operator_2))
            case 'CALL' if operator_2 is None:
                self.write_operator('SP', self.read_operator('SP') - 2)
                self.write_operator('PC', self.read_operator(operator_1))
            case 'CALL':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'RET':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'RST':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'RETI':
                self.write_operator(operator_1, self.read_operator(operator_2))
            # bit operations
            case 'BIT':
                value = self.read_operator(operator_1)
                self.write_flags(Z=(value & (1 << self.read_operator(operator_2))) == 0, N=False, H=True)
            case 'SET':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value | (1 << self.read_operator(operator_2)))
            case 'RES':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, value & ~(1 << self.read_operator(operator_2)))
            case 'LD':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'LDH':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'LDHL':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'PUSH':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'POP':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'SWAP':
                value = self.read_operator(operator_1)
                self.write_operator(operator_1, ((value & 0xF) << 4) | ((value & 0xF0) >> 4))
                self.write_flags(Z=value == 0, N=False, H=False, C=False)
            case 'DI':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'EI':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'HALT':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'STOP':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case 'PREFIX':
                self.write_operator(operator_1, self.read_operator(operator_2))
            case _:
                print('Unknown instruction: ' + instruction.mnemonic)
        return instruction

    def step(self):
        op_code = self.fetch()
        constants.logger.debug('Op code: ' + hex(op_code))
        instruction = self.decode(op_code)
        constants.logger.debug(f"Instruction {instruction.mnemonic} {instruction.operand1} {instruction.operand2}")
        self.execute(instruction)
        constants.logger.debug('Registers: ' + str(self.reg))
        constants.logger.debug('Flags: ' + str(self.read_flags('ZNHC')))
        return instruction

    def run(self, cart):
        constants.logger.debug('Running | ' + cart.title)
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

    @staticmethod
    def check_cb(opcode):
        return opcode in [0xCB, 0xDDCB, 0xEDCB, 0xFDCB]

    def draw_ppu(self):
        for y in range(0, 144):
            for x in range(0, 160):
                print(self.ppu[x + y], end='')
            print()

    def print_registers(self):
        print('Registers: ' + str(self.reg))

    def print_flags(self):
        print('Flags: ' + str(self.read_flags('ZNHC')))


if __name__ == "__main__":
    cpu = CPU()
    cpu.reset()
    cpu.print_registers()
    cpu.print_flags()
    for instruction in cpu.run(Cartridge('Tetris.gb')):
        print(instruction.mnemonic, instruction.operand1, instruction.operand2)
        cpu.print_registers()
        cpu.print_flags()
        print()
    print('Done')
