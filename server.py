import socket
import struct
import os
import sys
import time
from thread import*
from common import *

# time.asctime(time.localtime(time.time()))
# http://python.readthedocs.org/en/latest/howto/curses.html

class User:
	def __init__ (self, username, pw):
		self.username = username
		self.pw = pw
		self.isOnline = False
		self.subs = []
		self.msg_read = []
		self.msg_unread = []

def subscribe(user, name, conn):
	for subUser in userList:
		# if the subcription username exists
		if subUser.username == name:
			# check the user already subscribed to this person
			for subName in subUser.subs:
				# if the name already exists in the list of subs, return
				if subName == name:
					return
			# only arrive here if name doesn't exist, OK to subscribe
			user.subs.append(name)
			return
			
			

# determines whether or not the user exists	and does stuff
# used for Deleting a subscription	
def unsubscribe(user, name, conn):
	for u in userList:
		if u.username == name:
			x = 0
	return " "

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
				msg = '1 ' + str(len(user.msg_unread))
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

# serverside ViewOffline
def serverView(user, conn):
	print 'View Offline Messages'

# serverside SearchByHashTag	
def serverSearch(user, conn):
	print "Searching by Hashtags"

# serverside EditSubs
def serverEdit(user, conn):
	# send the number of people the user is subscribed to
	numFollowing = len(user.subs)
	print str(numFollowing)
	conn.send(str(numFollowing))
	
	# Loop 
	while True:
		# wait for client input
		option = recv(1024)
		
		if option == '1':
			username = recv(1024)
			
			
			if tempFlag == True:
				conn.send('1')
				 
			
			# conn.send('1' if userExists(username) else '0')
			
		elif option == '2'
			# send subscriptions
			for i in range(0, numFollowing):
				currUser = user.subs[i]
				conn.send(str(i+1) + " " + currUser.username)
				
			# wait for user to select 
		
		elif option == '~':
			return

def serverPost(user, conn):
	print 'User wants to post a message.'

# serverside logout
def serverLogout(user, conn, addr):
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
			serverView(currUser, conn)
			
		elif optionNum == SEARCH: 
			serverSearch(currUser, conn)
			
		elif optionNum == EDIT: 
			serverEdit(currUser, conn)
			
		elif optionNum == POST:
			serverPost(currUser, conn)
			
		elif optionNum == LOGOUT: 
			serverLogout(currUser, conn, addr)
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
