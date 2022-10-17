import radon.complexity
import ast
import pathlib
component_path = pathlib.Path(__file__).parent.parent / 'components'


def test_performance():
    for path in [
        component_path / 'cpu.py',
        component_path / 'system_mappings.py',
    ]:
       # rank using radon
        radon_rank = radon.complexity.cc_visit(path.read_text())
        for rank in radon.complexity.sorted_results(radon_rank, order=radon.complexity.SCORE)[:10]:
            if hasattr(rank, 'classname'):
                class_name = rank.classname + "."
            else:
                class_name = ''
            name, rank = rank.name, rank.complexity
            print(f'{class_name}{name}: {rank} => {radon.complexity.cc_rank(rank)}')







test_performance()