from PySide6.QtWidgets import (
    QLabel,
    QDialog,
    QWidget,
    QSpinBox,
    QCheckBox,
    QLineEdit,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
)

from core.config import ConfigManager


OK_BUTTON = QDialogButtonBox.StandardButton.Ok
CANCEL_BUTTON = QDialogButtonBox.StandardButton.Cancel


class SettingsTab:
    """A tab to be added to the Settings dialog."""

    def __init__(self, name: str):
        self.name: str = name

        self.tab_area: QWidget = QWidget()

        self.tab_widget: QTabWidget = QTabWidget()
        self.tab_widget.addTab(self.tab_area, self.name)

        self.config_manager = ConfigManager()

        self.vertical_layout = QVBoxLayout()
        self.tab_area.setLayout(self.vertical_layout)

    def add_checkbox(self, text: str, option: str) -> QCheckBox:
        """Adds the checkbox widget to a tab."""
        checkbox = QCheckBox(text)
        checkbox.setChecked(self.config_manager.get_boolean(self.name, option))
        checkbox.stateChanged.connect(
            lambda: self.config_manager.set(
                self.name, option, str(checkbox.isChecked())
            )
        )
        self.vertical_layout.addWidget(checkbox)
        return checkbox

    def add_spinbox(self, text: str, option: str, min: int, max: int) -> QSpinBox:
        """Adds the spinbox widget to a tab."""
        spinbox = QSpinBox()
        spinbox.setMinimum(min)
        spinbox.setMaximum(max)
        spinbox.setValue(self.config_manager.getint(self.name, option))
        spinbox.valueChanged.connect(
            lambda: self.config_manager.set(self.name, option, str(spinbox.value()))
        )
        self.vertical_layout.addWidget(spinbox)
        return spinbox

    def add_line_edit(self, text: str, option: str) -> QLineEdit:
        """Adds a line edit to the tab."""
        # should have a label to the left of the line edit
        label = QLabel(text)
        line_edit = QLineEdit()
        line_edit.setText(self.config_manager.get(self.name, option))
        line_edit.textChanged.connect(
            lambda: self.config_manager.set(self.name, option, line_edit.text())
        )
        widget_pair = QWidget()
        widget_pair_layout = QHBoxLayout()
        widget_pair.setLayout(widget_pair_layout)
        widget_pair_layout.addWidget(label)
        widget_pair_layout.addWidget(line_edit)
        self.vertical_layout.addWidget(widget_pair)
        return line_edit


class SettingsDialog(QDialog):
    """A dialog that provides changing GameBoa's settings."""

    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 300)
        self.setWindowTitle("Settings")

        self.tab_widget = QTabWidget()

        for section in self.config_manager.sections():
            settings_tab = SettingsTab(self.tab_widget, section)

            for option in self.config_manager.options(section):
                value = self.config_manager.get_value_as_dtype(section, option)
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
