#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from re import compile, search

for year in range(1970,2013):
	html = urlopen("http://www.pro-football-reference.com/years/%i/" % year).read()
	soup = BeautifulSoup(''.join(html))
	team_urls = soup.findAll("a",href=True)
	def find_teams(hf):
		return search("teams.*htm.{7,}$", str(hf))	

	team_url_set = set()
	for tu in filter(find_teams, team_urls):
		#print tu
		team_url_set.add(str(tu))
	
	team_url_dict = {}
	for team in team_url_set:
		data = search("\"(.*)\">(.*)</a>", team).groups()
		team_url = data[0]
		team_name = data[1]
		team_url_dict[team_name] = team_url

	f = open("%i.txt" % year,'w')
	for team in team_url_dict.keys():
		html = urlopen("http://www.pro-football-reference.com" + team_url_dict[team])
		soup = BeautifulSoup(''.join(html))
		team_game_log_soup = soup.findAll('table', id = 'team_gamelogs')
		win_count = 0
		playoffs = False
		round = ''
		body = team_game_log_soup[0].findAll('tbody')
		for games in body:
			for stuff in games.contents:
				if not playoffs:
					if search(">W<", str(stuff)):
						#print "STUFF:" + str(stuff)
						win_count += 1
					elif search(">L<", str(stuff)):
						win_count = 0
					elif search("Playoffs", str(stuff)):
						playoffs = True
				else:
					if search("WildCard", str(stuff)):
						round = "WildCard"
					elif search("Division", str(stuff)):
						round = "Division"
					elif search("ConfChamp", str(stuff)):
						round = "ConfChamp"
					elif search("SuperBowl", str(stuff)):
						if search(">W<", str(stuff)):
							round = "Champions"
						else:
							round = "SuperBowl"
		#print team + "," + str(win_count) + "," + round +  "\n"
		f.write(team + "," + str(win_count) + "," + round +  "\n")
	f.close()
	print str(year) + " Complete!"
