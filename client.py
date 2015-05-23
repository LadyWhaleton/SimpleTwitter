import socket
import struct
import os
import sys
import time
import getpass

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
	print "2. Edit Subscriptions"
	print "3. Post a Message"
	print "4. Logout"
	
def logout(mySocket):
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
	
	if optionNum == '1':
			print 'Offline messages'
	elif optionNum == '2': 
			print 'Edit Subscriptions'
	elif optionNum == '3': 
			print 'Post a message'
	elif optionNum == '4': 
			logout(sock)
			logOut = True
	else:
			print 'Invalid option. Please try again.'

