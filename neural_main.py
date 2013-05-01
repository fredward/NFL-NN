from neural_network import Neural_Network
from data_loader import Data_Loader
from nfl_predictor import NFL_Predictor
'''
A main file, for directing user input from the highest level. Will load and use
all our other classes
'''



import argparse


def train(args):
	try:
		nn = Neural_Network.createWithRandomWeights(66,args.nodes,6)
		inputs = []
		targets = []
		y = range(args.start,args.end+1)
		if(args.db == 'u'):
			dl = Data_Loader()
			i,t = dl.getTargets(y)
		elif(args.db == 'b'):
			dl = Data_Loader()
			i,t = dl.getBalancedTargets(y)
		elif(args.db == 'o'):
			dl = Data_Loader('balancedData.csv')
			i,t = dl.getTargets(y)
		elif(args.db == 's'):
			dl = Data_Loader()
			print 'Creating SMOTE targets...'
			i,t = dl.getSmoteTargets(y)
		print t
		inputs += i
		targets += t
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
		teams = dl.getAllTeams(args.year)
		for team in teams:
			print "RESULTS: %s \n EXPECTED: %s" % (nn.feed_forward(team.stats), dl.encode(team.classification))
		post_processor = NFL_Predictor(nn)
		similar_teams = post_processor.compareWithPastTeams(dl.getEveryTeam(), team, 15)
		for t in similar_teams:
			print "%s \tScore: %f" % t
	except Exception as e:
		print "invalid formatting, consult neural_main.py t --help \n Error: %s" % e


parser = argparse.ArgumentParser(description='Predict NFL playoff results with OR train a neural network on NFL results')

subparsers = parser.add_subparsers(help='Possible Actions')

'''
Create a parser for the train command, specified with 't'
'''
parser_train = subparsers.add_parser('t',help='train a NN over start-end years for e epochs')
parser_train.add_argument('nodes',type=int,help='number of hidden nodes')
parser_train.add_argument('db',type=str,help='data balancing method, u: unbalanced, o: oversampled, b:undersampled, s: SMOTE (not implemented)',choices="uobs")
parser_train.add_argument('start',type=int,help='starting year to train on')
parser_train.add_argument('end',type=int,help='ending year')
parser_train.add_argument('epochs',type=int,help='number of epochs to train for')
parser_train.add_argument('learn_rate',type=float,help='the NN learning rate')
parser_train.add_argument('file',type=str,help='NN output file')
# set the function to be called when this parses is used
parser_train.set_defaults(func=train)

'''
Create a parser for the predict command, specified with 'p'
'''
parser_pred = subparsers.add_parser('p',help='predict the given team\'s based on the given NN')
parser_pred.add_argument('team',type=str,help='team to predict')
parser_pred.add_argument('year',type=int,help='year to predict')
parser_pred.add_argument('file',type=str,help='NN file to load')
# set the function to be called when this parser is used
parser_pred.set_defaults(func=predict)

args = parser.parse_args()
args.func(args)
