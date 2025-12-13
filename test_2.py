import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QPushButton, QProgressBar, QMessageBox
)

from PyQt6.QtCore import QTimer, Qt, QTime
class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        
        self.work_duration = 25
        self.break_duration = 5
        self.total_cycles = 4

        self.timer = QTimer()   
        self.timer.timeout.connect(self.update_timer)
        self.current_cycle = 0
        self.is_working = True
        self.is_running = False
        self.is_paused = False
        self.time_left = 0
        self.total_interval_time = 0

        self.init_ui()
    def init_ui(self):

        main_layout = QVBoxLayout()
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Work time (min)):"))
        self.work_spinbox = QSpinBox()
        self.work_spinbox.setRange(1, 180)
        self.work_spinbox.setValue(self.work_duration)
        settings_layout.addWidget(self.work_spinbox)
        settings_layout.addWidget(QLabel("Braek time (min):"))
        self.break_spinbox = QSpinBox()
        self.break_spinbox.setRange(1, 60)
        self.break_spinbox.setValue(self.break_duration)
        settings_layout.addWidget(self.break_spinbox)
        settings_layout.addWidget(QLabel("Cycles:"))
        self.cycles_spinbox = QSpinBox()
        self.cycles_spinbox.setRange(1, 20)
        self.cycles_spinbox.setValue(self.total_cycles)
        settings_layout.addWidget(self.cycles_spinbox)
        main_layout.addLayout(settings_layout)

        self.status_label = QLabel("Setting")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label = QLabel("00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.time_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_continue_timer)
        self.pause_button.setEnabled(False)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setEnabled(False)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.reset_button)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)
        self.set_display_for_new_interval()

    def start_timer(self):
        self.work_duration = self.work_spinbox.value()
        self.break_duration = self.break_spinbox.value()
        self.total_cycles = self.cycles_spinbox.value()
        
        if self.work_duration <= 0 or self.break_duration <= 0 or self.total_cycles <= 0:
            QMessageBox.critical(self, "Input error", "All values (work, break, cycles) must be greater than zero.")
            return
        if not self.is_running:

            self.current_cycle = 1
            self.is_working = True
            self.set_display_for_new_interval()
        
        self.is_running = True
        self.is_paused = False
        self.timer.start(1000)

        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.pause_button.setText("Pause")
        self.reset_button.setEnabled(True)
        self.set_settings_enabled(False)

    def pause_continue_timer(self):
        if not self.is_running:
            return

        if self.is_paused:
            self.is_paused = False
            self.timer.start(1000)
            self.pause_button.setText("Pause")
        else:
            self.is_paused = True
            self.timer.stop()
            self.pause_button.setText("Continue")

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self.current_cycle = 0
        self.is_working = True
        
        self.time_left = self.work_spinbox.value() * 60
        self.total_interval_time = self.time_left
        
        self.status_label.setText("Setting")
        self.update_time_display()
        self.progress_bar.setValue(0)
        
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.reset_button.setEnabled(False)
        self.set_settings_enabled(True)
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_time_display()
            self.update_progress_bar()
        else:
            self.timer.stop()
            self.next_interval()

    def update_time_display(self):
        time = QTime(0, 0)
        time = time.addSecs(self.time_left)
        self.time_label.setText(time.toString("mm:ss"))

    def update_progress_bar(self):
        if self.total_interval_time > 0:
            progress = int((1 - self.time_left / self.total_interval_time) * 100)
            self.progress_bar.setValue(progress)

    def set_display_for_new_interval(self):
        if self.is_working:
            duration_minutes = self.work_duration
            status_text = f"WORK (Cycle {self.current_cycle}/{self.total_cycles})"
        else:
            duration_minutes = self.break_duration
            status_text = f"BREAK (Cycle {self.current_cycle}/{self.total_cycles})"
            
        self.time_left = duration_minutes * 60
        self.total_interval_time = self.time_left
        
        self.status_label.setText(status_text)
        
        self.update_time_display()
        self.progress_bar.setValue(0)

    def next_interval(self):
        
        if self.is_working:
            self.is_working = False
            self.set_display_for_new_interval()
            self.timer.start(1000)
        else:
            self.current_cycle += 1
            
            if self.current_cycle <= self.total_cycles:
                self.is_working = True
                self.set_display_for_new_interval()
                self.timer.start(1000)
            else:
                self.finish_all_cycles()

    def finish_all_cycles(self):
        self.is_running = False
        self.is_paused = False
        
        self.status_label.setText("COMPLETED!")
        self.time_label.setText("00:00")
        self.progress_bar.setValue(100)
        
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        self.set_settings_enabled(True)
        
        QMessageBox.information(self, "Completing", "All planned cycles of work and breaks are completed! \nGreat Work!")

    def set_settings_enabled(self, enabled):
        self.work_spinbox.setEnabled(enabled)
        self.break_spinbox.setEnabled(enabled)
        self.cycles_spinbox.setEnabled(enabled)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PomodoroTimer()
    ex.show()
    sys.exit(app.exec())