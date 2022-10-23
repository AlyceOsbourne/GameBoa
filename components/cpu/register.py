import array
from core import system_mappings


class Register:

    # works like a slimmed down, array backed dict,
    # but the keys are also variables of the class kinda like a named tuple

    def __init__(self, registry: array.array = None):
        self._registry = registry if registry else array.array('B', [0] * 12)

    def __getitem__(self, item):
        match item:
            case "reg_8_a" | "reg_8_f" | "reg_8_b" | "reg_8_c" | "reg_8_d" | "reg_8_e" | "reg_8_h" | "reg_8_l":
                return self._registry["afbcdehl".index(item[-1])] & 0xff
            case "reg_16_af" | "reg_16_bc" | "reg_16_de" | "reg_16_hl" | "reg_16_sp" | "reg_16_pc":
                idx = "afbcdehlsppc".index(item[-2:]) & 0xff
                return (self._registry[idx] << 8) | self._registry[idx + 1]
            case "flag_z" | "flag_n" | "flag_h" | "flag_c":
                return (self._registry[1] >> (7 - 'znhc'.index(item[-1]))) & 1 & 0xff
            case _:
                raise KeyError(f"Invalid key: {item}")

    def __setitem__(self, key, value):
        match key:
            case "reg_8_a" | "reg_8_f" | "reg_8_b" | "reg_8_c" | "reg_8_d" | "reg_8_e" | "reg_8_h" | "reg_8_l" if value <= 0xff:
                self._registry["afbcdehl".index(key[-1])] = value

            case "reg_16_af" | "reg_16_bc" | "reg_16_de" | "reg_16_hl" | "reg_16_sp" | "reg_16_pc" if value <= 0xffff:
                idx = "afbcdehlsppc".index(key[-2:])
                self._registry[idx] = value >> 8
                self._registry[idx + 1] = value & 0xff

            case "flag_z" | "flag_n" | "flag_h" | "flag_c" if value <= 1:
                self._registry[1] = (self._registry[1] & ~(1 << (7 - "znhc".index(key[-1])))) | (
                            value << (7 - "znhc".index(key[-1])))

            case (
            'flag_z' | 'flag_n' | 'flag_h' | 'flag_c' |
            "reg_8_a" | "reg_8_f" | "reg_8_b" | "reg_8_c" | "reg_8_d" | "reg_8_e" | "reg_8_h" | "reg_8_l"|
            "reg_16_af" | "reg_16_bc" | "reg_16_de" | "reg_16_hl" | "reg_16_sp" | "reg_16_pc"):
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
        register = cls()
        register._registry = array.array('B', data)
        return register

    @classmethod
    def from_default(cls, default: system_mappings.RegisterDefaults):
        """Creates a new register with default values."""
        register = cls()
        for k, v in default._asdict().items():
            register[f"reg_16_{k}"] = v
        return register
