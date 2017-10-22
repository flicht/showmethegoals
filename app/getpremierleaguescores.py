#try and rewrite using classes? good learning exercise
import requests
import bs4
import praw
import sys

client_id = 'CO8F17n36tkXeg'
client_secret = 'PsMWW7027eHFMyMzeJPLaEJ5h_U'
user_agent = 'my user agent'
team = 'manchester united'
team_replace = team.replace( ' ', '-')
team_subreddit = 'reddevils'
link = "http://www.livescores.com/soccer/england/premier-league"
league = "premier-league"

dict_of_subreddits = {
	'afc bournemouth': '',
	'arsenal' 				: 'gunners',
	'brighton & hove albion': '',
	'burnley'				: '',
	'chelsea' 				: 'chelseafc',
	'crystal palace'		: 'crystalpalace',
	'everton'				: 'everton',
	'huddersfield town'		: '',
	'leicester city'		: 'lcfc',
	'liverpool'				: 'liverpoolfc',	
	'manchester united' 	: 'reddevils',
	'manchester city' 		: 'mcfc',
	'newcastle united'		: 'nufc',
	'southampton'			: '',
	'stoke city'			: '',	
	'swansea city'			: '',
	'tottenham hotspur'		: 'coys',
	'watford'				: '',
	'west bromwich albion'	: '',
	'west ham united'		: 'hammers',

	}

def getLiveScores(link=link):
	res = requests.get(link)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	return soup


def getPremierLeagueLinks(soup, league=league):
	links = soup.select('.row-gray') #find_all('div', attrs={'dat-type': 'evt'}).select('a') # alternatively can use data-type = evt
	list_of_links = []


	for i in range(len(links)):
		try:
			list_of_links.append(links[i].select('a')[0]['href']) #list of links that lead to the matches
		except IndexError:
			pass
	
	matches = [x for x in list_of_links if league in x] #to get the match you want change team as a global variable. maybe later could do all premier league matches? or all matches?

	return matches

def getSoupFromLink(match):
	try:
		res = requests.get("http://www.livescores.com" + match)
		soup=bs4.BeautifulSoup(res.text, 'html.parser')
	except IndexError:
		print 'No link match'

		
	return soup


def getArsenalGame(soup, ):
	links = soup.select('.row-gray') #find_all('div', attrs={'dat-type': 'evt'}).select('a') # alternatively can use data-type = evt
	list_of_links = []

	for i in range(len(links)):
		try:
			list_of_links.append(links[i].select('a')[0]['href']) #list of links that lead to the matches
		except IndexError:
			pass

	matches = [x for x in list_of_links if 'premier' in x and team_replace in x] #to get the match you want change team as a global variable. maybe later could do all premier league matches? or all matches?
	
	try:
		res = requests.get("http://www.livescores.com" + matches[0])
	except IndexError:
		print 'No link match'

	soup=bs4.BeautifulSoup(res.text, 'html.parser')
	return soup

def getTheGoalscorers(soup):
	teams_goalscorers = [ [], [] ]
	rows = soup.select(".row-gray")
	home_team = soup.select('.row')[0].select('.ply')[0].getText()
	away_team = soup.select('.row')[0].select('.ply')[1].getText()
	teams_goalscorers[0].append(home_team)
	teams_goalscorers[1].append(away_team)

	for i in range(len(rows)):
		if rows[i].select(".goal") != []:
			if rows[i].select('.name')[0].getText() == '':
				teams_goalscorers[1].append(rows[i].select(".name")[1].getText())
			else:
				teams_goalscorers[0].append(rows[i].select(".name")[0].getText())


	return teams_goalscorers #goalscorers [[home_team, home goalscorers],[away_team, away goalscorers]]










# def printTheScores(soup):
# 	array_of_goalscorers = []
# 	print soup.select('.row')[0].getText()
# 	i=1
# 	scorers = []
# 	#print str(soup.select('.row-gray')[3])
	
# 	while 'min' in str(soup.select('.row-gray')[i]):
# 		print soup.select('.row-gray')[i].getText()
# 		i+=1	
	
# 	for j in range(i):
# 		if 'yellowcard' not in 	str(soup.select('.row-gray')[j]):
# 			a = soup.select('.row-gray')[j].select('.name')
# 			scorers.append(a)
			
# 	for i in range(1,len(scorers)):
# 		if scorers[i][0].getText() != '':
# 			array_of_goalscorers.append([scorers[i][0].getText(), True])
# 		else:
# 			array_of_goalscorers.append([scorers[i][1].getText(), False])


