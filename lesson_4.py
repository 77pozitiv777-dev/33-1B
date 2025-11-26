import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QLabel, QPushButton, QVBoxLayout
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Счетчик кликов")
        self.resize(270, 70)

        layout = QVBoxLayout()
        layout.addLayout(self.count_clicks())
        self.setLayout(layout)

    def count_clicks(self):
        layout = QVBoxLayout()
        self.count = 0
        self.counter_label = QLabel("Количество кликов: 0")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        btn = QPushButton("Нажми меня")
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn); layout.addWidget(self.counter_label)
        return layout

    def on_click(self, checked=False):
        self.count += 1
        self.counter_label.setText(f"Количество кликов: {self.count}")

def main():
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()