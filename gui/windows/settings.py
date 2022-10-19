from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QHBoxLayout


OK_BUTTON = QDialogButtonBox.StandardButton.Ok
CANCEL_BUTTON = QDialogButtonBox.StandardButton.Cancel


class SettingsDialog(QDialog):
    """A dialog that provides changing GameBoa's settings."""

    def __init__(self):
        super().__init__()

        self.set_options()
        self.set_properties()
        self.set_custom_layout()
        self.connect_signals_with_slots()

    def set_options(self) -> None:
        """Sets options that represent GameBoa's settings."""
        self.test_option = QCheckBox()
        self.test_option.setText("Test")
        self.test_option.setChecked(True)

    def set_properties(self) -> None:
        """
        Sets specific properties for the dialog.

        > Sets a fixed size.
        > Sets the title to be Settings.
        > Sets the standard buttons to be OK and Cancel.
        """
        self.setFixedSize(300, 300)
        self.setWindowTitle("Settings")

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(OK_BUTTON | CANCEL_BUTTON)

    def set_custom_layout(self) -> None:
        """Sets a horizontal layout for the widgets."""
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.test_option)
        self.setLayout(horizontal_layout)

    def connect_signals_with_slots(self) -> None:
        """Connects event signals with relevant widget actions."""
        self.accepted.connect(self.save_settings)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def save_settings(self) -> None:
        """Saves GameBoa's settings."""
        ...
