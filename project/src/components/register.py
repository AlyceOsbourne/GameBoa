import array

from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents, GuiEvents


class Register:
    _registry: array.array

    def __init__(self, data=None):
        if data is None:
            data = [0] * 12
        self._registry = array.array('B', data)
        EventHandler.subscribe(ComponentEvents.RequestRegisterRead, self.requested_read)
        EventHandler.subscribe(ComponentEvents.RequestRegisterWrite, self.__setitem__)
        EventHandler.subscribe(GuiEvents.RequestRegistryStatus, self.requested_status)

    def __getitem__(self, item):
        match item:
            case "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L":
                return self._registry["AFBCDEHL".index(item)]
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
                self._registry["AFBCDEHL".index(key)] = value

            case "AF" | "BC" | "DE" | "HL" | "SP" | "PC" if value <= 0xffff:
                idx = "AFBCDEHLSPPC".index(key)
                self._registry[idx] = value >> 8
                self._registry[idx + 1] = value & 0xff

            case "FZ" | "FN" | "FH" | "FC" if value <= 1:
                self._registry[1] = (self._registry[1] & ~(
                        1 << (7 - 'ZNCH'.index(key[-1])))) | (value << (7 - 'ZNCH'.index(key[-1])))

            case (
            'FZ' | 'FN' | 'FH' | 'FC' |
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
        output += f"    A: 0x{self['A']:02x}, F: 0x{self['F']:02x}, AF: 0x{self['AF']:04x}\n"
        output += f"    B: 0x{self['B']:02x}, C: 0x{self['C']:02x}, BC: 0x{self['BC']:04x}\n"
        output += f"    D: 0x{self['D']:02x}, E: 0x{self['E']:02x}, DE: 0x{self['DE']:04x}\n"
        output += f"    H: 0x{self['H']:02x}, L: 0x{self['L']:02x}, HL: 0x{self['HL']:04x}\n"
        output += f"    SP: 0x{self['SP']:04x}, PC: 0x{self['PC']:04x}\n"
        output += f"    Z: {self['FZ'] >> 7 & 1}, " \
                  f"N: {self['FN'] >> 6 & 1}, " \
                  f"H: {self['FH'] >> 5 & 1}, " \
                  f"C: {self['FC'] >> 4 & 1}\n"
        return output + ")"

    def to_bytes(self) -> bytes:
        """Converts the register to bytes."""
        return self._registry.tobytes()


    def requested_read(self, register: str, callback):
        """Reads a value from the register."""
        callback(self[register])

    def requested_status(self, callback):
        """Reads a value from the register."""
        callback(str(self))




