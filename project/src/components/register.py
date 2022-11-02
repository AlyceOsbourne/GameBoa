import array
from functools import partial
from project.src.system import ComponentEvents, LogEvent, GuiEvents

registry = array.array("B", [0] * 16)

_set_8 = lambda i, v: registry.__setitem__(i, v)
_set_16 = lambda i, v: registry.__setitem__(
    slice(i, i + 2), array.array("B", [v >> 8, v & 0xFF])
)
_get_8 = lambda i: registry[i]
_get_16 = lambda i: int.from_bytes(registry[slice(i, i + 2)], byteorder="big")


_make_regs = lambda regs: {
    c: (
        partial(_set_16 if len(c) == 2 else _set_8, i),
        partial(_get_16 if len(c) == 2 else _get_8, i),
    )
    for i, c in enumerate(regs)
}

_8_bit_regs = _make_regs(["A", "F", "B", "C", "D", "E", "H", "L"])
_18_bit_regs = _make_regs(["AF", "BC", "DE", "HL"])


@ComponentEvents.RequestRegisterWrite
def set_register(register, value):
    LogEvent.LogDebug(f"Writing {value} to {register}")
    match register:
        case "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L":
            _8_bit_regs[register][0](value)
        case "AF" | "BC" | "DE" | "HL":
            _18_bit_regs[register][0](value)
        case "SP":
            _set_16(8, value)
        case "PC":
            _set_16(10, value)
        case "FZ" | "FN" | "FH" | "FC":
            _set_8(1, _get_8(1) & ~(1 << "ZNC".index(register[1])) | (value << "ZNC".index(register[1])))
        case _:
            raise KeyError(f"Unknown register for given key {register}")


@ComponentEvents.RequestRegisterRead.allow_requests
def get_register(register):
    LogEvent.LogDebug(f"Reading {register}")
    match register:
        case "A" | "F" | "B" | "C" | "D" | "E" | "H" | "L":
            return _8_bit_regs[register][1]()
        case "AF" | "BC" | "DE" | "HL":
            return _18_bit_regs[register][1]()
        case "SP":
            return _get_16(8)
        case "PC":
            return _get_16(10)
        case "FZ", "FN", "FH", "FC":
            return _get_8(1) >> "ZNC".index(register[1]) & 1


@GuiEvents.RequestRegistryStatus.allow_requests
def get_registry_status():
    return_string = ""
    for i, reg in enumerate(["AF", "BC", "DE", "HL", "SP", "PC"]):
        left, right = registry[i * 2], registry[i * 2 + 1]
        return_string += f"{reg}: {left:02X}{right:02X} "
    return_string = return_string[:-1]
    return return_string


@ComponentEvents.RequestReset
def reset():
    for i in range(12):
        registry[i] = 0
