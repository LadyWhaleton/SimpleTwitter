ONLINE = True
OFFLINE = False

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
myList = {NAME1:USER1, NAME2:USER2, NAME3:USER3, NAME4:USER4}
