class Igmp:

	def __init__(self, typ, frame):
		# Parsing the default header fields
		self.typ = typ
		self.type_igmp = frame[:2]
		self.unused = frame[2:4]
		self.chk = frame[4:8]
		self.class_ip = f"{int(frame[8:10], 16)}.{int(frame[10:12], 16)}.{int(frame[12:14], 16)}.{int(frame[14:16], 16)}"
		self.data = frame[16:]

		if (self.type_igmp == "11"):
			self.type_igmp2 = "Request"

		elif (self.type_igmp == "22"):
			self.type_igmp2 = "Report v3"
		elif (self.type_igmp == "12"):

			self.type_igmp2 = "Report v1"
		elif (self.type_igmp == "16"):

			self.type_igmp2 = "Report v2"
		elif (self.type_igmp == "17"):

			self.type_igmp2 = "Exit v2"
		else:
			self.type_igmp2 = "Unknown"



	# Getters
	def get_typ(self):
		return self.typ

	def get_type_igmp(self):
		return self.type_igmp
	
	def get_type_igmp2(self):
		return self.type_igmp2

	def get_unused(self):
		return self.unused

	def get_chk(self):
		return self.chk

	def get_class_ip(self):
		return self.class_ip

	def get_data(self):
		return self.data



	# String
	def __str__(self):
		return f"{self.typ}:\
		\n\tIGMP Type: {self.type_igmp}\
		\n\tChecksum: 0x{self.chk}\
		\n\tGroup Address: {self.class_ip}"
