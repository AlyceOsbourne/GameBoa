from functools import partial

from protocols import Bus, Timer
from components.system_mappings import Instructions


class CPU:
    """The CPU of the Game Boy."""

    is_stopped: bool
    is_halted: bool
    instructions: dict[int, Instructions]
    cb_instructions: dict[int, Instructions]
    is_cb: bool = False
    interrupts_enabled = False

    def decode(self, op_code: int, cb: bool = False) -> Instructions:
        """Checks whether a CPU instruction is prefixed with 'cb_'."""
        decoded = getattr(self, ("cb_" if cb else "") + "instructions")[op_code]

        if self.is_cb:
            self.is_cb = False

        return decoded

    def execute(self, bus: Bus, instruction: Instructions) -> int:
        """Uses pattern matching to execute the given instruction."""
        op_code = instruction.op_code
        mnemonic = instruction.mnemonic
        operand1, operand2 = instruction.operand1, instruction.operand2
        flags = instruction.flags

        read_1 = partial(bus.read, operand1)
        read_2 = partial(bus.read, operand2)
        write_1 = partial(bus.write, operand1)

        match instruction.mnemonic:
            case "NOP":
                return 0
            case "HALT":
                self.is_halted = True
            case "STOP":
                # this has some funky logic as I understand it
                self.is_stopped = True
            case "PREFIX":
                self.is_cb = True
            case "SET":
                write_1(read_1() | (1 << op_code & 0b111))
            case "CALL" | "RET" | "RETI" | "RETN" | "RST":
                bus.write("SP", bus.read("SP") + 2)
            case "JP":
                bus.write("PC", read_1())
            case "JR":
                if read_2() or operand2 is None:
                    bus.write("PC", bus.read("PC") + read_1())
            case "DI" | "EI":
                self.interrupts_enabled = op_code == 0xF3
            case "SWAP":
                write_1((read_1() << 4) | (read_1() >> 4))
            case "BIT":
                bus.write(
                    "F",
                    (bus.read("F") & 0b11110000)
                    | (1 << 4)
                    | (read_1() & (1 << op_code & 0b111)),
                )
            case "RES":
                write_1(read_1() & ~(1 << op_code & 0b111))
            case "RLC" | "RRC":
                if mnemonic[1] == "L":
                    write_1((read_1() << 1) | (read_1() >> 7))
                else:
                    write_1((read_1() >> 1) | (read_1() << 7))
            case "RL" | "RR":
                if mnemonic[1] == "L":
                    write_1((read_1() << 1) | (bus.read("F") & 1))
                else:
                    write_1((read_1() >> 1) | (bus.read("F") & 1))
            case "SLA" | "SRA":
                if mnemonic[1] == "L":
                    write_1((read_1() << 1) | (read_1() >> 7))
                else:
                    write_1((read_1() >> 1) | (read_1() & 0b10000000))
            case "SRL":
                write_1((read_1() >> 1) | (read_1() & 0b10000000))
            case "RLCA" | "RRCA" if operand1 is None and operand2 is None:
                if mnemonic[2] == "L":
                    bus.write("A", (bus.read("A") << 1) | (bus.read("A") >> 7))
                else:
                    bus.write("A", (bus.read("A") >> 1) | (bus.read("A") << 7))
            case "RLA" | "RRA":
                if mnemonic[2] == "L":
                    bus.write("A", (bus.read("A") << 1) | (bus.read("F") & 1))
                else:
                    bus.write("A", (bus.read("A") >> 1) | (bus.read("F") & 1))
            case "DAA":
                if bus.read("F") & 0b10000000:
                    if bus.read("F") & 0b10000:
                        bus.write("A", bus.read("A") - 0x60)
                    if bus.read("F") & 0b1000:
                        bus.write("A", bus.read("A") - 0x6)
                else:
                    if bus.read("F") & 0b10000 or bus.read("A") > 0x99:
                        bus.write("A", bus.read("A") + 0x60)
                        bus.write("F", bus.read("F") | 0b10000)
                    if bus.read("F") & 0b1000 or (bus.read("A") & 0x0F) > 0x09:
                        bus.write("A", bus.read("A") + 0x6)
            case "CPL":
                bus.write("A", ~bus.read("A"))
            case "CCF":
                bus.write("F", bus.read("F") ^ 0b10000)
            case "SCF":
                bus.write("F", bus.read("F") | 0b10000)
            case "LD" | "LDH" | "LDI" | "LDD":
                write_1(read_2())
            case "PUSH":
                bus.write("SP", read_1())
            case "POP":
                write_1(bus.read("SP"))
                bus.write("SP", bus.read("SP") + 2)
            case "ADD":
                write_1(
                    read_1() + (read_2() if operand2 is not None else bus.read("A"))
                )
            case "SUB":
                write_1(read_1() - read_2() if operand2 is not None else bus.read("A"))
            case "ADC":
                write_1(read_1() + read_2() + (bus.read("F") & 1))
            case "SBC":
                write_1(read_1() - read_2() - (bus.read("F") & 1))
            case "AND":
                write_1(
                    read_1() & (read_2() if operand2 is not None else bus.read("A"))
                )
            case "OR":
                write_1(
                    read_1() | (read_2() if operand2 is not None else bus.read("A"))
                )
            case "XOR":
                write_1(
                    read_1() ^ (read_2() if operand2 is not None else bus.read("A"))
                )
            case "INC":
                write_1(read_1() + 1)
            case "DEC":
                write_1(read_1() - 1)
            case "CP":
                bus.write(
                    "F",
                    (bus.read("F") & 0b11110000)
                    | (
                        read_1() - (read_2() if operand2 is not None else bus.read("A"))
                    ),
                )
            case _:
                print(
                    f"Unknown instruction: {hex(op_code)} | {mnemonic} | {repr(operand1)} {repr(operand2)} | {repr(flags)}"
                )
        return instruction.cycles

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __init__(self, instructions, cb_instructions):
        self.instructions = instructions
        self.cb_instructions = cb_instructions

    def __str__(self):
        return f"CPU"

    def run(self, bus: Bus):
        cycles = 0

        while True:
            op_code = yield cycles
            print(f"OP_CODE: {op_code:#02X}")
            current_instruction = self.decode(op_code, self.is_cb)
            print(
                f"DECODED: {current_instruction.mnemonic} {current_instruction.operand1} {current_instruction.operand2} {current_instruction.flags}"
            )
            cycles = self.execute(bus, current_instruction)
            print(f"CYCLES: {cycles}")
