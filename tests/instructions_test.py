import constants
import bus
import bus.cpu
import pytest
instructions, cb_instructions = constants.Instruction.load_instructions('../op_codes.json').values()


_cpu = bus.cpu.CPU(
    instructions=instructions,
    cb_instructions=cb_instructions,
)
ppu = bus.PPU()
mmu = bus.MMU()
timer = bus.Timer()
register = bus.Register()
_bus = bus.Bus(
    ppu=ppu,
    mmu=mmu,
    timer=timer,
    register=register,
    cpu=_cpu,
)
_cpu.bus = _bus



def run_all_instructions():
    for instruction in instructions.values():
        _cpu.execute(_bus, instruction)

    for instruction in cb_instructions.values():
        _cpu.execute(_bus, instruction)

if __name__ == "__main__":
    run_all_instructions()