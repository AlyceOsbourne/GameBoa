from bus import Bus
from constants import Instruction


class CPU:

    def fetch(self, bus: 'Bus'):
        raise NotImplementedError('fetch not implemented')

    def fetch16(self, bus: 'Bus'):
        return self.fetch(bus) | (self.fetch(bus) << 8)

    def decode(self, opcode: int, cb=False):
        return getattr(self, 'cb_' if cb else '' + 'instructions')[opcode]

    def execute(self, bus: 'Bus', instruction: 'Instruction'):
        raise NotImplementedError('execute not implemented')