import colorama
VERSION = MAJOR, MINOR, DEBUG, DEV = 0, 0, 0, 12
__version__ = ".".join(map(str, [MAJOR, MINOR, DEBUG])) + ("." + str(DEV) + " DEV" if DEV else " RELEASE")
__authors__ = "Alyce Osbourne", "Boštjan Mejak"
__github__ = "https://github.com/AlyceOsbourne/GameBoaV2"
__license__ = "MIT"

__license_text__ = """
{license} Copyright 2022 {authors} 
<{github}> 

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(license=__license__ ,authors=", ".join(__authors__), github=__github__)


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
print(__license_text__)