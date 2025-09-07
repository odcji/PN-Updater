import os
import sys
import yaml
import shutil
import threading

from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    progress_changed = pyqtSignal(int) # Progress bar value change signal
    process_changed = pyqtSignal(str) # QLabel 'Процесс' text change signal

    def __init__(self):
        super().__init__()

        self.current_program_path = self.__get_base_path() # Get the current program path
        self.config_data = self.__get_config_data() # Get data from the configuration file
        self.server_program_path = self.__get_server_program_path() # Get the path to the program on the server
        self.program_name = self.__get_program_name() # Get the program name

    def __get_config_data(self):
        """Функция возвращает данные из файла конфигурации"""
        config_file_path = os.path.join(self.current_program_path, "config.yaml") # Путь к файлу конфигу

        if not os.path.exists(config_file_path): # Проверяем существование файла конфигурации
            raise FileNotFoundError(f"Файл конфигурации не найден. Путь: {config_file_path}")

        try:
            with open(config_file_path, "r") as config_file: # Открываем файл конфигурации
                config_data = yaml.safe_load(config_file) # Загружаем данные из файла конфигурации
        except Exception as e:
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
            raise ValueError("Configuration data not loaded")
        
        server_program_path = self.config_data.get("server_program_path") # Get the path to the program on the server

        if server_program_path is None: # Check that the path to the program on the server is set
            raise ValueError("Path to program on server not specified in configuration file")
        else:
            return server_program_path
        
    def __get_program_name(self):
        """Returns the program name"""
        if self.config_data is None: # Check that configuration data is loaded
            raise ValueError("Configuration data not loaded")
        
        program_name = self.config_data.get("program_name") # Get the program name

        if program_name is None: # Check that the program name is set
            raise ValueError("Program name not specified in configuration file")
        else:
            return program_name
        
    def __perform_update(self, callback):
        """Updates the program"""
        # Check that the current program path is set
        if not self.current_program_path or self.current_program_path is None:
            raise ValueError("Current program path not set")
        
        # Check that the path to the program on the server is set
        if not self.server_program_path or self.server_program_path is None:
            raise ValueError("Path to program on server not set")
        
        if not os.path.exists(self.current_program_path): # Проверяем существование текущего пути к программе
            raise FileNotFoundError(f"Текущий путь к программе не найден. Путь: {self.current_program_path}")
        
        if not os.path.exists(self.server_program_path): # Проверяем существование пути к прогамме на сервере
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

                self.process_changed.emit(f"deleting file - {file}") # Update text in QLabel 'Процесс'

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
                    self.progress_changed.emit(progress) # Сигнал изменения значения прогресс бара
                    
                    self.process_changed.emit(f"копирование файла - {file}") # Обновляем текст в QLabel 'Процесс'

            self.progress_changed.emit(100) # Fully fill the progress bar
            self.process_changed.emit("Program successfully updated") # Update text in QLabel 'Процесс'

            callback() # Call the update completion function

        except Exception as e:
            raise IOError(f"An error occurred during program update. Error: {e}") 
        
    def perform_update_in_thread(self, callback):
        """Launches the program update in a separate thread"""
        thread = threading.Thread(target=self.__perform_update, args=(callback,)) # Create a thread
        thread.daemon = True
        thread.start()
        return thread