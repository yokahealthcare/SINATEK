from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
	def __init__(self, app):
		super().__init__()

		self.app = app

		self.setWindowTitle("POPURI Secret Cashflow")
		self.setWindowIcon(QIcon("marriage_popuri.jpg"))
		self.setGeometry(200, 200, 600, 400)

		
		# menu bar
		menu_bar = self.menuBar()
		file_menu = menu_bar.addMenu("File")
		file_menu.addAction("New Transaction")
		exit_action = file_menu.addAction("Exit")

		exit_action.triggered.connect(self.quitApp)


	def quitApp(self):
		self.app.quit()




