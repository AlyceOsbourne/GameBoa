class Bus:
    def __init__(self, register, memory, decoder):
        self.register = register
        self.memory = memory
        self.decoder = decoder

    def fetch_op_code(self):
        return self.register['PC']

    def read_byte(self, address):
        return self.memory[address]

    def write_byte(self, address, value):
        self.memory[address] = value