import os
import sys
import yaml
import shutil
import threading

from classes.notifications import Notificator

from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    progress_changed = pyqtSignal(int) # Progress bar value change signal
    process_changed = pyqtSignal(str) # QLabel 'Процесс' text change signal
    update_complited = pyqtSignal(bool) # Update completion signal


    def __init__(self):
        super().__init__()

        self.current_program_path = self.__get_base_path() # Get the current program path
        self.config_data = self.__get_config_data() # Get data from the configuration file
        self.server_program_path = self.__get_server_program_path() # Get the path to the program on the server
        self.program_name = self.__get_program_name() # Get the program name
        self.current_program_version = self.__get_current_program_version() # Get the current program version
        self.server_program_version = self.__get_server_program_version() # Get the server program version

    def __get_config_data(self):
        """The function returns data from the configuration file"""
        config_file_path = os.path.join(self.current_program_path, "config.yaml") # The Way to the Config file

        if not os.path.exists(config_file_path): # ПRover the existence of a configuration file
            notification_text = f"Файл конфигурации не найден.\nПуть: {config_file_path}" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise FileNotFoundError(f"Файл конфигурации не найден. Путь: {config_file_path}")

        try:
            with open(config_file_path, "r") as config_file: # Open the configuration file
                config_data = yaml.safe_load(config_file) # We download the data from the configuration file
        except Exception as e:
            notification_text = f"Ошибка при чтении файла конфигурации.\nОшибка: {e}" # Notification text"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise IOError(f"Ошибка при чтении файла конфигурации: {e}")
        
        return config_data
    
    def __get_base_path(self):
        """Returns the path to the executable file or script"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable) # Path for a compiled .exe file
        else:
            # Path for a regular .py script (project root)
            return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    def __get_server_program_path(self):
        """Returns the path to the program on the server"""
        if self.config_data is None: # Check that configuration data is loaded
            notification_text = "Данные конфигурации не загружены" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Данные конфигурации не загружены")
        
        server_program_path = self.config_data.get("server_program_path") # Get the path to the program on the server

        if server_program_path is None: # Check that the path to the program on the server is set
            notification_text = "Путь к программе на сервере не указан в файле конфигурации" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Путь к программе на сервере не указан в файле конфигурации")
        else:
            return server_program_path
        
    def __get_program_name(self):
        """Returns the program name"""
        if self.config_data is None: # Check that configuration data is loaded
            notification_text = "Данные файла конфигурации не загружены" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Данные файла конфигурации не загружены")
        
        program_name = self.config_data.get("program_name") # Get the program name

        if program_name is None: # Check that the program name is set
            notification_text = "Имя программы не указано в файле конфигурации" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Имя программы не указано в файле конфигурации")
        else:
            return program_name
        
    def __get_current_program_version(self):
        """Returns the current program version"""
        if self.config_data is None: # Check that configuration data is loaded
            notification_text = "Данные файла конфигурации не загружены" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Данные файла конфигурации не загружены")
        
        current_program_version = self.config_data.get("program_version_number") # Get the current program version

        if current_program_version is None: # Check that the program name is set
            notification_text = "Имя программы не указано в файле конфигурации" # Notification text
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Имя программы не указано в файле конфигурации")
        else:
            return current_program_version
        
    def __get_server_program_version(self):
        """Returns the server program version"""
        server_config_file_path = os.path.join(self.server_program_path, "config.yaml") # The path to the config file

        if not os.path.exists(server_config_file_path): # Check the existence of the config file
            notification_text = f"Файл конфигурации на сервере не найден.\nПуть: {server_config_file_path}"
            
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError(f"Файл конфигурации на сервере не найден.\nПуть: {server_config_file_path}")
        
        try:
            with open(server_config_file_path, "r") as server_config_file: # Open the config file
                server_config_data = yaml.safe_load(server_config_file) # We download the data from the config file

        except Exception as e:
            notification_text = f"Ошибка при чтении файла конфигурации на сервере.\nОшибка: {e}"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError(f"Ошибка при чтении файла конфигурации на сервере.\nОшибка: {e}")
        
        return server_config_data.get("program_version_number") # Get the server program version
        
    def __perform_update(self):
        """Updates the program"""
        # Check that the current program path is set
        if not self.current_program_path or self.current_program_path is None:
            notification_text = "Текущий путь программы не установлен"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Текущий путь программы не установлен")
        
        # Check that the path to the program on the server is set
        if not self.server_program_path or self.server_program_path is None:
            notification_text = "Путь к программе на сервере не установлен"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise ValueError("Путь к программе на сервере не установлен")
        
        if not os.path.exists(self.current_program_path): # We check the existence of the current path to the program
            notification_text = f"Текущий путь к программе не найден.\nПуть: {self.current_program_path}"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise FileNotFoundError(f"Текущий путь к программе не найден. Путь: {self.current_program_path}")
        
        if not os.path.exists(self.server_program_path): # Check the existence of the path to the program on the server
            notification_text = f"Путь к прогамме на сервере не найден.\nПуть: {self.server_program_path}"
            # We display a notification
            Notificator.show_notification(notify_type="error", notify_title="Ошибка", notify_text=notification_text)
            raise FileNotFoundError(f"Путь к прогамме на сервере не найден. Путь: {self.server_program_path}")
        
        try:
            # Get the list of files in the current program path
            current_program_files = os.listdir(self.current_program_path)
            server_program_files = os.listdir(self.server_program_path) # Get the list of files in the program path on the server

            total_files = len(current_program_files) + len(server_program_files) # Total number of files
            files_processed = 0 # Number of processed files

            if total_files == 0: # If the number of files is 0, exit
                return

            # Delete old program files
            for file in current_program_files:

                if file == 'updater.exe': # Check that the file is not updater.exe
                    continue
                
                file_path = os.path.join(self.current_program_path, file)
                if os.path.isfile(file_path): # Check if it's a file
                    os.remove(file_path) # Delete the file

                elif os.path.isdir(file_path): # Check if it's a directory
                    shutil.rmtree(file_path) # Delete the directory

                files_processed += 1
                progress = int((files_processed / total_files) * 100)
                self.progress_changed.emit(progress) # Progress bar value change signal

                self.process_changed.emit(f"удаление файла - {file}") # Update text in QLabel 'Процесс'

            # Copy new program files
            if server_program_files: # Check if there are files in the program path on the server
                for file in server_program_files:
                    if file == 'updater.exe': # Check that the file is not updater.exe
                        continue

                    source_path = os.path.join(self.server_program_path, file)
                    destination_path = os.path.join(self.current_program_path, file)
                    
                    if os.path.isfile(source_path): # Check if it's a file
                        shutil.copy2(source_path, destination_path) # Copy the file

                    elif os.path.isdir(source_path): # Check if it's a directory
                        shutil.copytree(source_path, destination_path, dirs_exist_ok=True) # Copy the directory

                    files_processed += 1
                    progress = int((files_processed / total_files) * 100)
                    self.progress_changed.emit(progress) # A signal for changing the value of the progress bar
                    
                    self.process_changed.emit(f"копирование файла - {file}") # We update the text in QLabel 'Процесс'

            self.progress_changed.emit(100) # Fully fill the progress bar
            self.process_changed.emit("Программа успешно обновлена") # Update text in QLabel 'Процесс'

            self.update_complited.emit(True) # Update completion signal

        except Exception as e:
            self.update_complited.emit(False) # Update completion signal
        
    def perform_update_in_thread(self):
        """Launches the program update in a separate thread"""
        thread = threading.Thread(target=self.__perform_update) # Create a thread
        thread.daemon = True
        thread.start()
        return thread