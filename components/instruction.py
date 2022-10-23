import json
from typing import NamedTuple


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
    def load(cls, json_file: str = "/op_codes.json") -> dict:
        loaded_instructions: dict = {}

        try:
            with open(json_file, "r") as op_codes_file:
                json_data = json.load(op_codes_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {json_file} in current directory.")

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