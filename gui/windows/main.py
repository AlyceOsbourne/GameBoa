from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox


LOGO_ICON = QIcon("gui/icons/logo.svg")
QUIT_ICON = QIcon("gui/icons/quit.svg")
ABOUT_ICON = QIcon("gui/icons/about.svg")


class MainWindow(QMainWindow):
    """The main window of GameBoa."""

    def __init__(self):
        super().__init__()

        self.set_properties()
        self.create_actions()
        self.create_menu_bar()
        self.create_status_bar()

    def set_properties(self) -> None:
        """Sets a fixed size, a logo icon, and a title."""
        self.setFixedSize(500, 500)
        self.setWindowIcon(LOGO_ICON)
        self.setWindowTitle("GameBoa")

    def create_actions(self) -> None:
        """Creates actions for the menu bar."""

        # Quit action
        self.quit_action = QAction()
        self.quit_action.setIcon(QUIT_ICON)
        self.quit_action.setText("Quit...")
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        self.quit_action.setStatusTip("Offers to quit GameBoa.")

        # About action
        self.about_action = QAction()
        self.about_action.setIcon(LOGO_ICON)
        self.about_action.setText("About...")
        self.about_action.setShortcut("Ctrl+I")
        self.about_action.triggered.connect(self.about)
        self.about_action.setStatusTip("Shows an About GameBoa message box.")

    def create_menu_bar(self) -> None:
        """Creates a menu bar with actions in separate menus."""

        # Menu bar
        self.menu_bar: QMenuBar = self.menuBar()

        # General menu
        general_menu = self.menu_bar.addMenu("General")

        # Help menu
        help_menu = self.menu_bar.addMenu("Help")

        # General > Quit...
        general_menu.addAction(self.quit_action)

        # Help > About...
        help_menu.addAction(self.about_action)

    def create_status_bar(self):
        """Creates a status bar to show status messages."""
        self.status_bar: QStatusBar = self.statusBar()

    def about(self) -> None:
        """Shows an About GameBoa message box."""
        parent = self
        title = "About GameBoa"
        message = "A Python-based Game Boy emulator.\n\nCopyright 2022 Alyce Osbourne"
        QMessageBox.about(parent, title, message)

    def closeEvent(self, event) -> None:
        """Offers to quit GameBoa."""
        parent = self
        title = "Quit"
        message = "Do you want to quit GameBoa?"
        answer = QMessageBox.question(parent, title, message)

        if answer == answer.Yes:
            event.accept()
        else:
            event.ignore()
