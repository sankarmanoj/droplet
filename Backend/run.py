#sys.path.append(os.path.abspath(pathfordroplet[:-1])) ###Uncomment when necessary###sys.path is where python checks when importing various modules
#Hash passed must be like : drop:sha1_hash=78715ff4b5ae858dcaf797efefe364e4861a380b?version=1

import cPickle
import collections
import csv
import os
import subprocess
import sys
import threading
import time
from socket import *

'''Variable Definitions start
'''

Release_Version = "1"


rport = 25555
sport = 25556
uri = sys.argv[-1]
running = True
send_size = 500
if sys.platform == "win32":
	pathfordroplet = "C:/droplet/"
	system_folder = "C:\\Program Files (x86)\\droplet\\"
	hash_path =  "C:\\droplet\\config\\hashes"
	network_path = "C:\\droplet\\config\\networks"
else:
		print "Platform Not Supported"
		print "Multi-platform support will be added soon"
		print "Contact us for further information"
		time.sleep(10)
		sys.exit(0)


if "sha1_hash" in uri:
	hash = uri.partition("?")[0].partition("=")[-1]
	current_version=uri.partition("?")[-1].partition("=")[-1]
	print "Current Version ",current_version
	print hash
	hashes = cPickle.load(open(hash_path,"rb+"))
	for hasha in hashes:
		if hasha[0] == hash:
			path = hasha[1]
			name = os.path.split(path)[-1]
			print "\nThe file is already available at : "+path
			print "The movie's name as stored by you is : "+name.partition(".")[0]
			time.sleep(10)
			sys.exit(0)
	if current_version != Release_Version:
		
		print " Please Update "
		print " This is not the latest version"
		time.sleep(10)
		sys.exit(0)
else:
	print "Hash not received"
	print "Exiting Program"
	time.sleep(3)
	sys.exit(0)
	
'''Function Definitions start
'''
def check_sender():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	num =0
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'sender.exe':
			num+=1
	if num ==1:
		return True
	elif num ==0:
		return False
	else:
		subprocess.call('taskkill /f /im sender.exe',shell = True, stdout=subprocess.PIPE)
		return False
def nafinder():				#Returns all possible network addresses
	try:
		file = open(network_path, "r+")
	except:
		print "Error - Networks file not found"
		print "Please create a file called 'networks' in the directory ",system_folder
		print "Contact us if the problem persists"
		for x in range(0,10):
			print ".",
			time.sleep(1)
		sys.exit(0)
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
	start = time.time()
	data = "t"
	global running
	avail_ip=[]
	print "Loop started"
	while (time.time() - start) < 10 and running:
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
	path=pathfordroplet
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
	def get_info(self,peer_num=0):   	#Get the name, and size of the file using the hash
		info_send ="info" 	# Maybe we can get the name from the web server
		info_send = info_send + "-"*(send_size-len(info_send))
		self.peers[peer_num].send(info_send)
		hash_send = self.hash + "-"*(send_size-len(self.hash))
		self.peers[peer_num].send(hash_send)
		self.file_size = int(self.peers[peer_num].recv(send_size).strip('-'))
		if(self.file_size==0):
			print "File Not available"
		self.file_name = self.peers[peer_num].recv(send_size).strip('-')
		
		print self.file_size," got info"
		return self.file_size
	
		
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
			time.sleep(5)
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

version = "0"
ver_cnt = socket(SOCK_DGRAM,AF_INET)
addr = ("localhost",rport)
times = 0
ver_cnt.settimeout(0.5)

os.startfile(os.path.join(os.getcwd(),"droplet.exe"))

while True:
	if times > 5:
		break
	try:
		ver_cnt.sendto("vrequest",addr)
		version,addr = ver_cnt.recvfrom(100)
		if version=="-1":
			print "There is a fatal error in the code that is never expected to happen. Please contact an administrator and say ERROR IN RUN. It is very important to correct this error now and in further releases"
			time.sleep(10)
			sys.exit(0)
		if version ==Release_Version:
			break
	except:
		if not check_sender():
			os.startfile(os.path.join(os.getcwd(),"droplet.exe"))
			time.sleep(0.5)
	times +=1
	
if version==current_version:
	networks = nafinder()
	i1 = threading.Thread(target = find, args= (networks,))
	i1.start()
	ips= meet(uri,hash)
	if(len(ips)<2):
		i2 = threading.Thread(target = find, args = (networks,))
		i2.start()
		ips+= meet(uri,hash)
	ips = list(collections.OrderedDict.fromkeys(ips))	#To remove duplicates from ips
	if len(ips)==0:
		print "No Peers Found"
		print "Please try again later, or contact an administrator if this problem persists"
		time.sleep(10)
		sys.exit(0)
	else:
		getter = downloader(ips,hash)
		getter.get_info()
		temp=getter.file_size
		num_pieces = getter.open_file()
		if(len(ips)>1):
			if not (temp==getter.get_info(1)):
				print "Error in syncing with other peers"
				print "Please contact an administrator if this problem persists"
				print "#Error in File Size Sync"
				time.sleep(10)
				sys.exit(0)
		peer_num = 0 
		for x in range(0,num_pieces):		
			threading.Thread(target = getter.down_file(x,peer_num)).start()
			peer_num+=1
			if peer_num >= len(getter.peers):
				peer_num = 0
else:
	print "CRITICAL ERROR... Please install the latest version of Droplet."