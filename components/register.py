class Register:
    """
    Stores memory data and CPU instructions while processing them.

    The accessors support both 8-bit and 16-bit registers.
    """

    a, b, c, d, e, h, l, f, sp, pc = (
        0x01,
        0x00,
        0x13,
        0x00,
        0xD8,
        0x01,
        0x4D,
        0xB0,
        0xFFFE,
        0x0100,
    )

    # Convert two 8-bit registers into one 16-bit register.
    _get_16 = lambda self, r1, r2: (self.read(r1) << 8) | self.read(r2)
    _set_16 = lambda self, r1, r2, value: (
        self.write(r1, (value >> 8) & 0xFF),
        self.write(r2, value & 0xFF),
    )

    # Provide a getter and a setter for 16-bit registers.
    af = property(
        lambda self: self._get_16("a", "f"),
        lambda self, value: self._set_16("a", "f", value),
        doc="AF reg",
    )
    bc = property(
        lambda self: self._get_16("b", "c"),
        lambda self, value: self._set_16("b", "c", value),
        doc="BC reg",
    )
    de = property(
        lambda self: self._get_16("d", "e"),
        lambda self, value: self._set_16("d", "e", value),
        doc="DE reg",
    )
    hl = property(
        lambda self: self._get_16("h", "l"),
        lambda self, value: self._set_16("h", "l", value),
        doc="HL reg",
    )

    def __str__(self):
        return (
            f"A: {self.a:02X} F: {self.f:02X} B: {self.b:02X} C: {self.c:02X} D: {self.d:02X}"
            f" E: {self.e:02X} H: {self.h:02X} L: {self.l:02X} SP: {self.sp:04X} PC: {self.pc:04X}"
        )

    def read(self, register: str):
        if not hasattr(self, register.lower()):
            raise Exception(f"Invalid register {register}.")
        return getattr(self, register.lower(), None)

    def write(self, register: str, value: int):
        if not hasattr(self, register.lower()):
            raise Exception(f"Invalid register {register}")
        setattr(self, register.lower(), value)
