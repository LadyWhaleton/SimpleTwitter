import socket
import struct
import os
import sys
import time
import datetime
import curses
import getpass
from common import *
from echo_connect import *
from thread import *

# https://www.youtube.com/watch?v=RXEOIAxgldw

def displayMenu(username, numUnread):

	print "~~~~~~~~~~~~~~~~~~~~~~~~~WhaleSpeak~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "                               ','. '. ; : ,','"
	print "                                 '..'.,',..'"
	print "                                    ';.'  ,'    Hello!"
	print "                                     ;;         /"
	print "                                     ;'	       /"
	print "                       :._   _.------------.___"
	print "               __      :__:-'                  '--."
	print "        __   ,'_.'    .'             ______________'."
	print "      /__'.-  /__.__..'          ^  .' .'  .'  _.-_.'"
	print "         '._                     .-': .' _.' _.'_.'"
	print "            '----'._____________.'_'._:_:_.-'--'"
	print username + ", you have " + str(numUnread) + " unread messages."
	print "1. See Offline Messages"
	print "2. Search by Hashtag"
	print "3. Edit Subscriptions"
	print "4. View Followers"
	print "5. Post a Message"
	print "6. Logout"

def displayFollowers(mySocket):
	os.system('clear')
	mySocket.send(FOLLOWERS)
	
	message = mySocket.recv(1024)
	print message
	
	if message == 'You have no followers!':
		return
		
	mySocket.send('OK')
		
	while True:
		msg = mySocket.recv(1024)
		mySocket.send('OK')
		
		if msg == 'STOP':
			return
		
		print msg	
	

def receiveMessages(mySocket):
	os.system('clear')
	msg = ""
	while ( msg != 'STOP'):
		msg = mySocket.recv(2048)
			
		# check if that were all of the messages
		if msg != 'STOP':
			print msg
			mySocket.send('OK')
		
	# send final acknowledgement
	mySocket.send('OK')
	
	# check if there weren't any messages to output
	msg = mySocket.recv(1024)
	if msg == 'good':
		return
	else:
		print msg
		
def viewBySubscription(mySocket, numFollowing):
	
	# display subscriptions if you are actually subscribed to stuff	
	displaySubscriptions(mySocket, numFollowing)
	
	while True:
		# select who to view messages from
		user = raw_input('Who do you want to hear Echoes from? (Pick by number): ')
		mySocket.send(user)
	
		check = mySocket.recv(1024)
		mySocket.send('OK')
		
		if check == '-1':
			print 'Error: Invalid selection!\n'
		else:
			break
			
	receiveMessages(mySocket)
		
	
def clientView(mySocket):
	mySocket.send(VIEW)
	os.system('clear')
	
	while True:
		numFollowing = int(mySocket.recv(1024))
		mySocket.send('OK')
	
		if numFollowing < 1:
			msg = mySocket.recv(1024)
			print msg
			mySocket.send('OK')
			return
		
 		print '1. View All'
		print '2. View by Subscription'
		print '~. Return to Menu'
		option = raw_input('What would you like to do?: ')		
		
		if option == '1':
			mySocket.send(option)
			receiveMessages(mySocket)
		elif option == '2':
			mySocket.send(option)
			viewBySubscription(mySocket, numFollowing)
		elif option == '~':
			mySocket.send(option)
			return	
		else: 
			print 'Error: Not a valid option! Please try again.'	
		

def clientSearch(mySocket):
	mySocket.send(SEARCH)
	
	while True:
 		os.system('clear')           
		tag = raw_input('What tag to search by?: ')
		mySocket.send(tag)
		
		receiveMessages(mySocket)
		
		# ask the user if they want to search again
		choice = raw_input('Search again? (y/n): ')
		mySocket.send(choice)
		
		# wait until server receives the choice
		mySocket.recv(1024)
		
		if choice != 'y' and choice != 'Y':
			break

def trySubscribe(mySocket):
	mySocket.send('1')	
	name = raw_input('Who do you want to subscribe to?: ')
	mySocket.send(name)
			
	# wait for server to validate user
	msg = mySocket.recv(1024)
	print msg
	
	mySocket.send('OK')

def displaySubscriptions(mySocket, numFollowing):
	for i in range(0, numFollowing):
		userFollowing = mySocket.recv(1024)
		print userFollowing
		mySocket.send('OK')	
			
def tryUnsubscribe(mySocket, numFollowing):
	mySocket.send('2')	
	
	# Display subscriptions
	displaySubscriptions(mySocket, numFollowing)
	
	# select who to unsubscribe from
	userToRemove = raw_input('Who do you want to unsubscribe from? (Pick by number): ')
	mySocket.send(userToRemove)
	
	msg = mySocket.recv(1024)
	
	if msg == 'unsubscribe check':
		choice = raw_input('Are you sure? (y/n): ')
		
		if choice == 'y' or choice == 'Y':
			mySocket.send(choice)
		else:
			mySocket.send('-1')
			
		msg2 = mySocket.recv(1024)
		print msg2
		
	else:
		print msg	
	
	
