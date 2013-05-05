import random
import itertools
import smote
from team import Team
from random import choice, random, sample
from math import pow, sqrt, ceil


'''
TODO:
    Optimize? Perhaps load the csv file into a dictionary (key: year, value: list of team data)
    for fast access each time its needed (i.e. not having to re-read through the whole csv file)
'''

class Data_Loader:

    data_list = [0,1,2,3,4,5,6,8,11,17,21,22,23,29,35,39]
    def __init__(self,f=None):
        self.year_dict = {}
        # load the list of input vectors for a given year
        # year is in the 2nd column of the csv file'''
        if f == None:   
            datafile = open('scaledData.csv', 'rU')
        else:
            datafile = open(f, 'rU')
        #datareader = csv.reader(datafile, dialect=csv.excel_tab)

        #skip first line
        datafile.readline()
        for row in datafile:
            data = row.strip().split(',')
            #print "Row :" + str(data) + "\n"
            #print "Year: " + str(year) + "\ndata[1] :" + str(data[1]) + "\n"
            
            #print "SAME!\n"
            (name,year) = (data.pop(0),int(data.pop(0)))
    
            #print (year,team)
            if year in self.year_dict:
                data = [float(x) for x in data]
                classif = int(data.pop(0))
                output = self.encode(classif)
                data = [data[i] for i in self.data_list]
                self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

            else:
                self.year_dict[year] = {}
                data = [float(x) for x in data]
                
                classif = int(data.pop(0))
                output = self.encode(classif)
                data = [data[i] for i in self.data_list]
                self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

            
            
            
    '''
    helper, converts classification number to output encoding 
    i.e. 1-5 to [0,0,0,0,0,1] etc.
    '''
    '''def encode(self, classification):
        o = [0,0,0,0,0,0]
        o[classification] = 1
        return o 
    '''
    def encode(self, classification):
        return [float(classification)/5]

    '''
    reverse encodes an output encoding to a classification number
    Parameters: 
        encoding: the encoding array
    Return:
        classification: an in representing the classification
    '''  
    '''
    def rev_encode(self, encoding):
        return encoding.index(1)
    '''
    def rev_encode(self, enc_classification):
        return enc_classification[0] * 5.0

    '''
    returns an ordered tuple of inputs, targets for the given year
    '''             
    def getTargets(self,years):
        inputs = []
        targets = []
        for year in years:
	        for k,v in self.year_dict[year].items():
	            inputs += reduce(lambda a, b : a + [b.stats],v, list())
	            targets += itertools.repeat(self.encode(k),len(v))
        return inputs,targets
    
    '''
    returns an 5 member ordered tuple of inputs, targets, with one from each class (randomly selected
        for classifications with more than one member)
    '''
    def getBalancedTargets(self,years):
        inputs = []
        targets = []
        for year in years:
	        for k,v in self.year_dict[year].items():
	            # notice we are appending here because these are just single lists, not lists of lists
	            inputs.append(choice(v).stats)
	            targets.append(self.encode(k))
        return inputs,targets

    '''
    Fills the data with BorderLine SMOTE targets until every classification has N members
    Parameters:
        N: the size to fill each class to
    Return Value:
        inputs, targets
    '''
    def getBLSmoteTargets(self,years,R):
        print "Creating SMOTE targets..."
        smote_count = 0
        inputs = []
        targets = []
        all_teams = []
        all_years = {}
        
        # build a class dictionary for all the years, must be done for SMOTE
        for year in years:
            for k,v in self.year_dict[year].items():
                all_years.setdefault(k,[]).extend(v)
                all_teams += v
        # find the largest class size and then increase it by R% for the new fill size
        largest_class_size = max(map(lambda c: len(c),all_years.values()))
        fill_size = int(ceil((1.0+R)*largest_class_size))
        
        # fill the inputs, targets, with SMOTE synthetics values
        for k,v in all_years.items():
            
            new_smote_number = (fill_size - len(v))
            smote_count += new_smote_number
            
            i,t =  smote.performBorderLineSmote(all_teams,k,new_smote_number)
            inputs += i
            targets += t

        # fill the i,t with the data set values
        i,t = self.getTargets(years)
        inputs += i
        targets += t
        print "Created %i SMOTE targets" % smote_count        
        return inputs, targets
        

    '''
    Will perform SMOTE oversampling to fix data imbalance problem in our data
    Parameters:
        years:  a list of years that we should do SMOTE processing on
    Return:
        a tuple of ordered lists representing the input stats and target results for ever
        team and SMOTE-produced synthetic team in the years provided
    '''
    def getSmoteTargets(self, years):
        pre_all_years = {}
        oversampled = []
        #for all the year range, make a list of lists by classifications - lists are tuple (input, target)
        for y in years:
            for (c,ts) in self.year_dict[y].items():
                map(lambda t: pre_all_years.setdefault(c,[]).append(t), ts)
           # map(lambda (c,l): all_years[c].append((l, self.encode(c))), zip(self.year_dict[y].keys(), self.year_dict[y].values()))
            #print str(all_years)
        all_years = {}#pre_all_years
        for i in range(20):
        	for k in pre_all_years.keys():
        		all_years.setdefault(k, []).append(choice(pre_all_years[k]))
        largest_classification = reduce(lambda m,l:  max(m, len(l)), all_years.values(), 0)
        #print "years: "+ all_years
        for l,c in all_years.items():
            oversample_amount = 3#largest_classification/float(len(c))
            #print "amount: " + str(oversample_amount)
            #print len(c)
            if oversample_amount > 1:
             #   print "in range for smote"
                for i in range(len(c)):
                    t = c[i]
                    number_of_neighbors = int(round(oversample_amount))
                    neighbors = smote.getClosestNeighbors(t, c, number_of_neighbors)
                    new_data = map(lambda n: (smote.vectorBetweenVectors(t.stats,n.stats), self.encode(t.classification)), neighbors)
                    oversampled+=new_data
            else:
                #print "over threshold for smote: " +str(self.encode(c[0].classification))
                oversampled+= map(lambda t: (t.stats, self.encode(t.classification)), c)
        inputs, targets = zip(*oversampled)
        return inputs, targets
                    
                
                    

    '''
    Get all (data, stats) tuples for the given year
    ''' 
    def getAllTeams(self,year):
        teams = []
        for v in self.year_dict[year].values():
            teams += v
        return teams
        
    '''
    Get all the times in the dictionary, for every year
    '''
    def getEveryTeam(self):
    	teams = []
    	for year in self.year_dict.values():
    		teams += reduce(lambda a,b: a + b, year.values())
    	return teams

    '''
    Get the given team by team code and year
    parameters:
        team: the team code as a string
        year: the year as an int
    return:
        the team as team object
    '''
    def getTeam(self, team, year):
        return filter(lambda t: t.name == team,self.getAllTeams(year))[0]



'''
Testing
'''     
if __name__ == "__main__":  
    dl = Data_Loader()
    #print dl.getBalancedTargets(2000)
    #print dl.getAllTeams(1992)
    all_i, all_t =  dl.getSmoteTargets([2008, 2009,2010,2011])
    smote = zip(all_i, all_t)
    smote_test_dict = {}
    for i,t in smote:
        smote_test_dict.setdefault(dl.rev_encode(t),[]).append(i)
    for k,v in smote_test_dict.items():
        print str(dl.encode(k)) + ": " + str(len(v))
    rk,rv = choice(smote_test_dict.items())
    for t in rv:
    	print str(dl.encode(rk))	 + " -> " + str(t)

