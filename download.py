from socket import *
from threading import Thread
from time import sleep,time
s= socket()
port = 12345
send_size = 500
def send_text(input):
		input_text = str(input)
		send_text = input_text + "-"*(send_size-len(input_text))
		return send_text
class downloader:
	peers = []
	path = "C:\\droplet_alpha\\"
	
	def __init__(self,ips,hash):
		self.hash = hash
		for ip in ips:
			try:
				s = socket()
				s.connect((ip,12345))
				s.settimeout(15)
				self.peers.append(s)
			except:
				ips.remove(ip)
	
	def get_info(self):
		info_send ="info"
		info_send = info_send + "-"*(send_size-len(info_send))
		self.peers[0].send(info_send)
		hash_send = self.hash + "-"*(send_size-len(self.hash))
		self.peers[0].send(hash_send)
		self.file_size = int(self.peers[0].recv(send_size).strip('-'))
		self.file_name = self.peers[0].recv(send_size).strip('-')
		print self.file_size," got info"
	
		
	def open_file(self):
		self.pieces = []
		self.piece_number = len(self.peers)
		self.file = open(self.path + self.file_name,"ab")
		self.piece_size = int(self.file_size/len(self.peers))
		if(self.piece_size>314572800):
			self.piece_number=int(self.file_size/314572800)+1
			self.piece_size=314572800
		for x in range(0,self.piece_number):
			self.pieces.append([x*self.piece_size,(x+1)*self.piece_size])
		if(self.piece_number==1):
			self.pieces.append([0,self.file_size])
		self.pieces[-1][-1]=self.file_size
		print self.pieces
	def down_file(self,id_num,peer_num=0):
		peer = self.peers[peer_num]
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
	
	def __del__(self):
		quit_send = "quit"+"-"*(send_size-4)
		for peer in self.peers:
			peer.send(quit_send)
	
ips = ["192.168.0.3",]
hash = "812b7aa67bfda826d1520d285864113d0452c774"
file1 = downloader(ips,hash)
file1.get_info()

print file1.file_name
print file1.file_size
file1.open_file()
file1.down_file(1)
		
	