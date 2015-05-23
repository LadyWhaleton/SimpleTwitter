import socket
import sys
import time

def login(mySocket):
	data = mySocket.recv(1024)
	print data

	loginSuccess = 0

	while loginSuccess == 0:
		username = raw_input ("Username: ")
		pw = raw_input ("Password: ")

		mySocket.send(username)
		mySocket.send(pw)

		loginSuccess = mySocket.recv(1024)
		
		if not(loginSuccess):
			print "Error: Invalid username / password!\n"
	


# ========================== M A I N ===========================
host = ''
port = 2124

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

login(sock)

# while (1):


# now we close the socket
sock.close()
