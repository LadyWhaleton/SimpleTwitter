import socket
import struct
import string
import os
import sys
import time
from thread import*

def handleBroadcasts(unused):
	while True:
		msg = serverConn.recv(1024)
		
		if msg == SHUTDOWN:
			break
		
		for conn in onlineUsers:
			conn.send(msg)
	
	for clientConn in onlineUsers:
		conn.close()
	
	killServer = True	
	thread.exit()		

# ============================= MAIN =========================

HOST = ''
PORT = 1337

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

# now we listen for any incoming connections
sock.listen(10)

print 'Socket now listening'

# wait for server to connect
serverConn, serverAddr = sock.accept()
print 'Server connected at ' + serverAddr[0] + ':' + str(serverAddr[1])

onlineUsers = []
killServer = False

# start a new thread that will actually do the broadcasts
start_new_thread(handleBroadcasts, (" ", ))
	
while not(killServer):
	# wait to accept a connection
	clientConn, clientAddr = sock.accept()
	onlineUsers.append(clientConn)	
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(clientAddr[1])		

sock.close()
