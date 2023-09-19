#!/usr/bin/env python

# JCT Technology Ltd Datalogger 1.0
# by Andrew Keeley (andy@pcman.ca)
# March 2018

# standard / third party libraries
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph
import time
import gc

# project libraries
from config import *
from inc.logger import Logger
from inc.circbuff import CircularBuffer
from inc.modbusrx import ModBusRX
from inc.mainui import MainUI
from inc.mainwin import MainWindow
from inc.persist import Persist
from inc.recorder import Recorder


def prepareregisters():
    validtypes = ['U2', 'I2', 'U4', 'I4', 'F']
    wordtypes = ['U2', 'I2']

    regmap = [[]]
    inpmin = []
    inpmax = []
    hldmin = []
    hldmax = []

    # MODBUS_REGISTERS = [
    # 	("Channel 1", 40001, "I2", 2, 1),
    # 	("Channel 2", 40002, "I2", 2, 1),
    # 	("Channel 3", 40003, "I2", 2, 1),
    # 	("Channel 4", 40004, "I2", 2, 1),
    # 	("Channel 5", 40005, "I2", 2, 1),
    # 	("Channel 6", 40006, "I2", 2, 1)
    # ]

    for s in SERVERS:
        inpmin.append(0)
        inpmax.append(0)
        hldmin.append(0)
        hldmax.append(0)

    for r in MODBUS_REGISTERS:
        if len(r) == 3:
            r += (0, 1)  # append decimals and server if not present
        elif len(r) == 4:
            r += (1,)  # append server if not present
        if r[2] in validtypes:
            if 1 <= r[4] <= len(SERVERS):
                s = r[4] - 1
                if 30001 <= r[1] <= 39999:
                    regmap[0].append(r)
                    inpmin[s] = r[1] if inpmin[s] == 0 else min(inpmin[s], r[1])
                    inpmax[s] = max(inpmax[s], r[1] + (0 if r[2] in wordtypes else 1))
                elif 40001 <= r[1] <= 49999:
                    regmap[0].append(r)
                    hldmin[s] = r[1] if hldmin[s] == 0 else min(hldmin[s], r[1])
                    hldmax[s] = max(hldmax[s], r[1] + (0 if r[2] in wordtypes else 1))
    for i, _ in enumerate(SERVERS):
        regmap += [[inpmin[i], inpmax[i], hldmin[i], hldmax[i]]]
    # for i in range(len(regmap)):
    # 	print regmap[i]
    return regmap


if __name__ == "__main__":
    pyqtgraph.setConfigOptions(antialias=True)

    app = QtWidgets.QApplication(sys.argv)  # instantiate a QT app

    splashpm = QtGui.QPixmap(":/images/logo.png")
    splash = QtWidgets.QSplashScreen(splashpm, QtCore.Qt.WindowStaysOnTopHint)

    while True:
        splash.show()
        app.processEvents()
        registermap = prepareregisters()
        # print(registermap)

        win = MainWindow(app)  # instantiate a QMainWindow subclass
        ui = MainUI(win, registermap[0])  # instantiate the ui
        appname = str(win.windowTitle())
        history = CircularBuffer(registermap[0])  # array for register history
        recorder = Recorder(ui, registermap[0])
        persist = Persist(ui, appname)
        modbus = ModBusRX(registermap)
        logger = Logger(registermap[0], win, ui, history, recorder, persist, modbus)  # create the logger thread

        persist.connect()

        time.sleep(1)
        win.show()  # display the window
        splash.finish(win)

        # pyqtgraph bug workaround
        g = win.geometry()
        win.resize(g.width() - 1, g.height())
        win.resize(g.width(), g.height())

        modbus.start()
        modbus.updatedata.connect(logger.modbusupdate)

        exitcode = app.exec_()  # start the window's message loop
        recorder.close()
        persist.close()
        modbus.stop()
        while not modbus.hasstopped():
            time.sleep(0.1)

        del logger
        del recorder
        del win
        del ui
        del history
        del modbus
        del persist

        gc.collect()

        if exitcode != -1:
            break
