from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from windows import MainWindow
import sys

app = QApplication(sys.argv)

wd = MainWindow(app)
wd.show()

# start the program event loop
sys.exit(app.exec())










"""
# Find the width and height of the screen
sc_geometry = app.primaryScreen().geometry()
sc_width = sc_geometry.width()
sc_height = sc_geometry.height()

print("Width : {}".format(sc_width))
print("height : {}".format(sc_height))
"""