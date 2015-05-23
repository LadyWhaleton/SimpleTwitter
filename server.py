import socket
import sys
import time
from thread import*

# time.asctime(time.localtime(time.time()))

class User:
	def __init__ (self, user, pw):
		self.user = user
		self.pw = pw
		self.subs = []
		self.msg_read = []
		self.msg_unread = []

def validateUser(username, pw):
	for user in User:
		if user.username == username and user.pw == pw:
			return true

	return false
	
# initializes list of users
def serverSetup():
	userList.append( User ("abc", "abc") )
	userList.append( User ("pizza", "cheese") )
	userList.append( User ("apple", "sauce") )

def handleClient(conn):
	# Sending message to client
	conn.send ('Welcome to SimpleTwitter. Please log in.\nUsername: ')

	while 1:
		data = conn.recv(1024)
		if not data:
			break

		if ( data[0:12] == "Send to all:"):
			for client in clientList:
				reply = "OK..." + data[12:]
				client.send(replt)
		else:
			reply = "OK..." + data
			conn.sendall (reply)

	conn.close()

# ======================== M A I N ===============================
HOST = ''
PORT = 2124

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
oldPacket = ""
newPacket = ""
userList = []
onlineUsers = []
clientList = []

serverSetup()

# now we listen for any incoming connections
sock.listen(10)

print 'Socket now listening'
	
while 1:
	# wait to accept a connection
	conn, clientAddr = sock.accept()
	clientList.append(conn)	
	
	# display client info
	print 'Connected with ' + clientAddr[0] + ':' + str(addr[1])

	# start a new thread
	start_new_thread(handleClient, (conn,) )		

sock.close()
