from datetime import date

__version__ = __major__, __minor__, __micro__ = 0, 0, 1
__app_name__ = "GameBoa"
__app_version__ = "{}.{}.{}".format(*__version__)
__license__ = "MIT License"
__year__ = date.today().year
__authors__ = "Alyce Osbourne, Boštjan Mejak"
__github_link__ = "https://github.com/AlyceOsbourne/GameBoa"

__about__ = f"""
{__app_name__} {__app_version__}
Authors: {__authors__}
License: {__license__}
GitHub: {__github_link__}
"""

__notice__ = f"""
Copyright {__year__} {__authors__}

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


print(__about__)
print(__notice__)
