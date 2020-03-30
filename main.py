import json
import requests
import re
import time
from datetime import datetime
from prettytable import PrettyTable

def team_info():
	team_response = requests.get('https://api.footystats.org/league-teams?key=test85g57&include=stats&league_id=1625')
	# accessing team list
	with open('data.json', 'w') as outfile:
		json.dump(team_response.json(), outfile, sort_keys=True, indent=4)
	
def match_info():
	match_response = requests.get('https://api.footystats.org/league-matches?key=test85g57&league_id=1625')
	# accessing matches list
	with open('match.json', 'w') as outfile:
		json.dump(match_response.json(), outfile, sort_keys=True, indent=4)

def scores_info():
	scores_response = requests.get('https://api.footystats.org/league-tables?key=test85g57&season_id=1625')
	# accessing scores list
	with open('scores.json', 'w') as outfile:
		json.dump(scores_response.json(), outfile, sort_keys=True, indent=4)


def data_receiving():
	try:
		team_info()
		match_info()
		scores_info()
		print('Information loaded successfuly!\nPlease, enter your query\nIf you want to input a date, please do it in this format: Month.Day.Year')
	except:
		print('Something went wrong.\nPlease relaunch the program with help of Ctrl+D\n')


def input_rendering():
	req = str(input())
	flag = re.findall(r'\d{2}[.]\d{2}[.]\d{4}', req)
	if len(flag)==0:
		if req == "table":
			with open('scores.json', 'r') as infile:
				data = json.load(infile)
				with open('data.json', 'r') as tfile:
					tdata = json.load(tfile)
					points = {}
					for i in range (len(data['data']['all_matches_table_overall'])):
						points.update({str(data['data']['all_matches_table_overall'][i]['cleanName']):int(data['data']['all_matches_table_overall'][i]['points'])})
						sort = sorted(points.items(), key=lambda x: -x[1])

					th = ['Place', 'Name', 'Number of games', 'Number of wins', 'Number of draws', 'Number of losses', 'Goal difference', 'Pts']
					table = PrettyTable(th)
					for i in range (len(data['data']['league_table'])):
						td = [i+1, str(data['data']['league_table'][i]['cleanName']), data['data']['league_table'][i]['matchesPlayed'], tdata['data'][i]['stats']['seasonWinsNum_overall'], tdata['data'][i]['stats']['seasonDrawsNum_overall'], tdata['data'][i]['stats']['seasonLossesNum_overall'], tdata['data'][i]['stats']['seasonGoalDifference_overall'], data['data']['league_table'][i]['points']]
						table.add_row(td)
			print(table)
			print('\n')
		else:
			with open('data.json', 'r') as infile:
				data = json.load(infile)
				teams=[]
				for i in range (len(data['data'])):
					teams.append(str(data['data'][i]['cleanName']))
				if req in teams:
					print('\nHere is some information about '+req+':')
					with open('match.json', 'r') as mfile:
						th = ['Guest team', 'Score', 'Home team', 'Date']
						info = PrettyTable(th)
						mdata = json.load(mfile)
						for i in range (len(mdata['data'])):
							if req == str(mdata['data'][i]['away_name']) or req == str(mdata['data'][i]['home_name']):
								td = [ str(mdata['data'][i]['away_name']), str(mdata['data'][i]['awayGoalCount'])+':'+str(mdata['data'][i]['homeGoalCount']), str(mdata['data'][i]['home_name']), datetime.utcfromtimestamp(int(mdata['data'][i]['date_unix'])).strftime('%m.%d.%Y')]
								info.add_row(td)
						print(info)
					print('\n')
				else:
					print('\nSomething gone wrong :(\n\nHere is a list of teams:')
					for i in range (len(data['data'])):
						print(str(data['data'][i]['cleanName']))
					print('\nPlease, try again\n')
	else:
		dates = []
		with open('match.json', 'r') as mfile:
			mdata = json.load(mfile)
			for i in range (len(mdata['data'])):
				dates.append(str(datetime.utcfromtimestamp(int(mdata['data'][i]['date_unix'])).strftime('%m.%d.%Y')))
			if req in dates:
				print("\nHere are all matches on that day:")
				th = ['Guest team', 'Score', 'Home team']
				matches = PrettyTable(th)
				for i in range (len(dates)):
					if str(datetime.utcfromtimestamp(int(mdata['data'][i]['date_unix'])).strftime('%m.%d.%Y')) == req:
						td = [str(mdata['data'][i]['away_name']), str(mdata['data'][i]['awayGoalCount'])+':'+str(mdata['data'][i]['homeGoalCount']), str(mdata['data'][i]['home_name'])]
						matches.add_row(td)
				print(matches)				
				print('\n')
			else:
				print("\nThere are no matches on that day")

if __name__ == "__main__":
	print('We are loading statistic, please wait...')
	data_receiving()
	while True:
		input_rendering()
