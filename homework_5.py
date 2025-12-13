
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QTableWidget,
    QTableWidgetItem, QAbstractItemView, QMessageBox
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
import sys

class MovieCatalog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catalog")
        self.resize(800, 500)
        self.status = self.statusBar()
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        fields_form = QFormLayout()
        self.title_edit = QLineEdit()
        fields_form.addRow(QLabel("Title:"), self.title_edit)
        self.director_edit = QLineEdit()
        fields_form.addRow(QLabel("Director:"), self.director_edit)
        self.year_edit = QLineEdit()
        self.year_edit.setValidator(QIntValidator(1800, 2100))
        self.year_edit.setPlaceholderText("2020")
        fields_form.addRow(QLabel("Year:"), self.year_edit)
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["Action", "Comedy", "Drama", "Sci-Fi"])
        fields_form.addRow(QLabel("Genre:"), self.genre_combo)
        self.watched_check = QCheckBox("Watched")
        fields_form.addRow(self.watched_check)
        form_layout.addLayout(fields_form)
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_movie)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_form)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addWidget(exit_btn)
        form_layout.addLayout(buttons_layout)
        form_layout.addStretch()
        main_layout.addWidget(form_widget, 1)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Title", "Director", "Year", "Genre", "Watched"]) 
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table, 2)
    def add_movie(self):
        title = self.title_edit.text().strip()
        director = self.director_edit.text().strip()
        year = self.year_edit.text().strip()
        genre = self.genre_combo.currentText()
        watched = "Yes" if self.watched_check.isChecked() else "No"
        if not title or not director:
            self.status.showMessage("Fill the blanks: Title and Director", 3000)
            return
        row = self.table.rowCount()
        self.table.insertRow(row)
        items = [title, director, year, genre, watched]
        for col, text in enumerate(items):
            it = QTableWidgetItem(text)
            it.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, col, it)
        self.status.showMessage("Movie added", 3000)
        self.clear_form()
    def clear_form(self):
        self.title_edit.clear()
        self.director_edit.clear()
        self.year_edit.clear()
        self.genre_combo.setCurrentIndex(0)
        self.watched_check.setChecked(False)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieCatalog()
    win.show()
    sys.exit(app.exec())