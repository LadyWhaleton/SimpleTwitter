# this file stuff shared across client and server

# =====================================================
# flags for optionNum
VIEW = '1'
SEARCH = '2'
EDIT = '3'
POST = '4'
LOGOUT = '5'


# Message class
class Message:
	def __init__ (self, body, tags, timestamp):
		self.body = body
		self.tags = tags
		self.timestamp = timestamp

