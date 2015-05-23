from check import ip_checksum
import socket
import select
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
	userList.append( User ("pizza", "cheese")
	userList.append( User ("apple", "sauce")

def make_pkt (seqNum, checksum):
	packet = str(seqNum) + checksum
	return packet

# ======================== M A I N ===============================
HOST = ''
PORT = 2124

sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created'

# try to bind the socket
try:
	sock.bind ( (HOST, PORT) )
except socket.error , msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind success'

expectedseqnum = 0
oldPacket = ""
newPacket = ""
userList []

serverSetup()
	
while 1:
	data = []
	clientAddr = []

	data, clientAddr = sock.recvfrom (1024)
		
	if not data: 
		break

	print '\nMessage[' + clientAddr[0] + ':' + str(clientAddr[1]) + '] ' + data.strip()	
	checksum = data[1:3]
	newPacket = make_pkt (expectedseqnum, checksum)

	if oldPacket != newPacket:
		# send back the message so the client knows server got message
		oldPacket = newPacket
		sock.sendto (oldpacket, clientAddr)
		expectedseqnum += 1
	else:
		print "Error: Duplicate packet detected!"
		

sock.close()
