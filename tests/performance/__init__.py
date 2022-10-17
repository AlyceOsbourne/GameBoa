from pathlib import Path
from radon import complexity


COMPONENTS_PATH = Path(__file__).parent.parent / "components"


def test_complexity():
    for path in [
        COMPONENTS_PATH / "cpu.py",
        COMPONENTS_PATH / "system_mappings.py",
    ]:
        radon_rank = complexity.cc_visit(path.read_text())
        for rank in complexity.sorted_results(radon_rank, complexity.SCORE)[:10]:
            if hasattr(rank, "classname"):
                class_name = rank.classname + "."
            else:
                class_name = ""
            name, rank = rank.name, rank.complexity
            print(f"{class_name}{name}: {rank} => {complexity.cc_rank(rank)}")


test_complexity()
