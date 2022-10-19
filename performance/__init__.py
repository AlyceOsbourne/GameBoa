import radon.complexity
import cProfile
import pathlib

from components.timer import Timer
from components.register import Register
from components.cpu import CPU
from components.memory_bank import MemoryBank
from components.cartridge import Cartridge
from components.bus import Bus
from components.system_mappings import Instructions

component_path = pathlib.Path(__file__).parent.parent / 'components'


def test_complexity(*paths, num_entries=5):
    for path in paths:
        print(f"Testing complexity for {path} and getting the top {num_entries} most complex functions")
        radon_rank = radon.complexity.cc_visit(path.read_text())
        for rank in radon.complexity.sorted_results(radon_rank, order=radon.complexity.SCORE)[:num_entries]:
            if hasattr(rank, 'classname'):
                class_name = rank.classname + "."
            else:
                class_name = ''
            name, rank = rank.name, rank.complexity
            print(f'{class_name}{name}: {rank} => {radon.complexity.cc_rank(rank)}')
        print()


def test_performance():
    timer = Timer()
    register = Register()
    cpu = CPU(
        *Instructions.load().values()
    )
    bus = Bus()



def run_tests():
    test_complexity(
        component_path / 'cpu.py',
        component_path / 'system_mappings.py',
        component_path / 'bus.py',
        component_path / 'ppu.py',
        component_path / 'cartridge.py',
        component_path / 'register.py',
        component_path / 'timer.py',
        component_path / 'memory_bank.py',
        num_entries=100
    )
    test_performance()


if __name__ == '__main__':
    run_tests()