class Tcp:

	def __init__(self, typ, trame):
		# Parser
		self.typ = typ

		self.port_src = trame[:4]
		self.port_dst = trame[4:8]

		self.seq_num = trame[8:16]

		self.ack_num = trame[16:24]

		self.thl = trame[24]
		self.reserved = str(hex(int(trame[25:28], 16) >> 6))
		self.urg = str((int(trame[25:28], 16) & 32) >> 5)
		self.ack = str((int(trame[25:28], 16) & 16) >> 4)
		self.psh = str((int(trame[25:28], 16) & 8) >> 3)
		self.rst = str((int(trame[25:28], 16) & 4) >> 2)
		self.syn = str((int(trame[25:28], 16) & 2) >> 1)
		self.fin = str(int(trame[25:28], 16) & 1)
		self.window = trame[28:32]

		self.chk = trame[32:36]
		self.up = trame[36:40]

		# Options
		self.opt_length = int(self.thl, 16)*8 - 40
		self.opt = trame[40:40+self.opt_length]
		
		if (trame[40+self.opt_length:] != ""):
			self.data = trame[40+self.opt_length:]
		else:
			self.data = None


		# Application according to the source or destination port
		if (self.port_src=="0050" or self.port_dst=="0050"):
			self.appli = "HTTP"

		elif (self.port_src=="0019" or self.port_dst=="00019"):
			self.appli = "SMTP"

		elif (self.port_src=="008F" or self.port_dst=="0008F"):
			self.appli = "IMAP"

		elif (self.port_src=="006E" or self.port_dst=="006E"):
			self.appli = "POP"

		elif (self.port_src=="0035" or self.port_dst=="0035"):
			self.appli = "DNS"

		elif (self.port_src=="01BB" or self.port_dst=="01BB"):
			self.appli = "HTTPS"

		elif (self.port_src=="0043" or self.port_dst=="0043"):
			self.appli = "DHCP"

		elif (self.port_src=="0016" or self.port_dst=="0016"):
			self.appli = "SSH"

		elif (self.port_src=="0D3D" or self.port_dst=="0D3D"):
			self.appli = "RDP"

		elif (self.port_src=="0014" or self.port_dst=="0014" or self.port_src=="0015" or self.port_dst=="0015"):
			self.appli = "FTP"

		else:
			self.appli = "Unknown"

		self.options()

	def options(self):
		self.opt_det = []
		len_opt = 0
		next_opt = 0
		nb_opt = 0

		while (next_opt != self.opt_length):

			if (self.opt[next_opt:next_opt+2] == "00"):
				self.opt_det.append({"Name": "EOL (0x00)"})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "01"):

				self.opt_det.append({"Name": "No-Operation (0x01)", "Len":1})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1

			elif(self.opt[next_opt:next_opt+2] == "02"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "MSS (0x02)", "Len":len_opt})
				self.opt_det[nb_opt]["MSS"] = int(self.opt[next_opt+4:next_opt+8], 16)
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "03"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Window Scale (0x03)", "Len":len_opt})
				self.opt_det[nb_opt]["Scale"] = self.opt[next_opt+4:next_opt+6]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "04"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "SACK Permitted (0x04)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "05"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "SACK (0x05)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["SACK"] = self.opt[next_opt+4:next_opt+len_opt]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "06"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Echo (0x06)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["Info"] = self.opt[next_opt+4:next_opt+len_opt]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "07"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Echo Reply (0x07)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["Info"] = self.opt[next_opt+4:next_opt+len_opt]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "08"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Timestamp (0x08)", "Len": len_opt})
				self.opt_det[nb_opt]["Timestamp Value"] = self.opt[next_opt+4:next_opt+12]
				self.opt_det[nb_opt]["Timestamp Echo Reply Value"] = self.opt[next_opt+12:next_opt+20]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "09"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Partial Order Connection Permitted (0x09)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "0A"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "POC Service-Profile (0x0A)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["Start_Flag"] = self.opt[next_opt+4] and 0x8
				self.opt_det[nb_opt]["End_Flag"] = self.opt[next_opt+4] and 0x4
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "0B"):
				
				self.opt_det.append({"CC (0x0B)": self.opt[next_opt:]})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "0C"):
				
				self.opt_det.append({"CC.NEW (0x0C)": self.opt[next_opt:]})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1
			
			elif (self.opt[next_opt:next_opt+2] == "0D"):
				
				self.opt_det.append({"CC.ECHO (0x0D)": self.opt[next_opt:]})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "0E"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "TCP: Alternate Checksum Request (0x0E)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["CHK"] = self.opt[next_opt+4:next_opt+6]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			elif (self.opt[next_opt:next_opt+2] == "0F"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "TCP: Alternate Checksum Data (0x0F)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["CHK Data"] = self.opt[next_opt+4:next_opt+len_opt]
				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1

			else:
				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Other": self.opt[next_opt:next_opt+len_opt*2]})
				next_opt = next_opt+len_opt*2

		self.nb_opt = nb_opt




	# Getters
	def get_typ(self):
		return self.typ

	def get_port_dst(self):
		return self.port_dst

	def get_port_src(self):
		return self.port_src

	def get_seq_num(self):
		return self.seq_num

	def get_ack_num(self):
		return self.ack_num

	def get_thl(self):
		return self.thl

	def get_reserved(self):
		return self.reserved

	def get_urg(self):
		return self.urg

	def get_ack(self):
		return self.ack

	def get_psh(self):
		return self.psh

	def get_rst(self):
		return self.rst

	def get_syn(self):
		return self.syn

	def get_fin(self):
		return self.fin

	def get_window(self):
		return self.window

	def get_chk(self):
		return self.chk

	def get_up(self):
		return self.up

	def get_opt(self):
		return self.opt

	def get_data(self):
		return self.data

	def get_appli(self):
		return self.appli



	# String
	def __str__(self):
		chaine =  f"{self.typ}:\n\tSource Port: {int(self.port_src, 16)}\
		\n\tDestination Port: {int(self.port_dst, 16)}\
		\n\tSequence Number: {int(self.seq_num, 16)}\
		\n\tACK Number: {int(self.ack_num, 16)}\
		\n\tTHL: {int(self.thl, 16)*4}\
		\n\tReserved: {self.reserved}\
		\n\tURG: {self.urg}\
		\n\tACK: {self.ack}\
		\n\tPSH: {self.psh}\
		\n\tRST: {self.rst}\
		\n\tSYN: {self.syn}\
		\n\tFIN: {self.fin}\
		\n\tWindow: {int(self.window, 16)}\
		\n\tChecksum: 0x{self.chk}\
		\n\tUrgent pointer: {int(self.up, 16)}\
		\n\tApplication: {self.appli}"
		
		if (self.nb_opt > 0):
			chaine += f"\n\tOptions:\n\t     "

			for i in range(len(self.opt_det)):
				for key, value in self.opt_det[i].items():
					chaine += f"{key} = {value}   "
				chaine += "\n\t     "

		return chaine