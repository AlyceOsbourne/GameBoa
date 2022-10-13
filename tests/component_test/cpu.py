from components import cpu, system_mappings
import pathlib
import pytest


class MockBus:
    def read(self, address, length=1):
        return 0

    def write(self, address, value):
        pass


def test_cpu_opcode_decoding():
    op_codes_path = pathlib.Path(__file__).parent.parent.parent / 'op_codes.json'
    instr, cb_instr = system_mappings.Instruction.load_instructions(op_codes_path).values()
    _cpu = cpu.CPU(
        instructions=instr,
        cb_instructions=cb_instr,
    )
    coro = _cpu.run(bus=MockBus())
    coro.send(None)
    assert coro.send(0xcb) == instr[0xcb]
    assert _cpu.is_cb
    assert coro.send(0x00) == cb_instr[0x00]
    assert not _cpu.is_cb
    assert coro.send(0x00) == instr[0x00]
    assert not _cpu.is_cb


test_cpu_opcode_decoding()
