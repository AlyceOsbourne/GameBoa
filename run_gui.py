from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
import __metadata__ as meta
from gui.windows.main import MainWindow


APP_NAME = "GameBoa"
APP_VERSION_NUMBER = meta.__version__
LOGO_ICON = QIcon("gui/icons/logo.svg")


def main() -> None:
    app = QApplication()
    app.setWindowIcon(LOGO_ICON)
    app.setApplicationName(APP_NAME)
    app.setDesktopFileName(APP_NAME)
    app.setApplicationVersion(APP_VERSION_NUMBER)

    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == "__main__":
    main()
