import os
import sys
import subprocess

from classes.notifications import Notificator

from PyQt5.QtCore import QTimer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.__update_label_text() # Set the text in QLabel 'Обновление'

        # Buttons
        self.view.open_button_clicked(handler=self.on_open_button_clicked) # 'Открыть' button
        self.view.exit_button_clicked(handler=self.on_exit_button_clicked) # 'Закрыть' button

        # Signals
        self.model.progress_changed.connect(self.on_progress_changed) # Progress bar value change signal
        self.model.process_changed.connect(self.on_process_changed) # QLabel text change signal
        self.model.update_complited.connect(self.on_update_complited) # Update completion signal

    def __launch_program(self):
        """Launches the program"""
        program_name = self.model.program_name # Record the program name
        # Create the path to the program's executable file
        program_path = os.path.join(self.model.current_program_path, f"{program_name}.exe")
        
        if not os.path.exists(program_path): # We check the existence of the program
            notification_text = f"Программа {program_name} не найдена.\nПуть: {program_path}" # Notification text
            # Show notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise FileNotFoundError(f"Программа не найдена. Путь: {program_path}") 

        try:
            subprocess.Popen([program_path]) # Open the program
        except Exception as e:
            notification_text = f"Ошибка при запуске программы {program_name}.\nОшибка: {e}" # Notification text
            # Show notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise IOError(f"Ошибка при запуске программы: {e}")
        
    def __update_label_text(self):
        """Sets the text in QLabel 'Обновление'"""
        text = self.model.program_name # Record the program name
        self.view.set_update_label_text(text=text) # Update the text in QLabel

    def update_program(self):
        """Triggers the program update"""
        self.model.perform_update_in_thread() # Call the program update

    def check_update(self):
        """Функция проверяет необдимость обновления программы"""
        current_program_version = self.model.current_program_version # Get the current program version
        server_program_version = self.model.server_program_version # Get the server program version

        if current_program_version is None:
            notification_text = "Произошла ошибка при получении текущей версии программы"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Произошла ошибка при получении текущей версии программы")

        if server_program_version is None:
            notification_text = "Произошла ошибка при получении версии программы на сервере"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Произошла ошибка при получении версии программы на сервере")

        # We check the versions
        if current_program_version >= server_program_version: # If the current version is greater or the version are equal
            return False
        else:
            return True
        
    def on_update_complited(self, success):
        """Handles the completion of the program update"""
        if success:
            self.view.update_buttons_state(open_btn_state=True, exit_btn_state=True)
            notification_text = "Программа успешно обновлена"
            # Show notification
            Notificator.show_notification(notify_type="info", notify_title="Успешно", notify_text=notification_text)
            
        else:
            self.view.update_buttons_state(open_btn_state=False, exit_btn_state=True)
            notification_text = "Во время обновления произошла ошибка. Проверьте пути и права доступа."
            # Show notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка обновления", notify_text=notification_text)

    def on_progress_changed(self, value):
        """Handles the change in ProgressBar value"""
        self.view.set_progress_bar_value(value) # Update the value in the progress bar
        self.view.set_progress_bar_label_value(value) # Update the value in the progress bar label

    def on_process_changed(self, text):
        """Handles the change in QLabel 'Процесс' text"""
        self.view.set_process_text(text) # Update the text in QLabel

    def on_open_button_clicked(self):
        """Handles the 'Открыть' button click"""
        self.__launch_program() # Launch the program

    def on_exit_button_clicked(self):
        """Handles the 'Выход' button click"""
        sys.exit() # Exit the program