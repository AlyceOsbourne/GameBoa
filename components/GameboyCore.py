from functools import partial

from components import system_mappings
from components.system_mappings import Instruction, Flags


class CPU:
    """The Central Processing Unit of the Game Boy."""

    is_halted: bool
    is_stopped: bool
    interrupts_enabled = False
    is_cb_instruction: bool = False
    instructions: dict[int, Instruction]
    cb_instructions: dict[int, Instruction]

    a: int = 0x00
    b: int = 0x00
    c: int = 0x00
    d: int = 0x00
    e: int = 0x00
    f: int = 0x00
    h: int = 0x00
    l: int = 0x00
    pc: int = 0x0000
    sp: int = 0x0000



    # Convert two 8-bit registers into one 16-bit register.
    _get_16 = lambda self, r1, r2: (self.read(r1) << 8) | self.read(r2)
    _set_16 = lambda self, r1, r2, value: (
        self.write(r1, (value >> 8) & 0xFF),
        self.write(r2, value & 0xFF),
    )

    # Provide a getter and a setter for 16-bit registers.
    af = property(
        lambda self: self._get_16("A", "F"),
        lambda self, value: self._set_16("A", "F", value),
        doc="Accumulator & Flags register.",
    )
    bc = property(
        lambda self: self._get_16("B", "C"),
        lambda self, value: self._set_16("B", "C", value),
        doc="BC reg",
    )
    de = property(
        lambda self: self._get_16("D", "E"),
        lambda self, value: self._set_16("D", "E", value),
        doc="DE reg",
    )
    hl = property(
        lambda self: self._get_16("H", "L"),
        lambda self, value: self._set_16("H", "L", value),
        doc="HL reg",
    )

    flag_z = property(
        lambda self: (self.f & Flags.Z) == Flags.Z,
        lambda self, value: self.set_flag(Flags.Z, value),
        doc="Zero flag.",
    )

    flag_n = property(
        lambda self: (self.f & Flags.N) == Flags.N,
        lambda self, value: self.set_flag(Flags.N, value),
        doc="Subtraction flag.",
    )

    flag_h = property(
        lambda self: (self.f & Flags.H) == Flags.H,
        lambda self, value: self.set_flag(Flags.H, value),
        doc="Half carry flag.",
    )

    flag_c = property(
        lambda self: (self.f & Flags.C) == Flags.C,
        lambda self, value: self.set_flag(Flags.C, value),
        doc="Carry flag.",
    )

    def __init__(self, instruction_set, default_register_values: system_mappings.RegisterDefault):
        self.instructions, self.cb_instructions = instruction_set
        self.af, self.bc, self.de, self.hl, self.sp, self.pc = default_register_values

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return f"CPU"

    def decode(self, op_code: int) -> Instruction:
        """Decodes the given op_code into an instruction."""
        op = getattr(self, ("cb_" if self.is_cb_instruction else "") + "instructions").get(op_code, None)
        self.is_cb_instruction = False
        return op

    def set_flags(self, values: str):
        for flag, value in zip("znhc", values):
            match value:
                case "0":
                    self.write(flag, False)
                case "1":
                    self.write(flag, True)
                case "-":
                    pass
                case _:
                    raise ValueError(f"Unknown flag value: {value}")

    def execute(self, instruction: Instruction) -> int:
        """Uses pattern matching to execute the given instruction."""
        self.set_flags(instruction.flags)
        match instruction.mnemonic:
            case "NOP":
                return instruction.cycles
            case "LD":
                self.write(instruction.operand1, self.read(instruction.operand2))
                return instruction.cycles
            case _:
                raise ValueError(f"Unknown instruction: {instruction}")

    def read(self, operand: str) -> int:
        match operand:
            case (
                "A" |
                "B" |
                "C" |
                "D" |
                "E" |
                "F" |
                "H" |
                "L" |
                "PC" |
                "SP" |
                "AF" |
                "BC" |
                "DE" |
                "HL" |
                "Z" |
                "N" |
                "H" |
                "C"
            ):
                return getattr(self, operand.lower())
            case 'd8':
                return self.read('PC')
            case 'd16':
                return self.read('d8') << 8 | self.read('d8')
            case _:
                raise ValueError(f"Unknown operand: {operand}")

    def write(self, operand: str, value: int) -> None:
        match operand:
            case (
                "A" |
                "B" |
                "C" |
                "D" |
                "E" |
                "F" |
                "H" |
                "L" |
                "PC" |
                "SP" |
                "AF" |
                "BC" |
                "DE" |
                "HL" |
                "Z" |
                "N" |
                "H" |
                "C"
            ):
                setattr(self, operand, value)
            case _:
                raise ValueError(f"Unknown operand: {operand}")

    def read_address(self, address: int) -> int:
        match address:
            case _:
                raise ValueError(f"Unknown address: {address}")

    def write_address(self, address: int, value: int) -> None:
        match address:
            case _:
                raise ValueError(f"Unknown address: {address}")

    def run(self):
        cycles = 0

        while True:
            op_code = yield cycles
            current_instruction = self.decode(op_code)
            if current_instruction is None:
                print(f"Unknown instruction: {op_code}")
                continue
            cycles = self.execute(current_instruction)


if __name__ == "__main__":
    cpu = CPU(system_mappings.Instruction.load('../op_codes.json').values(),
              system_mappings.DMGModelRegisterDefaults.DMG)
    for op_code in cpu.instructions.values():
        cpu.execute(op_code)
    for op_code in cpu.cb_instructions.values():
        cpu.execute(op_code)
