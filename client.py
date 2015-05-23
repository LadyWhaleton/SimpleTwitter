from check import ip_checksum
import socket
import select
import sys
import time

# this is the code for the client
# in rdt3.0, the client is the sender in this case
def isSameChecksum (old, new):
	if old != new:
		print "Error: Invalid checksum!"

def make_pkt(seqNum, msg, checksum):
	packet = str(seqNum) + checksum + msg[seqNum]
	return packet

def getacknum(packet):
	acknum = packet[0:1]

# -----------------------------------------------------------
# this is main

try:
	sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1] 
	sys.exit();

host = ''
port = 2124


base = 0
nextseqnum = 0
timeOut = False

while (1):
	
	if not(timeOut):
		checksum = ip_checksum (msg)
		packet = make_pkt (nextseqnum, msg, checksum)
		sock.sendto (packet, (host, port))
		
	# select
	inputs = [sock]
	outputs = []
	timeout = 5
	readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
	
	data = []
	serverAddr = []	

	for tempSocket in readable:
		data, serverAddr = tempSocket.recvfrom(2048)
		print 'Message[' + serverAddr[0] + ':' + str(serverAddr[1]) + '] ' + data.strip()
		isSameChecksum (data[1:3],checksum)
		timeOut = False	
	
	# handle timeouts here (slide 48 from lecture 5-6-7)	
	if not data:
		print "Error: Timed out! Resending packet!"
		packet = make_pkt(nextseqnum, msg, checksum)
		sock.sendto (packet, (host, port))
		timeOut = True
		
	
	if not(timeOut):	
		nextseqnum += 1
		

# now we close the socket
sock.close()
