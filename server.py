import socket
import struct
import string
import os
import sys
import time
from thread import *
from echo_connect import *
from common import *

# time.asctime(time.localtime(time.time()))
# http://python.readthedocs.org/en/latest/howto/curses.html

# ================== Server setup related functions ==========================
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
def setupServer():
	HOST = ''
	PORT = 2124

	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	print 'Server socket created'

	# try to bind the socket
	try:
		s.bind ( (HOST, PORT) )
	except socket.error , msg:
		print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Server socket bind success'
	
	userList.append( User ("abc", "abc") )
	userList.append( User ("pizza", "cheese") )
	userList.append( User ("apple", "sauce") )
	
	return s
			
def setupEchoer():
	HOST = ''
	PORT = 1337

	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	print 'Echo socket created'

	# try to bind the socket
	try:
		s.bind ( (HOST, PORT) )
	except socket.error , msg:
		print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Echo socket bind success'
	
# ===================== echo thread ===================================
def handleEchoes(unused):
	print 'doing nothing atm'
	
	while not(SHUTDOWN):
		x = 0
	
	thread.exit()
				
# ============================== other functions ======================

# serverside ViewOffline
def serverView(user, conn):
	print 'View Offline Messages'

def serverFindTag(tag, tagList):
	for t in tagList:
		if t == tag:
			return True
	return False

# serverside SearchByHashTag	
def serverSearch(user, conn):
	
	while True:
		tag = conn.recv(1024)
		length = len(messageList)
		
		ctr = 0
		for i in range(length):
			if ctr == 10:
				break
			
			message = messageList[i]
			tagFound = serverFindTag(tag, message.tagList)
			
			if tagFound:
				waitForClientACK(conn, str(ctr+1) + '. ' + message.formatMessage())
				ctr += 1
		
		# wait for final acknowledgement indicating user received all messages
		waitForClientACK(conn, 'STOP')
		
		# check if ctr was zero (no messages with the tag)
		if ctr == 0:
			conn.send('none')
		else:
			conn.send('good')
		
		clientChoice = conn.recv(1024)
		conn.send('OK') # send ack
		# if user doesn't want to search again, break
		if clientChoice != 'y' and clientChoice != 'Y':
			break

def waitForClientACK(conn, msg):
	conn.send(msg)
	
	while True:
		if conn.recv(1024) == 'OK':
			return

def subscribe(user, conn):
	otherName = conn.recv(1024)
	
	# you can't subscribe to yourself!
	if user.username == otherName:
		waitForClientACK(conn, 'Error: You cannot subscribe to yourself!\n')
		return
	
	for subUser in userList:
		# if the subcription username exists
		if subUser.username == otherName:
			# check the user already subscribed to this person
			
			for subName in subUser.subscriptions:
				# if the name already exists in the list of subs, return
				if subName == otherName:
					waitForClientACK(conn, 'Error: ' + user.username + ' already subscribed to' + otherName +'\n') 
					return
					
			# only arrive here if otherName isn't in sublist, OK to subscribe
			user.subscriptions.append(otherName)
			waitForClientACK(conn, 'Successfully subscribed to ' + otherName + '\n')
			return
	
	waitForClientACK(conn, 'Error: ' + otherName + ' does not exist!\n')

			
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
	
	# check if the user inputted the appropriate number
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
	msg = conn.recv(2048)
	
	if msg == '-1':
		return
	
	# send OK0 to client indicating server got message
	conn.send('OK0')

	tags = conn.recv(1024)
	conn.send('OK1') # server got tags from client

	timestamp = conn.recv(1024)
	conn.send('OK2') # server got timestamp from client

	timeval = conn.recv(1024)

	tagList = tags.split()
	newMessage = Message(user.username, msg, tags, tagList, timestamp, int(timeval))

	# messageList.append(newMessage)
	messageList.insert(0, newMessage)
	
	# notify echo server if it's up
	if not(isEchoServerDown):
		esock.send('\nBROAAADDDCAAASSSSSTTTTT\n')

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
os.system('clear')

SHUTDOWN = False
isEchoServerDown = False
esock = connectEchoServer()
if esock == -1:
	print 'Echo Server is down. Some functionalities will be disabled.'
	isEchoServerDown = True	

messageList = []
userList = []
onlineUsers = []
offlineUsers = []

sock = setupServer()
print '~~~~~~~~~~~~~~~~~~~~~~'
esock = setupEchoer()
start_new_thread(handleEchoes, (" ", ) )

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
esock.close()
