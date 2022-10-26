import gzip
import json
from pathlib import Path
from typing import NamedTuple

from project.src.system import EventHandler

default_path = Path("../../resources/ops.bin")

class Instruction(
    NamedTuple(
        "Instruction",
        [
            ("op_code", int),
            ("mnemonic", str),
            ("length", int),
            ("cycles", int),
            ("flags", str),
            ("addr", int),
            ("group", str),
            ("operand1", str | None),
            ("operand2", str | None),
        ],
    )
):
    """Instructions of the CPU."""

    @classmethod
    def load(cls, file_path:Path) -> dict:
        loaded_instructions: dict = {}
        try:
            json_data = json.loads(gzip.decompress(file_path.read_bytes()).decode())
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {file_path} in current directory.")

        for category, operation in json_data.items():
            if category not in loaded_instructions:
                loaded_instructions[category] = {}

            for op_code, op_code_settings in operation.items():
                op_code = int(op_code, 16)
                loaded_instructions[category][op_code] = cls(
                    op_code,
                    op_code_settings["mnemonic"],
                    op_code_settings.get("length"),
                    op_code_settings.get("cycles"),
                    op_code_settings.get("flags"),
                    op_code_settings.get("addr"),
                    op_code_settings.get("group"),
                    op_code_settings.get("operand1", None),
                    op_code_settings.get("operand2", None),
                )

        return loaded_instructions

    def __str__(self) -> str:
        return f"{self.mnemonic}({self.operand1}, {self.operand2})"


class Decoder:
    """ simply handles the decoding of the opcodes """

    def __init__(self, instruction_set):
        self.instructions, self.cb_instructions = instruction_set

    def decode(self, op_code: int, is_cb: bool) -> Instruction:
        """Decodes the given op_code into an instruction."""
        return getattr(self, ("cb_" if is_cb else "") + "instructions").get(op_code, None)

    def __str__(self):
        return f"{self.instructions} {self.cb_instructions}"

decoder = Decoder(Instruction.load(default_path))

@EventHandler.subscriber('Decode OpCode')
def decode_op_code(op_code: int, is_cb: bool):
    EventHandler.publish('Execute Instruction', decoder.decode(op_code, is_cb))