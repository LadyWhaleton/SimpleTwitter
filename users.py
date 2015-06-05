ONLINE = True
OFFLINE = False

class User:
	def __init__ (self, username, pw):
		self.username = username
		self.pw = pw
		self.status = OFFLINE
		self.port = -1
		self.subscriptions = []
		self.followers = []
		self.myEchoes = []
		self.msg_all = []	#all messages from all my subcriptions
		self.msg_unread = []	#unread messages from my subcriptions
	
	def goOnline(self, echo_conn):
		self.status = ONLINE
		self.port = echo_conn
	
	def goOffline(self):
		self.status = OFFLINE
		self.port = -1
		
	def follow(self, otherUser):
		if self.username == otherUser:
			return -1, 'Error: You cannot follow yourself!\n'
		
		# check if you're already following someone	
		for subName in self.subscriptions:
			if subName == otherUser:
				return -1, 'Error: ' + self.username + ' already following' + otherUser +'\n'
		
		if not(UserList.has_key(otherUser)):
			return -1, 'Error: ' + otherUser + ' does not exist in user database!\n'

		self.subscriptions.append(otherUser)
		UserList[otherUser].addFollower(self.username)
		return 1, 'You are now following ' + otherUser+ '\n'
		
	def unfollow(self, otherUser):
		self.subscriptions.remove(otherUser)
		
	def addFollower(self, otherUser):
		self.followers.append(otherUser)
		
	def removeFollower(self, user):
		self.followers.remove(user)
		
	def addMyEcho(self, newEcho):
		self.myEchoes.insert(0, newEcho)
		
	def addUnread(self, msg):
		self.msg_unread.insert(0, msg)
	
	def isFollowing(self, otherUser):
		otherUserFollowers = UserList[otherUser].followers
		for name in otherUserFollowers:
			# if you found your name om the otherUser's followers
			if self.username == name:
				return True

		return False

	def echoToFollowers(self, message):
		for follower in self.followers:
			if UserList[follower].status == ONLINE:
				followerPort = UserList[follower].port
				followerPort.send('\n' + message.formatMessage())

			else:
				UserList[follower].addUnread(message)			
	
NAME1 = "Wailord"
NAME2 = "Orca"
NAME3 = "abc"
NAME4 = "Taigo"
		
USER1 = User(NAME1, "whales92")
USER2 = User(NAME2, "killGelimer")
USER3 = User(NAME3, "abc")
USER4 = User(NAME4, "squirrels")

# dictionary for user status (key=username : value=status)
userStatus = {NAME1:OFFLINE, NAME2:OFFLINE, NAME3:OFFLINE, NAME4:OFFLINE}

# other dictionaries
userConnections = {NAME1:-1, NAME2:-1, NAME3:-1, NAME4:-1}
UserList = {NAME1:USER1, NAME2:USER2, NAME3:USER3, NAME4:USER4}
userList = [NAME1, NAME2, NAME3, NAME4]

# sample usages
# print UserList["Wailord"].pw
# dict.has_key(key) returns true or false
