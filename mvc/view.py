class View:
    def __init__(self, ui):
        self.ui = ui

    def set_update_label_text(self, text=""):
        """The function updates the text in Qlabel 'Обновление'"""
        update_text = f"Обновление: {text}" # Create a text
        self.ui.update_label.setText(update_text) # We update the text in Qlabel
        
    def set_process_text(self, text=""):
        """The function updates the text in Qlabel 'Процесс'"""
        process_text = f"Процесс: {text}" # Create a text
        self.ui.process_label.setText(process_text) # We update the text in Qlabel

    def set_progress_bar_value(self, value):
        """The function updates the value of Progressbar """
        self.ui.progressBar.setValue(value) # We update the value of Progressbar

    def update_buttons_state(self, open_btn_state=bool, exit_btn_state=bool):
        """The function updates the state of the 'Открыть' and 'Выход' buttons"""
        self.ui.open_pushButton.setEnabled(open_btn_state)
        self.ui.exit_pushButton.setEnabled(exit_btn_state)

    def open_button_clicked(self, handler):
        """The function causes the click of the 'Открыть' button"""
        self.ui.open_pushButton.clicked.connect(handler) # Connect the click on the button

    def exit_button_clicked(self, handler):
        """The function causes the click of the 'Выход' button"""
        self.ui.exit_pushButton.clicked.connect(handler) # Connect the click on the button