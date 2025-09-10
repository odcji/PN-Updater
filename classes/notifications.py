from PyQt5.QtWidgets import QMessageBox

class Notificator:
    def show_notification(notify_type="", notify_title="", notify_text=""):
        """Shows a notification message box.

        Args:
            notify_type (str): The type of notification. Can be "info", "warning", or "error".
            notify_title (str): The title of the notification.
            notify_text (str): The main text of the notification.
        """
        if not notify_type:
            return
        
        # We display a notification depending on the transferred type of notification
        if notify_type == "info":
            QMessageBox.information(None, notify_title, notify_text) # Information
        elif notify_type == "warning":
            QMessageBox.warning(None, notify_title, notify_text) # Warning
        elif notify_type == "error":
            QMessageBox.critical(None, notify_title, notify_text) # Error
        else:
            return