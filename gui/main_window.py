from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QWidget


LOGO_ICON = QIcon("gui/icons/logo.svg")
QUIT_ICON = QIcon("gui/icons/quit.svg")


class MainWindow(QMainWindow):
    """The main window of pyGB."""

    def __init__(self):
        super().__init__()

        self.set_properties()
        self.create_actions()
        self.create_menu_bar()
        self.create_status_bar()
        self.set_window_layout()

    def set_properties(self) -> None:
        """Sets a fixed size of 500 by 500 pixels and a title."""
        self.setFixedSize(500, 500)
        self.setWindowTitle("pyGB")
        self.setWindowIcon(LOGO_ICON)

    def create_actions(self) -> None:
        """Creates actions for the menu bar."""

        # Quit action
        self.quit_action = QAction()
        self.quit_action.setIcon(QUIT_ICON)
        self.quit_action.setText("Quit...")
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        self.quit_action.setStatusTip("Offers to quit pyGB.")

    def create_menu_bar(self) -> None:
        """Creates a menu bar with actions in separate menus."""

        # Menu bar
        self.menu_bar: QMenuBar = self.menuBar()

        # General menu
        general_menu = self.menu_bar.addMenu("General")

        # General > Quit...
        general_menu.addAction(self.quit_action)

    def create_status_bar(self):
        """Creates a status bar to show status messages."""
        self.status_bar: QStatusBar = self.statusBar()

    def set_window_layout(self) -> None:
        """Sets a horizontal layout for widgets on the main window."""

        # THIS IS FOR A FUTURE IMPLEMENTATION WHEN WIDGETS WILL EXIST
        # widget_container = QWidget()
        # horizontal_layout = QHBoxLayout()
        # horizontal_layout.addWidget(self.XY)
        # widget_container.setLayout(horizontal_layout)
        # self.setCentralWidget(widget_container)

    def closeEvent(self, event) -> None:
        """Offers to quit pyGB."""
        parent = self
        title = "Quit"
        message = "Do you want to quit pyGB?"
        answer = QMessageBox.question(parent, title, message)

        if answer == answer.Yes:
            event.accept()
        else:
            event.ignore()
