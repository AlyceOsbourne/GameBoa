#!/usr/bin/env python3.10


# Copyright 2022 Alyce Osbourne, Boštjan Mejak
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from sys import exit

from PySide6.QtGui import QIcon
from PySide6.QtCore import QLockFile
from PySide6.QtWidgets import QApplication, QMessageBox

from gui.windows.main import MainWindow


APP_NAME = "GameBoa"
APP_VERSION = "1.0.0"
APP_LOCK_FILE = QLockFile("running.lock")
APP_LOGO_ICON = QIcon("gui/icons/logo.svg")


class GameBoa:
    """An entry point to GameBoa."""

    def __init__(self):
        self.app = QApplication()
        self.app.setApplicationName(APP_NAME)
        self.app.setDesktopFileName(APP_NAME)
        self.app.setWindowIcon(APP_LOGO_ICON)
        self.app.setApplicationVersion(APP_VERSION)

    def run(self):
        """Run GameBoa if it is unlocked, else show a warning."""
        if self.is_app_unlocked():
            main_window = MainWindow()
            main_window.showMaximized()
            app_running = self.app.exec()
            exit(app_running)

        parent: QWidget = None
        title: str = "Warning"
        message: str = "GameBoa is already running!"
        QMessageBox.warning(parent, title_text, message_text)

    def is_app_unlocked(self):
        """Check whether GameBoa is unlocked, hence not running."""
        return APP_LOCK_FILE.tryLock()


if __name__ == "__main__":
    app = GameBoa()
    app.run()
