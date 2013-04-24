'''
Here we will take a team's stats and run it through the trained neural network. 
This will output the projected playoff results, as well as teams from the past that
produced a similar output result.
'''
from neural_network import Neural_Network

class NFL_Predictor:
    
    '''
    create a predictor class
    Parameters:
        network_path:	file path of saved neural network
    '''
    def __init__(self, network):
        self.nn = network
        
    '''
    returns expected playoff wins from trained neural network
    Parameters:
        team_stats: list of a single team's stats ordered as required for the neural
                    network
	Return:
		feed-forward result of team's stats from neural network
    '''
    def runPrediction(team_stats):
    	return nn.feed_forward(team_stats)
        
    '''
    returns the team that produces the closest prediction to the given team
    Parameters:
        all_stats: 	list of list of stats for all NFL teams in the playoff era
        			must be ordered as required for the neural network
        team_stats: list of a single team's stats ordered as required for the neural 
        			network
        num_teams: 	number of similar teams to return
    Return:
    	list of tuples containing num_teams of similar teams in the format
    	(list of team's stats, least squares difference)
    '''
    def compareWithPastTeams(all_stats, team_stats, num_teams):
        all_ff_results = []
        team_ff_results = runPrediction(team_stas)
        for t in all_stats:
            all_ff_results.append(nn.feed_forward(t))
        distances_to_team = map(lambda t: (t, compareVector(team_ff_results, t)), team_ff_results)
        'more work to be done here'
        
    '''
    compare two vectors by euclidean distance
    Parameters:
    	v1,v2: 	two lists of numbers representing a vector - assumes they are the same
    			length because the neural network produces an output list of uniform
    			length
    Return:
    	euclidean distance between two vectors
    '''
    def compareVector(v1, v2):
    	sum = 0
    	for i1,i2 in zip(v1,v2):
    		sum += math.pow((i1-i2),2)
    	return math.sqrt(sum)
    	
        
        
    
        
        
    