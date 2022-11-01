# import so we can increment numbers, take strings as input etc etc
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QLineEdit,
    QLabel,
)

from project.src.system import (
    get_value,
    set_value,
    sections,
    section_options,
    option_type,
    save_config,
    load_config,
    bus
)


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
        checkbox.setChecked(get_value(self.name, option))
        checkbox.stateChanged.connect(lambda: set_value(self.name, option, checkbox.isChecked()))
        self.layout.addWidget(checkbox)
        return checkbox

    def add_spinbox(self, text: str, option: str, min: int, max: int) -> QSpinBox:
        """Adds a spinbox to the tab."""
        spinbox = QSpinBox()
        spinbox.setMinimum(min)
        spinbox.setMaximum(max)
        spinbox.setValue(get_value(self.name, option))
        spinbox.valueChanged.connect(lambda: set_value(self.name, option, spinbox.value()))
        self.layout.addWidget(spinbox)
        return spinbox

    def add_line_edit(self, text: str, option: str) -> QLineEdit:
        """Adds a line edit to the tab."""
        # should have a label to the left of the line edit
        label = QLabel(text)
        line_edit = QLineEdit()
        line_edit.setText(get_value(self.name, option))
        line_edit.textChanged.connect(lambda: set_value(self.name, option, line_edit.text()))
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
        sects = sections()
        for section in sects:
            settings_tab = SettingsTab(self.tab_widget, section)
            for option in section_options(section):
                if option_type(section, option) == bool:
                    settings_tab.add_checkbox(option, option)
                elif option_type(section, option) == int:
                    settings_tab.add_spinbox(option, option, 0, 100)
                elif option_type(section, option) == str:
                    settings_tab.add_line_edit(option, option)
                else:
                    raise TypeError(f"Unknown option type {option_type(section, option)}")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(
            lambda: save_config() or bus.broadcast(bus.SystemEvents.SettingsUpdated) or self.accept()
        )
        self.button_box.rejected.connect(lambda: load_config() or self.reject())

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
