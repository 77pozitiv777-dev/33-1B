import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простое приложение")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Нажмите 'Показать текст' после ввода.", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Введите текст здесь...")

        self.show_button = QPushButton("Показать текст", self)

        self.close_button = QPushButton("Закрыть приложение", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.show_button)
        vbox.addWidget(self.close_button)

        self.setLayout(vbox)

        self.show_button.clicked.connect(self.update_label)
        self.close_button.clicked.connect(self.close)

    def update_label(self):
        text = self.line_edit.text()
        if text:
            self.label.setText(f"Введённый текст:\n{text}")
        else:
            self.label.setText("Пожалуйста, введите текст.")

def main():
    app = QApplication(sys.argv)
    ex = SimpleApp()
    ex.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()