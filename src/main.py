from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from annexe.main_windows import Main
from sys import argv
if __name__ == '__main__':
    app = QApplication(argv)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
    windows = Main('UI/interface.ui')
    app.setStyle('Fusion')
    app.setPalette(palette)
    app.exec()
