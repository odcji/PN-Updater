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

    def __launch_program(self):
        """Launches the program"""
        program_name = self.model.program_name # Record the program name
        # Create the path to the program's executable file
        program_path = os.path.join(self.model.current_program_path, f"{program_name}.exe")
        
        if not os.path.exists(program_path): # We check the existence of the program
            notification_text = f"Программа {program_name} не найдена.\nПуть: {program_path}" # Notification text
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text) # Show notification
            raise FileNotFoundError(f"Программа не найдена. Путь: {program_path}") 

        try:
            subprocess.Popen([program_path]) # Open the program
        except Exception as e:
            notification_text = f"Ошибка при запуске программы {program_name}.\nОшибка: {e}" # Notification text
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text) # Show notification
            raise IOError(f"Ошибка при запуске программы: {e}")
        
    def __update_label_text(self):
        """Sets the text in QLabel 'Обновление'"""
        text = self.model.program_name # Record the program name
        self.view.set_update_label_text(text=text) # Update the text in QLabel

    def update_program(self):
        """Triggers the program update"""
        self.model.perform_update_in_thread(callback=self.on_update_complited) # Call the program update

    def on_update_complited(self):
        """Handles the completion of the program update"""
        self.view.update_buttons_state(state=True)
        notification_text = "Программа успешно обновлена"
        Notificator.show_notification(notify_type="info", notify_title="Успешно", notify_text=notification_text) # Show notification

    def on_progress_changed(self, value):
        """Handles the change in ProgressBar value"""
        self.view.set_progress_bar_value(value) # Update the value in the progress bar

    def on_process_changed(self, text):
        """Handles the change in QLabel 'Процесс' text"""
        self.view.set_process_text(text) # Update the text in QLabel

    def on_open_button_clicked(self):
        """Handles the 'Открыть' button click"""
        self.__launch_program() # Launch the program

    def on_exit_button_clicked(self):
        """Handles the 'Выход' button click"""
        sys.exit() # Exit the program