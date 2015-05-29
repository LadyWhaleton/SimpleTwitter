import socket
import struct
import os
import sys
import time
from thread import*
from common import *

# time.asctime(time.localtime(time.time()))

class User:
	def __init__ (self, username, pw):
		self.username = username
		self.pw = pw
		self.isOnline = False
		self.subs = []
		self.msg_read = []
		self.msg_unread = []
		self.numUnread = 0

def validateUser(conn, addr):
	
	validUser = False
	
	while not(validUser):
		username = conn.recv(1024)
		pw = conn.recv (1024)
		
		for user in userList:
			if user.username == username and user.pw == pw:
				print 'Client ' + addr[0] + ':' + str(addr[1]) + ', ' + username + ' is authorized.'
				validUser = True
				user.isOnline = True
				msg = '1 ' + str(user.numUnread)
				conn.send (msg) 
				return user

		if not(validUser):
			print 'Client' + addr[0] + ':' + str(addr[1]) + ', ' + username + 'unauthorized user.'
			conn.send ('0') 
			
	
# initializes list of users
def serverSetup():
	userList.append( User ("abc", "abc") )
	userList.append( User ("pizza", "cheese") )
	userList.append( User ("apple", "sauce") )

# serverside logout
def logout(user, conn, addr):
	user.isOnline = False
	print user.username + " is logging out."
	conn.close()
	
def handleClient(conn, addr):
	# Sending message to client
	conn.send ('Please log in.')
	
	# Validate the user
	currUser = validateUser(conn, addr)
	
	UserLogout = False
	
	# Infinite loop
	while (not(UserLogout)):
		# Waiting for user command
		optionNum = conn.recv(1024)
		
		if optionNum == VIEW:
			print 'View Offline Messages'
		elif optionNum == SEARCH: 
			print 'Search by Hashtag'
		elif optionNum == EDIT: 
			print 'Edit Subscriptions'
		elif optionNum == POST:
			print 'Post a Message'
		elif optionNum == LOGOUT: 
			logout(currUser, conn, addr)
			UserLogout = True


# ======================== M A I N ===============================
HOST = ''
PORT = 2124

os.system ('clear')

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

# Maybe make a admin thread????
	
while 1:
	# wait to accept a connection
	conn, clientAddr = sock.accept()
	clientList.append(conn)	
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(clientAddr[1])

	# start a new thread
	start_new_thread(handleClient, (conn, clientAddr) )		

sock.close()
