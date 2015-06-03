SHUTDOWN = 'shutdown'
userList = []

class User:
	def __init__ (self, username, pw):
		self.username = username
		self.pw = pw
		self.isOnline = False
		self.subscriptions = []
		self.followers = []
		self.myEchoes = []
		self.msg_all = []
		self.msg_unread = []

def initUserList():
	userList.append( User ("abc", "abc") )
	userList.append( User ("pizza", "cheese") )
	userList.append( User ("apple", "sauce") )
	
def addUser(name, pw):
	newUser = User(name, pw)
	userList.append(newUser)

