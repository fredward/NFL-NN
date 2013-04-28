'''
Here we will take a team's stats and run it through the trained neural network. 
This will output the projected playoff results, as well as teams from the past that
produced a similar output result.
'''
from neural_network import Neural_Network
from math import pow, sqrt

class NFL_Predictor:
    
    '''
    create a predictor class
    Parameters:
        network: 	a Neural_Network object
    '''
    def __init__(self, network):
        self.nn = network
        
    '''
    returns expected playoff wins from trained neural network
    Parameters:
        team_stats: list of a single team's stats ordered as required for the neural
                    network
    Return:
        feed-forward result of team's stats from neural network (float list)
    '''
    def runPrediction(self, team_stats):
        return nn.feed_forward(team_stats)
        
        
    '''
    returns the team that produces the closest prediction to the given team
    Parameters:
        all_stats:  list of tuples of teams' stats for the team to be compared against
        			each tuple should be in standard format from the dataLoader
        				((year, team_name), stats)
                    stats must be ordered as required for the neural network
        team_stats: tuple of a single team's stats for the team to be compared against
        			each tuple should be in standard format from the dataLoader
        				((year, team_name), stats)
        num_teams:  number of similar teams to return
    Return:
        list of tuples containing num_teams of similar teams in the format
        (((year, team_name), stats), least squares difference)
    '''
    def compareWithPastTeams(self, all, team, num_teams):
        all_ff_results = []
        all_stats = map(lambda ((y,n),l): l, all)
        team_stats = team[1]
        team_ff_results = self.runPrediction(team_stats)
        for t in all:
        	stat = t[1]
        	all_ff_results.append((t,nn.feed_forward(stat)))
        distances_to_team = map(lambda (t,r): (t, self.compareVector(team_ff_results, r)), all_ff_results)
        sorted_distances = sorted(distances_to_team, key = lambda (t,d): d)
        similar_teams = []
        for i in range(num_teams):
            similar_teams.append(sorted_distances.pop(0))
        return similar_teams
        
        
    '''
    compare two vectors by euclidean distance
    Parameters:
        v1,v2:  two lists of numbers representing a vector - assumes they are the same
                length because the neural network produces an output list of uniform
                length
    Return:
        euclidean distance between two vectors (float)
    '''
    def compareVector(self, v1, v2):
        sum = 0
        for i1,i2 in zip(v1,v2):
            sum += pow((i1-i2),2)
        return sqrt(sum)
        
'''
Testing
'''   
if __name__ == "__main__":
	from data_loader import Data_Loader 
	nn = Neural_Network.createWithRandomWeights(66,40,6)	
		
	# train! with learning rate proportional to # of teams in the situations
	inputs = []
	targets = []
	for y in range(2005,2007):
		DL = Data_Loader()
		i,t = DL.getTargets(y)
		inputs += i
		targets += t 
		#print targets
	nn = nn.train(30,inputs,targets,1.5)
	
	DL = Data_Loader()
	teams_2011 = DL.getAllTeams(2011)
	pats_2011 = filter(lambda ((y,n),l): n == "nwe", teams_2011)[0]
	pats_data = pats_2011[1]
	all_other_teams = filter(lambda ((y,n),l): n != "nwe", teams_2011)
	all_other_teams_data = map(lambda ((y,n),l): l, all_other_teams)
	predictor = NFL_Predictor(nn)
	similar = predictor.compareWithPastTeams(all_other_teams, pats_2011, 3)
	print str(similar)
	
	
	 
	
	
        
        
    
        
        
    