# -*- coding: utf-8 -*-

#  Copyright (c) 2021 Francesco Santini <francesco.santini@gmail.com>


from PySide2.QtWidgets import QWidget, QMainWindow, QFileDialog, QLabel, QApplication
from PySide2.QtCore import Slot, Signal
from .dcmMvDialog import Ui_DcmMvDialogUI
from .ThreadHelpers import separate_thread_decorator
from .dcmMvUtils import move_directory
import sys
import os

example_placeholders = [
'%PatientID%', '%PatientName%', '%StudyID%',
'%StudyDate%', '%StudyTime%', '%SeriesID%',
'%SeriesNumber%', '%SeriesName%', '%SeriesDate%',
'%SeriesTime%', '%ScannerName%', '%SequenceName%',
'ProtocolName%', '%InstitutionName%'
]
N_COLUMNS = 3

class DicomMoveWindow(QWidget, Ui_DcmMvDialogUI):
    update_progress = Signal(int, int)
    success = Signal()
    enable_signal = Signal(bool)

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pattern_text.setText(self.pattern_text.text().replace('/', os.path.sep))
        self.update_progress.connect(self.update_progress_bar)
        self.enable_signal.connect(self.enable_buttons)
        self.source_choose_button.clicked.connect(self.choose_src)
        self.destination_choose_button.clicked.connect(self.choose_dest)
        self.move_button.clicked.connect(self.move_clicked)
        self.pattern_text.textChanged.connect(self.execute_conditional_enable)
        self.move_radio.toggled.connect(self.change_button_label)
        col = 0
        row = 0
        for placeholder in example_placeholders:
            self.gridLayout.addWidget(QLabel(placeholder), row, col)
            col += 1
            if col == N_COLUMNS:
                row += 1
                col = 0

    @Slot()
    def change_button_label(self):
        if self.copy_radio.isChecked():
            self.move_button.setText('Copy')
        else:
            self.move_button.setText('Move')

    @Slot()
    def choose_src(self):
        selected_dir = QFileDialog.getExistingDirectory(self, 'Select source folder')
        self.source_location_text.setText(selected_dir.replace('/', os.sep))
        self.execute_conditional_enable()

    @Slot()
    def choose_dest(self):
        selected_dir = QFileDialog.getExistingDirectory(self, 'Select destination folder')
        self.destination_location_text.setText(selected_dir.replace('/', os.sep))
        self.execute_conditional_enable()

    @Slot()
    def execute_conditional_enable(self):
        if self.destination_location_text.text() != '' and \
                self.source_location_text.text() != '' and \
                self.pattern_text.text() != '':
            self.move_button.setEnabled(True)
        else:
            self.move_button.setEnabled(False)

    @Slot(int, int)
    def update_progress_bar(self, current, maximum):
        self.progressBar.setMaximum(maximum)
        self.progressBar.setValue(current)

    @Slot(bool)
    def enable_buttons(self, status):
        self.progressBar.setEnabled(not status)
        self.move_button.setEnabled(status)
        self.source_choose_button.setEnabled(status)
        self.destination_choose_button.setEnabled(status)
        self.pattern_text.setEnabled(status)

    @Slot()
    def move_clicked(self):
        self.enable_buttons(False)
        self.do_move()

    @separate_thread_decorator
    def do_move(self):
        src = self.source_location_text.text()
        dest = self.destination_location_text.text()
        pattern = self.pattern_text.text()
        do_copy = self.copy_radio.isChecked()
        move_directory(src, dest, pattern, do_copy, self.update_progress.emit)
        self.enable_signal.emit(True)


def run_interface():
    app = QApplication(sys.argv)
    window = QMainWindow()
    widget = DicomMoveWindow()
    window.setCentralWidget(widget)
    window.setWindowTitle("Dicom move")
    window.resize(600, widget.sizeHint().height())
    window.show()
    sys.exit(app.exec_())
