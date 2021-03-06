from neural_network import Neural_Network
from data_loader import Data_Loader
from itertools import izip, count, repeat
from nfl_predictor import NFL_Predictor
import team_dict
import os
import argparse
'''
A main file, for directing user input from the highest level. Will load and use
all our other classes
'''

def train(args):
	try:
		
		inputs = []
		targets = []
		y = range(args.start,args.end+1)
		if(args.db == 'u'):
			dl = Data_Loader()
			i,t = dl.getTargets(y)
		elif(args.db == 'b'):
			dl = Data_Loader()
			i,t = dl.getBalancedTargets(y)
		elif(args.db == 'p'):
			dl = Data_Loader('playoffTeams.csv')
			i,t = dl.getTargets(y)
		elif(args.db == 'o'):
			dl = Data_Loader('balancedData.csv')
			i,t = dl.getTargets(y)
		elif(args.db == 's'):
			dl = Data_Loader()
			i,t = dl.getBLSmoteTargets(y,.25)
			#i,t = dl.getSmoteTargets(y)
		inputs += i
		targets += t
		#create NN
		# if file already exists, build on that training
		if (os.path.exists(args.file)):
			print "file exists"
			nn = Neural_Network.createFromFile(args.file)
			pass
		else:
			print "file does not exist"
			nn = Neural_Network.createWithRandomWeights(len(inputs[0]),args.nodes,len(targets[0]))
		
		#train NN with the given data
		print 'Beginning Training...'
		nn = nn.train(args.epochs,inputs,targets,args.learn_rate)
		nn.saveToFile(args.file)
		print "Neural Network saved to %s" % (args.file)
	except Exception as e:
		print "invalid formatting, consult neural_main.py t --help \n Error: %s" % e

def predict(args):
	try:
		nn = Neural_Network.createFromFile(args.file)
		dl = Data_Loader()

		#team = dl.getTeam(args.team, args.year)
		team = dl.getTeam(args.team, args.year)
		result = nn.feed_forward(team.stats)
		print "\n\nPredicting the %i %s..." % (args.year, team_dict.teams[args.team])
		print "RESULTS: %.3f\n" % result[0]
		if args.show_expected:
			print "EXPECTED: %s" % (dl.encode(team.classification))[0]
		results_graph = "\t|" + "".join(repeat("-",int(result[0]/.8*50))) + "|" + "".join(repeat("-",(int((1-result[0]/.8)*50)))) + "|"
		print "  Not in playoffs" + "".join(repeat(" ",35)) + "Super Bowl Champs"
		print results_graph
		post_processor = NFL_Predictor(nn)
		similar_teams = post_processor.compareWithPastTeams(dl.getEveryTeam(), team, 16)
		print"\nThe 15 most similar teams throughout history:"
		del similar_teams[0]
		for t in similar_teams:
			print "%s \tScore: %f" % t
	except Exception as e:
		print "invalid formatting, consult neural_main.py t --help \n Error: %s" % e

def cross_validate(args):
	# import some functions
	encode = Data_Loader().encode
	find_error = NFL_Predictor().compareVector
	try:	
		nn = Neural_Network.createFromFile(args.file)
		print "Loaded Neural Network with %i hidden nodes" % len(nn.hidden_nodes)
		totalCorrect = 0.0
		total_tested = 0.0
		for y in range(args.start,args.end+1):
			classRight = [0, 0, 0, 0, 0, 0]
			correct = incorrect = 0
			if(args.db == 'u'):
				dl = Data_Loader()
				teams = dl.getAllTeams(y)
			elif(args.db == 'b'):
				dl = Data_Loader()
				teams = dl.getAllTeams(y)
			elif(args.db == 'p'):
				dl = Data_Loader('playoffTeams.csv')
				teams = dl.getAllTeams(y)
			elif(args.db == 'o'):
				dl = Data_Loader('balancedData.csv')
				teams = dl.getAllTeams(y)
			total_tested += len(teams)
			total_error = 0.0
			for t in teams:
				t.result = nn.feed_forward(t.stats)
				error = (find_error(t.result, encode(t.classification)))
				total_error += error**2
				if error < .08:
					correct += 1
					classRight
				if args.v:
					print "team %s, results %s, class %s, error %s" % (t.name, t.result, encode(t.classification), error)
			if not args.q:
				print "%d \t within threshold: %d/%d \t error: %s" % (y, correct, len(teams), str(total_error))
			totalCorrect += correct
		print "totalCorrect: %i/%i, %.2f%%" % (totalCorrect, total_tested, (totalCorrect/total_tested)*100)
	except Exception as e:
		print "invalid formatting, consult neural_main.py c --help \nError: %s" % e

def show_teams(args):
	for d in sorted(team_dict.teams.items(),key=lambda (k,v): v):
		print "%s: %s" % d

parser = argparse.ArgumentParser(description='Predict NFL playoff results with OR train a neural network on NFL results')

subparsers = parser.add_subparsers(help='Possible Actions')

'''
Create a parser for the train command, specified with 't'
'''
parser_train = subparsers.add_parser('t',help='train a NN over start-end years for e epochs')
parser_train.add_argument('nodes',type=int,help='number of hidden nodes')
parser_train.add_argument('db',type=str,help='data balancing method, u: unbalanced, o: oversampled, b:undersampled, p:playoffTeams, s: Borderline SMOTE-(RECOMMENDED)',choices="uobps")
parser_train.add_argument('start',type=int,help='starting year to train on')
parser_train.add_argument('end',type=int,help='ending year')
parser_train.add_argument('epochs',type=int,help='number of epochs to train for')
parser_train.add_argument('learn_rate',type=float,help='the NN learning rate')
parser_train.add_argument('file',type=str,help='NN output file')
# set the function to be called when this parses is used
parser_train.set_defaults(func=train)

'''
Create a parser for the cross_validate command, specified with 'c'
'''
parser_cross = subparsers.add_parser('c',help='compare predicted outcomes with actual outcomes')
parser_cross.add_argument('start',type=int,help='starting year to train on')
parser_cross.add_argument('end',type=int,help='ending year')
parser_cross.add_argument('db',type=str,help='data balancing method, u: unbalanced (RECOMMENDED), p:playoffTeams',choices="up")
parser_cross.add_argument('file',type=str,help='NN input file')
parser_cross.add_argument('-v',action='store_true',help='the results of every team in validation')
parser_cross.add_argument('-q',action='store_true',help='only the final results')
# set the function to be called when this parses is used
parser_cross.set_defaults(func=cross_validate)

'''
Create a parser for the predict command, specified with 'p'
'''
parser_pred = subparsers.add_parser('p',help='predict the given team\'s based on the given NN')
parser_pred.add_argument('team',type=str,help='team to predict')
parser_pred.add_argument('year',type=int,help='year to predict')
parser_pred.add_argument('file',type=str,help='NN file to load')
parser_pred.add_argument('-se','--show_expected',action='store_true',help='show the target value (useful for validation)')
# set the function to be called when this parser is used
parser_pred.set_defaults(func=predict)

'''
parser for showing teams
'''

parser_teams = subparsers.add_parser('teams',help='show the team codes')
parser_teams.set_defaults(func=show_teams)
args = parser.parse_args()
args.func(args)
