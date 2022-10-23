
from core.system_mappings import Instruction


class Decoder:
    """ simply handles the decoding of the opcodes """

    def __init__(self, instruction_set):
        self.instructions, self.cb_instructions = instruction_set

    def decode(self, op_code: int, is_cb: bool) -> Instruction:
        """Decodes the given op_code into an instruction."""
        return getattr(self, ("cb_" if is_cb else "") + "instructions").get(op_code, None)