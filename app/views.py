from app import app
from flask import render_template
from getpremierleaguescores import *

def display_everything(link="http://www.livescores.com/soccer/england/premier-league", league="premier-league"):
	soup = getLiveScores(link)
	#a = printTheScores(getArsenalGame(getLiveScores()))
	#getGoalFromReddit(a[0],a[1])

	prem_links = getPremierLeagueLinks(soup,league)
	display_links = []
	check_duplicate = []
	for game in prem_links:
		output_links = []
		mug_of_soup = getSoupFromLink(game)
		teams_goalscorers = getTheGoalscorers(mug_of_soup)
		
		goal_links = getGoalLinksFromReddit(teams_goalscorers)
		fixture = goal_links[0][0] +' vs. ' + goal_links[1][0]
		output_links.append(fixture)
		for i in range(2):
			
			for goal in goal_links[i][1:]:
				if 'imgtc' in goal[1] or 'streamable' in goal[1]:	
					if goal[1] in check_duplicate:
						pass
					else:
						check_duplicate.append(goal[1])
						output_links.append([goal[0],goal[1]]) 
							
				else:
					pass
		display_links.append(output_links)
	
	return display_links



@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',
							title = 'ShowMeTheGoals',
							subheader = 'A work in progress',
							links = display_everything())



@app.route('/europa-league')
def europa_league():
	return render_template('index.html',
							title = 'ShowMeTheGoals',
							subheader = 'A work in progress',
							links = display_everything("http://www.livescores.com/soccer/europa-league","europa-league"))


@app.route('/champions-league')
def champions_league():
	return render_template('index.html',
							title = 'ShowMeTheGoals',
							subheader = 'A work in progress',
							links = display_everything("http://www.livescores.com/soccer/champions-league", "champions-league"))

@app.route('/league-cup')
def league_cup():
	return render_template('index.html',
							title = 'ShowMeTheGoals',
							subheader = 'A work in progress',
							links = display_everything("http://www.livescores.com/soccer/england/carling-cup","carling-cup"))


	

	