def clientEdit(mySocket):
	mySocket.send(EDIT)
	
	while True:
		# somehow it forever waits here
		numFollowing = int(mySocket.recv(1024))
		
		print 'You are subscribed to ' + str(numFollowing) + ' Whale(s).'
		
		print '1. Subscribe to a Whale'
		
		if numFollowing > 0:
			print '2. Unsubscribe from a Whale'
			
		print '~. Return to Menu'
		
		option = raw_input('What would you like to do?: ')
		
		if option == '1':
			trySubscribe(mySocket)
				
		elif option == '2' and numFollowing > 0:
			tryUnsubscribe(mySocket, numFollowing)		
		
		elif option == '~':
			mySocket.send('~')
			return
			
		else:
			print 'Error: Invalid option! Please try again.\n'
			mySocket.send('-1')

def clientPost(mySocket):
	mySocket.send(POST)
	
	# client needs to write stuff for message body
	while True:
		msg = raw_input ('Enter a message to Echo: ')
		if len(msg) <= 140:
			break
		else:
			print 'Error: Message must be 140 characters or less!'
			answer = raw_input ('Try again? (y/n): ')
			if answer != 'y' and answer != 'Y':
				mySocket.send('-1')
				return
	
	# client needs to create hashtags for this message
	tags = raw_input('Enter the tags (separated by space): ')
	
	# os.system('clear')
	print 'Message: ' + msg
	print 'Tags: ' + tags
	
	choice = raw_input('Are you sure you want to Echo this message? (y/n): ')
	if choice == 'y' or choice == 'Y':
		now = datetime.datetime.now()
		t = now.strftime("%I:%M %p") 
		timestamp = now.strftime("%b-%d-%Y %I:%M %p")
		timeval = now.strftime("%Y%m%d%H%M%S")

		mySocket.send(msg)
		
		# wait for acknowledgement (server received message body)
		if mySocket.recv(1024) == 'OK0':
			mySocket.send(tags)

		if mySocket.recv(1024) == 'OK1':
			mySocket.send(timestamp)

		if mySocket.recv(1024) == 'OK2':
			mySocket.send(timeval)

		# get verification that the message was received from the server
		
	else:
		print "Message was not Echo'd."
		mySocket.send('-1')
	
# clientside logout	
def clientLogout(mySocket):
	print "~~~~~~~~~~~~~~~~~~~~~~~~~WhaleSpeak~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "                               ','. '. ; : ,','"
	print "                                 '..'.,',..'"
	print "                                    ';.'  ,'    Goodbye!"
	print "                                     ;;         /"
	print "                                     ;'	       /"
	print "                       :._   _.------------.___"
	print "               __      :__:-'                  '--."
	print "        __   ,'_.'    .'             ______________'."
	print "      /__'.-  /__.__..'          =  .' .'  .'  _.-_.'"
	print "         '._                     .-': .' _.' _.'_.'"
	print "            '----'._____________.'_'._:_:_.-'--'"
	
	mySocket.send(LOGOUT)
	mySocket.close()
	
def login(mySocket):
	data = mySocket.recv(1024)
	print data

	loginSuccess = '0'

	while loginSuccess == '0':
		name = raw_input ("Username: ")
		mySocket.send(name)
		
		pw = getpass.getpass ("Password: ")
		mySocket.send(pw)

		data = mySocket.recv(1024)
		loginSuccess = data[0:1]
		num = data[2:]
		
		if loginSuccess == '0':
			print "Error: Invalid username / password!\n"
			
	print "Login successful!"
	
	return (name, int(num))

def handleEchoPort(unused):
	esock = connectEchoServer()
	
	while not(logOut):
		msg = esock.recv(2048)
		print msg
	
	esock.close()
	# thread.exit()
	return
	
# ========================== M A I N ===========================
host = ''
port = 2124

os.system ('clear')

try:
	sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1] 
	sys.exit()

# try to connect to the server
ret = sock.connect_ex ( (host, port))

if ret > 0:
	print 'Error: Unable to connect to server!'
	sys.exit()

# attempt to connect to echoServer
isEchoServerDown = False
esock = connectEchoServer()
if esock == -1:
	print "Echo Port is down. New messages will not be Echo'd."
	isEchoServerDown = True
else:
	start_new_thread(handleEchoPort, (" ", ))	


logOut = False

username, numUnread = login(sock)

while (not(logOut)):
	displayMenu(username, numUnread)
	optionNum = raw_input ("Which option to perform?: ")
	os.system ('clear')
	
	if optionNum == VIEW:
			clientView(sock)
			
	elif optionNum == SEARCH: 
			clientSearch(sock)
			
	elif optionNum == EDIT: 
			clientEdit(sock)
			
	elif optionNum == FOLLOWERS:
			displayFollowers(sock)
			
	elif optionNum == POST:
			clientPost(sock)
			
	elif optionNum == LOGOUT: 
			clientLogout(sock)
			logOut = True
			
	else:
			print 'Invalid option. Please try again.\n'

