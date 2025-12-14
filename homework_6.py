import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem, QAbstractItemView
)

class Library(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My library")
        self.resize(800, 500)

        self.statusBar().showMessage("App is ready to work")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()

        left_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        left_layout.addWidget(self.title_input)

        left_layout.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        left_layout.addWidget(self.author_input)

        left_layout.addWidget(QLabel("Year:"))
        self.year_input = QLineEdit()
        left_layout.addWidget(self.year_input)

        left_layout.addWidget(QLabel("Genre:"))
        self.genre_input = QComboBox()
        self.genre_input.addItems(["Romance", "Detective", "Sci-Fi", "Scientific", "Classic"])
        left_layout.addWidget(self.genre_input)

        self.read_check = QCheckBox("Read")
        left_layout.addWidget(self.read_check)

        left_layout.addStretch()

        buttons_layout = QVBoxLayout()

        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add_book)
        buttons_layout.addWidget(self.btn_add)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.btn_clear)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.close)
        buttons_layout.addWidget(self.btn_exit)

        left_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["TItle", "Author", "Year", "Genre", "Read"])
        
        self.table.setSortingEnabled(True)
        
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addWidget(self.table, stretch=3)

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        genre = self.genre_input.currentText()
        is_read = "Yes" if self.read_check.isChecked() else "No"

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        self.table.setItem(row_count, 0, QTableWidgetItem(title))
        self.table.setItem(row_count, 1, QTableWidgetItem(author))
        self.table.setItem(row_count, 2, QTableWidgetItem(year))
        self.table.setItem(row_count, 3, QTableWidgetItem(genre))
        self.table.setItem(row_count, 4, QTableWidgetItem(is_read))

        self.statusBar().showMessage(f"Book '{title}' added.")

    def clear_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.genre_input.setCurrentIndex(0)
        self.read_check.setChecked(False)
        self.statusBar().showMessage("Form is cleared.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Library()
    window.show()
    sys.exit(app.exec())