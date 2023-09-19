# Path to save log files
LOG_PATH = "C:\Log Files"

# Modbus server
SERVERS = [
('127.0.0.1', 502),  #frac pump 192.168.1.10
('127.0.0.1', 502)   #twin pump 192.168.2.10
]

# Modbus register map
# Friendly name, Modbus register number, type (U2, I2, U4, I4, F), decimals (0-9), Server number
MODBUS_REGISTERS = [
	("Pump Pressure", 40001, "I2",2, 1),        #registers[0]
	("Pump Rate", 40001, "I2",0, 1),            #registers[1]
	("Pump Total", 40002, "I2",2, 1),           #registers[2]
	("Aux Rate", 40003, "I2",0, 1),             #registers[3]   
	("Aux Total", 40004, "I2",2, 1),            #registers[4]
	("Combined Rate", 40005, "I2",0, 1),        #registers[5]
	("Combined Total", 40006, "I2",2, 1),       #registers[6]

	("DS Pump Pressure", 40007, "I2", 2, 2),    #registers[7]
	("PS Pump Pressure", 40008, "I2", 2, 2),    #registers[8]
	("Combined Rate LPM", 40009, "I2", 0, 2),   #registers[9]
	("DS Pump Rate", 40010, "I2", 0, 2),        #registers[10]
	("PS Pump Rate", 40011, "I2", 0, 2),        #registers[11]
	("Combined Total M3", 40012, "I2", 2, 2),   #registers[12]S
	("DS Pump Total", 40013, "I2", 3, 2),       #registers[13]
	("PS Pump Total", 40014, "I2", 3, 2),       #registers[14]
	("DS Boost Pressure", 40015, "I2", 2, 2),   #registers[15]
	("PS Boost Pressure", 40016, "I2", 2, 2),   #registers[16]
	("DS Lube Pressure", 40017, "I2", 0, 2),    #registers[17]
	("PS Lube Pressure", 40018, "I2", 0, 2),    #registers[18]
	("DS Lube Temp", 40019, "I2", 2, 2),        #registers[19]
	("PS Lube Temp", 40020, "I2", 2, 2),        #registers[20]


    # Below this only dummy for local tags
	("Total Rate", 30001, "I2", 0, 2),           #registers[21]
	("Total Totaliser 1 twin", 30002, "I2", 2, 2),    #registers[22]
	("Total Totaliser 2 twin", 30003, "I2", 2, 2),    #registers[23]
	("Total Totaliser 3 twin", 30004, "I2", 2, 2),    #registers[24]
	("Total Totaliser 4 twin", 30005, "I2", 2, 2),    #registers[25]
	("Total Totaliser 5 twin", 30006, "I2", 2, 2),    #registers[26]
    
    #("Pump Pressure", 44096, "F",2, 1),
	#("Pump Rate", 44098, "F",0, 1),
	#("Pump Total", 44100, "F",2, 1),
	#("Aux Rate", 44102, "F",0, 1),
	#("Aux Total", 44104, "F",2, 1),
	#("Combined Rate", 44106, "F",0, 1),
	#("Combined Total", 44108, "F",2, 1),

	#("DS Pump Pressure", 30001, "I2", 2, 2),
	#("PS Pump Pressure", 30002, "I2", 2, 2),
	#("Combined Rate LPM", 40112, "I2", 0, 2),
	#("DS Pump Rate", 40102, "I2", 0, 2),
	#("PS Pump Rate", 40101, "I2", 0, 2),
	#("Combined Total M3", 40107, "U4", 3, 2),
	#("DS Pump Total", 40105, "U4", 3, 2),
	#("PS Pump Total", 40103, "U4", 3, 2),
	#("DS Boost Pressure", 30003, "I2", 2, 2),
	#("PS Boost Pressure", 30004, "I2", 2, 2),
	#("DS Lube Pressure", 30006, "I2", 0, 2),
	#("PS Lube Pressure", 30005, "I2", 0, 2),
	#("DS Lube Temp", 30008, "I2", 2, 2),
	#("PS Lube Temp", 30007, "I2", 2, 2),

         #for Reset
	("reset1", 40120, "I2", 0, 2),               #registers[27] 20
	("reset2", 40121, "I2", 0, 2),               #registers[28] 21
	("reset3", 40122, "I2", 0, 2),               #registers[29] 22
	("reset4", 40123, "I2", 0, 2),               #registers[30] 23
	("reset5", 40124, "I2", 0, 2),             #registers[31] 24

	("Total Totaliser 6 Frac", 30007, "I2", 2, 2),  # registers[32]
	("Total Totaliser 7 Frac", 30008, "I2", 2, 2),  # registers[33]
	("Total Totaliser 8 Frac", 30009, "I2", 2, 2),  # registers[34]
	("Total Totaliser 9 Frac", 30010, "I2", 2, 2),  # registers[35]
	("Total Totaliser 10 Frac", 30011, "I2", 2, 2),  # registers[36]

	("reset6", 40125, "I2", 0, 2),  # registers[37] 20
	("reset7", 40126, "I2", 0, 2),  # registers[38] 21
	("reset8", 40127, "I2", 0, 2),  # registers[39] 22
	("reset9", 40128, "I2", 0, 2),  # registers[40] 23
	("reset10", 40129, "I2", 0, 2),  # registers[41] 24
	("Total Totaliser", 30012, "I2", 2, 2),  # registers[42]

		
]

# Text for up to three custom annotation buttons. Use "" for unused buttons.
ANNOTATION_1 = "Start Job"
ANNOTATION_2 = 'Pressure Test'
ANNOTATION_3 = "Custom 0"
ANNOTATION_4 = "Custom 1"
ANNOTATION_5 = 'Custom 2'
ANNOTATION_6 = "Custom 3"
