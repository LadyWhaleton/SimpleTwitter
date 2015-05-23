import socket
import sys
import time




# ========================== M A I N ===========================
host = ''
port = 2124

try:
	sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1] 
	sys.exit();

# try to connect to the server
ret = sock.connect_ex ( (host, port))

if ret > 0:
	print 'Error: Unable to connect to server!'
	exit(0)

while (1):
	msg = "hi"	
				

# now we close the socket
sock.close()
