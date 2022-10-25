import array
from enum import Enum
from typing import NamedTuple

RegisterDefault = NamedTuple('RegisterDefaults', [
    ('af', int),
    ('bc', int),
    ('de', int),
    ('hl', int),
    ('sp', int),
    ('pc', int),
])


class RegisterDefaults(RegisterDefault, Enum):
    ...


class DMGModelRegisterDefaults(RegisterDefaults):
    DMG = 0x01B0, 0x0013, 0x00D8, 0x014D, 0xFFFE, 0x0100
    MGB = 0xFFB0, 0x0013, 0x00D8, 0x014D, 0xFFFE, 0x0100
    SGB = 0x0100, 0x0014, 0x0000, 0x060C, 0xFFFE, 0x0100
    CGB = 0x1180, 0x0000, 0x0008, 0x007C, 0xFFFE, 0x0100
    AGB = 0x1100, 0x0100, 0x0008, 0x007C, 0xFFFE, 0x0100
    AGS = 0x1100, 0x0100, 0x0008, 0x007C, 0xFFFE, 0x0100


class CGBModelRegisterDefaults(RegisterDefaults):
    CGB = 0x1180, 0x0000, 0xFF56, 0x000D, 0xFFFE, 0x0100
    AGB = 0x1100, 0x0100, 0xFF56, 0x000D, 0xFFFE, 0x0100
    AGS = 0x1100, 0x0100, 0xFF56, 0x000D, 0xFFFE, 0x0100


class Register:

    # works like a slimmed down, array backed dict,
    # but the keys are also variables of the class kinda like a named tuple

    def __init__(self, registry: array.array = None):
        self._registry = registry if registry else array.array('B', [0] * 12)


    def __getitem__(self, item):
        match item:
            case "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L":
                return self._registry["ABCDEFHL".index(item)]
            case "AF" | "BC" | "DE" | "HL" | "SP" | "PC":
                idx = "AFBCDEHLSPPC".index(item)
                return (self._registry[idx] << 8) | self._registry[idx + 1]
            case "FZ" | "FN" | "FH" | "FC":
                return (self._registry[1] >> (7 - 'ZNCH'.index(item[-1]))) & 1 & 0xff
            case _:
                raise KeyError(f"Invalid key: {item}")

    def __setitem__(self, key, value):
        match key:
            case "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L" if value <= 0xff:
                self._registry["ABCDEFHL".index(key)] = value

            case "AF" | "BC" | "DE" | "HL" | "SP" | "PC" if value <= 0xffff:
                idx = "AFBCDEHLSPPC".index(key)
                self._registry[idx] = value >> 8
                self._registry[idx + 1] = value & 0xff

            case "flag_z" | "flag_n" | "flag_h" | "flag_c" if value <= 1:
                self._registry[1] = (self._registry[1] & ~(1 << (7 - "znhc".index(key[-1])))) | (
                            value << (7 - "znhc".index(key[-1])))

            case (
            'flag_z' | 'flag_n' | 'flag_h' | 'flag_c' |
            "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L" |
            "AF" | "BC" | "DE" | "HL" | "SP" | "PC"):
                raise ValueError(f"Value {value} is too large for {key}")
            case _:
                raise KeyError(f"Invalid key: {key}")

    def __getattr__(self, item):
        try:
            if item in ['_registry']:
                return super().__getattribute__(item)
            return self[item]
        except KeyError:
            raise AttributeError(f"Invalid attribute: {item}")

    def __setattr__(self, key, value):
        try:
            if key in ["_registry"]:
                super().__setattr__(key, value)
            else:
                self[key] = value
        except KeyError:
            raise AttributeError(f"Invalid attribute: {key}")

    def __repr__(self):
        return f"Register({self._registry})"

    def __str__(self):
        output = "Register(\n"
        output += f"    A: 0x{self['reg_8_a']:02x}, F: 0x{self['reg_8_d']:02x}, AF: 0x{self['reg_16_af']:04x}\n"
        output += f"    B: 0x{self['reg_8_b']:02x}, C: 0x{self['reg_8_c']:02x}, BC: 0x{self['reg_16_bc']:04x}\n"
        output += f"    D: 0x{self['reg_8_d']:02x}, E: 0x{self['reg_8_e']:02x}, DE: 0x{self['reg_16_de']:04x}\n"
        output += f"    H: 0x{self['reg_8_h']:02x}, L: 0x{self['reg_8_l']:02x}, HL: 0x{self['reg_16_hl']:04x}\n"
        output += f"    SP: 0x{self['reg_16_sp']:04x}, PC: 0x{self['reg_16_pc']:04x}\n"
        output += f"    Z: {self['flag_z'] >> 7 & 1}, N: {self['flag_n'] >> 6 & 1}, H: {self['flag_h'] >> 5 & 1}, C: {self['flag_c'] >> 4 & 1}\n"
        return output + ")"

    def to_bytes(self) -> bytes:
        """Converts the register to bytes."""
        return self._registry.tobytes()

    @classmethod
    def from_bytes(cls, data: bytes):
        """Creates a new register from the given bytes."""
        return cls(array.array('B', data))

    @classmethod
    def from_default(cls, default: RegisterDefaults):
        """Creates a new register with default values."""
        register = cls()
        for k, v in default._asdict().items():
            register[f"reg_16_{k}"] = v
        return register
