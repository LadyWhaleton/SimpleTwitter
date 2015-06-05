import socket

def connectEchoServer():
	echoHost = ''
	echoPort = 1338
	
	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create Echo socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1] 
		return -1
	
	# try to connect to the echo server
	ret = s.connect_ex ( (echoHost, echoPort))
	
	if ret > 0:
		print 'Error: Unable to connect to Echo server!'
		return -1
	
	return s

