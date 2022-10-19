from pathlib import Path

from components.cpu import CPU
from tests.mock_components import MockBus
from components.system_mappings import Instruction


OP_CODES_FILE = Path(__file__).parent.parent.parent / "op_codes.json"


def test_decoding_op_code():
    mock_bus = MockBus()
    instructions, cb_instructions = Instruction.load(OP_CODES_FILE).values()
    cpu = CPU(instructions=instructions, cb_instructions=cb_instructions)

    coroutine = cpu.run(bus=mock_bus)
    coroutine.send(None)

    assert coroutine.send(0xCB) == instructions[0xCB]
    assert cpu.is_cb_instruction
    assert coroutine.send(0x00) == instructions[0x00]
    assert not cpu.is_cb_instruction
    assert coroutine.send(0x00) == instructions[0x00]
    assert not cpu.is_cb_instruction
