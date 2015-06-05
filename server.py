import socket
import struct
import string
import os
import sys
import time
from thread import *
import threading
from echo_connect import *
from common import *
from message import *
from users import *

# time.asctime(time.localtime(time.time()))
# http://python.readthedocs.org/en/latest/howto/curses.html

def setNewestUser(newUser):
	newestUser = newUser

def getNewestUser():
	return newestUser

# ================== Server setup related functions ==========================

def validateUser(conn, addr):
	
	validUser = False
	
	while not(validUser):
		username = conn.recv(1024)
		pw = conn.recv (1024)
		
		# if there's a user with that username in Userlist, don't short circuit
		# it the above if-statement is true, check if the pw is correct
		if UserList.has_key(username) and UserList[username].pw == pw:
			print 'Client ' + addr[0] + ':' + str(addr[1]) + ', ' + username + ' is authorized.'
			validUser = True
			msg = '1 ' + str(len(UserList[username].msg_unread))
			conn.send (msg) 
			return username

		print 'Client' + addr[0] + ':' + str(addr[1]) + ', ' + username + ' unauthorized user.'
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
	
	userList.append(USER1)
	userList.append(USER2)
	userList.append(USER3)
	userList.append(USER4)
	
	return s
			
def setupEchoer():
	host = ''
	port = 1338

	es = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	print 'Echo socket created'

	# try to bind the socket
	try:
		es.bind ( (host, port) )
	except socket.error , msg:
		print 'Echo bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Echo socket bind success'

	return es
	
# ===================== echo thread ===================================
def handleEchoPorts(unused):

	EchoSocket = setupEchoer()
	print 'Echo socket now listening'

	EchoSocket.listen(10)

	while not(SHUTDOWN):
		echoClient, echoClientAddr = EchoSocket.accept()
		
		# wait until there's a new user assigned
		event.wait()		

		print 'New user connected to Echo port!'
		UserList[recentlyConnected[0]].goOnline(echoClient) 	
	
	return
				
# ============================== server functions ======================

# serverside ViewOffline
def serverView(username, conn):
	print 'View Offline Messages'

def serverFindTag(tag, tagList):
	for t in tagList:
		if t == tag:
			return True
	return False

# serverside SearchByHashTag	
def serverSearch(username, conn):
	
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

def subscribe(username, conn):
	otherName = conn.recv(1024)
	
	val, msg = UserList[username].follow(otherName)
	waitForClientACK(conn, msg)
	
	return 

			
# determines whether or not the user exists	and does stuff
# used for Deleting a subscription	
def unsubscribe(username, conn, numFollowing):
	# send subscriptions
	for i in range(0, numFollowing):
		currUser = UserList[username].subscriptions[i]
		waitForClientACK(conn, str(i+1) + ". " + currUser)
	
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
		otherUser = UserList[username].subscriptions[int(userToRemove)-1]
		
		if clientChoice == 'y' or clientChoice == 'Y':
			# search user's list of subscriptions and remove
			
			UserList[username].unfollow(otherUser)
			UserList[otherUser].removeFollower(username)
			
			conn.send ('You are no longer following ' + otherUser + '.\n')
		else:
			conn.send('You are still following ' + otherUser + '.\n')
	
	else:
		conn.send('Error: Invalid selection!\n')
	
# serverside EditSubs
def serverEdit(username, conn):
	# send the number of people the user is subscribed to
	numFollowing = len(UserList[username].subscriptions)
	conn.send(str(numFollowing))
	
	# Loop 
	while True:
		# wait for client input
		option = conn.recv(1024)
		
		if option == '1':
			subscribe(username, conn)
			 
			# conn.send('1' if userExists(username) else '0')
			
		elif option == '2':
			unsubscribe(username, conn, numFollowing)
		
		elif option == '~':
			return
		
		numFollowing = len(UserList[username].subscriptions)
		conn.send(str(numFollowing))

def distributeEchos(poster, newMessage):
	list_items = UserList.items()
	for user in list_items:
		username = user[0]

		# if the user is offline and isn't the poster
		if poster != username and UserList[username].status == OFFLINE:
			print username + ' is offline.'
			
			# if the user is offline and follows the poster, add to unread messages
			if UserList[username].isFollowing(poster):
				print username + ' is following ' + poster + ' and is offline.'
				UserList[username].addUnread(newMessage)

		# if the user is online and isn't the poster
		elif poster != username and UserList[username].status == ONLINE:
			print username + 'is online.'

			# if the user is online and follows the poster, broadcast
			if UserList[username].isFollowing(poster):
				print username + ' is following ' + poster + ' and is online.'
				followerPort = UserList[username].port
				follwerPort.send (newMessage.formatMessage())


def serverPost(username, conn):
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
	newMessage = Message(username, msg, tags, tagList, timestamp, int(timeval))

	messageList.insert(0, newMessage)
	UserList[username].addMyEcho(newMessage)
	
	distributeEchos(username, newMessage)
	
	# notify echo server if it's up
	if not(isEchoServerDown):
		esock.send('\nBROAAADDDCAAASSSSSTTTTT\n')

# serverside logout
def serverLogout(username, conn, addr):
	UserList[username].goOffline()
	print username + " is logging out."
	conn.close()
	
def handleClient(conn, addr):
	# Sending message to client
	conn.send ('Please log in.')
	
	# Validate the user and login if validated
	event.clear()
	currUser = validateUser(conn, addr)
	recentlyConnected.insert(0, currUser)
	# set global flag
	event.set()
	event.clear()
	
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
# esock = connectEchoServer()
esock = -1
if esock == -1:
	print 'Echo Server is down. Some functionalities will be disabled.'
	isEchoServerDown = True	

messageList = []
userList = []
onlineUsers = []
recentlyConnected  = []

event = threading.Event()

sock = setupServer()
sock.listen(10)
print 'Server socket now listening'
print '~~~~~~~~~~~~~~~~~~~~~'

start_new_thread(handleEchoPorts, (" ", ))

# Maybe make a admin thread????
	
while 1:
	# wait to accept a connection
	conn, clientAddr = sock.accept()
	onlineUsers.append(conn) #maybe we want to append this somewhere else..
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(clientAddr[1])

	# start a new thread
	start_new_thread(handleClient, (conn, clientAddr) )		

sock.close()
