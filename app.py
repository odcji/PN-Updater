import sys

from ui.app_ui import Ui_MainWindow

from mvc.model import Model
from mvc.view import View
from mvc.controller import Controller

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Install the base size of the window programmatically
        self.resize(self.minimumSizeHint())

        # MVC Initialization
        self.model = Model()
        self.view = View(ui=self.ui)
        self.controller = Controller(model=self.model, view=self.view)


if __name__ == "__main__":
    # Turn on Hight-DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())