from time import sleep

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QProgressDialog, QMessageBox, QDialog

from gui.file_transfer import Ui_FileTransferDialog
from src.file_transfer import FileTransfer


class FileTransferDialog(QDialog, Ui_FileTransferDialog):
    _update_signal = pyqtSignal()

    UPLOAD = 0
    DOWNLOAD = 1

    def __init__(self, type):
        super(FileTransferDialog, self).__init__()
        self.setupUi(self)
        self.setModal(True)

        if type == FileTransferDialog.UPLOAD:
            self.label.setText("Saving file.")
            self.progressBar.setRange(0, 100)
        elif type == FileTransferDialog.DOWNLOAD:
            self.label.setText("Reading file.")
            self.progressBar.setRange(0, 0)

        self.progressBar.setValue(0)
        self._update_signal.connect(self._update_progress)
        self._transfer = FileTransfer(lambda: self._update_signal.emit())

    def _update_progress(self):
        if self._transfer.error:
            QMessageBox.critical(self, "Error", "File transfer failed.")
            self.reject()
        elif self._transfer.finished:
            sleep(0.5)
            self.accept()
        else:
            self.progressBar.setValue(self._transfer.progress * 100)

    @property
    def transfer(self):
        return self._transfer
