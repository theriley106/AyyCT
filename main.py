# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import bs4
import re

class act(object):
	def __init__(self, username, password):
		self.session = requests.Session()
		self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.loginReddit(username, password)
		for e in self.returnAllTitle():
			solved = self.solvePostTitle(e["Title"])
			if solved == 36 or '36' in str(e["Title"]):
				print("Upvoting {}".format(e["Title"]))
				self.upvote(e["PostID"], e["Rank"])
	def loginReddit(self, username, password):
		data = {"op":"login-main", "user":username, "passwd": password, "api_type": "json"}
		a = self.session.post('https://www.reddit.com/api/login/{}'.format(username), data=data)
		a = self.session.get('https://www.reddit.com/')
		page = bs4.BeautifulSoup(a.text, "lxml")
		try:
			print "Logged in as {}".format(page.select(".user a")[0].getText())
		except:
			print "Wrong Password Bruh..."
			sys.exit()
	def returnAllTitle(self):
		listOfTitles = []
		r = self.session.get('https://www.reddit.com/r/ACT/new/')
		self.voteHash = str(r.text).partition('"vote_hash": "')[2].partition('"')[0]
		self.UH = str(r.text).partition('name="uh" value="')[2].partition('"')[0]
		page = bs4.BeautifulSoup(r.text, "lxml")
		for i, e in enumerate(page.select("#siteTable .loggedin")):
			try:
				PostID = 't3_' + str(e).partition('/comments/')[2].partition('/')[0]
				Title = e.getText()
				listOfTitles.append({"Rank": i, "PostID": PostID, "Title": Title})
			except Exception as exp:
				pass
		return listOfTitles
	def solvePostTitle(self, title):
		a = re.findall('[\d\(\)\+\-\*\/]', str(title))
		if a != None:
			equation = ''.join(a)
			try:
				solved = eval(equation)
				return solved
			except:
				pass
		return None

	def upvote(self, postID, rank):
		data = {"id":postID, "dir":"1","vh": self.voteHash, "isTrusted": "true", "vote_event_data":'{"page_type":"listing","sort":"hot"}', 'rank':rank, 'r':'ACT', 'uh':self.UH, 'renderstyle':'html'}
		url = 'https://www.reddit.com/api/vote?dir=1&id={}&sr=ACT'.format(postID)
		self.session.post(url, data=data)

if __name__ == "__main__":
	username = raw_input("Username: ")
	password = raw_input("Password: ")
	a = act(username, password)