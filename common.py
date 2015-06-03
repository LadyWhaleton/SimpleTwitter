# this file stuff shared across client and server

# =====================================================
# flags for optionNum
VIEW = '1'
SEARCH = '2'
EDIT = '3'
POST = '4'
LOGOUT = '5'

UNREAD = 'unread'
READ = 'read'

# Message class
class Message:
	def __init__ (self, author, body, tags, timestamp, id):
		self.author = author
		self.body = body
		self.tags = tags
		self.timestamp = timestamp
		self.id = id
		self.isRead = UNREAD

	def setRead():
		self.isRead = READ

