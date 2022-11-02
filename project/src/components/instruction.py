import gzip
import json
from pathlib import Path
from pprint import pprint
from typing import NamedTuple
from functools import partial

from project.src.system import bus
from project.src.system import ComponentEvents
from project.src.system.system_paths import opcode_path


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
    def load(cls, file_path: Path) -> dict:
        try: json_data = json.loads(gzip.decompress(file_path.read_bytes()).decode())
        except FileNotFoundError: raise FileNotFoundError(f"Could not find {file_path} in current directory.")
        return {
            category: {
                int(op_code, 16): cls(
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
                for op_code, op_code_settings in operation.items()
            }
            for category, operation in json_data.items()
        }

    def __str__(self) -> str:
        return f"{self.mnemonic}({self.operand1}, {self.operand2})"

instructions, cb_instructions = Instruction.load(opcode_path).values()


