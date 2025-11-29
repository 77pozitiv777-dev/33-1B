import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox
)

def calculate_product(data: list[int]) -> int:
    product = 1
    for num in data:
        product *= num
    return product
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Tap the button!')
        self.resize(300, 200)

        self.button = QPushButton('Calculate the product', parent=self)
        self.button.move(85, 75)

        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        nums = [1, 2, 3, 4, 5, 6, 7]
        p = calculate_product(nums)
        self.show_result(p)

    def show_result(self, result: int):
        msg = QMessageBox(self)
        msg.setWindowTitle("Result")
        msg.setText(f"Product of numbers: {result}")
        msg.exec()
def main():
    app =QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
if __name__ == '__main__':
    main()