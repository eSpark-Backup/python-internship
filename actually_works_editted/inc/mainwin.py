# JCT Technology Ltd Datalogger 1.0
# by Andrew Keeley (andy@pcman.ca)
# March 2018

# standard / third party libraries
from PyQt5 import  QtCore
from PyQt5.QtWidgets import QMainWindow
import time
import sys


class MainWindow(QMainWindow):
	resized = QtCore.pyqtSignal()

	def __init__(self, app):
		super(MainWindow, self).__init__()
		self.app = app

	def resizeEvent(self, event):
		self.resized.emit()

	def reset(self):
		self.close()
		time.sleep(0.25)
		self.app.exit(-1)