import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class CurrencyConverterApp(QWidget):
    RATES = {
        'USD': 1.0,
        'EUR': 0.93,
        'KGS': 88.0
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        main_vbox = QVBoxLayout()
        main_vbox.setSpacing(15)

        header_label = QLabel("Введите сумму и выберите валюты для конвертации:")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_vbox.addWidget(header_label)

        amount_hbox = QHBoxLayout()
        
        amount_label = QLabel("Введите сумму:")
        amount_label.setFixedWidth(120)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        
        validator = QDoubleValidator(0.01, 1000000000.00, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.amount_input.setValidator(validator)
        
        amount_hbox.addWidget(amount_label)
        amount_hbox.addWidget(self.amount_input)
        main_vbox.addLayout(amount_hbox)
        
        currencies = list(self.RATES.keys())
        
        currency_hbox = QHBoxLayout()
        
        from_label = QLabel("Из валюты:")
        from_label.setFixedWidth(120)
        self.from_combo = QComboBox()
        self.from_combo.addItems(currencies)
        self.from_combo.setCurrentText('USD')

        to_label = QLabel("В валюту:")
        to_label.setFixedWidth(80)
        self.to_combo = QComboBox()
        self.to_combo.addItems(currencies)
        self.to_combo.setCurrentText('KGS')

        currency_hbox.addWidget(from_label)
        currency_hbox.addWidget(self.from_combo)
        currency_hbox.addWidget(to_label)
        currency_hbox.addWidget(QLabel("→"))
        currency_hbox.addWidget(self.to_combo)
        
        main_vbox.addLayout(currency_hbox)
        
        button_hbox = QHBoxLayout()
        
        self.convert_button = QPushButton("Конвертировать")
        
        self.clear_button = QPushButton("Очистить")

        button_hbox.addWidget(self.convert_button)
        button_hbox.addWidget(self.clear_button)
        main_vbox.addLayout(button_hbox)

        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        result_vbox = QVBoxLayout(result_frame)
        
        result_header = QLabel("Результат конвертации:")
        
        self.result_label = QLabel("0.00")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        result_vbox.addWidget(result_header)
        result_vbox.addWidget(self.result_label)
        
        main_vbox.addWidget(result_frame)

        self.setLayout(main_vbox)

        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_fields)

    def convert_currency(self):
        try:
            amount_str = self.amount_input.text().replace(',', '.')
            amount = float(amount_str)
            
            if amount <= 0:
                self.show_error("Ошибка ввода", "Сумма должна быть положительным числом.")
                return

        except ValueError:
            self.show_error("Ошибка ввода", "Пожалуйста, введите корректное числовое значение в поле суммы.")
            return

        from_currency = self.from_combo.currentText()
        to_currency = self.to_combo.currentText()

        rate_from = self.RATES.get(from_currency)
        rate_to = self.RATES.get(to_currency)

        conversion_rate = rate_to / rate_from
        
        result = amount * conversion_rate
        
        formatted_result = f"{result:,.2f} {to_currency}"
        self.result_label.setText(formatted_result)

    def clear_fields(self):
        self.amount_input.clear()
        self.result_label.setText("0.00")

    def show_error(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.exec()

def main():
    app = QApplication(sys.argv)
    ex = CurrencyConverterApp()
    ex.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()