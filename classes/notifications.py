from PyQt5.QtWidgets import QMessageBox

class Notificator:
    def show_notification(notify_type="", notify_title="", notify_text=""):
        """Function for showing notifications"""
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