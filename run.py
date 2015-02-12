#sys.path.append(os.path.abspath(pathfordroplet[:-1])) ###Uncomment when necessary###sys.path is where python checks when importing various modules

import sys
from sys import platform as _platform
import os
from threading import Thread
from collections import OrderedDict
from socket import *
from time import sleep, time

'''Variable Definitions start
'''

rport = 25555
sport = 25556
uri = sys.argv[-1]
running = True
send_size = 500

if _platform == "linux" or _platform == "linux2":
    hash_path = "/droplet/dpl/hashes"
    network_path = "/droplet/dpl/networks"
    pathfordroplet = "/droplet/"
elif _platform == "darwin":
    hash_path = "/droplet/dpl/hashes"
    network_path = "/droplet/dpl/networks"
    pathfordroplet = "/droplet/"
elif _platform == "win32":
    pathfordroplet = "C:/droplet/"
    hash_path = "C:/droplet/dpl/hashes.txt"
    network_path ="C:/droplet/dpl/networks.txt"
    ip_path = "C:/droplet/dpl/ip.txt"


if "sha1_hash" in uri:
	hash = uri.partition("=")[-1]
else:
	hash = "**HASH**"
	
if __name__=="__main__":	#If file is run directly from prompt and not imported
	print "\nSearching for file with hash :" + hash + '\n'

'''Function Definitions start
'''

def nafinder():				#Returns all possible network addresses
	try:
		file = open("C:/droplet/dpl/networks.txt", "r+")
	except:
		file = open("C:/droplet/dpl/networks.txt", "w+")
	networks = []
	data = "adf"
	while data != "":
		data = file.readline()
		data = data.strip(" \n")
		networks.append(data)
	print networks
	return networks[:-1]	#The last entry is blank : ''

def find(networks):		#Sends "alive" to all ip addresses using their network address as base
	for netip in networks:
		netbytes = netip.split(".")
		netbytes[-1] = 0
		receiver = socket(AF_INET, SOCK_DGRAM)
		tosend = str(netbytes[0]) + "." + str(netbytes[1]) + "." + str(netbytes[2]) + "."
		for i in xrange(1, 255):
			receiver.sendto("alive", (tosend + str(i), rport))
	print "Exit Find"
	running = False


def meet(drop_uri,send_hash):
	finder = socket(AF_INET, SOCK_DGRAM)
	finder.bind(('', sport))	
	start = time()
	data = "t"
	global running
	avail_ip=[]
	print "Loop started"
	while (time() - start) < 10 and running:
		try:
			finder.settimeout(10)
			data, addr = finder.recvfrom(1024)
			print data,
			print addr
		except:
			pass
		if "available" in data:
			recv_hash = data.split(":")[1]
			if recv_hash == send_hash:
				print "Hash Available"
				avail_ip.append(addr[0])
		try:
			addr
		except NameError:
			pass
		else:
			if data == "alive":
				finder.sendto(drop_uri,addr)
	print "Exit meet"
	finder.close()
	return avail_ip

def send_text(input):
		input_text = str(input)
		send_text = input_text + "-"*(send_size-len(input_text))
		return send_text

class downloader:  #Class to handle downloads.
	peers = []  	#List of socket objects
	if _platform == "linux" or _platform == "linux2":	#'path' where downloaded files go. 'path' is also 'self.path'?
		path = "/droplet/"
	elif _platform == "darwin":
		path = "/droplet/"
	elif _platform == "win32":
		path = "C:\\droplet_alpha\\"
	def __init__(self,ips,hash):
		self.hash = hash
		for ip in ips:
			try:
				s = socket()
				s.connect((ip,12345))
				self.peers.append(s)
			except:
				ips.remove(ip)
				if not ips:		#Checking if ips is empty
					print "No peers currently uploading file."
					sys.exit(0)
	def get_info(self):   	#Get the name, and size of the file using the hash
		info_send ="info" 	# Maybe we can get the name from the web server
		info_send = info_send + "-"*(send_size-len(info_send))
		self.peers[0].send(info_send)
		hash_send = self.hash + "-"*(send_size-len(self.hash))
		self.peers[0].send(hash_send)
		self.file_size = int(self.peers[0].recv(send_size).strip('-'))
		self.file_name = self.peers[0].recv(send_size).strip('-')
		print self.file_size," got info"
	
		
	def open_file(self):
		self.pieces = []													#Opens the file for writing
		self.piece_number = len(self.peers)									
		#Creates a list called pieces which stores start and stop 
		try:
			self.file = open(self.path + self.file_name,"rb+")					#positions for downloading the file in pieces
		except:
			self.file = open(self.path + self.file_name,"wb+")
		self.piece_size = int(self.file_size/len(self.peers))				# max size of each piece is 300 MB
		if(self.piece_size>314572800):
			self.piece_number=int(self.file_size/314572800)+1
			self.piece_size=314572800
		if(self.piece_number==1):
			self.pieces.append([0,self.file_size])
		else:
			for x in range(0,self.piece_number):
				self.pieces.append([x*self.piece_size,(x+1)*self.piece_size])
		
		self.pieces[-1][-1]=self.file_size
		print self.pieces
		return len(self.pieces)
	def down_file(self,id_num,peer_num=0):                              #gets the piece from a peer. 
		peer = self.peers[peer_num]										#pass the piece number and the peer number
		peer.send(send_text("init_download"))
		reply = peer.recv(send_size).strip('-')
		print reply
		if(reply=="ready"):
			start = self.pieces[id_num][0]
			end = self.pieces[id_num][1]
			
			size = end - start
			peer.send(send_text("seek"))
			peer.send(send_text(start))
			peer.send(send_text("size"))
			peer.send(send_text(size))
			print "send size"
		reply = peer.recv(send_size).strip('-')
		print reply
		if(reply == "willsend"):
			sleep(5)
			recieved = 0
			self.file.seek(start)
			print "Downloading ..."
			fileRecv = peer.recv(size)
			peer.settimeout(2)
			while (fileRecv):
				
				recieved+=len(fileRecv)
				self.file.write(fileRecv)
				try:
					fileRecv = peer.recv(size)
				except:
					break
		else:
			return 0


networks = nafinder()
i1 = Thread(target = find, args= (networks,))
i1.start()
ips= meet(uri,hash)
if(len(ips)<2):
	i2 = Thread(target = find, args = (networks,))
	i2.start()
	ips+= meet(uri,hash)
ips = list(OrderedDict.fromkeys(ips))	#To remove duplicates from ips
if len(ips)==0:
	print "No Peers Found"
	print "Please try again later, or contact an administrator if this problem persists"
	sleep(10)
	sys.exit(0)
else:
	getter = downloader(ips,hash)
	getter.get_info()
	num_pieces = getter.open_file()
	if(len(ips)>1):
		if not (getter.file_size==getter.get_info(1)):
			print "Error in syncing with other peers"
			print "Please contact an administrator if this problem persists"
			print "#Error in File Size Sync"
			sleep(10)
			sys.exit(0)
	peer_num = 0 
	for x in range(0,num_pieces):		
		Thread(target = getter.down_file(x,peer_num)).start()
		peer_num+=1
		if peer_num >= len(getter.peers):
			peer_num = 0 

			
			
			

#Example URI : drop:sha1_hash=6be88cd386da58689bbc1a16f6d08309ce5b5fae
#Example for shubh : drop:sha1_hash=680327857ee663080d77389be4497c2b68fca650		