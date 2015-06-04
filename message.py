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
