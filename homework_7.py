import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from db_7 import Database


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To Do List")
        self.resize(500, 400)

        self.db = Database()

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter the task's text:")
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add_task)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.btn_add)
        layout.addLayout(input_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Task", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.table.itemChanged.connect(self.update_task_status)

        layout.addWidget(self.table)

        self.btn_delete = QPushButton("Delete chosen")
        self.btn_delete.clicked.connect(self.delete_task)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

    def load_tasks(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        tasks = self.db.get_all_tasks()

        for row_idx, task_data in enumerate(tasks):
            task_id, title, is_done = task_data 

            self.table.insertRow(row_idx)

            title_item = QTableWidgetItem(str(title))
            title_item.setData(Qt.ItemDataRole.UserRole, task_id)
            title_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table.setItem(row_idx, 0, title_item)

            status_item = QTableWidgetItem()
            if is_done == 1:
                status_item.setCheckState(Qt.CheckState.Checked)
                status_item.setText("Completed")
            else:
                status_item.setCheckState(Qt.CheckState.Unchecked)
                status_item.setText("Not completed")
            self.table.setItem(row_idx, 1, status_item)

        self.table.blockSignals(False)

    def add_task(self):
        text = self.input_field.text().strip()
        if text:
            self.db.add_task(text)
            self.input_field.clear()
            self.load_tasks()

    def update_task_status(self, item):
        if item.column() == 1:
            row = item.row()
            title_item = self.table.item(row, 0)
            task_id = title_item.data(Qt.ItemDataRole.UserRole)
            
            is_done = 1 if item.checkState() == Qt.CheckState.Checked else 0
            
            item.setText("Completed" if is_done else "Not completed")
            
            self.db.update_status(task_id, is_done)

    def delete_task(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            title_item = self.table.item(current_row, 0)
            task_id = title_item.data(Qt.ItemDataRole.UserRole)

            self.db.delete_task(task_id)
            self.load_tasks()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec())