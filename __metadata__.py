import colorama
VERSION = MAJOR, MINOR, DEBUG, DEV = 0, 0, 0, 12
__version__ = ".".join(map(str, [MAJOR, MINOR, DEBUG])) + ("." + str(DEV) + " DEV" if DEV else " RELEASE")
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
    metadata = metadata.replace(line, colorama.Fore.LIGHTMAGENTA_EX + line + colorama.Fore.RESET)
    if i == 1:
        metadata = metadata.replace(line, colorama.Fore.LIGHTBLUE_EX + line + colorama.Fore.RESET)
    elif i == 2:
        metadata = metadata.replace(line, colorama.Fore.LIGHTGREEN_EX + line + colorama.Fore.RESET)
    elif i == 3:
        metadata = metadata.replace(line, colorama.Fore.LIGHTYELLOW_EX + line + colorama.Fore.RESET)
    elif i == 4:
        metadata = metadata.replace(line, colorama.Fore.LIGHTCYAN_EX + line + colorama.Fore.RESET)

print(metadata)