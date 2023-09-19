# JCT Technology Ltd Datalogger 1.0
# by Andrew Keeley (andy@pcman.ca)
# March 2018

# Modbus Client class

# standard / third party libraries

from PyQt5 import QtCore
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException,  ConnectionException
import struct
import datetime
import time
import threading


class ModbusClient(QtCore.QThread):
	update = QtCore.pyqtSignal(bool, list, int)									# emits status, values, servernum


	def __init__(self, server, registers, servernum):


		super(ModbusClient, self).__init__()
		self.stop_event = threading.Event()										# create a flag event to close

		self.regmap = registers[0]

		self.server = servernum
		metrics = registers[self.server + 1]
		self.inpbase = 0 if metrics[0] == 0 else (metrics[0] - 30001)			# the first input register to read
		self.inpcount = 0 if metrics[0] == 0 else (metrics[1] - metrics[0] + 1)
		self.hldbase = 0 if metrics[2] == 0 else (metrics[2] - 40001)			# the first holding register to read
		self.hldcount = 0 if metrics[2] == 0 else (metrics[3] - metrics[2] + 1)
		self.mbc = ModbusTcpClient(server[0], server[1])						# create a Modbus client to server at IP address specified in config
		self.inpregs = None
		self.hldregs = None
		self.stopped = True
		self.offline = False

		self.inpregs_reset = None


	def run(self):
		self.stopped = False
		lastsec = datetime.datetime.now().second  								# used to check when seconds change
		while not self.stop_event.is_set():  									# repeat until stop event
			time.sleep(.1)  													# sleep for 1/10th sec
			timenow = datetime.datetime.now()  									# get current time
			cursec = timenow.second  											# get seconds from current time
			if cursec != lastsec:												# if second has changed
				lastsec = cursec  												# update last second
				s, r = self.read()  											# get success flag and registers
				if not s:
					r = []
				self.update.emit(s, r, self.server)								# emit new data to Modbus manager

		self.mbc.close()
		self.stopped = True


	def read(self):
		try:
			if (self.server + 1) == 1:
				if self.inpcount:
					self.inpregs = self.mbc.read_input_registers(self.inpbase, self.inpcount,unit=110)  # read input registers
				if self.hldcount:
					self.hldregs = self.mbc.read_holding_registers(self.hldbase, self.hldcount,unit=110)  # read holding registers
			else:
				if self.inpcount:
					self.inpregs = self.mbc.read_input_registers(self.inpbase, self.inpcount)  # read input registers
				if self.hldcount:
					self.hldregs = self.mbc.read_holding_registers(self.hldbase,self.hldcount)  # read holding registers
                                

		except ConnectionException:												# if connection failed
			self.offline = True
			return False, None
		if type(self.hldregs) is ModbusIOException:								# connected but no response!
			self.offline = True
			return False, None

		self.offline = False
		self.values = []																# initialise a list for the values
		for r in self.regmap:													# iterare the register map
			if r[4] == self.server + 1:
				if r[2] in ['U2', 'I2']:
					b = self.getword(r)											# get one register as a U2
				else:
					b = self.getdword(r)										# get two registers as a U4
				if r[2][0] == 'U':
					self.values.append(b)
				elif r[2][0] == 'F':
					self.values.append(struct.unpack(">f", struct.pack(">I", b))[0])
				elif r[2] == 'I4':
					self.values.append(struct.unpack(">i", struct.pack(">I", b))[0])
				elif r[2] == 'I2':
					self.values.append(struct.unpack(">h", struct.pack(">H", b))[0])
				else:
					self.values.append(0)											# safety net

		return True, self.values														# return success flags and values

	def getword(self, register):
		if 30001 <= register[1] <= 39999:
			return self.inpregs.registers[register[1] - 30001 - self.inpbase]
		elif 40001 <= register[1] <= 49999:
			return self.hldregs.registers[register[1] - 40001 - self.hldbase]

		return 0																# safety net

	def getdword(self, register):
		if 30001 <= register[1] <= 39998:
			return self.inpregs.registers[register[1]-30000-self.inpbase]*2**16+self.inpregs.registers[register[1]-30001-self.inpbase]
		elif 40001 <= register[1] <= 49998:
			return self.hldregs.registers[register[1]-40000-self.hldbase]*2**16+self.hldregs.registers[register[1]-40001-self.hldbase]
		return 0																# safety net

	def resettotalisers(self):
		if not self.offline:
			try:
				self.mbc.write_register(address=2049, value=0x01, unit=110)        #Reset Reset Combined Total 
			except ConnectionException:
				pass

    #MRS START            
	def resettotalisers2(self):
		if not self.offline:
			try:
				self.mbc.write_register(address=110, value=0x01, unit=0)        #Reset Reset Combined Total
			except ConnectionException:
				pass                
			
	def resettotalisers3(self):
		if not self.offline:
			try:
				self.mbc.write_register(address=112, value=0x01, unit=0)        #Reset Reset Combined Total
			except ConnectionException:
				pass

	def reset1(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=119,count=1,unit=0)
				self.x = self.rr.registers[0]
				self.x += 1

				self.mbc.write_register(address=119, value=self.x, unit=0)  # Reset total 1
			except ConnectionException:
				pass

	def reset2(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=120,count=1,unit=0)
				self.x = self.rr.registers[0]
				self.x += 1

				self.mbc.write_register(address=120, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset3(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=121,count=1,unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=121, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset4(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=122,count=1,unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=122, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset5(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=123,count=1,unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=123, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

			def reset5(self):
				if not self.offline:
					try:
						self.rr = self.mbc.read_holding_registers(address=123, count=1, unit=0)
						self.x = self.rr.registers[0]
						self.x += 1
						self.mbc.write_register(address=123, value=self.x, unit=0)  # Reset total 2
					except ConnectionException:
						pass


	def reset6(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=124, count=1, unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=124, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset7(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=125, count=1, unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=125, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset8(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=126, count=1, unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=126, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset9(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=127, count=1, unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=127, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass

	def reset10(self):
		if not self.offline:
			try:
				self.rr = self.mbc.read_holding_registers(address=126, count=1, unit=0)
				self.x = self.rr.registers[0]
				self.x += 1
				self.mbc.write_register(address=126, value=self.x, unit=0)  # Reset total 2
			except ConnectionException:
				pass




			#MRS END
	def hasstopped(self):
		return self.stopped

	def stop(self):
		self.stop_event.set()  													# set event to stop the thread
