import csv
import random

class Data_Loader:

	def __init__(self, year):
		self.inputs = []
		self.target = []
		if year == None:
			self.year = random.randrange(1970, 2012)
		else:
			self.year = year
			
		datafile = open('scaledData.csv', 'rU')
		#datareader = csv.reader(datafile, dialect=csv.excel_tab)
		for row in datafile:
			data = row.strip().split(',')
			#print "Row :" + str(data) + "\n"
			#print "Year: " + str(year) + "\ndata[1] :" + str(data[1]) + "\n"
			if (data[1] == str(year)):
				#print "SAME!\n"
				del data[0]
				del data[0]
				#print "Row :" + str(data) + "\n"
				data = [int(float(x)) for x in data]
				output = [0, 0, 0, 0, 0, 0]
				output[data.pop(0)] = 1
				self.target.append(output)
				self.inputs.append(data)
		


	
	# load the list of input vectors for a given year
	# year is in the 2nd column of the csv file'''
	@staticmethod
	def createFromRandomYear():
		year = random.randrange(1970, 2012)
		DL = Data_Loader(year)
				
		return DL
		
	@staticmethod
	def createFromYear(year):
		
		DL = Data_Loader(year)
				
		return DL
