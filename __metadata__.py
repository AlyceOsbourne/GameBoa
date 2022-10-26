import colorama
from datetime import date

VERSION = MAJOR, MINOR, MICRO, NIGHTLY = 0, 0, 0, 13
__version__ = f'{MAJOR}.{MINOR}.{MICRO}{f"-dev{NIGHTLY}" if NIGHTLY else "-release"}'
__authors__ = "Alyce Osbourne", "Boštjan Mejak"
__github__ = "https://github.com/AlyceOsbourne/GameBoaV2"
__license__ = "MIT"


metadata = f"""GameBoa {__version__}
GitHub: {__github__}
Authors: {", ".join(__authors__)}
License: {__license__}
"""

# make the metadata string rainbow
for i, line in enumerate(metadata.splitlines()):
    if i == 1:
        metadata = metadata.replace(line, colorama.Fore.LIGHTBLUE_EX + line + colorama.Fore.RESET)
    elif i == 2:
        metadata = metadata.replace(line, colorama.Fore.LIGHTGREEN_EX + line + colorama.Fore.RESET)
    elif i == 3:
        metadata = metadata.replace(line, colorama.Fore.LIGHTYELLOW_EX + line + colorama.Fore.RESET)
    elif i == 4:
        metadata = metadata.replace(line, colorama.Fore.LIGHTCYAN_EX + line + colorama.Fore.RESET)
    else:
        metadata = metadata.replace(line, colorama.Fore.CYAN + line + colorama.Fore.RESET)

print(metadata)
