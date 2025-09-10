from resources import resources_rc

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class Notificator:
    @staticmethod
    def show_notification(notify_type="", notify_title="", notify_text=""):
        """Shows a notification message box.

        Args:
            notify_type (str): The type of notification. Can be "info", "warning", or "error".
            notify_title (str): The title of the notification.
            notify_text (str): The main text of the notification.
        """
        if not notify_type:
            return
        
        
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(":/icons/icon.ico")) # Устанавливаем иконку окна
        msg_box.setWindowTitle(notify_title)
        msg_box.setText(notify_text)

        # We display a notification depending on the transferred type of notification
        # Устанавливаем иконку внутри самого сообщения
        if notify_type == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif notify_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif notify_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        else:
            return
        
        msg_box.exec_()