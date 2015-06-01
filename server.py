import socket
import struct
import string
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
		self.subscriptions = []
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

def subscribe(user, conn):
	otherName = conn.recv(1024)
	
	# you can't subscribe to yourself!
	if user.username == otherName:
		conn.send('Error: You cannot subscribe to yourself!\n')
		return
	
	for subUser in userList:
		# if the subcription username exists
		if subUser.username == otherName:
			# check the user already subscribed to this person
			
			for subName in subUser.subscriptions:
				# if the name already exists in the list of subs, return
				if subName == otherName:
					conn.send('Error: ' + user.username + ' already subscribed to' + otherName +'\n') 
					return
					
			# only arrive here if otherName isn't in sublist, OK to subscribe
			user.subscriptions.append(otherName)
			conn.send('Successfully subscribed to ' + otherName + '\n')
			return
	
	conn.send('Error: ' + otherName + ' does not exist!\n')
			
# determines whether or not the user exists	and does stuff
# used for Deleting a subscription	
def unsubscribe(user, conn, numFollowing):
	# send subscriptions
	for i in range(0, numFollowing):
		currUser = user.subscriptions[i]
		conn.send(str(i+1) + ". " + currUser)
	
	# wait for user to select
	userToRemove = conn.recv(1024)
	
	if not(userToRemove.isdigit()):
		conn.send('Error: Invalid selection!\n')
		return

	if  0 < int(userToRemove) and int(userToRemove) <= numFollowing:
		# ask if client really wants to unsubscribe
		conn.send('unsubscribe check')
		
		clientChoice = conn.recv(1024)
		otherUser = user.subscriptions[int(userToRemove)-1]
		
		if clientChoice == 'y' or clientChoice == 'Y':
			# search user's list of subscriptions and remove
			
			user.subscriptions.remove(otherUser)
			conn.send ('Successfully unsubscribed from ' + otherUser + '.\n')
		else:
			conn.send('You did not unsubscribe from ' + otherUser + '.\n')
	
	else:
		conn.send('Error: Invalid selection!\n')
	
# serverside EditSubs
def serverEdit(user, conn):
	# send the number of people the user is subscribed to
	numFollowing = len(user.subscriptions)
	conn.send(str(numFollowing))
	
	# Loop 
	while True:
		
		# wait for client input
		option = conn.recv(1024)
		
		if option == '1':
			subscribe(user, conn)
			
			# conn.send('1' if userExists(username) else '0')
			
		elif option == '2':
			unsubscribe(user, conn, numFollowing)
		
		elif option == '~':
			return
		
		numFollowing = len(user.subscriptions)
		conn.send(str(numFollowing))

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
userList = []
onlineUsers = []

serverSetup()

# now we listen for any incoming connections
sock.listen(10)

print 'Socket now listening'

# Maybe make a admin thread????
	
while 1:
	# wait to accept a connection
	conn, clientAddr = sock.accept()
	onlineUsers.append(conn)	
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(clientAddr[1])

	# start a new thread
	start_new_thread(handleClient, (conn, clientAddr) )		

sock.close()
