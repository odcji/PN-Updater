import sys

from ui.app_ui import Ui_MainWindow

from mvc.model import Model
from mvc.view import View
from mvc.controller import Controller

from classes.notifications import Notificator

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from resources import resources_rc


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window icon
        icon = QIcon(":/icons/icon.ico")
        self.setWindowIcon(icon)

        # Install the base size of the window programmatically
        self.resize(self.minimumSizeHint())

        # MVC Initialization
        self.model = Model()
        self.view = View(ui=self.ui)
        self.controller = Controller(model=self.model, view=self.view)

        # We check the need to update
        self.is_update_available = self.controller.check_update() # Check for an update
        if self.is_update_available:
            QTimer.singleShot(0, self.controller.update_program) # We call the program output
        else:
            Notificator.show_notification(notify_type="info", notify_title="Обновление", notify_text="Обновление не требуется")
            self.view.update_buttons_state(open_btn_state=True, exit_btn_state=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Fonts for the application
    default_font = QFont()
    default_font.setFamilies(["Segoe UI", "Inter", "Arial", "Noto Sans", "sans-serif"])

    app.setFont(default_font) # We set the default font for the entire application

    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
