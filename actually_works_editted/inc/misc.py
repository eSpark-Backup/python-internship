# JCT Technology Ltd Datalogger 1.0
# by Andrew Keeley (andy@pcman.ca)
# March 2018

# standard / third party libraries
from PyQt5 import QtGui, QtCore, QtWidgets


def yesnobox(win, title, text, info):
	msg = QtWidgets.QMessageBox(win)  											# create a Qt message box
	msg.setIcon(QtWidgets.QMessageBox.Question)  								# with a question icon
	msg.setInformativeText(info)  											# set informative text
	msg.setWindowTitle(title)  												# set the title text
	msg.setText(text)  														# set the question text
	msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)  	# add yes and no buttons
	return msg.exec_() == QtWidgets.QMessageBox.Yes  							# show message box and return True if yes


def messagebox(win, title, text, info):
	msg = QtWidgets.QMessageBox(win)
	msg.setIcon(QtWidgets.QMessageBox.NoIcon)
	msg.setInformativeText(info)  											# set informative text
	msg.setWindowTitle(title)  												# set the title text
	msg.setText(text)  														# set the warning text

	w = msg.fontMetrics().width(info)
	spc = QtWidgets.QSpacerItem(w + 100, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
	lay = msg.layout()
	lay.addItem(spc, lay.rowCount(), 0, 1, lay.columnCount())

	msg.exec_()


def errorbox(win, title, text, info):
	msg = QtWidgets.QMessageBox(win)
	msg.setIcon(QtWidgets.QMessageBox.Critical)
	msg.setInformativeText(info)  											# set informative text
	msg.setWindowTitle(title)  												# set the title text
	msg.setText(text)  														# set the warning text

	w = msg.fontMetrics().width(info)
	spc = QtWidgets.QSpacerItem(w + 100, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
	lay = msg.layout()
	lay.addItem(spc, lay.rowCount(), 0, 1, lay.columnCount())

	msg.exec_()


