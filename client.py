import socket
import struct
import os
import sys
import time
import curses
import getpass
from common import *

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
	print "4. Post a Message"
	print "5. Logout"

	
def clientView(mySocket):
	mySocket.send(VIEW)
	print "Viewing offline messages"

def clientSearch(mySocket):
	mySocket.send(SEARCH)
	print 'Searching by hashtags'
	
def clientEdit(mySocket):
	mySocket.send(EDIT)
	numFollowing = int(mySocket.recv(1024))
	
	while True:
		
		os.system ('clear')
		print 'You are subscribed to ' + str(numFollowing) + ' whales.'
		
		print '1. Subscribe to a Whale'
		
		if numFollowing > 0:
			print '2. Unsubscribe a Whale'
			
		print '~. Return to Menu'
		
		option = raw_input('What would you like to do?: ')
		
		if option == '1':
			name = raw_input('Who do you want to subscribe to?: ')
			mySocket.send(name)
			
			# wait for server to validate user
			tempflag = mySocket.recv(1024)
			
			if tempFlag == '1':
				
			
		elif option == '2' and numFollowing > 0:
			# Display subscriptions
			for i in range(0, numFollowing):
				
		
		elif option == '~':
			return
			
		else:
			print 'Error: Invalid option! Please try again.'
	
	
	
def clientPost(mySocket):
	print 'Create a message'

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
		pw = raw_input ("Password: ")

		mySocket.send(name)
		mySocket.send(pw)

		data = mySocket.recv(1024)
		loginSuccess = data[0:1]
		num = data[2:]
		
		if loginSuccess == '0':
			print "Error: Invalid username / password!\n"
			
	print "Login successful!"
	
	return (name, int(num))

# ========================== M A I N ===========================
host = ''
port = 2124

os.system ('clear')

try:
	sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1] 
	sys.exit();

# try to connect to the server
ret = sock.connect_ex ( (host, port))

if ret > 0:
	print 'Error: Unable to connect to server!'
	exit(0)
	
logOut = False

username, numUnread = login(sock)

# http://stackoverflow.com/questions/16790725/sending-file-from-server-to-client-python
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
			
	elif optionNum == POST:
			clientPost(sock)
			
	elif optionNum == LOGOUT: 
			clientLogout(sock)
			logOut = True
			
	else:
			print 'Invalid option. Please try again.'

