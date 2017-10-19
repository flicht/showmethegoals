from app import app
from flask import render_template
from getpremierleaguescores import *

@app.route('/')
@app.route('/index')
def index():

	client_id = 'CO8F17n36tkXeg'
	client_secret = 'PsMWW7027eHFMyMzeJPLaEJ5h_U'
	user_agent = 'my user agent'
	soup = getLiveScores()
	#a = printTheScores(getArsenalGame(getLiveScores()))
	#getGoalFromReddit(a[0],a[1])

	prem_links = getPremierLeagueLinks(soup)
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
	
	return render_template('index.html',
							title = 'ShowMeTheGoals',
							subheader = 'A work in progress',
							links = display_links)