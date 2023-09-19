# JCT Technology Ltd Datalogger 1.0
# by Andrew Keeley (andy@pcman.ca)
# March 2018

# ModBus Manager Thread
# Launches ModBus TCP receiver threads and collates results then emits them to main thread

# standard / third party libraries
import threading
import time
import datetime
from PyQt5 import QtCore

# project libraries
from inc.modbus import ModbusClient
from config import *



class ModBusRX(QtCore.QThread):
	updatedata = QtCore.pyqtSignal(list, list, datetime.datetime)
    
	# def __del__(self):
	# 	self.wait()

	def __init__(self, registers):
		super(ModBusRX, self).__init__()
		self.stop_event = threading.Event()										        # create a flag event to close
		self.registers = registers

		self.modbus = []
		for i, s in enumerate(SERVERS):
			self.modbus.append(ModbusClient(server=s,registers=registers,servernum=i))	# create ModbusClient instance
			self.modbus[i].update.connect(self.incoming)
			self.modbus[i].start()
		self.stopped = True
		self.values = [0 for _ in registers[0]]
		self.status = [True for _ in SERVERS]



	def run(self):
		self.stopped = False


		lastsec = datetime.datetime.now().second								# used to check when seconds change
		#MRS2 Start

		reset1 = 0
		reset2 = 0
		reset3 = 0
		reset4 = 0
		reset5 = 0
		reset6 = 0
		reset7 = 0
		reset8 = 0
		reset9 = 0
		reset10 = 0

		total = 0


		#MRS2 END
		while not self.stop_event.is_set():										# repeat until stop event
			time.sleep(.1)														# sleep for 1/10th sec
			timenow = datetime.datetime.now()									# get current time
			cursec = timenow.second												# get seconds from current time
			if cursec != lastsec and timenow.microsecond > 500000:				# if second has changed
				lastsec = cursec												# update last second
				#MRS2 START
				#print(self.values)


				#calculation total rate
				self.values[21] = self.values[5] + self.values[10] + self.values[11]

				#calculation for total totaliser 1

				total += self.values[21]/60

				self.values[22] = total
				self.values[23] = total
				self.values[24] = total
				self.values[25] = total
				self.values[26] = total
				self.values[32] = total
				self.values[33] = total
				self.values[34] = total
				self.values[35] = total
				self.values[36] = total
				#print(self.values[2])
				#print(self.values[12])

				self.values[42] = (self.values[2] * 1000) + self.values[12]
				#print(self.values[42])



				if self.values[27] != reset1:
					self.values[22] = 0
					reset1 = self.values[27]

				if self.values[28] != reset2:
					self.values[23] = 0
					reset2 = self.values[28]

				if self.values[29] != reset3:
					self.values[24] = 0
					reset3 = self.values[29]

				if self.values[30] != reset4:
					self.values[25] = 0
					reset4 = self.values[30]

				if self.values[31] != reset5:
					self.values[26] = 0
					reset5 = self.values[31]

				if self.values[31] != reset5:
					self.values[26] = 0
					reset5 = self.values[31]

				if self.values[27] != reset6:
					self.values[32] = 0
					reset6 = self.values[27]

				if self.values[28] != reset7:
					self.values[33] = 0
					reset7 = self.values[28]

				if self.values[29] != reset8:
					self.values[34] = 0
					reset8 = self.values[29]

				if self.values[30] != reset9:
					self.values[35] = 0
					reset9 = self.values[30]

				if self.values[31] != reset10:
					self.values[36] = 0
					reset10 = self.values[31]


				#MRS2 END
				#print (c_1)

				self.updatedata.emit(self.status, self.values, timenow)			# emit new data for processing
		for m in self.modbus:
			m.stop()
			while not m.hasstopped():
				time.sleep(0.1)
		self.stopped = True

	def incoming(self, status, values, server):
		#print(values)
		self.status[server] = status
		if status:
			c = 0
			for i, r in enumerate(self.registers[0]):
				if r[4]-1 == server:
					self.values[i] = values[c]
					c += 1

	def hasstopped(self):
		return self.stopped

	def stop(self):
		self.stop_event.set()													# set event to stop the thread

	def resettotalisers(self):

		for m in self.modbus:
			m.resettotalisers()

    #MRS START
	def resettotalisers2(self):
		for m in self.modbus:
			m.resettotalisers2()
            
	def resettotalisers3(self):
		for m in self.modbus:
			m.resettotalisers3()

	def reset1(self):
		for m in self.modbus:
			m.reset1()

	def reset2(self):
		for m in self.modbus:
			m.reset2()

	def reset3(self):
		for m in self.modbus:
			m.reset3()

	def reset4(self):
		for m in self.modbus:
			m.reset4()

	def reset5(self):
		for m in self.modbus:
			m.reset5()

	def reset6(self):
		for m in self.modbus:
			m.reset6()

	def reset7(self):
		for m in self.modbus:
			m.reset7()

	def reset8(self):
		for m in self.modbus:
			m.reset8()

	def reset9(self):
		for m in self.modbus:
			m.reset9()

	def reset10(self):
		for m in self.modbus:
			m.reset10()
	#MRS END

    #MRS2 START



    #MRS2 END