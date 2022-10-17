from pathlib import Path

from mock_components import MockBus
from components import cpu, system_mappings


def test_cpu_opcode_decoding():
    op_codes_file = Path(__file__).parent.parent.parent / "op_codes.json"
    instructions, cb_instructions = system_mappings.Instructions.load(
        op_codes_file
    ).values()
    _cpu = cpu.CPU(
        instructions=instructions,
        cb_instructions=cb_instructions,
    )
    coroutine = _cpu.run(bus=MockBus())
    coroutine.send(None)
    assert coroutine.send(0xCB) == instr[0xCB]
    assert _cpu.is_cb
    assert coroutine.send(0x00) == cb_instr[0x00]
    assert not _cpu.is_cb
    assert coroutine.send(0x00) == instr[0x00]
    assert not _cpu.is_cb
