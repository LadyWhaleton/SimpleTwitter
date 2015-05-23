from check import ip_checksum
import socket
import select
import sys
import time
from thread import*

class User:
	def __init__ (self, user, pw

def validateUser(username, pw):


# this is the server side
def make_pkt (seqNum, checksum):
	packet = str(seqNum) + checksum
	return packet

# this is main
HOST = ''
PORT = 2124
winSize = 4

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
	
while 1:
	data = []
	clientAddr = []

	# rdt_rcv(rcvpkt) transition
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
