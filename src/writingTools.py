import os
from fpdf import FPDF
from trame import *
from liste_trames import *

class PDF(FPDF):

	# PDF Header
	def header(self):
		self.set_font("Helvetica", "B", size = 20)
		self.set_line_width(1)
		self.image(os.path.join(os.path.dirname(__file__), "../icons/logo.png"), 10, 8, 15)
		self.cell(0, 10, "FLOW GRAPH", new_x = "LMARGIN", new_y = "NEXT", align = "C", border = "B")
		self.ln(8)

	# PDF Pages
	def footer(self):
		self.set_y(-15)
		self.set_font("Helvetica", size = 10)
		self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "R")

	# Writing Content
	def print_cell(self, frame):
		content = frame.flow_graph()

		self.set_font("Helvetica", size = 9)
		self.set_fill_color(255, 255, 255)


		# Fill color according to highest protocol
		if (frame.ip != None and frame.ip.typ=="IPv4"):
			if (frame.transport != None and frame.transport.get_typ() == "TCP"):
				self.set_fill_color(228, 255, 199)
				
			elif (frame.transport != None and frame.transport.get_typ() == "UDP"):
				self.set_fill_color(218, 238, 255)

			elif (frame.transport != None and frame.transport.get_typ()=="ICMP"):
				self.set_fill_color(252, 224, 255)

			elif (frame.transport != None and frame.transport.get_typ()=="IGMP"):
				self.set_fill_color(254, 255, 208)

			if (frame.http != None):
				self.set_fill_color(231, 230, 255)


		elif (frame.ip != None and frame.ip.get_typ() == "ARP"):
			self.set_fill_color(250, 240, 215)


		self.cell(0, 10, txt = content, new_x = "LMARGIN", fill = 1)
		self.ln(8)
		


# PDF Creation
def create_pdf(filename, frame_liste):
	pdf = PDF(orientation = "L", unit = "mm", format = "A4")

	# Metadata and Default Settings
	pdf.set_title("FLOW CHART")
	pdf.set_author("WireLinks 1.0.0")
	pdf.add_page()
	pdf.set_auto_page_break(auto = True, margin = 15)

	for frame in frame_liste:
		pdf.print_cell(frame)
		
	if not filename.endswith(".pdf"):
		filename += ".pdf"	

	pdf.output(filename)
