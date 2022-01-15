"""
Créée des boites de dialogues d'avertissement personnalisé
et permet aussi de lancer une QFileDialog
"""
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QFileDialog


class Dialog(QMessageBox):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(message)
        self.setWindowTitle("Avertissement")
        self.setWindowIcon(QIcon("../icons/20211206_222718_0000.png"))
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()


class File(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