# 	teams = [soup.select('.row')[0].select('.ply')[0].getText(), soup.select('.row')[0].select('.ply')[1].getText()]
# 	return [array_of_goalscorers, teams]

	#print soup.find_all('div', attrs={'data-type' : 'tab'})

# def getGoalFromReddit(array_of_goalscorers,teams):
# 	if team.lower() in teams[0].lower():
# 		vs_team = teams[1].lower()
# 	else:
# 		vs_team = teams[0].lower()

# 	goalscorers = []
# 	reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent=user_agent)
# 	for goalscorer in array_of_goalscorers:
# 		if goalscorer[1] == True:
# 			goalscorers.append(goalscorer[0])

# 	for scorer in goalscorers:			
# 		for sub in reddit.subreddit(team_subreddit).search( scorer.split()[1] + ' ' + vs_team , sort='new', time_filter='month'):
# 			if len(sub.title) < 70 and 'reddit' not in sub.url:
# 				print sub.url, sub.title

def getGoalLinksFromReddit(array_of_teams_goalscorers):
	home_team = array_of_teams_goalscorers[0][0]
	away_team = array_of_teams_goalscorers[1][0]
	home_goalscorers = array_of_teams_goalscorers[0][1:]
	away_goalscorers = array_of_teams_goalscorers[1][1:]

	stream_links_and_titles = [[home_team],[away_team]]

	if len(home_team.split()[0]) < 4:
		home_team = home_team.split()[1]


	if len(away_team.split()[0]) < 4:
		away_team = away_team.split()[1]

	reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent=user_agent)
	max_title_length = 80

	

	for scorer in home_goalscorers:

		if 'oe' in scorer:
			scorer = scorer.replace('oe','o')
		if 'ue' in scorer:
			scorer = scorer.replace('ue','u')
		posts = reddit.subreddit('soccer').search( scorer.split()[-1] + ' ' + away_team.split()[0], sort='new', time_filter='month')
		

		# if dict_of_subreddits[home_team.lower()] != '':
		# 	team_subreddit_posts = reddit.subreddit(dict_of_subreddits[home_team.lower()]).search( scorer.split()[-1] + ' ' + away_team, sort='new', time_filter='month')
		# 	for post in team_subreddit_posts:
		# 		if len(post.title) < max_title_length:
		# 			stream_links_and_titles[0].append([post.title,post.url])
		
		for post in posts:
			if len(post.title) < max_title_length:
				stream_links_and_titles[1].append([post.title, post.url])

	for scorer in away_goalscorers:
		if 'oe' in scorer:
			scorer = scorer.replace('oe','e')


		if 'ue' in scorer:
			scorer = scorer.replace('ue','e')
		posts = reddit.subreddit('soccer').search( scorer.split()[-1] + ' ' + home_team.split()[0], sort='new', time_filter='month')

		
		# if dict_of_subreddits[away_team.lower()] != '':
		# 	team_subreddit_posts = reddit.subreddit(dict_of_subreddits[away_team.lower()]).search( scorer.split()[-1] + ' ' + home_team, sort='new', time_filter='month')
		# 	for post in team_subreddit_posts:
		# 		if len(post.title) < max_title_length:
		# 			stream_links_and_titles[1].append([post.title,post.url])

		for post in posts:
			if len(post.title)< max_title_length:
				stream_links_and_titles[1].append([post.title, post.url])


	return stream_links_and_titles ##[[home_team, home goalscorers links],[away_team, away goalscorers links]]

def main():
	client_id = 'CO8F17n36tkXeg'
	client_secret = 'PsMWW7027eHFMyMzeJPLaEJ5h_U'
	user_agent = 'my user agent'
	soup = getLiveScores()
	#a = printTheScores(getArsenalGame(getLiveScores()))
	#getGoalFromReddit(a[0],a[1])

	prem_links = getPremierLeagueLinks(soup)

	check_duplicate = []

	for game in prem_links:
		mug_of_soup = getSoupFromLink(game)
		teams_goalscorers = getTheGoalscorers(mug_of_soup)
		
		game_links = getGoalLinksFromReddit(teams_goalscorers) ##[[home_team,  [title,url], ... ],[away_team, [title,url], ... ,]]

		print game_links[0][0] +' vs. ' + game_links[1][0] #print teams
		for i in range(2):
			
			for goal in game_links[i][1:]:
				if 'imgtc' in goal[1] or 'streamable' in goal[1]:	
					if goal[1] in check_duplicate:
						pass
					else:
						check_duplicate.append(goal[1])
						print '\t' + goal[0] + ' ' + '-' + ' ' + goal[1] 	
				else:
					pass



if __name__ == '__main__':
	main()





