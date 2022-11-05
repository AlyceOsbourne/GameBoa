from array import array
from .cartridge import Cart

class Memory:
    data: array
    start_offset: int
    def __init__(self, size: int, start_offset: int = 0, read_only: bool = False):
        self.data = array("B", [0] * size)
        self.start_offset = start_offset
        self.read_only = read_only

    def read(self, address: int) -> int:
        return self.data[address - self.start_offset]

    def write(self, address: int, value: int):
        if self.read_only:
            raise Exception("Memory is read only")
        self.data[address - self.start_offset] = value

V_RAM_SIZE = 0x2000
V_RAM_OFFSET = 0x2000
H_RAM_SIZE = 0x80
H_RAM_OFFSET = 0x8000
OAM_SIZE = 0xA0
OAM_OFFSET = 0xFE00
IO_SIZE = 0x80
IO_OFFSET = 0xFF00
Z_RAM_SIZE = 0x7F
Z_RAM_OFFSET = 0xFF80


v_ram: Memory = Memory(V_RAM_SIZE, V_RAM_OFFSET)
h_ram: Memory = Memory(H_RAM_SIZE, H_RAM_OFFSET)
oam: Memory = Memory(OAM_SIZE, OAM_OFFSET)
io: Memory = Memory(IO_SIZE, IO_OFFSET)
z_ram:Memory = Memory(Z_RAM_SIZE, Z_RAM_OFFSET)
cart: Cart | None = None

def read(address: int) -> int:
    if address < V_RAM_OFFSET:
        if cart:
            return cart.read(address)
        return 0
    elif address < H_RAM_OFFSET:
        return v_ram.read(address)
    elif address < OAM_OFFSET:
        return h_ram.read(address)
    elif address < IO_OFFSET:
        return oam.read(address)
    elif address < Z_RAM_OFFSET:
        return io.read(address)
    else:
        return z_ram.read(address)

def write(address: int, value: int):
    if address < V_RAM_OFFSET:
        if cart:
            cart.write(address, value)
    elif address < H_RAM_OFFSET:
        v_ram.write(address, value)
    elif address < OAM_OFFSET:
        h_ram.write(address, value)
    elif address < IO_OFFSET:
        oam.write(address, value)
    elif address < Z_RAM_OFFSET:
        io.write(address, value)
    else:
        z_ram.write(address, value)

def load_cartridge(array: array):
    global cart
    cart = Cart(array)

