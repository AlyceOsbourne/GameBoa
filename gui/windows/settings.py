# import so we can increment numbers, take strings as input etc etc
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox, QLineEdit, QLabel,
)

from core.config import config

OK_BUTTON = QDialogButtonBox.StandardButton.Ok
CANCEL_BUTTON = QDialogButtonBox.StandardButton.Cancel


class SettingsTab:
    """A class to handle a tab in the settings window."""

    def __init__(self, tab_widget: QTabWidget, name: str):
        self.tab_widget = tab_widget
        self.name = name
        self.tab = QWidget()
        self.tab_widget.addTab(self.tab, self.name)
        self.layout = QVBoxLayout()
        self.tab.setLayout(self.layout)

    def add_checkbox(self, text: str, option: str) -> QCheckBox:
        """Adds a checkbox to the tab."""
        checkbox = QCheckBox(text)
        checkbox.setChecked(config.get_boolean(self.name, option))
        checkbox.stateChanged.connect(lambda: config.set(self.name, option, str(checkbox.isChecked())))
        self.layout.addWidget(checkbox)
        return checkbox

    def add_spinbox(self, text: str, option: str, min: int, max: int) -> QSpinBox:
        """Adds a spinbox to the tab."""
        spinbox = QSpinBox()
        spinbox.setMinimum(min)
        spinbox.setMaximum(max)
        spinbox.setValue(config.getint(self.name, option))
        spinbox.valueChanged.connect(lambda: config.set(self.name, option, str(spinbox.value())))
        self.layout.addWidget(spinbox)
        return spinbox

    def add_line_edit(self, text: str, option: str) -> QLineEdit:
        """Adds a line edit to the tab."""
        # should have a label to the left of the line edit
        label = QLabel(text)
        line_edit = QLineEdit()
        line_edit.setText(config.get(self.name, option))
        line_edit.textChanged.connect(lambda: config.set(self.name, option, line_edit.text()))
        widget_pair = QWidget()
        widget_pair_layout = QHBoxLayout()
        widget_pair.setLayout(widget_pair_layout)
        widget_pair_layout.addWidget(label)
        widget_pair_layout.addWidget(line_edit)
        self.layout.addWidget(widget_pair)
        return line_edit






class SettingsDialog(QDialog):
    """A dialog that provides changing GameBoa's settings."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)

        self.tab_widget = QTabWidget()
        for section in config.sections():
            settings_tab = SettingsTab(self.tab_widget, section)
            for option in config.options(section):
                value = config.get_value_as_dtype(section, option)
                if isinstance(value, bool):
                    settings_tab.add_checkbox(option, option)
                elif isinstance(value, int):
                    settings_tab.add_spinbox(option, option, 0, 100)
                elif isinstance(value, str):
                    settings_tab.add_line_edit(option, option)





        self.button_box = QDialogButtonBox(OK_BUTTON | CANCEL_BUTTON)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
