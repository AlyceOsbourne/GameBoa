from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox


OK_BUTTON = QDialogButtonBox.StandardButton.Ok
CANCEL_BUTTON = QDialogButtonBox.StandardButton.Cancel


class SettingsDialogWindow(QDialog):
    """A dialog window that provides changing GameBoa's settings."""

    def __init__(self):
        super().__init__()

        self.set_options()
        self.set_properties()
        self.set_custom_layout()
        self.connect_signals_with_slots()

        self.exec()

    def set_options(self) -> None:
        """Sets options that represent GameBoa's settings."""
        self.test_option = QCheckBox()
        self.test_option.setText("Test")
        self.test_option.setChecked(True)

    def set_properties(self) -> None:
        """
        Sets specific properties for the dialog window.

        > Sets the title to be Settings.
        > Sets the standard buttons to be OK and Cancel.
        """
        self.setWindowTitle("Settings")

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(OK_BUTTON | CANCEL_BUTTON)

    def set_custom_layout(self) -> None:
        """Sets a custom layout for the widgets on the dialog window."""
        ...

    def connect_signals_with_slots(self) -> None:
        """Connects event signals with relevant slots as actions."""
        self.accepted.connect(self.save_settings)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def save_settings(self) -> None:
        """Saves GameBoa's settings to a specific file."""
        ...
