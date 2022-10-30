import gzip
import json
from pathlib import Path
from typing import NamedTuple

from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents
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


instructions, cb_instructions = Instruction.load(opcode_path)

EventHandler.subscribe(
    ComponentEvents.RequestDecode,
    lambda op_code, is_cb_instruction: EventHandler.publish(
        ComponentEvents.RequestExecute,
        cb_instructions[op_code] if is_cb_instruction else instructions[op_code],
    ),
)
