import csv
import random

'''
TODO:
	Optimize? Perhaps load the csv file into a dictionary (key: year, value: list of team data)
	for fast access each time its needed (i.e. not having to re-read through the whole csv file)
'''

class Data_Loader:

	def __init__(self, year):
		self.class_dict = {}
		self.inputs = []
		self.targets = []
		if year == None:
			self.year = random.randrange(1970, 2012)
		else:
			self.year = year
		# load the list of input vectors for a given year
		# year is in the 2nd column of the csv file'''	
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
				classif = data.pop(0)
				output[classif] = 1
				self.class_dict.setdefault(classif, []).append(data)
				self.targets.append(output)
				self.inputs.append(data)
		

	'''
	returns a 'balanced' list of inputs/targets. IE 1 non-playoff, 1 wc, 1 div, 1 conf, 1 super, 1 champ
	'''
	def getBalancedTargets(self):
		i = []
		t = []
		for classif,data in self.class_dict.items():
			num = random.randint(0,len(data)-1)
			i.append(data[num])
			_o = [0,0,0,0,0,0]
			_o[classif] = 1
			t.append(_o)
		return i,t
				
	
	

	@staticmethod
	def createFromRandomYear():
		year = random.randrange(1970, 2012)
		DL = Data_Loader(year)
				
		return DL
		
	@staticmethod
	def createFromYear(year):
		
		DL = Data_Loader(year)
				
		return DL
