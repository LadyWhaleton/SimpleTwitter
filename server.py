import socket
import sys
import time
from thread import*

# time.asctime(time.localtime(time.time()))

class User:
	def __init__ (self, username, pw):
		self.username = username
		self.pw = pw
		self.online = False
		self.subs = []
		self.msg_read = []
		self.msg_unread = []

def validateUser(conn, addr):
	
	validUser = False
	
	while not(validUser):
		username = conn.recv(1024)
		pw = conn.recv (1024)
	
		for user in userList:
			if user.username == username and user.pw == pw:
				print 'Client ' + addr[0] + ':' + str(addr[1]) + ', ' + username + ' is authorized.'
				validUser = True
				conn.send ('1')
				return username

		if not(validUser):
			print 'Client' + addr[0] + ':' + str(addr[1]) + ', ' + username + 'unauthorized user.'
			conn.send ('0') 
			

			
	
# initializes list of users
def serverSetup():
	userList.append( User ("abc", "abc") )
	userList.append( User ("pizza", "cheese") )
	userList.append( User ("apple", "sauce") )

def handleClient(conn, addr):
	# Sending message to client
	conn.send ('Welcome to SimpleTwitter. Please log in.')

	currUser = validateUser(conn, addr)

	conn.close()

# ======================== M A I N ===============================
HOST = ''
PORT = 2124

sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# try to bind the socket
try:
	sock.bind ( (HOST, PORT) )
except socket.error , msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind success'

messageNum = 0
oldPacket = ""
newPacket = ""
userList = []
onlineUsers = []
clientList = []

serverSetup()

# now we listen for any incoming connections
sock.listen(10)

print 'Socket now listening'
	
while 1:
	# wait to accept a connection
	conn, clientAddr = sock.accept()
	clientList.append(conn)	
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(clientAddr[1])

	# start a new thread
	start_new_thread(handleClient, (conn, clientAddr) )		

sock.close()
