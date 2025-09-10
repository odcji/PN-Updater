class View:
    def __init__(self, ui):
        """Initializes the View.

        Args:
            ui: The UI object.
        """
        self.ui = ui

    def set_update_label_text(self, text=""):
        """Sets the text of the 'Обновление' label.

        Args:
            text (str): The text to display. Defaults to "".
        """
        update_text = f"Обновление: {text}"  # Create a text
        self.ui.update_label.setText(update_text)  # We update the text in Qlabel

    def set_process_text(self, text=""):
        """Sets the text of the 'Процесс' label.

        Args:
            text (str): The text to display. Defaults to "".
        """
        process_text = f"Процесс: {text}"  # Create a text
        self.ui.process_label.setText(process_text)  # We update the text in Qlabel

    def set_progress_bar_value(self, value):
        """Sets the value of the progress bar.

        Args:
            value (int): The progress value.
        """
        self.ui.progressBar.setValue(value)  # We update the value of Progressbar

    def set_progress_bar_label_value(self, value):
        """Sets the text of the progress bar's label.

        Args:
            value (int): The value to display.
        """
        progress_text = f"{value}%"  # Create a text
        self.ui.progressBar_label.setText(progress_text)  # We update the text in Qlabel

    def update_buttons_state(self, open_btn_state=bool, exit_btn_state=bool):
        """Updates the enabled state of the 'Открыть' and 'Выход' buttons.

        Args:
            open_btn_state (bool): The enabled state of the 'Открыть' button.
            exit_btn_state (bool): The enabled state of the 'Выход' button.
        """
        self.ui.open_pushButton.setEnabled(open_btn_state)
        self.ui.exit_pushButton.setEnabled(exit_btn_state)

    def open_button_clicked(self, handler):
        """Connects a handler to the 'Открыть' button's clicked signal.

        Args:
            handler: The function to call when the button is clicked.
        """
        self.ui.open_pushButton.clicked.connect(handler)  # Connect the click on the button

    def exit_button_clicked(self, handler):
        """Connects a handler to the 'Выход' button's clicked signal.
        
        Args:
            handler: The function to call when the button is clicked.
        """
        self.ui.exit_pushButton.clicked.connect(handler)  # Connect the click on the button