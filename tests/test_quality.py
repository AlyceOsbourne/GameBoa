from enum import IntFlag

import radon.metrics
import radon.complexity
import pathlib
import colorama

optimal = colorama.Fore.GREEN + "{}" + colorama.Fore.RESET
warning_str = colorama.Fore.YELLOW + '{}' + colorama.Fore.RESET
urgent_str = colorama.Fore.RED + '{}' + colorama.Fore.RESET



class Rank(IntFlag):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4

    def __str__(self):
        match self.value:
            case 0:
                return optimal.format(self.name)
            case 4:
                return urgent_str.format(self.name)
            case _:
                return warning_str.format(self.name)



# todo, more study needs to go into the values here, besides the radon related ones these are fairly arbitrary chosen


def rank_difficulty(difficulty:int):
    if difficulty < 10:
        return Rank.A
    elif difficulty < 20:
        return Rank.B
    elif difficulty < 30:
        return Rank.C
    elif difficulty < 40:
        return Rank.D
    else:
        return Rank.E


def rank_volume(volume:int):
    if volume < 200:
        return Rank.A
    elif volume < 400:
        return Rank.B
    elif volume < 600:
        return Rank.C
    elif volume < 800:
        return Rank.D
    else:
        return Rank.E


def rank_bugs(bugs:int):
    if bugs < 1:
        return Rank.A
    elif bugs < 2:
        return Rank.B
    elif bugs < 3:
        return Rank.C
    elif bugs < 4:
        return Rank.D
    else:
        return Rank.E

def rank_time(time:int):
    if time < 20:
        return Rank.A
    elif time < 40:
        return Rank.B
    elif time < 60:
        return Rank.C
    elif time < 100:
        return Rank.D
    else:
        return Rank.E

def rank_complexity(complexity:int):
    if complexity < 6:
        return Rank.A
    elif complexity < 11:
        return Rank.B
    elif complexity < 21:
        return Rank.C
    elif complexity < 31:
        return Rank.D
    else:
        return Rank.E


def rank_maintainability(maintainability:int):
    # gives a wider range of scores than the radon version, consider the min/max to be the same,
    # bit the ranks between are different, this is actually a slightly harsher critic
    if maintainability > 19:
        return Rank.A
    elif maintainability > 15:
        return Rank.B
    elif maintainability > 10:
        return Rank.C
    elif maintainability > 5:
        return Rank.D
    else:
        return Rank.E



def test_quality(folders_to_glob):
    # recursively search for all python files in the given folders
    for file in folders_to_glob.glob('**/*.py'):
        if file.is_dir():
            test_quality(file)
        else:
            file_contents = file.read_text()
            maintainability = radon.metrics.mi_visit(file_contents, True)
            complexity = radon.complexity.cc_visit(file_contents)
            halstead = radon.metrics.h_visit(file_contents)

            title_len = 30
            output_str = f'{file.name}:\n'
            output_str += f'\tModule ranks:\n'
            output_str += f'\t\t| {"maintainability":<{title_len}} | {rank_maintainability(maintainability)} |\n'
            output_str += f'\t\t| {"difficulty":<{title_len}} | {rank_difficulty(halstead.total.difficulty)} |\n'
            output_str += f'\t\t| {"volume":<{title_len}} | {rank_volume(halstead.total.volume)} |\n'
            output_str += f'\t\t| {"time":<{title_len}} | {rank_time(halstead.total.time)} |\n'
            output_str += f'\t\t| {"bugs":<{title_len}} | {rank_bugs(halstead.total.bugs)} |\n\n'
            if len(complexity) > 0:
                output_str += f'\tfunction complexity ranks:\n'
                for function in complexity:
                    output_str += f'\t\t| {function.name:<{title_len}} | {rank_complexity(function.complexity)} |\n'
            print(output_str)


if __name__ == "__main__":
    root = pathlib.Path.cwd().parent
    for folder in [
        'components',
        'tests',
        'gui'
    ]:
        test_quality(root / folder)
