from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenuBar, QStatusBar, QFileDialog

from gui.windows.settings import SettingsDialog


LOGO_ICON = QIcon("gui/icons/logo.svg")
QUIT_ICON = QIcon("gui/icons/quit.svg")
ABOUT_ICON = QIcon("gui/icons/about.svg")
SETTINGS_ICON = QIcon("gui/icons/settings.svg")


class MainWindow(QMainWindow):
    """The main window of GameBoa."""

    def __init__(self):
        super().__init__()

        self.set_properties()
        self.create_actions()
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()

    def set_properties(self) -> None:
        """Sets a fixed size of 500 by 500 pixels."""
        self.setFixedSize(500, 500)

    def create_actions(self) -> None:
        """Creates actions for the menu bar."""

        # About action
        self.about_action = QAction()
        self.about_action.setIcon(LOGO_ICON)
        self.about_action.setText("About...")
        self.about_action.setShortcut("Ctrl+I")
        self.about_action.triggered.connect(self.about)
        self.about_action.setStatusTip("Shows an About GameBoa message box.")

        # Settings action
        self.settings_action = QAction()
        self.settings_action.setIcon(SETTINGS_ICON)
        self.settings_action.setText("Settings...")
        self.settings_action.setShortcut("Ctrl+Alt+S")
        self.settings_action.setStatusTip("Shows the Settings dialog.")
        self.settings_action.triggered.connect(self.show_settings_dialog)

        # Quit action
        self.quit_action = QAction()
        self.quit_action.setIcon(QUIT_ICON)
        self.quit_action.setText("Quit...")
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        self.quit_action.setStatusTip("Offers to quit GameBoa.")

        # Load ROM action
        self.load_rom_action = QAction()
        self.load_rom_action.setText("Load ROM...")
        self.load_rom_action.setShortcut("Ctrl+O")
        self.load_rom_action.setStatusTip("Loads a ROM file.")
        self.load_rom_action.triggered.connect(self.load_rom)

    def create_menu_bar(self) -> None:
        """Creates a menu bar with actions in separate menus."""

        # Menu bar
        self.menu_bar: QMenuBar = self.menuBar()

        # General menu
        general_menu = self.menu_bar.addMenu("General")

        # Edit menu
        edit_menu = self.menu_bar.addMenu("Edit")

        # Help menu
        help_menu = self.menu_bar.addMenu("Help")

        # General > Load ROM...
        general_menu.addAction(self.load_rom_action)

        # General > Quit...
        general_menu.addAction(self.quit_action)

        # Edit > Settings...
        edit_menu.addAction(self.settings_action)

        # Help > About...
        help_menu.addAction(self.about_action)

    def create_tool_bar(self):
        """Creates a tool bar with buttons in separate areas."""

        # General
        general_area = self.addToolBar("General")

        # Edit
        edit_area = self.addToolBar("Edit")

        # Help
        help_area = self.addToolBar("Help")

        # General > Quit
        general_area.addAction(self.quit_action)

        # Edit > Settings
        help_area.addAction(self.settings_action)

        # Help > About
        help_area.addAction(self.about_action)

    def create_status_bar(self):
        """Creates a status bar to show status messages."""
        self.status_bar: QStatusBar = self.statusBar()

    def about(self) -> None:
        """Shows an About GameBoa message box."""
        parent = self
        title = "About GameBoa"
        message = "A Python-based Game Boy emulator.\n\nCopyright 2022 Alyce Osbourne"
        QMessageBox.about(parent, title, message)

    def show_settings_dialog(self):
        """Shows the Settings dialog."""
        self.settings_dialog = SettingsDialog()
        self.settings_dialog.exec()

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

    def load_rom(self):
        """Loads a ROM file."""
        # open file dialog
        # load ROM if extension is .gb, .gbc, or .zip
        # show error message if extension is not .gb, .gbc, or .zip
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("*GB; *GBC; *ZIP")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setWindowTitle("Load ROM")
        file_dialog.setLabelText(QFileDialog.Accept, "Load")
        file_dialog.setLabelText(QFileDialog.Reject, "Cancel")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            print(file_path)

            if file_path.endswith(".gb") or file_path.endswith(".gbc") or file_path.endswith(".zip"):
                print("Valid ROM")
            else:
                print("Invalid ROM")
                parent = self
                title = "Invalid ROM"
                message = "The ROM file must be a .gb, .gbc, or .zip file."
                QMessageBox.critical(parent, title, message)

        else:
            print("Cancelled")


