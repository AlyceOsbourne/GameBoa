from PySide6.QtWidgets import QApplication

from project.src import MainWindow, system


def run():
    q_app = QApplication()
    main_window = MainWindow()
    main_window.show()
    q_app.exec_()


if __name__ == "__main__":
    run()